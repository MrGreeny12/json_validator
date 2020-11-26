import json
import os
from jsonschema import Draft4Validator


def json_validate(file_json, schema, file_logs):
    '''
    :param file: путь к файлу json
    :param schema: путь к схеме json
    :param file_logs: путь к файлу с логами.
    :return: записывает ошибки в файл txt в виде лога
    '''
    with open(file_json, "r") as read_file:
        obj_json = json.load(read_file)
    with open(schema, "r") as read_file:
        obj_schema = json.load(read_file)
    v = Draft4Validator(obj_schema)
    with open(file_logs, 'a') as log:
        log.write(f'\nJson-файл: {file_json}\nJson-schema: {schema}\n\n\n')
        for error in sorted(v.iter_errors(obj_json), key=str):
            log.write(f'Ошибка: {error.message} \n')
        print(f'Логи файла {file_json} созданы успешно!')


def validate_folder(json_folder, schema_folder, file_logs):
    '''
    :param json_folder: папка с json-файлами
    :param schema_folder: папка с json-схемами
    :param file_logs: название файла, куда будут писаться логи
    :return: проверяет сразу несколько json-файлов на основе схем
    '''
    list_json = os.listdir(json_folder)
    list_schema = os.listdir(schema_folder)
    for schema in list_schema:
        for json_file in list_json:
            full_path_sc = schema_folder + '/' + schema
            full_path_js = json_folder + '/' + json_file
            json_validate(full_path_js, full_path_sc, file_logs=file_logs)
    print('Все логи созданы успешно!')


if __name__ == '__main__':
    #пример с проверкой 1-го файла по 1-й схеме
    json_validate('event/1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3.json', 'schema/label_selected.schema', 'logs.txt')
    #пример с проверкой множества файлов по множеству схем
    validate_folder('event', 'schema', 'logs_1.txt')