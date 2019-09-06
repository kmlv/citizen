from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import collections, random

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Voting(Page):
    form_model = 'player'
    form_fields = ['ran']

    def vars_for_template(self):
        # distance to each other for this given round
        self.player.participant.vars['distances'] = {d:
            abs(self.player.candidate_number - d) for d in Constants.preferences}
        return {
            'candidate_number': self.player.candidate_number,
        }

    timeout_seconds = 60

    def before_next_page(self):
        # each player votes
        if self.timeout_happened:
            self.player.ran = False
        if self.player.ran:
            self.player.preference = self.player.candidate_number

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        votes = collections.Counter() # data structure for holding votes
        for p in Constants.preferences:
            votes[p] = 0
        self.session.vars['ran'] = [] # list storing who ran
        self.session.vars['nominees'] = [] # list storing winners of first round
        self.session.vars['second_round'] = False # boolean storing whether a second_round occurred
        self.session.vars['winner'] = None # candidate_number of the winner
        
        # record who ran and count votes. Since counters only hold ints,
        # we double the count of each vote
        for p in self.group.get_players():
            if p.ran:
                self.session.vars['ran'].append(p.candidate_number)
        
        # Create list of nominees
        # special case: everyone runs
        if len(self.session.vars['ran']) == Constants.players_per_group:
            self.session.vars['nominees'] = random.sample(
                Constants.preferences, 2)
        # special case: no one runs
        elif len(self.session.vars['ran']) == 0:
            self.session.vars['nominees'] = random.sample(
                Constants.preferences, 1)
        # 1-4 people run 
        else:
            for p in self.group.get_players():
                if not p.ran:
                    d = p.participant.vars['distances'].copy()
                    d.pop(p.candidate_number, None)
                    for pp in self.group.get_players():
                        if not pp.ran:
                            d.pop(pp.candidate_number, None)
                    # d is guaranteed to be non-empty here
                    closest = min(d.items(), key=lambda x: x[1])
                    d.pop(closest[0], None)
                    p.preference = closest[0]
                    p.preference2 = None
                    if d:
                        second_closest = min(d.items(), key=lambda x: x[1])
                    else:
                        second_closest = (None, None)
                    if closest[1] == second_closest[1] and self.round_number <= Constants.num_rounds_runoff:
                        p.preference2 = second_closest[0]
                    elif closest[1] == second_closest[1]:
                        if random.random() < 0.5:
                            p.preference = second_closest[0]
                if p.preference2:
                    votes[p.preference] += 1
                    votes[p.preference2] += 1
                else:
                    votes[p.preference] += 2
            
            first, second = votes.most_common(2)
            # add the highest voted person to nominees
            self.session.vars['nominees'].append(first[0])
            # if there is a tie, add the tie person to nominees
            if first[1] == second[1]:
                self.session.vars['nominees'].append(second[0])       
            # if runoffs are turned on, and the nominee did not get more than
            # half of the vote, pick the second highest voted person as the
            # second nominee, breaking ties randomly
            elif self.round_number <= Constants.num_rounds_runoff and first[1] <= \
                Constants.players_per_group:
                votes_needed = second[1]
                candidates = [c[0] for c in votes.most_common() \
                    if c[1] == votes_needed]
                # NOTE: do all candidates who received votes_needed votes get
                # entered, or just the ones who also ran?
                self.session.vars['nominees'].append(random.choice(candidates))

        # Determine winner
        # 1 nominee
        if len(self.session.vars['nominees']) == 1:
            self.session.vars['winner'] = self.session.vars['nominees'][0]
        # 2 nominees and second round
        elif len(self.session.vars['nominees']) > 1 and self.round_number <= Constants.num_rounds_runoff:
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
    timeout_seconds = 60
 
    def vars_for_template(self):
        round_payoff = c(self.session.config['endowment'])
        if self.player.ran:
            round_payoff -= self.session.config['C']
            if self.player.candidate_number in self.session.vars['nominees'] and \
                self.session.vars['second_round']:
                round_payoff -= self.session.config['D']
            if self.player.candidate_number == self.session.vars['winner']:
                round_payoff += self.session.config['B']
        round_payoff -= abs((self.player.candidate_number - self.session.vars['winner']) / 100.0)
        self.player.round_payoff = round_payoff
        if self.player.id_in_group == 1:
            self.group.nominees = str(self.session.vars['nominees'])
            self.group.winner = str(self.session.vars['winner'])
            self.group.ran = str(self.session.vars['ran'])
            self.group.second_round = self.session.vars['second_round']
        if self.round_number == self.player.participant.vars['paying_round']:
            self.player.set_payoffs(round_payoff) 
        return {
            'nominees': str(self.session.vars['nominees']),
            'winner': self.session.vars['winner'],
            'ran': str(self.session.vars['ran']),
            'second_round': self.session.vars['second_round'],
            'round_payoff': round_payoff
        }

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        chosen_round = self.player.participant.vars['paying_round']
        payout = self.player.in_round(chosen_round).payoff
        return {
            'chosen_round': chosen_round,
            'payout': payout,
        }

page_sequence = [
    Introduction,
    Voting,
    ResultsWaitPage,
    Results,
    FinalResults,
]
