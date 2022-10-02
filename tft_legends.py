from distutils.util import execute
import sqlite3

# Establishing the connection to the databases
connection = sqlite3.connect('tft_info.db')
cursor = connection.cursor()

# Creating the main table if it doesn't already exist, otherwise will do nothing
cursor.execute("CREATE TABLE IF NOT EXISTS champions (name TEXT PRIMARY KEY, health INT, damage INT, speed REAL, range INT, dps REAL, armor INT, magic_resist INT, cost INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS types (name TEXT PRIMARY KEY, one TEXT, two TEXT, three TEXT, four TEXT, five TEXT, six TEXT)")

# This function gets the name of the champion from the table and returns it
def get_name(cursor, table):
    cursor.execute(f"SELECT name FROM {table}")
    results = cursor.fetchall()
    num = 0
    for name in results:
        print(f"{num+1}) {results[num][0]}")
        num+=1
    
    choice = int(input("Select> "))
    return results[choice-1][0]

def suggestion(cursor, list, dict):
    cursor.execute(f"SELECT * FROM types")
    types = cursor.fetchall()

    new_list = []
    num = 0
    for item in types:
        if 1 <= len(set(list)&set(item)):
            for i in item:
                if i not in list and i != "null" and i != item[num][0]:
                    new_list.append(i)
        num+=1
    
    return new_list


# Getting what the user wants to do

run_types = {}
run_champions = []
choice = 0
while choice != "quit":
    print("\n1) Display Champions\n2) Display Types\n3) Update a Row\n4) Delete a Row\n5) Add Champions\n6) Add a Type\n7) Sort Champions\n8) Suggest\n9) Champions in Run\n10) Delete Champion from Run")
    choice = input("> ")

    print()

    if choice == "1":
        # Display all champions in the databse
        cursor.execute(f"SELECT * FROM champions")
        print("{:>12} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>14} {:>8}".format("Name", "Health", "Damage", "Speed", "Range", "DPS", "Armor", "Magic Resist", "Cost"))

        for item in cursor.fetchall():
            print("{:>12} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>14} {:>8}".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))
    
    elif choice == "2":
        # Display all types in the databse
        cursor.execute(f"SELECT * FROM types")
        
        for item in cursor.fetchall():
            print("{:>12} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    
    elif choice == "3":
        # Update a specific item in a row in either table
        table = input("Table: ")
        name = input("Name/Type: ")
        thing = input("What do you want to change: ")
        change = input("The Change: ")
        values = (change, name)
        cursor.execute(f"UPDATE {table} SET {thing} = ? WHERE name = ?", values)
        connection.commit()
    
    elif choice == "4":
        # Delete a row from a table in the Database
        table = input("Table: ")
        name = get_name(cursor, table)
        values = (name,)
        cursor.execute(f"DELETE FROM {table} WHERE name = ?", values)
        connection.commit()
    
    elif choice == "5":
        # Add a new champion to the database
        table = input("Table: ")
        name = input("Name: ")
        health = input("Health: ")
        damage = int(input("Damage: "))
        speed = float(input("Speed: "))
        range = int(input("Range: "))
        dps = float(input("DPS: "))
        armor = int(input("Armor: "))
        mr = int(input("Magic Resist: "))
        cost = int(input("Cost: "))
        values = (name, health, damage, speed, range, dps, armor, mr, cost)
        cursor.execute(f"INSERT INTO champions VALUES (?,?,?,?,?,?,?,?,?)", values)
        connection.commit()
    
    elif choice == "6":
        # Add a new type to the database
        name = input("Name: ")
        first = input("First Champion: ")
        second = input("Second Champion: ")
        third = input("Third Champion: ")
        fourth = input("Fourth Champion: ")
        fifth = input("Fifth Champion: ")
        sixth = input("Sixth Champion: ")
        values = (name, first, second, third, fourth, fifth, sixth)
        cursor.execute(f"INSERT INTO types VALUES (?,?,?,?,?,?,?)", values)
        connection.commit()

    elif choice == "7":
        # Sorts champions and prints them
        sort = input("Sort: ")
        order = input("ASC or DESC: ").upper()

        cursor.execute(f"SELECT * FROM champions ORDER BY {sort} {order}")
        print("{:>12} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>14} {:>8}".format("Name", "Health", "Damage", "Speed", "Range", "DPS", "Armor", "Magic Resist", "Cost"))

        for champion in cursor.fetchall():
            print("{:>12} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>14} {:>8}".format(champion[0], champion[1], champion[2], champion[3], champion[4], champion[5], champion[6], champion[7], champion[8]))
    
    elif choice == "8":
        # Suggestion maker
        suggest = suggestion(cursor, run_champions, run_types)
        num = 1
        for champ in suggest:
            print(f"{num}) {champ}")
            num+=1
    
    elif choice == "9":
        # Adding current champions to our list
        champion = input("New Champion Name: ")
        run_champions.append(champion)

        cursor.execute(f"SELECT * FROM types")
        types = cursor.fetchall()
        num = 0
        for item in types:
            if champion in types:
                run_types[types[num][0]] = 1 + run_types.get(types[num][0])
            num+=1

    elif choice == "10":
        # Deleting current champions from our list
        champion = input("Delete Champion: ")
        run_champions.remove(champion)

        cursor.execute(f"SELECT * FROM types")
        types = cursor.fetchall()
        num = 0
        for item in types:
            if champion in types:
                run_types[types[num][0]] = 1 + run_types.get(types[num][0])
            num+=1
        
    elif choice == "11":
        thing = input("Max Champion: ")
        cursor.execute(f"SELECT MAX({thing}) FROM champions;")
        print(cursor.fetchall())

    else: choice = "quit"