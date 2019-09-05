# Instructions for playing locally
I assume you already have python3 installed.
1. Install otree: `pip3 install -U otree`
1. Create a project: `otree startproject candicitizen`
1. Navigate into the project directory: `cd citizen`
1. Clone this repo: `git clone https://github.com/kmlv/citizen.git`
1. Edit SESSION_CONFIGS in the settings.py file to look like this:
```
SESSION_CONFIGS = [
    dict(
        name='citizen',
        num_demo_participants=5,
        app_sequence=['citizen'],
        endowment=50.0,
        B=15.25,
        C=7.5,
        D=3.75,
    ),
 ]
 ```
Or change `endowment`, `B`, `C`, and `D` as you wish.

1. There will always be 10 rounds. By default,
there are 5 rounds of runoff then 5 rounds of non-runoff.
To change these numbers, edit models.py, in class Constants,
and change num_rounds_runoff to a different number. If you change it
to 1, there will be 1 round of runoff then 9 rounds of non-runoff.
 1. Start the server: `otree devserver`
 1. Navigate to `localhost:8000` in your browser.
 1. Play the experiment.

# Instructions for playing on the server
1. Navigate in your browser to `leeps-otree.ucsc.edu:8000`
1. To use the default config values shown above, simply click 'Candidate Citizen'
and play the game.
1. To configure your own config values and play a real session, click the
'Sessions' link at the top left, then click 'Create new session'
1. Select 'Candidate Citizen' as the session config. Enter your number of
participants.
1. Click 'Configure session'. Fill in the values you want for endowment, B,
C, and D.
1. Click 'Create'
1. Play the game.

# Testing
If you edit anything, and want to make sure you didn't break something
accidentally, run `otree test citizen` from the `candicitizen` directory.
It should not fail. Warnings are fine.

