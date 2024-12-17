from flask import Flask, render_template
from flask_socketio import SocketIO
import psycopg2
import time
import threading
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Função para conectar ao banco de dados
def get_db_connection():
    return psycopg2.connect(
        host="dpg-ctg5u0hopnds73dllme0-a.oregon-postgres.render.com",
        database="mosquitodb",
        user="mosquitodb_user",
        password="j5uG5nEkVlPhEIIaG4ggrVavmBM2oNyz"
    )

# Função para serializar os dados (converter datetime para string)
def serializar_dados(armadilhas):
    for armadilha in armadilhas:
        for key, value in armadilha.items():
            if isinstance(value, datetime):
                armadilha[key] = value.isoformat()  # Converte datetime para string
    return armadilhas

# Monitoramento do banco de dados em uma thread separada
def monitorar_banco():
    ultima_atualizacao = None
    while True:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM armadilhas WHERE updated_at > %s OR %s IS NULL', (ultima_atualizacao, ultima_atualizacao))
            columns = [desc[0] for desc in cur.description]
            dados = [dict(zip(columns, row)) for row in cur.fetchall()]
            cur.close()
            conn.close()

            if dados:
                # Atualiza o timestamp da última alteração
                ultima_atualizacao = max(item['updated_at'] for item in dados)
                # Serializa os dados e emite o evento para o frontend
                socketio.emit('nova_dados', serializar_dados(dados))

        except Exception as e:
            print("Erro ao monitorar banco de dados:", e)

        time.sleep(5)  # Verifica o banco a cada 5 segundos

# Rota principal
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM armadilhas')
    columns = [desc[0] for desc in cur.description]
    armadilhas = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template('ignorar.html', armadilhas=serializar_dados(armadilhas))

if __name__ == '__main__':
    # Inicia a thread para monitorar o banco
    thread = threading.Thread(target=monitorar_banco)
    thread.start()
    socketio.run(app, debug=True)