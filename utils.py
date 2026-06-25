import re

def validate_email(text):
    """
    проверяет, является ли текст корректной введенная почта
    здесь выполняется обязательное требование по использованию re
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, text):
        return True
    return False
