from flask import Flask, render_template

app = Flask(__name__)  # Cria a aplicação Flask

@app.route('/')  # Define a rota principal ("/")
def home():
    return render_template('ignorar.html')  # Retorna uma mensagem simples

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor com modo debug ativado
