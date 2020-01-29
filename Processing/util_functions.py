import os
import json
import logging

logging.getLogger().setLevel(logging.INFO)


class DoProcessing() :

	def __init__( self, JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR ) : 
		''' Constructor for this class '''

		self.JSON_FILE_URL = JSON_FILE_URL
		self.LOG_FILE_URL  = LOG_FILE_URL
		self.STORAGE_DIR   = STORAGE_DIR 


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
		
		error = False  

		try :	
			jsonFileDict    = self.getJsonFileContent( self.JSON_FILE_URL )			
		
		except Exception as e :
			error = True
			logging.error(e)	
			return error

		try :	
			logFileLineList = self.getLogFileContent( self.LOG_FILE_URL )
		
		except Exception as e :
			error = True
			logging.error(e)
			return error 	

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

		finalContentDict = {}

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

					directoryName = date  
					fileName      = ipAddress + '_' + infoDict[ 'status' ] + '.log' 

					pathTuple 	  = ( directoryName, fileName )

					if pathTuple in finalContentDict.keys() :
						finalContentDict[ pathTuple ].append( infoDict[ 'Message' ] + '\n')
					else :
						finalContentDict[ pathTuple ] = [ infoDict[ 'Message' ] + '\n' ]

		for pathTuple, messageList in finalContentDict.items() :
			directoryName = pathTuple[ 0 ]
			fileName      = pathTuple[ 1 ]
			
			directoryPath = os.path.join( self.STORAGE_DIR, directoryName )				
			filePath      = os.path.join( directoryPath, fileName )

			fullContentOfFile = ''
			for message in messageList :
				fullContentOfFile += message

			if os.path.isdir( directoryPath ) == 0 :
				os.mkdir( directoryPath )			

			file 	  = open( filePath, "w+" )
			file.write( fullContentOfFile )
			file.close()
			logging.info( "Created file with file name %s at path %s", fileName, directoryPath )

		return error 



class FindContentForFile() : 

 	def __init__( self, STORAGE_DIR, folderName, fileName ) :
 		''' Constructor for this class '''

 		self.STORAGE_DIR = STORAGE_DIR
 		self.folderName  = folderName
 		self.fileName    = fileName


 	def getFileContent( self ) :
 		''' Gets the content of a file '''

 		filePath = self.STORAGE_DIR + '/' + self.folderName + '/' + self.fileName
 		
 		error   = False
 		message = '' 

 		try : 
	 		file 	= open( filePath, "r" )
	 		message = file.read()
	 		file.close()

 		except FileNotFoundError as e :
 			error = True
 			logging.error(e)

 		except Exception as e :
 			error = True
 			logging.error(e)

 		return ( error, message ) 



class FindContentForAll() : 

	def __init__( self, STORAGE_DIR ) :
		''' Constructor for this class '''

		self.STORAGE_DIR = STORAGE_DIR


	def getContentForAll( self ) :
		''' Gets the content for all the files and returns a dictionary with file name, directory name and message '''

		contentDictList = [ ]

		folderNameList  = os.listdir( self.STORAGE_DIR )
		
		for folderName in folderNameList :
			fileNameList = os.listdir( self.STORAGE_DIR + '/' + folderName ) 

			for fileName in fileNameList :
				contentDict                 = {}
				contentDict[ 'folderName' ] = folderName
				
				ipAddress                   = fileName[ 0 : fileName.index('_') ]
				
				status 	  				    = fileName[ fileName.index('_') + 1 : -4 ]

				contentDict[ 'fileName' ]   = ipAddress + '_' + status + '.log' 
				
				obj 	  				    = FindContentForFile( self.STORAGE_DIR, folderName, fileName )
				message   				    = obj.getFileContent() 
				contentDict[ 'message' ]    = message 

				contentDictList.append( contentDict )
		
		return contentDictList










