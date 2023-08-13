import re
from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from



app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = {
    'swagger': '2.0',
    'info' : {
        'description' :  'API Documentation for Data Processing and Modeling',
        'title' : 'Dokumentasi API untuk data processing dan modelling',
        'version' : '1.0.0'
        
    }

}
swagger_config = {
    'headers' : [],
    'specs' : [
        {
            'endpoint' : 'docs',
            'route' : '/docs.json'
        }
    ],
    'static_url_path' :'/flasgger_statis',
    'swagger_ui' :True,
    'specs_route' : '/docs/' # kenapa pake router tidak bisa jalan, sedangkan route jalan?

}

swagger = Swagger(app, config=swagger_config,template=swagger_template)
@swag_from("./docs/hello_world.yml", methods=['GET'])

@app.route('/', methods = ['GET'])
def call_hello_world():
    json_response = {
        'status_code': 200,
        'description': 'Menyapa Hello World',
        'data' : 'Hello World'
    }

    response_data = jsonify(json_response)
    return response_data

@app.route('/text', methods = ['GET'])
@swag_from("./docs/hello_world.yml", methods=['GET'])
def text ():
    json_response = {
        'status_code': 200,
        'description': 'Original teks',
        'data' : 'Hello World, Baik-baik saja?'
    }
    respons_data = jsonify(json_response)
    return respons_data

@app.route('/text-clean', methods=['POST'])
@swag_from("./docs/text_clean.yml", methods=['POST'])
def text_clean():
    if request.method == 'POST':
        text = request.args.get('text')
        if text:
            cleaned_text = re.sub(r'[^a-zA-Z]', ' ','text')
            json_response = {
                'status_code': 200,
                'description': 'Cleaned text',
                'data': cleaned_text
            }
            return jsonify(json_response)
        else:
            return jsonify({'error': 'No text provided'}), 400
    else:
        return jsonify({'error': 'Invalid request method'}), 405


                               

if __name__ == '__main__':
    app.run()