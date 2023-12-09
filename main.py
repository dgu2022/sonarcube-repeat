from fastapi import FastAPI
from github_score_12 import *
from get_profile import *
from sonarcloud-crawling import *
import pickle

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
            get_score_sonarcloud(NAME)

        with open('project_data_last.pkl', 'wb') as f:
            normalize_data = pickle.load(f)

        df = pd.DataFrame(normalize_data)

        for key in list(normalize_data.keys()):
            df = detect_outliers(df, key, 30)

        df_normalization = (df - df.min()) / (df.max() - df.min())





