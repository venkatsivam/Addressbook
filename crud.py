from flask import *
import sqlite3
import pdfkit
import os
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pdf")
def pdf():
    # pdfkit.from_file('view.html', 'output.pdf')
    # pdfkit.from_url('http://127.0.0.1:5000/view', 'addrrssbook.pdf')
    # pdfkit.from_string('Shaurya Stackoverflow', 'SOF.pdf')
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url('http://127.0.0.1:5000/view', "addressbook2.pdf", configuration=config)
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
            with sqlite3.connect("addressbook.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Address SET name=?, email=?, address=?, mobile=?, pincode=?, city=? WHERE id=?", (name, email, address,mobile,pincode,city, id))
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
            with sqlite3.connect("addressbook.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Address (name, email, address, mobile,pincode,city) values (?,?,?,?,?,?)",(name,email,address,mobile,pincode,city))
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
