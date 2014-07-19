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


def extract_probabilities(the_dict, direct=False):
    '''
    :param the_list:
    :param direct: True = less value gets less probability. False = less value gets more probability.
    :return:
    '''
    non_repeated = set(the_dict.values())
    sorted_values = sorted(non_repeated) if direct else sorted(non_repeated)[::-1]

    nelems = len(sorted_values)
    # logarithm with margin to not assign 1 or 0
    l_margin, r_margin = (nelems*L_RANGE), (nelems*R_RANGE)
    probabilities = [-math.log((x+l_margin)/float(nelems+r_margin)) for x in xrange(nelems)]
    # normalize the logatithm
    probabilities = [x/sum(probabilities) for x in probabilities]
    prob_by_value = {sorted_values[index]: prob for index, prob in enumerate(probabilities)}

    # assign each probability to each id
    return {k: prob_by_value[the_dict[k]] for k in the_dict.keys()}


def final_probability(last_times, errors, times):
    '''
    :param last_times:
    :param errors:
    :param times:
    :return: ponderation
    '''
    return (last_times * RATIO_LASTTIME) + (errors * RATIO_ERRORS) + (errors * RATIO_TIMES)


def obtain_probabilities(questions):
    ids = [q.id for q in questions]
    dnow = datetime.now()

    last_times = {q.id: (dnow - q.last_time).total_seconds() for q in questions}
    errors = {q.id: q.error_rate for q in questions}
    times = {q.id: q.times for q in questions}

    plast_times = extract_probabilities(last_times, False)
    perrors = extract_probabilities(errors, False)
    ptimes = extract_probabilities(times, True)

    return [(key, final_probability(plast_times[key], perrors[key], ptimes[key])) for key in ids]


def rulette_of_fortune(elems, nchoices):
    selected = []
    for _ in xrange(nchoices):
        search = True
        while search:
            val = random()
            current = 0
            for e in elems:
                if current >= val:
                    if e[0] not in selected:
                        selected.append(e[0])
                        search = False
                    break
                else:
                    current = current + e[1]
    return selected


def extract_game(questions, nchoices=10):
    probabilities = obtain_probabilities(questions)
    sorted_probs = sorted(probabilities, key=get_key2sort)
    return rulette_of_fortune(sorted_probs, nchoices)