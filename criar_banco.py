from FakePinterest import app, database

with app.app_context():
    database.create_all()

# Cria o banco de dados
