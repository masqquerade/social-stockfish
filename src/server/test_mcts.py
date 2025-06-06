import json
import requests
import os

def test_mcts_generation(file_path):
    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    
    # Формируем запрос
    url = "http://localhost:8000/api/mcts/generate"
    payload = {
        "file_path": file_path,
        "iterations": 3,
        "k": 2,
        "c": 2.0
    }
    
    print(f"\nSend request with file: {file_path}")
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("\nSucsefully generated message:")
            print(f"ID of message in db: {result['message_id']}")
            print(f"Message: {result['message']}")
            print(f"Score: {result['score']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to server. Ensure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Testing MCTS message generation from file")
    print("=============================================")
    
    while True:
        # Запрашиваем путь к файлу у пользователя
        file_path = input("\nEnter the path to the JSON file: ")
        test_mcts_generation(file_path)
        
        if input("\nDo you want to generate another message? (y/n): ").lower() != 'y':
            break
    
    print("\nThank you for using!")