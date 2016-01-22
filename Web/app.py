from flask import Flask, render_template, request, flash, url_for, redirect, session
from wtforms import Form, TextField, PasswordField, validators
import pyodbc
from passlib.hash import sha256_crypt
import gc



app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password',[validators.Required(), \
                        validators.EqualTo('confirm', message='Passwords \
                        must match')
    ])
    confirm = PasswordField('Repeat Password')


class GMRegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password',[validators.Required(), \
                        validators.EqualTo('confirm', message='Passwords \
                        must match')
    ])
    confirm = PasswordField('Repeat Password')


def connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=RF_User;UID=sa;PWD=wanker12')
    cur = conn.cursor()
    return cur, conn



@app.route('/', methods=["GET"])
def main_page():
    return render_template('main.html')


@app.route('/about', methods=["GET"])
def about_page():
    return render_template('about.html')


@app.errorhandler(404)
def fileNotFound(e):
    return render_template('404.html'), 404


@app.route('/gm', methods=["GET", "POST"])
def gm_register():
    try:
        form = GMRegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            password = form.password.data
            cur, conn = connection()
            cur.execute("select id from dbo.tbl_StaffAccount where id = CONVERT(binary, ?)", (username))
            row = cur.fetchone()
            if row:
                flash(u'That username is already taken, try another one.', 'error')
                print("Username is already taken!")
                return render_template('gm.html', form=form)
            else:
                cur.execute("insert into dbo.tbl_StaffAccount (ID,PW,Grade,Depart,RealName,SubGrade,Birthday,ComClass) values(convert(binary, ?),convert(binary, ?),'2', 'none', ?, '4', '01/01/1991', 'GM')", username, password, username.strip('!'))
                conn.commit()
                flash(u'Registration successful!', 'success')
                print("Registration Successful!")
                cur.close()
                gc.collect()
        return render_template('gm.html', form=form)

    except Exception as e:
        return(str(e))


@app.route('/register', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            cur, conn = connection()
            cur.execute("select id from dbo.tbl_RFTestAccount where id = CONVERT(binary, ?)", (username))
            row = cur.fetchone()
            if row:
                flash(u'That username is already taken, try another one.', 'error')
                print("Username is already taken!")
                return render_template('register.html', form=form)

            else:
                cur.execute("insert into dbo.tbl_RFTestAccount(id, password, email) values(convert(binary(13), ?),convert(binary(13), ?), ?)", username, password, email)
                conn.commit()
                flash(u'Registration successful!', 'success')
                print("Registration Successful!")
                cur.close()
                gc.collect()

        return render_template('register.html', form=form)

    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8666, debug=True)
