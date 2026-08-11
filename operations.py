from db import get_connection

def search_flats(flat_no):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * from flats where flat_no = %s"
    cursor.execute(query, (flat_no,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def get_financial_year():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT financial_year from financial_years order by financial_year"

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_charges(flat_no, financial_year):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT charge_id, from_date, to_date, amount, charge_type FROM charges where flat_no=%s and financial_year = %s order by from_date"
    cursor.execute(query, (flat_no, financial_year))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_total_charges(flat_no, financial_year):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT SUM(amount) from charges where flat_no=%s and financial_year=%s"

    cursor.execute(query, (flat_no, financial_year))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result[0] is not None else 0

def get_total_paid(flat_no, financial_year):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT SUM(amount_paid) from payments where flat_no=%s and financial_year=%s"

    cursor.execute(query, (flat_no, financial_year))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result[0] is not None else 0
    

def add_payment(flat_no, financial_year, payment_date, amount_paid):
    conn = get_connection()
    cursor = conn.cursor()

    query = "insert into payments(flat_no, financial_year, payment_date, amount_paid) values (%s, %s, %s, %s)"
    cursor.execute(query, (flat_no, financial_year, payment_date, amount_paid))

    conn.commit()

    cursor.close()
    conn.close()

def add_charge(flat_no, financial_year, from_date, to_date, amount, charge_type):
    conn = get_connection()
    cursor = conn.cursor()

    query = "insert into charges (flat_no, financial_year, from_date, to_date, amount, charge_type) values (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (flat_no, financial_year, from_date, to_date, amount, charge_type))

    conn.commit()

    cursor.close()
    conn.close()

def get_payments(flat_no, financial_year):
    conn = get_connection()
    cursor = conn.cursor()

    query = "select payment_id, payment_date, amount_paid from payments where flat_no=%s and financial_year=%s order by payment_date" 
    
    cursor.execute(query, (flat_no, financial_year))

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_all_flats():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT flat_no, owner_name, phone_number
    FROM flats
    ORDER BY flat_no
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
