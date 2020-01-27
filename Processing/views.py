from django.shortcuts import render
from django.http import  HttpResponse
import os

from .config import JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR
from .util_functions import DoProcessing, FindContentForFile, FindContentForAll


def home( request ):
	''''''
	obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	return render( request, 'home.html' )


def invokeCreationOfFiles( request ):
	'''''' 
	obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	obj.createDirectoryAndFiles()
	
	return render( request, 'invoke.html' )


def getContentOfFile( request ):
	''''''
	folderName = request.GET[ 'Folder Name' ] 
	fileName   = request.GET[ 'File Name' ]

	obj 	   = FindContentForFile( STORAGE_DIR, folderName, fileName )
	message    = obj.getFileContent()

	return render( request, 'message.html', { 'message' : message } )


def getListOfAllFiles( request ):

	obj               = FindContentForAll( STORAGE_DIR )
	contentDictList   = obj.getContentForAll()

	context 		  = {}
	context[ 'rows' ] = contentDictList  
	
	return render( request, 'listoffiles.html', context )