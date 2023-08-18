from flask import Flask,jsonify,request


app = Flask(__name__)


livros=[{
    "id":1,
    "title":"Ao Farol",
    "autor":"clarisse lispector"
    },
    {
    "id":2,
    "title":"A casa dos espíritos",
    "autor":"mario farias"
    },
    {
    "id":3,
    "title":"Memórias póstumas de Brás Cubas",
    "autor":"lula da silva"
    },
    
    ]

@app.route('/livros',methods=['GET'])
def obterlivros():
    return jsonify(livros)


@app.route('/livros/<int:id>', methods=['GET'])
def buscar_livro_por_id(id):
    for livro in livros:
        if livro.get('id')== id:
            return jsonify(livro)
    
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_nome(id):
    livroalt = request.get_json()
    for ind,livro in enumerate(livros):
        if livro.get('id') == id:
            livros[ind].update(livroalt)
            return jsonify(livros[ind])
    
@app.route('/livros/add', methods=['POST'])
def incluir_livro():
    livro_novo = request.get_json()
    livros.append(livro_novo)
    return jsonify(livros)
    
@app.route('/livros/excluir/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    for ind,livro in enumerate(livros):
        if livro.get('id')== id:
            del livros[ind]
    
    return jsonify(livros)



app.run(port=5000,host='localhost',debug=True)
