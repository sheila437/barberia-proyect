import app.database.connect as database

class Product:
    def __init__(self, id_product: int = None, name: str = None, description: str = None, price: float = None, stock: int = None):
        self.id = id_product
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description
    
    def execute(self, opcion:int):
        with database.connection.cursor() as cursor:
            result_args = cursor.callproc('productos_abcc', (opcion, None, None, self.id, self.name, self.price, self.stock, self.description))
            
            p_valido = result_args[1]
            p_error = result_args[2]
            self.id = result_args[3]
            self.name = result_args[4]
            self.price = result_args[5]
            self.stock = result_args[6]
            self.description = result_args[7]
    
            products = []
        
            for result in cursor.stored_results():
                for result in result.fetchall():
                    products.append(
                        Product(
                            id_product=result[0],
                            name=result[1],
                            price=result[2],
                            stock=result[3],
                            description=result[4]
                        )
                    )

            database.connection.commit()

        return {
            "valido": p_valido,
            "error": p_error,
            "products": products
        }