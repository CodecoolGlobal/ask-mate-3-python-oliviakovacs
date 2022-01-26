from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import connection
import datetime
from bonus_questions import SAMPLE_QUESTIONS
import security


app = Flask(__name__)
app.secret_key = "ask_mate_3"


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        username = request.form['username']
        all_user_names = data_manager.get_user_names()
        if username in all_user_names:
            return render_template('registration.html', new_user=False)
        password = request.form['password']
        hash_password = security.hash_password(password)
        now = datetime.datetime.now()
        data_manager.add_user(username, hash_password, now)
        session["user"] = username
        return redirect(url_for('main_page'))
    return render_template('registration.html', new_user=True)


# ilyen user már van
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        all_users = data_manager.get_user_names()
        for user in all_users:
            if user["name"] == username:
                hashed_password = user["user_password"]
                if security.verify_password(password, hashed_password):
                        session['user'] = username
                        return redirect(url_for("main_page"))
                else:
                    valid_login = False
                    return render_template("login.html", valid_login=valid_login)
    return render_template("login.html", valid_login=True)


@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        search = request.form['search']
        return search
    if "user" in session:
        user = session["user"]
        all_questions = data_manager.get_latest_questions()
        return render_template('main.html', questions=all_questions, logged_in=True)

    all_questions = data_manager.get_latest_questions()
    return render_template('main.html', questions=all_questions, logged_in=False)


@app.route("/list", methods=['GET'])
def list_page():
    if "user" in session:
        if request.args:
            order = request.args['order-by']
            direction = request.args['direction']
            data = data_manager.get_questions(order, direction)
            headers = data_manager.get_question_headers()
            return render_template('list.html', questions=data, headers=headers, logged_in=True)
        data = data_manager.get_questions('submission_time', 'DESC')
        headers = data_manager.get_question_headers()
        return render_template('list.html', questions=data, headers=headers,logged_in=True)
    if request.args:
        order = request.args['order-by']
        direction = request.args['direction']
        data = data_manager.get_questions(order, direction)
        headers = data_manager.get_question_headers()
        return render_template('list.html', questions=data, headers=headers, logged_in=False)
    data = data_manager.get_questions('submission_time', 'DESC')
    headers = data_manager.get_question_headers()
    return render_template('list.html', questions=data, headers=headers, logged_in=False)


@app.route("/search", methods=['POST'])
def display_search_result():
    search = main_page()
    questions_n_answers = data_manager.get_content_by_search(search)
    if questions_n_answers:
        highlight = f"<mark> {search} </mark>"
        return render_template("search.html", questions_n_answers=questions_n_answers, keyword=search, highlight=highlight)
    else:
        return render_template("error.html")


@app.route("/question/<id>")
def display_question(id):
    if "user" in session:
        question = data_manager.get_question_by_id(id)
        answers = data_manager.get_answers_by_question_id(id)
        question_comments = data_manager.get_question_comment_by_question_id(id)
        answers_comments = data_manager.get_answer_comment_by_question_id(id)
        tags = data_manager.tags_by_question_id(id)
        user = data_manager.get_user_id_by_username(session["user"])
        user_id = user["id"]
        return render_template("question_by_id.html", question=question, answers=answers,\
                               question_comments=question_comments,\
                               answers_comments=answers_comments, id=id, tags=tags, logged_in=True, same_user=user_id)
    question = data_manager.get_question_by_id(id)
    answers = data_manager.get_answers_by_question_id(id)
    question_comments = data_manager.get_question_comment_by_question_id(id)
    answers_comments = data_manager.get_answer_comment_by_question_id(id)
    tags = data_manager.tags_by_question_id(id)
    not_existent_user_id = -1
    return render_template("question_by_id.html", question=question, answers=answers, question_comments=question_comments,\
                           answers_comments=answers_comments, id=id, tags=tags, logged_in=False, user_id=not_existent_user_id)


