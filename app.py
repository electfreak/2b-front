from flask import Flask, render_template, request, abort
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import requests

app = Flask(__name__)

mysql = MySQL()

# configuring MySQL for the web application
# default user of MySQL to be replaced with appropriate username
app.config['MYSQL_DATABASE_USER'] = 'group25admin'
app.config[
    'MYSQL_DATABASE_PASSWORD'] = 'MoveSent'  # default passwrod of MySQL to be replaced with appropriate password
# Database name to be replaced with appropriate database name
app.config['MYSQL_DATABASE_DB'] = 'group25'
app.config[
    'MYSQL_DATABASE_HOST'] = 'localhost'  # default database host of MySQL to be replaced with appropriate database host
# initialise mySQL
mysql.init_app(app)
# create connection to access data

ip_info_token = "f78203537e6d2e"

def get_all_users():
    query = f"""
    SELECT name FROM Users
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    
    return [x['name'] for x in cursor.fetchall()]

def get_all_addresses():
    query = f"""
    SELECT address FROM Locations
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    
    return [x['address'] for x in cursor.fetchall()]

def get_all_coordinates():
    query = f"""
    SELECT coordinates FROM Locations
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    
    return [x['coordinates'] for x in cursor.fetchall()]

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
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

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

@app.route("/admin/obligatory", methods=['GET'])
def admin_obligatory():
    return render_template('admin/obligatory.html')

@app.route("/admin/obligatory", methods=['POST'])
def add_obligatory():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    tid = request.form['tid']
    pid = request.form['pid']

    cursor.execute(
        "INSERT INTO ObligatoryTasks (tid) VALUES ( %s)",
        (tid)
    )
    cursor.execute(
        "INSERT INTO PartyToObligatoryTasks (pid, otid) VALUES (%s, LAST_INSERT_ID())",
        (pid,)
    )
    conn.commit()
    return render_template("/admin/obligatory.html")

@app.route("/admin/urgent", methods=['GET'])
def admin_urgent():
    return render_template('admin/urgent.html')

@app.route("/admin/urgent", methods=['POST'])
def add_urgent():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    tid = request.form['tid']
    pid = request.form['pid']

    cursor.execute(
        "INSERT INTO UrgentTasks (tid) VALUES ( %s)",
        (tid)
    )
    cursor.execute(
        "INSERT INTO PartyToUrgentTasks (pid, utid) VALUES (%s, LAST_INSERT_ID())",
        (pid,)
    )
    conn.commit()
    return render_template("/admin/urgent.html")


@app.route("/admin/room", methods=['GET'])
def admin_room():
    return render_template('admin/room.html')

@app.route("/admin/room", methods=['POST'])
def add_room():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    number = request.form['number']
    building = request.form['building']
    lid = request.form['lid']

    cursor.execute(
        "INSERT INTO Rooms (number, building, lid) VALUES ( %s, %s, %s)",
        (number, building, lid)
    )
    conn.commit()
    return render_template("/admin/room.html")



@app.route("/admin/party_notification", methods=['GET'])
def admin_party_notification():
    return render_template('admin/party_notification.html')

@app.route("/admin/party_notification", methods=['POST'])
def add_party_notification():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    mid = request.form['mid']
    pid = request.form['pid']

    cursor.execute(
        "INSERT INTO PartyNotifications (mid) VALUES ( %s)",
        (mid)
    )
    cursor.execute(
        "INSERT INTO PartyToPartyNotifications (pid, pnid) VALUES (%s, LAST_INSERT_ID())",
        (pid,)
    )
    conn.commit()
    return render_template("/admin/party_notification.html")


@app.route("/admin/party_announcement", methods=['GET'])
def admin_party_announcement():
    return render_template('admin/party_announcement.html')

@app.route("/admin/party_announcement", methods=['POST'])
def add_party_announcement():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    mid = request.form['mid']
    pid = request.form['pid']

    cursor.execute(
        "INSERT INTO PartyAnnouncements (mid) VALUES ( %s)",
        (mid)
    )
    cursor.execute(
        "INSERT INTO PartyToPartyAnnouncement (pid, paid) VALUES (%s, LAST_INSERT_ID())",
        (pid,)
    )
    conn.commit()
    return render_template("/admin/party_announcement.html")



@app.route("/admin/user", methods=['GET'])
def admin_user():
    return render_template('admin/user.html')


@app.route("/admin/users", methods=['GET'])
def get_users():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select uid from Users")
    conn.commit()
    res = {'options': cursor.fetchall()}
    print(res)
    return res


@app.route("/admin/messages", methods=['GET'])
def get_messages():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select mid from Messages")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/locations", methods=['GET'])
def get_locations():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select lid from Locations")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/tasks", methods=['GET'])
def get_tasks():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select tid from Tasks")
    conn.commit()
    return {'options': cursor.fetchall()}

@app.route("/admin/urgents", methods=['GET'])
def get_urgents():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select utid from UrgentTasks")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/obligatories", methods=['GET'])
def get_obligatories():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select otid from ObligatoryTasks")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/announcements", methods=['GET'])
def get_announcements():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select paid from PartyAnnouncements")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/notifications", methods=['GET'])
def get_notifications():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select pnid from PartyNotifications")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/feedbacks", methods=['GET'])
def get_feedbacks():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select fid from Feedbacks")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/user", methods=['POST'])
def add_user():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

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
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401


    uid = request.form['uid']
    text = request.form['text']
    date = request.form['date']
    time = request.form['time']
    cursor.execute(
        "INSERT INTO Messages (uid, text, time) VALUES (%s, %s, %s)",
        (uid, text, f'{date} {time}'))
    conn.commit()
    return render_template('admin/message.html')


@app.route("/admin/task", methods=['GET'])
def admin_task():
    return render_template('admin/task.html')


@app.route("/admin/task", methods=['POST'])
def add_task():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    text = request.form['text']
    cursor.execute(
        "INSERT INTO Tasks (text) VALUES (%s)",
        (text))
    conn.commit()
    return render_template('admin/task.html')


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

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('single_entity/message.html', mid=mid, message=cursor.fetchall())

@app.route("/user")
def view_user():
    if 'uid' not in request.args:
        abort(404)
    
    uid = request.args['uid']

    query = f"""
    SELECT Users.*
    FROM Users
    WHERE uid = {uid};
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('single_entity/user.html', uid=uid, user=cursor.fetchall())



