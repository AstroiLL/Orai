# CLAUDE.md

Этот файл содержит руководство для Claude Code (claude.ai/code) при работе с кодом в этом репозитории.

## Обзор проекта

Orai — это Python-проект (версия 0.1.0), находящийся на ранней стадии разработки. Проект использует Python 3.12+ и управляется пакетным менеджером uv.

## Окружение для разработки

Проект использует:
- Python 3.12 (указано в `.python-version`)
- uv для управления зависимостями (указано в `pyproject.toml`)
- Виртуальное окружение в `.venv/`

### Команды для настройки

Активировать виртуальное окружение:
```bash
source .venv/bin/activate
```

Запустить основное приложение:
```bash
python main.py
```

Установить зависимости (когда будут добавлены):
```bash
uv pip install -e .
```

## Структура проекта

Текущая минимальная структура:
- `main.py` - точка входа с функцией `main()`
- `pyproject.toml` - метаданные проекта и зависимости
- `.venv/` - виртуальное окружение

## Соглашения о коде

**ВАЖНО:** Все комментарии в коде должны быть написаны на русском языке.

## Архитектура проекта

### Основа: PocketFlow

Проект построен на **PocketFlow** — минималистичном LLM-фреймворке (100 строк кода, без зависимостей).

**Основные концепции:**
- **Node (Узел)** — базовая единица логики с тремя методами:
  - `prep(shared)` — подготовка данных из общего хранилища
  - `exec(prep_res)` — выполнение основной логики
  - `post(shared, prep_res, exec_res)` — сохранение результатов и выбор следующего узла
- **Flow (Поток)** — соединение узлов через оператор `>>`
- **Shared Store** — общее хранилище (словарь) для обмена данными между узлами

### Структура проекта

```
orai/
├── main.py              # Точка входа приложения
├── nodes.py             # Определения узлов агентной системы
├── flow.py              # Создание и настройка потоков
├── utils/               # Утилиты (LLM вызовы и др.)
│   ├── __init__.py
│   └── call_llm.py      # Функция для вызова LLM
├── docs/                # Документация
│   └── design.md        # Детальное описание архитектуры
├── pyproject.toml       # Метаданные проекта
└── requirements.txt     # Зависимости Python
```

### Текущая реализация

Агентная система с последовательным потоком из 5 узлов:

1. **InputNode** → Получение входных данных от пользователя
2. **AnalyzeNode** → Анализ запроса через LLM
3. **DecisionNode** → Принятие решения о действиях
4. **ActionNode** → Выполнение действия
5. **OutputNode** → Форматирование и вывод результата

Поток данных:
```
user_input → analysis → decision → action_result → final_output
```

Все данные передаются через `shared` store (словарь Python).

### Agentic Coding: 8-шаговый процесс разработки

**Философия:** "Люди проектируют, агенты кодят"

1. **Requirements (Требования)** — оценка применимости AI для задачи
2. **Flow Design (Дизайн потока)** — создание высокоуровневой оркестрации
3. **Utilities (Утилиты)** — реализация внешних функций (API, файлы, инструменты)
4. **Data Design (Дизайн данных)** — структура shared store для коммуникации узлов
5. **Node Design (Дизайн узлов)** — планирование чтения/записи данных каждым узлом
6. **Implementation (Реализация)** — создание узлов и потоков
7. **Optimization (Оптимизация)** — итерация через prompt engineering и in-context learning
8. **Reliability (Надёжность)** — добавление retry, логирования, self-evaluation

### Команды для работы

```bash
# Запуск приложения
python main.py

# Установка зависимостей
uv pip install -r requirements.txt

# Обновление зависимостей
uv pip install --upgrade pocketflow
```

### Работа с узлами

При добавлении нового узла:

```python
# В nodes.py
from pocketflow import Node

class МойУзел(Node):
    def prep(self, shared):
        # Извлечение данных из shared store
        return shared.get("некоторые_данные")

    def exec(self, prep_res):
        # Основная логика узла
        result = обработать(prep_res)
        return result

    def post(self, shared, prep_res, exec_res):
        # Сохранение результатов
        shared["мой_результат"] = exec_res
        return "default"  # имя следующего действия
```

При обновлении потока:

```python
# В flow.py
новый_узел = МойУзел()
существующий_узел >> новый_узел >> следующий_узел
```

### LLM интеграция

Текущая версия использует mock-реализацию LLM в `utils/call_llm.py`.

Для интеграции реального LLM:

1. Выберите провайдера (OpenAI, Anthropic, Ollama)
2. Установите библиотеку: `uv pip install openai` (или anthropic)
3. Обновите функцию `call_llm()` в `utils/call_llm.py`
4. Добавьте API ключ в переменные окружения

Пример интеграции с OpenAI:

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt, model="gpt-4", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content
```

### Расширение системы

**Добавление ветвлений:**
```python
def post(self, shared, prep_res, exec_res):
    if условие:
        return "действие_а"  # переход к узлу с этим именем
    else:
        return "действие_б"
```

**Добавление циклов:**
```python
def post(self, shared, prep_res, exec_res):
    iteration = shared.get("iteration", 0)
    if iteration < max_iterations:
        shared["iteration"] = iteration + 1
        return "повторить"  # возврат к предыдущему узлу
    return "default"
```

## Архитектурные заметки

Подробное описание архитектуры, контрактов данных и дизайна узлов см. в `docs/design.md`.
