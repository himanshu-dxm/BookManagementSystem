from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/libMngSys'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.books


# @app.route("/")
# def index():
#     return "<h1>Hello</h1>"


@app.route('/books', methods=['POST'])
def createBook():
    id = db.insert_one({
        'title': request.json['title'],
        'author': request.json['author'],
        'email': request.json['email'],
        'amount': request.json['amount']
    })
    print(type(id))
    return jsonify({
        'id': str(ObjectId(id.inserted_id)),
        'msg': "Record Added Successfully"
    })


@app.route('/books', methods=['GET'])
def getBooks():
    books = []
    for doc in db.find():
        books.append({
            '_id': str(ObjectId(doc['_id'])),
            'title': doc['title'],
            'author': doc['author'],
            'email': doc['email'],
            'amount': doc['amount']
        })
    return jsonify(books)


@app.route('/book/<id>', methods=['GET'])
def getBook(id):
    book = db.find_one({'_id': ObjectId(id)}),
    return jsonify({
        '_id': str(ObjectId(book['_id'])),
        'title': book['title'],
        'author': book['author'],
        'email': book['email'],
        'amount': book['amount']
    })


@app.route('/books/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({
        '_id': ObjectId(id)
    })
    return jsonify({
        'msg': "Record Deleted Successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)
