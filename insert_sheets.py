import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import calendar

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "SUA_PLANILHA_ID_AQUI"
ENTIDADES_JSON = "entidades.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

def nome_aba_atual(data: date) -> str:
    meses = ["jan", "fev", "mar", "abr", "mai", "jun",
             "jul", "ago", "set", "out", "nov", "dez"]
    return f"{meses[data.month - 1]}/{str(data.year)[2:]}"

def proxima_aba(data: date) -> str:
    ano = data.year
    mes = data.month + 1
    if mes > 12:
        mes = 1
        ano += 1
    meses = ["jan", "fev", "mar", "abr", "mai", "jun",
             "jul", "ago", "set", "out", "nov", "dez"]
    return f"{meses[mes - 1]}/{str(ano)[2:]}"

def preparar_nova_aba(planilha, aba_nome_atual, aba_nome_nova):
    aba_atual = planilha.worksheet(aba_nome_atual)

    nova_aba = planilha.duplicate_sheet(aba_atual.id, new_sheet_name=aba_nome_nova)

    todas_linhas = nova_aba.get_all_values()
    if len(todas_linhas) > 3:
        ultima_linha = len(todas_linhas)
        nova_aba.delete_rows(4, ultima_linha)

def inserir_gasto():
    planilha = gc.open_by_key(SPREADSHEET_ID)

    hoje = date.today()
    aba_nome = nome_aba_atual(hoje)

    if hoje.day >= 26:
        aba_nome_nova = proxima_aba(hoje)
        try:
            planilha.worksheet(aba_nome_nova)
        except gspread.exceptions.WorksheetNotFound:
            preparar_nova_aba(planilha, aba_nome, aba_nome_nova)
        aba_nome = aba_nome_nova

    aba = planilha.worksheet(aba_nome)

    with open(ENTIDADES_JSON, "r", encoding="utf-8") as f:
        entidades = json.load(f)

    nova_linha = [entidades["data"], entidades["local"], entidades["valor"], entidades["categoria"]]
    aba.append_row(nova_linha, value_input_option="USER_ENTERED")

    print(f"Gasto inserido na aba '{aba_nome}': {nova_linha}")

if __name__ == "__main__":
    inserir_gasto()
