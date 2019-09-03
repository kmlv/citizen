from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import collections, random

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Voting(Page):
    form_model = 'player'
    form_fields = ['ran', 'preference', 'preference2']

    def vars_for_template(self):
        return {
            'candidate_number': self.player.candidate_number,
        }

    timeout_seconds = 30

    def before_next_page(self):
        # each player votes
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
            if closest[1] == second_closest[1] and self.session.config['second_round_toggle']:
                self.player.preference2 = second_closest[0]
            elif closest[1] == second_closest[1]:
                if random.random() < 0.5:
                    self.player.preference = second_closest[0]

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        votes = collections.Counter() # data structure for holding votes
        self.session.vars['ran'] = [] # list storing who ran
        self.session.vars['nominees'] = [] # list storing winners of first round
        self.session.vars['second_round'] = False # boolean storing whether a second_round occurred
        self.session.vars['winner'] = None # candidate_number of the winner
        
        # record who ran and count votes
        for p in self.group.get_players():
            if p.ran:
                self.session.vars['ran'].append(p.candidate_number)
            votes[p.preference] += 1
            if p.preference2:
                votes[p.preference2] += 1
        
        # Create list of nominees
        # special case: everyone runs
        if len(self.session.vars['ran']) == Constants.players_per_group:
            self.session.vars['nominees'] = random.sample(
                Constants.preferences, 2)
        # special case: no one runs
        elif len(self.session.vars['ran']) == 0:
            self.session.vars['nominees'] = random.sample(
                Constants.preferences, 1)
        # 2-4 people run 
        else:
            first, second = votes.most_common(2)
            for p in self.group.get_players():
                if p.candidate_number == first[0]:
                    self.session.vars['nominees'].append(p.candidate_number)
            if first[1] == second[1]:
                for p in self.group.get_players():
                    if p.candidate_number == second[0]:
                        self.session.vars['nominees'].append(p.candidate_number)       
        
        # Determine winner
        # 1 nominee
        if len(self.session.vars['nominees']) == 1:
            self.session.vars['winner'] = self.session.vars['nominees'][0]
        # 2 nominees and second round
        elif len(self.session.vars['nominees']) > 1 and self.session.vars['second_round_toggle']:
            votes2 = collections.Counter()
            # each player votes again
            for p in self.group.get_players():
                if p.candidate_number in self.session.vars['nominees']:
                    votes2[p.candidate_number] += 1
                else:
                    w = self.session.vars['nominees']
                    d = []
                    d.append((w[0], abs(p.candidate_number - w[0])))
                    d.append((w[1], abs(p.candidate_number - w[1])))
                    d = sorted(d, key=lambda x: x[1])
                    if d[0][1] == d[1][1]: # tie
                        choice = random.choice(d)[0]
                        votes2[choice] += 1
                    else:
                        votes2[d[0][0]] += 1
            self.session.vars['winner'] = votes2.most_common(1)[0][0]
            self.session.vars['second_round'] = True
        # 2 nominees, no second round
        else:
            self.session.vars['winner'] = random.choice(
                self.session.vars['nominees'])

class Results(Page):
    timeout_seconds = 30
    form_model = 'group'
    form_fields = ['nominees', 'winner', 'ran', 'second_round']
 
    def vars_for_template(self):
        self.player.set_payoffs()
        return {
            'nominees': str(self.session.vars['nominees']),
            'winner': self.session.vars['winner'],
            'ran': str(self.session.vars['ran']),
            'second_round': self.session.vars['second_round'],
        }

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        chosen_round = random.randint(1, 10)
        payout = self.player.in_round(chosen_round).payoff
        return {
            'payout': payout,
        }

page_sequence = [
    Introduction,
    Voting,
    ResultsWaitPage,
    Results,
    FinalResults,
]
