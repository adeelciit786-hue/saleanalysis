#!/usr/bin/env python3
"""
Sale Analysis - Command Line Interface
Main entry point for the sales analysis application
"""

import sys
import argparse
from pathlib import Path
from sales_data import SalesData
from data_loader import DataLoader
from sales_analyzer import SalesAnalyzer
from sales_visualizer import SalesVisualizer


def main():
    """Main function to run the sales analysis"""
    parser = argparse.ArgumentParser(
        description='Sales Analysis Tool - Analyze sales data and generate insights'
    )
    
    parser.add_argument(
        '--products',
        type=str,
        help='Path to products CSV or JSON file'
    )
    
    parser.add_argument(
        '--transactions',
        type=str,
        help='Path to transactions CSV or JSON file'
    )
    
    parser.add_argument(
        '--customers',
        type=str,
        help='Path to customers CSV or JSON file'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run with demo data'
    )
    
    parser.add_argument(
        '--report',
        type=str,
        choices=['summary', 'categories', 'monthly', 'daily', 'all'],
        default='all',
        help='Type of report to generate (default: all)'
    )
    
    args = parser.parse_args()
    
    # Initialize sales data
    sales_data = SalesData()
    loader = DataLoader(sales_data)
    
    # Load data
    if args.demo:
        print("Running with demo data from 'data/' directory...")
        demo_data_dir = Path('data')
        if not demo_data_dir.exists():
            print("Error: Demo data directory 'data/' not found.")
            print("Please create sample data files or specify custom data files.")
            return 1
        
        try:
            products_file = demo_data_dir / 'products.csv'
            transactions_file = demo_data_dir / 'transactions.csv'
            customers_file = demo_data_dir / 'customers.csv'
            
            if products_file.exists():
                loader.load_products_from_csv(str(products_file))
                print(f"✓ Loaded products from {products_file}")
            
            if transactions_file.exists():
                loader.load_transactions_from_csv(str(transactions_file))
                print(f"✓ Loaded transactions from {transactions_file}")
            
            if customers_file.exists():
                loader.load_customers_from_csv(str(customers_file))
                print(f"✓ Loaded customers from {customers_file}")
        
        except Exception as e:
            print(f"Error loading demo data: {e}")
            return 1
    
    else:
        # Load custom data files
        try:
            if args.products:
                if args.products.endswith('.json'):
                    loader.load_products_from_json(args.products)
                else:
                    loader.load_products_from_csv(args.products)
                print(f"✓ Loaded products from {args.products}")
            
            if args.transactions:
                if args.transactions.endswith('.json'):
                    loader.load_transactions_from_json(args.transactions)
                else:
                    loader.load_transactions_from_csv(args.transactions)
                print(f"✓ Loaded transactions from {args.transactions}")
            
            if args.customers:
                if args.customers.endswith('.json'):
                    loader.load_customers_from_json(args.customers)
                else:
                    loader.load_customers_from_csv(args.customers)
                print(f"✓ Loaded customers from {args.customers}")
        
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return 1
        except Exception as e:
            print(f"Error loading data: {e}")
            return 1
    
    # Check if we have data to analyze
    if not sales_data.transactions:
        print("\nNo transaction data loaded. Please provide transaction data to analyze.")
        print("Use --demo flag to use sample data or specify data files with --transactions")
        return 1
    
    # Perform analysis
    analyzer = SalesAnalyzer(sales_data)
    visualizer = SalesVisualizer(analyzer)
    
    # Generate reports based on user selection
    print("\n" + "=" * 60)
    print("GENERATING SALES ANALYSIS REPORTS")
    print("=" * 60)
    
    if args.report in ['summary', 'all']:
        visualizer.print_summary()
    
    if args.report in ['categories', 'all']:
        visualizer.display_sales_by_category()
    
    if args.report in ['monthly', 'all']:
        visualizer.display_monthly_sales()
    
    if args.report in ['daily', 'all']:
        visualizer.display_daily_sales()
    
    print("=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
