import connection
import time


def sort(filename, type="submission_time", order="descending"):
    data = connection.get_data(filename)
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[i][type].isnumeric() and int(data[i][type]) > int(data[j][type]):
                data[i], data[j] = data[j], data[i]
            elif data[i][type] > data[j][type]:
                data[i], data[j] = data[j], data[i]
    if order == "descending":
        return data
    return data[::-1]


def get_question_by_id(id):
    questions = connection.get_data(connection.DATA_FILE_PATH_QUESTION)
    for question in questions:
        if question["id"] == id:
            return question


def get_answers_by_question_id(question_id):
    answers = connection.get_data(connection.DATA_FILE_PATH_ANSWER)
    question_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            question_answers.append(answer)
    return question_answers


def create_new_data(headers, file):
    file_list = connection.get_data(file)
    ids = []
    for file in file_list:
        ids.append(file["id"])
    new_data = {}
    for header in headers:
        if header == "id":
            new_data.update({"id": max(ids) + 1})
        if header == "submission_time":
            new_data.update({"submission_time": time.time()})
        if header == "vote_number":
            new_data.update({"vote_number": 0})
        if header == "view_number":
            new_data.update({"view_number": 0})
    return new_data


def delete_by_id(filename, index, key):
    finale_file = []
    for row in filename:
        if row[key] != index:
            finale_file.append(row)
    return finale_file



