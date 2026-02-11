from __future__ import annotations

import csv
import json
from pathlib import Path


def read_csv_as_dicts(input_path: Path) -> list[dict[str, str]]:
    """
    lê um CSV e devolve uma lista de dicionários.
    - chaves: nomes das colunas
    - valores: strings (por enquanto, para manter simples)
    """
    rows: list[dict[str, str]] = []

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # row já vem como dict (coluna -> valor)
            rows.append(dict(row))

    return rows


def write_json(output_path: Path, data: object) -> None:
    """Salva qualquer estrutura Python em JSON."""
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def parse_filter_expression(expr: str) -> tuple[str, str]:
    """
    Recebe algo como: "status=ativo"
    Retorna: ("status", "ativo")
    """
    if "=" not in expr:
        raise ValueError("Filtro inválido. Use campo=valor (ex: status=ativo).")

    field, value = expr.split("=", 1)
    field = field.strip()
    value = value.strip()

    if not field:
        raise ValueError("Filtro inválido: campo vazio.")
    if value == "":
        raise ValueError("Filtro inválido: valor vazio.")

    return field, value


def apply_filter(rows: list[dict[str, str]], expr: str) -> list[dict[str, str]]:
    if not rows:
        return rows

    field, value = parse_filter_expression(expr)

    if field not in rows[0]:
        raise ValueError(f"Campo '{field}' não existe no CSV.")

    return [r for r in rows if r.get(field) == value]


def sort_rows(rows: list[dict[str, str]], field: str) -> list[dict[str, str]]:
    if not rows:
        return rows

    if field not in rows[0]:
        raise ValueError(f"Campo '{field}' não existe no CSV.")

    def key_func(r: dict[str, str]):
        raw = (r.get(field) or "").strip()
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            return raw.lower()

    return sorted(rows, key=key_func)
