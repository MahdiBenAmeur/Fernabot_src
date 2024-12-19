from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests

import config
import db
#from nlpmodul import get_intent
from config import  VERIFICATION_TOKEN, moreOptionsPressedIndicator

app = FastAPI()

# Conversation tree structure
# Each node represents a step in the conversation.
# "options" contains references to other nodes (identified by keys like "2", "3", etc.)
# "action" can be a function that fetches data or returns dynamic content.
tree = {
    # Main Menu
    "1": {
        "message": "أهلا وسهلا بيك في فرنا بوت 🤖! هاني هنا باش نعاونك تلقى فرص تدريب 📚 وخدمة في فرنانة. نقدر نعطيك آخر الأخبار على التدريبات والفرص المهنية. إختار شنوا تحب تعرف أكثر 🤔 وأنا في الخدمة! 😊",
        "title": "القائمة الرئيسية",
        "options": ["2", "3", "4", "6"],
        "action": ""
    },

    # Job Opportunities
    "2": {
        "message": "تحب تعرف على فرص الخدمة؟ اختار واحد من هالقطاعات:",
        "title": "فرص الخدمة",
        "options": ["2,1", "2,2", "2,3", "2,4"],
        "action": ""
    },
    "2,1": {
        "message": "أحدث فرص العمل في **القطاع التونسي**:",
        "title": "تونسية",
        "options": ["2,1,1","1"],
        "action": lambda: db.get_emploi_by_genre("تونسية")
    },
    "2,2": {
        "message": "أحدث فرص العمل في **القطاع الدولي**:",
        "title": "دولية",
        "options": ["2,1,1","1"],
        "action": lambda: db.get_emploi_by_genre("دولية")
    },
    "2,3": {
        "message": "أحدث فرص العمل في **القطاع الخليجي**:",
        "title": "خليجية",
        "options": ["2,1,1","1"],
        "action": lambda: db.get_emploi_by_genre("خليجية")
    },
    "2,4": {
        "message": "أحدث فرص العمل في **تكوين مهني**:",
        "title": "تكوين مهني",
        "options": ["2,1,1","1"],
        "action": lambda: db.get_emploi_by_genre("تكوين مهني")
    },

    # Training Opportunities
    "3": {
        "message": "تحب تعرف على الدورات التدريبية المتاحة؟ اختار من المجالات التالية:",
        "title": "دورات تدريبية",
        "options": ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7", "3,8"],
        "action": ""
    },
    "3,1": {
        "message": "أحدث دورات في مجال **التكنولوجيا**:",
        "title": "التكنولوجيا",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("التكنولوجيا")
    },
    "3,2": {
        "message": "أحدث دورات في مجال **الأعمال**:",
        "title": "الأعمال",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("الأعمال")
    },
    "3,3": {
        "message": "أحدث دورات في مجال **علوم البيانات**:",
        "title": "علوم البيانات",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("علوم البيانات")
    },
    "3,4": {
        "message": "أحدث دورات في مجال **الصحة**:",
        "title": "الصحة",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("الصحة")
    },
    "3,5": {
        "message": "أحدث دورات في مجال **العلوم الاجتماعية**:",
        "title": "العلوم الاجتماعية",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("العلوم الاجتماعية")
    },
    "3,6": {
        "message": "أحدث دورات في مجال **التنمية المستدامة**:",
        "title": "التنمية المستدامة",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("التنمية المستدامة")
    },
    "3,7": {
        "message": "أحدث دورات في مجال **حقوق الإنسان**:",
        "title": "حقوق الإنسان",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("حقوق الإنسان")
    },
    "3,8": {
        "message": "أحدث دورات في مجال **الفنون والتعليم**:",
        "title": "الفنون والتعليم",
        "options": ["3,1,1","1"],
        "action": lambda: db.get_courses_by_genre("الفنون والتعليم")
    },

    # Project Support
    "4": {
        "message": "عندك مشروع أو فكرة مشروع جديدة و تحب تلقى دعم أو تمويل؟ نجمو نعاونوك في هذا.",
        "title": "بعث مشروع",
        "options": ["4,1", "5", "1"],
        "action": ""
    },
    "4,1": {
        "message": "باش تتعرف على فرص الدعم المتوفره ، إختار نوع الدعم الي حاشتك بيه:",
        "title": "دعم إداري ومؤسساتي؟",
        "options": ["4,1,1", "4,1,2", "4,1,3", "4,1,4", "4,1,5", "1"],
        "action": ""
    },
    "4,1,1": {
        "message": "أحدث الفرص المتاحة للمنح الدراسية:",
        "title": "منح دراسية",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_support_opportunities_by_type("منح دراسية")
    },
    "4,1,2": {
        "message": "أحدث الفرص المتاحة للزمالات:",
        "title": "زمالات",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_support_opportunities_by_type("زمالات")
    },
    "4,1,3": {
        "message": "أحدث الفرص المتاحة لبرامج التبادل:",
        "title": "برامج التبادل",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_support_opportunities_by_type("برامج التبادل")
    },
    "4,1,4": {
        "message": "أحدث الفرص المتاحة لبرامج التطوع:",
        "title": "برامج التطوع",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_support_opportunities_by_type("برامج التطوع")
    },
    "4,1,5": {
        "message": "اكتشف فرص تعلم لغات جديدة:",
        "title": "تعلم لغة جديدة",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_support_opportunities_by_type("تعلم لغة جديدة")
    },

    "5": {
        "message": "تلوج على طريقة باش تمول المشروع تاعك؟ اختار نوع الدعم الي حاشتك بيه:",
        "title": "بحث عن تمويل؟",
        "options": ["5,1", "5,2", "5,3", "5,4", "5,5", "5,6", "5,7", "5,8", "5,9"],
        "action": ""
    },
    "5,1": {
        "message": "أحدث فرص الدعم لمشاريع **ريادة الأعمال**",
        "title": "ريادة الأعمال",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("ريادة الأعمال")
    },
    "5,2": {
        "message": "أحدث فرص الدعم لمشاريع **التمويل**",
        "title": "التمويل",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("التمويل")
    },
    "5,3": {
        "message": "أحدث فرص الدعم لمشاريع **إدارة المشاريع**",
        "title": "إدارة المشاريع",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("إدارة المشاريع")
    },
    "5,4": {
        "message": "أحدث فرص الدعم لمشاريع **الابتكار**",
        "title": "الابتكار",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("الابتكار")
    },
    "5,5": {
        "message": "أحدث فرص الدعم لمشاريع **الفلاحة**",
        "title": "الفلاحة",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("الفلاحة")
    },
    "5,6": {
        "message": "أحدث فرص الدعم لمشاريع **التنمية المستدامة**",
        "title": "التنمية المستدامة",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("التنمية المستدامة")
    },
    "5,7": {
        "message": "أحدث فرص الدعم لمشاريع **الصناعة**",
        "title": "الصناعة",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("الصناعة")
    },
    "5,8": {
        "message": "أحدث فرص الدعم لمشاريع **التنمية المحلية**",
        "title": "التنمية المحلية",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("التنمية المحلية")
    },
    "5,9": {
        "message": "أحدث فرص الدعم لمشاريع **التعليم والتدريب المهني**",
        "title": "التعليم والتدريب المهني",
        "options": ["4,1,1,1","1"],
        "action": lambda: db.get_financing_opportunities("التعليم والتدريب المهني")
    },

    # Help and Support
    "6": {
        "message": "للمساعدة أو الإستفسارات اتصل بينا. :12 345 678",
        "title": "مساعدة",
        "options": ["1"],
        "action": ""
    },

    # Additional Pagination Nodes
    "2,1,1": {
        "message": "..",
        "title": "زيدني",
        "options": ["1", "2,1,1"],
        "action": ""
    },
    "3,1,1": {
        "message": "..",
        "title": "زيدني",
        "options": ["1", "3,1,1"],
        "action": ""
    },
    "4,1,1,1": {
        "message": "..",
        "title": "زيدني",
        "options": ["1", "4,1,1,1"],
        "action": ""
    }
}


