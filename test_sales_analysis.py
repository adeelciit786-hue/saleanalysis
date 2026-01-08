"""
Unit tests for Sales Analysis Application
"""

import unittest
from datetime import datetime
from sales_data import SalesData, Product, Transaction, Customer
from sales_analyzer import SalesAnalyzer
from data_loader import DataLoader
import tempfile
import os


class TestSalesData(unittest.TestCase):
    """Test cases for SalesData class"""
    
    def setUp(self):
        """Set up test data"""
        self.sales_data = SalesData()
    
    def test_add_product(self):
        """Test adding a product"""
        product = Product("P001", "Test Product", "Electronics", 99.99)
        self.sales_data.add_product(product)
        
        self.assertEqual(len(self.sales_data.products), 1)
        self.assertEqual(self.sales_data.get_product("P001").name, "Test Product")
    
    def test_add_transaction(self):
        """Test adding a transaction"""
        transaction = Transaction(
            "T001", "P001", "C001", 2, 
            datetime(2024, 1, 1), 199.98
        )
        self.sales_data.add_transaction(transaction)
        
        self.assertEqual(len(self.sales_data.transactions), 1)
        self.assertEqual(self.sales_data.transactions[0].quantity, 2)
    
    def test_add_customer(self):
        """Test adding a customer"""
        customer = Customer(
            "C001", "John Doe", "john@example.com",
            datetime(2023, 1, 1)
        )
        self.sales_data.add_customer(customer)
        
        self.assertEqual(len(self.sales_data.customers), 1)
        self.assertEqual(self.sales_data.get_customer("C001").name, "John Doe")


class TestSalesAnalyzer(unittest.TestCase):
    """Test cases for SalesAnalyzer class"""
    
    def setUp(self):
        """Set up test data"""
        self.sales_data = SalesData()
        
        # Add test products
        self.sales_data.add_product(Product("P001", "Laptop", "Electronics", 1000.00))
        self.sales_data.add_product(Product("P002", "Mouse", "Electronics", 25.00))
        self.sales_data.add_product(Product("P003", "Desk", "Furniture", 300.00))
        
        # Add test customers
        self.sales_data.add_customer(Customer("C001", "John Doe", "john@email.com", datetime(2023, 1, 1)))
        self.sales_data.add_customer(Customer("C002", "Jane Smith", "jane@email.com", datetime(2023, 1, 1)))
        
        # Add test transactions
        self.sales_data.add_transaction(
            Transaction("T001", "P001", "C001", 1, datetime(2024, 1, 5), 1000.00)
        )
        self.sales_data.add_transaction(
            Transaction("T002", "P002", "C001", 2, datetime(2024, 1, 6), 50.00)
        )
        self.sales_data.add_transaction(
            Transaction("T003", "P003", "C002", 1, datetime(2024, 2, 10), 300.00)
        )
        
        self.analyzer = SalesAnalyzer(self.sales_data)
    
    def test_calculate_total_sales(self):
        """Test total sales calculation"""
        total = self.analyzer.calculate_total_sales()
        self.assertEqual(total, 1350.00)
    
    def test_calculate_total_quantity(self):
        """Test total quantity calculation"""
        total_qty = self.analyzer.calculate_total_quantity()
        self.assertEqual(total_qty, 4)
    
    def test_sales_by_product(self):
        """Test sales by product"""
        product_sales = self.analyzer.sales_by_product()
        
        self.assertEqual(product_sales["P001"]["revenue"], 1000.00)
        self.assertEqual(product_sales["P001"]["quantity"], 1)
        self.assertEqual(product_sales["P002"]["revenue"], 50.00)
        self.assertEqual(product_sales["P002"]["quantity"], 2)
    
    def test_sales_by_category(self):
        """Test sales by category"""
        category_sales = self.analyzer.sales_by_category()
        
        self.assertEqual(category_sales["Electronics"], 1050.00)
        self.assertEqual(category_sales["Furniture"], 300.00)
    
    def test_top_products(self):
        """Test top products"""
        top_products = self.analyzer.top_products(2)
        
        self.assertEqual(len(top_products), 2)
        self.assertEqual(top_products[0][0], "Laptop")
        self.assertEqual(top_products[0][1], 1000.00)
    
    def test_sales_by_customer(self):
        """Test sales by customer"""
        customer_sales = self.analyzer.sales_by_customer()
        
        self.assertEqual(customer_sales["C001"]["revenue"], 1050.00)
        self.assertEqual(customer_sales["C001"]["transactions"], 2)
        self.assertEqual(customer_sales["C002"]["revenue"], 300.00)
    
    def test_top_customers(self):
        """Test top customers"""
        top_customers = self.analyzer.top_customers(2)
        
        self.assertEqual(len(top_customers), 2)
        self.assertEqual(top_customers[0][0], "John Doe")
        self.assertEqual(top_customers[0][1], 1050.00)
    
    def test_sales_by_month(self):
        """Test sales by month"""
        monthly_sales = self.analyzer.sales_by_month()
        
        self.assertEqual(monthly_sales["2024-01"], 1050.00)
        self.assertEqual(monthly_sales["2024-02"], 300.00)
    
    def test_average_transaction_value(self):
        """Test average transaction value"""
        avg = self.analyzer.average_transaction_value()
        self.assertEqual(avg, 450.00)
    
    def test_get_summary(self):
        """Test summary generation"""
        summary = self.analyzer.get_summary()
        
        self.assertEqual(summary["total_revenue"], 1350.00)
        self.assertEqual(summary["total_quantity"], 4)
        self.assertEqual(summary["total_transactions"], 3)
        self.assertEqual(summary["total_products"], 3)
        self.assertEqual(summary["total_customers"], 2)


class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader class"""
    
    def setUp(self):
        """Set up test data"""
        self.sales_data = SalesData()
        self.loader = DataLoader(self.sales_data)
    
    def test_load_products_from_csv(self):
        """Test loading products from CSV"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write("product_id,name,category,price\n")
            f.write("P001,Test Product,Electronics,99.99\n")
            f.write("P002,Another Product,Furniture,199.99\n")
            temp_file = f.name
        
        try:
            self.loader.load_products_from_csv(temp_file)
            
            self.assertEqual(len(self.sales_data.products), 2)
            self.assertEqual(self.sales_data.get_product("P001").name, "Test Product")
            self.assertEqual(self.sales_data.get_product("P002").price, 199.99)
        finally:
            os.unlink(temp_file)
    
    def test_load_transactions_from_csv(self):
        """Test loading transactions from CSV"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write("transaction_id,product_id,customer_id,quantity,date,total_amount\n")
            f.write("T001,P001,C001,2,2024-01-05T10:00:00,199.98\n")
            temp_file = f.name
        
        try:
            self.loader.load_transactions_from_csv(temp_file)
            
            self.assertEqual(len(self.sales_data.transactions), 1)
            self.assertEqual(self.sales_data.transactions[0].quantity, 2)
        finally:
            os.unlink(temp_file)
    
    def test_load_customers_from_csv(self):
        """Test loading customers from CSV"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write("customer_id,name,email,join_date\n")
            f.write("C001,John Doe,john@email.com,2023-01-01T00:00:00\n")
            temp_file = f.name
        
        try:
            self.loader.load_customers_from_csv(temp_file)
            
            self.assertEqual(len(self.sales_data.customers), 1)
            self.assertEqual(self.sales_data.get_customer("C001").name, "John Doe")
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