@app.route("/location")
def view_location():
    if 'lid' not in request.args:
        abort(404)
    
    lid = request.args['lid']

    query = f"""
    SELECT Locations.*
    FROM Locations
    WHERE lid = {lid};
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('single_entity/location.html', lid=lid, location=cursor.fetchall())


@app.route("/feedback")
def view_feedback():
    if 'fid' not in request.args:
        abort(404)
    
    fid = request.args['fid']

    query = f"""
    SELECT *
    FROM Feedbacks
    JOIN Messages ON Messages.mid = Feedbacks.mid
    WHERE Feedbacks.fid = {fid}
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('single_entity/feedback.html', fid=fid, feedback=cursor.fetchall())


@app.route("/party")
def view_party():
    if 'pid' not in request.args:
        abort(404)
    
    pid = request.args['pid']

    query = f"""
    SELECT *
    FROM Parties
    WHERE Parties.pid = {pid}
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('single_entity/party.html', pid=pid, party=cursor.fetchall())


@app.route("/admin/party", methods=['GET'])
def admin_party():
    return render_template('admin/party.html')


@app.route("/admin/party", methods=['POST'])
def add_party():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401
    
    start_date = request.form['start_date']
    start_time = request.form['start_time']
    has_end = '1' if 'has_end' in request.form else '0'
    end_date = request.form['end_date']
    end_time = request.form['end_time']
    lid = request.form['lid']

    cursor.execute(
        "INSERT INTO Parties (startDate, hasEnd, endDate) VALUES (%s, %s, %s)",
        (f'{start_date} {start_time}', has_end, f'{end_date} {end_time}'))
    cursor.execute(
        "INSERT INTO PartyToLocation (pid, lid) VALUES (LAST_INSERT_ID(), %s)",
        (lid,)
    )
    conn.commit()
    return render_template('admin/party.html')


@app.route("/admin/parties", methods=['GET'])
def get_parties():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select pid from Parties")
    conn.commit()
    return {'options': cursor.fetchall()}


@app.route("/admin/location", methods=['GET'])
def admin_location():
    return render_template('admin/location.html')


@app.route("/admin/location", methods=['POST'])
def add_location():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

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
    tags = {
        'users': get_all_users()
    }
    return render_template("/admin/requests/get_messages_from_user.html", tags=tags)

@app.route("/admin/requests/get_messages_from_user", methods=['POST'])
def get_messages_from_user():
    name = request.form['username']

    tags = {
        'users': get_all_users()
    }

    query = f"""
    SELECT Messages.*
    FROM Messages, Users
    WHERE Messages.uid = Users.uid
    AND Users.name = '{name}'
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/get_messages_from_user.html', user=name, messages=cursor.fetchall(), tags=tags)


