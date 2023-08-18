from flask import Flask, render_template, request, redirect, url_for
from flask import flash, get_flashed_messages
import json
from hexlet_web_test_1.users_functions import load_users, validate_user


app = Flask(__name__)
app.secret_key = "lolkek"

@app.route('/')
def hello_world():
    url_for('users')
    return render_template(
        'index.html'
    )


@app.route('/users/')
def users():
    messages = get_flashed_messages()
    users_list = load_users('users.json')
    url_for('users_new')
    for user in users_list:
        url_for('user_page', id=user['id'])
    return render_template(
        'users/index.html',
        users=users_list,
        messages=messages
    )


@app.route('/users/create-new')
def users_new():
    user = {'name': '',
            'email': '',
            }
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors
    )


@app.post('/users/')
def users_post():
    user = request.form.to_dict()
    user['kek'] = user.get('kek', '0')
    errors = validate_user(user)

    if errors != {}:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors,
        ), 422

    users_list = load_users('users.json')
    user['id'] = str(len(users_list) + 1)
    users_list.append(user)

    with open('users.json', 'w') as file:
        json.dump(users_list, file, indent=1)

    flash('User successfully created! You are awesome!', 'success')

    return redirect(url_for('users'), code=302)


@app.route('/users/<id>')
def user_page(id):
    users_list = load_users('users.json')
    selected_users = [user for user in users_list if user['id'] == id]
    return render_template(
        'users/user-page.html',
        user=selected_users[0]
    )
