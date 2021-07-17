from flask import Flask, request, render_template
from module_outputs import get_question,correct_answer
import json

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

    # Read from cache
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    qid = cache['qid']
    question = cache['question']
    answer = cache['answer']
    correction = cache['correction']

    if 'qid' in request.form:

        # QUESTION GENERATION
        try:
            qid = request.form['qid']
            question_text, identifier_info, formula_info = get_question(qid)
            question = question_text
        except:
            qid = ''
            question = ''

    if 'answer' in request.form:

        # ANSWER CORRECTION
        try:
            answer = request.form['answer']
            question_text, identifier_info, formula_info = get_question(qid)
            value_correct, unit_correct = correct_answer(identifier_info, formula_info, answer)
            correction = value_correct, unit_correct

        except:
            answer = ''
            correction = ''

    # Write to cache
    cache['qid'] = qid
    cache['question'] = question
    cache['answer'] = answer
    cache['correction'] = correction
    with open('cache.json', 'w') as f:
        json.dump(cache,f)

    return render_template('my-form.html',qid=qid,question=question,answer=answer,correction=correction)

if __name__ == '__main__':
    app.run(debug=True)