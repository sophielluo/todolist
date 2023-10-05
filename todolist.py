import flask,os,sqlite3
import datetime
from flask import render_template,request
from flask import send_from_directory
from werkzeug.utils import secure_filename

def fetchList():
    db = sqlite3.connect('todo.db')
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
    db = sqlite3.connect('todo.db')
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM Todo WHERE ID=?",
                            (itemID,))
    result = cursor.fetchone()
    db.close()
    return result

def fetchCat():
    db = sqlite3.connect('todo.db')
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM Category")
    result = cursor.fetchall()
    db.close()
    return result

def editItem(id,edits,photo):
    db = sqlite3.connect('todo.db')
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
    db = sqlite3.connect('todo.db')
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

app = flask.Flask(__name__)

#display table with list of todo items
@app.route('/')
def display():
    print(fetchList())
    return render_template('display.html', todoList=fetchList())

@app.route('/photos/<filename>')
def get_file(filename):
    return send_from_directory('uploads',filename)

#add todo items
@app.route('/add')
def add():
     return render_template('add.html', categories=fetchCat())

@app.route('/process/add', methods=['GET','POST'])
def process_add():
    if request.method == 'POST':
        categoryID = request.form['categoryID']
        description = request.form['description']
        print(categoryID,description)
        status = 'Pending'
        addOn = datetime.datetime.now()
        if request.files and 'photo' in request.files:
            photo = request.files['photo']
            if photo:
                filename = secure_filename(photo.filename)
                if not checkFilename(filename):
                    return 'file type not supported.'
                path = os.path.join('web_app_exercise/uploads',filename)
                photo.save(path)
            else:
                filename = 'None'
        db = sqlite3.connect('todo.db')
        db.execute('INSERT INTO Todo(Category,Description,Image,Status,AddOn) VALUES(?,?,?,?,?)',
                    (categoryID,description,filename,status,addOn)) 
        db.commit()
        db.close()
    return render_template('display.html', todoList=fetchList(), categories=fetchCat())


#edit todo items
@app.route('/edit', methods=['GET','POST'])
def edit():
    itemID = request.args['itemID']
    #itemID = request.args.get('itemID') why this one cannot?
    if request.method == 'GET':
        print(itemID)
        return render_template('edit.html',
            item=fetchItem(itemID),
            categories=fetchCat())
    else:
        print(itemID)
        if request.files and 'Image' in request.files:
            photo = request.files['Image']
            if photo:
                print('yes photo')
                filename = secure_filename(photo.filename)
                path = os.path.join('web_app_exercise/uploads',filename)
                photo.save(path)
                photo = filename
            else:
                print('no photo')
                photo = None
        success = editItem(itemID, request.form, photo)
        if success:
            return render_template('editresults.html',
                resulttext='SUCCESS!', itemID = itemID)
        else:
            return render_template('editresults.html',
                resulttext='ERROR.', itemID = itemID)

#delete todo items
@app.route('/delete', methods=['GET','POST'])
def delete():
    itemID = request.args['itemID']
    if request.method == 'GET':
        print('section 1')
        return render_template("delete.html",item=fetchItem(itemID))
    elif 'delete' in request.form:
        print('section 2')
        success = deleteItem(itemID)
        if success:
            return render_template('editresults.html',
                resulttext='SUCCESSFULLY DELETED!', deleted=True, itemID = itemID)
        else:
            return render_template('editresults.html',
                resulttext='ERROR.', deleted=False, itemID = itemID)
            
if __name__ == '__main__':
    app.run(port=8000)