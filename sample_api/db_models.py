import arrow
import json
from collections import OrderedDict
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, DateTime, Integer, BIGINT, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///stores.sdb')
create_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
session = create_session()


class Store(Base):
    __tablename__ = 'stores'

    store_id = Column(Integer(), primary_key=True)
    identifier = Column(String(), unique=True)
    address_line_1 = Column(String())
    address_line_2 = Column(String())
    zip = Column(String())
    state = Column(String())
    created = Column(DateTime())
    updated = Column(DateTime())
    cash_registers = relationship('Register', back_populates='store', lazy=False)

    def __init__(self, identifier: str, address_line_1: str,
                 zip_code: str, state: str, address_line_2: str = '', ):
        self.identifier = identifier
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.zip = zip_code
        self.state = state
        self.created = arrow.utcnow().datetime
        self.updated = arrow.utcnow().datetime

    def __repr__(self):
        res = OrderedDict()
        registers = list()
        for cash_register in self.cash_registers:
            registers.append({'identifier': cash_register.identifier,
                              'balance': cash_register.balance})
        res['store_id'] = self.store_id
        res['identifier'] = self.identifier
        res['Address_line_1'] = self.address_line_1
        res['Address_line_2'] = self.address_line_2
        res['Zip'] = self.zip
        res['State'] = self.state
        res['Registers'] = registers
        return json.dumps(res)


class Register(Base):
    __tablename__ = 'registers'

    register_id = Column(Integer(), primary_key=True)
    store_id = Column(Integer(), ForeignKey('stores.store_id'))
    identifier = Column(String(), unique=True)
    balance = Column(BIGINT)
    created = Column(DateTime())
    updated = Column(DateTime())
    store = relationship('Store', back_populates='cash_registers', lazy=False)

    def __init__(self, identifier: str, balance: int = 0):
        self.identifier = identifier
        self.balance = balance
        self.created = arrow.utcnow().datetime
        self.updated = arrow.utcnow().datetime

    def __repr__(self):
        res = OrderedDict()
        res['store_id'] = self.store_id
        res['identifier'] = self.identifier
        res['balance'] = self.balance
        return json.dumps(res)


def initialize_data():
    stores = ['WABot1234', 'WABel673', 'WALyn8973']
    cnt = 0
    for store in stores:
        reg_list = []
        store_rec = Store(store, 'addr line 1', '98012', 'WA', 'addr line 2')
        cnt += 1
        reg1 = Register('REG_' + store + str(cnt), 12593)
        reg_list.append(reg1)
        cnt += 1
        reg2 = Register('REG_' + store + str(cnt), 12500)
        reg_list.append(reg2)
        store_rec.registers = reg_list
        session.add(store_rec)
        session.add(reg1)
        session.add(reg2)

    session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()

    initialize_data()
