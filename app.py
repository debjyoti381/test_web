from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'bank'
)

curs = conn.cursor()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/submit_about', methods = ['POST'])
def from_about_submit():
    email = request.form['email']

    query = 'select * from contact where email = %s'
    values = (email,)
    try:
        curs.execute(query,values)
        details = curs.fetchone()
        if details:
            return render_template('about.html', detail = details)
        else:
            return render_template('about.html', detail = ['No Record Found'])

    except Exception as e:
        return f"error : {e}"

@app.route('/services')
def services_page():
    return render_template('services.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/submit', methods = ['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    query = 'insert into contact (name, email, message) values (%s, %s, %s)'
    values =(name, email, message)
    try:
        curs.execute(query, values)
        conn.commit()
    except Exception as e:
        return e

    return render_template('contact.html', msg = 'Message Sent')

def close_conn():
    curs.close()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)