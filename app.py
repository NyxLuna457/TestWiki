from flask import Flask
import os
from dotenv import load_dotenv
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home ():
    with open( 'templates/index.html', 'r') as file:
        return file.read()



load_dotenv()

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)