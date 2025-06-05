import json
import os

from mcts.MCTS import parse_response, MCTS
from dotenv import load_dotenv

from src.LLM.LLMController import LLMController

load_dotenv()

def get_char_history_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        history_str = f.read()

    return history_str

def main():
    history = get_char_history_from_file(os.getenv('HISTORY_FILE_PATH'))
    json_history = json.loads(history)

    controller = LLMController()
    # controller.list_models()
    print(controller.generate_actions(json_history, "flirt", m=8))
    # mcts = MCTS(
    #     max_tokens=max_tokens,
    #     k=2\,
    #     c=2,
    #     base_history=json_history,
    #     api_key=os.getenv('API_KEY'),
    # )
    #
    # mcts.init_root()
    # result_node = mcts.search(10)
    #
    # print("Best message: " + result_node.msg)

if __name__ == "__main__":
    main()
