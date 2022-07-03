from database.scheme.scheme import create_connection


# Методы добавления новых записей в таблицу

def add_user(userid: int) -> bool:  # Добавление нового пользователя в таблицу
    connection = create_connection()  # Установка соединения с базой данных
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора для выполнения запросо
                sql = "INSERT INTO `users` (`userid`) VALUES (%s)"  # Структура запроса
                cursor.execute(sql, (userid,))  # Выполнение запроса

            connection.commit()  # Подтверждение результата при успешном выполнении транзакции
            return True  # Сообщение боту, что операция прошла успешно
        except:
            print("Пользователь не был добавлен")  # Сообщение об ошибке


def add_credit(userid: int, size: float, bank: str) -> bool:  # Добавление нового кредита
    connection = create_connection()  # Установка соединения с базой данных
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора
                sql = "INSERT INTO `credits` (`userid`, `size`, `bank`) VALUES (%s, %s, %s)"  # Структура запроса
                cursor.execute(sql, (userid, size, bank))  # Выполнение запроса

            connection.commit()  # Подтверждение успешной транзакции
            return True  # Сообщение боту об успехе
        except:
            print("Ошибка при добавлении нового кредита")
            return False
