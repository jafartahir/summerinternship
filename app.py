from flask import Flask, jsonify, make_response
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
def hello():
    item = SongsModel("Romero Allen", "Atomic Dim")
    item.update(
        actions=[
            SongsModel.id.set(str(random.randint(100, 999)))
        ]
    )
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
