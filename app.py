from flask import Flask, render_template
import psycopg2

app = Flask(__name__)  # Cria a aplicação Flask

def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-ctg5u0hopnds73dllme0-a.oregon-postgres.render.com",
        database="mosquitodb",
        user="mosquitodb_user",
        password="j5uG5nEkVlPhEIIaG4ggrVavmBM2oNyz"
    )
    return conn

@app.route('/')  # Define a rota principal ("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM armadilhas')
    columns = [desc[0] for desc in cur.description]
    armadilhas = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template('ignorar.html', armadilhas=armadilhas)  # Passa os dados para o template

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor com modo debug ativado
