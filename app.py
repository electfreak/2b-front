from flask import Flask, render_template, request, abort
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

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
dcursor = conn.cursor(DictCursor)

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/imprint")
def imprint():
    return render_template('imprint.html')


@app.route("/admin")
def admin():
    return render_template('admin/admin.html')


@app.route("/admin/feedback", methods=['GET'])
def admin_feedback():
    return render_template('admin/feedback.html')


@app.route("/admin/feedback", methods=['POST'])
def add_feedback():
    mid = request.form['mid']
    pid = request.form['pid']
    rating = request.form['rating']

    cursor.execute(
        "INSERT INTO Feedbacks (mid, pid, rating) VALUES (%s, %s, %s)",
        (mid, pid, rating)
    )
    cursor.execute(
        "INSERT INTO PartyToFeedback (pid, fid) VALUES (%s, LAST_INSERT_ID())",
        (pid,)
    )
    conn.commit()
    return render_template("/admin/feedback.html")


@app.route("/admin/user", methods=['GET'])
def admin_user():
    return render_template('admin/user.html')


@app.route("/admin/users", methods=['GET'])
def get_users():
    cursor.execute("select uid from Users")
    conn.commit()
    return {'uids': cursor.fetchall()}


@app.route("/admin/user", methods=['POST'])
def add_user():
    print(request.form)

    name = request.form['name']
    bio = request.form['bio']
    photo = request.form['photo']
    cursor.execute(
        "INSERT INTO Users (name, photo, bio) VALUES (%s, %s, %s)",
        (name, photo, bio))
    conn.commit()
    return render_template("admin/user.html")


@app.route("/admin/message", methods=['GET'])
def admin_message():
    return render_template('admin/message.html')


@app.route("/admin/message", methods=['POST'])
def add_message():
    uid = request.form['uid']
    text = request.form['text']
    date = request.form['date']
    time = request.form['time']
    cursor.execute(
        "INSERT INTO Messages (uid, text, time) VALUES (%s, %s, %s)",
        (uid, text, f'{date} {time}'))
    conn.commit()
    return render_template('admin/message.html')


@app.route("/message")
def view_message():
    if 'mid' not in request.args:
        abort(404)
    
    mid = request.args['mid']

    query = f"""
    SELECT *
    FROM Messages
    JOIN Users ON Messages.uid = Users.uid
    WHERE Messages.mid = {mid}
    """

    dcursor.execute(query)
    conn.commit()
    return render_template('single_entity/message.html', mid=mid, message=dcursor.fetchall())



@app.route("/admin/party", methods=['GET'])
def admin_party():
    return render_template('admin/party.html')


@app.route("/admin/party", methods=['POST'])
def add_party():
    start_date = request.form['start_date']
    start_time = request.form['start_time']
    has_end = '1' if 'has_end' in request.form else '0'
    end_date = request.form['end_date']
    end_time = request.form['end_time']

    cursor.execute(
        "INSERT INTO Parties (startDate, hasEnd, endDate) VALUES (%s, %s, %s)",
        (f'{start_date} {start_time}', has_end, f'{end_date} {end_time}'))
    conn.commit()
    return render_template('admin/party.html')


@app.route("/admin/parties", methods=['GET'])
def get_parties():
    cursor.execute("select pid from Parties")
    conn.commit()
    return {'pids': cursor.fetchall()}


@app.route("/admin/location", methods=['GET'])
def admin_location():
    return render_template('admin/location.html')


@app.route("/admin/location", methods=['POST'])
def add_location():
    coordinates = request.form['coordinates']
    address = request.form['address']

    cursor.execute(
        "INSERT INTO Locations (coordinates, address) VALUES (%s, %s)",
        (coordinates, address)
    )
    conn.commit()
    return render_template('admin/location.html')


@app.route("/admin/requests/get_messages_from_user", methods=['GET'])
def get_messages_from_user_get():
    return render_template("/admin/requests/get_messages_from_user.html")

@app.route("/admin/requests/get_messages_from_user", methods=['POST'])
def get_messages_from_user():
    uid = request.form['uid']

    query = f"""
    SELECT Messages.*
    FROM Messages, Users
    WHERE Messages.uid = Users.uid
    AND Users.uid = {uid}
    """

    dcursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/get_messages_from_user.html', user=uid, messages=dcursor.fetchall())


@app.route("/admin/requests/get_feedbacks_by_party", methods=['GET'])
def get_feedbacks_by_party_get():
    return render_template("/admin/requests/get_feedbacks_by_party.html")


@app.route("/admin/requests/get_feedbacks_by_party", methods=['POST'])
def get_feedbacks_by_party():
    pid = request.form['pid']

    query = f"""
    SELECT  Feedbacks.rating, Messages.text
    FROM Feedbacks, Messages, Parties, PartyToFeedback
    WHERE Parties.pid = PartyToFeedback.pid
    AND Feedbacks.fid = PartyToFeedback.fid
    AND Feedbacks.mid = Messages.mid
    AND Parties.pid = {pid}
    """

    print(query)

    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/get_feedbacks_by_party.html', party=pid, feedbacks=cursor.fetchall())


@app.route("/admin/requests/get_ongoing_parties", methods=['GET'])
def get_ongoing_parties_get():
    return render_template("/admin/requests/get_ongoing_parties.html")


@app.route("/admin/requests/get_ongoing_parties", methods=['POST'])
def get_ongoing_parties():
    cur_date = f"{request.form['date']} {request.form['time']}"

    query = f"""
    SELECT pid, startDate, hasEnd, endDate FROM Parties
    WHERE startDate <= '{cur_date}'
    AND (hasEnd = 0 OR endDate >= '{cur_date}')
    """

    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/get_ongoing_parties.html', cur_date=cur_date, parties=cursor.fetchall())


@app.route("/admin/requests/search_locations", methods=['GET'])
def search_locations_get():
    return render_template("/admin/requests/search_locations.html")


@app.route("/admin/requests/search_locations", methods=['POST'])
def search_locations():
    term = request.form['term']

    query = f"""
    SELECT coordinates, address FROM Locations
    WHERE coordinates LIKE '%{term}%'
    OR address LIKE '%{term}%'
    """

    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/search_locations.html', term=term, locations=cursor.fetchall())


@app.route("/admin/requests/search_users", methods=['GET'])
def search_users_get():
    return render_template("/admin/requests/search_users.html")


@app.route("/admin/requests/search_users", methods=['POST'])
def search_users():
    term = request.form['term']

    query = f"""
    SELECT name, photo, bio FROM Users
    WHERE name LIKE '%{term}%'
    """

    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/search_users.html', term=term, users=cursor.fetchall())


if __name__ == "__main__":
    app.run()
