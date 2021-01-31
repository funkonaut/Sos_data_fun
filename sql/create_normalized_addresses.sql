CREATE EXTENSION postal;
CREATE EXTENSION fuzzystrmatch;

-- ADDRESS NORMALIZATION FOR ALL TABLES WITH ADDRESSES: Lok into redoing with FOR loop
-- address table
CREATE TABLE address_normalized_add AS 
  SELECT filing_num, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT filing_num, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', address1, address2, city), 
           state, zip_code))) AS na 
FROM address ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_address_idx ON address_normalized_add USING gin(ts);

-- registered_agent_business
CREATE TABLE ra_business_normalized_add AS 
  SELECT filing_num, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT filing_num, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', address1, address2, city),
           state, zip_code))) AS na 
FROM registered_agent_business ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_ra_business_idx ON ra_business_normalized_add USING gin(ts);

-- registered_agent_personal
CREATE TABLE ra_personal_normalized_add AS 
  SELECT filing_num, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT filing_num, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', address1, address2, city), 
           state, zip_code))) AS na 
FROM registered_agent_personal ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_ra_personal_idx ON ra_personal_normalized_add USING gin(ts);

-- charter_officer_business
CREATE TABLE co_business_normalized_add AS 
  SELECT filing_num, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT filing_num, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', address1, address2, city), 
           state, zip_code))) AS na 
FROM charter_officer_business ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_co_business_idx ON co_business_normalized_add USING gin(ts);

CREATE TABLE co_personal_normalized_add AS 
  SELECT filing_num, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT filing_num, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', address1, address2, city), 
           state, zip_code))) AS na 
FROM charter_officer_personal ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_co_personal_idx ON co_personal_normalized_add USING gin(ts);

-- tcad property address
CREATE TABLE tcad_prop_normalized_add AS 
  SELECT geo_id, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT geo_id, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', st_number, prefix, st_name, suffix, city), 
           'TX', zip))) AS na 
FROM tcad ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_tcad_prop_idx ON tcad_prop_normalized_add USING gin(ts);

-- tcad property address
CREATE TABLE tcad_mail_normalized_add AS 
  SELECT geo_id, 
         na, -- normalized address 
         to_tsvector('simple', na) AS ts -- tsearch address 
  FROM ( 
    SELECT geo_id, 
           unnest(postal_normalize(
           concat_ws(', ', 
             concat_ws(' ', mail_add_1, mail_add_2, mail_add_3, mail_city), 
           mail_state, mail_zip))) AS na 
FROM tcad ) 
AS subq;
-- Create index for fast searching
CREATE INDEX tsv_tcad_mail_idx ON tcad_prop_normalized_add USING gin(ts);

-- Example Search
/*WITH normalized AS (
    SELECT unnest(postal_normalize('SEARCH ADDRESS')) AS na
), tsqueries as (
    SELECT phraseto_tsquery('simple', na) AS ts, na
    FROM normalized
)
SELECT DISTINCT ON (filing_num)
    {TABLE}.*,
    {NORMALIZED_TABLE}.na AS addresses_normalized_na,
    tsqueries.na AS tsqueries_na,
    levenshtein(tsqueries.na, {NORMALIZED_TABLE}.na) AS levenshtein
FROM {TABLE}
JOIN {NOMALIZED_TABLE} USING ({key})
JOIN tsqueries ON ({NORMALIZED_TABLE}.ts @@ tsqueries.ts)
ORDER BY {key};*/

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

-- BUSINESS NAMES/Associations INDEX FOR FAST SEARCHING AND RECORD LINKAGE
--master(name)
--master(dba_name)
--registered_agent_business(business_name)
--charter_officer_businness(business_name)
--charrer_names(name)

-- AGENT NAMES INDEX FOR FAST SEARCHING AND RECORD LINKAGE
--registered_agent_personal(concat_ws(' ', agent_first_name, agent_middle_name, agent_last_name, agent_suffix)
--charter_officer_personal(concat_ws(' ', first_name, middle_name, last_name, suffix))
--associated_entity(associated_entity_name)


