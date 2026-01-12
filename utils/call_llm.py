"""
Утилита для вызова LLM (Language Model).

Предоставляет функции для отправки запросов к языковым моделям
и получения ответов. Использует OpenAI API.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

# Загрузка переменных окружения из .env файла
load_dotenv()

# Инициализация клиента OpenAI
_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")
_default_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if _api_key:
    client = OpenAI(api_key=_api_key, base_url=_base_url)
else:
    client = None


def call_llm(prompt: str, model: str = None, temperature: float = 0.7) -> str:
    """
    Отправляет запрос к LLM и возвращает ответ.

    Args:
        prompt: Текст запроса к LLM
        model: Название модели (по умолчанию из OPENAI_MODEL или "gpt-4o-mini")
        temperature: Параметр температуры для генерации (0.0 - 1.0)

    Returns:
        str: Ответ от LLM

    Raises:
        ValueError: Если не настроен API ключ
        Exception: При ошибке API вызова

    Example:
        >>> response = call_llm("Что такое агентная система?")
        >>> print(response)
    """
    if client is None:
        raise ValueError(
            "OpenAI API ключ не найден. Установите переменную OPENAI_API_KEY в .env файле"
        )

    if model is None:
        model = _default_model

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Ошибка при вызове LLM: {e}") from e


# Дополнительные утилитарные функции

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
    if len(prompt) > 100000:
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


def get_models() -> list[str]:
    """
    Получает список доступных моделей.

    Returns:
        list[str]: Список идентификаторов моделей

    Raises:
        ValueError: Если не настроен API ключ
    """
    if client is None:
        raise ValueError(
            "OpenAI API ключ не найден. Установите переменную OPENAI_API_KEY в .env файле"
        )

    try:
        models = client.models.list()
        return [m.id for m in models.data]
    except Exception as e:
        raise Exception(f"Ошибка при получении списка моделей: {e}") from e


def is_configured() -> bool:
    """
    Проверяет, настроен ли OpenAI клиент.

    Returns:
        bool: True если API ключ установлен, иначе False
    """
    return client is not None
