"""
Sales Analyzer Module - Core analysis functionality for sales data
"""

from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict
from sales_data import SalesData, Transaction, Product


class SalesAnalyzer:
    """Analyzes sales data and provides insights"""
    
    def __init__(self, sales_data: SalesData):
        self.sales_data = sales_data
    
    def calculate_total_sales(self) -> float:
        """Calculate total sales revenue"""
        return sum(transaction.total_amount for transaction in self.sales_data.transactions)
    
    def calculate_total_quantity(self) -> int:
        """Calculate total quantity of items sold"""
        return sum(transaction.quantity for transaction in self.sales_data.transactions)
    
    def sales_by_product(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate sales statistics by product
        Returns dict with product_id as key and stats (revenue, quantity) as value
        """
        product_stats = defaultdict(lambda: {'revenue': 0.0, 'quantity': 0})
        
        for transaction in self.sales_data.transactions:
            product_stats[transaction.product_id]['revenue'] += transaction.total_amount
            product_stats[transaction.product_id]['quantity'] += transaction.quantity
        
        return dict(product_stats)
    
    def sales_by_category(self) -> Dict[str, float]:
        """Calculate total sales revenue by product category"""
        category_sales = defaultdict(float)
        
        for transaction in self.sales_data.transactions:
            product = self.sales_data.get_product(transaction.product_id)
            if product:
                category_sales[product.category] += transaction.total_amount
        
        return dict(category_sales)
    
    def top_products(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Get top N products by revenue
        Returns list of tuples (product_name, revenue)
        """
        product_sales = self.sales_by_product()
        
        # Create list with product names and revenue
        products_with_revenue = []
        for product_id, stats in product_sales.items():
            product = self.sales_data.get_product(product_id)
            if product:
                products_with_revenue.append((product.name, stats['revenue']))
        
        # Sort by revenue and return top N
        products_with_revenue.sort(key=lambda x: x[1], reverse=True)
        return products_with_revenue[:n]
    
    def sales_by_customer(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate sales statistics by customer
        Returns dict with customer_id as key and stats as value
        """
        customer_stats = defaultdict(lambda: {'revenue': 0.0, 'transactions': 0})
        
        for transaction in self.sales_data.transactions:
            customer_stats[transaction.customer_id]['revenue'] += transaction.total_amount
            customer_stats[transaction.customer_id]['transactions'] += 1
        
        return dict(customer_stats)
    
    def top_customers(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Get top N customers by revenue
        Returns list of tuples (customer_name, revenue)
        """
        customer_sales = self.sales_by_customer()
        
        # Create list with customer names and revenue
        customers_with_revenue = []
        for customer_id, stats in customer_sales.items():
            customer = self.sales_data.get_customer(customer_id)
            if customer:
                customers_with_revenue.append((customer.name, stats['revenue']))
        
        # Sort by revenue and return top N
        customers_with_revenue.sort(key=lambda x: x[1], reverse=True)
        return customers_with_revenue[:n]
    
    def sales_by_date(self) -> Dict[str, float]:
        """Calculate daily sales revenue"""
        daily_sales = defaultdict(float)
        
        for transaction in self.sales_data.transactions:
            date_key = transaction.date.strftime('%Y-%m-%d')
            daily_sales[date_key] += transaction.total_amount
        
        return dict(daily_sales)
    
    def sales_by_month(self) -> Dict[str, float]:
        """Calculate monthly sales revenue"""
        monthly_sales = defaultdict(float)
        
        for transaction in self.sales_data.transactions:
            month_key = transaction.date.strftime('%Y-%m')
            monthly_sales[month_key] += transaction.total_amount
        
        return dict(monthly_sales)
    
    def average_transaction_value(self) -> float:
        """Calculate average transaction value"""
        if not self.sales_data.transactions:
            return 0.0
        return self.calculate_total_sales() / len(self.sales_data.transactions)
    
    def get_summary(self) -> Dict[str, any]:
        """Get a comprehensive summary of sales data"""
        return {
            'total_revenue': self.calculate_total_sales(),
            'total_quantity': self.calculate_total_quantity(),
            'total_transactions': len(self.sales_data.transactions),
            'total_products': len(self.sales_data.products),
            'total_customers': len(self.sales_data.customers),
            'average_transaction_value': self.average_transaction_value(),
            'top_products': self.top_products(3),
            'top_customers': self.top_customers(3)
        }
