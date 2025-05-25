# TODO
import os
import random

import anthropic
from anthropic.types import MessageParam, Message, TextBlock, Usage

from src.LLM.PromptManager import *

def get_max_tokens(history_len):
    """
    :param history_len: length of history
    :return: maximum amount of tokens
    """

    if history_len < 5:
        max_tokens = 512

    elif history_len < 15:
        max_tokens = 768

    else:
        max_tokens = 1024

    return max_tokens

class MessagesCreationAgent:
    def __init__(self, api_key, max_tokens):
        self.client = anthropic.Anthropic(
            api_key=api_key,
        )

        self.max_tokens = max_tokens

    def get_messages(self, k, prompt):
        """
        :param prompt: user_msg, system_msg
        :param k: Amount of messages to generate
        :param content: message content
        :return: messages in raw format
        """

        messages = []
        content, system = prompt

        # get k message-candidates from the LLM
        # may be too slow --> we need to use Batches API which is async...
        for _ in range(k):
            message = self.client.messages.create(
                model=os.getenv('LLM_MODEL'),
                system=system,
                temperature=0.5,
                max_tokens=self.max_tokens,
                messages=[
                    MessageParam(
                        role="user",
                        content=content,
                    )
                ]
            )

            messages.append(message)

        ## MOCK
        # msgs = ["Как дела?", "Давай я позвоню", "что делаешь", "Приветствую, уважаемая!", "Люблю тебя!", "го фильм посмотрим"]
        # users = ["Davyd", "Girl"]
        # for _ in range(k):
        #     messages.append(
        #         Message(id='msg_01CH2jdx8Cc8WbKzcDPtdC9A', content=[TextBlock(citations=None,
        #                                                                       text='{\n  "user": "' + random.choice(users) + '",\n  "message": "' + random.choice(msgs) + '"\n}',
        #                                                                       type='text')],
        #                 model='claude-sonnet-4-20250514', role='assistant', stop_reason='end_turn', stop_sequence=None,
        #                 type='message',
        #                 usage=Usage(cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=2538,
        #                             output_tokens=32, server_tool_use=None, service_tier='standard'))
        #
        #     )


        return messages

    def get_client_messages(self, history, k):
        """
        :param history: history of the current node
        :param k: Amount of messages to generate
        :return: Messages in raw format
        """

        return self.get_messages(
            k=k,
            prompt=get_message_prompt("flirt", {"client": os.getenv("CLIENT_NICKNAME"), "partner": os.getenv("PARTNER_NICKNAME")}, history)
        )

    def get_partner_messages(self, history, k):
        """
        :param history: history of the current node
        :param k: Amount of messages to generate
        :return: Messages in raw format
        """

        return self.get_messages(
            k=k,
            prompt=get_message_prompt("flirt", {"client": os.getenv("PARTNER_NICKNAME"), "partner": os.getenv("CLIENT_NICKNAME")}, history)
        )
