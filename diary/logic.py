from datetime import datetime

def validate_date(date_str, expected_format):
    try:
        return datetime.strptime(date_str, expected_format)
    except ValueError:
        return None

def add_entry(conn, date_str, text, expected_format):
    date_obj = validate_date(date_str, expected_format)
    if not date_obj:
        return "Неверный формат даты."
    date_sql = date_obj.strftime("%Y-%m-%d")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (date, text) VALUES (?, ?)", (date_sql, text.strip()))
    conn.commit()
    return "Запись добавлена."

def search_entry(conn, date_str, expected_format):
    date_obj = validate_date(date_str, expected_format)
    if not date_obj:
        return "Неверный формат даты."
    date_sql = date_obj.strftime("%Y-%m-%d")

    cursor = conn.cursor()
    cursor.execute("SELECT text FROM entries WHERE date = ?", (date_sql,))
    results = cursor.fetchall()
    if results:
        return "\n".join([f"{i+1}) {row[0]}" for i, row in enumerate(results)])
    return "Нет записей за эту дату."

def search_by_keyword(conn, keyword):
    if not keyword.strip():
        return "Ключевое слово пустое."
    cursor = conn.cursor()
    cursor.execute("SELECT date, text FROM entries WHERE text LIKE ?", (f"%{keyword}%",))
    results = cursor.fetchall()
    if results:
        output = ""
        grouped = {}
        for date, text in results:
            grouped.setdefault(date, []).append(text)
        for date in sorted(grouped.keys()):
            output += f"\n{date}:\n"
            for i, text in enumerate(grouped[date], 1):
                output += f"  {i}) {text}\n"
        return output
    return "Нет совпадений."

def show_all_entries(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT date, text FROM entries ORDER BY date")
    results = cursor.fetchall()
    if not results:
        return "Дневник пуст."
    output = ""
    grouped = {}
    for date, text in results:
        grouped.setdefault(date, []).append(text)
    for date in sorted(grouped.keys()):
        output += f"\n{date}:\n"
        for i, text in enumerate(grouped[date], 1):
            output += f"  {i}) {text}\n"
    return output

def delete_entries_by_date(conn, date_str, expected_format):
    date_obj = validate_date(date_str, expected_format)
    if not date_obj:
        return "Неверный формат даты."
    date_sql = date_obj.strftime("%Y-%m-%d")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE date = ?", (date_sql,))
    conn.commit()
    return "Записи удалены."

def search_by_date_range(conn, start_str, end_str, expected_format):
    start_obj = validate_date(start_str, expected_format)
    end_obj = validate_date(end_str, expected_format)
    if not start_obj or not end_obj:
        return "Неверный формат даты."
    if start_obj > end_obj:
        return "Начальная дата позже конечной."

    start_sql = start_obj.strftime("%Y-%m-%d")
    end_sql = end_obj.strftime("%Y-%m-%d")

    cursor = conn.cursor()
    cursor.execute("SELECT date, text FROM entries WHERE date BETWEEN ? AND ? ORDER BY date", (start_sql, end_sql))
    results = cursor.fetchall()
    if not results:
        return "Нет записей в этом диапазоне."

    output = ""
    grouped = {}
    for date, text in results:
        grouped.setdefault(date, []).append(text)
    for date in sorted(grouped.keys()):
        output += f"\n{date}:\n"
        for i, text in enumerate(grouped[date], 1):
            output += f"  {i}) {text}\n"
    return output

def delete_all_entries(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries")
    conn.commit()
    return "Все записи удалены."
