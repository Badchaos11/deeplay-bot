from database.scheme.scheme import create_connection


def check_user(userid: int) -> bool:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `userid` FROM `users` WHERE `userid`=%s"
                cursor.execute(sql, (userid,))
                result = cursor.fetchone()
                if len(result) == 0:
                    print("Пользователя в базе нет")
                    return False
                else:
                    print("Пользователь есть в базе")
                    return True
        except:
            print("Ошибка при проверке пользователя")


def get_all_credits(userid: int) -> tuple:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `size`, `bank` FROM `credits` WHERE `userid`=%s"
                cursor.execute(sql, (userid,))
                result = cursor.fetchall()
                return result
        except:
            print("Ошибка при получении данных о кредитах")
            return ()


def check_credit_in_bank(userid: int, bank: str) -> bool:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `credits` WHERE `userid`=%s AND `bank`=%s"
                cursor.execute(sql, (userid, bank))
                if len(cursor.fetchone()) == 0:
                    print(f"Кредитов в банке {bank}  у пользователя {userid} нет")
                    return False
                else:
                    print(f"В банке {bank} у пользователя {userid} уже есть кредит")
                    return True
        except:
            print("Ошибка при проверке кредитов")


def get_credit_data(userid: int, bank: str) -> float:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `credits` WHERE `userid`=%s AND `bank`=%s"
                cursor.execute(sql, (userid, bank,))
                result = cursor.fetchone()
                return result['size']
        except:
            print("Ошибка при получении кредита")
