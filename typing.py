"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime
import string


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    a = [x for x in paragraphs if select(x)]
    if k >= len(a):
        return ''
    return a[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(a):
        a = a.translate(str.maketrans('', '', string.punctuation)).split()
        for i in topic:
            for x in a:
                if i == lower(x):
                    return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """

    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed_words) == 0:
        return 0.0
    total = 0
    for typed_word,referenced_word in zip(typed_words,reference_words):
        if typed_word == referenced_word:
            total += 1
    return (total / len(typed_words)) * 100.0
    # END PROBLEM 3

def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return 12 * (len(typed) / elapsed)
    # END PROBLEM 4

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    closest_word = valid_words[0]
    smallest = diff_function(user_word, closest_word, limit)
    for w in valid_words:
        difference = diff_function(user_word, w, limit)
        if difference < smallest:
            smallest = difference
            closest_word = w
    return (closest_word,user_word)[smallest > limit]

def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6

    def diff(start, goal, changed):
        match = 0
        if changed > limit:
            return changed
        if len(start) <= 0 or len(goal) <= 0:
            return max(len(start), len(goal))
        if start[0] != goal[0]:
            match = 1
        return diff(start[1::], goal[1::], changed + match) + match
    return diff(start, goal, 0)

    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if limit < 0 or (len(start) <= 0 or len(goal) <= 0): # Feel free to remove or add additional cases
        return  max(len(start), len(goal))
    elif start[0] == goal[0]:
        return edit_diff(goal[1:], start[1:], limit)
    else:
        add_diff = 1 + edit_diff(goal[0] + start, goal, limit - 1)  # Fill in these lines
        remove_diff = 1 + edit_diff(start[1:], goal, limit - 1)
        substitute_diff = 1 + edit_diff(goal[0] + start[1:] , goal, limit - 1)
        return min(add_diff, remove_diff, substitute_diff)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'

###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    total = 0
    for x, y in zip(typed, prompt):
        if x == y:
            total += 1
        else:
            break
    progress = total / len(prompt)    
    send(dict(id = id, progress = progress))
    return progress

def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0

    a = [[] for _ in range(n_players)]
    for x in range(n_words): 
        myDict = {y: elapsed_time(word_times[y][x+1]) - elapsed_time(word_times[y][x]) for y in range(n_players)}
        min_value =min(myDict.values())
        for i, j in myDict.items():
            if abs(min_value - j) < margin:
                a[i].append(word(word_times[i][x + 1]))
    return a
    
def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)