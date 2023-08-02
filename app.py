from flask import Flask, json, request
from gen import gen

application = Flask(__name__)
# application.debug = True

@application.route('/generate/', methods=['POST'])
def generate():
    data = request.json

    style = data['style']
    count = data['count']

    files = gen(style, count)

    response = {
        'files': files
    }

    return json.dumps(response)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
