from flask import Flask, render_template, make_response, jsonify, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from sqlalchemy.orm import joinedload

from utils.config import secret_key
from utils.help_functions import get_number
from forms.user import RegisterUser, LoginUser
from data.database import create_session, global_init
from data.users import User, Detail, Basket, basket_details, Photo
import base64


global_init()


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=["GET", "POST"])
def main_page():
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
    session = create_session()
    details = session.query(Detail).filter(Detail.brand.ilike(car_name)).all()

    # Декодируем все изображения в base64
    for detail in details:
        if detail.photos:
            # Получаем все фото и кодируем их в base64
            encoded_photos = []
            for photo in detail.photos:
                if photo.photo:  # Проверяем, что фото существует
                    encoded_photos.append(base64.b64encode(photo.photo).decode('utf-8'))
            detail.encoded_photos = encoded_photos  # Сохраняем список закодированных изображений
        else:
            detail.encoded_photos = []  # Если нет фотографий, устанавливаем пустой список

    session.close()  # Закрываем сессию
    return render_template('car.html', products=details)


@app.route('/edit_photo/<int:photo_id>', methods=['PUT'])
def edit_photo(photo_id):
    session = create_session()
    photo = session.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        session.close()
        return {'status': 'error', 'message': 'Фото не найдено'}, 404

    if 'file' not in request.files:
        session.close()
        return {'status': 'error', 'message': 'Нет файла для загрузки'}, 400

    file = request.files.get('file')
    if file:
        photo.photo = file.read()
        session.commit()
        session.close()
        return {'status': 'success', 'message': 'Фото успешно обновлено!'}, 200
    else:
        session.close()
        return {'status': 'error', 'message': 'Файл отсутствует'}, 400


