import peeweedbevolve
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Store, Warehouse
from peewee import fn
import logging

app = Flask(__name__)
app.secret_key = b"\xe3\x86\xc7\xe7\xf2\xfc'\xb0c\xda)\xfa\xfe%\x13\x8b"


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


@app.route('/store/new', methods=['GET'])
def store():
    return render_template('store.html')


@app.route("/store", methods=['POST'])
def create_new_store():
    s = Store(name=request.form.get('store_name'))
    if s.save():
        flash('New store successfully created!')
        return redirect(url_for('store'))
    else:
        return render_template('store.html', name=request.form.get('store_name'))


@app.route('/stores', methods=['GET'])
def stores():
    # stores = Store.select(Store.id, Store.name, fn.Count(
    #     Warehouse.id).alias('num')).join(Warehouse).group_by(Store.id).order_by(Store.id)
    stores = Store.select()
    return render_template('stores.html', stores=stores)


@app.route('/store/<id>', methods=['GET'])
def show_store(id):
    store = Store.get_by_id(id)
    return render_template('show.html', store=store)


@app.route('/warehouse/new', methods=['GET'])
def warehouse():
    stores = Store.select()
    return render_template('warehouse.html', stores=stores)


@app.route('/warehouse/new', methods=['POST'])
def create_new_warehouse():
    store = Store.get_by_id(request.form['store_id'])
    w = Warehouse(store=store, location=request.form['location'])
    if w.save():
        flash('New warehouse successfully added!')
        return redirect(url_for('warehouse'))
    else:
        flash('Error - Unable to create warehouse.')
        return render_template('warehouse.html')


if __name__ == '__main__':
    app.run()
