from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
import os

from .config import JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR
from .util_functions import DoProcessing, FindContentForFile, FindContentForAll

@csrf_exempt 
def home( request ):
	''' Returns html page for home page '''

	obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	return render( request, 'home.html' )


@csrf_exempt 
def invokeCreationOfFiles( request ):
	''' Returns html page for storing files and invokes the operation of creating files ''' 

	obj   = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	error = obj.createDirectoryAndFiles()
	
	if error :
		return render( request, 'error.html', status = 500 )
	
	return render( request, 'invoke.html', status = 200 )


@csrf_exempt 
def getListOfAllFiles( request ):
	''' Returns html page for showing list of all the files present in storage '''

	obj               = FindContentForAll( STORAGE_DIR )
	contentDictList   = obj.getContentForAll()

	context 		  = {}
	context[ 'rows' ] = contentDictList
	
	if len( contentDictList ) == 0 : 
		return render( request, 'empty.html', status = 404 )
		'''To get JSON response on Postman or Swagger, comment out the above line and uncomment the below line.'''
		##return JsonResponse( context, status = 404 )

	return render( request, 'listoffiles.html', context, status = 200  )
	
	'''To get JSON response on Postman or Swagger, comment out the above line and uncomment the below line.'''
	##return JsonResponse( context, status = 404 )


@csrf_exempt 
def getContentOfFile( request ):
	''' Returns html page to show the content of a file '''

	folderName 		   = request.GET[ 'Folder Name' ] 
	fileName   		   = request.GET[ 'File Name' ]

	obj 	   		   = FindContentForFile( STORAGE_DIR, folderName, fileName )
	( error, message ) = obj.getFileContent()

	if error :
		return render( request, 'wrongname.html', status = 400 )
		'''To get JSON response on Postman or Swagger, comment out the above line and uncomment the below line.'''
		##return JsonResponse( messageDict, status = 400 )

	message     = message.replace( "\n", "<br>" )	
	messageDict = { 'message' : message } 
	
	return render( request, 'message.html', messageDict, status = 200 ) 
	
	'''To get JSON response on Postman or Swagger, comment out the above line and uncomment the below line.'''
	##return JsonResponse( messageDict, status = 400 )
