import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.api import head

load_dotenv()

CSV_FILE = os.getenv("CSV_PATH")
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.clockify.me/api/v1"
HEADER = {"X-Api-Key": API_KEY}


def get_workspaces_id() -> list:
    url = API_URL + "/workspaces"
    request = requests.get(url, headers=HEADER)
    workspaces = request.json()
    return [workspace["id"] for workspace in workspaces]


def get_clients(workspace_id: str) -> dict:
    url = API_URL + f"/workspaces/{workspace_id}/clients"
    request = requests.get(url, headers=HEADER)
    return request.json()


def post_time(client: str, start: str, end: str) -> str:
    url = API_URL + f"/workspaces/{workspace_id}/time-entries"
    data = {"clientId": client, "start": start, "end": end}
    return requests.post(url, headers=HEADER, json=data)


def push_time_from_csv(
    workspace_id: str, path: str, start_col: str = "start", end_col: str = "end"
) -> None:
    csv = pd.read_csv(CSV_FILE)
    for index, row in csv.iterrows():
        print(index, row)
    post_time(row["task"], row["start"], row["end"])

if __name__ == "__main__":
    push_time_from_csv(CSV_FILE)
    # workspaces_id = get_workspaces_id()
    # for workspace_id in workspaces_id:
    #     clients = get_clients(workspace_id)
    #     for client in clients:
    #         print(client["name"])
    #         print()
