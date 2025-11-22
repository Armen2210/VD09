from flask_wtf import FlaskForm  # Базовый класс для всех форм Flask-WTF
from wtforms import StringField, PasswordField, SubmitField, BooleanField  # Поля формы (текст, пароль, кнопка и др.)
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError  # Валидаторы для проверки данных

# Импортируем модель User, чтобы проверять существование пользователя в БД.
# models.py использует db из __init__.py, а forms.py получает User из models.py.
from app.models import User


# Форма регистрации — отображается в register.html и обрабатывается во view-функции register() в routes.py
class RegistrationForm(FlaskForm):
    # Поле ввода имени пользователя
    # DataRequired — поле не может быть пустым
    # Length — ограничение длины (мин. 2 символа, макс. 20)
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    # Поле ввода пароля
    password = PasswordField('Password', validators=[DataRequired()])

    # Поле повторного ввода пароля
    # EqualTo — проверяет, совпадает ли со значением поля "password"
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )

    # Кнопка подтверждения формы
    submit = SubmitField('Регистрация')


    # Дополнительный метод-валидатор.
    # Flask-WTF автоматически вызывает методы вида validate_<имя_поля>().
    # Здесь мы проверяем, не существует ли пользователь с таким же именем.
    def validate_username(self, username):
        # Ищем пользователя в базе данных по имени
        user = User.query.filter_by(username=username.data).first()

        # Если найден — выбрасываем исключение ValidationError,
        # и форма покажет сообщение под соответствующим полем.
        if user:
            raise ValidationError('Такое имя уже существует.')


# Форма входа — отображается в login.html и обрабатывается во view-функции login() в routes.py
class LoginForm(FlaskForm):
    # Поле имени пользователя
    username = StringField('Username', validators=[DataRequired()])

    # Поле пароля
    password = PasswordField('Password', validators=[DataRequired()])

    # Кнопка подтверждения
    submit = SubmitField('Вход')
