# Instructions for playing locally
I assume you already have python3 installed.
1. Install otree: `pip3 install -U otree`
1. Create a project: `otree startproject candicitizen`
1. Navigate into the project directory: `cd candicitizen`
1. Clone this repo: `git clone https://github.com/kmlv/citizen.git`
1. Edit SESSION_CONFIGS in the settings.py file to look like this:
```
SESSION_CONFIGS = [
    dict(
        name='citizen',
        num_demo_participants=5,
        app_sequence=['citizen'],
        endowment=10.0,
        B=3.0,
        C=1.5,
        D=0.75,
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
'Sessions' link at the top left.
1. Username: admin. Password: slugtree. Then click 'Create new session'
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

# Brief git tutorial
Git is a way for multiple people to collaborate on a project simultaneously.
You need to know how to do 3 things: *clone*, *push*, and *pull*.

### Clone
`git clone https://github.com/kmlv/citizen.git` will create a copy of this
repository, including the directory structure and all files, into a directory
that gets automatically created and is called `citizen`. You should only need
to do this once on your local machine.

### Push
This is how you take work you have done in the `citizen` repo on your local
computer, and upload it to github.
1. Change some files in the `citizen` repo.
2. Into your terminal, type the command `git status`. It should show a list
of files that have been edited. If there is any file on there that you did
not edit, something is wrong.
1. Into your terminal, type the command `git add -A`.
1. Into your terminal, type the command `git commit -m "<message>", replacing
<message> with a short message about what you changed.
1. Into your terminal, type the command `git push origin master`

### Pull
This is how you take work that exists on github, and merge it into your copy
of the repository on your local computer.

Into your terminal, from inside the `citizen` directory,
type `git pull origin master`. If you get any merge conflicts, talk to Eli.

