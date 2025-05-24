# TODO
import os

import anthropic
from anthropic.types import MessageParam

from src.LLM.PromptManager import *

class MessagesCreationAgent:
    # TODO
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(
            api_key=api_key,
        )

    # TODO
    def get_messages(self, history, k):
        messages = []

        # get k message-candidates from the LLM
        # may be too slow --> we need to use Batches API which is async...
        for _ in range(k):
            message = self.client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1024,
                messages=[
                    MessageParam(
                        role="user",
                        content=get_message_prompt(
                            "flirt", # hardcoded
                            additional_context={"client": os.getenv("CLIENT_NICKNAME"), "companion": os.getenv("COMPANION_NICKNAME")},
                            chat_history=history,
                        )
                    )
                ]
            )

            messages.append(message)

        return messages