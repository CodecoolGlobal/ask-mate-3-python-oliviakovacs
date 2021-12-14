import csv
import os

DATA_FILE_PATH_QUESTION = os.getenv('DATA_FILE_PATH_QUESTION') if 'DATA_FILE_PATH_QUESTION' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWER = os.getenv('DATA_FILE_PATH_ANSWER') if 'DATA_FILE_PATH_ANSWER' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTION = ["id","submission_time","view_number","vote_number","title","message","image"]
DATA_HEADER_ANSWER = ["id","submission_time","vote_number","question_id","message","image"]


def get_data(filename):
    final_files = []
    with open(filename) as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',')
        for row in csv_reader:
            final_files.append(row)
    return final_files


def write_data(file_name, data, headers):
    with open(file_name, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)