-- Schema Definition and Star Schema Constraints
CREATE SCHEMA IF NOT EXISTS superstore;

-- Dimension: Customers
CREATE TABLE IF NOT EXISTS superstore.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    segment VARCHAR(50) NOT NULL
);

-- Dimension: Products
CREATE TABLE IF NOT EXISTS superstore.products (
    product_id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL
);

-- Fact Table: Orders
CREATE TABLE IF NOT EXISTS superstore.orders (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL REFERENCES superstore.customers(customer_id),
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    region VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL REFERENCES superstore.products(product_id),
    sales NUMERIC(12, 4) NOT NULL,
    quantity INT NOT NULL,
    discount NUMERIC(6, 4) NOT NULL,
    profit NUMERIC(12, 4) NOT NULL
);