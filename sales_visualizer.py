"""
Visualization Module - Create charts and visualizations for sales data
"""

from typing import Dict, List
from sales_analyzer import SalesAnalyzer


class SalesVisualizer:
    """Creates text-based visualizations for sales data"""
    
    def __init__(self, analyzer: SalesAnalyzer):
        self.analyzer = analyzer
    
    def print_bar_chart(self, data: Dict[str, float], title: str, max_width: int = 50) -> None:
        """Print a horizontal bar chart"""
        if not data:
            print(f"\n{title}\nNo data available.\n")
            return
        
        print(f"\n{title}")
        print("=" * (max_width + 30))
        
        max_value = max(data.values()) if data else 1
        
        for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
            bar = "█" * bar_length
            print(f"{label[:20]:20} | {bar} ${value:,.2f}")
        print()
    
    def print_top_items(self, items: List[tuple], title: str) -> None:
        """Print a list of top items"""
        if not items:
            print(f"\n{title}\nNo data available.\n")
            return
        
        print(f"\n{title}")
        print("=" * 60)
        for i, (name, value) in enumerate(items, 1):
            print(f"{i}. {name[:35]:35} ${value:,.2f}")
        print()
    
    def print_summary(self) -> None:
        """Print a comprehensive summary of sales data"""
        summary = self.analyzer.get_summary()
        
        print("\n" + "=" * 60)
        print("SALES ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"\nTotal Revenue:           ${summary['total_revenue']:,.2f}")
        print(f"Total Quantity Sold:     {summary['total_quantity']:,}")
        print(f"Total Transactions:      {summary['total_transactions']:,}")
        print(f"Total Products:          {summary['total_products']:,}")
        print(f"Total Customers:         {summary['total_customers']:,}")
        print(f"Average Transaction:     ${summary['average_transaction_value']:,.2f}")
        
        self.print_top_items(summary['top_products'], "\nTOP 3 PRODUCTS BY REVENUE")
        self.print_top_items(summary['top_customers'], "TOP 3 CUSTOMERS BY REVENUE")
    
    def display_sales_by_category(self) -> None:
        """Display sales by product category"""
        category_sales = self.analyzer.sales_by_category()
        self.print_bar_chart(category_sales, "SALES BY CATEGORY")
    
    def display_monthly_sales(self) -> None:
        """Display monthly sales"""
        monthly_sales = self.analyzer.sales_by_month()
        self.print_bar_chart(monthly_sales, "MONTHLY SALES")
    
    def display_daily_sales(self) -> None:
        """Display daily sales"""
        daily_sales = self.analyzer.sales_by_date()
        # Limit to recent days if too many
        if len(daily_sales) > 10:
            sorted_dates = sorted(daily_sales.items(), reverse=True)[:10]
            daily_sales = dict(sorted_dates)
        self.print_bar_chart(daily_sales, "DAILY SALES (Recent)")
