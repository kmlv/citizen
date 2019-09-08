from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):

        TEST_CASES = [
            {15: False, 30: False, 50: True, 70: False, 95: False, 's': False, 'n': [50], 'w': 50},
            {15: True, 30: False, 50: True, 70: False, 95: True, 's': True, 'n': [15,50]},
            {15: True, 30: True, 50: False, 70: False, 95: True, 's': True, 'n': [30,95], 'w': 30},
            {15: False, 30: True, 50: True, 70: True, 95: True, 's': True, 'n':[30]},
            {15: False, 30: True, 50: False, 70: True, 95: True, 's': True, 'n': [30,70]},
            {15: False, 30: False, 50: True, 70: False, 95: False, 'n': [50], 'w': 50},
            {15: True, 30: True, 50: False, 70: True, 95: False, 'n': [70], 'w': 70},
            {15: False, 30: True, 50: True, 70: True, 95: True, 'n': [30], 'w': 30},
            {15: True, 30: False, 50: False, 70: False, 95: True, 'n': [15], 'w': 15},
            {15: False, 30: True, 50: False, 70: False, 95: True, 'n': [30], 'w': 30},
        ]

        if self.round_number == 1:
            yield (pages.Introduction)
        
        ran = TEST_CASES[self.round_number - 1][self.player.candidate_number]
        yield (pages.Voting, {
            'ran': ran,
        })
       
        print(self.round_number)
        case = TEST_CASES[self.round_number - 1]
        if 'n' in case:
            for num in case['n']:
                assert(num in self.session.vars['nominees'])
        if 'w' in case:
            assert(case['w'] == self.session.vars['winner'])
            assert(self.session.vars['winner'] in self.session.vars['nominees'])
        if 's' in case:
            assert(case['s'] == self.session.vars['second_round'])
        yield (pages.Results)
        if self.subsession.round_number == Constants.num_rounds:
            yield (pages.FinalResults)

