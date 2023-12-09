from common_variable import *

# sonarcloud에 전달할 목적으로 깃허브 레포지토리 id 가져오기
def get_project_id_gh2sc(GITHUB_API_TOKEN, NAME):
    GH_REPO = '%s/repos/%s' % (GH_API, NAME)
    response = requests.get('%s' % (GH_REPO), headers=headers)
    response = response.json()
    print(response['id'])
    return response['id']

def is_json(obj):
    try:
        test = obj.json()
    except Exception as e:
        return False
    return True

def create_project(SC_TOKEN, USER, PROJECT_NAME, CREATE_NAME, ORG):
    headers = {
        'Authorization': 'token %s' % (SC_TOKEN),
    }

    data = {
        'name': CREATE_NAME,
        'project': PROJECT_NAME,
        'organization': ORG,
    }

    response = requests.post('https://sonarcloud.io/api/projects/create', data=data, headers=headers)

    if (is_json(response)):
        response = response.json()
    print(response)
    return response

# 깃허브 레포지토리 연동된 프로젝트 만드는 함수
def create_project_linked_github(SC_GH_ORG, SC_GH_REPO, SC_ORG, SC_GH_KEY, SC_TOKEN):
    data = {
        'installationKeys': SC_GH_ORG + '/' + SC_GH_REPO + '|' + SC_GH_KEY,
        'organization': SC_ORG,
    }

    response = requests.post(
        'https://sonarcloud.io/api/alm_integration/provision_projects',
        data=data,
        auth=(SC_TOKEN, ''),
    )
    if (is_json(response)):
        response = response.json()
    print(response)
    return response

# 생성한 깃허브 기반 프로젝트의 자동스캔 기능을 허용하는 함수
def set_autoscan(SC_GH_ORG, SC_GH_REPO, SC_TOKEN):
    params = {
        'autoEnable': 'true',
        'projectKey': SC_GH_ORG + '_' + SC_GH_REPO,
    }

    response = requests.get(
        'https://sonarcloud.io/api/autoscan/eligibility',
        params=params,
        auth=(SC_TOKEN, ''),
    )
    if (is_json(response)):
        response = response.json()
    print(response)
    return response

# autoscan을 허용한 프로젝트를 분석하는 함수
def scan_project(SC_GH_ORG, SC_GH_REPO, SC_TOKEN):
    data = {
        'enable': 'true',
        'projectKey': SC_GH_ORG + '_' + SC_GH_REPO,
    }

    response = requests.post('https://sonarcloud.io/api/autoscan/activation', data=data, auth=(SC_TOKEN, ''))

    if (is_json(response)):
        response = response.json()
    print(response)
    return response

# 프로젝트가 분석이 끝났을 때 분석이 끝났음을 알리는 url을 설정하는 함수
def create_webhook(SC_GH_ORG, SC_GH_REPO, SC_ORG, URL, SC_TOKEN):
    data = {
        'name': SC_GH_ORG + '/' + SC_GH_REPO + '_webhook',
        'organization': SC_ORG,
        'url': 'https://dgu2022.requestcatcher.com/',
    }

    response = requests.post('https://sonarcloud.io/api/webhooks/create', data=data, headers=headers,
                             auth=(SC_TOKEN, ''))

    if (is_json(response)):
        response = response.json()
    print(response)
    return response

# 프로젝트 분석 결과 가져오는 함수
def get_value_metric(SC_GH_ORG, SC_GH_REPO, SC_ORG, METRIC, SC_TOKEN):
    params = {
        'component': SC_GH_ORG + '_' + SC_GH_REPO,
        'metricKeys': METRIC
    }

    response = requests.get(
        'https://sonarcloud.io/api/measures/component',
        params=params,
        auth=(SC_TOKEN, ''),
    )

    if (is_json(response)):
        response = response.json()
    print(response)
    return response


# 프로젝트 지우는 함수
def delete_project(key, SC_ORG, SC_TOKEN):
    params = {
        'project': key,
    }

    response = requests.post(
        'https://sonarcloud.io/api/projects/delete',
        params=params,
        auth=(SC_TOKEN, ''),
    )

    if (is_json(response)):
        response = response.json()
    print(response)
    return response


def get_score_sonarcloud(NAME):

    USER = 'dgu2022'
    CREATE_NAME = 'dgu2022-test'
    PROJECT_NAME = 'sonarcube-repeat'
    ORG = 'dgu2022'
    SC_ORG = 'dgu2022'
    METRIC = 'complexity,cognitive_complexity,duplicated_lines_density,code_smells,bugs,vulnerabilities,comment_lines'

    SC_GH_ORG = NAME.split('/')[0]
    SC_GH_REPO = NAME.split('/')[-1]
    #SC_GH_ORG = NAME.split('_')[0]
    #SC_GH_REPO = NAME.split('_')[-1]
    SC_GH_KEY = str(get_project_id_gh2sc(GITHUB_API_TOKEN, NAME))

    create_project_linked_github(SC_GH_ORG, SC_GH_REPO, SC_ORG, SC_GH_KEY, SC_TOKEN)
    set_autoscan(SC_GH_ORG, SC_GH_REPO, SC_TOKEN)
    scan_project(SC_GH_ORG, SC_GH_REPO, SC_TOKEN)
    create_webhook(SC_GH_ORG, SC_GH_REPO, SC_ORG, URL, SC_TOKEN)
