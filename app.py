from dotenv import load_dotenv
import os
import psycopg2
from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
from user_repo import UserRepository
from validator import validate

# Загружаем переменные окружения из .env файла
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


conn = psycopg2.connect(app.config['DATABASE_URL'])
repo = UserRepository(conn)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/users/')
def users_get():
    messages = get_flashed_messages(with_categories=True)
    term = request.args.get('term', '')
    if term:
        users = repo.get_by_term(term)
    else:
        users = repo.get_content()
    return render_template(
        'users/index.html',
        users=users,
        search=term,
        messages=messages
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'users/new.html',
            user=user_data,
            errors=errors,
        )
    repo.save(user_data)

    flash('Пользователь успешно добавлен', 'success')
    return redirect(url_for('users_get'), code=302)


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<id>/edit')
def users_edit(id):
    user = repo.find(id)
    errors = {}

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<id>/patch', methods=['POST'])
def users_patch(id):
    user = repo.find(id)
    data = request.form.to_dict()

    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
        ), 422
    data['id'] = user['id']
    repo.save(data)
    flash('Пользователь успешно обновлен', 'success')
    return redirect(url_for('users_get'))


@app.route('/users/<id>/delete', methods=['POST'])
def users_delete(id):
    repo.destroy(id)
    flash('Пользователь удален', 'success')
    return redirect(url_for('users_get'))


@app.route('/users/<id>')
def users_show(id):
    user = repo.find(id)
    return render_template(
        'users/show.html',
        user=user,
    )
