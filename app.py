from flask import Flask, request, render_template

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

    qid = ''
    question = ''

    qid = request.form['qid']
    #question = request.form['question']

    return render_template('my-form.html',qid=qid,question=qid)

if __name__ == '__main__':
    app.run(debug=True)