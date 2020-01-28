from django.shortcuts import render
from django.http import  HttpResponse
import os

from .config import JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR
from .util_functions import DoProcessing, FindContentForFile, FindContentForAll


def home( request ):
	''' Returns html page for home page '''

	obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	return render( request, 'home.html' )


def invokeCreationOfFiles( request ):
	''' Returns html page for storing files and invokes the operation of creating files ''' 

	obj   = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	error = obj.createDirectoryAndFiles()
	
	if error :
		return render( request, 'error.html' )
	
	return render( request, 'invoke.html' )


def getContentOfFile( request ):
	''' Returns html page to show the content of a file '''

	folderName 		   = request.GET[ 'Folder Name' ] 
	fileName   		   = request.GET[ 'File Name' ]

	obj 	   		   = FindContentForFile( STORAGE_DIR, folderName, fileName )
	( error, message ) = obj.getFileContent()

	if error :
		return render( request, 'wrongname.html' )

	message.replace( '/\n/g', "<br/>" )	
	return render( request, 'message.html', { 'message' : message } )


def getListOfAllFiles( request ):
	''' Returns html page for showing list of all the files present in storage '''

	obj               = FindContentForAll( STORAGE_DIR )
	contentDictList   = obj.getContentForAll()

	context 		  = {}
	context[ 'rows' ] = contentDictList  
	
	if len( contentDictList ) == 0 : 
		return render( request, 'empty.html' )
	
	return render( request, 'listoffiles.html', context )