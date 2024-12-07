import app.database.connect as database

class Client:
    def __init__(self, id_client: int = None, name: str = None, email: str = None, password: str = None, last_name_pat: str = None, last_name_mat: str = None, phone: str = None):
        self.id = id_client
        self.name = name
        self.last_name_pat = last_name_pat
        self.last_name_mat = last_name_mat
        self.phone = phone
        self.email = email
        self.password = password

    def execute(self, opcion: int):
        with database.connection.cursor() as cursor:
            result_args = cursor.callproc('clientes_abcc', (opcion, None, None, self.id, self.name, self.last_name_pat, self.last_name_mat, self.phone, self.email, self.password, None))
            
            p_valido = result_args[1]
            p_error = result_args[2]
            self.id = result_args[3]
            self.name = result_args[4]
            self.last_name_pat = result_args[5]
            self.last_name_mat = result_args[6]
            self.phone = result_args[7]
            self.email = result_args[8]
            self.password = result_args[9]
            p_fecha = result_args[10]
    
            clients = []
        
            for result in cursor.stored_results():
                for result in result.fetchall():
                    clients.append(
                        Client(
                            id_client=result[0],
                            name=result[1],
                            last_name_pat=result[2],
                            last_name_mat=result[3],
                            phone=result[4],
                            email=result[5],
                            password=result[6]
                        )
                    )

            database.connection.commit()

        return {
            "valido": p_valido,
            "error": p_error,
            "clients": clients,
            "fecha": p_fecha
        }
