-- RETAIL CUSTOMER INTELLIGENCE
-- DATABASE SCHEMA

DROP TABLE IF EXISTS customer_analysis;
DROP TABLE IF EXISTS retail_sales;

-- TRANSACTION TABLE
CREATE TABLE retail_sales (
    invoiceno VARCHAR(20),
    stockcode VARCHAR(50),
    description TEXT,
    quantity INTEGER,
    invoicedate TIMESTAMP,
    unitprice NUMERIC(12,2),
    customerid INTEGER,
    country VARCHAR(100),

    invoice_str VARCHAR(20),
    is_cancellation BOOLEAN,
    is_negative_quantity BOOLEAN,

    revenue NUMERIC(14,2),

    order_date DATE,
    order_month VARCHAR(7),
    order_year INTEGER,
    order_month_number INTEGER,
    day_of_week VARCHAR(20),
    hour INTEGER,

    first_purchase_date DATE,
    last_purchase_date DATE,
    first_purchase_month VARCHAR(7),

    customer_order_count INTEGER,
    customer_type VARCHAR(30)
);

-- CUSTOMER ANALYTICS TABLE
CREATE TABLE customer_analysis (
    customer_id INTEGER PRIMARY KEY,

    first_purchase_date TIMESTAMP,
    last_purchase_date TIMESTAMP,

    total_orders INTEGER,
    total_items INTEGER,
    total_revenue NUMERIC(14,2),
    average_order_value NUMERIC(14,2),

    unique_products INTEGER,
    unique_categories INTEGER,
    unique_countries INTEGER,

    recency_days INTEGER,
    frequency INTEGER,
    monetary NUMERIC(14,2),

    customer_lifetime_days INTEGER,

    customer_type VARCHAR(30),

    r_score INTEGER,
    f_score INTEGER,
    m_score INTEGER,

    rfm_score VARCHAR(10),
    rfm_total INTEGER,

    customer_segment VARCHAR(50),

    cohort_month VARCHAR(7),
    first_purchase_year INTEGER,

    revenue_share_pct NUMERIC(8,4)
);