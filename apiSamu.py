from flask import Flask,request
from flask_restful import Resource, Api
import psycopg2

app = Flask(__name__)
api = Api(app)


db_config = {
    'user': 'postgres',
    'password': 'admin',
    'dbname': 'dbase',
    'host': 'localhost',
    'port': '5432' 
}


def conectar():
    return psycopg2.connect(**db_config)

class equipe_unico(Resource):
    def get(self,nome):
        print(nome)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM samu WHERE vtr LIKE %s", (f'%{nome}%',))
        resultados = cursor.fetchall() #RETORNAR 
        cursor.close()
        conn.close()
        equipes = []
        for resultado in resultados:
            id,vtr,turno,data,profi,ativado  = resultado
            equipe = {"id":id,"vtr": vtr, "data": data.isoformat(), "turno": turno,"profi":profi,"ativado":ativado}
            equipes.append(equipe)

        return equipes
    
    def put(self,nome):
        print(nome)
        equipe_novo = request.get_json()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE samu SET vtr = %s, turno = %s,data = %s,profi = %s,ativado = %s WHERE vtr LIKE %s;", (equipe_novo['vtr'],equipe_novo['turno'],equipe_novo['data'],equipe_novo['profi'],equipe_novo['ativado'],f'%{nome}%'))
        conn.commit()
        cursor.close()
        conn.close()
        return equipe_novo
    
    def delete(self,nome):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM samu WHERE vtr LIKE %s ", (f'%{nome}%',))
        conn.commit()
        cursor.close()
        conn.close()

        return ({"msg":f"{nome} exlcuido do banco"})

class equipesamu(Resource):
    def get(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM samu;")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        equipes = []
        for resultado in resultados:
            id,vtr,turno,data,profi,ativado = resultado
            equipe = {"id":id,"vtr": vtr, "data": data.isoformat(), "turno": turno,"profi":profi,"ativado":ativado}
            equipes.append(equipe)
        return equipes 
    
    def post(self):
        equipes = request.get_json()
        conn = conectar()
        cursor = conn.cursor()
        for equipe in equipes:
            cursor.execute("INSERT INTO samu (vtr, turno,data,profi,ativado) VALUES (%s, %s,%s, %s,%s)", (equipe['vtr'],equipe['turno'],equipe['data'],equipe['profi'],equipe['ativado']))
        conn.commit()
        cursor.close()
        conn.close()
        return ({"message": "Equipe inserida com suces!",
                        "Equipes":equipes})  
    
class equipeID(Resource):
    def get(self, num):
        print(num)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM samu WHERE id = {num}")
        resultados = cursor.fetchone()
        cursor.close()
        conn.close()
        id,vtr,turno,data,profi,ativado  = resultados
        equipe = {"id":id,"vtr": vtr, "data": data.isoformat(), "turno": turno,"profi":profi,"ativado":ativado}
            

        return equipe


api.add_resource(equipesamu, '/equipesamu')
api.add_resource(equipe_unico, '/equipesamu/<nome>')
api.add_resource(equipeID, '/equipesamuid/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)

