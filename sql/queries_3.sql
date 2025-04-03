SELECT * FROM enem.estados;

SELECT * FROM enem.municipios m LIMIT 10;

ALTER TABLE enem.estados DROP CONSTRAINT estados_pkey;
ALTER TABLE enem.estados ADD CONSTRAINT estados_pkey PRIMARY KEY (codigo_uf);
ALTER TABLE enem.estados DROP COLUMN ogc_fid;

SELECT * FROM enem.microdados m LIMIT 10;

ALTER TABLE enem.estados ADD COLUMN codigo_uf INTEGER;

UPDATE enem.estados
SET codigo_uf = CASE id
  WHEN 'RO' THEN 11
  WHEN 'AC' THEN 12
  WHEN 'AM' THEN 13
  WHEN 'RR' THEN 14
  WHEN 'PA' THEN 15
  WHEN 'AP' THEN 16
  WHEN 'TO' THEN 17
  WHEN 'MA' THEN 21
  WHEN 'PI' THEN 22
  WHEN 'CE' THEN 23
  WHEN 'RN' THEN 24
  WHEN 'PB' THEN 25
  WHEN 'PE' THEN 26
  WHEN 'AL' THEN 27
  WHEN 'SE' THEN 28
  WHEN 'BA' THEN 29
  WHEN 'MG' THEN 31
  WHEN 'ES' THEN 32
  WHEN 'RJ' THEN 33
  WHEN 'SP' THEN 35
  WHEN 'PR' THEN 41
  WHEN 'SC' THEN 42
  WHEN 'RS' THEN 43
  WHEN 'MS' THEN 50
  WHEN 'MT' THEN 51
  WHEN 'GO' THEN 52
  WHEN 'DF' THEN 53
  ELSE NULL
END;


ALTER TABLE enem.municipios
ADD CONSTRAINT fk_municipios_estados
FOREIGN KEY (codigo_uf)
REFERENCES enem.estados(codigo_uf);

SELECT DISTINCT m.co_municipio_prova
FROM enem.microdados m
LEFT JOIN enem.municipios mu ON m.co_municipio_prova = mu.codigo_ibge
WHERE mu.codigo_ibge IS NULL;

ALTER TABLE enem.microdados
ADD CONSTRAINT fk_microdados_municipios
FOREIGN KEY (co_municipio_prova)
REFERENCES enem.municipios(codigo_ibge);

ALTER TABLE enem.microdados
ADD CONSTRAINT fk_microdados_estados
FOREIGN KEY (co_uf_prova)
REFERENCES enem.estados(codigo_uf);

CREATE INDEX idx_microdados_nu_ano ON enem.microdados (nu_ano);
CREATE INDEX idx_microdados_co_uf_prova ON enem.microdados (co_uf_prova);
CREATE INDEX idx_microdados_co_municipio_prova ON enem.microdados (co_municipio_prova);

CREATE INDEX idx_microdados_nu_ano_co_uf_prova 
ON enem.microdados (nu_ano, co_uf_prova);

CREATE INDEX idx_microdados_nu_ano_co_municipio_prova 
ON enem.microdados (nu_ano, co_municipio_prova);

