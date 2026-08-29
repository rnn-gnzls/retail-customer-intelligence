-- COHORT RETENTION ANALYSIS

DROP VIEW IF EXISTS vw_cohort_retention;


CREATE VIEW vw_cohort_retention AS

WITH customer_orders AS (

    SELECT DISTINCT
        customerid,
        DATE_TRUNC(
            'month',
            invoicedate
        )::date AS purchase_month
    FROM retail_sales
),

customer_cohorts AS (

    SELECT
        customerid,

        MIN(purchase_month)
            AS cohort_month

    FROM customer_orders

    GROUP BY customerid
),

cohort_activity AS (

    SELECT
        o.customerid,

        c.cohort_month,

        o.purchase_month,

        (
            (
                EXTRACT(
                    YEAR FROM o.purchase_month
                )
                -
                EXTRACT(
                    YEAR FROM c.cohort_month
                )
            ) * 12

            +

            (
                EXTRACT(
                    MONTH FROM o.purchase_month
                )
                -
                EXTRACT(
                    MONTH FROM c.cohort_month
                )
            )
        )::integer AS months_since_first_purchase

    FROM customer_orders o

    JOIN customer_cohorts c
        ON o.customerid = c.customerid
),

cohort_counts AS (

    SELECT
        cohort_month,

        months_since_first_purchase,

        COUNT(
            DISTINCT customerid
        ) AS active_customers

    FROM cohort_activity

    GROUP BY
        cohort_month,
        months_since_first_purchase
),

cohort_sizes AS (

    SELECT
        cohort_month,

        COUNT(
            DISTINCT customerid
        ) AS cohort_customers

    FROM customer_cohorts

    GROUP BY cohort_month
)

SELECT

    cc.cohort_month,

    cc.months_since_first_purchase,

    cs.cohort_customers,

    cc.active_customers,

    ROUND(
        cc.active_customers::numeric
        / cs.cohort_customers
        * 100,
        2
    ) AS retention_rate_pct

FROM cohort_counts cc

JOIN cohort_sizes cs
    ON cc.cohort_month = cs.cohort_month

ORDER BY
    cc.cohort_month,
    cc.months_since_first_purchase;