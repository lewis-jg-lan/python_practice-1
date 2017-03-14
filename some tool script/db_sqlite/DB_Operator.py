from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import get_class_by_table, get_tables, get_columns
import sqlite3
from datetime import datetime
from faker import *

class DBERROR(Exception):
	pass

class DB:
	Base = declarative_base()

	def __init__(self, db_name):
		db = 'sqlite:///%s' % db_name
		self.engine = create_engine(db)
		self.session = self.get_session()
		self.conn = sqlite3.connect(db_name)

	def create_db(self):
		DB.Base.metadata.create_all(self.engine)

	def get_session(self):
		DBSession = sessionmaker()
		DBSession.configure(bind=self.engine)
		session = DBSession()
		return session

	def drop_table(self, tablename):
		inspector = Inspector.from_engine(self.engine)
		if tablename in inspector.get_table_names():
			if tablename == IFA_DATA.__tablename__:
				print(inspector.get_table_names())
				IFA_DATA.__table__.drop(self.engine)
			elif tablename == QCR_DATA.__tablename__:
				QCR_DATA.__table__.drop(self.engine)
			else:
				print('there is no table such as ', tablename)
		else:
			print('there is no table such as %s' % tablename)

	def add_data(self, tablename, data):
		if tablename == IFA_DATA.__tablename__:
			if self.session.query(IFA_DATA).filter(IFA_DATA.id == data.id).first() is not None:
				print(data.id)
				self.session.merge(data)
			else:
				self.session.add(data)
		if tablename == QCR_DATA.__tablename__:
			if self.session.query(QCR_DATA).filter(QCR_DATA.id == data.id).first() is not None:
				print(data.id)
				self.session.merge(data)
			else:
				self.session.add(data)
		self.session.flush()
		self.session.commit()

	def delete_data(self, tablename, data):
		if tablename == IFA_DATA.__tablename__:
			if self.session.query(IFA_DATA).filter(IFA_DATA.id == data.id).first() is not None:
				self.session.query(IFA_DATA).filter(IFA_DATA.id == data.id).delete()
				self.session.commit()
			else:
				print('the data is not found')
		if tablename == QCR_DATA.__tablename__:
			if self.session.query(QCR_DATA).filter(QCR_DATA.id == data.id).first() is not None:
				self.session.query(QCR_DATA).filter(QCR_DATA.id == data.id).delete()
				self.session.commit()
			else:
				print('the data is not found')

	def query_data(self, tablename, filter_element=None, filter_value=None, query_all=True, **kwargs):
		cursor = self.conn.cursor()
		if filter_element is None and filter_value is None:
			execute_sql = 'select * from %s' % tablename
			return cursor.execute(execute_sql)
		elif kwargs['query'] is not None:
			execute_sql = 'select %s from %s where %s=?' % (kwargs['query'], tablename, filter_element)
		else:
			execute_sql = 'select * from %s where %s=?' % (tablename, filter_element)
		cursor.execute(execute_sql, (filter_value,))
		if query_all:
			values = cursor.fetchall()
			return values
		else:
			value = cursor.fetchone()
			return value[0]

	def update_data(self, tablename, id, *update_data, **kwargs):
		print(update_data)
		for x in update_data:
			print(x)
			update_sql = 'UPDATE %s SET %s = \'%s\' WHERE id = ?' % (tablename, x['column'], x['value'] )
			print(update_data)
			cursor = self.conn.cursor()
			cursor.execute(update_sql, (id, ))
			print(self.query_data(tablename))
			cursor.connection.commit()


class IFA_DATA(DB.Base):
	__tablename__ = 'IFA'
	id = Column('id', Integer, primary_key=True)
	station = Column('station', String(16))
	unit_sn = Column('unit_sn', String(16))
	fail_item = Column('fail_items', String(16))
	fail_date = Column('fail_date', DATETIME)
	issue_status = Column('issue_status', String(20))
	value = Column('value', String(20))
	remark = Column('remark', String(20))


class QCR_DATA(DB.Base):
	__tablename__ = 'QCR'
	id = Column('id', Integer, primary_key=True)
	station = Column('station', String(20))
	unit_sn = Column('unit_sn', String(20))
	first_result = Column('first_result', String(16))
	first_fail_log = Column('first_fail_log', String(200))
	second_result = Column('second_result', String(16))
	second_fail_log = Column('second_fail_log', String(200))
	third_result = Column('third_result', String(16))
	third_fail_log = Column('third_fail_log', String(200))
	except_fail_reason = Column('except_fail_reason', String(200))


if __name__ == '__main__':
	db = DB('xxx.db')
	db.create_db()
	faker = Faker()
	ifa = IFA_DATA(id=1,
	               station=faker.name(),
	               unit_sn=faker.phone_number(),
	               fail_item=faker.text(),
	               fail_date=datetime.now(),
	               issue_status=faker.text(),
	               value=faker.text(),
	               remark=faker.text())
	db.add_data('IFA', ifa)
	s = db.query_data('IFA', filter_element='id', filter_value='1', query='fail_items', query_all=False)
	print(s)
	columns = ['station', 'unit_sn', 'value']
	values = ['QT1', '1234567890', '100']
	updates_values =[{'column':columns[x],
	                  'value': values[x]} for x in range(0, len(columns))]

	db.update_data('IFA', 1, *updates_values)
	s = db.query_data('IFA', filter_element='id', filter_value='1', query='fail_items', query_all=False)
	print(s)

	s = db.query_data('IFA', filter_element='id', filter_value='1', query='station', query_all=False)
	print(s)

	s = db.query_data('IFA', filter_element='id', filter_value='1', query='unit_sn', query_all=False)
	print(s)

	s = db.query_data('IFA', filter_element='id', filter_value='1', query='value', query_all=False)
	print(s)
