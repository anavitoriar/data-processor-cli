from __future__ import annotations

import csv
import json
from pathlib import Path


def read_csv_as_dicts(input_path: Path) -> list[dict[str, str]]:
    """
    Lê um CSV e devolve uma lista de dicionários.
    - Chaves: nomes das colunas
    - Valores: strings (por enquanto, para manter simples)
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
