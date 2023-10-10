import mysql.connector

connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database='db')
print("DB connected")

cursor = connection.cursor()
cursor.execute('Select * FROM students')
students = cursor.fetchall()


first = input("First Name:")
lastN = input("Last Name:")
script = 'INSERT INTO students(FirstName, Surname) VALUES(%s,%s)'
info = (first,lastN)
cursor.execute(script,info)

# Confirmar los cambios en la base de datos
connection.commit()

cursor.execute('Select * FROM students')
students = cursor.fetchall()
connection.close()

print(students)
