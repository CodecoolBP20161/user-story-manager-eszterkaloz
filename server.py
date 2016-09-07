from flask import Flask, jsonify, g, current_app, request, render_template, redirect, url_for
from peewee import *
from build import *

app = Flask("Sprint reporter app server")


# def get_connect_string():
#     with open('connect_str.txt', "r") as f:
#         return f.readline().strip()


# @app.before_request
# def before_request():
#     db = get_db()
#     db.connect()
#
#
# @app.after_request
# def after_request(response):
#     db = get_db()
#     db.close()
#     return response


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#
# Routes
#


@app.route('/story', methods=['GET'])
def show_form_template():
    return render_template('form.html', title="Add new user story", action="Save", userstory="")


@app.route('/story', methods=['POST'])
def add_new_user_story():
    columns = ['story_title', 'user_story', 'acceptance_crit', 'business_value', 'estimation', 'status']
    data = [request.form[element] for element in columns]
    new_user_story = UserStory.create(story_title=data[0],
                                      user_story=data[1],
                                      acceptance_crit=data[2],
                                      business_value=data[3],
                                      estimation=data[4],
                                      status=data[5]
                                      )
    new_user_story.save()
    return redirect(url_for('show_user_story_table'))


@app.route('/story/<story_id>', methods=['POST', 'GET'])
def edit_user_story(story_id):
    if request.method == 'POST':
        columns = ['story_title', 'user_story', 'acceptance_crit', 'business_value', 'estimation', 'status']
        data = [request.form[element] for element in columns]
        UserStory.update(story_title=data[0],
                         user_story=data[1],
                         acceptance_crit=data[2],
                         business_value=data[3],
                         estimation=data[4],
                         status=data[5]).where(UserStory.id == story_id).execute()
        return redirect(url_for('show_user_story_table'))

    else:
        user_story = UserStory.get(UserStory.id == story_id)
        return render_template('form.html', title="Edit user story", action="Update", userstory=user_story)


@app.route('/story/<story_id>/delete')
def delete_user_story(story_id):
    UserStory.delete().where(UserStory.id == story_id).execute()
    return redirect(url_for('show_user_story_table'))


@app.route('/list')
def show_user_story_table():
    user_stories = UserStory.select()
    return render_template('list.html', userstories=user_stories)


@app.route('/')
def show_user_story_list():
    return redirect(url_for('show_user_story_table'))


with app.app_context():
    create_table()
    print(current_app.name + ' started')


if __name__ == "__main__":
    # create_table()
    app.run(debug=True)
