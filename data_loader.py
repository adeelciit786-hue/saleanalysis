"""
Data Loader Module - Load sales data from CSV and JSON files
"""

import csv
import json
from datetime import datetime
from typing import List
from sales_data import SalesData, Product, Transaction, Customer


class DataLoader:
    """Handles loading data from various file formats"""
    
    def __init__(self, sales_data: SalesData):
        self.sales_data = sales_data
    
    def load_products_from_csv(self, filepath: str) -> None:
        """Load products from a CSV file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    category=row['category'],
                    price=float(row['price'])
                )
                self.sales_data.add_product(product)
    
    def load_transactions_from_csv(self, filepath: str) -> None:
        """Load transactions from a CSV file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction = Transaction(
                    transaction_id=row['transaction_id'],
                    product_id=row['product_id'],
                    customer_id=row['customer_id'],
                    quantity=int(row['quantity']),
                    date=datetime.fromisoformat(row['date']),
                    total_amount=float(row['total_amount'])
                )
                self.sales_data.add_transaction(transaction)
    
    def load_customers_from_csv(self, filepath: str) -> None:
        """Load customers from a CSV file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer = Customer(
                    customer_id=row['customer_id'],
                    name=row['name'],
                    email=row['email'],
                    join_date=datetime.fromisoformat(row['join_date'])
                )
                self.sales_data.add_customer(customer)
    
    def load_products_from_json(self, filepath: str) -> None:
        """Load products from a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                product = Product(
                    product_id=item['product_id'],
                    name=item['name'],
                    category=item['category'],
                    price=float(item['price'])
                )
                self.sales_data.add_product(product)
    
    def load_transactions_from_json(self, filepath: str) -> None:
        """Load transactions from a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                transaction = Transaction(
                    transaction_id=item['transaction_id'],
                    product_id=item['product_id'],
                    customer_id=item['customer_id'],
                    quantity=int(item['quantity']),
                    date=datetime.fromisoformat(item['date']),
                    total_amount=float(item['total_amount'])
                )
                self.sales_data.add_transaction(transaction)
    
    def load_customers_from_json(self, filepath: str) -> None:
        """Load customers from a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                customer = Customer(
                    customer_id=item['customer_id'],
                    name=item['name'],
                    email=item['email'],
                    join_date=datetime.fromisoformat(item['join_date'])
                )
                self.sales_data.add_customer(customer)
