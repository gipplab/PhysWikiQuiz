from flask import Flask, request, render_template
from module_outputs import get_question,correct_answer

#Flask forms tutorial:
#https://web.itu.edu.tr/uyar/fad/forms.html

#https://www.w3schools.com/tags/tag_label.asp

#MathQA (template)
#https://github.com/ag-gipp/MathQA
#https://github.com/askplatypus/platypus-ui

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():

    # QID QUERY
    qid = ''
    try:
        qid = request.form['qid']
    except:
        pass

    # QUESTION GENERATION
    question = ''
    identifier_info = None
    formula_info = None
    try:
        qid = request.form['qid']
        question_text, identifier_info, formula_info = get_question(qid)
        question = question_text
    except:
        pass

    # ANSWER QUERY
    answer = ''
    try:
        answer = request.form['answer']
    except:
        pass

    # ANSWER CORRECTION
    correction = ''
    if len(answer) != 0:
        try:
            value_correct, unit_correct = correct_answer(identifier_info, formula_info, answer)
            correction = value_correct, unit_correct
        except:
            pass

    return render_template('my-form.html',qid=qid,question=question,
                           identifier_info=identifier_info,formula_info=formula_info,
                           answer=answer,correction=correction)

if __name__ == '__main__':
    app.run(debug=True)