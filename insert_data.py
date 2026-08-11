import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="agri2511",               
    database="om_charges_management"
)

cursor = conn.cursor()

flats_data = [
    (1, "Rajat", 9563562512),
    (2, "Shukla", 4304492130),
    (101, "Riya", 3459283921),
    (102, "Suresh", 9667752983),
    (103, "Rajesh", 9958580930),
    (104, "Yogesh", 9599949320),
    (105, "Mayank", 9821909323),
    (106, "Akash", 3049283921),
    (201, "Amit", 3485948592),
    (202, "Manoj", 9563562512),
    (203, "Divya", 9563562512),
    (204, "Harsh", 9563562512),
    (205, "Kritika", 9563562512),
    (206, "Kavya", 9563562512),
    (301, "Deepak", 9563562512),
    (302, "Suman", 9563562512),
    (303, "Dinesh", 9563562512),
    (304, "Suryansh", 9563562512),
    (305, "Manav", 9563562512),
    (306, "Aditya", 9563562512),
    (401, "Dev", 9563562512),
    (402, "Mahesh", 9563562512),
    (403, "Mitaksh", 9563562512),
    (404, "Raj", 9563562512),
    (405, "Ramandeep", 9563562512),
    (406, "Vikas", 9563562512),
]

years_data = [("2024-25",), ("2025-26",), ("2026-27",)]

# flats_query = "insert into flats (flat_no, owner_name, phone_number) values (%s, %s, %s)"

# cursor.executemany(flats_query, flats_data)

years_query = "insert into financial_years (financial_year) values (%s)"

cursor.executemany(years_query, years_data)
conn.commit()

print(cursor.rowcount, "records inserted successfully")

cursor.close()
conn.close()