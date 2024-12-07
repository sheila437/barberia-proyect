import app.database.connect as database

class Service:
    def __init__(self, id_service: int = None, name: str = None, description: str = None, price: float = None):
        self.id = id_service
        self.name = name
        self.price = price
        self.description = description
    
    def execute(self, opcion: int):
        with database.connection.cursor() as cursor:
            result_args = cursor.callproc('servicios_abcc', (opcion, None, None, self.id, self.name, self.price, self.description))
            
            p_valido = result_args[1]
            p_error = result_args[2]
            self.id = result_args[3]
            self.name = result_args[4]
            self.price = result_args[5]
            self.description = result_args[6]
    
            services = []
        
            for result in cursor.stored_results():
                for result in result.fetchall():
                    services.append(
                        Service(
                            id_service=result[0],
                            name=result[1],
                            price=result[2],
                            description=result[3]
                        )
                    )

            database.connection.commit()

        return {
            "valido": p_valido,
            "error": p_error,
            "services": services
        }
