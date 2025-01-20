import psycopg2 as pg

class DatabaseManager:

    def __init__(self):
        pass

    @staticmethod
    def testConnection(host, port, user, password):
        try:
            connection = pg.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
            connection.close()
            return "Connection successful"
        except Exception as e:
            return f"Connection failed: {str(e)}"

    @staticmethod
    def createConnection(host, port, user, password):
        try:
            connection = pg.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
            return connection
        except Exception as e:
            return f"Failed to create connection: {str(e)}"

    @staticmethod
    def deleteConnection(connection):
        try:
            if connection:
                connection.close()
                return "Connection closed successfully!"
            else:
                return "No connection to close"
        except Exception as e:
            return f"Failed to close connection: {str(e)}"
