import flask,os,sqlite3
from flask import send_from_directory
from werkzeug.utils import secure_filename


def fetchList():
    db = sqlite3.connect('project/todolist.db')
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT\
                        Todo.ID as ID,\
                        Category.Name as categoryName,\
                        Todo.Description as description,\
                        Todo.Image as imageURL,\
                        Todo.Status as status,\
                        Todo.AddOn as addOn\
                        FROM Todo INNER JOIN Category\
                        ON Todo.Category = Category.ID")
    result = cursor.fetchall()
    db.close()
    return result

def fetchItem(itemID):
    db = sqlite3.connect('project/todolist.db')
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM Todo WHERE ID=?",
                            (itemID,))
    result = cursor.fetchone()
    db.close()
    return result

def fetchCat():
    db = sqlite3.connect('project/todolist.db')
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM Category")
    result = cursor.fetchall()
    db.close()
    return result

def editItem(id,edits,photo):
    db = sqlite3.connect('project/todolist.db')
    db.row_factory = sqlite3.Row
    print('id of item edited:',id)
    category = edits['Category']
    description = edits['Description']
    status = edits['Status']
    if photo:
        db.execute("UPDATE Todo SET Category=?, Description=?, Image=?, Status=? WHERE Todo.ID=?",(category,description,photo,status,id))
        db.commit()
        db.close()
        return True
    elif not photo:
        db.execute("UPDATE Todo SET Category=?, Description=?, Status=? WHERE Todo.ID=?",(category,description,status,id))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False
   
def deleteItem(id):
    db = sqlite3.connect('project/todolist.db')
    db.row_factory = sqlite3.Row
    print('id of item deleted:',id)
    db.execute("DELETE FROM Todo WHERE Todo.ID=?",(id,))
    db.commit()
    db.close()
    return True

def checkFilename(filename):
    check = filename.split('.')
    if check[-1] not in ['gif','png','jpg','jpeg']:
        return False
    return True
