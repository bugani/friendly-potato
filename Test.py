import requests
import json

# Пример JSON, который нужно распарсить
json_data = '''
{
    "metrics": [
        {
            "metricselector": "cpu_usage",
            "value": 50
        },
        {
            "metricselector": "memory_usage",
            "value": 70
        }
    ]
}
'''

# Парсинг JSON
data = json.loads(json_data)

# Извлечение всех полей metricselector
metric_selectors = [item['metricselector'] for item in data['metrics']]

# Настройки Grafana API
GRAFANA_URL = "http://your-grafana-url.com"
GRAFANA_API_KEY = "your-api-key"
DASHBOARD_TITLE = "My Dashboard"

# Создание дашборда в Grafana
def create_grafana_dashboard(metrics):
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_KEY}",
        "Content-Type": "application/json"
    }

    # Создание панелей для каждой метрики
    panels = []
    for i, metric in enumerate(metrics):
        panel = {
            "type": "graph",
            "title": metric,
            "gridPos": {
                "x": i % 2 * 12,
                "y": int(i / 2) * 8,
                "w": 12,
                "h": 8
            },
            "targets": [
                {
                    "expr": metric,
                    "refId": "A"
                }
            ]
        }
        panels.append(panel)

    # Создание дашборда
    dashboard = {
        "dashboard": {
            "title": DASHBOARD_TITLE,
            "panels": panels
        },
        "overwrite": False
    }

    # Отправка запроса на создание дашборда
    response = requests.post(
        f"{GRAFANA_URL}/api/dashboards/db",
        headers=headers,
        data=json.dumps(dashboard)
    )

    if response.status_code == 200:
        print("Дашборд успешно создан!")
    else:
        print(f"Ошибка при создании дашборда: {response.status_code}, {response.text}")

# Создание дашборда в Grafana
create_grafana_dashboard(metric_selectors)
