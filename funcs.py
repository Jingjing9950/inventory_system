import pandas as pd

df_store = pd.DataFrame({"Shop_id":[1001,1002,1003],'Shop_name':['Tempines','Serangoon','Raffles']})
df_item = pd.DataFrame({'Item_id':[100001,100002,100003],'Item_name':['Slurpee','Sandwiches','Snacks']})
df_inventory = pd.DataFrame({'Shop_id':[1001,1001,1002,1002,1003,1003],'Item_id':[100001,100001,100002,100003,100001,100003],'quantity':[100,200,300,230,360,120]})

df_store.index = df_store.index + 1
df_item.index = df_item.index + 1

def add_new_shop(shop_name):
    new_row_index = len(df_store.index)+1
    df_store.loc[new_row_index] = [1000 + new_row_index, shop_name]
    return df_store.to_json()

def get_name_by_shopid(shop_id):
    name_find = df_store[df_store.Shop_id == shop_id].Shop_name.item()
    return name_find

def add_new_item(item_name):
    item_index = len(df_item.index) + 1
    df_item.loc[item_index] = [100000 + item_index,item_name]
    return df_item.to_json()

def get_name_by_itemid(item_id):
    name_find = df_item[df_item.Item_id == item_id].Item_name.item()
    return name_find

def add_quan_by_id(item_id, shop_id,volume):
    new_row_index = len(df_inventory)
    df_inventory.loc[new_row_index] = [item_id,shop_id,volume]
    #df_inventory.loc[(df_inventory['Shop_id'] == shop_id) & (df_inventory['Item_id'] == item_id),'quantity'] += volume
    return df_inventory.to_json()

def get_quan_by_id(shop_id, item_id):
    summary = df_inventory.groupby(['Shop_id', 'Item_id'], as_index=False)['quantity'].sum()
    find_inventory = str(summary[(summary.Shop_id== shop_id) & (summary.Item_id == item_id)].quantity.item())
    return find_inventory

def get_quan_all_by_id(item_id):
    find_inventory_item = str(df_inventory[df_inventory['Item_id']==item_id].sum()['quantity'])
    return find_inventory_item

def get_item_name_null_shop_id(shop_id):
    summary = df_inventory.groupby(['Shop_id', 'Item_id'], as_index=False)['quantity'].sum()
    sub_list_by_shop_id = summary.loc[summary['Shop_id'] == shop_id]
    match_result = pd.merge(df_item,sub_list_by_shop_id, on = 'Item_id', how='outer')
    find_null_item = pd.Series(dict(match_result[(match_result['quantity'] < 1)|(match_result['quantity'].isnull())].Item_name.items()))
    result_item =""
    for i in find_null_item:
        result_item += i + ' ,'
    return result_item

def get_max_quan_by_shop():
    summary = df_inventory.groupby(['Shop_id', 'Item_id'], as_index=False)['quantity'].sum()
    find_all_max_shop = summary[summary.groupby(['Shop_id'])['quantity'].transform(max) == summary['quantity']]
    find_shop_name = pd.merge(find_all_max_shop, df_store, on = 'Shop_id', how='left')
    find_item_name = pd.merge(find_shop_name, df_item, on = 'Item_id', how='left')
    #max_item_list = find_item_name[['Shop_name','Item_name','quantity']]
    string = "<html>"
    string += "<body>"
    string += "<ul>"
    for q in range(len(find_item_name['Shop_name'])):
        string += str("<li>" +find_item_name['Shop_name'][q]) + " - " + str(find_item_name['Item_name'][q]) + " - " + str(find_item_name['quantity'][q]) + "</li>\n"
    string += "</ul>"
    string += "</body>"
    string += "</html>"
    return string
