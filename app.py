
# Importa as bibliotecas necessárias
# Flask é o microframework para web e pyodbc é usado para conectar ao SQL Server
from flask import Flask, request, render_template
import pyodbc

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Define a string de conexão com o SQL Server
# - DRIVER: nome do driver ODBC instalado (verificado com `pyodbc.drivers()`)
# - SERVER: nome do servidor (localhost se estiver local)
# - DATABASE: nome do banco de dados
# - UID e PWD: usuário e senha criados no SQL Server
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'  # ou o nome do servidor SQL, como 'SENAI103\SQLEXPRESS'
    'DATABASE=FlaskDB;'  # nome do banco criado no SQL Server
    'UID=flask_user;'    # usuário com permissões no banco
    'PWD=zxc123@' # senha definida ao criar o usuário
)

# Rota principal: exibe o formulário HTML (form.html deve estar na pasta 'templates')
@app.route('/')
def index():
    return render_template('form.html')  # Mostra a página com o formulário de entrada

# Rota para tratar os dados enviados pelo formulário (método POST)
@app.route('/enviar', methods=['POST'])
def enviar():
    # Captura os dados do formulário HTML enviados pelo usuário
    nome = request.form['nome']
    email = request.form['email']

    try:
        # Abre a conexão com o banco usando a string de conexão definida
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Executa o comando SQL para inserir os dados na tabela Contatos
        # Os "?" são usados como parâmetros para prevenir SQL Injection
        cursor.execute("INSERT INTO Contatos (nome, email) VALUES (?, ?)", (nome, email))

        # Salva as mudanças no banco de dados
        conn.commit()

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()

        # Mensagem de sucesso com link para voltar ao formulário
        return f"<h2>Dados salvos com sucesso!</h2><a href='/'>Voltar</a>"

    except Exception as e:
        # Em caso de erro, exibe o erro no navegador
        return f"<h2>Erro ao salvar no banco:</h2><pre>{e}</pre>"

# Inicia o servidor Flask em modo debug
if __name__ == '__main__':
    app.run(debug=True)

