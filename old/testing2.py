from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import httpx
import asyncio

import db  # Ensure db functions are async
from old.nlpmodul import get_intent  # Ensure get_intent is async
from config import BOT_TOKEN, VERIFICATION_TOKEN, PAGE_ID, intent_to_payload, moreOptionsPressedIndicator

app = FastAPI()

# Conversation tree remains the same
tree = {
    "1": {
        "message": "أهلا وسهلا بيك في فرنا بوت 🤖! هاني هنا باش نعاونك تلقى فرص تدريب 📚 وخدمة في فرنانة. نقدر نعطيك آخر الأخبار على التدريبات والفرص المهنية. إختار شنوا تحب تعرف أكثر 🤔 وأنا في الخدمة! 😊",
        "title": "القائمة الرئيسية",
        "options": ["2", "3", "4"],
        "action": ""
    },
    "2": {
        "message": "تحب تعرف على فرص الخدمة؟ اختار واحد من هالقطاعات:",
        "title": "فرص الخدمة",
        "options": ["2,1", "2,2", "2,3", "2,4", "2,5"],
        "action": ""
    },
    # Job Opportunities
    "2,1": {
        "message": "أحدث فرص العمل في **تكنولوجيا**:",
        "title": "تكنولوجيا",
        "options": ["2,1,1", "1"],
        "action": lambda: db.get_job_opportunities("تكنولوجيا")
    },
    "2,2": {
        "message": "أحدث فرص العمل في **إدارة**:",
        "title": "إدارة",
        "options": ["2,1,1", "1"],
        "action": lambda: db.get_job_opportunities("إدارة")
    },
    "2,3": {
        "message": "أحدث فرص العمل في **تصميم**:",
        "title": "تصميم",
        "options": ["2,1,1", "1"],
        "action": lambda: db.get_job_opportunities("تصميم")
    },
    "2,4": {
        "message": "أحدث فرص العمل في **تعليم**:",
        "title": "تعليم",
        "options": ["2,1,1", "1"],
        "action": lambda: db.get_job_opportunities("تعليم")
    },
    "2,5": {
        "message": "أحدث فرص العمل في **صحة**:",
        "title": "صحة",
        "options": ["2,1,1", "1"],
        "action": lambda: db.get_job_opportunities("صحة")
    },

    "3": {
        "message": "تحب تعرف على الدورات التدريبية المتاحة؟ قولنا شنوة مجالات التدريب إلي تهمك.",
        "title": "دورات تدريبية",
        "options": ["3,1", "3,2", "3,3"],
        "action": ""
    },
    "4": {
        "message": "للمساعدة أو الإستفسارات اتصل بينا.",
        "title": "مساعدة",
        "options": ["4,1"],
        "action": ""
    },
    "5": {
        "message": "sorry mafhemtch",
        "title": "مساعدة",
        "options": ["4,1"],
        "action": ""
    },

    # Training Opportunities
    "3,1": {
        "message": "عندنا دورات في تكنولوجيا المعلومات والبرمجة. تحب تسجل؟",
        "title": "تكنولوجيا",
        "options": ["3,1,1", "1"],
        "action": lambda: db.get_training_opportunities("تكنولوجيا")
    },
    "3,2": {
        "message": "في تدريبات في التصميم والفنون. تحب تعرف أكثر؟",
        "title": "تصميم وفنون",
        "options": ["3,1,1", "1"],
        "action": lambda: db.get_training_opportunities("تصميم وفنون")
    },
    "3,3": {
        "message": "لو تحب تدريب في إدارة الأعمال، عنا خيارات متعددة. اختار اللي يعجبك.",
        "title": "إدارة أعمال",
        "options": ["3,1,1", "1"],
        "action": lambda: db.get_training_opportunities("إدارة أعمال")
    },

    # Support
    "4,1": {
        "message": "للاتصال: 12 345 678",
        "title": "كيفاش نتصل؟",
        "options": ["1"],
        "action": ""
    },

    # Additional pagination nodes
    "2,1,1": {
        "message": "..",
        "title": "زيدني",
        "options": ["1", "2,1,1"],
        "action": ""
    },
    "3,1,1": {
        "message": "..",
        "title": "زيدني",
        "options": ["1", "2,1,1"],
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

async def send_message(recipient_id: str, message: dict) -> dict:
    """
    Asynchronously send a message using Facebook's Send API.
    """
    url = f"https://graph.facebook.com/v11.0/me/messages?access_token={BOT_TOKEN}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"recipient": {"id": recipient_id}, "message": message})
        return response.json()

async def show_typing(user_id: str, on: bool) -> dict:
    """
    Asynchronously show or hide the typing indicator for the user.
    """
    url = f"https://graph.facebook.com/v11.0/{PAGE_ID}/messages?access_token={BOT_TOKEN}"
    action = "typing_on" if on else "typing_off"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"recipient": {"id": user_id}, "sender_action": action})
        return response.json()

