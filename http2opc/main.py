###########################################################################
#
# API Functions for http2opc - Copyright (c) 2015-2016 Matz Persson (matz@headstation.com)
#
# OpenOPC for Python Library Module - Copyright (c) 2007-2015 Barry Barnreiter (barrybb@gmail.com)
#
###########################################################################
import os
import sys
import ConfigParser
import time
import includes.mTools as mTools
import includes.ApiServers as ApiServers

logfile_prefix = None

level_name = 'info' 
logger = mTools.initLogging(logfile_prefix, level_name, 'vplcd')

logger.info('## ---------------------------------- ##') 
logger.info('## STARTING http2opc daemon -------- ##') 
logger.info('## ---------------------------------- ##') 		

config_filename = 'main.conf'
config = ConfigParser.ConfigParser()
file_handle = open(config_filename)
config.readfp(file_handle)
logger.info('Config file: ' + config_filename) 		

server_ip = config.get('rest', 'server_ip')
server_port = int(config.get('rest', 'server_port'))


if server_ip:
	logger.info('RestApi Server IP: ' + server_ip)
else:
	logger.info('RestApi Server IP: Listening on ALL NICs' )

logger.info('RestApi Server Port: ' + str(server_port) ) 		

rest =  ApiServers.RestApiServer(logger,server_ip, server_port)
rest.Start()

#rest.startPing()
