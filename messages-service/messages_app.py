#!flask/bin/python

from flask import Flask, request

# , static_folder='/messages'
app = Flask(__name__)


@app.route('/messages', methods=['GET', 'POST'])
def messg_requests():
    if request.method == 'GET':
        return "not implemented yet"

    if request.method == 'POST':
        return "not implemented yet"


if __name__ == '__main__':
    app.run(debug=True, port=8880)
