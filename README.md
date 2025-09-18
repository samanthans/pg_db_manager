# pg_db_manager

Ferramenta de linha de comando para manutenção de bancos PostgreSQL, incluindo backup, restauração, compactação, criptografia e limpeza (vacuum).

## Requisitos

- Python 3.11+
- PostgreSQL instalado (pg_dump e pg_restore disponíveis)
- Utilize o uv e rode `uv sync` na raiz do projeto. [Instale o UV.](https://docs.astral.sh/uv/getting-started/installation/)
- Ou, crie um ambiente virtual python e instale as dependências do projeto:

  ```pwsh
  pip install -r requirements.txt
  ```
  (Se não houver requirements.txt, instale manualmente: `psycopg`)

## Estrutura

- `backup.py`: Script para realizar backup do banco.
- `restore.py`: Script para restaurar backup.
- `src/`: Módulos auxiliares (dump, criptografia, zip, logger, vacuum).

## Backup

### Comando básico

```pwsh
python backup.py <CAMINHO_DESTINO> --db <NOME_BANCO> --user <USUARIO> --password <SENHA>
```

### Opções adicionais

- `--vacuum`: Executa vacuum antes do backup.
- `--full`: Vacuum no modo full.
- `--zip` ou `-z`: Compacta o backup.
- `--zip-pwd <SENHA>`: Compacta o backup com senha.
- `--encrypt` ou `-e`: Criptografa o backup.
- `--key <CHAVE>`: Chave para criptografia.
- `--copy <CAMINHO>`: Copia o backup para outro local.
- `--pg-dump-path <CAMINHO>`: Caminho para o binário do pg_dump.

### Exemplo completo

```pwsh
python backup.py dump/ --db test_db --user postgres --password 123456 --zip --encrypt --key minha_chave
```

## Restore

### Comando básico

```pwsh
python restore.py <CAMINHO_BACKUP> --db <NOME_BANCO> --user <USUARIO> --password <SENHA>
```

### Opções adicionais

- `--decrypt`: Descriptografa o backup.
- `--key <CHAVE>`: Chave para descriptografia.
- `--unzip`: Descompacta o backup.
- `--pg-restore-path <CAMINHO>`: Caminho para o binário do pg_restore.

### Exemplo completo

```pwsh
python restore.py dump/test_db-backup-20250911_143750.dump.enc --db test_db --user postgres --password 123456 --decrypt --key minha_chave --unzip
```

## Observações

- Os logs são gerados e removidos automaticamente após execução bem-sucedida.
- Os arquivos intermediários são salvos em diretórios temporários quando necessário.
- Para backups criptografados, guarde a chave gerada/informada para restaurar posteriormente.

## Dúvidas

Para mais detalhes, consulte os scripts ou abra uma issue.
