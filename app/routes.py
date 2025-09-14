from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app import db
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from datetime import datetime, timezone

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username' : 'Miguel'}
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'Hello everyone'
        },
        {
            'author' : {'username' : 'hiyen'},
            'body' : 'Hello Thanh, how are you today?'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar( # db.session.scalar để trả về giá trị duy nhất của query
            sa.select(User).where(User.username == form.username.data)) # bên trong là query
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Hello co gang len nhe, roi se duoc thoi'}, 
        {'author': user, 'body': 'Nếu hôm nay bỏ cuộc, thì sẽ thất bại mãi về sau'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request # ham nay se hoat dong ngay truoc view function -> kiem tra xem nguoi dung co dang nhap khong -> neu co update time hien tai vao database
def before_request():
    if current_user.is_authenticated:
        current_user.last_time = datetime.now(timezone.utc)
        db.session.commit() # khong can db.session.add() nua vi session da ghi nho user bang flask_login

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your change has been saved!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit profile', form=form)
