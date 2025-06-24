from flask import Flask, render_template, make_response, jsonify, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_mail import Mail, Message
from sqlalchemy.orm import joinedload
import os

from utils.config import (
    secret_key, SERGEY_EMAIL, SERGEY_PHONE_FORMATTED, 
    ORDER_SUCCESS_MESSAGE, EMAIL_SETTINGS, CONTACT_INFO
)
from utils.help_functions import get_number
import string
import random
from forms.user import RegisterUser, LoginUser, ChangePasswordForm
from data.database import create_session, global_init
from data.users import User, Detail, Basket, basket_details, Photo
import base64


global_init()


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# Конфигурация для отправки email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')

mail = Mail(app)
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
        return jsonify({'status': 'error', 'message': 'Фото не найдено'}), 404

    if 'file' not in request.files:
        session.close()
        return jsonify({'status': 'error', 'message': 'Нет файла для загрузки'}), 400

    file = request.files.get('file')
    if file and file.filename:
        try:
            photo.photo = file.read()
            session.commit()
            session.close()
            return jsonify({'status': 'success', 'message': 'Фото успешно обновлено!'}), 200
        except Exception as e:
            session.rollback()
            session.close()
            return jsonify({'status': 'error', 'message': f'Ошибка при обновлении фото: {str(e)}'}), 500
    else:
        session.close()
        return jsonify({'status': 'error', 'message': 'Файл отсутствует или пустой'}), 400


