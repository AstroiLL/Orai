"""
Модуль для создания потоков агентной системы Orai.

Определяет последовательность выполнения узлов и их соединение
в единый рабочий поток обработки запросов пользователя.
"""

from pocketflow import Flow
from nodes import (
    InputNode,
    AnalyzeNode,
    DecisionNode,
    ActionNode,
    OutputNode
)


def create_agent_flow():
    """
    Создаёт и возвращает агентный поток для обработки запросов пользователя.

    Поток включает следующие этапы:
    1. InputNode - получение входных данных от пользователя
    2. AnalyzeNode - анализ задачи через LLM
    3. DecisionNode - принятие решения о действиях
    4. ActionNode - выполнение действия
    5. OutputNode - форматирование и вывод результата

    Returns:
        Flow: Настроенный поток агентной системы
    """
    # Создаём экземпляры узлов
    input_node = InputNode()
    analyze_node = AnalyzeNode()
    decision_node = DecisionNode()
    action_node = ActionNode()
    output_node = OutputNode()

    # Соединяем узлы в последовательную цепочку
    # Используем оператор >> для определения направления потока
    input_node >> analyze_node >> decision_node >> action_node >> output_node

    # Создаём и возвращаем поток, начинающийся с входного узла
    return Flow(start=input_node)


# Создаём глобальный экземпляр потока для использования в main.py
agent_flow = create_agent_flow()
