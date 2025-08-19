import re
import json
from datetime import date

CATEGORIAS = ["CARTAO", "ALUGUEL", "COMIDA", "MERCADO", "ROLES", "OUTROS", "COMBUSTIVEL", "CONTAS"]

def processar_frase(frase: str):
    resultado = {
        "frase": frase,
        "valor": None,
        "local": "Desconhecido",
        "data": str(date.today()),
        "categoria": "OUTROS"
    }

    padrao_valor = re.search(r"(\d+[,.]?\d*)\s*(reais|rs|r\$)?", frase, re.IGNORECASE)
    if padrao_valor:
        valor_str = padrao_valor.group(1).replace(",", ".")
        try:
            resultado["valor"] = float(valor_str)
        except ValueError:
            pass

    for cat in CATEGORIAS:
        if cat.lower() in frase.lower():
            resultado["categoria"] = cat
            break

    tokens = frase.split()
    valor_idx = padrao_valor.start() if padrao_valor else len(frase)
    categoria_idx = min([frase.lower().find(cat.lower()) for cat in CATEGORIAS if cat.lower() in frase.lower()] + [len(frase)])
    possivel_local = frase[:min(valor_idx, categoria_idx)].strip()

    if possivel_local:
        resultado["local"] = possivel_local

    return resultado

if __name__ == "__main__":
    with open("transcricao.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    frase = data["resultados"][0]["alternativas"][0]["transcricao"]

    print(processar_frase(frase))