@app.get("/webhook")
async def verify(request: Request):
    """
    Endpoint to verify Facebook webhook setup.
    """
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFICATION_TOKEN:
        return PlainTextResponse(challenge)
    else:
        return PlainTextResponse("Verification failed", status_code=403)


def send_message(recipient_id: str, message: dict) -> dict:
    """
    Send a message using Facebook's Send API.
    """
    url = f"https://graph.facebook.com/v11.0/me/messages?access_token={config.BOT_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": message
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def build_quick_replies(options: list, trigger: str, start: int) -> list:
    """
    Build quick reply buttons based on the given options.
    Each option corresponds to a node in the conversation tree.
    """
    quick_replies = []
    for option in options:
        if option in tree:
            node = tree[option]
            title = node.get('title', node['message'])
            if title == "زيدني":
                # "زيدني" indicates loading more options (pagination).
                next_payload = f"{moreOptionsPressedIndicator}_{trigger[0]}_{tree[trigger]['title']}_{start}"
                print("next_payload", next_payload)
                quick_replies.append({
                    "content_type": "text",
                    "title": title,
                    "payload": next_payload
                })
            else:
                quick_replies.append({
                    "content_type": "text",
                    "title": title,
                    "payload": option
                })
    return quick_replies


def build_more_option_response(payload: str) -> dict:
    """
    Build a response when the user requests more options (pagination).
    The payload format: <indicator>_<part>_<genre>_<start>
    """
    print(payload)
    _, part, genre, start = payload.split('_')
    start_index = int(start)
    addition=0
    # Depending on the part ("2" for jobs, otherwise training)
    if part == "2":
        action_result = db.get_emploi_by_genre(genre, start_index)
    elif part == "3":
        action_result = db.get_courses_by_genre(genre, start_index)
    elif part == "4":
        action_result = db.get_support_opportunities_by_type(genre, start_index)
    elif part == "5":
        action_result = db.get_financing_opportunities(genre, start_index)
    

    response_text = action_result["text"]
    response = {}

    # If no titles are returned, just send a text message with a main menu option
    if "titles" not in action_result:
        response["text"] = response_text
        response["quick_replies"] = [{
            "content_type": "text",
            "title": "القائمة الرئيسية",
            "payload": "1"
        }]
        return response

    # Build a button template if titles are available
    addition=len(action_result["titles"])
    buttons = []
    for index, title in enumerate(action_result["titles"]):
        url = "https://www.messenger.com"
        if "urls" in action_result:
            url = action_result["urls"][index]
        buttons.append({
            "type": "web_url",
            "url": url,
            "title": title
        })
    response = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": response_text,
                "buttons": buttons
            }
        }
    }

    # Add pagination quick reply ("زيدني") and main menu
    next_payload = f"{_}_{part}_{genre}_{start_index+addition}"
    response["quick_replies"] = [
        {
            "content_type": "text",
            "title": "زيدني",
            "payload": next_payload
        },
        {
            "content_type": "text",
            "title": "القائمة الرئيسية",
            "payload": "1"
        }
    ]

    return response


