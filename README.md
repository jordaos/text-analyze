# Analyze v2.0

## Refatorações

Usando a ferramenta [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner), é possível pegar apenas commits que contenham refatorações. Os dados serão postos em um arquivo CSV. Trabalharemos aqui a partir desse CSV. 

Para saber como obtê-lo, siga as instruções no [repositório da ferramenta](https://github.com/tsantalis/RefactoringMiner#running-from-the-command-line).

### Premissas

1. Os dados projetos a ser analizados devem estar em `data/PROJECT_NAME`
    - O projeto deve ser clonado em `data/PROJECT_NAME/Repository`
    - O resultado da análise por _RefactoringMiner_ (log no terminal da análise) deve estar em `data/PROJECT_NAME/log.txt`

### Passos de execução

1. `src/from-csv-to-db.py PROJECT_NAME¹`: pega o CSV e transforma em um banco SQLite.

¹ substitua `PROJECT_NAME` pelo nome do prjeto no GitHub.

TABELA 1: Estrutura do armazenamento de refatorações.
| SHA | Total | extract_method | inline_method | move_method_or_attribute | pull_up_method_or_attribute | push_down_method_or_attribute | extract_superclass_or_interface | move_class | rename_class | rename_method | extract_and_move_method | change_package |
|------------------------------------------|-------|----------------|---------------|--------------------------|-----------------------------|-------------------------------|---------------------------------|------------|--------------|---------------|-------------------------|----------------|
| 36287f7c3b09eff78395267a3ac0d7da067863fd | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4c3bed414f5a1f712409010518429f02de220b7d | 10 | 0 | 0 | 2 | 5 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |

### Sentiment analysis

- Primeiro, baixe os dados de sentistrength: http://sentistrength.wlv.ac.uk/
- Baixe a ferramenta Java do sentistrength: http://gateway.path.berkeley.edu:8080/artifactory/list/release-local/com/sentistrength/sentistrength/0.1/sentistrength-0.1.jar
- Extraia os dados de sentistrength para `tools/sentistrength/sentistrength_data/`. E mova a ferramenta Java sentistrength para `tools/sentistrength/`.
- Renomear `tools/sentistrength/sentistrength_data/EmotionLookupTable.txt` para `tools/sentistrength/sentistrength_data/EmotionLookupTable-old.txt`.
- Copiar o arquivo de palavras neutras para `tools/sentistrength/words-neutral.txt`

#### Passos de execução

1. remover as palavras que são específicas do contexto (alterar o dicionário).
2. `src/compute-sentiment.py PROJECT_NAME`: para computar os sentimentos nas partes.

### Analizar commits sem refatorações a partir do log gerado pelo _RefactoringMiner_

1. `src/from-log-to-db.py PROJECT_NAME`: para transformar os commits do LOG para um SQLITE file.

### Exportar o CSV

- Commits com refatorações: `SELECT S.sha, S.Positive, S.Negative, R.total FROM sentiment S INNER JOIN refactorings R  ON S.sha = R.sha WHERE (S.Positive > 1 OR S.Negative < -1)`
- Commits sem refatorações: `SELECT S.sha, S.Positive, S.Negative FROM sentiment S LEFT JOIN refactorings R  ON S.sha = R.sha WHERE R.sha is null and (S.Positive > 1 OR S.Negative < -1)`
- *Ambos retornam apensa os commits com algum sentimento (pos > 1 OR neg < -1).

## Compute refactorings

Pega os commits com refatorações a partir de `all_refactorings.csv` e joga numa tabela

## Get all commits

Pega todos os commits do projeto e joga na tabela commits

- SELECT COUNT(*) FROM Sentiment S WHERE (S.Positive + S.Negative) = 0
- SELECT COUNT(*) FROM Sentiment S INNER JOIN findings F on F.sha = S.sha WHERE F.new > 0
- SELECT COUNT(*) FROM Sentiment S INNER JOIN refactorings R on R.sha = S.sha

- Findings (descarta os commits com sentimento neutro e que não tiveram findings)
```sql
SELECT S.sha, S.Positive, S.Negative, (S.Positive + S.Negative) as Final, F.new FROM sentiment S 
INNER JOIN Findings F ON S.sha = F.sha 
WHERE (S.Positive + S.Negative) <> 0 AND
F.new > 0;
```

- Refactorings (descarta os commits com sentimento neutro e que não tiveram refatorações)
```sql
SELECT S.sha, S.Positive, S.Negative, (S.Positive + S.Negative) as Final, R.total FROM sentiment S 
INNER JOIN Refactorings R ON S.sha = R.sha 
WHERE (S.Positive + S.Negative) <> 0 AND
R.total > 0;
```

- Get all data
```sql
SELECT S.sha, S.Positive, S.Negative, (S.Positive + S.Negative) as Final, F.new, R.total FROM sentiment S 
LEFT JOIN Findings F ON S.sha = F.sha 
LEFT JOIN Refactorings R ON S.sha = R.sha ;
```

# all-in-one
pega todos os projetos dentro de `data` e transforma em apenas um banco.