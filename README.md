# Sale Analysis

A comprehensive Python-based sales analysis application that helps you analyze sales data, generate insights, and visualize results.

## Features

- **Data Management**: Load sales data from CSV or JSON files
- **Sales Analytics**: 
  - Calculate total sales revenue and quantity
  - Analyze sales by product, category, and customer
  - Identify top-performing products and customers
  - Track daily and monthly sales trends
  - Calculate average transaction values
- **Visualizations**: Text-based charts and reports for easy understanding
- **Flexible Data Input**: Support for CSV and JSON formats
- **Command-Line Interface**: Easy-to-use CLI for quick analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/adeelciit786-hue/saleanalysis.git
cd saleanalysis
```

2. Install dependencies (optional, no external dependencies required for basic functionality):
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start with Demo Data

Run the application with sample data:

```bash
python main.py --demo
```

### Using Custom Data Files

Analyze your own sales data:

```bash
python main.py --products products.csv --transactions transactions.csv --customers customers.csv
```

### Generate Specific Reports

Generate only summary report:
```bash
python main.py --demo --report summary
```

Generate category analysis:
```bash
python main.py --demo --report categories
```

Generate monthly sales report:
```bash
python main.py --demo --report monthly
```

Available report types:
- `summary` - Overview with key metrics and top performers
- `categories` - Sales breakdown by product category
- `monthly` - Monthly sales trends
- `daily` - Daily sales (recent days)
- `all` - All reports (default)

### Using JSON Files

The application also supports JSON format:

```bash
python main.py --products products.json --transactions transactions.json --customers customers.json
```

## Data Format

### Products CSV Format
```csv
product_id,name,category,price
P001,Laptop Pro 15,Electronics,1299.99
P002,Wireless Mouse,Electronics,29.99
```

### Transactions CSV Format
```csv
transaction_id,product_id,customer_id,quantity,date,total_amount
T001,P001,C001,1,2024-01-05T10:30:00,1299.99
T002,P002,C001,2,2024-01-05T10:30:00,59.98
```

### Customers CSV Format
```csv
customer_id,name,email,join_date
C001,John Smith,john.smith@email.com,2023-01-15T00:00:00
C002,Sarah Johnson,sarah.j@email.com,2023-02-20T00:00:00
```

## Project Structure

```
saleanalysis/
├── main.py                 # CLI entry point
├── example.py             # Example usage script
├── sales_data.py          # Data models and structures
├── sales_analyzer.py      # Core analysis logic
├── data_loader.py         # Data loading utilities
├── sales_visualizer.py    # Visualization and reporting
├── test_sales_analysis.py # Unit tests
├── data/                  # Sample data files
│   ├── products.csv
│   ├── transactions.csv
│   └── customers.csv
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Programmatic Usage

You can also use the sales analysis API directly in your Python code:

```python
from datetime import datetime
from sales_data import SalesData, Product, Transaction, Customer
from sales_analyzer import SalesAnalyzer

# Create sales data
sales_data = SalesData()

# Add products
sales_data.add_product(Product("P001", "Laptop", "Electronics", 1299.99))

# Add customers
sales_data.add_customer(Customer("C001", "John Doe", "john@email.com", datetime.now()))

# Add transactions
sales_data.add_transaction(Transaction("T001", "P001", "C001", 1, datetime.now(), 1299.99))

# Analyze
analyzer = SalesAnalyzer(sales_data)
total_revenue = analyzer.calculate_total_sales()
print(f"Total Revenue: ${total_revenue:,.2f}")
```

See `example.py` for a complete working example.

## Running Tests

Run the unit tests:

```bash
python -m pytest test_sales_analysis.py -v
```

Or using Python's unittest:

```bash
python -m unittest test_sales_analysis.py
```

## Example Output

```
============================================================
SALES ANALYSIS SUMMARY
============================================================

Total Revenue:           $21,459.52
Total Quantity Sold:     58
Total Transactions:      40
Total Products:          15
Total Customers:         10
Average Transaction:     $536.49

TOP 3 PRODUCTS BY REVENUE
============================================================
1. Laptop Pro 15                    $5,199.96
2. Smartphone X                     $3,599.96
3. Standing Desk                    $1,999.96

TOP 3 CUSTOMERS BY REVENUE
============================================================
1. John Smith                       $2,889.93
2. James Taylor                     $1,259.95
3. Michael Brown                    $1,449.96
```

## Features Overview

### Sales Analysis Capabilities

- **Total Revenue Calculation**: Get overall sales performance
- **Product Analysis**: Identify best-selling products and categories
- **Customer Insights**: Find top customers and analyze purchase patterns
- **Time-based Analysis**: Track sales trends over time (daily, monthly)
- **Performance Metrics**: Average transaction value, total quantities sold

### Data Models

- **Product**: Represents items in your inventory with pricing
- **Transaction**: Records of individual sales
- **Customer**: Customer information and purchase history

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational and commercial use.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
