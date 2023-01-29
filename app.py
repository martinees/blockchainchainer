from flask import Flask, render_template, request, url_for, flash, redirect

# App config.
DEBUG = True
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd207ad32177dea34b7eb57eac1dcd53598bd76b55e1a3f34'

messages = [{'title': 'Message One', 'content': 'Message One Content'},
            {'title': 'Message Two', 'content': 'Message Two Content'}]
    
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))

    return render_template('create.html')
from blockchain import Blockchain
from flask import Flask, jsonify

# Creating the Web
# App using flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block
@app.route("/")
def hello():
    return "Hello!"

@app.route('/mine_block/', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'A block is MINED',
                            'index': block['index'],
                            'timestamp': block['timestamp'],
                            'proof': block['proof'],
                            'previous_hash': block['previous_hash']}

    return jsonify(response), 200

# Display blockchain in json format
@app.route('/get_chain/', methods=['GET'])
def display_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200

# Check validity of blockchain


@app.route('/valid/', methods=['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)

	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200


# Run the flask server locally
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

