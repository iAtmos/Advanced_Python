import logging
import getpass
import hashlib


prohibited_password = []
logger = logging.getLogger('password_checker')


def is_prohibited_password():
    with open("prohibited.txt", 'r', encoding='utf-8') as words:
        for i_words in words:
            for i_word in i_words.split():
                if len(i_word) > 4:
                    prohibited_password.append(i_word)
    logger.info("Список запрещенных слов создан")


def is_strong_password(password):
    if password in prohibited_password:
        logger.info("Пароль совпадает с запрещенным словом")
        return False

    return True


def input_and_check_password():
    logger.debug("Начало input_and_check_password ")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))
        if hasher == "098f6bcd4621d373cade4e832627b4f6" and is_strong_password(password):
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)
        return False


if __name__ == "__main__":
    is_prohibited_password()
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аунтифицироваться в SkillBox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввел неверный пароль")
    exit(1)