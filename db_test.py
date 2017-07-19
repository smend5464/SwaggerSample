import sample_api.db_models as db
import json


def create_store_record():
    session = db.create_session()
    try:
        record_list = list()
        for store in session.query(db.Store):
            record = dict()
            record['identifier'] = store.identifier
            record['Address_Line_1'] = store.address_line_1
            record['Address_Line_2'] = store.address_line_2
            record['Zip'] = store.zip
            record['State'] = store.state
            record['Created'] = store.created.strftime('%m%d%Y %H:%M:%S')
            record['Updated'] = store.updated.strftime('%m%d%Y %H:%M:%S')

            reg_list = list()
            for cash_register in store.cash_registers:
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


if __name__ == '__main__':

    rec_out = create_store_record()
    print(rec_out)
