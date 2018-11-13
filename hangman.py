import os
from functools import partial

from helper.helper import repeat, pipe
from model.model import init_model
from update import update
from view import view

topics = init_model["topics"]

def setup(model):
    update_topic_partial = partial(update.update_topic, view.get_init(model))
    setup_pipe = pipe(update_topic_partial, update.get_random_topic_ans)
    return setup_pipe(model)


def game_on(model):
    if(model['gameover']):
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    # get new view
    guesses_view = view.get_guesses(model)
    print(guesses_view)
    # get user guess and update state
    model = update.get_update_user_guess(model)
    if model['gameover']:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(view.get_guesses(model))
    game_on(model)


def app(model):
    model = setup(model)
    # get initial view to display current solved answers
    guesses_view = view.get_guesses(model)
    print(guesses_view)
    game_on(model)


def main():
    app(init_model)

if __name__ == "__main__":
    main()
