from flask_restplus import fields, Namespace, Resource
import sample_api.db_models as db

api = Namespace(name='Stores', description='API for store level access')

register = api.model(name='register', model={'identifier': fields.String(),
                                             'balance': fields.Fixed(decimals=2)})

store = api.model(name='store', model={'identifier': fields.String(),
                                       'Address_Line_1': fields.String(),
                                       'Address_Line_2': fields.String(),
                                       'Zip': fields.String(),
                                       'State': fields.String(),
                                       'Registers': fields.List(fields.Nested(register))})

store_list = api.model(name='store_list', model={'stores': fields.List(fields.Nested(store))})


@api.route('/')
class Stores(Resource):
    @api.marshal_with(store_list)
    def get(self):
        res = dict()
        res['stores'] = self.get_store_records()
        return res

    def get_store_records(self):
        session = db.create_session()
        try:
            record_list = list()
            for store_rec in session.query(db.Store):
                record = dict()
                record['identifier'] = store_rec.identifier
                record['Address_Line_1'] = store_rec.address_line_1
                record['Address_Line_2'] = store_rec.address_line_2
                record['Zip'] = store_rec.zip
                record['State'] = store_rec.state
                record['Created'] = store_rec.created.strftime('%m%d%Y %H:%M:%S')
                record['Updated'] = store_rec.updated.strftime('%m%d%Y %H:%M:%S')

                reg_list = list()
                for cash_register in store_rec.cash_registers:
                    reg_rec = dict()
                    reg_rec['identifier'] = cash_register.identifier
                    reg_rec['balance'] = cash_register.balance / 100
                    reg_rec['Created'] = cash_register.created.strftime('%m%d%Y %H:%M:%S')
                    reg_rec['Updated'] = cash_register.updated.strftime('%m%d%Y %H:%M:%S')
                    reg_list.append(reg_rec)

                record['Registers'] = reg_list

                record_list.append(record)

            return record_list
        finally:
            session.close()


@api.route('/store/<string:identifier>')
@api.param('identifier', 'The store number')
class Store(Resource):
    @api.marshal_with(store)
    @api.response(200, 'Store Found')
    @api.response(404, 'Not Found')
    def get(self, identifier: str):
        res = self.get_store_record(identifier)
        store_res = dict()
        store_res['store'] = res
        return res

    def get_store_record(self, identifier: str):
        session = db.create_session()
        try:
            store_rec = session.query(db.Store).filter(db.Store.identifier == identifier).first()
            if store_rec:
                record = dict()
                record['identifier'] = store_rec.identifier
                record['Address_Line_1'] = store_rec.address_line_1
                record['Address_Line_2'] = store_rec.address_line_2
                record['Zip'] = store_rec.zip
                record['State'] = store_rec.state
                record['Created'] = store_rec.created.strftime('%m%d%Y %H:%M:%S')
                record['Updated'] = store_rec.updated.strftime('%m%d%Y %H:%M:%S')

                reg_list = list()
                for cash_register in store_rec.cash_registers:
                    reg_rec = dict()
                    reg_rec['identifier'] = cash_register.identifier
                    reg_rec['balance'] = cash_register.balance / 100
                    reg_rec['Created'] = cash_register.created.strftime('%m%d%Y %H:%M:%S')
                    reg_rec['Updated'] = cash_register.updated.strftime('%m%d%Y %H:%M:%S')
                    reg_list.append(reg_rec)

                record['Registers'] = reg_list
                return record
            else:
                return 'Not Found', 404
        finally:
            session.close()

    @api.expect(store)
    @api.response(201, 'Store Created Successfully')
    @api.response(401, 'Store Not Created')
    def post(self, identifier: str):
        disp = True
        if disp:
            return 'Store Created Successfully', 201
        else:
            return 'Store Not Created', 401

    @api.expect(store)
    def put(self, identifier: str):
        pass
