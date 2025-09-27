import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))
app.config['MYSQL_USER'] = os.getenv('DB_USERNAME', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_DATABASE', 'flask')

mysql = MySQL(app)

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_pengguna")
    data = cur.fetchall()
    cur.close()
    return render_template("index.html", users=data)

@app.route("/tambah", methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        usia = request.form['usia']
        kota = request.form['kota']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data_pengguna (nama, usia, kota) VALUES (%s, %s, %s)", (nama, usia, kota))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template("tambah.html")

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_pengguna WHERE id=%s", (id,))
    user = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        nama = request.form['nama']
        usia = request.form['usia']
        kota = request.form['kota']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE data_pengguna 
            SET nama=%s, usia=%s, kota=%s 
            WHERE id=%s
        """, (nama, usia, kota, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template("edit.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data_pengguna WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
