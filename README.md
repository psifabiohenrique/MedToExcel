# MedToExcel

<!-- Imagem de capa do projeto -->
<!-- Substitua 'capa.png' por uma imagem que represente visualmente o projeto, como o logo do laboratório, uma montagem das caixas experimentais ou uma tela inicial do software. -->
![Imagem de capa do MedToExcel](docs/imagens/capa.png)

MedToExcel é uma interface gráfica desenvolvida para facilitar a análise de dados de experimentos comportamentais realizados em laboratórios de psicologia, especialmente aqueles que utilizam o sistema MedPC para controle de caixas experimentais com ratos ou pombos.

## Visão Geral

O aplicativo permite extrair, organizar e analisar dados de arquivos gerados pelo MedPC, oferecendo ferramentas específicas para análise de latência, variabilidade, sequências corretas, e outros parâmetros relevantes em pesquisas comportamentais.

<!-- Imagem ilustrativa do fluxo principal -->
<!-- Crie uma imagem (ex: fluxograma) mostrando o fluxo de uso do software: importação do arquivo MedPC, seleção de análise, exportação dos resultados. Pode ser um diagrama simples ou um print com setas explicativas. -->
![Fluxo principal do MedToExcel](docs/imagens/fluxo_principal.png)

## Principais Funcionalidades

- **Extração de Dados MedPC**: Importe arquivos `.MPC` e modelos para organizar os dados experimentais.
- **Análises FAP**: Calculo de latências, duração de sequências, duração de tentativas, tempo de resposta/correção e porcentagem de sequências corretas, de uma pesquisa específica realizada no laboratório.
- **Análises de Variabilidade**: Calcule U Value, Recorrência, Número de Sequências Diferentes, Switches e RNG.
- **Análise de Médias (FAP Analysis Mean)**: Permite análise agrupada ou por resposta individual da pesquisa específica da FAP.
- **Exportação**: Resultados podem ser copiados para a área de transferência ou exportados em planilhas Excel.

<!-- Imagem ilustrativa da interface -->
<!-- Capture uma screenshot da interface principal do MedToExcel, mostrando os botões e opções disponíveis. Se possível, destaque as áreas principais com caixas ou setas. -->
![Interface gráfica do MedToExcel](docs/imagens/interface.png)

## Instalação

Este projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciamento de dependências.

1. Certifique-se de ter o Poetry instalado:
   ```bash
   pipx install poetry
   ```
2. Instale as dependências do projeto:
   ```bash
   poetry install
   ```

## Como Usar

1. Execute o aplicativo:
   ```bash
   poetry run python main.py
   ```
2. A janela principal exibirá as opções:
   - **Med to Excel**: Extração e organização de dados MedPC.
   - **Variability Calc**: Análises de variabilidade.
   - **FAP analysis**: Análises detalhadas de desempenho experimental (configurado para a pesquisa da FAP realizada no laboratório).
   - **FAP analysis mean**: Análises de médias e respostas individuais (configurado para a pesquisa da FAP realizada no laboratório).

<!-- Imagem ilustrativa de uso -->
<!-- Capture um exemplo de uso real: por exemplo, um print mostrando um arquivo sendo selecionado, ou o resultado de uma análise sendo exibido/exportado. Pode ser uma sequência de imagens ou uma montagem. -->
![Exemplo de uso do MedToExcel](docs/imagens/exemplo_uso.png)

### Fluxo Básico de Trabalho

#### 1. Med to Excel
- Selecione o arquivo de modelo e o arquivo `.MPC`.
- Escolha se os dados estão em linha única e se deseja usar vírgula como separador decimal.
- Clique em "Copy data" para extrair e copiar os dados organizados.

#### 2. Variability
- Cole as sequências ou frequências conforme instrução de cada funcionalidade (U Value, Recurrence, etc).
- Clique em "Calculate" para obter o resultado.

#### 3. FAP Analysis
- Selecione o arquivo `.MPC`.
- Escolha o tipo de análise (latência, duração, etc).
- Para análises com opção "Individual Responses", marque se deseja análise por resposta.
- Clique em "Calculate". Os resultados são copiados para a área de transferência ou salvos em planilhas na pasta `planilhas/`.

#### 4. FAP Analysis Mean
- Similar ao FAP Analysis, mas focado em médias e agrupamentos.
- Permite análise por resposta individual.

## Tipos de Análises Disponíveis

- **Latência**: Tempo entre início da tentativa e respostas da sequência.
- **Duração da Sequência**: Tempo entre respostas dentro de uma sequência.
- **Duração da Tentativa**: Tempo total da tentativa (latência + duração da sequência).
- **Tempo de Resposta/Correção**: Análise de respostas corretas e seus tempos.
- **Porcentagem de Sequências Corretas**: Proporção de sequências realizadas corretamente.
- **Variabilidade**: U Value, Recorrência, Número de Sequências Diferentes, Switches, RNG.

## Entrada e Saída de Dados

- **Entrada**: Arquivos `.MPC` exportados do MedPC, arquivos de modelo (ex: `latency.txt`, `consequences.txt` em `src/`).
- **Saída**: Resultados copiados para a área de transferência ou salvos como planilhas Excel em `planilhas/`.

## Exemplo de Fluxo Completo

1. Exporte o arquivo `.MPC` do MedPC.
2. Abra o MedToExcel, selecione "Med to Excel" e extraia os dados.
3. Use "FAP analysis" para calcular latências ou outras métricas.
4. Os resultados estarão disponíveis para colar em relatórios ou em arquivos Excel.

## Solução de Problemas

- Certifique-se de que os arquivos de modelo (`latency.txt`, `consequences.txt`, etc) estejam presentes na pasta `src/`.
- A pasta `planilhas/` será criada automaticamente para salvar resultados.
- Em caso de erro, verifique se os arquivos de entrada estão no formato correto.

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

### Convenções de Commit
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Alterações de formatação
- `refactor:` Refatoração de código
- `test:` Adição ou correção de testes
- `chore:` Atualizações de build, configurações, etc.

## Licença e Créditos

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

Desenvolvido no Laboratório de Análise Experimental do Comportamento da Universidade de Brasília (LabAEC/UnB) por Fábio Henrique de Souza Silva.