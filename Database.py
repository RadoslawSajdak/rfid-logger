import mysql.connector as mysql
import const
from datetime import datetime

MAC_db = "F7:9F:CB:A6"

def setup():
    """ It gives You connection to database """
    db_connection = mysql.connect(host=const.HOST, database=const.DATABASE, user=const.USER, password=const.PASSWORD)
    print("Connected to:", db_connection.get_server_info())
    return db_connection


def get_status(MAC):
    """ Get status of item from database.

    Possibilities of return: AVAILABLE, NOT_AVAILABLE, NOT_PRESENT
    """
    cp_mac = (check_mac(MAC),)

    db_connection = setup()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Parts WHERE MAC = %s", cp_mac )
    status = cursor.fetchone()


    if status != None:
        return status[3]
    else:
        """ In our solution You should navigate to "add" window when you get "NOT_PRESENT" error """
        return "NOT_PRESENT"

def check_mac(MAC):
    """ MAC address is the most important data in our program so it should be always verified.

    You can use:
        - aaaaaaaa
        - aa:aa:aa:aa
        - AaaAaaaA
        - AA:aa:aA:aa
        etc. (where "a" is digit 0-9 or sign a-z)
    Function will change it to upper case and format to correct AA:AA:AA:AA
    """
    if len(MAC) == 11:
        t_mac = str(MAC).upper()
        if t_mac[2] == ":" and t_mac[5] == ":" and t_mac[8] == ":":
            return t_mac
        else:
            return "INPUT_ERROR"
    elif len(MAC) == 8:
        t_mac = ""
        for i in range(8):
            if i % 2 == 0 and i != 0:
                t_mac +=":"
            t_mac += MAC[i]
        MAC_db = t_mac.upper()
        return MAC_db
    else:
        return "INPUT_ERROR"


def get_order(MAC):
    """ Function to associate MAC of rented item with user. Function returns completly infos about
        user and item too as dictionaries.

        Examples of dictionaries are in consts.py
    """
    cp_mac = (check_mac(MAC),)
    rented_part = {}
    renting_person = {}

    db_connection = setup()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Parts WHERE MAC = %s", cp_mac )
    part = cursor.fetchone()
 
    # Get info about part #
    rented_part["mac"] = cp_mac[0]
    rented_part["part_id"] = part[0]
    rented_part["name"] = part[2]
    rented_part["status"] = part[3] # It is not necessary to use
    rented_part["return_date"] = part[4]

    # Get current owner info #
    cursor.execute("SELECT User_ID FROM Orders WHERE Part_ID = %s AND Available = 'NotReturned'", (part[0],) ) #TODO NotReturned -> NOT_RETURNED
    uid = cursor.fetchone()

    renting_person["user_id"] = uid[0]

    cursor.execute("SELECT * FROM Users WHERE User_ID = %s", (renting_person["user_id"],))
    user = cursor.fetchone()
 
    renting_person["name"] = user[1]
    renting_person["surname"] = user[2]
    renting_person["student_id"] = user[3]
    renting_person["email"] = user[4]
    renting_person["phone"] = user[5]

    return [renting_person, rented_part]

def add_item(MAC,name):
    """ 
    Simple adding item to database. You should insert name and MAC. Part ID will be added automatically in database.
    """
    cp_mac = (check_mac(MAC),)
    db_connection = setup()
    cursor = db_connection.cursor()

    # Adding new item #
    val = (cp_mac[0],name)
    cursor.execute("INSERT INTO Parts (MAC, Part_Name) VALUES (%s, %s)",val )
    db_connection.commit()

