import json
import pandas as pd

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection


def generate_report():

    with open("data/clients.json", "r", encoding="utf-8") as f:
        clients_data = json.load(f)

    clients = []

    for c in clients_data:
        clients.append(
            Client(
                c["client_id"],
                c["name"],
                c["country"],
                c["signup_date"]
            )
        )

    sales_df = pd.read_csv("data/sales.csv")

    sales = []

    for _, row in sales_df.iterrows():
        sales.append(
            Sale(
                row["sale_id"],
                row["client_id"],
                row["product"],
                row["category"],
                row["amount"],
                row["date"]
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

        average_sale = (
            round(total_spent / sale_count, 2)
            if sale_count > 0
            else 0
        )

        clients_report.append({
            "client_id": client.client_id,
            "name": client.name,
            "total_spent": round(total_spent, 2),
            "sale_count": sale_count,
            "average_sale": average_sale
        })

    top_client_by_country = {}

    for client in clients:

        spent = sales_collection.total_amount_by_client(
            client.client_id
        )

        country = client.country

        if country not in top_client_by_country:
            top_client_by_country[country] = (
                client.name,
                spent
            )
        elif spent > top_client_by_country[country][1]:
            top_client_by_country[country] = (
                client.name,
                spent
            )

    top_client_by_country = {
        country: data[0]
        for country, data in top_client_by_country.items()
    }

    sales_by_category = {}

    for sale in sales:

        if sale.category not in sales_by_category:
            sales_by_category[sale.category] = 0

        sales_by_category[sale.category] += sale.amount

    high_spending_clients = []

    for client in clients:

        spent = sales_collection.total_amount_by_client(
            client.client_id
        )

        if spent > 500:
            high_spending_clients.append(
                client.name
            )

    sales_df["date"] = pd.to_datetime(
        sales_df["date"]
    )

    sales_df["month"] = (
        sales_df["date"]
        .dt.to_period("M")
    )

    monthly_sales = (
        sales_df.groupby("month")["amount"]
        .sum()
        .to_dict()
    )

    monthly_sales = {
        str(k): float(v)
        for k, v in monthly_sales.items()
    }

    report = {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": round(total_revenue, 2)
        },
        "clients": clients_report,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales
    }

    return report
