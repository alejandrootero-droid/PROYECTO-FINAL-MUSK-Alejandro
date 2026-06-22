import json
import pandas as pd

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection


def generate_report():

    # -------------------------
    # Cargar clientes JSON
    # -------------------------
    with open("Datos/clients.json", "r", encoding="utf-8") as f:
        clients_data = json.load(f)

    clients = []

    for c in clients_data:
        client = Client(
            c["client_id"],
            c["name"],
            c["country"],
            c["signup_date"]
        )
        clients.append(client)

    # -------------------------
    # Cargar ventas CSV
    # -------------------------
    sales_df = pd.read_csv("Datos/sales.csv")

    sales = []

    for _, row in sales_df.iterrows():

        sale = Sale(
            row["sale_id"],
            row["client_id"],
            row["product"],
            row["category"],
            row["amount"],
            row["date"]
        )

        sales.append(sale)

    client_collection = ClientCollection(clients)
    sales_collection = SalesCollection(sales)

    return {}
