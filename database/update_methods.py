from database.scheme.scheme import create_connection


def update_credit(userid: int, size: float, bank: str) -> bool:
    connection = create_connection()
    with connection:
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `credits` SET `size`=%s WHERE `userid`=%s AND `bank` = %s"
                cursor.execute(sql, (size, userid, bank))
            connection.commit()
            print("Данные успешно обновлены")
            return True
        except:
            print("Не удалось обновить данные")
            return False

