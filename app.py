from flask imnport Flask, render_template
import os
from dotenv import load_dotenv
import mysql.connector
import os
import mariadb

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home ():
    with open( 'templates/index.html', 'r') as file:
        return file.read()

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    if connection.is_connected():
        print("✅ Connexion réussie à MariaDB")
except mysql.connector.Error as e:
    print(f"❌ Erreur de connexion : {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()


app = Flask(__name__)

def get_db_connection():
    return mariadb.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    # On récupère les données de la table Personel
    cur.execute("SELECT id, Prénoms, lastname FROM Personel")
    # On transforme les résultats en liste de dictionnaires pour un accès plus lisible dans le template
    Personel = [
        {"id": row[0], "Prénoms": row[1], "lastname": row[2]}
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return render_template('index.html', Personel=Personel)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)