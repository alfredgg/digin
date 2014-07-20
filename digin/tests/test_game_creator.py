#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from hamcrest import *
from digin.game_creator import log_values_for, probability_by_position, wheel_of_fortune
from collections import Counter


class TestGameCreator(TestCase):
    def test_log_values_for(self):
        nvalues = 100
        values = log_values_for(nvalues)
        for i in xrange(1, nvalues):
            assert_that(values[i-1], greater_than(values[i]))
        assert_that(values[0], less_than(1))
        assert_that(values[-1], greater_than(0))

    def test_probability_by_position(self):
        values = [(4, 4), (2, 2), (3, 3), (8, 8), (9, 9), (0, 0)]
        # direct
        dprobs = probability_by_position(values, True)
        assert_that(dprobs[4], greater_than(dprobs[3]), greater_than(dprobs[0]))
        assert_that(dprobs[9], greater_than(dprobs[4]))
        # indirect
        dprobs = probability_by_position(values, False)
        assert_that(dprobs[4], less_than(dprobs[3]), less_than(dprobs[0]))
        assert_that(dprobs[9], less_than(dprobs[4]))

    def test_wheel_of_fortune(self):
        ntests = 15000
        nsubs = 2
        elements = [('first', 0.25), ('second', 0.05), ('third', 0.6), ('fourth', 0.1)]
        values = []
        for _ in xrange(ntests):
            values.extend(wheel_of_fortune(elements, nsubs))
        frequency = Counter(values)
        for k in frequency.keys():
            frequency[k] = float(frequency[k]) / (ntests * nsubs)
        for e in elements:
            p, v = frequency[e[0]], e[1]
            assert_that(p, close_to(v, 0.2))