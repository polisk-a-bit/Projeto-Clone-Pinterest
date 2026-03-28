from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///comunidade.db"  # Define o bd e vincula com o site
)
app.config["SECRET_KEY"] = (
    "a80ca135be5ca00e22cf73952539e65b"  # Define uma senha para o site e a vincula com o mesmo
)
app.config["UPLOAD_FOLDER"] = (
    "static/fotos_post"  # Define a pasta para onde as fotos uploadadas irão
)

database = SQLAlchemy(app)  # Cria o banco de dados
bcrypt = Bcrypt(app)  # Cria a criptografia para senhas
login_manager = LoginManager(app)  # Cria um gerenciador de senhas
login_manager.login_view = "homepage"  # Onde envia o usuário não logado


from FakePinterest import routes

# Vincula banco de dados, front-end e back-end
