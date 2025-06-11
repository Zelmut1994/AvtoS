def search_part_by_name(name_query):
    """Поиск запчастей по частичному совпадению наименования (регистронезависимый)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Используем LOWER() для регистронезависимого поиска
        cursor.execute("SELECT id, article, name, quantity, price FROM parts WHERE LOWER(name) LIKE LOWER(?)", ('%' + name_query + '%',))
        parts = cursor.fetchall()
        return [dict(row) for row in parts]

def search_part_by_article(article_query):
    """Поиск запчасти по артикулу (частичное совпадение)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, article, name, quantity, price FROM parts WHERE article LIKE ?", ('%' + article_query + '%',))
        parts = cursor.fetchall()
        return [dict(row) for row in parts] 