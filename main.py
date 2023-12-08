from fastapi import FastAPI
from github_score_12 import *
from get_profile import *

app = FastAPI()

@app.post("/")
def get_score(name: str):
    list_project_name = get_profile_project_list(name)
    if len(list_project_name) < 1:
        print("프로젝트 수 부족")
        return -1
    else:
        list_project_score = []
        for project_name in list_project_name:
            dict_project_score = get_score_main(project_name)
            list_project_score.append(dict_project_score)