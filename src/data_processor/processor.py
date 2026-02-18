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


def apply_filter(rows: list[dict[str, str]], expr: str, ignore_case: bool = False) -> list[dict[str, str]]:
    """
    Aplica filtro no formato campo=valor.
    Se ignore_case=True, ignora maiúsculas/minúsculas.
    """
    if not rows:
        return rows

    field, value = parse_filter_expression(expr)

    if field not in rows[0]:
        raise ValueError(f"Campo '{field}' não existe no CSV.")

    target = value.lower() if ignore_case else value

    filtered: list[dict[str, str]] = []
    for row in rows:
        current = row.get(field)
        if current is None:
            continue

        current_cmp = current.lower() if ignore_case else current
        if current_cmp == target:
            filtered.append(row)

    return filtered

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

def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
