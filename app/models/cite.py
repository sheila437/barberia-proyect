import app.database.connect as database

class Cite:
    def __init__(self, id_cite=None, date=None, id_service=None, id_client=None) -> None:
        self.id_cite = id_cite
        self.date = date
        self.id_service = id_service
        self.id_client = id_client
    
    def execute(self, opcion: int):
        with database.connection.cursor() as cursor:
            result_args = cursor.callproc('citas_proceso', (opcion, None, None, self.id_cite, self.date, self.id_service, self.id_client))
            
            p_valido = result_args[1]
            p_error = result_args[2]
            self.id_cite = result_args[3]
            self.date = result_args[4]
            self.id_service = result_args[5]
            self.id_client = result_args[6]
            cites = []

            for result in cursor.stored_results():
                if opcion == 1:
                    cites = result.fetchall()

            database.connection.commit()

        return {
            "valido": p_valido,
            "error": p_error,
            "cites": cites
        }
