from flask import *
import sqlite3
import pdfkit
import sys
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pdf")
def pdf():
    # pdfkit.from_file('view.html', 'output.pdf')
    # # pdfkit.from_url('http://127.0.0.1:5000/view', 'addrrssbook.pdf')
    # # pdfkit.from_string('Shaurya Stackoverflow', 'SOF.pdf')
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url('http://127.0.0.1:5000/view', "pdf/addressbook1.pdf", configuration=config)
    pdfkit.from_url('http://127.0.0.1:5000/search', "pdf/addressbook5.pdf", configuration=config)
    return "Successfully created"

@app.route("/add")
def add():   
    return render_template("add.html")

@app.route("/edit/<id>")
def edit(id=0):
    con = sqlite3.connect("addressbook.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Address where id=?",[id])
    editrows = cur.fetchall()
    return render_template("edit.html", rows=editrows)

@app.route("/updatedetails",methods = ["POST"])
def update():
    if request.method == "POST":
        try:
            id = request.form["id"]
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            mobile = request.form["mobile"]
            pincode = request.form["pincode"]
            city = request.form["city"]
            file = request.files['img']
            path = os.path.join("./static/images", file.filename)
            file.save(path)
            with sqlite3.connect("addressbook.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Address SET name=?, email=?, address=?, mobile=?, pincode=?, city=?, image=? WHERE id=?",(name, email, address,mobile,pincode,city,file.filename,id))
                con.commit()
                msg = "Contact successfully updated"
                # print(msg)
                # sys.exit(1)
                savetext="Text saved"

        except:
            con.rollback()
            msg = "We can not update Contact to the list"
            savetext = "Error in updation"
        finally:
            return render_template("success.html",msg = msg,savevariable=savetext)
            con.close()

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            mobile = request.form["mobile"]
            pincode = request.form["pincode"]
            city = request.form["city"]
            file = request.files['img']
            # print(request.files)
            # sys.exit(1)
            path = os.path.join("./static/images", file.filename)
            file.save(path)
            with sqlite3.connect("addressbook.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Address (name, email, address, mobile,pincode,city,image) values (?,?,?,?,?,?,?)",(name,email,address,mobile,pincode,city,file.filename))
                con.commit()
                msg = "Contact successfully Added"
                savetext="Text saved"
        except:
            con.rollback()
            msg = "We can not add Contact to the list"
            savetext = "Error in updation"
        finally:
            return render_template("success.html",msg = msg,savevariable=savetext)
            con.close()

@app.route("/search", methods = ["POST"])
def search():
    search_result=request.form["search_value"]
    # sys.exit(1)
    con = sqlite3.connect("addressbook.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    posts = cur.execute(
        "SELECT * FROM Address WHERE name LIKE ? OR email LIKE ? OR address LIKE ? OR city LIKE ? OR mobile LIKE ?",
        ('%' + search_result + '%','%' + search_result + '%','%' + search_result + '%','%' + search_result + '%','%' + search_result + '%'))
    rows = cur.fetchall()
    # print(searchrows)
    # sys.exit(1)
    return render_template("view.html",rows = rows)


@app.route("/view")
def view():
    con = sqlite3.connect("addressbook.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Address")   
    rows = cur.fetchall()
    return render_template("view.html",rows = rows)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("addressbook.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Address where id = ?",id)
            msg = "Contact successfully deleted"   
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html",msg = msg)

@app.route("/deleteid/<id>",methods = ["GET"])
def deleteid(id=0):

    with sqlite3.connect("addressbook.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Address where id = ?",id)
            msg = "Contact successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html",msg = msg)

if __name__ == "__main__":
    app.run(debug = True)  
