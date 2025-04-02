# MedToExcel

Aplicativo para análise de dados de pesquisas comportamentais.

## Instalação

Este projeto usa Poetry para gerenciamento de dependências. Para instalar:

1. Certifique-se de ter o Poetry instalado
2. Execute:
```bash
poetry install
```

## Uso

Para executar o aplicativo:

```bash
poetry run python main.py
```

## Fluxo de Trabalho Git

Este projeto segue um fluxo de trabalho Git estruturado:

### Branches Principais
- `main`: Branch principal com código em produção
- `develop`: Branch de desenvolvimento com últimas alterações

### Branches de Funcionalidades
- Nomenclatura: `feature/nome-da-funcionalidade`
- Exemplo: `feature/interface-grafica`

### Branches de Correção
- Nomenclatura: `fix/nome-do-problema`
- Exemplo: `fix/erro-calculo`

### Branches de Release
- Nomenclatura: `release/versao`
- Exemplo: `release/v1.0.0`

### Fluxo de Trabalho

1. **Nova Funcionalidade**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nova-funcionalidade
   # Faça suas alterações
   git add .
   git commit -m "feat: descrição da nova funcionalidade"
   git push origin feature/nova-funcionalidade
   ```

2. **Correção de Bug**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b fix/descricao-do-bug
   # Faça suas correções
   git add .
   git commit -m "fix: descrição da correção"
   git push origin fix/descricao-do-bug
   ```

3. **Release**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.0.0
   # Atualize a versão e faça ajustes finais
   git add .
   git commit -m "chore: preparação para release v1.0.0"
   git push origin release/v1.0.0
   ```

### Convenções de Commit

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Alterações de formatação
- `refactor:` Refatoração de código
- `test:` Adição ou correção de testes
- `chore:` Atualizações de build, configurações, etc. 