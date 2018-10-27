Exclui os comentários com {1, -1} da análise
Excluimos commits de merge (mensagens sem sentimentos)
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

# Quantidades

- No total, temos __35232__ commits com sentimento neutro {1, -1}
- __11979__ commits com algum sentimento (Positivo > 1 ou Negativo < -1)
- Refatorações
  - __2271__ commits com Refatorações e com sentimento (não é {1, -1})
  - __9709__ commits sem Refatorações e com sentimento (não é {1, -1})
- Findings
  - __4474__ commits com no mínimo 1 finding (F.new > 1), com linhas alteradas e com sentimento (não é {1, -1})
  - __5445__ commits com no mínimo 1 issue resolvido(resolved) OU não resolvido(unresolved) e com sentimento (não é {1, -1})

## Quantidades / Projeto

### Issues / LOC

- dropwizard: 83
- guava: 719
- java-tron: 16
- kafka: 702
- mockito: 870
- netty: 1514
- rxjava: 370
- tutorials: 200

### res / ( unres + res )

- dropwizard: 143
- guava: 852
- java-tron: 76
- kafka: 801
- mockito: 1014
- netty: 1922
- rxjava: 522
- tutorials: 115

# R commands

*OBS: Remover a linha de títulos (se tiver) quando for passar os dados para o R. Deixar apenas os valores!

```R
list = list(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r)
scores = unlist(list)
length(scores)

wilcox.test(scores)
t.test(scores)
```

# SQL`s

- Com refatorações (descarta {1, -1})
```sql
SELECT (S.Positive + S.Negative) as Final FROM sentiment S 
INNER JOIN Refactorings R ON S.sha = R.sha 
WHERE S.Positive <> 1 OR S.Negative <> -1 AND
R.total > 0;
```

- Sem refatorações (descarta {1, -1})
```sql
SELECT (S.Positive + S.Negative) as Final FROM Sentiment S 
LEFT JOIN refactorings R ON S.sha = R.sha 
WHERE R.sha IS NULL AND 
(S.Positive <> 1 OR S.Negative <> -1)
```

- Todos (descarta {1, -1})
```sql
SELECT (S.Positive + S.Negative) as Final FROM Sentiment S 
WHERE (S.Positive <> 1 OR S.Negative <> -1)
```
- Retorna as médias de (insertion_lines/new_findings) para cada score final
```sql
SELECT (S.Positive + S.Negative) as Final, AVG(C.insertions / F.new) FROM findings F 
INNER JOIN commits C ON C.sha = F.sha
INNER JOIN sentiment S ON S.sha = F.sha
WHERE F.new > 0 AND 
C.insertions IS NOT NULL AND
(S.Positive <> 1 OR S.Negative <> -1) 
GROUP BY Final;
```

- Calcular as porcentagens commits com e sem refatorações por projeto
```sql
SELECT C1.project, R2.with_refactoring, (R2.with_refactoring * 1.0 / (R1.without_refactoring + R2.with_refactoring)) AS percentage,
R1.without_refactoring, (R1.without_refactoring * 1.0 / (R1.without_refactoring + R2.with_refactoring)) AS percentage
FROM commits C1,
(SELECT C.project AS project, COUNT(*) AS without_refactoring FROM commits C 
INNER JOIN sentiment S ON S.sha = C.sha
LEFT JOIN refactorings R ON R.sha = C.sha
WHERE R.sha IS NULL 
AND (S.positive <> 1 OR S.negative <> -1) 
GROUP BY C.project) AS R1, 
(SELECT C.project AS project, COUNT(*) AS with_refactoring FROM commits C 
INNER JOIN sentiment S ON S.sha = C.sha
INNER JOIN refactorings R ON R.sha = C.sha
WHERE (S.positive <> 1 OR S.negative <> -1) 
GROUP BY C.project) AS R2
WHERE R1.project = C1.project AND
R2.project = C1.project
GROUP BY C1.project
```

# Tests outputs

## All data

- Wilcoxon
```
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 22556000, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0
```

- T.test

```
> t.test(scores)

        One Sample t-test

data:  scores
t = -20.12, df = 11979, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.2138049 -0.1758446
sample estimates:
 mean of x
-0.1948247
```

## With Refactorings

- Wilcoxon

```
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 851420, p-value = 0.0002434
alternative hypothesis: true location is not equal to 0
```

- T.test
```
> t.test(scores)

        One Sample t-test

data:  scores
t = -3.7291, df = 2270, p-value = 0.0001968
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.12631530 -0.03925053
sample estimates:
  mean of x
-0.08278292
```

## Without refactorings

- Wilcoxon
```
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 14623000, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0
```

- T.test
```
> t.test(scores)

        One Sample t-test

data:  scores
t = -20.573, df = 9708, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.2420920 -0.1999721
sample estimates:
mean of x
-0.221032

```