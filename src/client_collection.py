class ClientCollection:                                            # Sirve para guardar una lista de clientes y hacer búsquedas sobre ellos.
    def __init__(self, clients):                                   # Guarda la lista de clientes dentro del objeto.
        self.clients = clients

    def get_client_by_id(self, client_id):                         # Busca un cliente por su ID.
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def clients_by_country(self, country):                         # Devuelve todos los clientes de un pais.
        return [
            client
            for client in self.clients
            if client.country == country
        ]
