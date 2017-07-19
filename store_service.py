import json
from flask import Flask
from flask_restplus import Resource
from sample_api import api
from waitress import serve
from werkzeug.contrib.fixers import ProxyFix


@api.route('/swagger')
@api.doc(False)
class Swagger(Resource):
    def get(self):
        with open('swagger.json', 'w') as f:
            f.write(json.dumps(api.__schema__))
        return 'success', 200

# Initialize the service
service = Flask(__name__)
service.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
service.config['RESTPLUS_MASK_SWAGGER'] = False
service.wsgi_app = ProxyFix(service.wsgi_app)
api.init_app(service)


if __name__ == '__main__':
    serve(app=service, listen="localhost:5501")
