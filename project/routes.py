import flask,os,sqlite3
import datetime
from flask import render_template,request, redirect, url_for, send_from_directory, Blueprint
from flask_login import login_user, login_required, logout_user

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from .helperfunctions import fetchList, fetchCat, fetchItem 
from .helperfunctions import checkFilename, editItem, deleteItem
from .extensions import db
from .models import User


#main = Blueprint('main',__name__,template_folder="templates")
main = Blueprint('main',__name__)

#display table with list of todo items
@main.route("/")
def index():
    return render_template("index.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.index"))
        # return "created user!"

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.index"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout_the_user():
    logout_user()
    return redirect(url_for("main.index"))


@main.route('/display')
@login_required
def display():
    #print(fetchList())
    #id = User.get_id()
    return render_template('display.html', todoList=fetchList())

@main.route('/photos/<filename>', methods=["GET", "POST"])
@login_required
def get_file(filename):
    return send_from_directory('uploads',filename)

#add todo items
@main.route('/add', methods=["GET", "POST"])
@login_required
def add():
     return render_template('add.html', categories=fetchCat())

@main.route('/process/add', methods=['GET','POST'])
@login_required
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
                path = os.path.join('project/uploads',filename)
                photo.save(path)
            else:
                filename = 'None'
        db = sqlite3.connect('project/todolist.db')
        db.execute('INSERT INTO Todo(Category,Description,Image,Status,AddOn) VALUES(?,?,?,?,?)',
                    (categoryID,description,filename,status,addOn)) 
        db.commit()
        db.close()
    return redirect(url_for("main.display"))
    #return render_template('display.html', todoList=fetchList(), categories=fetchCat())


#edit todo items
@main.route('/edit', methods=['GET','POST'])
@login_required
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
                path = os.path.join('project/uploads',filename)
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
@main.route('/delete', methods=['GET','POST'])
@login_required
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
            
# if __name__ == '__main__':
#     main.run(port=8000,debug=True)







