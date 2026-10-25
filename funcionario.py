
from flask import jsonify, request, render_template
from banco import conectar_banco


def registrar_rotas_funcionario(app):

    # Abrir a página de funcionários
    @app.route("/funcionario")
    def pagina_funcionario():
        return render_template("funcionario.html")

    # Listar todos os funcionários
    @app.route("/api/funcionario", methods=["GET"])
    def listar_funcionarios():
        conexao = None
        cursor = None

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, cargo, nome, id_empresa, salario
                FROM funcionario
                ORDER BY id
            """)

            funcionarios = cursor.fetchall()
            return jsonify(funcionarios), 200

        except Exception as erro:
            print("ERRO AO LISTAR FUNCIONÁRIOS:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # Cadastrar um funcionário
    @app.route("/api/funcionario", methods=["POST"])
    def cadastrar_funcionario():
        conexao = None
        cursor = None

        try:
            dados = request.get_json()

            if not dados:
                return jsonify({"erro": "Nenhum dado foi enviado."}), 400

            cargo = dados.get("cargo")
            nome = dados.get("nome")
            id_empresa = dados.get("id_empresa")
            salario = dados.get("salario")

            if not nome or not cargo or id_empresa is None or salario is None:
                return jsonify({
                    "erro": "Preencha nome, cargo, empresa e salário."
                }), 400

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO funcionario
                (cargo, nome, id_empresa, salario)
                VALUES (%s, %s, %s, %s)
            """, (cargo, nome, id_empresa, salario))

            conexao.commit()

            return jsonify({
                "mensagem": "Funcionário cadastrado com sucesso!",
                "id": cursor.lastrowid
            }), 201

        except Exception as erro:
            if conexao:
                conexao.rollback()

            print("ERRO AO CADASTRAR FUNCIONÁRIO:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # Buscar um funcionário pelo ID
    @app.route("/api/funcionario/<int:id_funcionario>", methods=["GET"])
    def buscar_funcionario(id_funcionario):
        conexao = None
        cursor = None

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, cargo, nome, id_empresa, salario
                FROM funcionario
                WHERE id = %s
            """, (id_funcionario,))

            funcionario = cursor.fetchone()

            if not funcionario:
                return jsonify({"erro": "Funcionário não encontrado."}), 404

            return jsonify(funcionario), 200

        except Exception as erro:
            print("ERRO AO BUSCAR FUNCIONÁRIO:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # Editar um funcionário
    @app.route("/api/funcionario/<int:id_funcionario>", methods=["PUT"])
    def editar_funcionario(id_funcionario):
        conexao = None
        cursor = None

        try:
            dados = request.get_json()

            if not dados:
                return jsonify({"erro": "Nenhum dado foi enviado."}), 400

            cargo = dados.get("cargo")
            nome = dados.get("nome")
            id_empresa = dados.get("id_empresa")
            salario = dados.get("salario")

            if not nome or not cargo or id_empresa is None or salario is None:
                return jsonify({
                    "erro": "Preencha nome, cargo, empresa e salário."
                }), 400

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE funcionario
                SET cargo = %s,
                    nome = %s,
                    id_empresa = %s,
                    salario = %s
                WHERE id = %s
            """, (cargo, nome, id_empresa, salario, id_funcionario))

            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT id FROM funcionario WHERE id = %s",
                    (id_funcionario,)
                )

                if not cursor.fetchone():
                    return jsonify({
                        "erro": "Funcionário não encontrado."
                    }), 404

            conexao.commit()

            return jsonify({
                "mensagem": "Funcionário atualizado com sucesso!"
            }), 200

        except Exception as erro:
            if conexao:
                conexao.rollback()

            print("ERRO AO EDITAR FUNCIONÁRIO:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # Excluir um funcionário
    @app.route("/api/funcionario/<int:id_funcionario>", methods=["DELETE"])
    def excluir_funcionario(id_funcionario):
        conexao = None
        cursor = None

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute(
                "DELETE FROM funcionario WHERE id = %s",
                (id_funcionario,)
            )

            if cursor.rowcount == 0:
                return jsonify({
                    "erro": "Funcionário não encontrado."
                }), 404

            conexao.commit()

            return jsonify({
                "mensagem": "Funcionário excluído com sucesso!"
            }), 200

        except Exception as erro:
            if conexao:
                conexao.rollback()

            print("ERRO AO EXCLUIR FUNCIONÁRIO:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()