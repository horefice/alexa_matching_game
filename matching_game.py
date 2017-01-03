import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import random

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def welcome():
    animals = ['cat','dog','cammel','bird','horse']
    session.attributes['not_machted'] = animals
    answer = list(animals)
    answer += answer
    random.shuffle(answer)
    session.attributes['answer'] = answer
    session.attributes['number_one'] = None
    msg = render_template('welcome')
    return question(msg)

@ask.intent("NumberIntent", convert={'number':int})
def next(number):
    answer = session.attributes['answer']
    number_one = session.attributes['number_one']
    if number_one is None:
        session.attributes['number_one'] = number
        msg = render_template('next', number = number, animal = answer[number])
    else:
        if number == number_one:
            msg = render_template('same')
        else:
            session.attributes['number_one'] = None
            print(answer)
            if answer[number] == answer[number_one]:
                if answer[number] in session.attributes['not_machted']:
                    session.attributes['not_machted'].remove(answer[number])
                if len(session.attributes['not_machted']) == 0:
                    msg = render_template('end', number = number, animal = answer[number])
                    return statement(msg)
                else:
                    msg = render_template('win', number = number, animal = answer[number])
            else:
                msg = render_template('lose', number = number, animal = answer[number])
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)