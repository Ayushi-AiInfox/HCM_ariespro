from waitress import serve

from globalworkforcemanagement.wsgi import application
# documentation: https://docs.pylonsproject.org/projects/waitress/en/stable/api.html

if __name__ == '__main__':
    
    serve(application, host = '10.0.0.5', port='8080')