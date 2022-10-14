from flask import Flask, request, jsonify
from users import Users
from organizations import Organizations, organization_schema, organizations_schema
from db import *
import routes

app = Flask(__name__)

app.register_blueprint(routes.users)
app.register_blueprint(routes.orgs)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://johnipson@127.0.0.1:5432/alchemy"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)


def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done!")


if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0")
