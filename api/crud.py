from .database import get_connection

def get_top_products(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT object_class, COUNT(*) as freq
        FROM analytics.fct_image_detections
        GROUP BY object_class
        ORDER BY freq DESC
        LIMIT %s;
    """, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"object_class": r[0], "count": r[1]} for r in results]

def get_channel_activity(channel_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date_day, COUNT(*) 
        FROM analytics.fct_messages
        WHERE channel = %s
        GROUP BY date_day
        ORDER BY date_day;
    """, (channel_name,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"date": str(r[0]), "count": r[1]} for r in results]

def search_messages(keyword):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT message_id, text, channel, date
        FROM analytics.stg_telegram_messages
        WHERE text ILIKE %s
        LIMIT 20;
    """, (f"%{keyword}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "text": r[1], "channel": r[2], "date": str(r[3])} for r in rows]
