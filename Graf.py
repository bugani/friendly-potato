import json
import re
import requests

# Функция для преобразования формата metricSelector
def transform_metric_selector(metric_selector):
    # Извлечение выражения из metricSelector
    match = re.search(r'filter\(and\(or\(eq\(Dimension,"([^"]+)"\)\)\)\)', metric_selector)
    if match:
        dimension_value = match.group(1)
        # Преобразование в Prometheus-подобный формат
        return f'calc_service_requesttime{{Dimension="{dimension_value}"}}'
    return None

# Функция для создания дашборда в Grafana
def create_grafana_dashboard(metrics):
    GRAFANA_URL = "http://your-grafana-url.com"
    GRAFANA_API_KEY = "your-api-key"
    DASHBOARD_TITLE = "My Dashboard"

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

# Основной код
def main():
    # Открытие и чтение JSON-файла
    with open('doc.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Поиск всех значений metricSelector
    metric_selectors = []
    def find_metric_selectors(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "metricSelector":
                    metric_selectors.append(value)
                elif isinstance(value, (dict, list)):
                    find_metric_selectors(value)
        elif isinstance(obj, list):
            for item in obj:
                find_metric_selectors(item)

    find_metric_selectors(data)

    # Преобразование metricSelector в нужный формат
    transformed_metrics = []
    for metric_selector in metric_selectors:
        transformed_metric = transform_metric_selector(metric_selector)
        if transformed_metric:
            transformed_metrics.append(transformed_metric)

    # Вывод преобразованных метрик
    print("Преобразованные метрики:")
    for metric in transformed_metrics:
        print(metric)

    # Создание дашборда в Grafana
    create_grafana_dashboard(transformed_metrics)

# Запуск программы
if __name__ == "__main__":
    main()
