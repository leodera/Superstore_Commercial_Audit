# Superstore Commercial Audit

An end-to-end commercial analytics project using Python, Google Sheets, and Power BI to investigate sales performance, profitability, loss-making areas, and the impact of discounting.

---

## Project Overview

This project analyzes a Superstore-style retail dataset to answer key commercial questions:

- How much revenue is the business generating?
- How profitable is the business?
- Where are losses occurring?
- Which categories, sub-categories, products, customers, and regions are contributing to losses?
- How does discounting affect profitability?
- At what level of discount does profit margin deteriorate significantly?
- What actions could management take to improve profitability?

The project combines **Python for data cleaning and analysis**, **Google Sheets for automated data delivery**, and **Power BI for interactive business intelligence and dashboarding**.

---

## Business Questions

The analysis was designed around three main areas.

### 1. Executive Performance

- What are total sales and net profit?
- What is the overall profit margin?
- How many orders and customers does the business have?
- What is the average order value?
- Which categories, regions, and customer segments generate the most sales?
- How are sales and profit changing over time?

### 2. Profit & Loss

- How much profit does the business generate?
- How much total loss is being incurred?
- How many orders are loss-making?
- Which categories and sub-categories are most and least profitable?
- Which regions and customer segments generate the greatest losses?
- Which customers and products are contributing to losses?

### 3. Discount Impact

- How does profitability change as discount levels increase?
- Which discount bands generate the strongest margins?
- At what discount level does profit margin deteriorate?
- Is aggressive discounting contributing to negative profitability?

---

# Data Pipeline

The project follows an automated analytics workflow:

```text
Google Sheets
      │
      ▼
Python Data Cleaning
      │
      ▼
Cleaned Dataset
      │
      ├───────────────┐
      ▼               ▼
Executive        Profit & Loss
Analysis          Analysis
      │               │
      └───────┬───────┘
              ▼
       Discount Analysis
              │
              ▼
      Analysis Outputs
              │
              ▼
       Google Sheets
              │
              ▼
          Power BI
              │
              ▼
      Interactive Dashboard