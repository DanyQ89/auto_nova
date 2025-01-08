from flask import Flask, render_template, make_response, jsonify
# from flask import render_template
from config import secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/guarantees")
def guarantee():
    return render_template("guarantees.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.errorhandler(404)
def not_found_error(_):
    return make_response(jsonify({'error': "this page doesn`t exist"}))


if __name__ == '__main__':
    app.register_error_handler(404, not_found_error)

    app.run(port=8888, host='127.0.0.1', debug=True)
