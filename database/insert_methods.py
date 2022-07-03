from database.scheme.scheme import create_connection


def add_user(userid: int) -> bool:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `users` (`userid`) VALUES (%s)"
                cursor.execute(sql, (userid,))

            connection.commit()
            return True
        except:
            print("Пользователь не был добавлен")


def add_credit(userid: int, size: float, bank: str) -> bool:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `credits` (`userid`, `size`, `bank`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (userid, size, bank))

            connection.commit()
            return True
        except:
            print("Ошибка при добавлении нового кредита")
            return False
