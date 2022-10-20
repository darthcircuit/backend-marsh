from flask import jsonify, request, Blueprint
from organizations import (
    Organizations,
    OrganizationsSchema,
    organization_schema,
    organizations_schema,
)
from db import db, populate_object


orgs = Blueprint("orgs", __name__)


@orgs.route("/orgs/get", methods=["GET"])
def get_all_active_org_ids_route():
    org_ids = db.session.query(Organizations).filter(Organizations.active == True).all()

    if org_ids:
        return jsonify(organizations_schema.dump(org_ids)), 200
    else:
        return jsonify("No matching records"), 404


@orgs.route("/org/get/<org_id>")
def get_org_by_id(org_id):
    org = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

    if org:
        return jsonify(organization_schema.dump(org))

    else:
        return jsonify("Invalid Organizaion")


@orgs.route("/org/update/<org_id>", methods=["POST"])
def update_org_id_route(org_id):
    org_id_ojb = (
        db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    )
    new_data = request.form if request.form else request.json

    if new_data:
        new_data = dict(new_data)
    else:
        return jsonify("No values to change")

    updated_fields = populate_object(org_id_ojb, new_data)

    if updated_fields:
        db.session.commit()
        return jsonify(f"{', '.join(updated_fields)} updated for org_id ID: {org_id}")

    else:
        return jsonify(f"No Fields Updated")


@orgs.route("/org/deactivate/<org_id>", methods=["POST"])
def deactivate_org_id_route(org_id):
    selected_org_id = (
        db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    )

    if selected_org_id:
        selected_org_id.active = False
        db.session.commit()
        return jsonify(f"org_id with ID {org_id} has been set to inactive."), 200
    else:
        return "Invalid"


@orgs.route("/org/activate/<org_id>", methods=["POST"])
def activate_org_id_route(org_id):
    selected_org_id = (
        db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    )

    if selected_org_id:
        selected_org_id.active = True
        db.session.commit()
        return jsonify(f"org_id with ID {org_id} has been set to active."), 200
    else:
        return "Invalid"


@orgs.route("/org/delete/<org_id>", methods=["POST"])
def delete_org_id_route(org_id):
    selected_org_id = (
        db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    )

    db.session.delete(selected_org_id)
    db.session.commit()

    return jsonify(f"Org with ID {org_id} has been deleted")


@orgs.route("/org/add", methods=["POST"])
def org_id_add():
    post_data = request.form if request.form else request.json

    # create blank org object to get org_id, then populate with dictionary from form.
    new_org = Organizations(" ", " ", " ", " ", " ")
    populate_object(new_org, post_data)
    db.session.add(new_org)
    db.session.commit()

    return jsonify("Organization created"), 201
