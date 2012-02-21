# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)'cmp-
"""
#Pragma
from __future__ import unicode_literals

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from model import CustomerOrderModel, CustomerIncidentalModel, CustomerOrderIncidentalModel, CustomerOrderItemModel

from session import Session
import ttystatus
import uuid
from decimal import *

from task.base_task import BaseTask

class FinancialReportTask(BaseTask):
	
	def run(self, start_date, end_date):
		
		self.incidentals = {}
		query = self.session.query(CustomerIncidentalModel)
		for customer_incidental in query.yield_per(1000):
			self.incidentals[customer_incidental.id] = customer_incidental.name
		
		query = self.session.query(CustomerOrderModel)
		query = query.filter(CustomerOrderModel.ordered >= start_date)
		query = query.filter(CustomerOrderModel.ordered <=  end_date)
		query = query.filter(CustomerOrderModel.void == False)
		query = query.order_by(CustomerOrderModel.ordered, CustomerOrderModel.identifier)
		
		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal('Updating Catalog Items '))
		ts.add(ttystatus.Literal(' Elapsed: '))
		ts.add(ttystatus.ElapsedTime())
		ts.add(ttystatus.Literal(' Remaining: '))
		ts.add(ttystatus.RemainingTime('done', 'total'))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.ProgressBar('done', 'total'))
		ts['total'] = query.count()
		ts['done'] = 0
		
		self.data = []
		
		for customer_order in query.yield_per(1000):
			self.load_order(customer_order)
			ts['done'] += 1
		
		
		columns = ['identifier', 'ordered', 'closed', 'item_count', 'item_quantity', 'item_total']
		total_columns = ['item_count', 'item_quantity', 'item_total']
		for v in self.incidentals.itervalues():
			columns.append(v)
			total_columns.append(v)

		f = open('/tmp/financial_report.csv', 'w')

		totals = {}
		totals['identifier'] = 'Total'
		totals['ordered'] = ''
		totals['closed'] = ''
		
		for v in total_columns:
			totals[v] = Decimal(0)

		line = []
		for column in columns:
			line.append(column)
		f.write(','.join(line) + "\n")
		
		for fields in self.data:
			line = []
			for column in columns:
				
				if column in total_columns:
					totals[column] += fields[column]
				
				d = str(fields[column])
				line.append(d)
			f.write(','.join(line) + "\n")
		
		line = []
		for column in columns:
			line.append(str(totals[column]))
		f.write(','.join(line) + "\n")

		
			
	def load_order(self, customer_order):
		#print customer_order.identifier
		self.order_data = {}
		self.data.append(self.order_data)
		self.order_data['identifier'] = customer_order.identifier
		self.order_data['ordered'] = customer_order.ordered
		self.order_data['closed'] = customer_order.closed
		self.order_data['item_count'] = 0;
		self.order_data['item_quantity'] = Decimal(0);
		self.order_data['item_total'] = Decimal(0);
		
		for v in self.incidentals.itervalues():
			self.order_data[v] = Decimal(0);
			
		query = self.session.query(CustomerOrderItemModel)
		query = query.filter(CustomerOrderItemModel.customer_order_id == customer_order.id)
		query = query.filter(CustomerOrderItemModel.void == False)
		for customer_order_item in query.yield_per(1000):
			self.load_order_item(customer_order_item)
			
		query = self.session.query(CustomerOrderIncidentalModel)
		query = query.filter(CustomerOrderIncidentalModel.customer_order_id == customer_order.id)
		for customer_order_incidental in query.yield_per(1000):
			self.load_order_incidental(customer_order_incidental)


	def load_order_item(self, customer_order_item):
		#print customer_order_item.id
		self.order_data['item_count'] += 1
		self.order_data['item_quantity'] += customer_order_item.quantity
		self.order_data['item_total'] += customer_order_item.extended()


	def load_order_incidental(self, customer_order_incidental):
		v = self.incidentals[customer_order_incidental.customer_incidental_id]
		self.order_data[v] += customer_order_incidental.price
