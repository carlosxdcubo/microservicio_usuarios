from turtle import st
from flask import Flask, request
import json

def user_field_validation(new_user):
    try:
        name=new_user['name']
    except:
        return{
            "message":"name field is empty"
            }  
    try:
        lastname=new_user['lastname']
    except:
        return{
            "message":"lastname field is empty"
            }
    try:
        document=new_user['document']
    except:
        return{
            "message":"document field is empty"
            }                    
    return{
        "message": "ok"
    }  
    


users ={
    "users": []
}
app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>Hello world</h1>"

@app.route("/health",methods=["GET"])
def health():
    return {
        "status": "ok",
        "message":"I'm alive"
    }

@app.route("/users", methods=["POST"])
def create_users():
    new_user = request.get_json()
    message=user_field_validation(new_user)
    if message["message"] == "ok":
        new_user={
            "name":str(new_user['name']),
            "lastname":str(new_user['lastname']),
            "document":int(new_user['document'])
        }
        users["users"].append(new_user)
        return {
        "message": "user created!"
      }
    else:
         return message


@app.route("/users", methods=["GET"])
def get_users():
    document=request.args.get('document')
    if document is not None:
        for i in users["users"]:
            if i["document"]== int(document):
                return {
                    "name": i["name"],
                    "lastname": i["lastname"]
                }
        return {
            "message":"El usuario con el documento "+str(document)+ " no existe"
        }        
    else:
        return dict(users)
    
@app.route("/users", methods=["DELETE"])
def delete_users():
    user_entry = request.get_json()
    user_document=user_entry["document"]
    for i in users["users"]:
            if i["document"]== int(user_document):
                users["users"].remove(i)
                return {
                     "message":"El usuario con el documento "+str(user_document)+ " ha sido eliminado"
                }
            
    return {
        "message":"El usuario con el documento "+str(user_document)+ " no existe"
    }        

app.run()