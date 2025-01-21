import numpy as np


def guess_number(number: int) -> int:
    """Угадываем число с использованием бинарного поиска.

    Args:
        number (int): Загаданное число.

    Returns:
        int: Число попыток.
    """
    low, high = 1, 100
    attempts = 0

    while low <= high:
        attempts += 1
        guess = (low + high) // 2  # среднее значение
        if guess == number:
            return attempts
        elif guess < number:
            low = guess + 1
        else:
            high = guess - 1

    raise ValueError("Число не найдено. Проверьте входные данные.")


def evaluate_algorithm(guess_function, trials: int = 1000, seed: int = 1) -> float:
    """Оцениваем среднее количество попыток для угадывания.

    Args:
        guess_function (function): Функция угадывания.
        trials (int): Количество запусков.

    Returns:
        float: Среднее число попыток.
    """
    np.random.seed(seed)  # для воспроизводимости
    random_numbers = np.random.randint(1, 101, size=trials)
    attempts = [guess_function(number) for number in random_numbers]
    mean_attempts = np.mean(attempts)
    return mean_attempts


if __name__ == "__main__":
    avg_attempts = evaluate_algorithm(guess_number, seed=42)  # Устанавливаем seed
    print(f"Среднее количество попыток: {avg_attempts}")
    if avg_attempts < 20:
        print("Условие выполнено: среднее количество попыток меньше 20.")
    else:
        print("Условие не выполнено.")