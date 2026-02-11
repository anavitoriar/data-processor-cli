import argparse
from pathlib import Path

from .processor import read_csv_as_dicts, write_json, apply_filter, sort_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="data-processor",
        description="CLI simples para ler CSV e gerar um report em JSON (base para filtros/ordenação).",
    )

    parser.add_argument("--input", required=True, help="Arquivo CSV de entrada.")
    parser.add_argument("--output", default="report.json", help="Arquivo JSON de saída. Padrão: report.json")
    parser.add_argument("--filter", help="Filtro no formato campo=valor (ex: status=ativo).")
    parser.add_argument("--sort", help="Campo para ordenação (ex: valor).")

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
    original_total = len(rows)

    try:
        if args.filter:
            rows = apply_filter(rows, args.filter)

        if args.sort:
            rows = sort_rows(rows, args.sort)
    except ValueError as e:
        print(f"Erro: {e}")
        return

    report = {
        "input": str(input_path),
        "output": str(output_path),
        "filter": args.filter,
        "sort": args.sort,
        "summary": {
            "total_rows_original": original_total,
            "total_rows_final": len(rows),
        },
        "preview_final": rows[:5],
        "rows_final": rows,
    }

    write_json(output_path, report)
    print(f"OK! Report gerado em: {output_path}")


if __name__ == "__main__":
    main()
