from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/market")
@login_required
def market_page():
    items = Item.query.all()  # returns the list of item objects stored in market.db file.
    return render_template('market.html', items=items)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully ! You are logged in as {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}:  # if the the form.error dictionary is not empty
        for err_msg in form.errors.values():
            flash(f'There is an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attemped_user = User.query.filter_by(username = form.username.data).first()
        if attemped_user and attemped_user.check_password_correction(attempted_password=form.password.data):
            login_user(attemped_user)
            flash(f'Success! You are logged in as {attemped_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password do not match', category='danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been loggedout", category="info")
    return redirect(url_for('home_page'))
