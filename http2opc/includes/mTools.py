import thread
import logging
import os
import datetime

def initLogging(logfile_prefix, level_name, log_name):
	LEVELS = {'debug': logging.DEBUG,
		'info': logging.INFO,
		'warning': logging.WARNING,
		'error': logging.ERROR,
		'critical': logging.CRITICAL}	

	datefmt='%Y-%m-%d %H:%M:%S'
	
	## -- Create Logfile Name if prefix exists    

	if logfile_prefix:
		now = datetime.datetime.now()
		LOG_FILENAME = mConfig.log_path + logfile_prefix + '_' + now.strftime("%Y-%m-%d") + '.log'
	else:
		LOG_FILENAME = None
		
	## -- Get the level for logging
	level = LEVELS.get(level_name, logging.NOTSET)  

	## -- add filename=LOG_FILENAME below as parameter to write to file      
	logging.basicConfig(level=level,
						format='%(asctime)s - %(message)s',
						datefmt=datefmt,
						filename=LOG_FILENAME
						)  
	logger = logging.getLogger(log_name)
    
    #formatter = logging.Formatter("%("+datefmt+")s - %(name)s - %(levelname)s - %(message)s")
    #ch = logging.StreamHandler()
    #ch.setFormatter(formatter)
    #logger.addHandler(ch)
            
	return logger    

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError
class Thread:
    def __init__(self):
        #self.logger = logger
        #self.session = session
        self.running = False

    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        #self.logger.info('STARTED Thread')

    def Stop(self):
        self.keepGoing = False
        self.running = False
        #self.logger.info('STOPPED Thread')

    def IsRunning(self):
        if hasattr(self,'running'):
            return self.running
        else:
            return False