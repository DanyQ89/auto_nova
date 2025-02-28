import base64
from datetime import datetime

from flask import Flask, render_template, make_response, jsonify, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from utils.config import secret_key
from utils.help_functions import get_number
from forms.user import RegisterUser, LoginUser
from data.database import create_session, global_init
from data.users import User, Detail, Basket, basket_details

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


@app.route("/get_thing_by_number")
def get_thing_by_number():
    return render_template("get_thing_by_number.html")


@app.route('/<car_name>')
def show_car(car_name):
    print("Catch query", car_name)
    session = create_session()
    details = session.query(Detail).filter(Detail.brand.ilike(car_name)).all()

    # Декодируем изображения в base64
    for detail in details:
        if detail.photo:
            detail.photo = base64.b64encode(detail.photo).decode('utf-8')  # Кодируем в base64

    for detail in details:
        print(detail.name, detail.brand, detail.price)

    return render_template('car.html', products=details)


@app.route('/update_detail/<int:detail_id>', methods=['GET'])
def update_detail(detail_id):
    session = create_session()
    print("update detail with ID:", detail_id)
    detail = session.query(Detail).filter(Detail.id==detail_id).first()
    if detail:
        return jsonify({
            'id': detail.id,
            'sklad': detail.sklad,
            'ID_detail': detail.ID_detail,
            'brand': detail.brand,
            'model_and_year': detail.model_and_year,
            'name': detail.name,
            'price': detail.price,
            'price_w_discount': detail.price_w_discount,
            'comment': detail.comment,
            'orig_number': detail.orig_number,
            'condition': detail.condition,
            'percent': detail.percent,
            'CpK': detail.CpK,
            'color': detail.color,
            'data_created': detail.data_created.strftime('%Y-%m-%d')
        })
    return jsonify({'error': 'Detail not found'}), 404


@app.route('/add_detail', methods=['POST'])
def add_detail():
    print(request.form)
    session = create_session()
    if request.form['id'] == '':
        new_detail = Detail(
            creator_id=request.form['creator_id'],  # Поле для идентификатора создателя
            sklad=request.form['sklad'],  # Поле для склада
            ID_detail=request.form['ID_detail'],  # Поле для уникального идентификатора детали
            brand=request.form['brand'],  # Поле для бренда
            model_and_year=request.form['model_and_year'],  # Поле для модели и года
            name=request.form['name'],  # Поле для названия
            price=request.form['price'],  # Поле для цены
            price_w_discount=request.form.get('price_w_discount', ''),  # Поле для цены со скидкой
            comment=request.form.get('comment', ''),  # Поле для комментария
            orig_number=request.form.get('orig_number', ''),  # Поле для оригинального номера
            condition=request.form.get('condition', ''),  # Поле для состояния
            percent=request.form.get('percent', 0),  # Поле для процента
            CpK=request.form.get('CpK', ''),  # Поле для CpK
            color=request.form.get('color', ''),  # Поле для цвета
        )

        # Обработка загрузки файла
        photo = request.files.get('photo')
        if photo:
            new_detail.photo = photo.read()  # Сохраняем содержимое файла в поле BLOB

        # Добавляем новую деталь в сессию и сохраняем изменения
        session.add(new_detail)
        session.commit()
        flash('Деталь успешно добавлена!', 'success')

    else:
        detail_id = request.form['id']
        # Находим деталь по id
        detail = session.query(Detail).filter(Detail.id == detail_id).first()

        if not detail:
            flash('Деталь не найдена!', 'error')
            return redirect('/admin')  # Перенаправляем на страницу администрирования

        # Обновляем поля детали на основе данных из request.form
        detail.creator_id = request.form.get('creator_id', detail.creator_id)
        detail.sklad = request.form.get('sklad', detail.sklad)
        detail.ID_detail = request.form.get('ID_detail', detail.ID_detail)
        detail.brand = request.form.get('brand', detail.brand)
        detail.model_and_year = request.form.get('model_and_year', detail.model_and_year)
        detail.name = request.form.get('name', detail.name)
        detail.price = request.form.get('price', detail.price)
        detail.price_w_discount = request.form.get('price_w_discount', detail.price_w_discount)
        detail.comment = request.form.get('comment', detail.comment)
        detail.orig_number = request.form.get('orig_number', detail.orig_number)
        detail.condition = request.form.get('condition', detail.condition)
        detail.percent = request.form.get('percent', detail.percent)
        detail.CpK = request.form.get('CpK', detail.CpK)
        detail.color = request.form.get('color', detail.color)

        # Обработка загрузки файла (если есть)
        photo = request.files.get('photo')
        print(photo)
        if photo:
            detail.photo = photo.read()  # Сохраняем содержимое файла в поле BLOB
        # Сохраняем изменения в базе данных
        session.commit()
        flash('Деталь успешно обновлена!', 'success')

    return redirect('/admin')

