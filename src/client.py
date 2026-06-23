class Client:
    def __init__(self, client_id, name, country, signup_date):                    # Recibe los datos de un cliente y los almacena en esas variables.
        self.client_id = client_id
        self.name = name
        self.country = country
        self.signup_date = signup_date

    def to_dict(self):                                                            # Convierte cliente en un diccionario con el dict.
        return {
            "client_id": self.client_id,
            "name": self.name,
            "country": self.country,
            "signup_date": self.signup_date
        }
