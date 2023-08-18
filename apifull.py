from flask import Flask,request
from flask_restful import Resource, Api
import psycopg2

app = Flask(__name__)
api = Api(app)


db_config = {
    'user': 'postgres',
    'password': 'admin',
    'dbname': 'postgres',
    'host': 'localhost',
    'port': '5432' 
}


def conectar():
    return psycopg2.connect(**db_config)

class city_unico(Resource):
    def get(self,nome):
        print(nome)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cidade WHERE nome LIKE %s", (f'%{nome}%',))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        cidades = []
        for resultado in resultados:
            id, nomeuf, uf = resultado
            cidade = {"id": id, "nome": nomeuf, "uf": uf}
            cidades.append(cidade)

        return cidades
    
    def put(self,nome):
        print(nome)
        city_novo = request.get_json()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE cidade SET nome = %s, uf = %s WHERE nome LIKE %s;", (city_novo['nome'], city_novo['uf'], f'%{nome}%'))
        conn.commit()
        cursor.close()
        conn.close()
        return city_novo
    
    def delete(self,nome):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cidade WHERE nome LIKE %s ", (f'%{nome}%',))
        conn.commit()
        cursor.close()
        conn.close()

        return ({"msg":f"{nome} exlcuido do banco"})

class citys(Resource):
    def get(self):
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
        return livros
    
    
    def post(self):
        city_novo = request.get_json()
        conn = conectar()
        cursor = conn.cursor()
        for cit in city_novo:
            cursor.execute("INSERT INTO cidade (nome, uf) VALUES (%s, %s)", (cit['nome'],cit['uf'],))
        conn.commit()
        cursor.close()
        conn.close()
        return ({"message": "Cidade inserida com suces!",
                        "CIDADES":city_novo})  
    



api.add_resource(citys, '/city')
api.add_resource(city_unico, '/city/<nome>')

if __name__ == '__main__':
    app.run(debug=True)

