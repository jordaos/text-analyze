SELECT IFNULL(F.new, 0) as new, IFNULL(F.resolved, 0) as resolved, IFNULL(F.unresolved, 0) as unresolved, IFNULL(C.insertions, 0) as insertions, (S.positive + S.negative) as score From commits C, sentiment S
LEFT JOIN findings F USING(sha)
WHERE 
C.sha = S.sha AND
(S.Positive <> 1 OR S.Negative <> -1) AND
C.sha <> 'b49c1296eb569afcaee5b521ad2d0c7afd921d8f'