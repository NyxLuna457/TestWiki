from flask import Flask, render_template
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

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/')
def afficher_personnes():
    try:
        conn = mariadb.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT id, Prénoms, Nom FROM Personel;")
        personnes = cur.fetchall()
        conn.close()
    except mariadb.Error as e:
        return f"<h1>Erreur de connexion à la base de données :</h1><pre>{e}</pre>"

    # Template HTML simple
    html = '''
    <h1>Liste du Personel</h1>
    <table border="1">
        <tr>
            <th>ID</th><th>Nom</th><th>Prénom</th><th>Âge</th><th>Job</th>
        </tr>
        {% for p in personnes %}
        <tr>
            <td>{{ p[0] }}</td>
            <td>{{ p[1] }}</td>
            <td>{{ p[2] }}</td>
            <td>{{ p[3] }}</td>
            <td>{{ p[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    '''
    return render_template_string(html, personnes=personnes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)