import sqlite3
from flask import Flask, request, jsonify

# Conectar ao banco de dados
conn = sqlite3.connect('produtos.db')
c = conn.cursor()

# Criar tabela de produtos
c.execute('''
          CREATE TABLE IF NOT EXISTS products
          (id INTEGER PRIMARY KEY,
          nome TEXT NOT NULL,
          preco REAL NOT NULL,
          quantidade INTEGER NOT NULL)
          ''')
conn.commit()
app = Flask(__name__)

@app.route('/produtos', methods=['GET'])
def listar_produtos_route():
    produtos = listar_produtos()
    return jsonify(produtos)

@app.route('/produto/<int:id>', methods=['GET'])
def buscar_produto_route(id):
    produto = buscar_produto(id)
    if produto:
        return jsonify(produto)
    return jsonify({'error': 'Produto não encontrado'}), 404

@app.route('/produto', methods=['POST'])
def adicionar_produto_route():
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')
    quantidade = data.get('quantidade')
    adicionar_produto(nome, preco, quantidade)
    return jsonify({'message': 'Produto adicionado com sucesso'}), 201

@app.route('/checkout/<int:id>', methods=['POST'])
def checkout_produto_route(id):
    data = request.get_json()
    quantidade_vendida = data.get('quantidade_vendida')
    if checkout_produto(id, quantidade_vendida):
        return jsonify({'message': 'Checkout realizado com sucesso'})
    return jsonify({'error': 'Quantidade insuficiente em estoque'}), 400

if __name__ == '__main__':
    app.run(debug=True)
# Função para adicionar produto
def adicionar_produto(nome, preco, quantidade):
    c.execute('''
              INSERT INTO produtos (nome, preco, quantidade)
              VALUES (?, ?, ?)
              ''', (nome, preco, quantidade))
    conn.commit()print("")

# Função para listar todos os produtos
def listar_produtos():
    c.execute('SELECT * FROM produtos')
    return c.fetchall()

# Função para buscar produto por ID
def buscar_produto(id):
    c.execute('SELECT * FROM produtos WHERE id = ?', (id,))
    return c.fetchone()

# Função para realizar checkout de um produto
def checkout_produto(id, quantidade_vendida):
    produto = buscar_produto(id)
    if produto and produto[3] >= quantidade_vendida:
        nova_quantidade = produto[3] - quantidade_vendida
        c.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, id))
        conn.commit()
        return True
    return False

# Exemplo de uso
adicionar_produto('Notebook', 2500.00, 10)
adicionar_produto('Mouse', 50.00, 100)

print("Lista de produtos:")
produtos = listar_produtos()
for produto in produtos:
    print(produto)

print("Realizando checkout de 2 notebooks:")
if checkout_produto(1, 2):
    print("Checkout realizado com sucesso!")
else:
    print("Quantidade insuficiente em estoque.")

print("Lista de produtos atualizada:")
produtos = listar_produtos()
for produto in produtos:
    print(produto)

# Fechar a conexão com o banco de dados
conn.close()
