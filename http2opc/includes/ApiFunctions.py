###########################################################################
#
# API Functions for http2opc
#
# OpenOPC for Python Library Module - Copyright (c) 2007-2015 Barry Barnreiter (barrybb@gmail.com)
#
###########################################################################

import sys
import time
import OpenOPC
import json
import ConfigParser
import mTools

class ApiFunctions():
	def __init__(self, logger):

		self.logger = logger


	def init(self):

		config_filename = 'main.conf'
		self.config = ConfigParser.ConfigParser()
		file_handle = open(config_filename)
		self.config.readfp(file_handle)

		self.opc_classname = self.config.get('opc', 'classname')
		self.opc_servers = self.config.get('opc', 'servers')
		self.opc_host = self.config.get('opc', 'host')

		self.logger.info('Opc Class: ' + self.opc_classname) 
		self.logger.info('Opc Servers: ' + self.opc_servers) 
		self.logger.info('Opc Host: ' + self.opc_host)


		self.preferences = {}
		self.preferences['show_root'] = mTools.str_to_bool(self.config.get('preferences', 'show_root'))

		self.opc = OpenOPC.client()
		result = self.opc.connect(self.opc_servers, self.opc_host)
		#result = False
		if result:
			self.logger.info('... Successfully connected to OPC server')
			return True

		else:
			self.logger.error('... FAILED to connect to OPC Server' )
			time.sleep(5)
			self.init()


	## -- Make sure Opc is running
	def ping(self):

		results = self.opc.info()

		found = False
		if results:
			for result in results:
				if result[0] == 'State':
					found = True
					if result[1] == 'Running':

						return True

					else:
						self.logger.error('PING ERROR: State Found but not Recognised: ' + result[1] )
						self.opc.close()
						self.init()

		if not found:

			self.logger.error('PING ERROR: Could not find State. Reconnecting...')
			self.opc.close()
			return False

	## -- Mirror to OpenOPC's list function with non-recursive options set. You can parse in either '*' or the branch that you would like to list.
	def list(self, params):

		if not self.preferences['show_root']:
			params = 'Root.' + params
		
		lst = self.opc.list(params, False, False, True)
		return lst

	## -- Mirror to the OpenOPC's list function with recursive options set. It returns a flat list of all leaves from the parameters set. You can parse in either '*' or the branch you would like to list.
	def listRecursive(self, params):
		
		lst = self.opc.list(params, True, False, True)
		return lst


	## -- Returns the next level of "branch" based on the parameters set. You can parse in either '*' or the branch you would like the next level of.
	def listTree(self, params):

		if not self.preferences['show_root']:
			params = 'Root.' + params

		lst = self.opc.list(params, False, False, True)
		parent = params[:-1]
		tree = []
		description = None
		for leaf in lst:
			
			leaf_stripped = leaf[0].replace(parent, '')

			split = leaf_stripped.split('.')

			if split[1] == 'Value':
				final_leaf = [leaf[0], 'Leaf']

			elif split[2] == 'Value':

				values = self.properties(leaf[0])
				for v in values:
					if v[2] == 'Item Description':
						description = v[3]

				final_leaf = [split[0], 'Branch', description]

			else:
				final_leaf = [split[0], 'Branch', description]

			if final_leaf not in tree:

				tree.append(final_leaf)


		return tree


	def listOneDeep(self, params):

		if not self.preferences['show_root']:
			params = 'Root.' + params

		lst = self.opc.list(params, False, False, True)
		parent = params[:-1]

		new_params = []
		for leaf in lst:
			
			leaf_stripped = leaf[0].replace(parent, '')

			split = leaf_stripped.split('.')

			new_params.append(leaf[0])

		new_lst = self.properties(new_params)

		branch = {}
		count = 0
		for tag_row in new_lst:

			if tag_row[0] not in branch:
				branch[tag_row[0]] = []

			branch[tag_row[0]].append(tag_row)


		for leaf in branch:
			branch[leaf].append('Leaf')

		return branch				

	## -- Mimics OpenOPC's read function. Parsing in a branch or leaf and it will return a tuple of values.
	def read(self, params):

		lst = self.opc.read(params)

		return lst

	## -- Mimics the OpenOPC's properties function. Parsing in a leaf name or multiple leaves will return the result that you would expect when calling it via OpenOPC
	def properties(self, params, json=False):

		if type(params).__name__=='list':
			split = params
		else:
			split = params.split(',')

		lst = self.opc.properties(split)

		if json:

			lst = self.buildJsonList(lst)

		return lst


	def buildJsonList(self, results):

		branch = []
		leaf = {}

		for result in results:

			if 'Item ID (virtual property)' not in leaf:

				leaf = {}

			elif leaf['Item ID (virtual property)'] != result[0]:

				branch.append(leaf)
				leaf = {}

			leaf[result[2]] = result[3]

		branch.append(leaf)

		return branch


	def search(self, params):

		params = '*' + params + '*'

		lst = self.opc.list(params, False, False, True)
		return lst

	def testing(self, params):

		params = '*' + params + '*'

		lst = self.opc.list(params, False, False, True)

		return lst

	def test_call(self):

		lst = self.opc.info()
		return lst