def build_quick_replies(options: list, trigger: str) -> list:
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
                next_payload = f"{moreOptionsPressedIndicator}_{trigger.split(',')[0]}_{tree[trigger]['title']}_1"
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

async def build_more_option_response(payload: str) -> dict:
    """
    Build a response when the user requests more options (pagination).
    The payload format: <indicator>_<part>_<genre>_<start>
    """
    _, part, genre, start = payload.split('_')
    start_index = int(start)

    if part == "2":
        action_result = await db.get_job_opportunities(genre, start_index)
    else:
        action_result = await db.get_training_opportunities(genre, start_index)

    response_text = action_result["text"]
    response = {}

    if "titles" not in action_result:
        response["text"] = response_text
        response["quick_replies"] = [{
            "content_type": "text",
            "title": "القائمة الرئيسية",
            "payload": "1"
        }]
        return response

    buttons = []
    for title in action_result["titles"]:
        buttons.append({
            "type": "web_url",
            "url": "https://www.messenger.com",
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

    next_payload = f"{_}_{part}_{genre}_{start_index + 1}"
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

async def build_response(payload: str) -> dict:
    """
    Construct a response message based on the conversation node identified by 'payload'.
    """
    node = tree.get(payload)
    if not node:
        return {"text": "عذراً، لم أفهم ذلك."}

    response_text = node['message']
    response = {}

    if callable(node["action"]):
        action_result = await node["action"]()  # Await the async action
        response_text += "\n" + action_result["text"]

        buttons = []
        for title in action_result.get("titles", []):
            buttons.append({
                "type": "web_url",
                "url": "https://www.messenger.com",
                "title": title
            })

        if buttons:
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
    else:
        response = {"text": response_text}

    if 'options' in node:
        response["quick_replies"] = build_quick_replies(node['options'], payload)

    return response

@app.post("/webhook")
async def webhook(request: Request):
    """
    Handle incoming webhook events from Facebook.
    """
    data = await request.json()
    print("Received a message event")

    if data.get('object') == 'page':
        tasks = []
        for entry in data.get('entry', []):
            for event in entry.get('messaging', []):
                sender_id = event['sender']['id']
                tasks.append(handle_event(sender_id, event))
        await asyncio.gather(*tasks)
    return PlainTextResponse("ok")

async def handle_event(sender_id: str, event: dict):
    """
    Handle individual messaging events asynchronously.
    """
    await show_typing(sender_id, True)

    if 'quick_reply' in event.get('message', {}):
        print("Quick reply received")
        payload = event['message']['quick_reply']['payload']

        if payload in tree:
            response_message = await build_response(payload)
            print("Sending message:", response_message)
            await send_message(sender_id, response_message)
        elif moreOptionsPressedIndicator in payload:
            print(payload)
            response_message = await build_more_option_response(payload)
            await send_message(sender_id, response_message)
        else:
            await send_message(sender_id, {"text": "عذراً، لم أفهم ذلك."})

    elif 'message' in event:
        print("Text message received")
        user_text = event['message']['text']
        intent = await get_intent(user_text)
        print("Identified intent:", intent)

        pred_payload = intent_to_payload.get(intent, "1")  # Default to main menu if intent not found
        response_message = await build_response(pred_payload)
        print("Sending message:", response_message)
        await send_message(sender_id, response_message)

    await show_typing(sender_id, False)

# Example main block for testing
if __name__ == "__main__":
    # Test parsing of a payload
    print((moreOptionsPressedIndicator + ";job;تكنولوجيا;2").split(";"))
