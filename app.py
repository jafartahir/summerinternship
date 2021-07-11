from flask import Flask, jsonify, make_response, request
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
import random

app = Flask(__name__)

class AdmissionModel(Model):
    class Meta:
        table_name = 'NewAdmissions'

    institute = UnicodeAttribute(hash_key = True)
    enrollment = UnicodeAttribute(range_key = True)
    name = UnicodeAttribute(null = False)
    branch = UnicodeAttribute(null = False)
    batch = UnicodeAttribute(null = False)

@app.route("/")
def students():
    return jsonify([student.attribute_values for student in AdmissionModel.scan(rate_limit=1)])


@app.route("/admission", methods=["GET", "POST", "PUT", "DELETE"])
def student():
    try:
        student_data = request.get_json()['student']
        print(student_data)
        institute = student_data['institute']
        enrollment = student_data['enrollment']
        if request.method == "PUT":
            try:
                item = AdmissionModel.get(
                    hash_key = institute,
                    range_key = enrollment
                )
                actions = []
                if 'name' in student_data:
                    actions.append(AdmissionModel.name.set(student_data['name']))
                if 'branch' in student_data:
                    actions.append(AdmissionModel.branch.set(student_data['branch']))
                if 'batch' in student_data:
                    actions.append(AdmissionModel.batch.set(student_data['batch']))
                if len(actions):
                    print(actions)
                    item.update(actions = actions)
            except AdmissionModel.DoesNotExist as e:
                print(e)
                return make_response(
                    jsonify(error='Student not found. Please check institute and enrollment information.'),
                    500
                )
        elif request.method == "POST":
            try:
                item = AdmissionModel.get(
                    hash_key = institute,
                    range_key = enrollment
                )
                return make_response(
                    jsonify(error='Student already exists.'),
                    500
                )
            except AdmissionModel.DoesNotExist as e:
                AdmissionModel(
                    institute = student_data['institute'],
                    enrollment = student_data['enrollment'],
                    name = student_data['name'],
                    branch = student_data['branch'],
                    batch = student_data['batch']
                ).save()
        elif request.method == "GET":
            try:
                item = AdmissionModel.get(
                    hash_key = institute,
                    range_key = enrollment
                )
                return item.attribute_values
            except AdmissionModel.DoesNotExist as e:
                return make_response(
                    jsonify(error='Student does not exist.'),
                    500
                )
        elif request.method == "DELETE":
            try:
                item = AdmissionModel.get(
                    hash_key = institute,
                    range_key = enrollment
                )
                item.delete()
            except AdmissionModel.DoesNotExist as e:
                return make_response(
                    jsonify(error='Student does not exist.'),
                    500
                )
        return {}
    except Exception as e:
        print(e)
        return make_response(
            jsonify(error='Unexpected error.'),
            500
        )

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
