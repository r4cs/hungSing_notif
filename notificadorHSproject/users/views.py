# notificadorHSproject/users/views.py

import datetime
import time
from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required, fresh_login_required

from notificadorHSproject import db, app
from notificadorHSproject.models import User, DelUser
from notificadorHSproject.users.forms import RegistrationForm, LoginForm, UpdateUserForm, DeleteUserForm
from notificadorHSproject.email_sender import activate_mail, send_mail

from itsdangerous import URLSafeTimedSerializer, SignatureExpired
serializer = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        # logout_user()
        return render_template('error_pages/403.html'), 403


    if form.validate_on_submit():
        user = User(email=request.form['email'],
                    enrollment=request.form['enrollment'],
                    username=request.form['username'],
                    last_name=request.form['last_name'],
                    age=request.form['age'],
                    # level=request.form.getlist('check'),
                    beginer=bool(request.form.get('inic')),
                    interm=bool(request.form.get('interm')),
                    adv=bool(request.form.get('adv')),
                    cellphone=request.form['cellphone'],
                    franchise=request.form['franchise'],
                    password=request.form['password'],
                    confirmed=False)

        # if User.query.filter_by(enrollment='enrollment') is None:
        #     return render_template('error_pages/409.html'), 409
        #
        # elif User.query.filter_by(email='email') is None:
        #     return render_template('error_pages/409.html'), 409

        # else:
        db.session.add(user)
        db.session.commit()

        # token = serializer.dumps(user.email, salt=app.config['PASSWORD_SALT'])
        # link = url_for('users.confirm_email', token=token, _external=True)
        # activate_mail(user.email, link)

        login_user(user, remember=True)

        #flash('Um email de confirmação foi enviado para seu email.', 'success')
        #time.sleep(3)
        return redirect(url_for("users.unconfirmed"))


    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        # logout_user()
        # flash("Você já está logado!")
        return render_template('error_pages/403.html'), 403

    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user is not None and user.check_password(form.password.data):
            #Log in the user
            session.permanent=True
            login_user(user, remember=True)
            # flash('Logade com sucesso (;')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html', form=form, current_user=current_user)


@users.route('/confirm_email/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        # flash("Conta já confirmada. Faça login", 'success')
        return redirect(url_for('index'))

    email = serializer.loads(token, salt=app.config['PASSWORD_SALT'])
    user = User.query.filter_by(email=current_user.email).first_or_404()

    if user.email == email:
        user.confirmed = True
        db.session.commit()
        # flash("Você confirmou sua conta !", "success")
        send_mail(user.username, user.email, user.password)
        time.sleep(3)
        return render_template('index.html')
    else:
        flash("O link de confirmação é inválido ou expirou", "danger")

    return render_template('index.html')

@users.route('/unconfirmed')
# @check_confirmed
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('core.index'))
    # flash('Você precisa confirmar sua conta para ter acesso!', 'warning')
    return render_template('unconfirmed.html')

@users.route('/resend')
@login_required
def resend_confirmation():
    token = serializer.dumps(current_user.email, salt=app.config['PASSWORD_SALT'])
    link = url_for('users.confirm_email', token=token, _external=True)
    activate_mail(current_user.email, link)
    # flash('Um email de confirmação foi enviado para seu email.', 'success')
    return redirect(url_for('users.unconfirmed'))


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@fresh_login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        # form.username.data = current_user.username
        form.email.data = current_user.email
        current_user.cellphone = form.cellphone.data
        # current_user.level = request.form.getlist('check')
        current_user.begginer = bool(request.form.get('inic'))
        current_user.interm = bool(request.form.get('interm'))
        current_user.adv = bool(request.form.get('adv'))
        current_user.age = form.age.data
        current_user.franchise = form.franchise.data

        # # current_user.username = form.username.data
        # current_user.email = request.form['email']
        # print(current_user.email)
        # current_user.cellphone = request.form['cellphone']
        # current_user.level = request.form['level']
        # current_user.age = request.form['age']
        # current_user.franchise = request.form['franchise']
        # current_user.notifications = request.form['notifications']
        # print('Notifications:', current_user.notifications)

        db.session.commit()
        flash('Conta atualizada', 'success')
        # return redirect(url_for('users.account'))

    return render_template('account.html', form=form)


@users.route("/del_account", methods=['GET', 'POST'])
@fresh_login_required
def del_account():
    del_form = DeleteUserForm()

    if del_form.validate_on_submit():
        del_users = DelUser(
            email=current_user.email,
            enrollment=current_user.enrollment,
            username=current_user.username,
            last_name=current_user.last_name,
            age=current_user.age,
            beginer=bool(request.form.get('inic')),
            interm=bool(request.form.get('interm')),
            adv=bool(request.form.get('adv')),
            cellphone=current_user.cellphone,
            franchise=current_user.franchise
        )

        db.session.add(del_users)
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for('core.index'))

    return render_template('del_account.html', del_form=del_form)
