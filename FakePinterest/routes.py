from flask import render_template, url_for, redirect, request
from FakePinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from FakePinterest.forms import FormLogin, FormCriarConta, FormFoto, AttPerfil
from FakePinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(
            email=form_login.email.data
        ).first()  # Busca o usuário

        if usuario and bcrypt.check_password_hash(
            usuario.senha, form_login.senha.data
        ):  # Verifica se existe um usuário e valida a senha
            login_user(usuario)

            return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("homepage.html", form=form_login)


@app.route("/criar-conta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(
            form_criarconta.senha.data
        )  # Criptografa a senha

        usuario = Usuario(
            username=form_criarconta.username.data,
            senha=senha,
            email=form_criarconta.email.data,
        )

        database.session.add(usuario)  # Abre uma sessão no banco de dados
        database.session.commit()  # Envia as informações ao bd

        login_user(usuario, remember=True)  # Loga o usuário

        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):

    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(
                arquivo.filename
            )  # Troca o nome da imagem por um identado

            caminho = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                nome_seguro,
            )  # os.path.abspath(os.path.dirname(__file__) <-- caminho até routes.py
            arquivo.save(caminho)  # Envia a imagem para a pasta

            foto = Foto(
                imagem=nome_seguro, id_usuario=current_user.id
            )  # Passa as informações da imagem para enviá-la para o bd
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/perfil/configuracoes", methods=["GET", "POST"])
@login_required
def config():
    attPerfil = AttPerfil()

    usuario = Usuario.query.get(int(current_user.id))
    if attPerfil.validate_on_submit():
        action = request.form.get("action")

        if action == ("update"):

            if attPerfil.username.data:
                username = attPerfil.username.data
                usuario.username = username

            if attPerfil.senha.data:
                senha = bcrypt.generate_password_hash(attPerfil.senha.data)
                usuario.senha = senha

            database.session.commit()

            return redirect(url_for("logout"))

        if action == ("delete"):
            database.session.delete(usuario)
            database.session.commit()

            return redirect(url_for("logout"))

    return render_template("configuracoes.html", form=attPerfil)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/Feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all()
    return render_template("feed.html", fotos=fotos)


# Rotas HTML
