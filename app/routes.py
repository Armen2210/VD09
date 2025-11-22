from flask import render_template, redirect, url_for, flash  # Импортируем функции Flask:
# render_template — для рендеринга HTML-шаблонов
# redirect — для перенаправления пользователя на другой URL
# url_for — для генерации URL по имени функции
# flash — для вывода уведомлений (сообщений) пользователю

from app import app, db, bcrypt  # Импортируем:
# app — экземпляр Flask-приложения
# db — объект SQLAlchemy для работы с БД
# bcrypt — объект для хэширования паролей (создан в __init__.py)

from app.forms import RegistrationForm, LoginForm  # Импортируем формы регистрации и логина из forms.py

from app.models import User  # Импортируем модель User для взаимодействия с таблицей пользователей

from flask_login import login_user, current_user, logout_user, login_required
# login_user — авторизует пользователя (создаёт сессию)
# current_user — объект текущего авторизванного пользователя
# logout_user — выход из аккаунта (очистка сессии)
# login_required — декоратор, ограничивающий доступ к маршруту только авторизованным пользователям


# ------------------------------
# Главная страница игры
# ------------------------------
@app.route('/')  # Маршрут главной страницы — URL "/"
@login_required   # Декоратор. Без авторизации пользователь не попадёт на эту страницу
def index():
    # Функция рендерит шаблон index.html
    # Шаблон использует current_user для отображения количества кликов
    return render_template('index.html')


# ------------------------------
# Регистрация нового пользователя
# ------------------------------
@app.route('/register', methods=['GET', 'POST'])  # Этот маршрут принимает GET и POST запросы
def register():
    # Если пользователь уже авторизован — нет смысла регистрировать нового
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Перенаправляем на главную страницу

    form = RegistrationForm()  # Создаём экземпляр формы регистрации

    # validate_on_submit() выполняет:
    # - проверку, что метод POST
    # - валидацию всех полей
    # - выполнение дополнительных методов валидации, например validate_username()
    if form.validate_on_submit():
        # Хэшируем введённый пароль (bcrypt вернёт байты, поэтому .decode('utf-8'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Создаём нового пользователя
        user = User(username=form.username.data, password=hashed_password)

        # Добавляем пользователя в базу
        db.session.add(user)
        db.session.commit()

        # Показываем всплывающее сообщение
        flash('Регистрация прошла успешно!', 'success')

        # После регистрации перенаправляем на страницу входа
        return redirect(url_for('login'))

    # Если GET запрос или форма не прошла валидацию — показываем HTML
    return render_template('register.html', form=form)


# ------------------------------
# Авторизация пользователя
# ------------------------------
@app.route('/login', methods=['GET', 'POST'])  # Маршрут принимает GET и POST
def login():
    # Если пользователь уже авторизован — отправляем на главную
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()  # Экземпляр формы входа

    if form.validate_on_submit():  # Проверка POST + валидация
        # Получаем пользователя по имени (может вернуть None, если такого нет)
        user = User.query.filter_by(username=form.username.data).first()

        # Проверяем:
        # - существует ли пользователь
        # - совпадает ли пароль (bcrypt сверяет хэш)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Авторизуем пользователя (создаем сессию)
            login_user(user)

            # Перенаправление на главную страницу
            return redirect(url_for('index'))
        else:
            # Если логин или пароль неправильный
            flash('Неверное имя пользователя или пароль', 'danger')

    # Если GET запрос или форма не прошла валидацию — показываем HTML
    return render_template('login.html', form=form)


# ------------------------------
# Выход из аккаунта
# ------------------------------
@app.route('/logout')  # Маршрут выхода
def logout():
    logout_user()  # Удаляем сессию пользователя
    return redirect(url_for('login'))  # Отправляем на страницу логина


# ------------------------------
# Кнопка клика (главная игра)
# ------------------------------
@app.route('/click')
@login_required  # Разрешено только авторизованным
def click():
    # Увеличиваем количество кликов у текущего пользователя
    current_user.clicks += 1

    # Сохраняем обновление в базе данных
    db.session.commit()

    # Возвращаем пользователя на главную страницу с обновлённым счётчиком
    return redirect(url_for('index'))
