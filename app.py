#https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cterminal-bash%2Clocal-git-deploy%2Cdeploy-instructions-azportal%2Cdeploy-instructions-zip-azcli#4---browse-to-the-app
#https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    dato = request.form.get('dato')

    if dato:
        print('Request para página de predicción con el dato =%s' % dato)

        #Librerías necesarias para la predicción
        import urllib.request
        import json
        import os
        import ssl

        def allowSelfSignedHttps(allowed):
            if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                ssl._create_default_https_context = ssl._create_unverified_context

        allowSelfSignedHttps(True)
        data =  {
        "Inputs": {
            "WebServiceInput0": [
            {
                "horsepower": dato
            }
            ]
        },
        "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))

        url = 'http://a0873cc3-0637-471f-94f7-909fc125d3fe.eastus.azurecontainer.io/score'
        api_key = 'y9YcBcZIY1QcXc9gXRwmq9NQKSv1nSVl'

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            print(result)
            prediccion = result[74:-4].decode("utf-8")
            print(prediccion)
            
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))

        return render_template('hello.html', prediccion = prediccion, entrada = dato)
    else:
        print('Request para página de predicción sin dato de entrada -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()