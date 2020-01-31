Screenshots show the json response of the 3 APIs used in this project. Please note that when an error is thrown, different response code is returned(other than 200) based on the type of error. 

To get the json response on Postman as shown in the screenshots in this folder, comment out all lines of code with 'render' in Processing/views.py except in home function and uncomment all lines of code with 'JSonResponse' in it.

'Render' returns a dictionary which is used in Django Template Language for the UI and postman can't show it as a json response. However, when Render is used, HTML page with rendered content is visible. 

The documentation of these APIs is stored in REST API Documentation/Swagger/swagger.json.