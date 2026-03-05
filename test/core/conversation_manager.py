import asyncio

class ConversationManager:
    def __init__(self):
        self.processing_lock = asyncio.Lock()
        self.last_user_text = None
        self.is_speaking = False
        self.memory = []

    async def handle_user_input(self, text, llm_func, tts_func):
        # Ignore empty
        if not text:
            return

        # Ignore duplicate
        if text == self.last_user_text:
            return

        self.last_user_text = text

        async with self.processing_lock:
            print(f"\n🧑 You said: {text}")

            # Add to memory
            self.memory.append({"role": "user", "content": text})

            # Generate AI response
            response = await llm_func(self.memory)

            # Add assistant memory
            self.memory.append({"role": "assistant", "content": response})

            print(f"🤖 Assistant: {response}")

            # Speak
            self.is_speaking = True
            await tts_func(response)
            self.is_speaking = False
