import json
import pandas as pd

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection


def generate_report():

    with open("Datos/clients.json", "r", encoding="utf-8") as f:
        clients_data = json.load(f)

    clients = []

    for c in clients_data:
        clients.append(
            Client(
                c["client_id"],
                c["Nombre"],
                c["país"],
                c["signup_date"]
            )
        )

    sales_df = pd.read_csv("Datos/sales.csv")

    sales = []

    for _, row in sales_df.iterrows():
        sales.append(
            Sale(
                row["sale_id"],
                row["client_id"],
                row["Producto"],
                row["Categoría"],
                row["Cantidad"],
                row["Fecha"]
            )
        )

    client_collection = ClientCollection(clients)
    sales_collection = SalesCollection(sales)
    

    total_clients = len(clients)

    total_sales = len(sales)

    total_revenue = sum(sale.amount for sale in sales)
    

    clients_report = []

    for client in clients:

        total_spent = sales_collection.total_amount_by_client(
            client.client_id
        )

        sale_count = len(
            sales_collection.sales_by_client(
                client.client_id
            )
        )

        if sale_count > 0:
            average_sale = round(
                total_spent / sale_count,
                2
            )
        else:
            average_sale = 0

        clients_report.append({
            "client_id": client.client_id,
            "name": client.name,
            "total_spent": round(total_spent, 2),
            "sale_count": sale_count,
            "average_sale": average_sale
        })



    report = {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": round(total_revenue, 2)
        },
        "clients": clients_report
    }

    return report
