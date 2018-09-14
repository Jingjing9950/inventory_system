import pandas as pd
from flask import Flask, render_template, request
import json
import funcs

app = Flask(__name__)

@app.route("/")
def inventory_system():
    return render_template("operation.html")

@app.route("/new-shop", methods = ['GET','POST'])
def add_new_shop():
    if request.method == "POST":
        shop_name = request.form['shop_name']
        return funcs.add_new_shop(shop_name)

@app.route("/get-shop", methods = ['GET','POST'])
def get_name_by_shopid():
    shop_id = int(request.values.get('shop_id'))
    return funcs.get_name_by_shopid(shop_id)

@app.route("/new-item", methods = ['GET','POST'])
def add_new_item():
    if request.method == "POST":
        item_name = request.form['item_name']
        return funcs.add_new_item(item_name)

@app.route("/get-item")
def get_name_by_itemid():
    item_id = int(request.values.get('item_id'))
    return funcs.get_name_by_itemid(item_id)

@app.route("/purchase")
def add_quan_by_id():
    shop_id = int(request.values.get('shop_id'))
    item_id = int(request.values.get('item_id'))
    volume = int(request.values.get('volume'))
    return funcs.add_quan_by_id(item_id, shop_id,volume)

@app.route("/find-inventory")
def get_quan_by_id():
    shop_id = int(request.values.get('shop_id'))
    item_id = int(request.values.get('item_id'))
    return funcs.get_quan_by_id(shop_id,item_id)

@app.route("/find-inventory-item")
def get_quan_all_by_id():
    item_id = int(request.values.get('item_id'))
    return funcs.get_quan_all_by_id(item_id)

@app.route("/find-null-item")
def get_item_name_null_shop_id():
    shop_id = int(request.values.get('shop_id'))
    return funcs.get_item_name_null_shop_id(shop_id)

@app.route("/find-max-item-shop")
def get_max_quan_by_shop():
    return funcs.get_max_quan_by_shop()


if __name__=="__main__":
    app.run(debug = True)
