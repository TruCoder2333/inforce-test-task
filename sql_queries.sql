--Query 1
SELECT signup_date, COUNT(*) as user_count
FROM users_transformed
GROUP BY signup_date
ORDER BY signup_date;

--Query 2
SELECT DISTINCT domain 
FROM users_transformed;

--Query 3
SELECT *
FROM users_transformed
WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days'

--Query 4
WITH domain_counts AS (
    SELECT 
        domain, 
        COUNT(*) AS domain_count
    FROM users_transformed
    GROUP BY domain
    ),
max_count AS (
    SELECT MAX(domain_count) AS max_domain_count
    FROM domain_counts
    )
SELECT u.*
FROM users_transformed u
JOIN domain_counts dc 
    ON u.domain = dc.domain
JOIN max_count mc
    ON dc.domain_count = mc.max_domain_count;

--Query 5
DELETE FROM users_transformed
WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'example.com');