@app.route('/delete_photo/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    session = create_session()
    photo = session.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        session.close()
        return {'status': 'error', 'message': 'Фото не найдено'}, 404

    session.delete(photo)
    session.commit()
    session.close()
    return {'status': 'success', 'message': 'Фото успешно удалено!'}, 200


@app.route('/add_photo', methods=['POST'])
def add_photo():
    print("catch add photo", request.form.get('detail_id'))
    detail_id = request.form.get('detail_id')
    if 'file' not in request.files:
        return {'status': 'error', 'message': 'Нет файла для загрузки'}, 400

    file = request.files.get('file')  # Получаем один файл
    session = create_session()
    detail = session.query(Detail).filter(Detail.id == detail_id).first()

    if detail and file:
        new_photo = Photo(detail_id=detail.id, photo=file.read())
        print("Ok")
        session.add(new_photo)
        session.commit()
        session.close()
        return {'status': 'success', 'message': 'Фото обновлено успешно!'}, 200
    else:
        session.close()
        return {'status': 'error', 'message': 'Деталь не найдена или файл отсутствует'}, 404


@app.route('/update_detail/<int:detail_id>', methods=['GET'])
def update_detail(detail_id):
    session = create_session()
    print("update detail with ID:", detail_id)
    detail = session.query(Detail).filter(Detail.id == detail_id).first()
    if detail:
        response = jsonify({
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
            'color': detail.color,
            'data_created': detail.data_created.strftime('%Y-%m-%d')
        })

        session.close()  # Закрываем сессию
        return response
    session.close()  # Закрываем сессию
    return jsonify({'error': 'Detail not found'}), 404


@app.route('/add_detail', methods=['POST'])
async def add_detail():
    session = create_session()
    print(request.form)
    if request.form['id'] == '':
        new_detail = Detail(
            creator_id=request.form['creator_id'],
            sklad=request.form['sklad'],
            ID_detail=request.form['ID_detail'],
            brand=request.form['brand'],
            model_and_year=request.form['model_and_year'],
            name=request.form['name'],
            price=request.form['price'],
            price_w_discount=request.form.get('price_w_discount', ''),
            comment=request.form.get('comment', ''),
            orig_number=request.form.get('orig_number', ''),
            condition=request.form.get('condition', ''),
            percent=request.form.get('percent', 0),
            color=request.form.get('color', ''),
        )

        # Обработка загрузки файлов
        photo = request.files.get('photo')
        if photo:
            new_photo = Photo(detail=new_detail, photo=photo.read())
            session.add(new_photo)

        session.add(new_detail)
        session.commit()
        flash('Деталь успешно добавлена!', 'success')

    else:
        detail_id = request.form['id']
        detail = session.query(Detail).filter(Detail.id == detail_id).first()

        if not detail:
            flash('Деталь не найдена!', 'error')
            session.close()
            return redirect('/admin')

        # Обновляем поля детали
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
        detail.color = request.form.get('color', detail.color)

        # Обработка загрузки файлов
        photo = request.files.get('photo')
        if photo:
            new_photo = Photo(detail_id=detail.id, photo=photo.read())
            session.add(new_photo)

        session.commit()
        flash('Деталь успешно обновлена!', 'success')

    session.close()
    return redirect('/admin')


@app.route("/remove_from_basket/<string:detail_id>", methods=["POST"])
@login_required
def remove_from_basket(detail_id):
    session = create_session()
    print("Removing detail with ID:", detail_id)
    detail = session.query(Detail).filter(Detail.ID_detail == detail_id).first()
    basket = session.query(Basket).filter_by(user_id=current_user.id).first()
    if not basket:
        session.close()  # Закрываем сессию
        return jsonify({"error": "Корзина не найдена."}), 404
    existing_detail = session.query(basket_details).filter_by(basket_id=basket.id, detail_id=detail.id).first()
    if existing_detail:
        session.execute(basket_details.delete().where(
            (basket_details.c.basket_id == basket.id) &
            (basket_details.c.detail_id == detail.id)
        ))
        session.commit()
        session.close()  # Закрываем сессию
        return jsonify({"success": "Деталь удалена из корзины."}), 200
    else:
        print("Detail not found in basket.")
        session.close()  # Закрываем сессию
        return jsonify({"error": "Деталь не найдена в корзине."}), 404


@app.route("/basket")
def basket():
    details = []
    total_price = 0
    total_card_price = 0

    if current_user.is_authenticated:
        session = create_session()
        basket = session.query(Basket).filter_by(user_id=current_user.id).first()
        if basket:
            details = basket.details
            for detail in details:
                print(f"ID: {detail.id}")
                print(f"Creator ID: {detail.creator_id}")
                print(f"Sklad: {detail.sklad}")
                print(f"ID Detail: {detail.ID_detail}")
                print(f"Brand: {detail.brand}")
                print(f"Model and Year: {detail.model_and_year}")
                print(f"Name: {detail.name}")
                print(f"Price: {detail.price}")
                print(f"Price with Discount: {detail.price_w_discount}")
                print(f"Comment: {detail.comment}")
                print(f"Original Number: {detail.orig_number}")
                print(f"Condition: {detail.condition}")
                print(f"Percent: {detail.percent}")
                print(f"Color: {detail.color}")
                print(f"Date Created: {detail.data_created}")
                print("-" * 40)  # Разделитель для удобства чтения

                total_price += float(detail.price)
                total_card_price += float(detail.price_w_discount) if detail.price_w_discount else float(detail.price)

        session.close()  # Закрываем сессию
    return render_template("basket.html", details=details, total_price=total_price, total_card_price=total_card_price)
@app.route("/add_to_basket/<string:num>", methods=["POST"])
@login_required
def add_to_basket(num):
    session = create_session()
    print("Add catch", num)
    detail = session.query(Detail).filter(Detail.ID_detail == num).first()
    if detail is None:
        session.close()  # Закрываем сессию
        return jsonify({"error": "Деталь не найдена."}), 404

    basket = session.query(Basket).filter_by(user_id=current_user.id).first()
    if not basket:
        basket = Basket(user_id=current_user.id)
        session.add(basket)

    existing_detail = session.query(basket_details).filter_by(basket_id=basket.id, detail_id=detail.id).first()
    if existing_detail:
        pass
    else:
        new_entry = {
            'basket_id': basket.id,
            'detail_id': detail.id,
        }
        session.execute(basket_details.insert().values(new_entry))

    try:
        session.commit()
    except Exception as err:
        session.rollback()
        print("Error during commit:", err)
        session.close()  # Закрываем сессию
        return jsonify({"error": "Что-то пошло не так ."}), 500

    session.close()  # Закрываем сессию
    return jsonify({"success": "Деталь добавлена в корзину."}), 200


@app.route("/get_detail/<string:part_number>", methods=["GET"])
def get_detail(part_number):
    session = create_session()
    detail = session.query(Detail).filter(Detail.ID_detail == part_number).first()
    detail_in_basket = False

    if current_user.is_authenticated:
        user_basket = session.query(Basket).filter_by(user_id=current_user.id).first()
        if user_basket and detail in user_basket.details:
            detail_in_basket = True

    if detail:
        # Получаем первое фото, если оно существует
        first_photo = detail.photos[0].photo if detail.photos else None
        photo_data = base64.b64encode(first_photo).decode('utf-8') if first_photo else 0

        session.close()
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
            'photo': photo_data,  # Возвращаем закодированное изображение или 0
            'detail_in_basket': detail_in_basket
        })

    session.close()  # Закрываем сессию
    return jsonify({'error': 'Деталь не найдена'}), 404


