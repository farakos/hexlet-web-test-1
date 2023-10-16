from flask import (
        Flask,
        render_template,
        request,
        redirect,
        url_for,
        flash,
        get_flashed_messages,
        make_response,
)
import json
from hexlet_web_test_1.users_functions import validate_user


app = Flask(__name__)
app.secret_key = "lolkek"


def load_users():
    return json.loads(request.cookies.get('users', json.dumps([])))


@app.route('/')
def hello_world():
    url_for('users')
    return render_template(
        'index.html'
    )


@app.route('/users/')
def users():
    messages = get_flashed_messages()
    users_list = load_users()
    existing_users = [user for user in users_list if user]
    response = make_response( render_template(
        'users/index.html',
        users=existing_users,
        messages=messages
    ))
    return response


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

    users_list = load_users()
    user['id'] = str(len(users_list) + 1)
    users_list.append(user)

#    with open('users.json', 'w') as file:
#        json.dump(users_list, file, indent=1)

    response = make_response(redirect(url_for('users'), code=302))
    response.set_cookie('users', json.dumps(users_list))
    flash('User successfully created! You are awesome!', 'success')

    return response

@app.route('/users/<id>')
def user_page(id):
    users_list = load_users()
    selected_users = [user for user in users_list if user.get('id') == id]

    if selected_users == []:
        return 'Page not found. No such user', 404

    return render_template(
        'users/user-page.html',
        user=selected_users[0]
    )


@app.route('/users/<id>/edit')
def edit_user(id):
    users_list = load_users()
    user = next(filter(lambda user: user.get('id') == str(id), users_list))
    errors = {}

    return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
    )


@app.post('/users/<id>/patch')
def user_patch(id):
    new_data = request.form.to_dict()
    errors = validate_user(new_data)

    if errors != {}:
        return render_template(
            'users/edit.html',
            user=new_data,
            errors=errors,
        ), 422
    

    new_data['id'] = id
    new_data['kek'] = new_data.get('kek', '0')

    users_list = load_users()
    users_list[int(id) - 1] = new_data

#    with open('users.json', 'w') as file:
#        json.dump(users_list, file, indent=1)

    response = make_response(redirect(url_for('users'), code=302))
    response.set_cookie('users', json.dumps(users_list))

    flash(f'User {new_data["name"]} successfully updated!', 'success')
    return response


@app.post('/users/<id>/delete')
def delete_user(id):
    users_list = load_users()
    users_list[int(id) - 1] = {}

#    with open('users.json', 'w') as file:
#        json.dump(users_list, file, indent=1)

    response = make_response(redirect(url_for('users'), code=302))
    response.set_cookie('users', json.dumps(users_list))
    flash('User successfully deleted!', 'success')
    return response

