'''
create table users(
id int not null auto_increment primary key,
name varchar(50),
age int,
city varchar(50)
);
select * from users;
insert into users (name,age,city) values ('vasanth',25,'salem');
drop table users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
'''
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Home page showing the list of users
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    try:
        con.execute(sql)
        res = con.fetchall()
        app.logger.info(res)  # Logging to verify data is fetched
    except Exception as e:
        app.logger.error(f"Error: {e}")
    return render_template("home.html", datas=res)
# res = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
    # return render_template("home.html", datas=res)
# Add a new user
@app.route("/addUsers", methods=['GET', 'POST'])
def addUsers():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        con = mysql.connection.cursor()
        sql = "INSERT INTO users(name, city, age) VALUES (%s, %s, %s)"
        con.execute(sql, [name, city, age])
        mysql.connection.commit()
        con.close()
        flash('User Details Added', 'success')
        return redirect(url_for("home"))
    return render_template("addUsers.html")

@app.route("/editUser/<string:id>", methods=['GET', 'POST'])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        # Handle form submission for editing
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        sql = "UPDATE users SET name=%s, city=%s, age=%s WHERE id=%s"
        con.execute(sql, [name, city, age, id])
        mysql.connection.commit()
        flash('User Details Updated', 'info')
        return redirect(url_for('home'))
    
    # Fetch user details for editing
    sql = "SELECT * FROM users WHERE id=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    return render_template('editUser.html', datas=res)


# Delete a user
@app.route("/deleteUser/<string:id>", methods=['GET', 'POST'])
def deleteUser(id):
    con = mysql.connection.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted', 'danger')
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.secret_key = "abc123"
    app.run(debug=True)
