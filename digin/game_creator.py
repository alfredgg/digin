#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import math
from random import random

RATIO_ERRORS = 0.4
RATIO_TIMES = 0.2
RATIO_LASTTIME = 0.4

L_RANGE = 0.1
R_RANGE = 0.9


def get_key2sort(q):
    return q[1]


# TODO: a cache of this function can be easily developed using a decorator
def log_values_for(nelements):
    # we apply margins, this way probabilities are not extreme (really bigger or really smaller values)
    l_margin, r_margin = (nelements*L_RANGE), (nelements*R_RANGE)
    probabilities = [-math.log((x+l_margin)/float(nelements+r_margin)) for x in xrange(nelements)]
    # normalize the probabilities
    return [x/sum(probabilities) for x in probabilities]


def probability_by_position(the_list, direct=False):
    '''
    :param the_list: list of (id, value) pairs
    :param direct: True = bigger value gets more probability. False = smaller value gets more probability.
    :return:
    '''
    # first elements in the list obtain bigger probabilities
    elements = sorted(the_list, key=get_key2sort)[::-1] if direct else sorted(the_list, key=get_key2sort)
    probabilities = log_values_for(len(elements))
    # assign each probability to each id
    return {k[0]: probabilities[i] for i, k in enumerate(elements)}


def ponderate_values(last_times, errors, times):
    '''
    :param last_times:
    :param errors:
    :param times:
    :return: ponderation
    '''
    return (last_times * RATIO_LASTTIME) + (errors * RATIO_ERRORS) + (times * RATIO_TIMES)


def obtain_probabilities(questions):
    print questions
    ids = [q.id for q in questions.query.all()]
    dnow = datetime.now()

    last_times = [(q.id, (dnow - q.last_time).total_seconds()) for q in questions]
    errors = [(q.id, q.error_rate) for q in questions]
    times = [(q.id, q.times) for q in questions]

    plast_times = probability_by_position(last_times, True)
    perrors = probability_by_position(errors, True)
    ptimes = probability_by_position(times, False)

    return [(key, ponderate_values(plast_times[key], perrors[key], ptimes[key])) for key in ids]


def wheel_of_fortune(elems, nchoices):
    selected = []
    while len(selected) < nchoices:
        val = random()
        current = 0
        for e in elems:
            current = current + e[1]
            if val <= current:
                if e[0] not in selected:
                    selected.append(e[0])
                break
    return selected


def extract_questions(questions, nchoices=10):
    probabilities = obtain_probabilities(questions)
    #sorted_probs = sorted(probabilities, key=get_key2sort)
    ids = wheel_of_fortune(probabilities, nchoices)
    ids = [v[0] for v in ids]
    return [q for q in questions if q.id in ids]