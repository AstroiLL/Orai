"""
Модуль с определениями узлов для агентной системы Orai.

Каждый узел наследуется от Node и реализует три метода:
- prep(shared): подготовка данных из общего хранилища
- exec(prep_res): выполнение основной логики узла
- post(shared, prep_res, exec_res): постобработка и выбор следующего узла
"""

from pocketflow import Node
from utils.call_llm import call_llm


class InputNode(Node):
    """Узел для получения входных данных от пользователя."""

    def exec(self, _):
        # Запрашиваем у пользователя вопрос или задачу
        user_input = input("Введите ваш вопрос или задачу: ")
        return user_input

    def post(self, shared, prep_res, exec_res):
        # Сохраняем входные данные в общее хранилище
        shared["user_input"] = exec_res
        shared["history"] = []  # Инициализируем историю действий
        return "default"  # Переходим к следующему узлу


class AnalyzeNode(Node):
    """Узел для анализа задачи через LLM."""

    def prep(self, shared):
        # Извлекаем входные данные пользователя
        return shared["user_input"]

    def exec(self, user_input):
        # Формируем промпт для анализа задачи
        prompt = f"""Проанализируй следующий запрос пользователя и определи:
1. Тип задачи (вопрос, расчёт, поиск информации, и т.д.)
2. Ключевые элементы, которые нужно учесть
3. Рекомендуемый подход к решению

Запрос пользователя: {user_input}

Предоставь краткий структурированный анализ."""

        # Вызываем LLM для анализа
        analysis = call_llm(prompt)
        return analysis

    def post(self, shared, prep_res, exec_res):
        # Сохраняем результаты анализа
        shared["analysis"] = exec_res
        shared["history"].append(f"Анализ: {exec_res[:100]}...")
        return "default"


class DecisionNode(Node):
    """Узел для принятия решения о дальнейших действиях."""

    def prep(self, shared):
        # Извлекаем данные для принятия решения
        return {
            "user_input": shared["user_input"],
            "analysis": shared["analysis"]
        }

    def exec(self, prep_data):
        # Формируем промпт для принятия решения
        prompt = f"""На основе анализа определи, какое действие следует предпринять.

Запрос: {prep_data['user_input']}
Анализ: {prep_data['analysis']}

Предложи конкретное действие для решения задачи (одним предложением)."""

        # Вызываем LLM для принятия решения
        decision = call_llm(prompt)
        return decision

    def post(self, shared, prep_res, exec_res):
        # Сохраняем принятое решение
        shared["decision"] = exec_res
        shared["history"].append(f"Решение: {exec_res}")
        return "default"


class ActionNode(Node):
    """Узел для выполнения действия на основе принятого решения."""

    def prep(self, shared):
        # Извлекаем все необходимые данные
        return {
            "user_input": shared["user_input"],
            "analysis": shared["analysis"],
            "decision": shared["decision"]
        }

    def exec(self, prep_data):
        # Формируем промпт для выполнения действия
        prompt = f"""Выполни следующее действие и предоставь результат.

Исходный запрос: {prep_data['user_input']}
Анализ: {prep_data['analysis']}
Действие: {prep_data['decision']}

Предоставь детальный ответ или результат выполнения."""

        # Вызываем LLM для выполнения действия
        result = call_llm(prompt)
        return result

    def post(self, shared, prep_res, exec_res):
        # Сохраняем результат действия
        shared["action_result"] = exec_res
        shared["history"].append(f"Выполнено: {exec_res[:100]}...")
        return "default"


class OutputNode(Node):
    """Узел для форматирования и вывода финального результата."""

    def prep(self, shared):
        # Извлекаем все данные для финального вывода
        return {
            "user_input": shared["user_input"],
            "action_result": shared["action_result"],
            "history": shared["history"]
        }

    def exec(self, prep_data):
        # Форматируем финальный ответ
        output = f"""
{'='*60}
РЕЗУЛЬТАТ РАБОТЫ АГЕНТНОЙ СИСТЕМЫ ORAI
{'='*60}

Ваш запрос:
{prep_data['user_input']}

Результат:
{prep_data['action_result']}

{'='*60}
История обработки:
{chr(10).join(f'- {item}' for item in prep_data['history'])}
{'='*60}
"""
        return output

    def post(self, shared, prep_res, exec_res):
        # Сохраняем финальный результат
        shared["final_output"] = exec_res
        # Выводим результат на экран
        print(exec_res)
        return "default"  # Завершаем выполнение потока
