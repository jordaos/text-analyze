Exclui os comentários com {1, -1} da análise

# Perguntas

## 1)
- Queremos saber se quando tem refatorações o sentimento tense a ser positivo
- Vamos comparar o conjunto de commits __com refatorações__ com o conjunto de sentimentos __sem refatorações__, para verificar se o projeto já não tem uma tendência a ter sentimentos positivos. Como fazer essa comparação entre esses dis conjuntos?

## 2
- O teste _Student’s t-Test_ nos dirá se a população tem significância estatística, OK.
- O teste _Wilcoxon test_ verifica se a distribuição das diferenças é simétrica em torno
do valor zero.
- Não falta com base nesses dois testes podemos afirmar alguma coisa em relação as duas populações?

## Um caso perfeito (ilustrativo)
- A média de sentimentos da população (1000 commits) sem refatorações (descartando {1, -1}), é igual a 0,5
- A média de sentimentos do mesmo projetos no conjunto de commits com refatorações (300 commits) é 1,3.
- Queremos afirmar que nesse caso, quando se refatora, os sentimentos positivos aumentam.

# SQL`s

- Com refatorações (descarta {1, -1})
```sql
SELECT (S.Positive + S.Negative) as Final FROM sentiment S 
INNER JOIN Refactorings R ON S.sha = R.sha 
WHERE S.Positive <> 1 AND S.Negative <> -1 AND
R.total > 0;
```

- Sem refatorações (descarta {1, -1})
```sql
SELECT (S.Positive + S.Negative) as Final FROM Sentiment S 
LEFT JOIN refactorings R ON S.sha = R.sha 
WHERE R.sha IS NULL AND 
(S.Positive <> 1 AND S.Negative <> -1)
```