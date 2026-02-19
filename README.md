# Data Processor CLI

Projeto pequeno para praticar leitura e tratamento de dados reais em CSV usando Python e linha de comando.
O foco aqui é *clareza do código* (didático e fácil de manter).

## Rodando

```bash
python -m src.data_processor.cli --input sample.csv
``` 

## Exemplos

Filtro + ordenação:

```bash
python -m src.data_processor.cli --input sample.csv --filter status=ativo --sort valor
```

Ignorar maiúsculas/minúsculas + limitar + exportar CSV:

```bash
python -m src.data_processor.cli --input sample.csv --filter status=ATIVO --ignore-case --sort valor --limit 50 --export-csv saida.csv
```

## Funcionalidades

- Leitura de CSV
- Filtro por campo
- Ordenação por coluna
- Filtro case-insensitive
- Limite de linhas no JSON
- Exportação para CSV
