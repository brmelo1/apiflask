from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_config = {
    'user': 'postgres',
    'password': 'admin',
    'dbname': 'postgres',
    'host': '192.168.100.250',
    'port': '5432'  # Porta padrão do PostgreSQL
}

# Função para conectar ao banco de dados
def conectar():
    return psycopg2.connect(**db_config)

@app.route('/city', methods=['GET'])
def obter_city():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cidade;")
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    livros = []
    for resultado in resultados:
        id, title, autor = resultado
        livro = {"id": id, "nome": title, "uf": autor}
        livros.append(livro)

    return jsonify(livros)

@app.route('/city/<int:id>', methods=['GET'])
def buscar_city_por_id(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cidade WHERE id = %s;", (id,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        id, nome, uf = resultado
        livro = {"id": id, "nome": nome, "uf": uf}
        return livro
    else:
        return None
    
@app.route('/city/add', methods=['POST'])
def incluir_city():
    city_novo = request.get_json()
    conn = conectar()
    cursor = conn.cursor()
    for cit in city_novo:
        cursor.execute("INSERT INTO cidade (nome, uf) VALUES (%s, %s)", (cit['nome'],cit['uf'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cidade inserida com sucesso!",
                    "CIDADES":city_novo})    


@app.route('/city/bu/<nome>', methods=['GET'])
def buscar_city_nome(nome):
    print(nome)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cidade WHERE nome LIKE %s", (f'%{nome}%',))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()
    cidades = []
    for resultado in resultados:
        id, title, autor = resultado
        cidade = {"id": id, "nome": title, "uf": autor}
        cidades.append(cidade)

    return jsonify(cidades)
   

@app.route('/city/bu/<nome>', methods=['DELETE'])
def delete_city_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cidade WHERE nome LIKE %s ", (f'%{nome}%',))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"msg":f"{nome} exlcuido do banco"})




if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
