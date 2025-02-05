from flask import Flask, render_template, make_response, jsonify, flash, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from utils.config import secret_key
from utils.help_functions import get_number
from forms.user import RegisterUser, LoginUser
from data.database import create_session, global_init
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=["GET", "POST"])
def main_page():
    print(1)
    print(current_user.__dict__)
    return render_template("index.html")


@app.route("/guarantees")
def guarantee():
    return render_template("guarantees.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/enter_data", methods=["GET", "POST"])
def enter_data():
    form = RegisterUser()
    if form.validate_on_submit():
        sess = create_session()
        user = sess.query(User).filter(User.phone == form.phone.data).first()
        if not user:
            new_user = User(
                name=form.name.data,
                phone=form.phone.data,
                address=form.address.data
            )
            sess.add(new_user)
            flash('Контактные данные успешно добавлены!', 'success')

        else:
            user.name = form.name.data
            user.phone = form.phone.data
            user.address = form.address.data
            flash('Контактные данные успешно изменены!', 'success')

        sess.commit()
    return render_template('enter_data.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        sess = create_session()
        phone = get_number(form.phone.data)
        if not phone:
            return render_template('register.html',
                                   form=form,
                                   message='Неверный формат номера')
        user = sess.query(User).filter(User.phone == phone).first()

        if not user:
            new_user = User(
                name=form.name.data,
                phone=phone,
                address=form.address.data,
                password=form.password.data
            )
            sess.add(new_user)
            sess.commit()
            login_user(new_user, remember=True)
            return redirect('/')

        else:
            return render_template('register.html',
                                   form=form,
                                   message='Пользователь с таким номером уже зарегистрирован')
    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        sess = create_session()

        # Вход в админку
        if form.phone.data.lower() == 'boss':
            if form.password.data == '51974376':
                user = sess.query(User).filter(User.phone == form.phone.data.lower()).first()
                login_user(user, remember=True)
                return redirect('/admin')
            else:
                return render_template('login.html',
                                       message="Неверный пароль",
                                       form=form)

        phone = get_number(form.phone.data)

        user = sess.query(User).filter(User.phone == phone).first()
        if not user:
            return render_template('login.html',
                                   message="Пользователь с таким номером не найден",
                                   form=form)
        else:
            if form.password.data == user.password:
                login_user(user, remember=True)
                return redirect('/')
            else:
                return render_template('login.html',
                                       message='Неверно введён пароль пользователя',
                                       form=form)

    return render_template('login.html', form=form)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    sess = create_session()
    user = sess.query(User).get(current_user.id)
    form = RegisterUser(obj=user)
    # phone = get_number(form.phone.data)
    if form.validate_on_submit():
        user = sess.query(User).filter(User.phone == form.phone.data).first()

        user.name = form.name.data
        user.address = form.address.data
        user.password = form.password.data
        sess.commit()
        return redirect('/')

    return render_template('edit_user.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
async def meow():
    # отслеживание админов в списке
    if not current_user.__dict__ or current_user.phone not in ['boss']:
        return jsonify({
            "error": 777,
            "message": "you don`t have the rights for this action"
        })
    return render_template('admin.html')


@login_manager.user_loader
def load_user(user_id):
    sess = create_session()
    return sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found_error(_):
    return make_response(jsonify({'error': "this page doesn`t exist"}))


if __name__ == '__main__':
    global_init("./db/data.sqlite")
    app.register_error_handler(404, not_found_error)

    app.run(port=8888, host='127.0.0.1', debug=True)
