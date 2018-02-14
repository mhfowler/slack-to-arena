# slack-to-arena

Even if you have a free slack you can export your entire slack history into a .json

This tool helps you to parse a slack export and upload any links 
 that were shared in slack messages to are.na, 
 a way of archiving links and information shared in a slack group.


# 1. export from slack

Follow the instructions on slack's website to create a standard export
from your slack group (you need to be an admin of the group):
https://get.slack.help/hc/en-us/articles/201658943-Export-data-and-message-history

Once the export is finished you will receive an email and can download a .zip
of the slack export. 


# 2. setup an are.na application

Login or create an account on are.na (it might make sense to create a new account
just for this archive).

Create an are.na application to integrate with the are.na API 


# 3. run the exporter (it takes a while, may want to run overnight)

0. `git clone https://github.com/mhfowler/slacktoarena ~/slacktoarena`

1. `cd ~/slacktoarena` 

2. `cp secret.json.sample secret.json # and enter your token in secret.json`

3. `python slacktoarena.py <path_to_slack_export> <arena_username>`


