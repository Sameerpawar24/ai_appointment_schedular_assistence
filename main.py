import asyncio
from test.core.conversation_manager import ConversationManager
from test.speech_to_text.stt_service import listen_once
from test.llm.llm_service import generate_response
from test.text_to_speech.tts_service import speak_text


async def main():
    manager = ConversationManager()

    while True:
        if manager.is_speaking:
            await asyncio.sleep(0.2)
            continue

        text = await listen_once()

        if text :
            await manager.handle_user_input(
                text,
                generate_response,
                speak_text
            )
        else:
            await asyncio.sleep(0.5)  # prevent rapid loop spam



if __name__ == "__main__":
    asyncio.run(main())
