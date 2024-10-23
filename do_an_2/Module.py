import psycopg2

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, db_name, user, password, host, port):
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            return "Connection Successful"
        except Exception as e:
            return f"Connection Failed: {e}"

    def create_table(self, table_name):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    stt SERIAL PRIMARY KEY,
                    mssv VARCHAR(20) NOT NULL,
                    ho_ten VARCHAR(50) NOT NULL,
                    nganh_hoc VARCHAR(50) NOT NULL
                );
            """)
            self.connection.commit()
            return f"Table {table_name} created successfully."
        except Exception as e:
            return f"Failed to create table: {e}"

    def select_table(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name};")
            rows = self.cursor.fetchall()
            return "Success", rows
        except Exception as e:
            return f"Failed to select from table: {e}", []

    def add_entry(self, table_name, mssv, ho_ten, nganh_hoc):
        try:
            self.cursor.execute(f"""
                INSERT INTO {table_name} (mssv, ho_ten, nganh_hoc) VALUES (%s, %s, %s);
            """, (mssv, ho_ten, nganh_hoc))
            self.connection.commit()
            return "Entry added successfully."
        except Exception as e:
            return f"Failed to add entry: {e}"

    def update_entry(self, table_name, mssv, ho_ten, nganh_hoc, stt):
        try:
            self.cursor.execute(f"""
                UPDATE {table_name} SET mssv=%s, ho_ten=%s, nganh_hoc=%s WHERE stt=%s;
            """, (mssv, ho_ten, nganh_hoc, stt))
            self.connection.commit()
            return "Entry updated successfully."
        except Exception as e:
            return f"Failed to update entry: {e}"

    def delete_entry(self, table_name, stt):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE stt=%s;", (stt,))
            self.connection.commit()
            return "Entry deleted successfully."
        except Exception as e:
            return f"Failed to delete entry: {e}"

    def delete_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self.connection.commit()
            return f"Table {table_name} deleted successfully."
        except Exception as e:
            return f"Failed to delete table: {e}"


