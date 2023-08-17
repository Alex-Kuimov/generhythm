from flask import Flask, json, request
from flask_cors import CORS
from gen import create_files

application = Flask(__name__)
CORS(application)
# application.debug = True

application.static_folder = '/out/'

@application.route('/generate/', methods=['POST'])
def generate():
    data = request.json

    data_name = data['data_name']
    count = data['count']

    allowed_data_names = ['rock', 'funk', 'punk', 'jazz']
    msg = ''

    # Проверка наличия значений для всех пропсов
    if data_name is None or count is None:
        msg = 'Все поля обязательные!'

    if data_name not in allowed_data_names:
        msg = 'Некорректное значение для "Модели". Разрешенные значения: rock, pop, funk'

    if count is not None and (count < 1 or count > 10):
        msg = 'Некорректное значение для "Кол-ва треков". Допустимый диапазон: от 1 до 10'

    if msg == '':
        files = create_files(data_name, count)

        response = {
            'files': files,
            'status': 'ok'
        }
    else:
        response = {
            'status': 'err',
            'msg': msg
        }

    return json.dumps(response)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
