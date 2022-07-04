from database.scheme.scheme import create_connection


# Методы для получения данных из базы данных

def check_user(userid: int) -> bool:  # ППроверка на наличие пользователя в базе
    connection = create_connection()  # Установка соединения
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора для выполнения запросов
                sql = "SELECT `userid` FROM `users` WHERE `userid`=%s"  # Структура запроса
                cursor.execute(sql, (userid,))  # Выполнение запроса
                result = cursor.fetchone()  # Получение одного результата
                if result is None:  # Проверка на то, что результат есть
                    print("Пользователя в базе нет")
                    return False  # Сообщение боту результата
                else:
                    print("Пользователь есть в базе")
                    return True  # Сообщение боту результата
        except:
            print("Ошибка при проверке пользователя")


def get_all_credits(userid: int) -> tuple:  # Получение данных по всем кредитам пользователя
    connection = create_connection()  # Установка соединения с базой данных
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора
                sql = "SELECT `size`, `bank` FROM `credits` WHERE `userid`=%s"  # Структура запроса
                cursor.execute(sql, (userid,))  # Выполнение запроса
                result = cursor.fetchall()  # Получение всех результатов
                return result  # Отправка результата боту
        except:
            print("Ошибка при получении данных о кредитах")


def check_credit_in_bank(userid: int, bank: str) -> bool:  # Проверка на наличие у пользователя кредита в банке
    connection = create_connection()  # Установка соединения
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора
                sql = "SELECT * FROM `credits` WHERE `userid`=%s AND `bank`=%s"  # Структура запроса
                cursor.execute(sql, (userid, bank))  # Выполнение запроса
                result = cursor.fetchone()
                if result is None:  # Проверка на наличие результата
                    print(f"Кредитов в банке {bank}  у пользователя {userid} нет")  # Вывод результата в консоль
                    return False  # Сообщение результата боту
                else:
                    print(f"В банке {bank} у пользователя {userid} уже есть кредит")
                    return True  # Сообщение результата боту
        except:
            print("Ошибка при проверке кредитов")


def get_credit_data(userid: int, bank: str) -> float:  # Получение суммы кредита
    connection = create_connection()  # Установка соединения
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора
                sql = "SELECT * FROM `credits` WHERE `userid`=%s AND `bank`=%s" # Структура запроса
                cursor.execute(sql, (userid, bank,))  # Выполнение запроса
                result = cursor.fetchone()  # Получение результата
                return result['size']  # Отправка результата боту
        except:
            print("Ошибка при получении кредита")