@app.route("/add-question", methods=["POST", "GET"])
def add_question():
    if "user" in session:
        if request.method == "POST":
            max_id = data_manager.get_question_ids()
            now = datetime.datetime.now()
            new_question=[]
            new_question.append(max_id[0]['maximum'])
            new_question.append(now)
            new_question.append(0)
            new_question.append(0)
            new_question.append(request.form.get("title"))
            new_question.append(request.form.get("message"))
            new_question.append(request.form.get("image"))
            user = session["user"]
            user_id = data_manager.get_user_id_by_username(user)
            new_question.append(user_id["id"])
            data_manager.add_new_question(new_question)
            return redirect('/list')

        question = {'title': '', 'message': ''}
        return render_template("form.html", visible_data=question, route="/add-question", is_question=True)
    return redirect(url_for("main_page"))


@app.route('/question/<question_id>/new-answer', methods=["POST", "GET"])
def add_answer(question_id):
    if "user" in session:
        if request.method == "POST":
            max_id = data_manager.get_question_ids()
            max_answer_id = data_manager.get_answer_ids()
            now = datetime.datetime.now()
            new_answer = []
            new_answer.append(max_answer_id[0]['maximum'])
            new_answer.append(now)
            new_answer.append(0)
            new_answer.append(question_id)
            new_answer.append(request.form.get("message"))
            new_answer.append(request.form.get("image"))
            user = session["user"]
            user_id = data_manager.get_user_id_by_username(user)
            new_answer.append(user_id["id"])
            data_manager.add_new_answer(new_answer)
            return redirect(f"/question/{question_id}")
        question = {'title': '', 'message': ''}
        return render_template("form.html", visible_data=question, route=f"/question/{question_id}/new-answer", is_question=False)
    return redirect(url_for("main_page"))


@app.route('/question/<question_id>/new-comment', methods=["POST", "GET"])
def add_comment_to_question(question_id):
    if "user" in session:
        if request.method == "POST":
            now = datetime.datetime.now()
            new_comment = []
            new_comment.append(now)
            new_comment.append(question_id)
            new_comment.append(request.form.get("message"))
            user = session["user"]
            user_id = data_manager.get_user_id_by_username(user)
            new_comment.append(user_id["id"])
            data_manager.add_new_comment_to_question(new_comment)
            return redirect(url_for("display_question", id=question_id))
        comment = {'title': '', 'message': ''}
        return render_template("comment.html", visible_data=comment, route=f"/question/{question_id}/new-comment")
    return redirect(url_for("main_page"))


@app.route('/answer/<answer_id>/new-comment', methods=["POST", "GET"])
def add_comment_to_answer(answer_id):
    if "user" in session:
        if request.method == "POST":
            question_id = data_manager.get_question_id_by_answer(answer_id)
            question_id = question_id['question_id']
            now = datetime.datetime.now()
            new_comment = []
            new_comment.append(now)
            new_comment.append(answer_id)
            new_comment.append(request.form.get("message"))
            user = session["user"]
            user_id = data_manager.get_user_id_by_username(user)
            new_comment.append(user_id["id"])
            data_manager.add_new_comment_to_answer(new_comment)
            return redirect(url_for("display_question", id=question_id))
        comment = {'title': '', 'message': ''}
        return render_template("comment.html", visible_data=comment, route=f"/answer/{answer_id}/new-comment")
    return redirect(url_for("main_page"))


@app.route('/question/<id>/delete', methods=["GET"])
def delete_question(id):
    question = data_manager.get_question_by_id(id)
    if "user" in session:
        user = session["user"]
        question_user = data_manager.get_user_id_by_username(user)
        user_id = question_user["id"]
        for data in question:
            q_user_id = data["user_id"]
        if int(user_id) == int(q_user_id):
            data_manager.delete_question_by_id(id)
    return redirect("/list")


# erre is
@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def edit_question(question_id):
    if request.method == "POST":
        pic = request.form["edit_question_pic"]
        question = request.form["question_title"]
        message = request.form["question_message"]
        data_manager.edit_question(question_id, question, message, pic)
        return redirect(url_for("display_question", id=question_id))
    question = data_manager.get_question_by_id(question_id)
    return render_template("edit_question.html", question=question, q_id=question_id)


# erre is
@app.route('/answer/<answer_id>/edit', methods=["POST", "GET"])
def edit_answer(answer_id):
    if request.method == "POST":
        message = request.form["answer_message"]
        pic = request.form["edit_image"]
        answer = data_manager.edit_answer(answer_id, message, pic)
        question_id = answer['question_id']
        return redirect(url_for("display_question", id=question_id))
    answer = data_manager.get_answer_by_id(answer_id)
    return render_template("edit_answer.html", answer=answer, a_id=answer_id)


