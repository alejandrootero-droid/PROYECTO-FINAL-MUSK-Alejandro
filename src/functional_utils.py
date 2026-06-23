def filter_sales_by_category(sales, category):                           # Filtra las ventas por categoría. -filter- es una función de python para quedarnos solo con lo que queremos de una lista.
    return list(
        filter(
            lambda sale: sale.category == category,
            sales
        )
    )


def filter_sales_by_client(sales, client_id):                            # Lo mismo que la primera funcón pero filtra por la ID del cliente no la categoria del producto.         
    return list(
        filter(
            lambda sale: sale.client_id == client_id,
            sales
        )
    )
