-- RETAIL CUSTOMER INTELLIGENCE
-- ADVANCED ANALYTICS VIEWS

-- MONTHLY SALES PERFORMANCE
DROP VIEW IF EXISTS vw_monthly_sales;

CREATE VIEW vw_monthly_sales AS

SELECT
    order_month,

    order_year,
    order_month_number,

    COUNT(DISTINCT invoiceno) AS orders,

    COUNT(DISTINCT customerid) AS customers,

    SUM(quantity) AS units_sold,

    ROUND(SUM(revenue), 2) AS revenue,

    ROUND(
        AVG(revenue),
        2
    ) AS avg_transaction_value

FROM retail_sales

GROUP BY
    order_month,
    order_year,
    order_month_number

ORDER BY order_month;


-- CUSTOMER SEGMENT PERFORMANCE
DROP VIEW IF EXISTS vw_customer_segments;

CREATE VIEW vw_customer_segments AS

SELECT
    customer_segment,

    COUNT(*) AS customers,

    ROUND(
        SUM(total_revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(total_revenue),
        2
    ) AS avg_customer_revenue,

    ROUND(
        AVG(total_orders),
        2
    ) AS avg_orders,

    ROUND(
        AVG(recency_days),
        2
    ) AS avg_recency_days,

    ROUND(
        AVG(average_order_value),
        2
    ) AS avg_order_value,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS customer_share_pct

FROM customer_analysis

GROUP BY customer_segment

ORDER BY revenue DESC;


-- PRODUCT PERFORMANCE
DROP VIEW IF EXISTS vw_product_performance;

CREATE VIEW vw_product_performance AS

SELECT
    stockcode,

    MAX(description) AS product,

    SUM(quantity) AS units_sold,

    COUNT(DISTINCT invoiceno) AS orders,

    COUNT(DISTINCT customerid) AS customers,

    ROUND(
        SUM(revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(unitprice),
        2
    ) AS avg_unit_price,

    RANK() OVER (
        ORDER BY SUM(revenue) DESC
    ) AS revenue_rank

FROM retail_sales

GROUP BY stockcode;


-- COUNTRY PERFORMANCE
DROP VIEW IF EXISTS vw_country_performance;

CREATE VIEW vw_country_performance AS

SELECT
    country,

    COUNT(DISTINCT customerid) AS customers,

    COUNT(DISTINCT invoiceno) AS orders,

    SUM(quantity) AS units_sold,

    ROUND(
        SUM(revenue),
        2
    ) AS revenue,

    ROUND(
        SUM(revenue)
        / SUM(SUM(revenue)) OVER ()
        * 100,
        2
    ) AS revenue_share_pct,

    ROUND(
        SUM(revenue)
        / COUNT(DISTINCT customerid),
        2
    ) AS revenue_per_customer

FROM retail_sales

GROUP BY country

ORDER BY revenue DESC;


-- CUSTOMER REVENUE RANKING
DROP VIEW IF EXISTS vw_customer_concentration;

CREATE VIEW vw_customer_concentration AS

WITH ranked_customers AS (

    SELECT
        customerid,

        total_orders,

        total_revenue,

        customer_segment,

        RANK() OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_rank,

        SUM(total_revenue) OVER (
            ORDER BY total_revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_revenue,

        SUM(total_revenue) OVER () AS total_business_revenue

    FROM customer_analysis
)

SELECT
    customerid,

    total_orders,

    ROUND(
        total_revenue,
        2
    ) AS total_revenue,

    customer_segment,

    revenue_rank,

    ROUND(
        cumulative_revenue,
        2
    ) AS cumulative_revenue,

    ROUND(
        cumulative_revenue
        / total_business_revenue
        * 100,
        2
    ) AS cumulative_revenue_pct

FROM ranked_customers;


-- RFM CUSTOMER DETAIL
DROP VIEW IF EXISTS vw_rfm_customers;

CREATE VIEW vw_rfm_customers AS

SELECT
    customerid,

    recency_days,

    frequency,

    monetary,

    r_score,
    f_score,
    m_score,

    rfm_score,
    rfm_total,

    customer_segment,

    total_orders,

    total_revenue,

    average_order_value,

    customer_lifetime_days,

    cohort_month,

    revenue_share_pct

FROM customer_analysis;


-- COHORT CUSTOMER BASE
DROP VIEW IF EXISTS vw_cohort_customers;

CREATE VIEW vw_cohort_customers AS

SELECT
    cohort_month,

    COUNT(*) AS customers,

    ROUND(
        SUM(total_revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(total_revenue),
        2
    ) AS avg_customer_revenue,

    ROUND(
        AVG(total_orders),
        2
    ) AS avg_orders

FROM customer_analysis

GROUP BY cohort_month

ORDER BY cohort_month;


-- CUSTOMER PURCHASE BEHAVIOR
DROP VIEW IF EXISTS vw_purchase_behavior;

CREATE VIEW vw_purchase_behavior AS

SELECT
    day_of_week,

    hour,

    COUNT(DISTINCT invoiceno) AS orders,

    COUNT(DISTINCT customerid) AS customers,

    SUM(quantity) AS units_sold,

    ROUND(
        SUM(revenue),
        2
    ) AS revenue

FROM retail_sales

GROUP BY
    day_of_week,
    hour;


-- EXECUTIVE KPI VIEW
DROP VIEW IF EXISTS vw_executive_kpis;

CREATE VIEW vw_executive_kpis AS

SELECT

    COUNT(DISTINCT invoiceno)
        AS total_orders,

    COUNT(DISTINCT customerid)
        AS total_customers,

    COUNT(DISTINCT stockcode)
        AS total_products,

    COUNT(DISTINCT country)
        AS countries,

    SUM(quantity)
        AS total_units_sold,

    ROUND(
        SUM(revenue),
        2
    ) AS total_revenue,

    ROUND(
        AVG(revenue),
        2
    ) AS avg_transaction_value,

    ROUND(
        SUM(revenue)
        / COUNT(DISTINCT customerid),
        2
    ) AS revenue_per_customer

FROM retail_sales;