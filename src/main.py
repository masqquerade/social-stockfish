import json
import os

from mcts.MCTS import parse_response, MCTS
from dotenv import load_dotenv

from src.LLM.MessagesCreationAgent import MessagesCreationAgent, get_max_tokens

load_dotenv()

def get_char_history_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        history_str = f.read()

    return history_str

def main():
    history = get_char_history_from_file(os.getenv('HISTORY_FILE_PATH'))
    json_history = json.loads(history)
    max_tokens = get_max_tokens(history_len=len(json_history))

    mcts = MCTS(
        max_tokens=max_tokens,
        k=2,
        c=2,
        base_history=json_history,
        api_key=os.getenv('API_KEY'),
    )

    mcts.init_root()
    result_node = mcts.search(10)

    print("Best message: " + result_node.msg)

if __name__ == "__main__":
    main()
