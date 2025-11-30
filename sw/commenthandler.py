import db

def add_comment(item_id, user_id, username, message):
    sql = "INSERT INTO comments (item_id, user_id, username, message) VALUES (?, ?, ?, ?)"
    db.execute(sql, [item_id, user_id, username, message])

def get_comments_for_item(item_id):
    sql = "SELECT id, user_id, username, message, created_at FROM comments WHERE item_id = ? ORDER BY created_at ASC"
    return db.query(sql, [item_id])
