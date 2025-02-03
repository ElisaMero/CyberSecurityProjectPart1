from database import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint


# fix 3: remove answer from the function:
def register(username, password, answer):
    try:
        query = text(
            "INSERT INTO users SET username='" + username + "', password='" + password + "', answer='" + answer + "'")
        db.session.execute(query)
        db.session.commit()
    except:
        return False
    return login(username, password)


# fix 2 and 4:
# def register(username, password):
#  hash_value = generate_password_hash(password)
#  try:
#     query = text("INSERT INTO users (username,password) VALUES (:username,:password)")
#     db.session.execute(query, {"username": username, "password": hash_value})
#     db.session.commit()
#   except:
#      return False
#   return login(username, password)


def login(username, password):
    query = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(query, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        return False

# fix 3: remove this function:


def check_question(username, answer):
    query = text(
        "SELECT id, answer FROM users WHERE username=:username AND answer=:answer")
    result = db.session.execute(
        query, {"username": username, "answer": answer})
    user = result.fetchone()
    if not user:
        return False
    return True


def user_id():
    return session.get("user_id", 0)


def logout():
    del session["user_id"]


def add_plant(name, latinname, light, water, other):
    visibility = "visible"
    check_name = text(
        "SELECT name FROM plant WHERE user_id = :id AND visibility=:visibility")
    result = db.session.execute(
        check_name, {"id": session["user_id"], "visibility": visibility})
    name_list = result.fetchall()
    for i in name_list:
        if i[0] == name:
            return False
    try:
        query = text(
            "INSERT INTO plant (name, latinname, light, water, other, user_id, visibility) VALUES (:name, :latinname, :light, :water, :other, :user_id, :visibility)")
        db.session.execute(query, {"name": name, "latinname": latinname, "light": light,
                           "water": water, "other": other, "user_id": session["user_id"], "visibility": visibility})
        db.session.commit()
    except:
        return False
    return True


def count_plants():
    visibility = "visible"
    query = text(
        "SELECT count(*) FROM plant WHERE user_id = :id AND visibility=:visibility")
    result = db.session.execute(
        query, {"id": session["user_id"], "visibility": visibility})
    count = result.fetchone()
    count = count[0]
    if not count:
        return 0
    return count


def show_user():
    query = text("SELECT username FROM users WHERE id = :id")
    result = db.session.execute(query, {"id": session["user_id"]})
    name = result.fetchone()
    name = name[0]
    return name


def plant_headings():
    visibility = "visible"
    query = text(
        "SELECT name FROM plant WHERE user_id=:id AND visibility=:visibility")
    result = db.session.execute(
        query, {"id": session["user_id"], "visibility": visibility})
    info = result.fetchall()
    if info == []:
        return " "
    else:
        info2 = []
        for i in info:
            info2.append(i[0])
        return info2


def plant_info(name):
    visibility = "visible"
    query = text(
        "SELECT * FROM plant WHERE user_id =:id AND name =:name AND visibility=:visibility")
    result = db.session.execute(
        query, {"id": session["user_id"], "name": name, "visibility": visibility})
    info = result.fetchall()
    if info == []:
        return " "
    return info


def add_notes(comment, name):
    try:
        query = text(
            "INSERT INTO note1 (comment, user_id, name) VALUES (:comment, :user_id, :name)")
        db.session.execute(
            query, {"comment": comment, "user_id": session["user_id"], "name": name})
        db.session.commit()
    except:
        return False
    return True


def get_comments(theplantname):
    comment = text(
        "SELECT comment FROM note1 WHERE user_id =:id AND name =:name")
    result = db.session.execute(
        comment, {"id": session["user_id"], "name": theplantname})
    info = result.fetchall()
    if info == []:
        return " "
    clean_info = []
    for i in info:
        clean_info.append(i[0])
    return clean_info


def create_emojis_table():
    emoji_list = [127800, 127799, 127793, 127795, 127807]
    for i in emoji_list:
        try:
            query = text("INSERT INTO emojis (number) VALUES (:number)")
            db.session.execute(query, {"number": i})
            db.session.commit()
        except:
            return False
    return True


def choose_emoji():
    random = randint(1, 5)
    query = text("SELECT number FROM emojis WHERE id =:id")
    result = db.session.execute(query, {"id": random})
    emoji = result.fetchone()
    if emoji == []:
        return 127807
    for i in emoji:
        emoji_code = i
    return emoji_code


def search_generator(input):
    query = text(
        "SELECT name FROM plant WHERE user_id =:id AND name LIKE :input and visibility = 'visible'")
    result = db.session.execute(
        query, {"id": session["user_id"], "input": "%"+input+"%"})
    results = result.fetchall()
    if results == []:
        return " "
    clean_info = []
    for i in results:
        clean_info.append(i[0])
    return clean_info


def delete_plant(name):
    try:
        query = text(
            "UPDATE plant SET visibility= 'invisible' WHERE name=:name AND user_id = :user_id")
        db.session.execute(
            query, {"name": name, "user_id": session["user_id"]})
        db.session.commit()
    except:
        return False
    return True


def create_direction_table():
    name_list = [("Pothos", "The Pothos-genus is one of the easiest and most common housplants across the world. It is a very forgiving plant, meaning they are thriving with only a little watering and light. Different varietis of Pothos are visually appealing with their different and vibrant colors. They are also very fast-growing, when the conditions are met."),
                 ("Snake plant", "Snake plants are highly beginner-friendly for neglecting plant parent. They tolrate drought well and only needs watering about once a month, depending on the amount light it gets.")]
    for i in name_list:
        try:
            query = text(
                "INSERT INTO directions (name, direction) VALUES (:name, :direction)")
            db.session.execute(query, {"name": i[0], "direction": i[1]})
            db.session.commit()
        except:
            return False
    return True


def show_pothos():
    query = text(
        "SELECT name, direction FROM directions WHERE name = 'Pothos'")
    result = db.session.execute(query)
    info = result.fetchall()
    return info


def show_snake():
    query = text(
        "SELECT name, direction FROM directions WHERE name = 'Snake plant'")
    result = db.session.execute(query)
    info = result.fetchall()
    return info
