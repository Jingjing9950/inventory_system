import pandas as pd
from flask import Flask
import json

app = Flask(__name__)

df_store = pd.DataFrame({"Shop_id":[1001,1002,1003],'Shop_name':['Tempines','Serangoon','Raffles']})
df_item = pd.DataFrame({'Item_id':[100001,100002,100003],'Item_name':['Slurpee','Sandwiches','Snacks']})
df_inventory = pd.DataFrame({'Shop_id':[1001,1001,1002,1002,1003,1003],'Item_id':[100001,100002,100002,100003,100001,100003],'quantity':[0,0,0,0,0,0]})

df_store.index = df_store.index + 1
df_item.index = df_item.index + 1

summary = df_inventory.groupby(['Shop_id', 'Item_id'], as_index=False)['quantity'].sum()

@app.route("/new-shop/<shop_name>")
def add_new_shop(shop_name):
    new_row_index = len(df_store.index)+1
    df_store.loc[new_row_index] = [1000 + new_row_index, shop_name]
    return df_store.to_json()

@app.route("/get-shop/<int:shop_id>")
def get_name_by_shopid(shop_id):
    name_find = df_store[df_store.Shop_id == shop_id].Shop_name.item()
    return name_find

@app.route("/new-item/<item_name>")
def add_new_item(item_name):
    item_index = len(df_item.index) + 1
    df_item.loc[item_index] = [100000 + item_index,item_name]
    return df_item.to_json()

@app.route("/get-item/<int:item_id>")
def get_name_by_itemid(item_id):
    name_find = df_item[df_item.Item_id == item_id].Item_name.item()
    return name_find

@app.route("/purchase/<int:shop_id>/<int:item_id>/<int:volume>")
def add_quan_by_id(shop_id, item_id,volume):
    df_inventory.loc[(df_inventory['Shop_id'] == shop_id) & (df_inventory['Item_id'] == item_id),'quantity'] += volume
    return df_inventory.to_json()

@app.route("/find-inventory/<int:shop_id>/<int:item_id>")
def get_quan_by_id(shop_id, item_id):
    find_inventory = str(df_inventory[(df_inventory.Shop_id== shop_id) & (df_inventory.Item_id == item_id)].quantity.item())
    return find_inventory

@app.route("/find-inventory-item/<int:item_id>")
def get_quan_all_by_id(item_id):
    find_inventory_item = str(df_inventory[df_inventory['Item_id']==item_id].sum()['quantity'])
    return find_inventory_item

@app.route("/find-null-item/<int:shop_id>")
def get_item_name_null_shop_id(shop_id):
    sub_list_by_shop_id = summary.loc[summary['Shop_id'] == shop_id]
    match_result = pd.merge(df_item,sub_list_by_shop_id, on = 'Item_id', how='outer')
    find_null_item = pd.Series(dict(match_result[(match_result['quantity'] < 1)|(match_result['quantity'].isnull())].Item_name.items()))
    result_item =""
    for i in find_null_item:
        result_item += i + ' ,'
    return result_item

@app.route("/find-max-item-shop")
def get_max_quan_by_shop():
    find_all_max_shop = summary[summary.groupby(['Shop_id'])['quantity'].transform(max) == summary['quantity']]
    find_shop_name = pd.merge(find_all_max_shop, df_store, on = 'Shop_id', how='left')
    find_item_name = pd.merge(find_shop_name, df_item, on = 'Item_id', how='left')
    #max_item_list = find_item_name[['Shop_name','Item_name','quantity']]
    string = "<html>"
    string += "<body>"
    string += "<ul>"
    for q in range(len(find_item_name['Shop_name'])):
        string += str("<li>" +find_item_name['Shop_name'][q]) + " - " + str(find_item_name['Item_id'][q]) + " - " + str(find_item_name['quantity'][q]) + "</li>\n"
    string += "</ul>"
    string += "</body>"
    string += "</html>"
    return string


if __name__=="__main__":
    app.run(debug = True)

