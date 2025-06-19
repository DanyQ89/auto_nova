import os
import dotenv
dotenv.load_dotenv()

# Секретный ключ для Flask
secret_key = 'your-secret-key-here'

# ==========================================
# КОНФИГУРАЦИЯ КОНТАКТНЫХ ДАННЫХ СЕРГЕЯ
# ==========================================

# Основная информация о менеджере
SERGEY_NAME = 'Сергей Михайлович'
SERGEY_POSITION = 'Менеджер по продажам'
SERGEY_COMPANY = 'AutoNova'

# Контактные данные для клиентов
SERGEY_EMAIL = os.getenv('SERGEY_EMAIL', 'sedunovandrey2007@gmail.com')
SERGEY_PHONE = os.getenv('SERGEY_PHONE', '+7 (XXX) XXX-XX-XX')
SERGEY_PHONE_FORMATTED = SERGEY_PHONE.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
SERGEY_WHATSAPP = '+79215551234'  # Номер для WhatsApp (без пробелов и скобок)
SERGEY_TELEGRAM = '@sergey_autonova'  # Telegram username

# Рабочие часы
SERGEY_WORK_HOURS = 'Пн-Пт: 9:00-18:00, Сб: 10:00-16:00'
SERGEY_TIMEZONE = 'МСК (UTC+3)'

# Дополнительная информация для клиентов
SERGEY_RESPONSE_TIME = 'в течение 30 минут в рабочее время'
SERGEY_LANGUAGES = ['Русский', 'English']

# Контактная информация для модального окна
CONTACT_INFO = {
    'name': 'Сергей',
    'position': 'Менеджер по продажам',
    'company': 'AutoNova',
    'phone': SERGEY_PHONE,
    'email': SERGEY_EMAIL,
    'whatsapp': SERGEY_PHONE_FORMATTED,
    'telegram': 'autonova_spb',  # Ник Сергея в Telegram
    'work_hours': '9:00 - 21:00',
    'response_time': '15 минут',
}

# Сообщение после успешного оформления заказа
ORDER_SUCCESS_MESSAGE = {
    'title': 'Спасибо за заказ!',
    'subtitle': 'Мы свяжемся с вами в ближайшее время',
    'details': f"""
        Ваш заказ успешно оформлен и передан менеджеру.
        Среднее время ответа: {CONTACT_INFO['response_time']}.
        Режим работы: {CONTACT_INFO['work_hours']}.
    """,
    'manager_info': f"""
        {CONTACT_INFO['name']}
        {CONTACT_INFO['position']} {CONTACT_INFO['company']}
    """
}

# Настройки для email уведомлений
EMAIL_SETTINGS = {
    'subject_prefix': '🚗 AutoNova: Новый заказ от',
    'recipient': SERGEY_EMAIL,
}

# Сообщения для уведомлений
NOTIFICATION_MESSAGES = {
    'order_processing': 'Ваш заказ принят в обработку',
    'manager_contact': f'С вами свяжется {SERGEY_NAME}',
    'contact_time': f'Обычно отвечаем {SERGEY_RESPONSE_TIME}',
    'thank_you': 'Благодарим за выбор AutoNova!'
}
