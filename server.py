from flask import Flask, render_template
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


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
