from django.shortcuts import render
from django.http import  HttpResponse
import os

from .config import JSON_FILE_URL, LOG_FILE_URL, PARENT_DIR
from .utilFunctions import DoProcessing

obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, PARENT_DIR )

def home( request ):
	''''''
	obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, PARENT_DIR )
	return render( request, 'home.html' )

def invokeCreationOfFiles( request ):
	'''''' 
	#if DoProcessing.count == 0 :
	obj.createDirectoryAndFiles()
	
	return render( request, 'invoke.html' )


