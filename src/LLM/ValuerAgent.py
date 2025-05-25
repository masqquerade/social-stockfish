# TODO
import os
import random

import anthropic
from anthropic.types import MessageParam

from src.LLM.PromptManager import *

class ValuerAgent:
    def __init__(self, api_key, max_tokens):
        self.client = anthropic.Anthropic(
            api_key=api_key,
        )

        self.max_tokens = max_tokens

    def value(self, history):
        content, system = get_message_score_prompt(
            chat_history=history,
            additional_context={"client": os.getenv("CLIENT_NICKNAME"), "partner": os.getenv("PARTNER_NICKNAME")},
            goal="flirt" # hardcoded!! TODO
        )

        message = self.client.messages.create(
            model=os.getenv('LLM_MODEL'),
            system=system,
            temperature=0.3,
            max_tokens=self.max_tokens,
            messages=[
                MessageParam(
                    role="user",
                    content=content,
                )
            ]
        )

        return message