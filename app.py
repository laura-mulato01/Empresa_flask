from flask import Flask

app = Flask(__name__)

from login import registrar_rotas_login
from empresa import registrar_rotas_empresa
from funcionario import registrar_rotas_funcionario

registrar_rotas_login(app)
registrar_rotas_empresa(app)
registrar_rotas_funcionario(app)

print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
