import logging.config
from logging_config import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger('calculate_logger')


def addition_numbers(numbers: list[float]) -> float:
    logger.info(f"Start of execution of the 'addition_numbers' function."
                f" Received data {numbers}")

    amount = 0.0
    for i_number in numbers:
        amount += i_number

    logger.info(f"The received answer is {amount}\n")
    return amount


def subtracting_numbers(numbers: list[float]) -> float:
    logger.info(f"Start of execution of the 'subtracting_numbers' function"
                f" Received data {numbers}")

    for i_number in range(1, len(numbers)):
        numbers[0] -= numbers[i_number]

    logger.info(f"The received answer is {numbers[0]}\n")
    return numbers[0]
