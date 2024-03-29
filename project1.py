import sqlite3
import sys
from datetime import date

def main():
    try:
        connection = sqlite3.connect(sys.argv[1])
    except:
        print("Missing Arguments")
        sys.exit()
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    connection.commit()
    utype = ''
    uid = ''

    while utype != "exit":
        utype, uid = login_screen(connection)
        if utype == "a":
            display_ra_functionalities(cursor, connection, uid)
        elif utype == "o":
            display_to_functionalities(connection)

    connection.close()
    sys.exit()


def login_screen(connection):
    user_true = False
    pwd_true = False

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT uid, pwd, utype FROM users;")
    rows = cursor.fetchall()

    print("Welcome! This is the login screen.")
    print("Type Exit to quit the program.\n")

    while user_true == False:
        username = input("Please enter your username: ")
        if username.lower() != "exit":
            for each in rows:
                if each["uid"].lower() == username.lower():
                    if check_password(each, pwd_true) == True:
                        user_true = True
                        return each["utype"].lower(), each["uid"]
                    else:
                        return "exit", None
            if user_true != True:
                print("Incorrect Username, please try again\n ")
        else:
            return "exit", None


def check_password(each, pwd_true):
    while pwd_true == False:
        password = input("Please enter your password: ")
        if password.lower() != "exit":
            if each["pwd"] == password:
                pwd_true = True
            if pwd_true != True:
                print("Incorrect Password, please try again\n ")
        if password.lower() == "exit":
            return pwd_true
    
    return pwd_true


def display_ra_functionalities(cursor, connection, uid):
    command = None
    while command != "7":
        print("\nYou are logged in as a Registry Agent")
        print("\nType Help in the command line to display commands\n")
        command = input("Please enter a command: ")
        if command.lower() == "help":
            print("Enter the number associated with each command to use command\n"
                  """Commands: (1) Register a birth
          (2) Register a marriage
          (3) Renew a vehicle registeration
          (4) Process a bill of sale
          (5) Process a payment
          (6) Get a driver abstract
          (7) Logout""")
        elif command not in ["1","2","3","4","5","6","7","help"]:
            print("Incorrect command. Please try again")
        elif command == "1":
            register_birth(cursor, connection, uid)
        elif command == "2":
            registerMarriage(cursor, connection, uid)
        elif command == "3":
            renew_vregistration(cursor, connection)
        elif command == "4":
            sellCar(cursor, connection)
        elif command == "5":
            payment(cursor, connection)
        elif command == "6":
            get_driver_abstract(connection)
        

def display_to_functionalities(connection):
    command = None
    while command != "3":
        print("\nYou are logged in as a Traffic Officer\n")
        print("Type Help in the command line to display commands\n")
        command = input("Please enter a command: ")
        if command.lower() == "help":
            print("Enter the number associated with each command to use command\n"
                  """Commands: (1) Issue a ticket
          (2) Find a car owner
          (3) Logout\n""")
        elif command not in ["1","2","3","help"]:
            print("Incorrect command. Please try again")
        elif command == "1":
            issue_ticket(connection)
        elif command == "2":
            find_car_owner(connection)



