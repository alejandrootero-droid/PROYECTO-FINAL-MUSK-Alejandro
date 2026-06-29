import json                                                                            # Para leer clients.json
import pandas as pd                                                                    # Para trabajar con sales.csv

from src.client import Client                                                          # Importamos nuestras clases: cliente, venta, muchos clientes, muchas ventas
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection


def generate_report():                                                                 # Funcion que genera el informe.

    with open("data/clients.json", "r", encoding="utf-8") as f:                        # Aber clientes y lo convierte en una lista.
        clients_data = json.load(f)

    clients = []                                                                       # Lista vacia.

    for c in clients_data:                                                             # Recorremos todos los clientes.
        clients.append(                                                                # Cada diccionario en un objeto.      
            Client(
                c["client_id"],
                c["name"],
                c["country"],
                c["signup_date"]
            )
        )

    sales_df = pd.read_csv("data/sales.csv")                                           # Cargamos.

    sales = []                                                                         # Lista vacia.

    for _, row in sales_df.iterrows():                                                 # Recorremos cada fila.
        sales.append(                                                                  # Cada fila en un objeto.
            Sale(
                row["sale_id"],
                row["client_id"],
                row["product"],
                row["category"],
                row["amount"],
                row["date"]
            )
        )

    client_collection = ClientCollection(clients)                                      # Creamos las colecciones para trabajar con clientes y ventas.
    sales_collection = SalesCollection(sales)

    total_clients = len(clients)                                                       # Totales.
    total_sales = len(sales)
    total_revenue = sum(sale.amount for sale in sales)                                 # Suma ventas.

    clients_report = []                                                                # Lista vacia informacion cliente.

    for client in clients:                                                             # Recorremos los clientes.

        total_spent = sales_collection.total_amount_by_client(                         # Total gastado.
            client.client_id
        )

        sale_count = len(                                                              # Numero de ventas.
            sales_collection.sales_by_client(
                client.client_id
            )
        )

        average_sale = (                                                               # Media gasto por venta.
            round(total_spent / sale_count, 2)
            if sale_count > 0
            else 0
        )

        clients_report.append({                                                        # Guardamos resultado.
            "client_id": client.client_id,
            "name": client.name,
            "total_spent": round(total_spent, 2),
            "sale_count": sale_count,
            "average_sale": average_sale
        })

    top_client_by_country = {}                                                          # Lista vacia.

    for client in clients:                                                              # Recorremos clientes.

        spent = sales_collection.total_amount_by_client(                                # Calcula cuanto gasta el cliente.
            client.client_id
        )

        country = client.country                                                        # Guardo el pais del cliente.

        if country not in top_client_by_country:                                        # Pregunta si el pais esta o no en el diccionario.
            top_client_by_country[country] = (                                          # Lo guardamos.
                client.name,
                spent
            )
        elif spent > top_client_by_country[country][1]:                                 # Si ya existe. Substituimos al que gasta menos.
            top_client_by_country[country] = (
                client.name,
                spent
            )

    top_client_by_country = {                                                           # Creamos diccionario.
        country: data[0]
        for country, data in top_client_by_country.items()
    }

    sales_by_category = {}

    for sale in sales:                                                                  # Recorremos todas las ventas.

        if sale.category not in sales_by_category:                                      # Comprobamso si la categoria ya existe.
            sales_by_category[sale.category] = 0

        sales_by_category[sale.category] += sale.amount                                 # Sumamos el importe.

    high_spending_clients = []                                                          # Lista vacia.

    for client in clients:                                                              # Recorre clientes.

        spent = sales_collection.total_amount_by_client(                                # Llama al metodo que tenemos el sales collection.
            client.client_id
        )

        if spent > 500:                                                                 # Si se cumple esto.
            high_spending_clients.append(                                               # Añade el nombre del cliente a la lista.
                client.name
            )

    sales_df["date"] = pd.to_datetime(                                                 # Convertir fecha en formato fecha.
        sales_df["date"]
    )

    sales_df["month"] = (                                                              # Creamos una columna con el mes.
        sales_df["date"]                                                               # Trabajo con la columna de fechas, mes.
        .dt.to_period("M")
    )

    monthly_sales = (                                                                  # Agrupamos por mes, sumamos, lo convertimos a diccionario normal.
        sales_df.groupby("month")["amount"]
        .sum()
        .to_dict()
    )

    monthly_sales = {                                                                  # Creamos otro diccionario, convertimos y recorremos.
        str(k): float(v)
        for k, v in monthly_sales.items()
    }

    report = {                                                                         # Informe, creamos diccionario, carpeta donde guardar los resultados del analisis, totales, ventas, etc.
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
