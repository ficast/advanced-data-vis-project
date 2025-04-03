SELECT * FROM enem.mv_evolucao_notas_ano ORDER BY nu_ano, nota_total DESC;

SELECT 
  nu_ano,
  MIN(nota_total) AS min_total,
  percentile_cont(0.25) WITHIN GROUP (ORDER BY nota_total) AS q1_total,
  percentile_cont(0.50) WITHIN GROUP (ORDER BY nota_total) AS median_total,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY nota_total) AS q3_total,
  MAX(nota_total) AS max_total,
  AVG(nota_total) AS avg_total
FROM (
  SELECT 
    nu_ano,
    (nu_nota_cn + nu_nota_ch + nu_nota_lc + nu_nota_mt + nu_nota_redacao) / 5.0 AS nota_total
  FROM enem.microdados
) sub
GROUP BY nu_ano
ORDER BY nu_ano;

CREATE MATERIALIZED VIEW enem.mv_boxplot_notas_por_ano AS
SELECT 
  nu_ano,
  MIN(nota_total) AS min_total,
  percentile_cont(0.25) WITHIN GROUP (ORDER BY nota_total) AS q1_total,
  percentile_cont(0.50) WITHIN GROUP (ORDER BY nota_total) AS median_total,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY nota_total) AS q3_total,
  MAX(nota_total) AS max_total,
  AVG(nota_total) AS avg_total
FROM (
  SELECT 
    nu_ano,
    (nu_nota_cn + nu_nota_ch + nu_nota_lc + nu_nota_mt + nu_nota_redacao) / 5.0 AS nota_total,
    ((CASE WHEN nu_nota_cn = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_ch = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_lc = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_mt = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_redacao = 0 THEN 1 ELSE 0 END)
    ) AS zero_count
  FROM enem.microdados
) sub
WHERE zero_count < 2
GROUP BY nu_ano
WITH DATA;

CREATE MATERIALIZED VIEW enem.mv_boxplot_notas_por_ano AS
SELECT 
  nu_ano,
  COUNT(*) AS total_inscritos,
  COUNT(*) FILTER (WHERE zero_count < 2) AS estudantes_presentes,
  MIN(nota_total) FILTER (WHERE zero_count < 2) AS min_total,
  percentile_cont(0.25) WITHIN GROUP (ORDER BY nota_total) FILTER (WHERE zero_count < 2) AS q1_total,
  percentile_cont(0.50) WITHIN GROUP (ORDER BY nota_total) FILTER (WHERE zero_count < 2) AS median_total,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY nota_total) FILTER (WHERE zero_count < 2) AS q3_total,
  MAX(nota_total) FILTER (WHERE zero_count < 2) AS max_total,
  AVG(nota_total) FILTER (WHERE zero_count < 2) AS avg_total
FROM (
  SELECT 
    nu_ano,
    (nu_nota_cn + nu_nota_ch + nu_nota_lc + nu_nota_mt + nu_nota_redacao) / 5.0 AS nota_total,
    ((CASE WHEN nu_nota_cn = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_ch = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_lc = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_mt = 0 THEN 1 ELSE 0 END) +
     (CASE WHEN nu_nota_redacao = 0 THEN 1 ELSE 0 END)
    ) AS zero_count
  FROM enem.microdados
) sub
GROUP BY nu_ano
WITH DATA;


SELECT * FROM enem.mv_boxplot_notas_por_ano;
