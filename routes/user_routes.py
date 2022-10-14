from flask import jsonify, request, Blueprint
from users import Users, user_schema, users_schema
from db import db, populate_object


users = Blueprint("users", __name__)


@users.route("/users/get", methods=["GET"])
def get_all_active_users_route():
    users = db.session.query(Users).filter(Users.active == True).all()

    if users:
        return jsonify(users_schema.dump(users)), 200
    else:
        return jsonify("No matching records"), 404


@users.route("/user/update/<user_id>", methods=["POST"])
def update_user_route(user_id):
    user_ojb = db.session.query(Users).filter(Users.user_id == user_id).first()
    new_data = request.form if request.form else request.json

    if new_data:
        new_data = dict(new_data)
    else:
        return jsonify("No values to change")

    updated_fields = populate_object(user_ojb, new_data)

    if updated_fields:
        db.session.commit()
        return jsonify(f"{', '.join(updated_fields)} updated for User ID: {user_id}")

    else:
        return jsonify(f"No Fields Updated")


@users.route("/user/deactivate/<user_id>", methods=["POST"])
def deactivate_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if selected_user:
        selected_user.active = False
        db.session.commit()
        return jsonify(f"User with ID {user_id} has been set to inactive."), 200
    else:
        return "Invalid"


@users.route("/user/activate/<user_id>", methods=["POST"])
def activate_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if selected_user:
        selected_user.active = True
        db.session.commit()
        return jsonify(f"User with ID {user_id} has been set to active."), 200
    else:
        return "Invalid"


@users.route("/user/delete/<user_id>", methods=["POST"])
def delete_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    db.session.delete(selected_user)
    db.session.commit()

    return jsonify(f"User with ID {user_id} has been deleted")


@users.route("/user/add", methods=["POST"])
def user_add():
    post_data = request.form if request.form else request.json

    # create blank user object to get user_id, then populate with dictionary from form.
    new_user = Users(" ", " ", " ", " ", " ", " ", post_data.get("org_id"), " ")
    populate_object(new_user, post_data)
    db.session.add(new_user)
    db.session.commit()

    return jsonify("User created"), 201
