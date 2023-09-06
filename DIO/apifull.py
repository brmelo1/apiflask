from flask import Flask,request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

desen=[
        {
    "id": 0,
    "nome":"bruno",
    "habi":["python","java","sql"]
    },
    {
    "id" : 1,
    "nome":"ana",
    "habi":["ruby","flutter","sql"]
    },
    {
    "id" : 2,
    "nome":"luiz",
    "habi":["assembly","react-native","no-sql"]
    },
    {
    "id" : 3,
    "nome":"aldo",
    "habi":["C++","javascript","no-code"]
    }
]

class devs(Resource):
    def get(self,id):
        dados = desen[id]
        return dados
    # f"{dados['nome']} esta aqui {dados['habi'][0] }"
    
    def put(self,id):
        desen[id]=request.get_json()
        return desen
    
    def delete(self,id):
        del desen[id]
        return desen
    
class lista_devs(Resource):
    def get(self):
        return desen
    
class new_devs(Resource):
    def post(self):
        desen.append(request.get_json())
        return desen

api.add_resource(devs, '/dev/<int:id>/')
api.add_resource(lista_devs, '/dev')
api.add_resource(new_devs, '/dev/add')

if __name__ == '__main__':
    app.run(debug=True)

