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
    deviation = data['deviation']
    time = data['time']
    note_count = data['note_count']

    allowed_data_names = ['rock', 'pop', 'funk']
    msg = ''

    # Проверка наличия значений для всех пропсов
    if data_name is None or count is None or deviation is None or time is None or note_count is None:
        msg = 'Все поля обязательные!'

    if data_name not in allowed_data_names:
        msg = 'Некорректное значение для "Модели". Разрешенные значения: rock, pop, funk'

    if count is not None and (count < 1 or count > 10):
        msg = 'Некорректное значение для "Кол-ва треков". Допустимый диапазон: от 1 до 10'

    if deviation is not None and (deviation < -2 or deviation > 2):
        msg = 'Некорректное значение для "Отклонения". Допустимый диапазон: от -2 до 2'

    if time is not None and (time < 45 or time > 360):
        msg = 'Некорректное значение для "Скорости трека". Допустимый диапазон: от 45 до 360'

    if note_count is not None and (note_count < 10 or note_count > 200):
        msg = 'Некорректное значение для "Длины трека". Допустимый диапазон: от 10 до 200'

    if msg == '':
        files = create_files(data_name, count, deviation, time, note_count)

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
