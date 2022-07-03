from database.scheme.scheme import create_connection


# Методы обновления записей в базе данных

def update_credit(userid: int, size: float, bank: str) -> bool:  # Обновдение суммы кредита
    connection = create_connection()  # Установка соединения
    with connection:
        try:
            with connection.cursor() as cursor:  # Создание курсора для выполнения запросов
                sql = "UPDATE `credits` SET `size`=%s WHERE `userid`=%s AND `bank` = %s"  # Структура запроса
                cursor.execute(sql, (size, userid, bank))  # Выполнение запроса
            connection.commit()  # Подтверждение успешной транзакции
            print("Данные успешно обновлены")
            return True  # Сообщение результата боту
        except:
            print("Не удалось обновить данные")
            return False
