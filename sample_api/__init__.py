from flask_restplus import Api
from .store_api import api as ns_store

api = Api(title='Store API', description='Sample usage of flask_restplus',
          version='0.01.0')

api.add_namespace(ns_store)