@app.route("/remove_from_basket/<string:detail_id>", methods=["POST"])
@login_required
def remove_from_basket(detail_id):
    session = create_session()
    print("Removing detail with ID:", detail_id)
    detail = session.query(Detail).filter(Detail.ID_detail == detail_id).first()
    # Получаем корзину текущего пользователя
    basket = session.query(Basket).filter_by(user_id=current_user.id).first()
    if not basket:
        return jsonify({"error": "Корзина не найдена."}), 404
    print(basket)
    # Ищем деталь в корзине
    existing_detail = session.query(basket_details).filter_by(basket_id=basket.id, detail_id=detail.id).first()
    print(existing_detail)
    if existing_detail:
        print("Detail found in basket:", existing_detail)
        session.execute(basket_details.delete().where(
            (basket_details.c.basket_id == basket.id) &
            (basket_details.c.detail_id == detail.id)
        ))
        session.commit()
        return jsonify({"success": "Деталь удалена из корзины."}), 200
    else:
        print("Detail not found in basket.")
        return jsonify({"error": "Деталь не найдена в корзине."}), 404


@app.route("/basket")
def basket():
    details = []
    total_price = 0
    total_card_price = 0  # Если у вас есть специальная цена по карте

    if current_user.is_authenticated:
        session = create_session()
        basket = session.query(Basket).filter_by(user_id=current_user.id).first()
        if basket:
            details = basket.details
            for detail in details:
                total_price += float(detail.price)  # Предполагается, что price - это строка
                total_card_price += float(detail.price_w_discount)  # Если есть цена по карте

    print(details)
    return render_template("basket.html", details=details, total_price=total_price, total_card_price=total_card_price)


@app.route("/add_to_basket/<string:num>", methods=["POST"])
@login_required
def add_to_basket(num):
    print("Add catch", num)
    session = create_session()

    # Ищем деталь по номеру
    detail = session.query(Detail).filter(Detail.ID_detail==num).first()
    if detail is None:
        return jsonify({"error": "Деталь не найдена."}), 404

    # Получаем корзину текущего пользователя
    basket = session.query(Basket).filter_by(user_id=current_user.id).first()
    if not basket:
        # Если корзины нет, создаем новую
        basket = Basket(user_id=current_user.id)
        session.add(basket)

    # Проверяем, есть ли уже эта деталь в корзине
    existing_detail = session.query(basket_details).filter_by(basket_id=basket.id, detail_id=detail.id).first()
    if existing_detail:
        # Если деталь уже есть, увеличиваем количество
        existing_detail.quantity += 1
    else:
        # Если детали нет, добавляем новую запись
        new_entry = {
            'basket_id': basket.id,
            'detail_id': detail.id,
        }
        session.execute(basket_details.insert().values(new_entry))  # Используем insert для добавления

    try:
        session.commit()
    except Exception as err:
        session.rollback()  # Откатить изменения в случае ошибки
        print("Error during commit:", err)  # Отладочное сообщение
        return jsonify({"error": "Что-то пошло не так."}), 500

    return jsonify({"success": "Деталь добавлена в корзину."}), 200


@app.route("/get_detail/<string:part_number>", methods=["GET"])
def get_detail(part_number):
    session = create_session()
    detail = session.query(Detail).filter(Detail.ID_detail == part_number).first()
    detail_in_basket = False

    if current_user.is_authenticated:
        # Получаем корзину текущего пользователя
        basket = session.query(Basket).filter_by(user_id=current_user.id).first()
        if basket and detail in basket.details:
            detail_in_basket = True

    if detail:
        return jsonify({
            'id': detail.id,
            'ID_detail': detail.ID_detail,
            'orig_number': detail.orig_number,
            'brand': detail.brand,
            'model_and_year': detail.model_and_year,
            'name': detail.name,
            'price': detail.price,
            'price_w_discount': detail.price_w_discount,
            'condition': detail.condition,
            'color': detail.color,
            'comment': detail.comment,
            'photo': detail.photo,
            'detail_in_basket': detail_in_basket  # Добавляем информацию о корзине
        })
    else:
        return jsonify({'error': 'Деталь не найдена'}), 404


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


@app.route('/admin', methods=['GET', 'POST'])
async def meow():
    if not current_user.__dict__ or current_user.phone not in ['boss']:
        return jsonify({
            "error": 777,
            "message": "you don`t have the rights for this action"
        })
    session = create_session()
    details = session.query(Detail).all()
    return render_template('admin.html', details=details)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        sess = create_session()

        # Вход в админку
        if form.phone.data.lower() == 'boss':
            if form.password.data == '51974376':
                print("boss here")
                user = sess.query(User).filter(User.phone == form.phone.data.lower()).first()
                print("user found", user)
                login_user(user, remember=True)
                print("OK")
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
