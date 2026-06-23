class Sale:
    def __init__(self, sale_id, client_id, product, category, amount, date):                   # Recibe los datos de una ventana y los guarda en las variables.
        self.sale_id = sale_id
        self.client_id = client_id
        self.product = product
        self.category = category
        self.amount = amount
        self.date = date

    def to_dict(self):                                                                         # Convierte los objetos en diccionarios.
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": self.date
        }
