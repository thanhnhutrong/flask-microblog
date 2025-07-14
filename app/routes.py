from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Miguel'}
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'Hello everyone'
        },
        {
            'author' : {'username' : 'hiyen'},
            'body' : 'Hello Thanh, i miss u so much.'
        }
    ]
    # return render_template('index.html', title='Home', user=user)
    return render_template('index.html', user=user, posts=posts)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for user{}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title="Login Page", form=form)