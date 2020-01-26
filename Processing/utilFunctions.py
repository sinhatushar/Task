import os
import json

class DoProcessing() :

	#count = 0 
	def __init__( self, JSON_FILE_URL, LOG_FILE_URL, PARENT_DIR  ) : 
		'''Constructor for this class'''

		self.JSON_FILE_URL = JSON_FILE_URL
		self.LOG_FILE_URL  = LOG_FILE_URL
		self.PARENT_DIR    = PARENT_DIR 

	def getJsonFileContent( self, url ) :
		''' Reads the content from filter json and returns it in a dictionary format '''
		
		cmd 			= 'curl ' + url

		jsonFileContent = os.popen( cmd ).read()
		jsonFileDict 	= json.loads( jsonFileContent )

		return jsonFileDict


	def getLogFileContent( self, url ) :
		''' Reads the content from log file and returns it in a line by line split list '''
		
		cmd 			= 'curl ' + url

		logFileContent  = os.popen( cmd ).read()
		logFileLineList = logFileContent.splitlines()

		return logFileLineList


	def getInfoFieldsFromLine( self, logFileLine ) :
		''' Parses given line from the log file and returns a dictionary containing the extracted information from the line ''' 
		
		infoDict 				   = { }
		splittedLine  		       = logFileLine.split() 
		
		infoDict[ 'year' ]		   = splittedLine[ 0 ]
		infoDict[ 'month' ]        = splittedLine[ 1 ]
		infoDict[ 'day' ]		   = splittedLine[ 2 ]
		
		infoDict[ 'status' ] 	   = splittedLine[ splittedLine.index( 'status:' ) + 1 ]	
		if infoDict[ 'status' ][ -1 ] == ',' :
			infoDict[ 'status' ] = infoDict[ 'status' ][0:-1]

		messageStartIndex   	   = splittedLine.index( 'Message:' ) + 1 
		Message  				   = ''	
		for i in range( messageStartIndex, len( splittedLine ) ) :
			Message += splittedLine[ i ] + ' '		
		
		infoDict[ 'Message' ] 	   = Message

		return infoDict 


	def createDirectoryAndFiles( self ) :
		''' Does the processing, creates the directory and stores the file with content '''

		#count = count + 1
		 
		jsonFileDict    = self.getJsonFileContent( self.JSON_FILE_URL )
		logFileLineList = self.getLogFileContent( self.LOG_FILE_URL )

		index = 0 
		dictIpAddress = { }	
		for logFileLine in logFileLineList : 
			splittedLine  		       = logFileLine.split() 
			ipAddress     			   = splittedLine[ splittedLine.index( 'ip-address:' ) + 1 ][:-1]
			
			if ipAddress in dictIpAddress.keys() :
				dictIpAddress[ ipAddress ].append( index )
			else :
				dictIpAddress[ ipAddress ] = [ index ]

			index 	      			   = index + 1 

		for dictionary in jsonFileDict[ 'data' ] :
			ipAddress 	  = dictionary[ 'ipAddress' ]
			degugFlagList = dictionary[ 'debugFlag' ]

			if ipAddress in dictIpAddress.keys() :
				indexList         = dictIpAddress[ ipAddress ]
				
				for index in indexList:
					logFileLine   = logFileLineList[ index ]
					infoDict      = self.getInfoFieldsFromLine( logFileLine )

					date 	      = '' 
					date 		  = infoDict[ 'month' ] + '-' + infoDict[ 'day' ] + '-' + infoDict[ 'year' ]  

					directoryPath = os.path.join( self.PARENT_DIR, date ) 

					if os.path.isdir( directoryPath ) == 0 :
						os.mkdir( directoryPath )

					filePath      = os.path.join( directoryPath, ipAddress + '_' + infoDict[ 'status' ] + '.log' )

					if os.path.isfile( filePath ) == 0 :				
						file 	  = open( filePath, "w+" )
						file.write( infoDict[ 'Message' ] + '\n' )
						file.close()
					else :
						file      = open( filePath, 'a' )
						file.write( infoDict[ 'Message' ] + '\n' )
						file.close()