SELECT
    e.id AS uf,
    m.nome AS municipio,
    AVG(md.nu_nota_cn) AS avg_nota_cn,
    AVG(md.nu_nota_ch) AS avg_nota_ch,
    AVG(md.nu_nota_lc) AS avg_nota_lc,
    AVG(md.nu_nota_mt) AS avg_nota_mt,
    AVG(md.nu_nota_redacao) AS avg_nota_redacao,
    (AVG(md.nu_nota_cn) + AVG(md.nu_nota_ch) + AVG(md.nu_nota_lc) + AVG(md.nu_nota_mt) + AVG(md.nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados md
JOIN enem.municipios m ON md.co_municipio_prova = m.codigo_ibge
JOIN enem.estados e ON CAST(SUBSTRING(m.codigo_ibge::text, 1, 2) AS INTEGER) = e.codigo_uf
WHERE m.nome ILIKE 'Itabirito'
GROUP BY e.id, m.nome
ORDER BY nota_total DESC;

SELECT
    md.co_uf_prova AS uf,
    AVG(md.nu_nota_cn)      AS avg_nota_cn,
    AVG(md.nu_nota_ch)      AS avg_nota_ch,
    AVG(md.nu_nota_lc)      AS avg_nota_lc,
    AVG(md.nu_nota_mt)      AS avg_nota_mt,
    AVG(md.nu_nota_redacao) AS avg_nota_redacao,
    (AVG(md.nu_nota_cn) + AVG(md.nu_nota_ch) + AVG(md.nu_nota_lc) + AVG(md.nu_nota_mt) + AVG(md.nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados md
JOIN enem.estados e ON md.co_uf_prova = e.codigo_uf
GROUP BY md.co_uf_prova
ORDER BY nota_total DESC;

SELECT
    e.codigo_uf,
    e.sigla,
    e.estado,
    e.wkb_geometry,
    AVG(md.nu_nota_cn)      AS avg_nota_cn,
    AVG(md.nu_nota_ch)      AS avg_nota_ch,
    AVG(md.nu_nota_lc)      AS avg_nota_lc,
    AVG(md.nu_nota_mt)      AS avg_nota_mt,
    AVG(md.nu_nota_redacao) AS avg_nota_redacao,
    (AVG(md.nu_nota_cn) + AVG(md.nu_nota_ch) + AVG(md.nu_nota_lc) +
     AVG(md.nu_nota_mt) + AVG(md.nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados md
JOIN enem.estados e ON md.co_uf_prova = e.codigo_uf
GROUP BY e.codigo_uf, e.sigla, e.estado, e.wkb_geometry
ORDER BY nota_total DESC;


SELECT
    e.codigo_uf,
    e.sigla,
    e.estado,
    md.renda_familiar,
    AVG(md.nu_nota_cn)      AS avg_nota_cn,
    MIN(md.nu_nota_cn)      AS min_nota_cn,
    MAX(md.nu_nota_cn)      AS max_nota_cn,
    AVG(md.nu_nota_ch)      AS avg_nota_ch,
    MIN(md.nu_nota_ch)      AS min_nota_ch,
    MAX(md.nu_nota_ch)      AS max_nota_ch,
    AVG(md.nu_nota_lc)      AS avg_nota_lc,
    MIN(md.nu_nota_lc)      AS min_nota_lc,
    MAX(md.nu_nota_lc)      AS max_nota_lc,
    AVG(md.nu_nota_mt)      AS avg_nota_mt,
    MIN(md.nu_nota_mt)      AS min_nota_mt,
    MAX(md.nu_nota_mt)      AS max_nota_mt,
    AVG(md.nu_nota_redacao) AS avg_nota_redacao,
    MIN(md.nu_nota_redacao) AS min_nota_redacao,
    MAX(md.nu_nota_redacao) AS max_nota_redacao,
    (AVG(md.nu_nota_cn) + AVG(md.nu_nota_ch) + AVG(md.nu_nota_lc) +
     AVG(md.nu_nota_mt) + AVG(md.nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados md
JOIN enem.estados e ON md.co_uf_prova = e.codigo_uf
GROUP BY e.codigo_uf, e.sigla, e.estado, md.renda_familiar
ORDER BY e.codigo_uf, nota_total DESC;

SELECT
    nu_ano,
    AVG(nu_nota_cn)      AS avg_nota_cn,
    AVG(nu_nota_ch)      AS avg_nota_ch,
    AVG(nu_nota_lc)      AS avg_nota_lc,
    AVG(nu_nota_mt)      AS avg_nota_mt,
    AVG(nu_nota_redacao) AS avg_nota_redacao,
    (AVG(nu_nota_cn) + AVG(nu_nota_ch) + AVG(nu_nota_lc) + AVG(nu_nota_mt) + AVG(nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados
GROUP BY nu_ano
ORDER BY nu_ano;

SELECT
    md.nu_ano,
    e.id AS uf,
    AVG(md.nu_nota_cn)      AS avg_nota_cn,
    AVG(md.nu_nota_ch)      AS avg_nota_ch,
    AVG(md.nu_nota_lc)      AS avg_nota_lc,
    AVG(md.nu_nota_mt)      AS avg_nota_mt,
    AVG(md.nu_nota_redacao) AS avg_nota_redacao,
    (AVG(md.nu_nota_cn) + AVG(md.nu_nota_ch) + AVG(md.nu_nota_lc) + AVG(md.nu_nota_mt) + AVG(md.nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados md
JOIN enem.estados e ON md.co_uf_prova = e.codigo_uf
GROUP BY md.nu_ano, e.id
ORDER BY md.nu_ano, nota_total DESC;

CREATE MATERIALIZED VIEW enem.mv_evolucao_notas_estado_ano AS
SELECT
    md.nu_ano,
    e.id AS uf,
    AVG(md.nu_nota_cn)      AS avg_nota_cn,
    AVG(md.nu_nota_ch)      AS avg_nota_ch,
    AVG(md.nu_nota_lc)      AS avg_nota_lc,
    AVG(md.nu_nota_mt)      AS avg_nota_mt,
    AVG(md.nu_nota_redacao) AS avg_nota_redacao,
    (AVG(md.nu_nota_cn) + AVG(md.nu_nota_ch) + AVG(md.nu_nota_lc) +
     AVG(md.nu_nota_mt) + AVG(md.nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados md
JOIN enem.estados e ON md.co_uf_prova = e.codigo_uf
GROUP BY md.nu_ano, e.id
WITH DATA;

CREATE MATERIALIZED VIEW enem.mv_evolucao_notas_ano AS
SELECT
    nu_ano,
    AVG(nu_nota_cn)      AS avg_nota_cn,
    AVG(nu_nota_ch)      AS avg_nota_ch,
    AVG(nu_nota_lc)      AS avg_nota_lc,
    AVG(nu_nota_mt)      AS avg_nota_mt,
    AVG(nu_nota_redacao) AS avg_nota_redacao,
    (AVG(nu_nota_cn) + AVG(nu_nota_ch) + AVG(nu_nota_lc) +
     AVG(nu_nota_mt) + AVG(nu_nota_redacao)) / 5 AS nota_total
FROM enem.microdados
GROUP BY nu_ano
WITH DATA;

SELECT * FROM enem.mv_evolucao_notas_estado_ano;
SELECT * FROM enem.mv_evolucao_notas_ano ORDER BY nu_ano, nota_total DESC;

