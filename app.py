from flask import Flask
from restapi import restapi

app = Flask(__name__)

app.register_blueprint(restapi)

#driver_function

if __name__=='__main__':
    app.run(debug=True)