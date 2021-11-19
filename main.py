import sqlite3 as sql


class Person:
    def __init__(self, iin, name):
        self.iin = iin
        self.name = name

    def show_persons(self):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("Select * from Person")
        persons = cursor.fetchall()
        print("IIN" + "\t\t\t\t" + "NAME")
        for person in persons:
            print(person[0] + "\t" + person[1])
        conn.commit()
        conn.close()

    def show_my_fines_by_iin(self, iin):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("Select * from Fine "
                       "inner join Person "
                       "on Fine.car_owner = Person.iin "
                       "WHERE car_owner = (?) ", (iin,))
        fines = cursor.fetchall()
        print("ID" + "\t" + "IIN" + "\t\t\t\t" + "Reg.Number" + "\t" + "NAME")
        for fine in fines:
            print(str(fine[0]) + "\t" + fine[1] + "\t" + fine[2] + "\t" + fine[4])
        conn.commit()
        conn.close()

    def add_fine_by_user_id(self):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()

        cursor.execute("SELECT rowid, * from Person")
        peoples = cursor.fetchall()
        print("ID" + "\t" + "IIN" + "\t\t\t\t" + "NAME")
        for people in peoples:
            print(str(people[0]) + "\t" + people[1] + "\t" + people[2])

        print("\nInput a ID of person to add FINE:")
        a = input('ID: ')

        for people in peoples:
            if str(people[0]) == a:
                fullname = str(people[2])
                IIN = str(people[1])
        conn.commit()

        list_cars = []
        cursor.execute("Select * from Car")
        cars = cursor.fetchall()
        for car in cars:
            if car[1] == IIN:
                list_cars.append(car)
        conn.commit()

        if len(list_cars) > 1:

            for carp in list_cars:
                print("Car number:", carp[0])
            print("Enter a reg.number of car")
            gos = input("Reg.Number: ")
            fee = Car('', '')
            fee.add_fine_by_reg_number(gos)

        elif len(list_cars) == 1:
            print("Car number:", list_cars[0][0])
            ide = list_cars[0][0]
            feticsh = Car('', '')
            feticsh.add_fine_by_reg_number(ide)

        else:
            print(" else else else else else else ")

        conn.commit()
        conn.close()


class Car:
    def __init__(self, car_reg_number, car_owner):
        self.car_reg_number = car_reg_number
        self.car_owner = car_owner

    def show_cars(self):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ROWID, * FROM Car")
        cars = cursor.fetchall()
        print("ID" + "\t" + "CAR_NUMBER" + "\t" + "OWNER_IIN")
        for car in cars:
            print(str(car[0]) + "\t" + car[1] + "\t" + car[2])
        conn.commit()
        conn.close()

    def show_fine_by_car_number(self, num):
        print("Fines:")
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("Select * from Fine "
                       "inner join Person "
                       "on Fine.car_owner = Person.iin "
                       "WHERE car_reg_number = (?) ", (num,))
        fines = cursor.fetchall()
        print("ID" + "\t" + "IIN" + "\t\t\t\t" + "Reg.Number" + "\t" + "NAME")
        for fine in fines:
            print(str(fine[0]) + "\t" + fine[1] + "\t" + fine[2] + "\t" + fine[4])
        conn.commit()
        conn.close()

    def db_add_fine(self, o_iin, reg_num):
        # print(o_iin, reg_num)
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Fine(car_owner, car_reg_number) VALUES(?,?)", (o_iin, reg_num))
        conn.commit()
        conn.close()
        print("Added to the FINE successfully!")

    def add_fine_by_reg_number(self, num):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Car")
        cars = cursor.fetchall()
        for car in cars:
            if str(car[0]) == str(num):
                reg_num = car[0]
                o_iin = car[1]
                self.db_add_fine(o_iin, reg_num)

        conn.commit()
        conn.close()

    def add_fine_by_car(self, ide):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()

        cursor.execute("SELECT ROWID, * FROM Car")
        cars = cursor.fetchall()
        for car in cars:
            if str(car[0]) == str(ide):
                reg_num = car[1]
                o_iin = car[2]
                self.db_add_fine(o_iin, reg_num)

        conn.commit()
        conn.close()


class Fine:
    def __init__(self, fine_id, car_owner, car_reg_number):
        self.fine_id = fine_id
        self.car_owner = car_owner
        self.car_reg_number = car_reg_number

    def delete_fine(self, ide):
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Fine WHERE fine_id = (?)", (ide,))
        conn.commit()
        conn.close()
        print("Successfully removed from FINE's")

    def see_all_fines(self):
        print("\nList of FINES:")
        conn = sql.connect("Final.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Fine.fine_id, Fine.car_reg_number, Person.name, Fine.car_owner "
                       "from Fine "
                       "inner join Person "
                       "on Fine.car_owner = Person.iin")
        fines = cursor.fetchall()
        print("ID" + "\t" + "Reg.Number" + "\t" + "Owner Name" + "\t" + "IIN")
        for fine in fines:
            print(str(fine[0]) + "\t" + fine[1] + "\t" + fine[2] + "\t\t" + fine[3])
        conn.commit()
        conn.close()

    def person_without_fine(self):
        print("List of peoples without FINE's")
        conn = sql.connect("Final.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name from Person WHERE iin NOT IN ( SELECT car_owner FROM Fine )")
        persons = cursor.fetchall()
        for person in persons:
            print(person[0])
        conn.commit()
        conn.close()


def choices():
    print("\nWelcome to the Fine management app!")
    print("(1) See fines by user ID\n"
          "(2) See fines by car reg.number\n"
          "(3) Add fine by user ID\n"
          "(4) Add fine by car reg.number\n"
          "(5) Erase fine by fine ID\n"
          "(6) See all fines\n"
          "(7) See people without fines\n"
          "(8) Exit\n")


def main():
    while True:
        choices()
        ch = input("Enter a number: ")
        if ch == '1':
            ma = Person('', '')
            ma.show_persons()
            print("Input a IIN of person")
            iin = input("IIN: ")
            ma.show_my_fines_by_iin(iin)

        elif ch == '2':
            ca = Car('', '')
            ca.show_cars()
            print('Input a car reg.number')
            num = input('Reg.Number:')
            ca.show_fine_by_car_number(num)

        elif ch == '3':
            p = Person('', '')
            p.add_fine_by_user_id()

        elif ch == '4':
            machine = Car('', '')
            machine.show_cars()
            print("Enter ID to add fine to the car")
            ide = int(input("ID: "))
            machine.add_fine_by_car(ide)

        elif ch == '5':
            fi = Fine('', '', '')
            fi.see_all_fines()
            print("Enter a ID which you wanna erase from FINE's")
            ide = int(input("ID: "))
            fi.delete_fine(ide)

        elif ch == '6':
            f = Fine('', '', '')
            f.see_all_fines()

        elif ch == '7':
            without = Fine('', '', '')
            without.person_without_fine()

        elif ch == '8':
            print("Exiting...")
            exit(0)
        else:
            print("*******************************\n"
                  "* Enter a number NOT a string *\n"
                  "*******************************")


main()
