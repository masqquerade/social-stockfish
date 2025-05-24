import os

from mcts.MCTS import MCTS
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

from src.LLM.MessagesCreationAgent import MessagesCreationAgent

load_dotenv()

def get_char_history_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        history_str = f.read()

    return history_str

def parse_response(message):
    raw = message.content[0].text
    wrapped = f"<root>{raw}</root>"
    root = ET.fromstring(wrapped)

    parsed_msg = root.find("suggested_message")
    return parsed_msg

def main():
    history = get_char_history_from_file(os.getenv('HISTORY_FILE_PATH'))
    parsed_msgs = []
    # mcts = MCTS(
    #     k=3,
    #     c=2,
    #     base_history=history,
    #     api_key=os.getenv('API_KEY')
    # )
    #
    # mcts.init_root()
    # result_node = mcts.search(100)
    #
    # print(result_node.msg)

    mca = MessagesCreationAgent(os.getenv('API_KEY'))
    for msg in mca.get_messages(history, 1):
        parsed_msgs.append(parse_response(msg))

    for msg in parsed_msgs:
        print(msg.text.strip())

if __name__ == "__main__":
    main()
