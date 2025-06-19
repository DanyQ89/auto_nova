# 🚗 AutoNova - Сайт автозапчастей

Современный веб-сайт для продажи автозапчастей с корзиной, системой уведомлений и администрированием.

## 📋 Оглавление

- [Установка и запуск](#установка-и-запуск)
- [Настройка Flask-Mail](#настройка-flask-mail)
- [Функционал сайта](#функционал-сайта)
- [Структура проекта](#структура-проекта)
- [API эндпоинты](#api-эндпоинты)
- [Устранение проблем](#устранение-проблем)

## 🚀 Установка и запуск

### 1. Клонирование и подготовка

```bash
git clone <repository-url>
cd auto_nova
```

### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте `.env-example` в `.env` и настройте:

```bash
cp .env-example .env
```

Отредактируйте `.env`:
```env
# Обязательные настройки для отправки email
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password

# Контактные данные (опционально)
SERGEY_EMAIL=sedunovandrey2007@gmail.com
SERGEY_PHONE=+7 (XXX) XXX-XX-XX
```

### 5. Запуск приложения

```bash
python main.py
```

Сайт будет доступен по адресу: `http://127.0.0.1:8888`

## 📧 Настройка Flask-Mail

### Пошаговая инструкция для Gmail

#### Шаг 1: Подготовка Gmail аккаунта

1. **Включите двухфакторную аутентификацию:**
   - Перейдите в [Аккаунт Google](https://myaccount.google.com/)
   - Выберите **Безопасность** → **Двухэтапная аутентификация**
   - Следуйте инструкциям для включения

2. **Создайте пароль приложения:**
   - В разделе **Безопасность** найдите **Пароли приложений**
   - Выберите приложение: **Почта**
   - Выберите устройство: **Windows компьютер** (или ваше устройство)
   - Скопируйте сгенерированный 16-символьный пароль

#### Шаг 2: Настройка переменных окружения

**Способ 1: Через файл .env (рекомендуется)**

Создайте файл `.env` в корне проекта:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
```

**Способ 2: Через командную строку**

Windows PowerShell:
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="abcd efgh ijkl mnop"
```

Windows CMD:
```cmd
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=abcd efgh ijkl mnop
```

Linux/Mac:
```bash
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="abcd efgh ijkl mnop"
```

#### Шаг 3: Проверка настройки

1. Запустите сайт: `python main.py`
2. Добавьте товар в корзину
3. Оформите заказ
4. В консоли должно появиться: `✅ Email успешно отправлен на sedunovandrey2007@gmail.com`

### Настройка для других почтовых провайдеров

#### Yandex Mail
```python
# В main.py измените настройки:
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
```

#### Mail.ru
```python
# В main.py измените настройки:
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
```

#### Outlook/Hotmail
```python
# В main.py измените настройки:
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
```

## 🎯 Функционал сайта

### Для покупателей:
- 🔍 Каталог автозапчастей по маркам
- 🛒 Корзина с возможностью добавления/удаления товаров
- 📸 Просмотр фотографий деталей с навигацией
- 💰 Отображение цен и скидок
- 📧 Автоматическое уведомление о заказе
- 📱 Контакты менеджера (Telegram)

### Для администратора:
- 👤 Административная панель (логин: `boss`, пароль: `51974376`)
- ➕ Добавление новых деталей
- ✏️ Редактирование существующих деталей
- 📸 Управление фотографиями
- 🗑️ Удаление деталей

### Система уведомлений:
- 📧 HTML-письма с информацией о заказе
- 🎉 Модальные окна благодарности
- 📱 Прямые ссылки на Telegram менеджера
- 🔄 Автоматическое удаление заказанных товаров

## 📁 Структура проекта

```
auto_nova/
├── data/                   # Модели базы данных
│   ├── database.py        # Настройка SQLAlchemy
│   └── users.py          # Модели User, Detail, Basket, Photo
├── forms/                 # WTF формы
│   └── user.py           # Формы регистрации и входа
├── static/               # Статические файлы
│   ├── css/             # Стили
│   ├── js/              # JavaScript
│   └── img/             # Изображения
├── templates/            # HTML шаблоны
│   ├── base.html        # Базовый шаблон
│   ├── basket.html      # Корзина
│   ├── admin.html       # Админ панель
│   └── ...
├── utils/               # Утилиты
│   ├── config.py        # Конфигурация
│   └── help_functions.py # Вспомогательные функции
├── db/                  # База данных
│   └── data.sqlite     # SQLite файл
├── main.py             # Главный файл приложения
├── requirements.txt    # Зависимости
├── .env-example       # Пример настроек
└── README.md          # Документация
```

## 🔌 API эндпоинты

### Основные страницы:
- `GET /` - Главная страница
- `GET /basket` - Корзина
- `GET /admin` - Админ панель
- `GET /<car_name>` - Каталог по марке авто

### API для корзины:
- `POST /add_to_basket/<detail_id>` - Добавить в корзину
- `POST /remove_from_basket/<detail_id>` - Удалить из корзины
- `POST /process_order` - Оформить заказ

### API для фотографий:
- `GET /photo/<detail_id>` - Получить фото детали
- `POST /add_photo` - Добавить фото
- `PUT /edit_photo/<photo_id>` - Редактировать фото
- `DELETE /delete_photo/<photo_id>` - Удалить фото

### Пользователи:
- `GET/POST /register` - Регистрация
- `GET/POST /login` - Вход
- `GET /logout` - Выход

## 🔧 Устранение проблем

### Проблемы с email

**❌ Ошибка "Authentication failed"**
```
Решение:
1. Убедитесь, что включена двухфакторная аутентификация
2. Используйте пароль приложения, а не обычный пароль
3. Проверьте правильность email в переменных окружения
```

**❌ Ошибка "Connection refused"**
```
Решение:
1. Проверьте интернет-соединение
2. Убедитесь, что порт 587 не заблокирован фаерволом
3. Попробуйте другой SMTP сервер
```

**❌ Письма не приходят**
```
Решение:
1. Проверьте папку "Спам" в почте получателя
2. Убедитесь, что email получателя правильный в config.py
3. Проверьте логи в консоли приложения
```

### Проблемы с базой данных

**❌ Ошибка "No such table"**
```bash
# Удалите базу и запустите заново
rm db/data.sqlite
python main.py
```

**❌ Ошибки SQLAlchemy**
```bash
# Обновите SQLAlchemy
pip install --upgrade SQLAlchemy
```

### Проблемы с фотографиями

**❌ Фото не отображаются**
```
Решение:
1. Убедитесь, что фото загружены в правильном формате (JPEG, PNG)
2. Проверьте размер файлов (не более 10MB)
3. Откройте консоль браузера для проверки ошибок JavaScript
```

**❌ Модальное окно не открывается**
```
Решение:
1. Проверьте консоль браузера на ошибки JavaScript
2. Убедитесь, что файл cart.js загружается
3. Проверьте ID элементов в HTML
```

## 👥 Контакты

- **Разработчик:** AutoNova Team
- **Email:** support@autonova.ru
- **Telegram:** @autonova_spb

## 📄 Лицензия

Этот проект предназначен для коммерческого использования AutoNova.

---

*Документация обновлена: 2024* 