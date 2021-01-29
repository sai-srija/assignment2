from flask import Blueprint,request,jsonify,make_response
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from functools import wraps 

restapi = Blueprint('restapi', __name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'admin' and auth.password == 'password':
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

cred=credentials.Certificate("test-23303-firebase-adminsdk-439b8-de5839ebb9.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
db_ref=db.collection('Detailsofperson')

@restapi.route('/add',methods=['GET','POST'])
@auth_required
def create():
    try:
        f=open('data.json',)
        data=json.load(f)
        db_ref.document(str(data["id"])).set(data)
        return jsonify({"success":True}), 200
    except Exception as e:
        return f"An Error Occured:{e}"

@restapi.route('/read/', methods=['GET'])
@auth_required
def read():
    try:
        id_ref = request.args.get('id')
        if id_ref:
            ans = db_ref.document(id_ref).get()
            return jsonify(ans.to_dict()), 200
        else:
            answers =[]
            for record in db_ref.stream():
                answers.append(record.to_dict())
            return jsonify(answers), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@restapi.route('/delete/', methods=['GET', 'DELETE'])
@auth_required
def delete():
    try:
        id_ref = request.args.get('id')
        ans=db_ref.document(id_ref).get()
        if ans.exists:
            db_ref.document(id_ref).delete()
            answers =[]
            for record in db_ref.stream():
                answers.append(record.to_dict())
        else:
            return jsonify({"not found":False}), 200
        return jsonify({"success": True},answers), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@restapi.route('/update/', methods=['GET','POST', 'PUT'])
@auth_required
def update():
    try:
        id_ref = request.args.get('id')
        ans=db_ref.document(id_ref).get()
        if ans.exists:
            f=open('update.json',)
            data=json.load(f)
            db_ref.document(id_ref).update(data)
        else:
            return "id not found"
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@restapi.route('/filter/', methods=['GET'])
@auth_required
def filter():
    try:
        age_ref = request.args.get('age')
        docs=db_ref.where("age","==",int(age_ref)).get()
        filterans=[]
        for doc in docs:
            filterans.append(doc.to_dict())
        return jsonify(filterans), 200
    except Exception as e:
        return f"An Error Occured: {e}"