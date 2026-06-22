def filter_sales_by_category(sales, category):
    return list(
        filter(
            lambda sale: sale.category == category,
            sales
        )
    )


def filter_sales_by_client(sales, client_id):
    return list(
        filter(
            lambda sale: sale.client_id == client_id,
            sales
        )
    )
