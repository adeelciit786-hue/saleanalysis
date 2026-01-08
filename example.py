#!/usr/bin/env python3
"""
Example usage of the Sales Analysis application
This script demonstrates how to use the sales analysis API programmatically
"""

from datetime import datetime
from sales_data import SalesData, Product, Transaction, Customer
from sales_analyzer import SalesAnalyzer
from sales_visualizer import SalesVisualizer


def main():
    """Example of using the sales analysis API"""
    
    print("Example: Creating Sales Data Programmatically")
    print("=" * 60)
    
    # Initialize sales data
    sales_data = SalesData()
    
    # Add products
    products = [
        Product("P001", "Gaming Laptop", "Electronics", 1499.99),
        Product("P002", "Office Chair", "Furniture", 299.99),
        Product("P003", "Coffee Machine", "Appliances", 199.99),
    ]
    
    for product in products:
        sales_data.add_product(product)
    
    print(f"✓ Added {len(products)} products")
    
    # Add customers
    customers = [
        Customer("C001", "Alice Johnson", "alice@email.com", datetime(2023, 1, 1)),
        Customer("C002", "Bob Smith", "bob@email.com", datetime(2023, 2, 1)),
    ]
    
    for customer in customers:
        sales_data.add_customer(customer)
    
    print(f"✓ Added {len(customers)} customers")
    
    # Add transactions
    transactions = [
        Transaction("T001", "P001", "C001", 1, datetime(2024, 1, 15), 1499.99),
        Transaction("T002", "P002", "C001", 2, datetime(2024, 1, 16), 599.98),
        Transaction("T003", "P003", "C002", 1, datetime(2024, 2, 10), 199.99),
        Transaction("T004", "P001", "C002", 1, datetime(2024, 2, 20), 1499.99),
    ]
    
    for transaction in transactions:
        sales_data.add_transaction(transaction)
    
    print(f"✓ Added {len(transactions)} transactions")
    print()
    
    # Perform analysis
    analyzer = SalesAnalyzer(sales_data)
    visualizer = SalesVisualizer(analyzer)
    
    # Display results
    print("Analysis Results:")
    print("-" * 60)
    
    total_revenue = analyzer.calculate_total_sales()
    print(f"Total Revenue: ${total_revenue:,.2f}")
    
    total_quantity = analyzer.calculate_total_quantity()
    print(f"Total Items Sold: {total_quantity}")
    
    avg_transaction = analyzer.average_transaction_value()
    print(f"Average Transaction Value: ${avg_transaction:,.2f}")
    
    print()
    
    # Show top products
    top_products = analyzer.top_products(3)
    print("Top Products:")
    for i, (name, revenue) in enumerate(top_products, 1):
        print(f"  {i}. {name}: ${revenue:,.2f}")
    
    print()
    
    # Show category breakdown
    visualizer.display_sales_by_category()
    
    # Show full summary
    visualizer.print_summary()


if __name__ == "__main__":
    main()
