from app import db  # Импортируем объект базы данных db, созданный в app/__init__.py
from app import login_manager  # Импортируем LoginManager, также созданный в app/__init__.py
from flask_login import UserMixin  # Миксин, добавляющий стандартные методы для работы с пользователем (Flask-Login)


# Описание модели пользователя.
# Класс User представляет таблицу в базе данных (SQLAlchemy создаст таблицу users по умолчанию).
# UserMixin добавляет свойства и методы, необходимые Flask-Login (is_authenticated, get_id и т.д.).
class User(db.Model, UserMixin):
    # Первичный ключ (идентификатор пользователя, уникальное целое число)
    id = db.Column(db.Integer, primary_key=True)

    # Имя пользователя (строка, максимум 100 символов)
    # unique=True — имя должно быть уникальным
    # nullable=False — поле обязательно для заполнения
    username = db.Column(db.String(100), unique=True, nullable=False)

    # Пароль пользователя (строка, максимум 200 символов)
    # Здесь хранится уже хэшированный пароль, а не "сырой" пароль.
    password = db.Column(db.String(200), nullable=False)

    # Количество кликов в игре «Кликер»
    # default=0 — при создании нового пользователя значение по умолчанию 0
    clicks = db.Column(db.Integer, default=0)

    # Служебный метод, который возвращает строковое представление объекта User.
    # Полезно для отладки и отображения в консоли.
    def __repr__(self):
        return f"User('{self.username}', '{self.clicks}')"


# Декоратор Flask-Login.
# Регистрирует функцию load_user как "загрузчик пользователя" по его id.
# Flask-Login будет вызывать эту функцию, когда нужно восстановить пользователя из сессии.
@login_manager.user_loader  # load user from database
def load_user(user_id):
    # user_id приходит как строка, поэтому преобразуем к int.
    # User.query.get(...) обращается к базе данных через модель User (эта модель описана в этом же файле).
    return User.query.get(int(user_id))
