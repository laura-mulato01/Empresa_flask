from flask import request, jsonify, render_template
from banco import conectar_banco


def registrar_rotas_empresa(app):

    @app.route("/empresa")
    def pagina_empresa():
        return render_template("empresa.html")

    # LISTAR EMPRESAS
    @app.route("/api/empresa", methods=["GET"])
    def listar_empresa():
        conexao = None
        cursor = None
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute(
                "SELECT id, nome, cnpj, cidade, ativo "
                "FROM empresa ORDER BY id DESC"
            )
            empresas = cursor.fetchall()
            return jsonify(empresas), 200

        except Exception as erro:
            print("ERRO AO LISTAR EMPRESAS:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # BUSCAR EMPRESA POR ID
    @app.route("/api/empresa/<int:id_empresa>", methods=["GET"])
    def obter_empresa(id_empresa):
        conexao = None
        cursor = None
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute(
                "SELECT id, nome, cnpj, cidade, ativo "
                "FROM empresa WHERE id = %s",
                (id_empresa,)
            )
            empresa = cursor.fetchone()

            if not empresa:
                return jsonify({"erro": "Empresa não encontrada"}), 404

            return jsonify(empresa), 200

        except Exception as erro:
            print("ERRO AO BUSCAR EMPRESA:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # CADASTRAR EMPRESA
    @app.route("/api/empresa", methods=["POST"])
    def criar_empresa():
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "Dados não recebidos em JSON"}), 400

        nome = dados.get("nome")
        cnpj = dados.get("cnpj") or None
        cidade = dados.get("cidade") or None
        ativo = dados.get("ativo", 1)

        if not nome:
            return jsonify({"erro": "O nome é obrigatório"}), 400

        conexao = None
        cursor = None
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()

            sql = """
                INSERT INTO empresa (nome, cnpj, cidade, ativo)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, cnpj, cidade, ativo))
            conexao.commit()

            novo_id = cursor.lastrowid

            return jsonify({
                "mensagem": "Empresa cadastrada com sucesso!",
                "id": novo_id
            }), 201

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("ERRO AO CADASTRAR EMPRESA:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # ATUALIZAR EMPRESA
    @app.route("/api/empresa/<int:id_empresa>", methods=["PUT"])
    def atualizar_empresa(id_empresa):
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "Dados não recebidos em JSON"}), 400

        nome = dados.get("nome")
        cnpj = dados.get("cnpj") or None
        cidade = dados.get("cidade") or None
        ativo = dados.get("ativo", 1)

        if not nome:
            return jsonify({"erro": "O nome é obrigatório"}), 400

        conexao = None
        cursor = None
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute(
                """UPDATE empresa
                   SET nome = %s, cnpj = %s, cidade = %s, ativo = %s
                   WHERE id = %s""",
                (nome, cnpj, cidade, ativo, id_empresa)
            )
            conexao.commit()

            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT id FROM empresa WHERE id = %s",
                    (id_empresa,)
                )
                if not cursor.fetchone():
                    return jsonify({"erro": "Empresa não encontrada"}), 404

            return jsonify({
                "mensagem": "Empresa atualizada com sucesso!"
            }), 200

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("ERRO AO ATUALIZAR EMPRESA:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    # EXCLUIR EMPRESA
    @app.route("/api/empresa/<int:id_empresa>", methods=["DELETE"])
    def deletar_empresa(id_empresa):
        conexao = None
        cursor = None
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute(
                "DELETE FROM empresa WHERE id = %s",
                (id_empresa,)
            )
            conexao.commit()

            if cursor.rowcount == 0:
                return jsonify({"erro": "Empresa não encontrada"}), 404

            return jsonify({
                "mensagem": "Empresa excluída com sucesso!"
            }), 200

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("ERRO AO EXCLUIR EMPRESA:", repr(erro))
            return jsonify({"erro": str(erro)}), 500

        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()
