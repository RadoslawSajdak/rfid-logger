def user_data():
    user = {"name": "Johny", "user_id" : 1, "surname":"Silverhand","student_id": "303030",\
        "email" : "Janek@gmail.com", "phone": "123456789", "project": "Moyo"}
    return user

def get_parts():
    parts = ({"name":"Arduimo UNO","return_date":"10.12.2020","status":"notreturned","part_id":0, "mac":"123qwe"},\
        {"name":"Arduimo DUE","return_date":"śmieci","status":"available","part_id":1, "mac":"234tyu"})
    return parts

def get_part():
    part = get_parts()
    return part[1]