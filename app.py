from flask import Flask, got_request_exception
from flask_restful import Api
from loguru import logger
from svbs import AskHandler

app = Flask(__name__)

# Routes
api = Api(app)

     
print("test")
api.add_resource(AskHandler, '/ask')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # Running on all addresses