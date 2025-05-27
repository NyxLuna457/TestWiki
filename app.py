from flask import Flask, render_template_string
import os
from dotenv import load_dotenv
import mariadb
from prometheus_flask_exporter import PrometheusMetrics

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Initialiser Prometheus Metrics (cela ajoute la route /metrics automatiquement)
metrics = PrometheusMetrics(app)

# Config DB unique
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/')
def home():
    # Affiche la page d'accueil depuis un template HTML
    try:
        with open('templates/index.html', 'r') as file:
            return file.read()
    except Exception as e:
        return f"<h1>Erreur lors de la lecture du template :</h1><pre>{e}</pre>"

@app.route('/personnes')
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
    <h1>Liste du Personnel</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Prénoms</th>
            <th>Nom</th>
        </tr>
        {% for p in personnes %}
        <tr>
            <td>{{ p[0] }}</td>
            <td>{{ p[1] }}</td>
            <td>{{ p[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    '''
    return render_template_string(html, personnes=personnes)

# La route /metrics est gérée automatiquement par PrometheusMetrics

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
