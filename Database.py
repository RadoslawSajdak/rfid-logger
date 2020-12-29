import mysql.connector as mysql
import const


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
        return t_mac.upper()
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
    cursor.execute("SELECT User_ID FROM Orders WHERE Part_ID = %s", (part[0],) )
    uid = cursor.fetchone()
    print(uid)
    renting_person["user_id"] = uid[0]

    cursor.execute("SELECT * FROM Users WHERE User_ID = %s", uid )
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

def rent_item(MAC,user,ret_date):
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
    except:
        cursor.execute("INSERT INTO Users (Name, Surname, StudentID, Email, Phone) VALUES (%s, %s,%s, %s,%s)",\
           (user["name"],user["surname"],user["student_id"],user["email"],user["phone"]))
        db_connection.commit()
        cursor.execute("SELECT User_ID FROM Users WHERE Email = %s", (user["email"],) )
        uid = cursor.fetchone()[0]
    # Make a new order
    cursor.execute("INSERT INTO Orders (User_ID, Part_ID,Return_date) VALUES (%s, %s, %s)",\
        (uid,pid,ret_date) )
    db_connection.commit()





if __name__ == "__main__":
    #print(get_status(MAC))
    #print(check_mac(MAC))
    #print(get_order(MAC2))
    #add_item(MAC3,"Raspberry")
    #rent_item(MAC3,const.Users,"2021-01-12")