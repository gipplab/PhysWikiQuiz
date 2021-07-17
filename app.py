from flask import Flask, request, render_template
from module_outputs import generate_question,correct_answer
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

    # Init variables
    qid = ''
    answer = ''
    correction = ''

    # Read from cache
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    question = cache['question']

    if 'qid' in request.form and cache['question_generated']==False:

        # QUESTION GENERATION
        try:
            qid = request.form['qid']
            question_text, identifier_info, formula_info = generate_question(qid)
            cache['correct_value'] = str(identifier_info[0])
            cache['correct_unit'] = formula_info
            question = question_text
            cache['question_generated'] = True
        except:
            pass

    if 'answer' in request.form and cache['question_generated']==True:

        # ANSWER CORRECTION
        try:
            answer = request.form['answer']
            value_correct, unit_correct = correct_answer(cache['correct_value'],cache['correct_unit'],answer)
            #correction = value_correct, unit_correct
            correction = 'Value answer correct: ' + str(value_correct) + ", " + 'Unit answer correct: ' + str(unit_correct)
            cache['question_generated'] = False

        except:
            pass

    # Write to cache
    cache['question'] = question
    with open('cache.json', 'w') as f:
        json.dump(cache,f)

    return render_template('my-form.html',qid=qid,question=question,answer=answer,correction=correction)

if __name__ == '__main__':
    app.run(debug=True)