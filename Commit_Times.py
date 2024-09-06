# item : https://github.com/maxam2017/productive-box
# Commit Search : https://docs.github.com/ko/search-github/searching-on-github/searching-commits
# Search Ranking : https://docs.github.com/ko/rest/search/search?apiVersion=2022-11-28#ranking-search-results
# Gist Content update : https://docs.github.com/ko/rest/reference/gists#update-a-gist-comment
# Get Generate token : https://github.com/settings/tokens -> New personal access token -> check repo and gists -> Expiration : need for you to set -> Generate token -> copy token
# Gist : https://gist.github.com/ -> new gist -> Name : Commit_Times -> Create public gist -> copy url -> https://gist.github.com/yourname/************* <- '*************' is Gist ID
# Repo Setting -> secrets and variables -> actions -> New repository secret -> Name :ACCESS_TOKEN -> paste token -> Add secret
# Repo Setting -> secrets and variables -> actions -> New repository secret -> Name :GIST_ID -> paste Gist ID -> Add secret

import os
from collections import defaultdict
from datetime import datetime

import requests

# GitHub Personal Access Token (optional)
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # 없을 경우 None으로 설정

# Your GitHub Username
USER_NAME = os.getenv('USER_NAME')

# Setting Gist ID
SETTING_GIST_ID = os.getenv('GIST_ID')

def get_repos(USER_NAME, ACCESS_TOKEN):
    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/users/{USER_NAME}/repos?per_page={per_page}&page={page}"
        headers = {}
        if ACCESS_TOKEN:
            headers["Authorization"] = f"token {ACCESS_TOKEN}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()

        if len(data) == 0:
            break

        repos.extend(data)
        page += 1

    return repos

def get_commits(repo_full_name, ACCESS_TOKEN):
    commits = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page={per_page}&page={page}"
        headers = {}
        if ACCESS_TOKEN:
            headers["Authorization"] = f"token {ACCESS_TOKEN}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()

        if len(data) == 0:
            break

        for commit in data:
            commit['repository'] = {'full_name': repo_full_name}  # 저장소 정보 추가

        commits.extend(data)
        page += 1

    return commits

def categorize_commit_time(commit_time):
    hour = commit_time.hour
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Daytime"
    elif 18 <= hour < 24:
        return "Evening"
    else:
        return "Night"

# 모든 저장소 가져오기
repos = get_repos(USER_NAME, ACCESS_TOKEN)

# 모든 커밋 가져오기
all_commits = []
for repo in repos:
    repo_full_name = repo['full_name']
    commits = get_commits(repo_full_name, ACCESS_TOKEN)
    all_commits.extend(commits)

# 시간대별 커밋 수 집계
commit_times = defaultdict(int)
for commit in all_commits:
    commit_time = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
    time_category = categorize_commit_time(commit_time)
    commit_times[time_category] += 1

# 전체 커밋 수 계산
total_commits = sum(commit_times.values())

# 시간대별 심볼
time_symbols = {
    "Morning": "🌞",
    "Daytime": "🌆",
    "Evening": "🌃",
    "Night": "🌙"
}

# 바 차트 생성 함수
def create_bar(count, total, length=20):  # 길이를 20으로 줄임
    bar_length = int((count / total) * length)
    return '█' * bar_length + '░' * (length - bar_length)

# 결과를 Gist에 업데이트
gist_content = ""
for time_category, count in commit_times.items():
    percentage = (count / total_commits) * 100
    symbol = time_symbols.get(time_category, "")
    bar = create_bar(count, total_commits)
    gist_content += f"{symbol} {time_category:<8} {count:>4} ({percentage:>5.2f}%) {bar:>22}\n"

gist_update_url = f"https://api.github.com/gists/{SETTING_GIST_ID}"
headers = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {
    "files": {
        "Commit_times": {
            "content": gist_content
        }
    }
}

response = requests.patch(gist_update_url, headers=headers, json=data)

if response.status_code == 200:
    print("Gist updated successfully.")
else:
    print(f"Failed to update Gist: {response.status_code}")
