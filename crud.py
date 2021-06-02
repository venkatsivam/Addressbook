from flask import *
import sqlite3
import pdfkit
import sys
import os
import urllib.request as urllib
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pdf/<pdf_url>/<search_val>")
def pdf(pdf_url,search_val):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    if pdf_url=="search":
        final_url=pdf_url+ "?search_value=" + search_val
    else:
        final_url=pdf_url
    pdfkit.from_url(['http://localhost:5000/' + final_url], "pdf/addressbook27.pdf", configuration=config)
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

@app.route("/search", methods = ["POST","GET"])
def search():
    search_result= request.args.get('search_value', '')
    con = sqlite3.connect("addressbook.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM Address WHERE name LIKE ? OR email LIKE ? OR address LIKE ? OR city LIKE ? OR mobile LIKE ?",
        ('%' + search_result + '%','%' + search_result + '%','%' + search_result + '%','%' + search_result + '%','%' + search_result + '%'))
    search_rows = cur.fetchall()
    current_url = request.base_url
    search_url=current_url.rsplit('/', 1).pop()
    return render_template("view.html",rows = search_rows, pdf_url=search_url, search_val=search_result)


@app.route("/view")
def view():
    con = sqlite3.connect("addressbook.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Address")   
    rows = cur.fetchall()
    current_url = request.base_url
    view_url = current_url.rsplit('/', 1).pop()
    return render_template("view.html",rows = rows,pdf_url=view_url,search_val="view")

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
