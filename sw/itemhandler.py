import db

def add_item(enemy_name, drops, user_id):
    sql = "INSERT INTO items (enemy_name, drops, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [enemy_name, drops, user_id])

def get_items():
    sql = "SELECT id, enemy_name FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = "SELECT items.id, items.enemy_name, items.drops,users.id user_id, users.username FROM items, users WHERE items.user_id = users.id AND items.id = ?"
    return db.query(sql, [item_id])[0]

def update_item(item_id, enemy_name, drops):
    sql = "UPDATE items SET enemy_name = ?, drops = ? WHERE id = ?"
    db.execute(sql, [enemy_name, drops, item_id])

def delete_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = "SELECT id, enemy_name FROM items WHERE drops LIKE ? OR enemy_name LIKE ? ORDER BY id DESC"
    like = "%" + query + "%"
    return db.query(sql, [like, like])