import mysql.connector
from config import dbconfig


def add_training_event(connection, event_name, event_date, event_description,genre):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO training_events (event_name, event_date, event_description)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (event_name, event_date, event_description,genre))
        connection.commit()
        print(f"Event '{event_name}' added successfully!")
    except mysql.connector.Error as e:
        print(f"Error adding event: {e}")
    finally:
        cursor.close()

def update_training_event(connection, event_id, new_name=None, new_date=None, new_description=None,genre=None):
    try:
        cursor = connection.cursor()
        updates = []
        params = []
        if new_name:
            updates.append("event_name = %s")
            params.append(new_name)
        if new_date:
            updates.append("event_date = %s")
            params.append(new_date)
        if new_description:
            updates.append("event_description = %s")
            params.append(new_description)
        if genre:
            updates.append("genre = %s")
            params.append(genre)
        params.append(event_id)

        query = f"UPDATE training_events SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, params)
        connection.commit()
        print(f"Event with ID {event_id} updated successfully!")
    except mysql.connector.Error as e:
        print(f"Error updating event: {e}")
    finally:
        cursor.close()

def remove_training_event(connection, event_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM training_events WHERE id = %s"
        cursor.execute(query, (event_id,))
        connection.commit()
        print(f"Event with ID {event_id} removed successfully!")
    except mysql.connector.Error as e:
        print(f"Error removing event: {e}")
    finally:
        cursor.close()


def add_working_opportunity(connection, opportunity_name, opportunity_date, opportunity_description, genre):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO working_opportunities (opportunity_name, opportunity_date, opportunity_description, genre)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (opportunity_name, opportunity_date, opportunity_description, genre))
        connection.commit()
        print(f"Opportunity '{opportunity_name}' added successfully!")
    except mysql.connector.Error as e:
        print(f"Error adding opportunity: {e}")
    finally:
        cursor.close()

def update_working_opportunity(connection, opportunity_id, new_name=None, new_date=None, new_description=None, genre=None):
    try:
        cursor = connection.cursor()
        updates = []
        params = []
        if new_name:
            updates.append("opportunity_name = %s")
            params.append(new_name)
        if new_date:
            updates.append("opportunity_date = %s")
            params.append(new_date)
        if new_description:
            updates.append("opportunity_description = %s")
            params.append(new_description)
        if genre:
            updates.append("genre = %s")
            params.append(genre)
        params.append(opportunity_id)

        query = f"UPDATE working_opportunities SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, params)
        connection.commit()
        print(f"Opportunity with ID {opportunity_id} updated successfully!")
    except mysql.connector.Error as e:
        print(f"Error updating opportunity: {e}")
    finally:
        cursor.close()

def remove_working_opportunity(connection, opportunity_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM working_opportunities WHERE id = %s"
        cursor.execute(query, (opportunity_id,))
        connection.commit()
        print(f"Opportunity with ID {opportunity_id} removed successfully!")
    except mysql.connector.Error as e:
        print(f"Error removing opportunity: {e}")
    finally:
        cursor.close()

def get_job_opportunities(genre, start=0):
    """
    Builds a response message based on job opportunities in the given genre.
    Includes pagination to return a subset of results.
    """
    events = search_working_opportunity_by_genre(genre)  # Query the database for events
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فرص خدمة ضمن الفئة '{genre}'."},-1,False

    # Apply pagination
    total_events = len(events)
    paginated_events = events[start:start + 2]
    more_available = (start + 3) < total_events

    # Build the response text
    response_text = f"هاذي بعض فرص الخدمة في مجال '{genre}':\n\n"
    titles = []
    for idx, event in enumerate(paginated_events, start=start + 1):
        response_text += f"{idx}. {event[1]} ({event[2]})\n"
        response_text += f"   الوصف: {event[3]}\n\n"
        titles.append(event[1])

    return {
        "text": response_text.strip(),
        "titles": titles,
    }, start+3 , more_available

def get_training_opportunities(genre, start=0):
    """
    Builds a response message based on job opportunities in the given genre.
    Includes pagination to return a subset of results.
    """
    events = search_training_event_by_genre(genre)  # Query the database for events
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فرص خدمة ضمن الفئة '{genre}'."},-1,False

    # Apply pagination
    total_events = len(events)
    paginated_events = events[start:start + 2]
    more_available = (start + 2) < total_events

    # Build the response text
    response_text = f"هذه بعض الفعاليات ضمن الفئة '{genre}':\n\n"
    titles = []
    for idx, event in enumerate(paginated_events, start=start + 1):
        response_text += f"{idx}. {event[1]} ({event[2]})\n"
        response_text += f"   الوصف: {event[3]}\n\n"
        titles.append(event[1])

    return {
        "text": response_text.strip(),
        "titles": titles,
    }, start+3 , more_available

def build_training_genre_response(genre = "تكنولوجيا"):
    """
    Builds a response message based on events in the given genre.
    """
    events = search_training_event_by_genre(genre)  # Query the database for events
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فعاليات ضمن الفئة '{genre}'."}

    # Build the response text
    response_text = f"هذه بعض الفعاليات ضمن الفئة '{genre}':\n\n"
    titles=[]
    for event in events:
        response_text += f"- {event[1]} ({event[2]})\n"
        response_text += f"  الوصف: {event[3]}\n\n"
        titles.append(event[1])
    return {"text": response_text.strip() ,"titles":titles}

def search_training_event_by_name(name):
    try:
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM training_events WHERE event_name LIKE %s"
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(f"Error searching for event: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def search_training_event_by_genre(genre):
    try:
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM training_events WHERE genre LIKE %s"
        cursor.execute(query, (f"%{genre}%",))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(f"Error searching for event: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def search_working_opportunity_by_name(name):
    try:
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM working_opportunities WHERE opportunity_name LIKE %s"
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(f"Error searching for opportunity: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def search_working_opportunity_by_genre(genre):
    try:
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM working_opportunities WHERE genre LIKE %s"
        cursor.execute(query, (f"%{genre}%",))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(f"Error searching for opportunity: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()