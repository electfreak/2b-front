from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# configuring MySQL for the web application
# default user of MySQL to be replaced with appropriate username
app.config['MYSQL_DATABASE_USER'] = 'group25'
app.config[
    'MYSQL_DATABASE_PASSWORD'] = 'buzzers228'  # default passwrod of MySQL to be replaced with appropriate password
# Database name to be replaced with appropriate database name
app.config['MYSQL_DATABASE_DB'] = 'group25'
app.config[
    'MYSQL_DATABASE_HOST'] = 'localhost'  # default database host of MySQL to be replaced with appropriate database host
# initialise mySQL
mysql.init_app(app)
# create connection to access data
conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/imprint")
def imprint():
    return render_template('imprint.html')


@app.route("/admin/feedback")
def admin_feedback():
    return render_template('admin/feedback.html')


@app.route("/admin/user", methods=['GET'])
def admin_user():
    return render_template('admin/user.html')


@app.route("/admin/users", methods=['GET'])
def get_users():
    cursor.execute("select uid from Users")
    conn.commit()
    return {'uids': cursor.fetchall()}


@app.route("/admin/messages", methods=['GET'])
def get_users():
    cursor.execute("select mid from Messages")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/locations", methods=['GET'])
def get_users():
    cursor.execute("select lid from Locations")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/tasks", methods=['GET'])
def get_users():
    cursor.execute("select tid from Tasks")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/user", methods=['POST'])
def add_user():
    name = request.form['name']
    bio = request.form['bio']
    photo = request.form['photo']
    cursor.execute(
        "INSERT INTO Users (name, photo, bio) VALUES (%s, %s, %s)",
        (name, bio, photo))
    conn.commit()
    return render_template("admin/user.html")


@app.route("/admin/message", methods=['GET'])
def admin_message():
    return render_template('admin/message.html')


@app.route("/admin/message", methods=['POST'])
def add_message():
    name = request.form['name']
    bio = request.form['bio']
    photo = request.form['photo']
    cursor.execute(
        "INSERT INTO Users (name, photo, bio) VALUES (%s, %s, %s)",
        (name, bio, photo))
    conn.commit()
    return render_template('admin/message.html')


@app.route("/admin/party", methods=['GET'])
def admin_party():
    return render_template('admin/party.html')


@app.route("/admin/party", methods=['POST'])
def add_party():
    date = request.form['date']
    time = request.form['time']
    cursor.execute(
        "INSERT INTO Parties (date) VALUES (%s)",
        (f'{date} {time}'))
    conn.commit()
    return render_template('admin/party.html')


if __name__ == "__main__":
    app.run()