@app.route("/admin/requests/get_feedbacks_by_party", methods=['GET'])
def get_feedbacks_by_party_get():
    return render_template("/admin/requests/get_feedbacks_by_party.html")


@app.route("/admin/requests/get_feedbacks_by_party", methods=['POST'])
def get_feedbacks_by_party():
    pid = request.form['pid']

    query = f"""
    SELECT Feedbacks.fid, Feedbacks.rating, Messages.text
    FROM Feedbacks, Messages, Parties, PartyToFeedback
    WHERE Parties.pid = PartyToFeedback.pid
    AND Feedbacks.fid = PartyToFeedback.fid
    AND Feedbacks.mid = Messages.mid
    AND Parties.pid = {pid}
    """

    print(query)

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
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

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/get_ongoing_parties.html', cur_date=cur_date, parties=cursor.fetchall())


@app.route("/admin/requests/search_locations", methods=['GET'])
def search_locations_get():
    tags = {
        'addresses': get_all_addresses(),
        'coordinates': get_all_coordinates()
    }

    return render_template("/admin/requests/search_locations.html", tags=tags)


@app.route("/admin/requests/search_locations", methods=['POST'])
def search_locations():
    term = request.form['term']

    tags = {
        'addresses': get_all_addresses(),
        'coordinates': get_all_coordinates()
    }

    query = f"""
    SELECT lid, coordinates, address FROM Locations
    WHERE coordinates LIKE '%{term}%'
    OR address LIKE '%{term}%'
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()
    return render_template('/admin/requests/search_locations.html', term=term, locations=cursor.fetchall(), tags=tags)


@app.route("/admin/requests/search_users", methods=['GET'])
def search_users_get():

    tags = {
        'users': get_all_users()
    }

    return render_template("/admin/requests/search_users.html", tags=tags)


@app.route("/admin/requests/search_users", methods=['POST'])
def search_users():
    term = request.form['term']

    tags = {
        'users': get_all_users()
    }

    query = f"""
    SELECT uid, name, photo, bio FROM Users
    WHERE name LIKE '%{term}%'
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()

    return render_template('/admin/requests/search_users.html', term=term, users=cursor.fetchall(), tags=tags)


@app.route("/admin/relations/party_to_feedback", methods=['GET'])
def admin_party_to_feedback():
    return render_template('admin/relations/party_to_feedback.html')


@app.route("/admin/relations/party_to_feedback", methods=['POST'])
def add_party_to_feedback():
    login = request.form['login']
    password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE login = %s AND password = %s', (login, password,))
    account = cursor.fetchone()

    if not account:
        return "Account with such login and password was not found", 401

    pid = request.form['pid']
    fid = request.form['fid']

    cursor.execute(
        "INSERT INTO PartyToFeedback (pid, fid) VALUES (%s, %s)",
        (pid, fid)
    )
    conn.commit()
    return render_template('admin/relations/party_to_feedback.html')

@app.route("/ac_test")
def ac_test():
    return render_template('ac_test.html', tags={'users': get_all_users()})

@app.route("/get_users_term")
def get_users_term():
    term = request.args["term"]

    query = f"""
    SELECT name FROM Users
    WHERE name LIKE '%{term}%'
    """

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)
    cursor.execute(query)
    conn.commit()


    return {"users": [x['name'] for x in cursor.fetchall()]}

@app.route("/map")
def display_location():
    ip = request.remote_addr

    request_url = f"http://ipinfo.io/{ip}?token={ip_info_token}" 

    r = requests.get(
        request_url
    )

    if 'bogon' in r.json() and r.json()['bogon']:
        r = requests.get("https://api.ipify.org?format=json")
        ip = r.json()['ip']

        request_url = f"http://ipinfo.io/{ip}?token={ip_info_token}" 
        r = requests.get(
            request_url
        )


    user_coords = r.json()['loc']

    return render_template('map.html', user_coords=user_coords, user_ip=ip)


if __name__ == "__main__":
    app.run(port=12354, host="0.0.0.0")