# erre is
@app.route('/answer/<answer_id>/delete', methods=["POST", "GET"])
def delete_answer(answer_id):
    return_question_id = data_manager.delete_answer_by_id(answer_id)
    return redirect("/question/" + str(return_question_id['question_id']))


# erre is
@app.route('/comment/<id>/<comment_id>/delete', methods=["POST", "GET"])
def delete_comment(id, comment_id):
    data_manager.delete_comment_by_id(comment_id)
    return redirect(url_for("display_question", id=id))


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    change = 1
    data_manager.change_vote_by_id(["question", question_id,  change, "id"])
    return redirect(url_for("display_question", id=question_id))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    change = -1
    data_manager.change_vote_by_id(["question", question_id,  change, "id"])
    return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<id>/vote_up')
def vote_up_answer(id):
    change = 1
    question_id = data_manager.get_question_id_by_answer(id)
    question_id = question_id['question_id']
    data_manager.change_vote_by_id(["answer", id, change, "id"])
    return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<id>/vote_down')
def vote_down_answer(id):
    change = -1
    question_id = data_manager.get_question_id_by_answer(id)
    question_id = question_id['question_id']
    data_manager.change_vote_by_id(["answer", id, change, "id"])
    return redirect(url_for("display_question", id=question_id))


# erre rá kell nézni
@app.route('/question/pics/<link>')
def giv_pics_to_question(link):
    header = connection.DATA_HEADER_QUESTION
    data = data_manager.get_selected_data("question")
    question_with_pics = data_manager.give_pics(link, data)
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, question_with_pics, header)
    default_sort_data = data_manager.sort(data)
    return render_template('ask_mate_1/list.html', questions=default_sort_data)


# erre is
@app.route('/answer/pics/<link>')
def giv_pics_to_answer(link):
    header = connection.DATA_HEADER_ANSWER
    data = data_manager.get_selected_data("answer")
    answer_with_pics = data_manager.give_pics(link, data)
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, answer_with_pics, header)
    default_sort_data = data_manager.sort(data)
    return render_template('ask_mate_1/list.html', questions=default_sort_data)


# erre is
@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == "POST":
        now = datetime.datetime.now()
        message = request.form["comment_message"]
        comment = data_manager.edit_comment(comment_id, message, now)
        question_id = comment['question_id']
        return redirect(url_for("display_question", id=question_id))
    comment = data_manager.get_comment_by_id(comment_id)
    return render_template("edit_comment.html", comment=comment, c_id=comment_id)


@app.route('/question/<question_id>/new-tag', methods=["POST", "GET"])
def give_tag(question_id):
    if request.method == "POST":
        tag_name = request.form.get("new_tag")
        tag_exist= data_manager.select_tag_id_by_tag_name(tag_name)
        if not tag_exist:
            tag_id = data_manager.make_new_tag(tag_name)
            data = [question_id, tag_id['id']]
            data_manager.pairing_tag_with_question(data)
            return redirect(url_for("display_question", id=question_id))
        tag_in_question = data_manager.tag_in_question_or_not(tag_exist["id"], question_id)
        if not tag_in_question:
            data = [question_id, tag_exist["id"]]
            data_manager.pairing_tag_with_question(data)
        return redirect(url_for("display_question", id=question_id))
    else:
        tags_for_listing = data_manager.all_tag()
        return render_template("adding_tag.html", question_id=question_id, tags=tags_for_listing)


@app.route('/question/<question_id>/select-tag')
def give_tag_with_select(question_id):
    tag_name=request.args['tag_name']
    tag_id = data_manager.select_tag_id_by_tag_name(tag_name)
    exist_in_question = data_manager.tag_in_question_or_not(tag_id["id"], question_id)
    if not exist_in_question:
        data = [question_id, tag_id["id"]]
        data_manager.pairing_tag_with_question(data)
    return redirect(url_for("display_question", id=question_id))


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag_from_question(question_id, tag_id):
    data_manager.delete_tag_from_question(question_id, tag_id)
    return redirect(url_for("display_question", id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5001
    )
