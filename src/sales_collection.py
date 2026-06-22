class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        return [
            sale
            for sale in self.sales
            if sale.client_id == client_id
        ]

    def total_amount_by_client(self, client_id):
        return sum(
            sale.amount
            for sale in self.sales
            if sale.client_id == client_id
        )

    def total_amount_by_category(self, category):
        return sum(
            sale.amount
            for sale in self.sales
            if sale.category == category
        )

    def average_sale_by_client(self, client_id):
        client_sales = self.sales_by_client(client_id)

        if len(client_sales) == 0:
            return 0

        return (
            self.total_amount_by_client(client_id)
            / len(client_sales)
        )