@app.route('/delete_photo/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    session = create_session()
    photo = session.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        session.close()
        return jsonify({'status': 'error', 'message': 'Фото не найдено'}), 404

    # Проверяем, сколько фотографий у детали
    detail_photos = session.query(Photo).filter(Photo.detail_id == photo.detail_id).all()
    
    if len(detail_photos) <= 1:
        session.close()
        return jsonify({'status': 'error', 'message': 'Нельзя удалить последнюю фотографию детали'}), 400

    session.delete(photo)
    session.commit()
    session.close()
    return jsonify({'status': 'success', 'message': 'Фото успешно удалено!'}), 200


@app.route('/add_photo', methods=['POST'])
def add_photo():
    print("catch add photo", request.form.get('detail_id'))
    detail_id = request.form.get('detail_id')
    
    if not detail_id:
        return jsonify({'status': 'error', 'message': 'ID детали не указан'}), 400
        
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Нет файла для загрузки'}), 400

    file = request.files.get('file')
    session = create_session()
    
    try:
        detail = session.query(Detail).filter(Detail.id == detail_id).first()

        if not detail:
            session.close()
            return jsonify({'status': 'error', 'message': 'Деталь не найдена'}), 404

        if file and file.filename:
            new_photo = Photo(detail_id=detail.id, photo=file.read())
            session.add(new_photo)
            session.commit()
            session.close()
            return jsonify({'status': 'success', 'message': 'Фото успешно добавлено!'}), 200
        else:
            session.close()
            return jsonify({'status': 'error', 'message': 'Файл отсутствует или пустой'}), 400
            
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({'status': 'error', 'message': f'Ошибка при добавлении фото: {str(e)}'}), 500


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

        # Обработка загрузки множественных файлов
        photos = request.files.getlist('photos')
        for photo in photos:
            if photo and photo.filename:  # Проверяем, что файл существует и имеет имя
                new_photo = Photo(detail=new_detail, photo=photo.read())
                session.add(new_photo)

        session.add(new_detail)
        session.commit()
        session.close()
        return redirect('/admin')
    else:
        # Обновление существующей детали
        detail_id = request.form['id']
        detail = session.query(Detail).filter(Detail.id == detail_id).first()
        
        if detail:
            detail.sklad = request.form['sklad']
            detail.ID_detail = request.form['ID_detail']
            detail.brand = request.form['brand']
            detail.model_and_year = request.form['model_and_year']
            detail.name = request.form['name']
            detail.price = request.form['price']
            detail.price_w_discount = request.form.get('price_w_discount', '')
            detail.comment = request.form.get('comment', '')
            detail.orig_number = request.form.get('orig_number', '')
            detail.condition = request.form.get('condition', '')
            detail.percent = request.form.get('percent', 0)
            detail.color = request.form.get('color', '')
            
            # Обработка загрузки множественных файлов для редактирования
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo and photo.filename:  # Проверяем, что файл существует и имеет имя
                    new_photo = Photo(detail=detail, photo=photo.read())
                    session.add(new_photo)
            
            session.commit()
            session.close()
            return redirect('/admin')
        else:
            session.close()
            return jsonify({'error': 'Деталь не найдена'}), 404


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
            # Используем joinedload для предварительной загрузки фотографий
            details = session.query(Detail).options(joinedload(Detail.photos)).filter(
                Detail.id.in_([d.id for d in basket.details])
            ).all()
            
            for detail in details:
                try:
                    price = float(detail.price) if detail.price else 0
                    price_w_discount = float(detail.price_w_discount) if detail.price_w_discount else price
                    total_price += price
                    total_card_price += price_w_discount
                except (ValueError, TypeError):
                    pass

        session.close()  # Закрываем сессию
    return render_template("basket.html", 
                          details=details, 
                          total_price=total_price, 
                          total_card_price=total_card_price,
                          order_success_message=ORDER_SUCCESS_MESSAGE,  # Изменено с order_success_msg на order_success_message
                          contact_info=CONTACT_INFO)


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
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data
            )
            session.add(new_user)
            session.commit()
            flash('Контактные данные успешно добавлены!', 'success')
        else:
            user.name = form.name.data
            user.email = form.email.data
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
        # Проверяем уникальность телефона и email
        existing_phone = session.query(User).filter(User.phone == phone).first()
        existing_email = session.query(User).filter(User.email == form.email.data).first()

        if existing_email:
            session.close()
            return render_template('register.html',
                                   form=form,
                                   message='Пользователь с таким email уже зарегистрирован')

        if not existing_phone:
            new_user = User(
                name=form.name.data,
                email=form.email.data,
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
            # Возвращаем список словарей с ID и данными фото
            photos_data = [
                {
                    'id': photo.id,
                    'data': base64.b64encode(photo.photo).decode('utf-8')
                }
                for photo in detail.photos if photo.photo
            ]
            return jsonify(photos_data), 200
        return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route('/delete_detail/<int:detail_id>', methods=['DELETE'])
def delete_detail(detail_id):
    if not current_user.__dict__ or current_user.phone not in ['boss']:
        return jsonify({
            "error": 777,
            "message": "you don`t have the rights for this action"
        }), 403

    session = create_session()
    try:
        detail = session.query(Detail).filter(Detail.id == detail_id).first()
        
        if not detail:
            return jsonify({'error': 'Деталь не найдена'}), 404
        
        # Удаляем связи из всех корзин
        session.execute(
            basket_details.delete().where(basket_details.c.detail_id == detail_id)
        )
        
        # Удаляем связанные фотографии
        photos_to_delete = session.query(Photo).filter(Photo.detail_id == detail_id).all()
        for photo in photos_to_delete:
            session.delete(photo)
        
        # Удаляем саму деталь
        session.delete(detail)
        session.commit()
        
        return jsonify({'success': 'Деталь успешно удалена'}), 200
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка при удалении детали: {e}")
        return jsonify({'error': 'Произошла ошибка при удалении детали'}), 500
    
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
                        email='admin@autonova.ru',
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


@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    phone = request.json.get('phone')
    
    if not phone:
        return jsonify({'error': 'Номер телефона не указан'}), 400
    
    session = create_session()
    
    try:
        # Проверяем формат номера
        formatted_phone = get_number(phone)
        if not formatted_phone:
            return jsonify({'error': 'Неверный формат номера телефона'}), 400
        
        # Ищем пользователя
        user = session.query(User).filter(User.phone == formatted_phone).first()
        
        if not user:
            return jsonify({'error': 'Пользователь с таким номером не найден'}), 404
        
        # Проверяем наличие email у пользователя
        if not user.email:
            return jsonify({'error': 'У пользователя не указан email адрес. Обратитесь к менеджеру.'}), 400
        
        # Генерируем новый пароль
        new_password = generate_password()
        
        # Обновляем пароль в базе
        user.password = new_password
        session.commit()
        
        # Отправляем пароль на email
        if send_password_reset_email(user, new_password):
            return jsonify({'success': f'Новый пароль отправлен на ваш email: {user.email}'}), 200
        else:
            return jsonify({'success': 'Пароль сброшен успешно, но не удалось отправить email. Обратитесь к менеджеру.'}), 200
            
    except Exception as e:
        session.rollback()
        print(f"Ошибка при восстановлении пароля: {e}")
        return jsonify({'error': 'Произошла ошибка при восстановлении пароля'}), 500
    
    finally:
        session.close()


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    session = create_session()
    user = session.get(User, current_user.id)  # Используем новый метод Session.get()
    form = RegisterUser(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.address = form.address.data
        user.password = form.password.data
        session.commit()
        session.close()  # Закрываем сессию
        return redirect('/')

    session.close()  # Закрываем сессию
    return render_template('edit_user.html', form=form)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        session = create_session()
        
        try:
            user = session.get(User, current_user.id)
            
            # Проверяем текущий пароль
            if user.password != form.current_password.data:
                flash('Неверный текущий пароль', 'error')
                session.close()
                return render_template('change_password.html', form=form)
            
            # Проверяем требования к новому паролю
            new_password = form.new_password.data
            
            # Дополнительная валидация пароля
            if len(new_password) < 6:
                flash('Пароль должен содержать минимум 6 символов', 'error')
                session.close()
                return render_template('change_password.html', form=form)
            
            # Проверяем наличие латинских букв и цифр
            has_letter = any(c.isalpha() for c in new_password)
            has_digit = any(c.isdigit() for c in new_password)
            
            if not (has_letter and has_digit):
                flash('Пароль должен содержать как минимум одну букву и одну цифру', 'error')
                session.close()
                return render_template('change_password.html', form=form)
            
            # Обновляем пароль
            user.password = new_password
            session.commit()
            flash('Пароль успешно изменен!', 'success')
            
            session.close()
            return redirect('/edit_profile')
            
        except Exception as e:
            session.rollback()
            print(f"Ошибка при смене пароля: {e}")
            flash('Произошла ошибка при смене пароля', 'error')
            session.close()
    
    return render_template('change_password.html', form=form)


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


@app.route('/process_order', methods=['POST'])
@login_required
def process_order():
    session = create_session()
    
    try:
        # Получаем корзину пользователя
        user_basket = session.query(Basket).filter_by(user_id=current_user.id).first()
        
        if not user_basket or not user_basket.details:
            return jsonify({'error': 'Корзина пуста'}), 400
        
        # Получаем данные пользователя
        user = session.query(User).get(current_user.id)
        
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        # Проверяем наличие каждого товара в базе
        available_details = []
        unavailable_details = []
        
        for detail in user_basket.details:
            # Проверяем, существует ли деталь в базе
            existing_detail = session.query(Detail).filter(Detail.id == detail.id).first()
            if existing_detail:
                available_details.append(detail)
            else:
                unavailable_details.append(detail)
        
        # Если есть недоступные товары, удаляем их из корзины
        if unavailable_details:
            for unavailable_detail in unavailable_details:
                # Удаляем связь из корзины
                session.execute(
                    basket_details.delete().where(
                        (basket_details.c.basket_id == user_basket.id) &
                        (basket_details.c.detail_id == unavailable_detail.id)
                    )
                )
            session.commit()
            
            # Если корзина стала пустой
            if not available_details:
                session.close()
                return jsonify({
                    'error': 'removed_items',
                    'message': 'Все товары из вашей корзины были куплены другими покупателями. Корзина очищена.',
                    'removed_count': len(unavailable_details)
                }), 400
            
            # Если часть товаров недоступна
            session.close()
            return jsonify({
                'error': 'removed_items',
                'message': f'Некоторые товары ({len(unavailable_details)} шт.) были куплены другими покупателями и удалены из корзины. Попробуйте оформить заказ снова.',
                'removed_count': len(unavailable_details),
                'remaining_count': len(available_details)
            }), 400
        
        # Формируем информацию о заказе только из доступных товаров
        order_details = []
        total_price = 0
        total_card_price = 0
        
        for detail in available_details:
            detail_info = {
                'article': detail.ID_detail,
                'brand': detail.brand,
                'model': detail.model_and_year,
                'name': detail.name,
                'price': detail.price,
                'price_w_discount': detail.price_w_discount,
                'condition': detail.condition,
                'color': detail.color,
                'comment': detail.comment,
                'orig_number': detail.orig_number
            }
            order_details.append(detail_info)
            
            try:
                total_price += float(detail.price) if detail.price else 0
                total_card_price += float(detail.price_w_discount) if detail.price_w_discount else float(detail.price) if detail.price else 0
            except ValueError:
                pass
        
        # Получаем ID деталей для удаления
        detail_ids = [detail.id for detail in available_details]
        
        # Отправляем email Сергею перед удалением (чтобы данные были доступны)
        send_order_email(user, order_details, total_price, total_card_price)
        
        # Удаляем детали из ВСЕХ корзин (не только пользователя)
        if detail_ids:
            # Удаляем связи basket_details для всех корзин
            session.execute(
                basket_details.delete().where(basket_details.c.detail_id.in_(detail_ids))
            )
            
            # Удаляем связанные фотографии
            photos_to_delete = session.query(Photo).filter(Photo.detail_id.in_(detail_ids)).all()
            for photo in photos_to_delete:
                session.delete(photo)
            
            # Удаляем сами детали
            details_to_delete = session.query(Detail).filter(Detail.id.in_(detail_ids)).all()
            for detail in details_to_delete:
                session.delete(detail)
        
        session.commit()
        return jsonify({'success': 'Заказ успешно оформлен'}), 200
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обработке заказа: {e}")
        return jsonify({'error': 'Произошла ошибка при обработке заказа'}), 500
    
    finally:
        session.close()


def generate_password(length=9):
    """Генерирует случайный пароль из латинских букв и цифр"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_password_reset_email(user, new_password):
    """Отправляет новый пароль на email пользователя"""
    try:
        # Проверяем наличие настроек email
        if not app.config.get('MAIL_USERNAME') or app.config['MAIL_USERNAME'] == 'your-email@gmail.com':
            print("⚠️ Email не настроен - установите переменные окружения MAIL_USERNAME и MAIL_PASSWORD")
            return False
            
        # Формируем HTML содержимое письма
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .password-box {{ background: #f8f9fa; border: 2px solid #007bff; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }}
                .password {{ font-size: 24px; font-weight: bold; color: #007bff; letter-spacing: 3px; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #6c757d; font-style: italic; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🚗 AutoNova - Восстановление пароля</h2>
            </div>
            
            <div class="content">
                <p>Здравствуйте, <strong>{user.name}</strong>!</p>
                
                <p>Наш сервис AutoNova высылает вам новый пароль для входа в личный кабинет:</p>
                
                <div class="password-box">
                    <div class="password">{new_password}</div>
                </div>
                
                <div class="warning">
                    <p><strong>⚠️ Важно:</strong></p>
                    <ul>
                        <li>Сохраните этот пароль в надежном месте</li>
                        <li>Рекомендуем сменить пароль после входа в личный кабинет</li>
                        <li>Не передавайте пароль третьим лицам</li>
                    </ul>
                </div>
                
                <p>Теперь вы можете войти в систему, используя ваш номер телефона <strong>{user.phone}</strong> и новый пароль.</p>
                
                <div class="footer">
                    <p>Письмо отправлено автоматически с сайта AutoNova</p>
                    <p>Если вы не запрашивали восстановление пароля, проигнорируйте это письмо</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Создаем и отправляем письмо с Flask-Mail
        with app.app_context():
            msg = Message()
            msg.subject = "🚗 AutoNova: Восстановление пароля"
            msg.recipients = [user.email]  # Отправляем на email пользователя
            msg.html = html_content
            msg.sender = app.config['MAIL_DEFAULT_SENDER']
            
            mail.send(msg)
            print(f"✅ Пароль отправлен на {user.email}")
            return True
        
    except Exception as e:
        print(f"❌ Ошибка при отправке пароля: {e}")
        return False


def send_order_email(user, order_details, total_price, total_card_price):
    """Отправляет email с информацией о заказе"""
    try:
        # Проверяем наличие настроек email
        if not app.config.get('MAIL_USERNAME') or app.config['MAIL_USERNAME'] == 'your-email@gmail.com':
            print("⚠️ Email не настроен - установите переменные окружения MAIL_USERNAME и MAIL_PASSWORD")
            return False
            
        # Формируем HTML содержимое письма
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .customer-info {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .order-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .order-table th {{ background: #e9ecef; padding: 12px; text-align: left; border: 1px solid #dee2e6; }}
                .order-table td {{ padding: 12px; border: 1px solid #dee2e6; }}
                .totals {{ background: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #6c757d; font-style: italic; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🚗 AutoNova - Новый заказ</h2>
            </div>
            
            <div class="content">
                <div class="customer-info">
                    <h3>👤 Информация о клиенте:</h3>
                    <p><strong>Имя:</strong> {user.name or 'Не указано'}</p>
                    <p><strong>Email:</strong> {user.email or 'Не указан'}</p>
                    <p><strong>Телефон:</strong> {user.phone or 'Не указан'}</p>
                    <p><strong>Адрес:</strong> {user.address or 'Не указан'}</p>
                </div>
                
                <h3>🛍️ Заказанные детали:</h3>
                <table class="order-table">
                    <tr>
                        <th>Артикул</th>
                        <th>Марка</th>
                        <th>Модель</th>
                        <th>Наименование</th>
                        <th>Цена</th>
                        <th>Цена со скидкой</th>
                        <th>Состояние</th>
                        <th>Оригинальный номер</th>
                        <th>Комментарий</th>
                    </tr>
        """
        
        for detail in order_details:
            html_content += f"""
                    <tr>
                        <td><strong>{detail['article'] or 'Не указан'}</strong></td>
                        <td>{detail['brand'] or 'Не указана'}</td>
                        <td>{detail['model'] or 'Не указана'}</td>
                        <td>{detail['name'] or 'Не указано'}</td>
                        <td>{detail['price'] or 'Не указана'} ₽</td>
                        <td><strong>{detail['price_w_discount'] or detail['price'] or 'Не указана'} ₽</strong></td>
                        <td>{detail['condition'] or 'Не указано'}</td>
                        <td>{detail['orig_number'] or 'Не указан'}</td>
                        <td>{detail['comment'] or 'Без комментария'}</td>
                    </tr>
            """
        
        html_content += f"""
                </table>
                
                <div class="totals">
                    <h3>💰 Итого:</h3>
                    <p><strong>Общая сумма:</strong> {total_price:.2f} ₽</p>
                    <p><strong>Итоговая сумма к оплате:</strong> <span style="color: #28a745; font-size: 18px;">{total_card_price:.2f} ₽</span></p>
                </div>
                
                <div class="footer">
                    <p>Письмо отправлено автоматически с сайта AutoNova</p>
                    <p>📧 Email: {user.email} | 📞 Телефон: {user.phone} | 📍 Адрес: {user.address}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Создаем и отправляем письмо с Flask-Mail 0.10.0
        with app.app_context():
            msg = Message()
            msg.subject = f"🚗 AutoNova: Заказ от {user.name} ({user.phone})"
            msg.recipients = [SERGEY_EMAIL]
            msg.html = html_content
            msg.sender = app.config['MAIL_DEFAULT_SENDER']
            
            mail.send(msg)
            print(f"✅ Email успешно отправлен на {SERGEY_EMAIL}")
            return True
        
    except Exception as e:
        print(f"❌ Ошибка при отправке email: {e}")
        return False


@app.errorhandler(404)
def not_found_error(_):
    return make_response(jsonify({'error': "this page doesn`t exist"}))


if __name__ == '__main__':
    # global_init("./db/data.sqlite")
    import locale

    locale.setlocale(locale.LC_ALL, '')  # Устанавливаем локаль по умолчанию

    app.register_error_handler(404, not_found_error)
    app.run(port=8888, host='127.0.0.1')
