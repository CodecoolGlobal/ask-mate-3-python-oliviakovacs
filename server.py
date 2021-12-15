from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main_page():
    data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    return render_template('list.html', questions=data)


# @app.route("/question")
@app.route("/question/<id>")
def display_question(id):
    question = data_manager.get_question_by_id(id)
    answers = data_manager.get_answers_by_question_id(id)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        data_manager.add_new_content(connection.DATA_FILE_PATH_QUESTION, connection.DATA_HEADER_QUESTION)
        return redirect("/list")
    question = {'title': '', 'message': ''}
    return render_template("form.html", visible_data=question, route="/add-question")


@app.route('/question/<question_id>/new-answer')
def add_answer():
    pass


@app.route('/question/<id>/delete', methods=["GET"])
def delete_question(id):
    old_data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    header = connection.DATA_HEADER_QUESTION
    data = data_manager.delete_by_id(old_data, id, "id")
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, data, header)
    old_answers = data_manager.sort(connection.DATA_FILE_PATH_ANSWER)
    answer = data_manager.delete_by_id(old_answers, id, "question_id")
    connection.write_data(connection.DATA_FILE_PATH_ANSWER, answer, header)
    return redirect("/list")


@app.route('/question/<question_id>/edit')
def edit_question():
    pass


@app.route('/answer/<answer_id>/delete')
def delete_answer():
    pass


@app.route('/question/<question_id>/vote_up')
def vote_up_question():
    pass


@app.route('/question/<question_id>/vote_down')
def vote_down_question():
    pass


@app.route('/answer/<question_id>/vote_up')
def vote_up_answer():
    pass


@app.route('/answer/<question_id>/vote_down')
def vote_down_answer():
    pass


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000
    )
