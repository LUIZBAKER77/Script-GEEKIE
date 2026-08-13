from __future__ import annotations

import argparse
import time
from pathlib import Path

from openpyxl import Workbook, load_workbook
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import geekie_automation as g


def page_text(driver):
    return g.normalize_text(g.normalize_ascii(driver.page_source))


def visible_page_text(driver):
    return g.normalize_text(g.normalize_ascii(driver.execute_script("return document.body?.innerText || ''")))


def expected_class_parts(class_code):
    grade, letter, _ = g.class_parts(class_code)
    return grade, letter


def login_for_audit(driver, email):
    g.ensure_one_logged_out(driver)
    driver.get(g.ONE_URL)
    visible = g.open_one_login(driver)
    if len(visible) < 2:
        raise RuntimeError("campos de login nao encontrados")
    g.fill_field(driver, visible[0], email)
    password_fields = [field for field in visible if g.normalize_text(field.get_attribute("type")) == "password"]
    pw_field = (password_fields or visible[1:])[-1]
    g.fill_field(driver, pw_field, g.PASSWORD)
    g.click_enabled_contains(driver, "Acessar", 10)
    start = time.time()
    invalid_markers = (
        "usuariosenha invalidos",
        "usuariosenha invalido",
        "usuario senha invalidos",
        "usuario senha invalido",
        "usuario ou senha invalidos",
        "usuario ou senha invalido",
        "senha invalida",
        "senha invalid",
        "credenciais invalid",
    )
    while time.time() - start < 30:
        text = f"{visible_page_text(driver)} {page_text(driver)}"
        if any(marker in text for marker in invalid_markers) or (
            "invalid" in text and ("senha" in text or "usuario" in text)
        ):
            raise RuntimeError("Usuario/Senha invalidos")

        login_title = "acessar com uma conta geekie one" in text
        login_option = driver.find_elements(By.XPATH, "//*[normalize-space()='Com uma conta Geekie One']")
        login_button = driver.find_elements(By.XPATH, "//*[normalize-space()='Acessar']")
        visible_inputs = [field for field in driver.find_elements(By.CSS_SELECTOR, "input") if field.is_displayed()]
        login_form = driver.execute_script(
            """
            const norm = (value) => (value || '')
              .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
              .replace(/[^a-zA-Z0-9\\s]/g, '')
              .replace(/\\s+/g, ' ').trim().toLowerCase();
            const visible = (el) => {
              const r = el.getBoundingClientRect();
              const st = getComputedStyle(el);
              return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
            };
            const inputs = [...document.querySelectorAll('input')].filter(visible);
            const hasUser = inputs.some((el) => norm(el.placeholder || el.getAttribute('aria-label') || '').includes('usuario')
              || norm(el.placeholder || el.getAttribute('aria-label') || '').includes('email'));
            const hasPassword = inputs.some((el) => (el.type || '').toLowerCase() === 'password'
              || norm(el.placeholder || el.getAttribute('aria-label') || '').includes('senha'));
            return hasUser && hasPassword;
            """
        )
        still_on_login = login_title or bool(login_option) or bool(login_form) or (len(visible_inputs) >= 2 and bool(login_button))

        if not still_on_login and "aproveite o geekie one" not in text:
            return
        if time.time() - start > 8 and still_on_login:
            raise RuntimeError("Usuario/Senha invalidos ou login nao avancou")
        time.sleep(0.4)

    raise RuntimeError("login nao avancou; possivel Usuario/Senha invalidos")


