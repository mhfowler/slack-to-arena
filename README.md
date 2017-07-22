# slack-to-arena

Parses a slack export and uploads all links to are.na


# note

still in progress


# setup

0. `git clone github.com/mhfowler/slacktoarena ~/slacktoarena`

1. `cd ~/slacktoarena` 

2. `cp secret.json.sample secret.json`

3. visit https://dev.are.na/ and create an are.na application

4. from you are.na application page, click 'regenerate token'

5. put the token in secret.json

6. `pip install -r requirements.txt`


# run

1. export slack from the slack website

2. unzip the export

3. `python slacktoarena.py <path_to_slack_export> <arena_username>`


