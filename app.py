import peeweedbevolve
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Store

app = Flask(__name__)
.secret_key = b"\xe3\x86\xc7\xe7\xf2\xfc'\xb0c\xda)\xfa\xfe%\x13\x8b"


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base'})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/store', methods=['GET'])
def store():
    return render_template('store.html')


@app.route("/store", methods=['POST'])
def create_new_store():
    new_store = Store(name=request.form.get('store_name'))
    if new_store.save():
        flash('Successfully saved!')
        return redirect(url_for('store'))
    else:
        return render_template('store.html', name=request.form.get('store_name'))

@app.route('/warehouse', methods=['GET'])
def warehouse():
    return render_template('warehouse.html')


if __name__ == '__main__':
    app.run()
