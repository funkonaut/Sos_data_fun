CREATE EXTENSION postal;
CREATE EXTENSION fuzzystrmatch;

-- ADDRESS NORMALIZATION FOR ALL TABLES WITH ADDRESSES:
-- address table
CREATE TABLE address_normalized AS 
  SELECT filing_number, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT filing_number, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', unit, number, street), --FIX
           'NEW YORK', postcode))) AS na 
FROM address ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_address_idx ON address USING gin(ts);


-- Example Search
/*WITH normalized AS (
    SELECT unnest(postal_normalize('388 Greenwich st, ny')) AS na
), tsqueries as (
    SELECT phraseto_tsquery('simple', na) AS ts, na
    FROM normalized
)
SELECT DISTINCT ON (pk)
    addresses.*,
    addresses_normalized.na AS addresses_normalized_na,
    tsqueries.na AS tsqueries_na,
    levenshtein(tsqueries.na, addresses_normalized.na) AS levenshtein
FROM addresses
JOIN addresses_normalized USING (pk)
JOIN tsqueries ON (addresses_normalized.ts @@ tsqueries.ts)
ORDER BY pk;*/

-- Example Join
/*WITH queries AS (
    SELECT
        name as health_name,
        address as health_address,
        phraseto_tsquery('simple', unnest(postal_normalize(concat_ws(', ', address, 'new york')))) AS tsq
    FROM health_centers
)
SELECT
    addresses.*,
    addresses_normalized.*,
    queries.health_name,
    queries.health_address
FROM addresses
JOIN addresses_normalized using (pk)
JOIN queries ON (addresses_normalized.ts @@ queries.tsq);*/
