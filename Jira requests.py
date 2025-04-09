# from requests.auth import HTTPBasicAuth
# import requests

# JIRA_URL = "https://e-magnum.atlassian.net/rest/api/3/myself"
# USERNAME = "yermek.zhunuspekov@e-magnum.kz"
# PASSWORD = "ATATT3xFfGF0sMdchFgiMsuqyNoZjXlYjBq160PXImJaqefBAGaxSW5yb9ySa1cn8DQ85vpoVQu_aorjEmx98iUxkPvFjixz-1Rdyk79sMgOaMXbquK76wi3TLC3Sjkjh5wLk1wIXoOstbf10Uc3dHMyyaqbbG-pA6Mqs08DmSPCSDRKnXpOJcA=2CCED707"

# response = requests.get(
#    JIRA_URL,
#    auth=HTTPBasicAuth(USERNAME, PASSWORD),
#    verify=False  # Отключаем проверку SSL
# )

# print(response.json())  # Должны увидеть данные о пользователе

# #print(response.status_code)
# #print(response.text)  # Если это HTML — проблема с авторизацией

import requests
import pandas as pd
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

# Конфигурация Jira
JIRA_URL = "https://e-magnum.atlassian.net/rest/api/3/myself"
USERNAME = "yermek.zhunuspekov@e-magnum.kz"
PASSWORD = "ATATT3xFfGF0sMdchFgiMsuqyNoZjXlYjBq160PXImJaqefBAGaxSW5yb9ySa1cn8DQ85vpoVQu_aorjEmx98iUxkPvFjixz-1Rdyk79sMgOaMXbquK76wi3TLC3Sjkjh5wLk1wIXoOstbf10Uc3dHMyyaqbbG-pA6Mqs08DmSPCSDRKnXpOJcA=2CCED707"

# Определяем временные диапазоны
today = datetime.today()
last_week = today - timedelta(days=7)
next_week = today + timedelta(days=7)

# Функция для выполнения запроса в Jira API
def get_issues(jql_query):
    params = {
        "jql": jql_query,
        "maxResults": 100,
        "fields": "key,summary,status,assignee,duedate"
    }
    
    response = requests.get(
        JIRA_URL,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        params=params,
        verify=False  # Отключаем проверку SSL (если используется самоподписанный сертификат)
    )
    
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}: {response.text}")
        return []
    
    issues = response.json().get("issues", [])
    data = []
    
    for issue in issues:
        data.append([
            issue["key"],
            issue["fields"]["summary"],
            issue["fields"]["status"]["name"],
            issue["fields"]["assignee"]["displayName"] if issue["fields"]["assignee"] else "Не назначен",
            issue["fields"]["duedate"] if issue["fields"]["duedate"] else "Нет срока"
        ])
    
    return data

# JQL-запросы
PROJECT_KEY = "New"  # Укажи код своего проекта

done_query = f'project = "{PROJECT_KEY}" AND status = "Done" AND resolved >= "{last_week.strftime("%Y-%m-%d")}"'
in_progress_query = f'project = "{PROJECT_KEY}" AND status IN ("В разработке", "To Do")'
planned_query = f'project = "{PROJECT_KEY}" AND duedate >= "{today.strftime("%Y-%m-%d")}" AND duedate <= "{next_week.strftime("%Y-%m-%d")}"'

# Получаем задачи
done_issues = get_issues(done_query)
in_progress_issues = get_issues(in_progress_query)
planned_issues = get_issues(planned_query)

# Записываем данные в Excel
with pd.ExcelWriter("jira_tasks.xlsx") as writer:
    pd.DataFrame(done_issues, columns=["Ключ", "Название", "Статус", "Исполнитель", "Срок"]).to_excel(writer, sheet_name="Выполнено", index=False)
    pd.DataFrame(in_progress_issues, columns=["Ключ", "Название", "Статус", "Исполнитель", "Срок"]).to_excel(writer, sheet_name="В работе", index=False)
    pd.DataFrame(planned_issues, columns=["Ключ", "Название", "Статус", "Исполнитель", "Срок"]).to_excel(writer, sheet_name="В планах", index=False)

print("✅ Файл jira_tasks.xlsx успешно создан!")