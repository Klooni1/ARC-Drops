import db

def add_item(enemy_name, drops, tag, user_id):
    sql = "INSERT INTO items (enemy_name, drops, tag, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [enemy_name, drops, tag, user_id])


def get_items():
    sql = "SELECT id, enemy_name FROM items ORDER BY id DESC"
    return db.query(sql)


def get_item(item_id):
    sql = """
        SELECT 
            items.id,
            items.enemy_name,
            items.drops,
            items.tag,
            users.id AS user_id,
            users.username
        FROM items
        JOIN users ON items.user_id = users.id
        WHERE items.id = ?
    """
    return db.query(sql, [item_id])[0]


def update_item(item_id, enemy_name, drops, tag):
    sql = "UPDATE items SET enemy_name = ?, drops = ?, tag = ? WHERE id = ?"
    db.execute(sql, [enemy_name, drops, tag, item_id])


def delete_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])


def find_items(query, tag=""):
    like = "%" + query + "%"
    if tag:
        sql = """SELECT id, enemy_name 
            FROM items 
            WHERE (drops LIKE ? OR enemy_name LIKE ?) AND tag = ?
            ORDER BY id DESC
        """
        return db.query(sql, [like, like, tag])
    else:
        sql = """SELECT id, enemy_name 
            FROM items 
            WHERE drops LIKE ? OR enemy_name LIKE ?
            ORDER BY id DESC
        """
        return db.query(sql, [like, like])
