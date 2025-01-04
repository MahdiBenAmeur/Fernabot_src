BOT_TOKEN="EAB9XyDt9eWABOZCCPo6GHJVUmpUhcF3wIRGGN5hMopQZBc2oSrmdFONauIQg43h5AeBrZB0fqmZC2loYDsB7AdZBupECRWXcaffqRysBZB46hyxZCq6UasP9iBw1emGC0pMPLo8oScMW0THjChhNMJ1BZBWboIiZCzMhGc8ZBAZAaZC2X6Xia6bqGGYQPeQrZB342hOvXCwZDZD"
VERIFICATION_TOKEN="fernabottopsercittokenHFGFkjuiohi454854"
PAGE_ID="487888641079383"
FB_API_URL='https://graph.facebook.com/v12.0/me/messages'
GEMINI_API_KEY="AIzaSyB3cq3n06NGuvgzUiN7wasZXDkTP0SgleI"
moreOptionsPressedIndicator = "moreOptionsStatusMessage"
dbconfig = {}

intent_to_payload={
    "greet":"1",
    "ask_about_jobs":"2",
    "ask_about_training":"3",
    "ask_for_help":"4",
    "other" : "5"
}

import os
import sys
import json

if getattr(sys, 'frozen', False):
    # The executable is running in a frozen state
    # sys.executable is the full path to the main.exe file
    base_path = os.path.dirname(sys.executable)
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(base_path, "config.json")

with open(config_path, "r") as f:
    configurations = dict(json.load(f))
dbconfig = configurations["db"]
BOT_TOKEN = configurations["pageconfig"]["BOT_TOKEN"]
PAGE_ID = configurations["pageconfig"]["PAGE_ID"]

#t_1567769057468221/messages?limit=20&fields=message,from,to,created_time

#https://a879-102-157-49-247.ngrok-free.app/webhook?hub.mode=subscribe&hub.challenge=773490065&hub.verify_token=fernabottopsercittokenHFGFkjuiohi454854