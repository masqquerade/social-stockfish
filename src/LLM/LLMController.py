import os
from collections import Counter
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.Planner.Actions import RomanceAction

def get_policy_prior_system_prompt():
    """
    :return: Policy-prior system-prompt
    """

    return (
        f"""
            You are Dialogue-StrategistGPT, helping User {os.getenv("CLIENT_NICKNAME")} decide the single next dialogue-act in a romantic chat.  
            Your decision must be tightly connected to the most recent messages—pick the act that logically “answers” 
            or builds on what User {os.getenv("PARTNER_NICKNAME")} just said.  
        """
    )

def get_policy_prior_prompt(history, goal):
    """
    :param history: Virtual history
    :param goal: Goal of the user
    :return: Policy-prior user-prompt
    """

    lines = []
    for act in RomanceAction:
        if act.name != "ROOT":
            lines.append(f" - {act.name} : {act}")

    return (
        f"""
        Context:
        {history}

        User {os.getenv("CLIENT_NICKNAME")}’s long-term goal: {goal}

        Below is the inventory of valid next dialogue-acts.  
        Respond with **ONE** act label from the list that would be the most plausible
        and contextually natural next move for User {os.getenv("CLIENT_NICKNAME")} right now.

        Valid acts:
        {"\n".join(lines)}

        Rules:
        1. Output must be *exactly* one label from the list (case-sensitive).
        2. Do NOT add any explanation or extra text.
        
        Steps:
        1. Analyze the chat history
        2. Analyze the context of the last conversation part and peak the most plausible Action which will bring thу {os.getenv("CLIENT_NICKNAME")} closer to the long-term goal.

        EXAMPLES
        {os.getenv("PARTNER_NICKNAME")}: “How was your day?”
        Action → SHARE_EMOTION

        {os.getenv("PARTNER_NICKNAME")}: “I really want to see you!!”
        Action → MOVE_TO_CALL_VIDEO
        """
    )

def parse_actions(response) -> List[RomanceAction]:
    choices = []

    for choice in response.choices:
        choices.append(RomanceAction[choice.message.content])

    return choices

class LLMController:
    def __init__(self):
        self.client = OpenAI()

    def generate_actions(self, history, goal, m=15) -> RomanceAction:
        """
        Generates m actions and finds the most probable one.

        :param goal: Goal of the user
        :param history: Virtual history
        :param m: Count of actions to be generated
        """

        resp = self.client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=[
                ChatCompletionSystemMessageParam(role="system", content=get_policy_prior_system_prompt()),
                ChatCompletionUserMessageParam(role="user", content=get_policy_prior_prompt(history, goal))
            ],
            n=m,
            temperature=1.0,
        )

        actions = parse_actions(resp)
        print(actions)
        tally = Counter(actions)

        return tally.most_common(1)[0][0]

    def list_models(self):
        print(self.client.models.list())