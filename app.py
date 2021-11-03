from flask import Flask, request, render_template
from module_outputs import generate_question,correct_answer
import json

#Flask forms tutorial:
#https://web.itu.edu.tr/uyar/fad/forms.html

#TODO: multilinguality employing Wikidata
#TODO: teacher and student login and question distribution:
#https://www.digitalocean.com/community/tutorials/
# how-to-add-authentication-to-your-app-with-flask-login-de
# https://hackersandslackers.com/flask-login-user-authentication/
# https://medium.com/analytics-vidhya/creating-login-page-on-flask-9d20738d9f42

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():

    # Init variables
    concept = ''
    answer = ''
    correction = ''
    explanation = ''

    # Read from cache
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    concept = cache['concept']
    question = cache['question']

    if 'concept' in request.form:# and cache['question_generated']==False:

        # QUESTION GENERATION
        try:
            concept = request.form['concept']
            question = 'Unknown error'
            question_text, identifier_info, formula_info, explanation = generate_question(concept)
            question = question_text
            cache['correct_value'] = str(identifier_info[0])
            cache['correct_unit'] = formula_info
            cache['explanation'] = explanation
            explanation = ''
            cache['question_generated'] = True
        except:
            pass
            #question = 'Question could not be generated'

    if 'answer' in request.form:# and cache['question_generated']==True:

        # ANSWER CORRECTION
        try:
            answer = request.form['answer']
            value_correct, unit_correct = correct_answer(cache['correct_value'],cache['correct_unit'],answer)
            # Set correction text
            # correction = value_correct, unit_correct
            # correction = 'Value answer correct: ' + str(value_correct) + ", " + 'Unit answer correct: ' + str(unit_correct)
            value_prefix = 'Value '
            unit_prefix = 'Unit '
            if value_correct:
                value_suffix = 'correct!'
            elif not value_correct:
                value_suffix = 'incorrect!'
            if unit_correct:
                unit_suffix = 'correct!'
            elif not unit_correct:
                unit_suffix = 'incorrect!'
            value_text = value_prefix + value_suffix
            unit_text = unit_prefix + unit_suffix
            # TODO: add references (defining formula,Wikidata item, Wikipedia URL) to correction text
            explanation = cache['explanation']
            correction = ' '.join([value_text,unit_text])
            # No question given
            if not '=' in question:
                correction = 'No question given'
                explanation = ''
            # Wrong format
            if len(answer.split()) < 2:
                correction = 'Please input value AND unit (space-separated)!'
                explanation = ''
            cache['question_generated'] = False

        except:
            pass

    # Write to cache
    cache['concept'] = concept
    cache['question'] = question
    with open('cache.json', 'w') as f:
        json.dump(cache,f)

    return render_template('my-form.html',concept=concept,question=question,answer=answer,correction=correction,explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')