def build_response(payload: str) -> dict:
    """
    Construct a response message based on the conversation node identified by 'payload'.
    """
    node = tree.get(payload)
    if not node:
        return {"text": "عذراً، لم أفهم ذلك."}

    response_text = node['message']
    response = {}
    start = 0
    # If the node has an action to execute, append its result
    if callable(node["action"]):
        action_result = node["action"]()
        start = len(action_result["titles"])
        response_text += "\n" + action_result["text"]

        # Construct button template if there are titles
        buttons = []
        if "titles" in   action_result :
            for index,title in enumerate(action_result["titles"]):
                url ="https://www.messenger.com"
                if "urls" in action_result:
                    url=action_result["urls"][index]
                buttons.append({
                    "type": "web_url",
                    "url":  url,
                    "title": title
                })

            response = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": response_text,
                        "buttons": buttons
                    }
                }
            }
    else:
        response = {"text": response_text}

    # Add quick replies if the node defines options
    if 'options' in node:
        response["quick_replies"] = build_quick_replies(node['options'], payload,start)

    return response


@app.post("/webhook")
async def webhook(request: Request):
    """
    Handle incoming webhook events from Facebook.
    """
    data = await request.json()
    print("Received a message event" )

    if data.get('object') == 'page':
        for entry in data.get('entry', []):
            for event in entry.get('messaging', []):
                sender_id = event['sender']['id']
                show_typing(sender_id, True)

                # If user pressed a quick reply button
                if 'quick_reply' in event.get('message', {}):
                    print("Quick reply received")
                    payload = event['message']['quick_reply']['payload']

                    if payload in tree:
                        response_message = build_response(payload)
                        print("Sending message:", response_message)
                        send_message(sender_id, response_message)
                    elif moreOptionsPressedIndicator in payload:
                        # Handle pagination (load more options)
                        print(payload)
                        response_message = build_more_option_response(payload)
                        send_message(sender_id, response_message)
                    else:
                        send_message(sender_id, {"text": "عذراً، لم أفهم ذلك."})

                # If user sent a text message
                elif 'message' in event:
                    print("Text message received")
                    """user_text = event["message"]["text"]
                    intent = await get_intent(user_text)
                    print("Identified intent:", intent)

                    # Map the identified intent to a node payload
                    predicted_payload = intent_to_payload[intent]"""
                    response_message = build_response("1")
                    print("Sending message:", response_message)
                    send_message(sender_id, response_message)

                show_typing(sender_id, False)


def show_typing(user_id: str, is_typing: bool) -> dict:
    """
    Show or hide the typing indicator for the user.
    """
    url = f"https://graph.facebook.com/v11.0/{config.PAGE_ID}/messages?access_token={config.BOT_TOKEN}"
    headers = {"Content-Type": "application/json"}
    action = "typing_on" if is_typing else "typing_off"
    body = {
        "recipient": {"id": user_id},
        "sender_action": action
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()


if __name__ == "__main__":
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
    config.dbconfig=configurations["db"]
    config.BOT_TOKEN=configurations["pageconfig"]["BOT_TOKEN"]
    config.PAGE_ID=configurations["pageconfig"]["PAGE_ID"]



    #if __name__ == "__main__":
    import uvicorn
    import os
    import sys

    # Determine if we are running in a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    ssl_key_path = os.path.join(base_path, "sslVerification", "fernabot.top.key")
    ssl_cert_path = os.path.join(base_path, "sslVerification", "fullchain.pem")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=ssl_key_path,
        ssl_certfile=ssl_cert_path
    )
