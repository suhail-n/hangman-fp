import random
import re

from functools import partial

from helper.helper import repeat, pipe
from model.model import init_model

topics = {
    "movies": ['FIGHT CLUB', 'INCEPTION', 'THE MATRIX']
}

# update topic
is_topic = lambda topic: not not list(filter(lambda t: topic.lower() == t.lower(), init_model['topics']))
get_topic_input = lambda msg: input(msg)
get_topic = lambda msg: repeat(lambda: get_topic_input(msg), is_topic)
update_topic = lambda msg, model: {**model, "current_topic": get_topic(msg)()}

# get random topic ans
set_correct_ans = lambda model: {**model, "correct_guesses": re.sub("\S", "_", model['current_topic_ans'])}
get_random_topic = lambda model: {**model, "current_topic_ans": random.choice(topics[model['current_topic'].lower()])}
# arg: model
get_random_topic_ans = pipe(get_random_topic, set_correct_ans)

# get user guesses
verify_user_guess = lambda model, arg: arg not in model['guesses']
get_user_guess = lambda model: {**model, "current_guess": repeat(lambda: input("Enter a letter: "), partial(verify_user_guess, model))()}


# update user guesses
def update_user_guess(model):
    model = {**model}
    model['guesses'].append(model['current_guess'])
    # get all indexes of guess in answer
    found = [i for i, c in enumerate(model['current_topic_ans']) if c.upper() == model['current_guess'].upper()]
    if not found:
        model['fails'] += 1
    else:
        # update correct guesses  
        correct_guesses = list(model['correct_guesses'])
        for i in found:
            correct_guesses[i] = model['current_guess'].upper()
        model['correct_guesses'] = "".join(correct_guesses)
    # check if game over
    if model['current_topic_ans'].upper() == model['correct_guesses'] or model['fails'] >= 5:
        model['gameover'] = True
    return model

# arg: model
get_update_user_guess = pipe(get_user_guess, update_user_guess)