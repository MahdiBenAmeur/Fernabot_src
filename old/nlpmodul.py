import time
import asyncio
from rasa.core.agent import Agent

agent = Agent.load("../models/nlu-20241209-095924-unary-actress.tar.gz")

async def get_intent(text: str) -> str:
    result = await agent.parse_message(text)
    confidence= result["intent"]["confidence"]
    return result["intent"]["name"]

if __name__ == "__main__":
    # Basic greetings
    for query in ["salut","hjdvhjsbvhjc jsdbsbjcd", "khobz mo9li", "n7eb nakel ", "Good morning" , "saleemmm" , "chfamma khedma ?" ,"شنية فرص الخدمة اللي موجودة؟" ,"famma 9raya jdyda?" ,"chnoua mawjoud training "]:
        start = time.time()
        intent , confidence = asyncio.run(get_intent(query))
        end = time.time()
        print(f"Query: {query} -> Intent: {intent} , Confidance : {confidence}, Time: {end - start:.4f}s")

