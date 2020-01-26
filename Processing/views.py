from django.shortcuts import render
from django.http import  HttpResponse
import os

from .config import JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR
from .util_functions import DoProcessing

obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )

def home( request ):
	''''''
	obj = DoProcessing( JSON_FILE_URL, LOG_FILE_URL, STORAGE_DIR )
	return render( request, 'home.html' )

def invokeCreationOfFiles( request ):
	'''''' 
	#if DoProcessing.count == 0 :
	obj.createDirectoryAndFiles()
	
	return render( request, 'invoke.html' )


