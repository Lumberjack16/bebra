import mysql.connector
# З'єднання з базою даних
connection = mysql.connector.connect(
    host='localhost',  # або 'ip' для локального сервера
    user='root',
    password='root',
    port=2023  # порт, на якому працює MySQL
)
# Створення об'єкта курсора
cursor = connection.cursor()
name_base="civilization3"
cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(name_base))

# оберем базу
cursor.execute("USE {0}".format(name_base))
cursor.execute("DELETE FROM users WHERE id_user=%s",(18,))

connection.commit()
cursor.close()
connection.close()