def register_birth(cursor, conn, login):

    cursor.execute('select max(regno) from births')
    bregno = cursor.fetchone()

    if bregno[0] == None:
        bregno = 1
    else:
        bregno = bregno[0] + 1

    bfname = ''
    blname = ''

    while bfname == '':
        bfname = input('What is the first name of the baby: ')
    while blname == '':
        blname = input('What is the last name of the baby: ')

    bregdate = date.today() 
    bregdate = bregdate.strftime('%Y-%m-%d')

    cursor.execute('select u.city from users u where u.uid = ?;', (login,))
    bregplace = cursor.fetchone()
    bregplace = bregplace[0]

    nbplace = input('What is the birth place: ')
    if nbplace =='':
        nbplace = None

    bgender = 'l'

    while bgender != 'M' and bgender != 'F':

        bgender = input('What is the gender of the child (M or F)?: ')
        bgender = bgender.upper()
    
    p1Fname = input('What is the first name the Mother: ')
    p1Lname = input('What is the last name of the Mother: ')

    #check if Mother exists
    p1Fname, p1Lname = find_person(p1Fname, p1Lname, conn)

    if p1Fname  == False and p1Lname == False:

        print('Mother info missing please enter the missing data')

        p1Fname = input('Please enter the first name of Mother: ')
        p1Lname = input('Please enter the last name of Mother: ')
        pabDate	= input('Please enter the birthdate of Mother: ')
        pabPlace = input('Please enter the birthplace of Mother: ')
        paAddress = input('Please enter the address of Mother: ')
        paPhone = input('Please enter the phone number of Mother: ')

        while p1Fname == '':
            p1Fname = input('Please enter the first name of Mother: ')
        while p1Lname == '':
            p1Lname = input('Please enter the last name of Mother: ')

        if pabDate == '':
            pabDate = None
        if pabPlace == '':
            pabPlace = None
        if paAddress == '':
            paAddress = None
        if paPhone == '':
            paPhone = None

        cursor.execute('insert into persons values (?, ?, ?, ?, ?, ?);', (p1Fname, p1Lname, pabDate, pabPlace, paAddress, paPhone))
        conn.commit()
    
    p2Fname = input('What is the first name of the Father: ')
    p2Lname = input('What is the last name of the Father: ')

    #check existence of Father
    p2Fname, p2Lname = find_person(p2Fname, p2Lname, conn)

    if p2Fname  == False and p2Lname == False:

        print('Father info missing please enter the missing data')
        
        p2Fname = input('Please enter the first name of Father: ')
        p2Lname = input('Please enter the last name of Father: ')
        pabDate = input('Please enter the birthdate of Father: ')
        pabPlace = input('Please enter the birthplace of Father: ')
        paAddress = input('Please enter the address of Father: ')
        paPhone = input('Please enter the phone number of Father: ')

        while p2Fname == '':
            p2Fname = input('Please enter the first name of Father: ')
        while p2Lname == '':
            p2Lname = input('Please enter the last name of Father: ')

        if pabDate == '':
            pabDate = None
        if pabPlace == '':
            pabPlace = None
        if paAddress == '':
            paAddress = None
        if paPhone == '':
            paPhone = None

        cursor.execute('insert into persons values (?, ?, ?, ?, ?, ?);', (p2Fname, p2Lname, pabDate, pabPlace, paAddress, paPhone))
        conn.commit()
    

    #create the persons entry
    nbdate = input('Please enter the birthdate of the baby: ')
    if nbdate == '':
        nbdate = None

    cursor.execute('select p.address from persons p where p.fname = ? and p.lname = ?;', (p1Fname, p1Lname))
    baddress = cursor.fetchone()
    baddress = baddress[0]

    cursor.execute('select p.phone from persons p where p.fname = ? and p.lname = ?;', (p1Fname, p1Lname))
    bphone = cursor.fetchone()
    bphone = bphone[0]

    cursor.execute('insert into persons values (?, ?, ?, ?, ?, ?);', (bfname, blname, nbdate, nbplace, baddress, bphone))
    conn.commit()

    cursor.execute('insert into births values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (bregno, bfname, blname, bregdate, bregplace, bgender, p2Fname, p2Lname, p1Fname, p1Lname))
    conn.commit()

def registerMarriage(cursor, conn, login):

    p1Fname = input('Please enter the first name of Partner 1: ')
    p1Lname = input('Please enter the last name of Partner 1: ')
    p2Fname = input('Please enter the first name of Partner 2: ')
    p2Lname = input('Please enter the last name of Partner 2: ')

    mregdate = date.today()
    mregdate = mregdate.strftime('%Y-%m-%d')

    cursor.execute('select max(regno) from marriages')
    mregno = cursor.fetchone()


    if mregno[0] == None:
        mregno = 1
    else:
        mregno = mregno[0] + 1

    p1Fname, p1Lname = find_person(p1Fname, p1Lname, conn)

    if p1Fname  == False and p1Lname == False:

        print('Partner 1 info missing please enter the missing data')

        p1Fname = input('Please enter the first name of Partner 1: ')
        p1Lname = input('Please enter the last name of Partner 1: ')
        pabDate	= input('Please enter the birthdate of Partner 1: ')
        pabPlace = input('Please enter the birthplace of Partner 1: ')
        paAddress = input('Please enter the address of Partner 1: ')
        paPhone = input('Please enter the phone number of Partner 1: ')

        while p1Fname == '':
            p1Fname = input('Please enter the first name of Partner 1: ')
        while p1Lname == '':
            p1Lname = input('Please enter the last name of Partner 1: ')
        
        if pabDate == '':
            pabDate = None
        if pabPlace == '':
            pabPlace = None
        if paAddress == '':
            paAddress = None
        if paPhone == '':
            paPhone = None

        cursor.execute('insert into persons values (?, ?, ?, ?, ?, ?);', (p1Fname, p1Lname, pabDate, pabPlace, paAddress, paPhone))
        conn.commit()

    
    p2Fname, p2Lname = find_person(p2Fname, p2Lname, conn)

    if p2Fname  == False and p2Lname == False:

        print('Partner 2 info missing please enter the missing data')

        p2Fname = input('Please enter the first name of Partner 2: ')
        p2Lname = input('Please enter the last name of Partner 2: ')
        pabDate	= input('Please enter the birthdate of Partner 2: ')
        pabPlace = input('Please enter the birthplace of Partner 2: ')
        paAddress = input('Please enter the address of Partner 2: ')
        paPhone = input('Please enter the phone number of Partner 2: ')

        while p2Fname == '':
            p2Fname = input('Please enter the first name of Partner 2: ')
        while p2Lname == '':
            p2Lname = input('Please enter the last name of Partner 2: ')

        if pabDate == '':
            pabDate = None
        if pabPlace == '':
            pabPlace = None
        if paAddress == '':
            paAddress = None
        if paPhone == '':
            paPhone = None

        cursor.execute('insert into persons values (?, ?, ?, ?, ?, ?);', (p2Fname, p2Lname, pabDate, pabPlace, paAddress, paPhone))
        conn.commit()

    cursor.execute('select u.city from users u where u.uid = ?;', (login,))
    mregplace = cursor.fetchone()
    mregplace = mregplace[0]
    cursor.execute('insert into marriages values (?, ?, ?, ?, ?, ?, ?);', (mregno, mregdate, mregplace, p1Fname, p1Lname, p2Fname, p2Lname))
    conn.commit()


def renew_vregistration(cursor, conn):

    vregno = input('Please enter the vehicles registration number: ')
    today = date.today()

    exp = None
    while exp == None:
        cursor.execute('select r.expiry from registrations r where r.regno = ?;', (vregno,))
        exp = cursor.fetchone()
        if exp == None:
            vregno = input('Please enter a valid registration number: ')
    
    exp = exp[0]
    currexp = exp.split('-')
    ndate = today
    ndate = ndate.replace(year = int(currexp[0]), month = int(currexp[1]), day = int(currexp[2]))
    
    if today >= ndate:

        ndate = today
        ndate = ndate.replace(year = today.year + 1)
        
    else:
        
        ndate = ndate.replace(year = ndate.year + 1)
    
    ndate = ndate.strftime('%Y-%m-%d')

    cursor.execute('update registrations set expiry = ? where regno = ?;', (ndate, vregno,))
    conn.commit()

def sellCar(cursor, conn):

    cvin = input('Please enter the vin of the car: ')
    ofname = input('Please enter the first name of the current owner: ')
    olname = input('Please enter the last name of the current owner: ')
    nfname = input('Please enter the first name of the new owner: ')
    nlname = input('Please enter the last name of the new owner: ')

    cursor.execute('select * from registrations where vin = ?;', (cvin,))
    check = cursor.fetchone()
    if check == None:

        print('Invalid vin')
        return

    cursor.execute('select fname from registrations where vin = ? order by regdate DESC limit 1;', (cvin,))
    cfname = cursor.fetchone()
    cfname = cfname[0]

    cursor.execute('select lname from registrations where vin = ? order by regdate DESC limit 1;', (cvin,))
    clname = cursor.fetchone()
    clname = clname[0]

    if cfname.lower() != ofname.lower() and clname.lower() != olname:
        print('Invalid seller')
        return 0

    nfname, nlname = find_person(nfname, nlname, conn)
    if nfname == False and nlname == False:
        print("Error: Cant find new owner in persons")
        return

    nplate = input('Please enter the new plate number: ')
    oexpdate = date.today()
    nexpdate = oexpdate
    nexpdate = nexpdate.replace( year = nexpdate.year + 1)
    oexpdate = oexpdate.strftime('%Y-%m-%d')
    nexpdate = nexpdate.strftime('%Y-%m-%d')

    cursor.execute('select regno from registrations where vin = ? order by regdate DESC limit 1;', (cvin,))
    oregno = cursor.fetchone()
    oregno = oregno[0]

    cursor.execute('update registrations set expiry = :oexpdate where regno = :oregno;', {'oexpdate': oexpdate, 'oregno': oregno})

    cursor.execute('select max(regno) from registrations')
    nregno = cursor.fetchone()
    nregno = nregno[0] + 1
    
    cursor.execute('insert into registrations values (?, ?, ?, ?, ?, ?, ?);', (nregno, oexpdate, nexpdate, nplate, cvin, nfname, nlname))
    conn.commit()

#Find Person in Persons and returns ther first and last name
def find_person(fname, lname, connection):
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    fname = fname
    lname = lname

    cursor.execute('select * from persons')
    row = cursor.fetchall()
    for each in row:
        if fname.lower() == each["fname"].lower() and lname.lower() == each["lname"].lower():
            return each["fname"], each["lname"]
    
    return False, False


def payment(cursor, conn):

    ptno = input('Please enter the ticket number for the ticket that is being paid: ')

    cursor.execute('select fine from tickets where tno = ?;', (ptno,))
    tfine = cursor.fetchone()

    if tfine == None:

        print('Invalid ticket number')
        return

    tfine = int(tfine[0])

    pamount = input('Please enter the amount being paid: ')
    pamount = int(pamount)
    
    cursor.execute('select sum(amount) as total from payments where tno = ? group by tno;', (ptno,))
    psum = cursor.fetchone()
    if psum != None:
        psum = psum[0]

        if (pamount + psum) > tfine:

            pmax = tfine - psum
            print('Invalid payment:too high max payment for this fine is ', pmax)
            return

    elif psum == None:
        if pamount > tfine:
            print('Invalid payment:too high max payment for this fine is', tfine)
            return

    today = date.today()
    pdate = today.strftime("%Y-%m-%d")

    try:
        cursor.execute('insert into payments values (?, ?, ?);', (ptno, pdate, pamount))
    except:
        print("Cant pay ticket twice in one day")
        return
        
    conn.commit()

def issue_ticket(connection):
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM registrations left outer join vehicles using (vin);")
    r_rows = cursor.fetchall()
    reg_number = input("\nPlease enter a registration number: ")

    for r_each in r_rows:

        if r_each["regno"] == int(reg_number):
            print("Name:", r_each["fname"], r_each["lname"], "Make:", r_each["make"], "Model:", 
            r_each["model"], "Year:", r_each["year"], "Colour:", r_each["color"])


            
            violation_date = input("\nPlease enter a violation date: ")
            if violation_date == "":
                today = date.today()
                violation_date = today.strftime("%Y-%m-%d")

            violation_text = input("Please enter violation text: ")
            fine_amount = input("Please enter a fine amount: ")

            regno = r_each["regno"]
            cursor.execute("SELECT MAX(tno) FROM tickets")
            tno = cursor.fetchone()
            cursor.execute("INSERT INTO tickets VALUES (?, ?, ?, ?, ?)", (tno[0]+1, regno, int(fine_amount), violation_text, violation_date))
            
            connection.commit()
            return

    print("\nRegistration number does not exist")
    return


def find_car_owner(connection):
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vehicles left outer join registrations using (vin)")
    rows = cursor.fetchall()

    variable_dict = {}
    for key in ["make", "model", "year", "color", "plate"]:
        variable = input("Please enter " + key + " of vehicle: ")
        if variable != "":
            variable_dict[key] = variable.lower()

    keys = list(variable_dict.keys())
    vins = []
    if len(variable_dict) == 1:
        for each in rows:
            if str(each[keys[0]]).lower() == variable_dict[keys[0]]:
                vins.append(each["vin"])
    elif len(variable_dict) == 2:
        for each in rows:
            if str(each[keys[0]]).lower() == variable_dict[keys[0]] and str(each[keys[1]]).lower() == variable_dict[keys[1]]:
                vins.append(each["vin"])
    elif len(variable_dict) == 3:
       for each in rows:
            if str(each[keys[0]]).lower() == variable_dict[keys[0]] and str(each[keys[1]]).lower() == variable_dict[keys[1]] and str(each[keys[2]]).lower() == variable_dict[keys[2]]:
                vins.append(each["vin"])
    elif len(variable_dict) == 4:
        for each in rows:
            if (str(each[keys[0]]).lower() == variable_dict[keys[0]] and str(each[keys[1]]).lower() == variable_dict[keys[1]] and str(each[keys[2]]).lower() == variable_dict[keys[2]] 
                and str(each[keys[3]]).lower() == variable_dict[keys[3]]):
                vins.append(each["vin"])
    elif len(variable_dict) == 5:
        for each in rows:
            if (str(each[keys[0]]).lower() == variable_dict[keys[0]] and str(each[keys[1]]).lower() == variable_dict[keys[1]] and str(each[keys[2]]).lower() == variable_dict[keys[2]] 
                and str(each[keys[3]]).lower() == variable_dict[keys[3]] and str(each[keys[4]]).lower() == variable_dict[keys[4]]):
                vins.append(each["vin"])
    
    if len(vins) < 4 and len(vins) > 0:
        for num in range(len(vins)):
            cursor.execute("SELECT * FROM vehicles left outer join registrations using (vin) where vin =:vin and fname IS NOT NULL group by vin having max(regdate)", {"vin": vins[num]})
            row = cursor.fetchone()
            if row == None:
                print("Car has no owner")
                return
            print("Make:", row["make"], "Model:", row["model"], "Year:", row["year"], "Color:", row["color"], "Plate:", row["plate"], "Registration Date:", row["regdate"],
                  "Expiry Date:", row["expiry"], "Name:", row["fname"], row["lname"])
    elif len(vins) >= 4:
        for num in range(len(vins)):
            cursor.execute("SELECT * FROM vehicles left outer join registrations using (vin) where vin =:vin and fname IS NOT NULL group by vin having max(regdate)", {"vin": vins[num]})
            row = cursor.fetchone()
            print("(", num,")" + " Make:", row["make"], "Model:", row["model"], "Year: ", row["year"], "Color:", row["color"], "Plate:", row["plate"])
        input_num = input("\nPlease enter the number of the car you would like to select: ")
        cursor.execute("SELECT * FROM vehicles left outer join registrations using (vin) where vin = :vin and fname IS NOT NULL group by vin having max(regdate)", {"vin": vins[int(input_num)]})
        row = cursor.fetchone()
        print("Make:", row["make"], "Model:", row["model"], "Year:", row["year"], "Color:", row["color"], "Plate:", row["plate"], "Registration Date:", row["regdate"],
              "Expiry Date:", row["expiry"], "Name:", row["fname"], row["lname"])
    elif len(vins) == 0:
        print("\nNo matches")


def get_driver_abstract(connection):
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    f_name = input("Please enter a first name: ")
    l_name = input("Please enter a last name: ")

    cursor.execute("SELECT count(regno) as tiknum, fname, lname FROM tickets left outer join registrations using (regno) group by fname, lname")
    rows = cursor.fetchall()
    tik_num = 0
    for each in rows:
        if (each["fname"].lower() == f_name.lower() and each["lname"].lower() == l_name.lower()):
            tik_num = each["tiknum"]
            database_fname = each["fname"]
            database_lname = each["lname"]

    cursor.execute("SELECT count()as demcount, fname, lname, sum(points) as demsum FROM demeritNotices group by fname, lname")
    rows = cursor.fetchall()
    dem_count = 0
    sum_count_lifetime = 0
    for each in rows:
        if (each["fname"].lower() == f_name.lower() and each["lname"].lower() == l_name.lower()):
            dem_count = each["demcount"]
            sum_count_lifetime = each["demsum"]
            database_fname = each["fname"]
            database_lname = each["lname"]

    cursor.execute("SELECT sum(points) as demsum, fname, lname FROM demeritNotices where ddate > date('now', '-2 year') group by fname, lname")
    rows = cursor.fetchall()
    sum_count_latest = 0
    for each in rows:
        if (each["fname"].lower() == f_name.lower() and each["lname"].lower() == l_name.lower()):
            sum_count_latest = each["demsum"]
            database_fname = each["fname"]
            database_lname = each["lname"]
    
    print("\nNumber of Tickets:", tik_num, "Number of demerit notices:", dem_count, "Total demerit points within two years:", sum_count_latest, 
          "Total demerit points within lifetime:", sum_count_lifetime)

    if tik_num == 0:
        return

    option = input("\nWould you like to see the tickets ordered from lastest to oldest (Yes/No): ")

    if option.lower() == "yes":
        cursor.execute("SELECT * FROM tickets left outer join registrations using (regno) left outer join vehicles using (vin) where fname =:f_name and lname =:l_name order by vdate DESC", {"f_name": database_fname, "l_name": database_lname})
        rows = cursor.fetchall()
        display_tickets(rows)
    elif option.lower() == "no":
        cursor.execute("SELECT * FROM tickets left outer join registrations using (regno) left outer join vehicles using (vin) where fname =:f_name and lname =:l_name order by vdate", {"f_name": database_fname, "l_name": database_lname})
        rows = cursor.fetchall()
        display_tickets(rows)
    return


def display_tickets(rows):
    if len(rows) > 5:
            right_point = 4
            left_point = 0

            while right_point < len(rows):
                for i in range(left_point, right_point + 1):
                    print("Ticket number:", rows[i]["tno"], "Violation date: ", rows[i]["vdate"], "Violation description: ", rows[i]["violation"], "Fine: ", rows[i]["fine"],
                           " Registration number: ", rows[i]["regno"], "Make: ", rows[i]["make"], "Model: ", rows[i]["model"])
                
                if right_point == len(rows) - 1:
                    return
                
                show_more = input("\nThere are more tickets to be shown would you like to show them? (Yes/No): ")

                if show_more.lower() == "yes":
                    right_point += 5
                    left_point += 5
                    if right_point >= len(rows):
                        for i in range(left_point, len(rows)):
                            print("Ticket number:", rows[i]["tno"], "Violation date: ", rows[i]["vdate"], "Violation description: ", rows[i]["violation"], "Fine: ", rows[i]["fine"],
                                " Registration number: ", rows[i]["regno"], "Make: ", rows[i]["make"], "Model: ", rows[i]["model"])
                elif show_more.lower() == "no":
                    return

    elif len(rows) <= 5:
        for each in rows:
            print("\nTicket number:", each["tno"], "Violation date:", each["vdate"], "Violation description:", each["violation"], "Fine:", each["fine"],
                    " Registration number:", each["regno"], "Make:", each["make"], "Model:", each["model"])



if __name__ == "__main__":
    main()
