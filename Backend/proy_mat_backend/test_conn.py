# test_conn.py
from dotenv import load_dotenv
from pathlib import Path
import os, pyodbc

# carga .env en la carpeta actual
load_dotenv(Path('.') / '.env')

server = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
pwd = os.getenv('DB_PASS')

# prueba con Driver 18 y TrustServerCertificate=yes
cn18 = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={server},1433;"
    f"Database={db};"
    f"Uid={user};"
    f"Pwd={pwd};"
    "Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=10;"
)
# prueba con Driver 17 (para comparar)
cn17 = cn18.replace("Driver={ODBC Driver 18 for SQL Server};", "Driver={ODBC Driver 17 for SQL Server};")

print(">>> Trying ODBC Driver 18 ...")
try:
    conn = pyodbc.connect(cn18)
    print("Driver 18: Connected OK")
    conn.close()
except Exception as e:
    print("Driver 18: ERROR ->", repr(e))

print("\n>>> Trying ODBC Driver 17 ...")
try:
    conn = pyodbc.connect(cn17)
    print("Driver 17: Connected OK")
    conn.close()
except Exception as e:
    print("Driver 17: ERROR ->", repr(e))
