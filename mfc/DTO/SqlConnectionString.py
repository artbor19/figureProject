from dataclasses import dataclass
from sqlalchemy import URL


@dataclass
class SqlConnectionString:
    driver: str = "{ODBC Driver 18 for SQL Server}"
    server: str = "localhost"
    database: str = "figure_tracker"
    trusted_connection: str = "yes"
    encrypt: str = "no"

    def get_sql_connection_string(self):
        return (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"Trusted_Connection={self.trusted_connection};"
            f"Encrypt={self.encrypt};"
        )

    def get_sql_alchemy_mssql_connection_string(self):
        return URL.create(
            drivername="mssql+pyodbc",
            query={"odbc_connect": self.get_sql_connection_string()}
        )
