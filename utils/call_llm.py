"""
Утилита для вызова LLM (Language Model).

Предоставляет функции для отправки запросов к языковым моделям
и получения ответов. Текущая версия содержит mock-реализацию
для демонстрации работы архитектуры.

TODO: Интегрировать реальный API LLM (OpenAI, Anthropic, локальная модель и т.д.)
"""

import time


def call_llm(prompt: str, model: str = "mock", temperature: float = 0.7) -> str:
    """
    Отправляет запрос к LLM и возвращает ответ.

    В текущей версии используется mock-реализация для демонстрации.
    Для продакшн-использования необходимо заменить на реальный API вызов.

    Args:
        prompt: Текст запроса к LLM
        model: Название модели (по умолчанию "mock")
        temperature: Параметр температуры для генерации (0.0 - 1.0)

    Returns:
        str: Ответ от LLM

    Example:
        >>> response = call_llm("Что такое агентная система?")
        >>> print(response)

    TODO: Реализовать интеграцию с реальным LLM API:
    - OpenAI GPT-4 (через библиотеку openai)
    - Anthropic Claude (через библиотеку anthropic)
    - Локальная модель через Ollama
    - Другие провайдеры
    """
    # Имитация задержки API вызова
    time.sleep(0.5)

    # Mock-ответы в зависимости от содержимого промпта
    if "анализ" in prompt.lower() or "проанализируй" in prompt.lower():
        return _generate_analysis_response(prompt)
    elif "решение" in prompt.lower() or "определи" in prompt.lower():
        return _generate_decision_response(prompt)
    elif "выполни" in prompt.lower() or "действие" in prompt.lower():
        return _generate_action_response(prompt)
    else:
        return _generate_generic_response(prompt)


def _generate_analysis_response(prompt: str) -> str:
    """
    Генерирует mock-ответ для запросов на анализ.

    Args:
        prompt: Исходный промпт

    Returns:
        str: Mock-ответ с анализом
    """
    return """Анализ запроса:
1. Тип задачи: Информационный запрос, требующий структурированного ответа
2. Ключевые элементы: Необходимо предоставить чёткую информацию с примерами
3. Рекомендуемый подход: Использовать пошаговое объяснение с конкретными примерами

Запрос относится к категории задач, требующих систематического подхода к решению."""


def _generate_decision_response(prompt: str) -> str:
    """
    Генерирует mock-ответ для запросов на принятие решения.

    Args:
        prompt: Исходный промпт

    Returns:
        str: Mock-ответ с решением
    """
    return """Предоставить детальный структурированный ответ с объяснениями и примерами."""


def _generate_action_response(prompt: str) -> str:
    """
    Генерирует mock-ответ для запросов на выполнение действия.

    Args:
        prompt: Исходный промпт

    Returns:
        str: Mock-ответ с результатом действия
    """
    return """Демонстрационный ответ агентной системы Orai:

Это mock-реализация LLM вызова для демонстрации работы архитектуры PocketFlow.

Агентная система успешно обработала ваш запрос через следующие этапы:
- Получение и валидация входных данных
- Анализ задачи с определением типа и контекста
- Принятие решения о наиболее подходящем подходе
- Выполнение соответствующего действия

Для получения реальных ответов от LLM необходимо:
1. Выбрать провайдера LLM (OpenAI, Anthropic, локальная модель)
2. Получить API ключ
3. Установить соответствующую библиотеку (openai, anthropic и т.д.)
4. Обновить функцию call_llm() в utils/call_llm.py

Текущая версия демонстрирует корректную работу потока узлов и
передачу данных через общее хранилище (shared store)."""


def _generate_generic_response(prompt: str) -> str:
    """
    Генерирует общий mock-ответ.

    Args:
        prompt: Исходный промпт

    Returns:
        str: Общий mock-ответ
    """
    return f"""Получен запрос к LLM (mock-режим).

Исходный промпт содержал {len(prompt)} символов.

Это демонстрационный ответ, показывающий работу агентной системы Orai
на базе PocketFlow фреймворка.

Для работы с реальным LLM необходимо обновить функцию call_llm()
в файле utils/call_llm.py, добавив интеграцию с выбранным API."""


# Дополнительные утилитарные функции для будущего расширения

def validate_prompt(prompt: str) -> bool:
    """
    Валидирует промпт перед отправкой к LLM.

    Args:
        prompt: Промпт для проверки

    Returns:
        bool: True если промпт валиден, иначе False
    """
    if not prompt or not prompt.strip():
        return False
    if len(prompt) > 100000:  # Примерное ограничение
        return False
    return True


def format_prompt(template: str, **kwargs) -> str:
    """
    Форматирует промпт по шаблону с подстановкой параметров.

    Args:
        template: Шаблон промпта с плейсхолдерами
        **kwargs: Параметры для подстановки

    Returns:
        str: Отформатированный промпт

    Example:
        >>> template = "Ответь на вопрос: {question}. Контекст: {context}"
        >>> prompt = format_prompt(template, question="Что такое AI?", context="ML курс")
    """
    return template.format(**kwargs)
