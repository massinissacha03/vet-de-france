import psycopg2
import psycopg2.extras
import os

# connexion à la base postgres
def connect():
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'postgres'),
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', ''),
        cursor_factory=psycopg2.extras.NamedTupleCursor  # pour avoir des objets avec attributs
    )
    conn.autocommit = True  # commit auto après chaque requête
    return conn