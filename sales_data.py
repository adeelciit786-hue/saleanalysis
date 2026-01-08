"""
Sales Data Module - Contains data models and structures for sale analysis
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Product:
    """Represents a product in the inventory"""
    product_id: str
    name: str
    category: str
    price: float


@dataclass
class Transaction:
    """Represents a sales transaction"""
    transaction_id: str
    product_id: str
    customer_id: str
    quantity: int
    date: datetime
    total_amount: float


@dataclass
class Customer:
    """Represents a customer"""
    customer_id: str
    name: str
    email: str
    join_date: datetime


class SalesData:
    """Container for all sales-related data"""
    
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.transactions: List[Transaction] = []
        self.customers: Dict[str, Customer] = {}
    
    def add_product(self, product: Product) -> None:
        """Add a product to the catalog"""
        self.products[product.product_id] = product
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the records"""
        self.transactions.append(transaction)
    
    def add_customer(self, customer: Customer) -> None:
        """Add a customer to the database"""
        self.customers[customer.customer_id] = customer
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID"""
        return self.products.get(product_id)
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID"""
        return self.customers.get(customer_id)
    
    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions"""
        return self.transactions