def rent_item(MAC,user):
    """ You can rent item (make a new order) using this function.
        Input "user" is a dictionary like in consts.py file.
        ret_date format is "yyyy-mm-dd"
    """
    cp_mac = (check_mac(MAC),)
    db_connection = setup()
    cursor = db_connection.cursor()

    # Get part ID
    cursor.execute("SELECT Part_ID FROM Parts WHERE MAC = %s", cp_mac )
    pid = cursor.fetchone()[0]

    # Get user ID
    try:
        cursor.execute("SELECT User_ID FROM Users WHERE Email = %s", (user["email"],) )
        uid = cursor.fetchone()[0]

        updates = "UPDATE Users SET Name = '" + user["name"] + "', Surname = '" + user["surname"] + "', StudentID = '" + user["student_id"] + "', Phone = '" + user["phone"] + "' WHERE Email = %s" 
        cursor.execute(updates,(user["email"],))
        db_connection.commit()

    except:
        cursor.execute("INSERT INTO Users (Name, Surname, StudentID, Email, Phone) VALUES (%s, %s,%s, %s,%s)",\
           (user["name"],user["surname"],user["student_id"],user["email"],user["phone"]))
        db_connection.commit()
        cursor.execute("SELECT User_ID FROM Users WHERE Email = %s", (user["email"],) )
        uid = cursor.fetchone()[0]

    # Make a new order
    cursor.execute("INSERT INTO Orders (User_ID, Part_ID,Rented, Return_date) VALUES (%s, %s, %s, %s)",\
        (uid,pid,str(datetime.today().strftime('%Y-%m-%d')),user["return_date"]) )
    db_connection.commit()

    # Change status of the part
    cursor.execute("UPDATE Parts SET Status = 'NOT_AVAILABLE' WHERE MAC = %s",cp_mac)
    db_connection.commit()

    sql = ("UPDATE `Parts` SET `Return_date` = '" + user["return_date"] + "' WHERE MAC = %s")
    cursor.execute(sql,cp_mac)

    db_connection.commit()


def get_one_part(MAC):
    single_part = {}
    cp_mac = (check_mac(MAC),)
    db_connection = setup()
    cursor = db_connection.cursor()

    # Get part ID
    cursor.execute("SELECT * FROM Parts WHERE MAC = %s", cp_mac )
    part_t = cursor.fetchone()

    single_part["part_id"] = part_t[0]
    single_part["mac"] = part_t[1]
    single_part["name"] = part_t[2]
    return single_part

def get_all_devices():
    single_part = {}
    parts_dictionary = []

    db_connection = setup()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Parts")
    part = cursor.fetchall()
    # Get info about part #
    for i in part:
        single_part["mac"] = i[1]
        single_part["part_id"] = i[0]
        single_part["name"] = i[2]
        single_part["status"] = i[3] # It is not necessary to use
        single_part["return_date"] = i[4]
        parts_dictionary.append(single_part.copy())
        print(parts_dictionary)
    return parts_dictionary

def prologue(part_id,date):
    db_connection = setup()
    cursor = db_connection.cursor()

    sql = "UPDATE Orders SET Return_date = '" + str(date) + "' WHERE Part_ID = '" + str(part_id) +"' AND Available = 'NotReturned'" #TODO NotReturned -> NOT_RETURNED
    cursor.execute(sql)

    db_connection.commit()
def return_item(MAC):
    cp_mac = (check_mac(MAC),)
    db_connection = setup()
    cursor = db_connection.cursor()
    part_id = get_one_part(MAC)["part_id"]
    cursor.execute("UPDATE Parts SET Status = 'AVAILABLE' WHERE MAC = %s", cp_mac )
    db_connection.commit()

    cursor.execute("UPDATE Parts SET Return_date = NULL WHERE MAC = %s", cp_mac )
    db_connection.commit()

    sql = "UPDATE Orders SET Return_date = '" + datetime.today().strftime('%Y-%m-%d') + "' WHERE Part_ID = '" + str(part_id) + "' AND Available = 'NotReturned' "
    cursor.execute(sql) #TODO Returned->RETURNED
    db_connection.commit()

    sql = "UPDATE Orders SET Available = 'Returned' WHERE Part_ID = '" + str(part_id) + "' AND Available = 'NotReturned' "#TODO NotReturned -> NOT_RETURNED
    cursor.execute(sql) #TODO Returned->RETURNED
    db_connection.commit()




if __name__ == "__main__":
    print(get_status(MAC))
    #return_item("0A:94:B1:1A")
    #prologue("11","2023-1-1")
    #print(check_mac(MAC))
    #print(get_order(MAC2))
    #add_item(MAC3,"Raspberry")
    #rent_item(MAC3,const.Users,"2021-01-12")
