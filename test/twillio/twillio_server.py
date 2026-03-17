from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

from langchain_core.messages import HumanMessage
from test.llm.llm_service import generate_response

app = FastAPI()

memory_store = {}


@app.post("/incoming-call")
async def incoming_call():

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/process",
        speechTimeout="auto"
    )

    gather.say(
        "Hello. Welcome to appointment assistant. "
        "You can schedule reschedule or cancel appointments."
    )

    response.append(gather)

    return Response(content=str(response), media_type="text/xml")


@app.post("/process")
async def process(request: Request):

    form = await request.form()

    user_text = form.get("SpeechResult")
    caller = form.get("From")

    if caller not in memory_store:
        memory_store[caller] = []

    memory = memory_store[caller]

    memory.append(HumanMessage(content=user_text))

    reply = await generate_response(memory)

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/process",
        speechTimeout="auto"
    )

    gather.say(reply)

    response.append(gather)

    return Response(content=str(response), media_type="text/xml")