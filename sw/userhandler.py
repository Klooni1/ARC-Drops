import db

def get_users():
    sql = "SELECT id, username FROM users ORDER BY id"
    return db.query(sql)

def get_user(user_id):
    sql = """SELECT id, username FROM users WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_item_count(user_id):
    sql = "SELECT COUNT(*) AS count FROM items WHERE user_id = ?"
    result = db.query(sql, [user_id])[0]
    return result["count"]

def get_items_by_user(user_id):
    sql = "SELECT id, enemy_name FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def get_user_comment_count(user_id):
    sql = "SELECT COUNT(*) as count FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])[0]
    return result["count"]