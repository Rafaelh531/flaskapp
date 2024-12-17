from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import psycopg2
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-ctg5u0hopnds73dllme0-a.oregon-postgres.render.com",
        database="mosquitodb",
        user="mosquitodb_user",
        password="j5uG5nEkVlPhEIIaG4ggrVavmBM2oNyz"
    )
    return conn

# Converter armadilhas antes de emitir
def formatar_dados(armadilhas):
    for armadilha in armadilhas:
        if isinstance(armadilha['updated_at'], datetime):
            armadilha['updated_at'] = armadilha['updated_at'].isoformat()
    return armadilhas

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM armadilhas')
    columns = [desc[0] for desc in cur.description]
    armadilhas = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template('ignorar.html', armadilhas=armadilhas)

# Thread para monitorar o banco de dados e enviar dados atualizados
def monitorar_banco():
    print("Iniciando monitoramento do banco...")
    ultima_atualizacao = None
    while True:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT MAX(updated_at) FROM armadilhas')
        atualizacao = cur.fetchone()[0]
        cur.close()
        conn.close()

        if atualizacao != ultima_atualizacao:
            print("Alteração detectada no banco. Emitindo atualização...")
            ultima_atualizacao = atualizacao
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM armadilhas')
            columns = [desc[0] for desc in cur.description]
            armadilhas = [dict(zip(columns, row)) for row in cur.fetchall()]
            cur.close()
            conn.close()
            print(formatar_dados(armadilhas))
            socketio.emit('nova_dados', {'data': formatar_dados(armadilhas)})

        time.sleep(5)  # Checa o banco a cada 5 segundos

if __name__ == '__main__':
    thread = threading.Thread(target=monitorar_banco)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)