def audit_current_account(driver, class_code):
    text = page_text(driver)
    visible_update = driver.execute_script(
        """
        const norm = (value) => (value || '')
          .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
          .replace(/[^a-zA-Z0-9\\s]/g, '')
          .replace(/\\s+/g, ' ').trim().toLowerCase();
        const visible = (el) => {
          const r = el.getBoundingClientRect();
          const st = getComputedStyle(el);
          return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
        };
        return [...document.querySelectorAll('h1, h2, h3, div, span')]
          .some((el) => visible(el) && norm(el.innerText || el.textContent) === 'atualizacao das informacoes');
        """
    )
    if visible_update:
        return "ERRO", "login abriu tela de atualizacao das informacoes"

    grade, letter = expected_class_parts(class_code)
    deadline = time.time() + 20
    while time.time() < deadline:
        last_text = visible_page_text(driver)
        if (
            "voce esta em qual turma" in last_text
            or "selecione a turma" in last_text
            or "selecionar turma" in last_text
        ):
            return "ERRO", f"pede selecao de turma; esperado {grade}{letter}"
        has_grade = grade in last_text
        has_letter = letter.lower() in last_text
        has_material = any(token in last_text for token in ("material", "turma", "serie", "série"))
        if has_grade and has_letter and has_material:
            return "OK", f"turma encontrada: {grade}{letter}"
        time.sleep(1)

    return "ERRO", f"turma esperada nao confirmada: {grade}{letter}"


def run(args):
    workbook_path = Path(args.workbook).resolve()
    wb = load_workbook(workbook_path, data_only=True)
    sheet_indexes = parse_sheet_indexes(args.sheet_indexes, args.sheet_index)

    out = Workbook()
    out_ws = out.active
    out_ws.title = "Auditoria Geekie"
    out_ws.append(["aba", "linha", "nome", "email", "usuario_planilha", "codigo", "turma", "resultado", "detalhe"])

    driver = g.new_driver()
    try:
        for sheet_index in sheet_indexes:
            ws = g.resolve_sheet(wb, args.sheet, sheet_index)
            first_data_row, columns = g.detect_layout(ws)
            start_row = max(args.start, first_data_row)
            print(f"=== Auditando aba {sheet_index}: {ws.title} ===")
            for row in range(start_row, ws.max_row + 1):
                name = ws[f"{columns['name']}{row}"].value
                email = ws[f"{columns['email']}{row}"].value
                username = ws[f"{columns['username']}{row}"].value
                code = ws[f"{columns['code']}{row}"].value
                class_code = ws[f"{columns['class_code']}{row}"].value
                if not name and not email:
                    continue
                print(f"[{ws.title} linha {row}] auditando {name}")
                if not email:
                    out_ws.append([ws.title, row, name, email, username, code, class_code, "ERRO", "sem email"])
                    continue
                if not code:
                    out_ws.append([ws.title, row, name, email, username, code, class_code, "PULADO", "sem codigo do material"])
                    continue
                try:
                    login_for_audit(driver, str(email))
                    result, detail = audit_current_account(driver, str(class_code))
                    out_ws.append([ws.title, row, name, email, username, code, class_code, result, detail])
                    print(f"{result}: {detail}")
                except Exception as exc:
                    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
                    detail = lines[0] if lines else type(exc).__name__
                    if detail.lower() in {"message:", "message"}:
                        detail = type(exc).__name__
                    out_ws.append([ws.title, row, name, email, username, code, class_code, "ERRO", detail])
                    print(f"ERRO: {detail}")
                finally:
                    try:
                        g.logout(driver)
                    except Exception:
                        pass
                    out.save(args.output)
    finally:
        driver.quit()
        out.save(args.output)
    print(f"Auditoria salva em: {args.output}")


def parse_sheet_indexes(raw_indexes, fallback_index):
    if raw_indexes:
        indexes = []
        for part in str(raw_indexes).split(","):
            part = part.strip()
            if part:
                indexes.append(int(part))
        if indexes:
            return indexes
    if fallback_index:
        return [fallback_index]
    return [4, 5]


def main():
    parser = argparse.ArgumentParser(description="Auditoria Geekie One")
    parser.add_argument("workbook")
    parser.add_argument("--sheet", default="9º Anos - Geekie")
    parser.add_argument("--sheet-index", type=int, help="Audita uma aba unica pelo indice.")
    parser.add_argument("--sheet-indexes", default="4,5", help="Indices das abas separados por virgula. Padrao: 4,5 (9 ano e 3a serie).")
    parser.add_argument("--start", type=int, default=2)
    parser.add_argument("--output", default="auditoria_geekie_resultado.xlsx")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
