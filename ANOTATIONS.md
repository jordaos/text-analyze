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
library(foreach)
scores = c()
dat <- read.csv("/home/jordao/Projects/text-analyze/CSV/refactorings/with/all.csv", header=FALSE)
foreach(elem = dat, .packages="foreach") %do% (scores <- c(scores, elem))

length(scores)
mean(scores)

wilcox.test(scores)
t.test(scores)
```

# SQL`s

## Refatorações

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

## Findings

Com findings são os commits com no mínimo um novo issue (F.new > 0). Também serão descartados os commits sem sentimentos (1, -1).

- _Commits_ com _findings_
```SQL
SELECT (S.positive + S.negative) as Final FROM sentiment S
INNER JOIN findings F ON F.sha = S.sha
WHERE F.new > 0
AND (S.Positive > 1 OR S.Negative < -1);
```

- _Commits_ sem _findings_
```SQL
SELECT (S.positive + S.negative) as Final FROM sentiment S
LEFT JOIN findings F ON F.sha = S.sha
WHERE (F.new = 0 OR F.sha IS NULL)
AND (S.Positive > 1 OR S.Negative < -1);
```

# Tests outputs

## Refactorings

### All data

- Wilcoxon
```R
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 22556000, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0
```

- T.test

```R
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

### With Refactorings

- Wilcoxon

```R
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 851420, p-value = 0.0002434
alternative hypothesis: true location is not equal to 0
```

- T.test
```R
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

### Without refactorings

- Wilcoxon
```R
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 14623000, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0
```

- T.test
```R
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

## Findings

### ALL Projects
- All data
```R
> length(scores)
[1] 11980
> mean(scores)
[1] -0.1948247
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 22556000, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

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

- With Findings

```R
> length(scores)
[1] 4819
> mean(scores)
[1] -0.08300477
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 3893900, p-value = 5.665e-08
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -5.4759, df = 4818, p-value = 4.574e-08
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.11272173 -0.05328782
sample estimates:
  mean of x
-0.08300477
```

- Whithout Findings
```R
> length(scores)
[1] 7163
> mean(scores)
[1] -0.2699986
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 7674600, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -21.592, df = 7162, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.2945114 -0.2454858
sample estimates:
 mean of x
-0.2699986
```

### DROPWIZARD

- With findings
```R
> length(scores)
[1] 132
> mean(scores)
[1] -0.25
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 2862, p-value = 0.01866
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -2.5458, df = 131, p-value = 0.01206
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4442625 -0.0557375
sample estimates:
mean of x
    -0.25
```

- Without findings
```R
> length(scores)
[1] 505
> mean(scores)
[1] -0.3762376
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 35700, p-value = 6.466e-13
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -7.657, df = 504, p-value = 9.794e-14
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4727754 -0.2796998
sample estimates:
 mean of x
-0.3762376
```

### GUAVA

- With findings
```R
> length(scores)
[1] 720
> mean(scores)
[1] -0.3458333
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 61672, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -8.8035, df = 719, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4229578 -0.2687089
sample estimates:
 mean of x
-0.3458333
```

- Without findings
```R
> length(scores)
[1] 759
> mean(scores)
[1] -0.3386034
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 71026, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -8.98, df = 758, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4126249 -0.2645820
sample estimates:
 mean of x
-0.3386034
```

### JAVA-TRON

- With findings
```R
> length(scores)
[1] 59
> mean(scores)
[1] -0.01694915
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 672, p-value = 0.8682
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -0.12115, df = 58, p-value = 0.904
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.2970054  0.2631071
sample estimates:
  mean of x
-0.01694915
```

- Without findings
```R
> length(scores)
[1] 456
> mean(scores)
[1] -0.372807
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 31160, p-value = 3.197e-12
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -7.1977, df = 455, p-value = 2.547e-12
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4745952 -0.2710189
sample estimates:
mean of x
-0.372807
```

### KAFKA

- With findings
```R
> length(scores)
[1] 702
> mean(scores)
[1] -0.3717949
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 54762, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -10.246, df = 701, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4430384 -0.3005513
sample estimates:
 mean of x
-0.3717949
```

- Without findings
```R
> length(scores)
[1] 1422
> mean(scores)
[1] -0.5576653
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 168020, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -23.893, df = 1421, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.6034499 -0.5118806
sample estimates:
 mean of x
-0.5576653
```

### MOCKITO

- With findings
```R
> length(scores)
[1] 915
> mean(scores)
[1] 0.4601093
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 226370, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = 16.05, df = 914, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 0.4038478 0.5163708
sample estimates:
mean of x
0.4601093
```

- Without findings
```R
> length(scores)
[1] 1278
> mean(scores)
[1] 0.286385
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 423240, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = 10.19, df = 1277, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 0.2312463 0.3415237
sample estimates:
mean of x
 0.286385
```

### NETTY

- With findings
```R
> length(scores)
[1] 1521
> mean(scores)
[1] -0.2952005
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 297270, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -10.853, df = 1520, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.3485541 -0.2418470
sample estimates:
 mean of x
-0.2952005
```

- Without findings
```
> length(scores)
[1] 1549
> mean(scores)
[1] -0.4983861
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 263510, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -18.799, df = 1548, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.5503866 -0.4463855
sample estimates:
 mean of x
-0.4983861
```

### RXJAVA

- With findings
```R
> length(scores)
[1] 548
> mean(scores)
[1] 0.4379562
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 81326, p-value < 2.2e-16
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = 12.006, df = 547, p-value < 2.2e-16
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 0.3663001 0.5096123
sample estimates:
mean of x
0.4379562
```

- Without findings
```R
> length(scores)
[1] 812
> mean(scores)
[1] -0.01477833
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 136280, p-value = 0.765
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -0.40899, df = 811, p-value = 0.6827
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.08570551  0.05614886
sample estimates:
  mean of x
-0.01477833
```

### TUTORIALS

- With findings
```R
> length(scores)
[1] 222
> mean(scores)
[1] -0.3063063
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 6847.5, p-value = 2.778e-05
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -4.3155, df = 221, p-value = 2.403e-05
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.4461875 -0.1664252
sample estimates:
 mean of x
-0.3063063
```

- Without findings
```R
> length(scores)
[1] 382
> mean(scores)
[1] -0.2774869
> wilcox.test(scores)

        Wilcoxon signed rank test with continuity correction

data:  scores
V = 23060, p-value = 1.126e-06
alternative hypothesis: true location is not equal to 0

> t.test(scores)

        One Sample t-test

data:  scores
t = -5.0664, df = 381, p-value = 6.332e-07
alternative hypothesis: true mean is not equal to 0
95 percent confidence interval:
 -0.3851758 -0.1697980
sample estimates:
 mean of x
-0.2774869
```

