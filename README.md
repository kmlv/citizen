# Instructions
I assume you already have python3 installed.
1. Install otree: `pip3 install -U otree`
1. Clone this repo: `git clone https://github.com/kmlv/citizen.git`
1. `cd` into the project directory: `cd citizen`
1. Edit SESSION_CONFIGS in the settings.py file to look like this:
```
SESSION_CONFIGS = [
    dict(
        name='candicitizen',
        num_demo_participants=5,
        app_sequence=['candicitizen']
    ),
 ]
 ```
 1. Start the server: `otree devserver`
 1. Navigate to `localhost:8000` in your browser.
 1. Play the experiment.

 Please tell me about any bugs that come up, I know there are a few.
 This is a prototype; not all features of the game have been implemented.

 Features not yet implemented:
    - payoffs
    - config file
