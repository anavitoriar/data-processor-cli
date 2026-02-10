import argparse
from pathlib import Path

from .processor import read_csv_as_dicts, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="data-processor",
        description="CLI simples para ler CSV e gerar um report em JSON (base para filtros/ordenação).",
    )

    parser.add_argument("--input", required=True, help="Arquivo CSV de entrada.")
    parser.add_argument("--output", default="report.json", help="Arquivo JSON de saída. Padrão: report.json")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        print(f"Arquivo não encontrado: {input_path}")
        return
    if not input_path.is_file():
        print(f"O caminho informado não é um arquivo: {input_path}")
        return

    rows = read_csv_as_dicts(input_path)

    report = {
        "input": str(input_path),
        "total_rows": len(rows),
        "preview": rows[:3],  # humano: mostra só um pedacinho
    }

    write_json(output_path, report)
    print(f"OK! Report gerado em: {output_path}")


if __name__ == "__main__":
    main()
