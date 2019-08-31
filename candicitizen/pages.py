from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import collections, random

class Voting(Page):
    form_model = 'player'
    form_fields = ['ran', 'preference', 'preference2']

    def vars_for_template(self):
        return {
            'candidate_number': self.player.candidate_number,
        }

    timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.ran = False
        if self.player.ran:
            self.player.preference = self.player.candidate_number
        else:
            d = self.player.participant.vars['distances']
            del d[self.player.candidate_number]
            closest = min(d.items(), key=lambda x: x[1])
            del d[closest[0]]
            second_closest = min(d.items(), key=lambda x: x[1])
            self.player.preference = closest[0]
            self.player.preference2 = None
            if closest[1] == second_closest[1] and Constants.second_round:
                self.player.preference2 = second_closest[0]
            elif closest[1] == second_closest[1]:
                if random.random() < 0.5:
                    self.player.preference = second_closest[0]

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # record who ran and count the votes
        votes = collections.Counter()
        self.session.vars['ran'] = []
        self.session.vars['second_round'] = False
        self.session.vars['won_second'] = None
        for p in self.group.get_players():
            if p.ran:
                self.session.vars['ran'].append(p.candidate_number)
            votes[p.preference] += 1
            if p.preference2:
                votes[p.preference2] += 1
        # special case: everyone or no one runs
        if len(self.session.vars['ran']) == Constants.players_per_group \
            or len(self.session.vars['ran']) == 0:
            self.session.vars['won_first'] = random.sample(
                Constants.preferences, 2)
        else:
            # record the winner(s)
            first, second = votes.most_common(2)
            self.session.vars['won_first'] = []
            for p in self.group.get_players():
                if p.candidate_number == first[0]:
                    self.session.vars['won_first'].append(p.candidate_number)
            if first[1] == second[1]:
                self.session.vars['second_round'] = True
                for p in self.group.get_players():
                    if p.candidate_number == second[0]:
                        self.session.vars['won_first'].append(p.candidate_number)       
        # implement the second round
        if self.session.vars['second_round'] and Constants.second_round:
            votes2 = collections.Counter()
            # each player votes again
            for p in self.group.get_players():
                if p.candidate_number in self.session.vars['won_first']:
                    votes2[p.candidate_number] += 1
                else:
                    w = self.session.vars['won_first']
                    d = []
                    d.append((w[0], abs(p.candidate_number - w[0])))
                    d.append((w[1], abs(p.candidate_number - w[1])))
                    d = sorted(d, key=lambda x: x[1])
                    if d[0][1] == d[1][1]: # tie
                        choice = random.choice(d)[0]
                        votes2[choice] += 1
                    else:
                        votes2[d[0][0]] += 1
            self.session.vars['won_second'] = votes2.most_common(1)[0][0]

class Results(Page):
    timeout_seconds = 30
    form_model = 'group'
    form_fields = ['won_first', 'won_second', 'ran', 'second_round']
 
    def vars_for_template(self):
        return {
            'won_first': str(self.session.vars['won_first']),
            'won_second': self.session.vars['won_second'],
            'ran': str(self.session.vars['ran']),
            'second_round': self.session.vars['second_round']
        }

page_sequence = [
    Voting,
    ResultsWaitPage,
    Results
]