@app.route("/enter_data", methods=["GET", "POST"])
def enter_data():
    form = RegisterUser()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.phone == form.phone.data).first()
        if not user:
            new_user = User(
                name=form.name.data,
                phone=form.phone.data,
                address=form.address.data
            )
            session.add(new_user)
            session.commit()
            flash('Контактные данные успешно добавлены!', 'success')
        else:
            user.name = form.name.data
            user.phone = form.phone.data
            user.address = form.address.data
            session.commit()
            flash('Контактные данные успешно изменены!', 'success')

        session.close()  # Закрываем сессию
    return render_template('enter_data.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        session = create_session()
        phone = get_number(form.phone.data)
        if not phone:
            return render_template('register.html',
                                   form=form,
                                   message='Неверный формат номера')
        user = session.query(User).filter(User.phone == phone).first()

        if not user:
            new_user = User(
                name=form.name.data,
                phone=phone,
                address=form.address.data,
                password=form.password.data
            )
            session.add(new_user)
            session.commit()
            login_user(new_user, remember=True)
            session.close()  # Закрываем сессию
            return redirect('/')

        else:
            session.close()  # Закрываем сессию
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
    # Используем joinedload для предварительной загрузки фотографий
    details = session.query(Detail).options(joinedload(Detail.photos)).all()
    session.close()  # Закрываем сессию
    return render_template('admin.html', details=details)


@app.route('/photo/<int:detail_id>', methods=['GET'])
def get_photo(detail_id):
    session = create_session()
    print("catch photo", detail_id)
    try:
        detail = session.query(Detail).filter(Detail.id == detail_id).first()

        if detail and detail.photos:
            image_data = [
                base64.b64encode(photo.photo).decode('utf-8')
                for photo in detail.photos if photo.photo
            ]
            return jsonify(image_data), 200
        return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        session = create_session()

        if form.phone.data.lower() == 'boss':
            if form.password.data == '51974376':
                user = session.query(User).filter(User.phone == form.phone.data.lower()).first()
                if not user:
                    admin = User(
                        name='BOSS',
                        phone='boss',
                        address='СПБ',
                        password='51974376'
                    )
                    session.add(admin)
                    session.commit()
                    login_user(admin, remember=True)
                else:
                    login_user(user, remember=True)
                session.close()  # Закрываем сессию
                return redirect('/admin')
            else:
                session.close()  # Закрываем сессию
                return render_template('login.html',
                                       message="Неверный пароль",
                                       form=form)

        phone = get_number(form.phone.data)
        user = session.query(User).filter(User.phone == phone).first()
        if not user:
            session.close()  # Закрываем сессию
            return render_template('login.html',
                                   message="Пользователь с таким номером не найден",
                                   form=form)
        else:
            if form.password.data == user.password:
                login_user(user, remember=True)
                session.close()  # Закрываем сессию
                return redirect('/')
            else:
                session.close()  # Закрываем сессию
                return render_template('login.html',
                                       message='Неверно введён пароль пользователя',
                                       form=form)

    return render_template('login.html', form=form)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    session = create_session()
    user = session.query(User).get(current_user.id)
    form = RegisterUser(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.address = form.address.data
        user.password = form.password.data
        session.commit()
        session.close()  # Закрываем сессию
        return redirect('/')

    session.close()  # Закрываем сессию
    return render_template('edit_user.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    user = session.get(User, user_id)
    session.close()  # Закрываем сессию
    return user


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found_error(_):
    return make_response(jsonify({'error': "this page doesn`t exist"}))




if __name__ == '__main__':
    # global_init("./db/data.sqlite")
    import locale

    locale.setlocale(locale.LC_ALL, '')  # Устанавливаем локаль по умолчанию

    app.register_error_handler(404, not_found_error)
    app.run(port=8888, host='127.0.0.1')
