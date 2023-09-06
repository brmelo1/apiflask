from flask import Flask,jsonify,request


app = Flask(__name__)

desen=[
    {
    "nome":"bruno",
    "habi":["python","java","sql"]
    },
    {
    "nome":"ana",
    "habi":["ruby","flutter","sql"]
    }
]



@app.route('/dev/<int:id>', methods=['GET','PUT','DELETE'])
def dev_buscar_id(id):
    if request.method == "GET":
        dados = desen[id]
        return jsonify(f"{dados['nome']}  {dados['habi']} ")
    elif request.method == "PUT":
        desen[id]=request.get_json()
        return jsonify(desen)
    elif request.method == 'DELETE':
        del desen[id]
        return jsonify(desen)
    

@app.route('/add', methods=['POST'])
def incluir_livro():
    dados = request.get_json()
    desen.append(dados)
    return jsonify(desen)

@app.route('/dev/<nome>', methods=['GET'])
def dev_buscar_nome(nome):
    for i in desen:
        if i['nome']== nome:
            return jsonify(i)
    
   



app.run(port=5000,host='localhost',debug=True)