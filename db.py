import mysql.connector
import validators

import config
from config import moreOptionsPressedIndicator


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

def get_emploi_by_genre(genre,start = 0):
    """
      Builds a response message based on events in the given genre.
      """
    events = search_Emploi_by_genre(genre)  # Query the database for events
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فعاليات ضمن الفئة '{genre}'."}

    if len(events)<= start:
        return {"text" : f"ممم سامحني أما ماعادش فرص خدمة أخرى في السيكتور هذا توا، أما دوب ما يهبطو تو نعلمك."}

    # Build the response text
    response_text = f"هاذوم بعض المنصات اللي تنجم تلقى فيهم فرص خدمة في {genre}:\n\n"
    titles = []
    urllist=[]
    for index, event in enumerate(events):
        if index<start:
            continue
        if index-start>2:
            break
        urllist.append(event[1])
        response_text += f"- إسم الموقع :{event[3]}\n "
        response_text += f"\n  الوصف: {event[2]}\n\n"

        titles.append(event[3])
    return {"text": response_text.strip(), "titles": titles , "urls":urllist }

def search_Emploi_by_genre(genre):
    try:
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM emplois WHERE type LIKE %s"
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

def get_courses_by_genre(genre,start = 0):
    """
      Builds a response message based on events in the given genre.
      """
    genre_keywords = {
        "التكنولوجيا": [
            "التكنولوجيا", "تطوير البرمجيات", "الكلاود", "البرودكتيفيتي", "تطوير الويب",
            "إدارة قواعد البيانات", "الشبكات", "الأمن السيبراني", "الذكاء الاصطناعي"
        ],
        "الأعمال": [
            "الأعمال", "SAP", "البيزنس", "التطوير الشخصي", "التسويق الرقمي"
        ],
        "علوم البيانات": [
            "علوم البيانات", "التعلم الآلي", "الذكاء الاصطناعي", "تحليل البيانات"
        ],
        "الصحة": [
            "الصحة", "الرعاية الصحية", "الاستجابة للطوارئ", "الصحة العامة"
        ],
        "العلوم الاجتماعية": [
            "العلوم الاجتماعية", "العلوم الإنسانية", "الهندسة", "علوم البيانات"
        ],
        "التنمية المستدامة": [
            "التنمية المستدامة", "الاستدامة البيئية", "التغير المناخي"
        ],
        "حقوق الإنسان": [
            "حقوق الإنسان", "الديمقراطية", "بناء السلام", "الذكاء الاصطناعي وحقوق الإنسان",
            "مكافحة خطاب الكراهية", "القانون الإنساني الدولي وحقوق الإنسان", "الحماية المؤقتة في الاتحاد الأوروبي"
        ],
        "الفنون والتعليم": [
            "الفنون", "التعليم", "العلوم", "التكنولوجيا"
        ]
    }
    list_of_keywords=genre_keywords[genre]
    events = search_courses_by_genre(list_of_keywords)  # Query the database for events
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فعاليات ضمن الفئة '{genre}'."}

    if len(events)<= start:
        return {"text" : f"ممم سامحني أما ماعادش فرص تعليم أخرى في secteur هذا توا، أما دوب ما يهبطو تو نعلمك."}

    # Build the response text
    response_text =  f"هاذوم بعض المنصات اللي تنجم تلقى فيهم فرص تعليم في {genre}:\n\n"
    titles = []
    urllist=[]
    char_limit=500
    for index, event in enumerate(events):

        if index<start:
            continue
        if index-start>2:
            break
        site_name = f"- إسم الموقع : {event[6]}\n"
        description = f"  الوصف: {event[2]}\n"
        registration_info = f"  التسجيل : {event[4]}\n"
        financial_aid_info = f"  فما مساعده مالية؟ : {event[5]}\n\n"

        # Calculate new section length and check if it will exceed the limit
        new_section = site_name + description + registration_info + financial_aid_info
        if len(response_text) + len(new_section) > char_limit:
            break  # Stop adding more if it exceeds 500 characters

        response_text += new_section
        titles.append(event[6])
        urllist.append(event[1])
    return {"text": response_text.strip(), "titles": titles , "urls":urllist }


def search_courses_by_genre(keywords):
    try:
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM courses WHERE " + " OR ".join([f"fields LIKE %s" for _ in keywords])
        cursor.execute(query, tuple(f"%{keyword}%" for keyword in keywords))
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
def get_financing_opportunities(genre,start = 0):
    """
      Builds a response message based on events in the given genre.
    """
    financing_support_keywords = {
        "ريادة الأعمال": [
            "ريادة الأعمال", "المحاسبة", "التصرف", "الابتكار", "المهارات الحياتية",
            "التسويق", "إدارة المشاريع", "التخطيط", "BMC", "التمكين الاقتصادي للنساء",
            "التنمية المحلية", "البحث والتطوير", "الابتكار التكنولوجي", "تطوير المنتجات وتحسين جودتها",
            "التعاون بين الصناعيين والمراكز البحثية", "تعزيز القدرة التنافسية"
        ],
        "التمويل": [
            "التمويل", "دعم المشاريع الصغيرة والمتوسطة", "تمويل المشاريع الصغيرة والمتوسطة",
            "الاقتصاد", "الإدارة المالية والمحاسبية", "استخدام التكنولوجيا المالية"
        ],
        "إدارة المشاريع": [
            "إدارة المشاريع", "دعم الشركات الناشئة"
        ],
        "الابتكار": [
            "الابتكار", "التكنولوجيا", "التجديد", "الابتكار التكنولوجي", "الابتكار الاجتماعي"
        ],
        "الفلاحة": [
            "الفلاحة", "الوقاية الصحية", "دعم المؤسسات الناشئة الإرشاد والمتابعة",
            "الإنتاج الزراعي والغذائي", "الزراعة المستدامة", "حماية البيئة", "استعادة المياه",
            "التنمية الاقتصادية للمناطق الريفية"
        ],
        "التنمية المستدامة": [
            "التنمية المستدامة", "الاقتصاد الاجتماعي والتضامني", "التنمية الاقتصادية المستدامة",
            "تطوير مهارات الشباب", "تعزيز قابلية التوظيف"
        ],
        "الصناعة": [
            "الصناعة", "دعم الشركات التجارية والصناعية والباعثين الشبان", "التصدير",
            "الأسواق الخارجية", "الاستشارات", "الحوافز المالية", "التجديد"
        ],
        "التنمية المحلية": [
            "التنمية المحلية", "دعم تقني واداري للمشاريع والاستثمار", "الاقتصاد الاجتماعي والتضامني",
            "ريادة الأعمال", "الابتكار الاجتماعي"
        ],
        "التعليم والتدريب المهني": [
            "التعليم والتدريب المهني", "التكوين المهني", "السياحة", "الصيانة", "الحرف التقليدية"
        ]
    }

    list_of_keywords=financing_support_keywords[genre]
    events = search_financing_by_genre(list_of_keywords)  # Query the database for events
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فعاليات ضمن الفئة '{genre}'."}

    if len(events)<= start:
        return {"text" : f"ممم سامحني أما ماعادش فرص تمويل أخرى في secteur هذا توا، أما دوب ما يهبطو تو نعلمك."}

    # Build the response text
    response_text =  f" هاذومه بعض فرص التمويل الموجوده عنا حاليا في مجال  {genre}:\n\n"
    titles = []
    urllist=[]
    char_limit=640
    description_limit=250
    added_any=False
    for index, event in enumerate(events):

        if index<start:
            continue
        if index-start>2:
            break
        # Check if fields are empty and build the response text accordingly
        site_name = f"- اسم المؤسسة: {event[6].strip()}\n\n" if event[6] else ""
        description = f"  -الفرص المتوفرة: {event[4].strip()}\n" if event[4] else ""
        if len(description) > description_limit:
            description = f"{description[:250]}..."+"اكتشف أكثر في الموقع"
        registration_info = f"  \n\n-التسجيل: {event[10].strip()}\n" if event[10] else ""
        financial_aid_info = f"  \n-فما مساعدة مالية؟: {event[11].strip()}\n\n" if event[11] else ""

        new_section = site_name + description + registration_info + financial_aid_info

        if len(response_text) + len(new_section) > char_limit:
            if not added_any:  # No sections have been added and the first is too long
                response_text += new_section[:char_limit - len(response_text)-4]+"..."  # Add truncated section
                titles.append(event[6].strip())
                url = event[1] if validators.url(str(event[1])) else ""
                urllist.append(url)
            break

        response_text += new_section
        added_any = True
        titles.append(event[6].strip())
        url = event[1] if validators.url(str(event[1])) else ""

        urllist.append(url)
    return {"text": response_text.strip(), "titles": titles, "urls": urllist}

def search_financing_by_genre(keywords):
    try:
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM entrep WHERE " + " OR ".join([f"fields LIKE %s" for _ in keywords])
        cursor.execute(query, tuple(f"%{keyword}%" for keyword in keywords))
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

def get_support_opportunities_by_type(type,start = 0):
    """
      Builds a response message based on events in the given genre.
      """
    events = search_support_opportunities_by_type(type)
    if not events:
        return {"text": f"عذراً، لم نعثر على أي فرص دعم ضمن الفئة '{type}'."}

    if len(events)<= start:
        return {"text" : f"ممم سامحني أما ماعادش فرص دعم أخرى من النوع هذا توا، أما دوب ما يهبطو تو نعلمك."}

    # Build the response text
    response_text = f"هاذوم بعض فرص الدعم اللي موجودين {type}:\n\n"
    titles = []
    urllist=[]
    char_limit = 500
    for index, event in enumerate(events):
        if index<start:
            continue
        if index-start>2:
            break
        site_name = f"- عنوان المنحه :{event[5]}\n "
        requirements = f" المتطلبات :{event[3]}\n "
        description = f"\n  التفاصيل: {event[2]}\n\n"
        new_section = site_name+ requirements + description
        if len(response_text) + len(new_section) > char_limit:
            break
        response_text += new_section
        urllist.append(event[1])
        titles.append(event[5])
    return {"text": response_text.strip(), "titles": titles , "urls":urllist }

def search_support_opportunities_by_type(keywords):
    try:
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()
        query = "SELECT * FROM scholars_fellowships_internships WHERE opportunity_type LIKE %s"
        cursor.execute(query, (f"%{keywords}%",))
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


def insert_data_to_db(sheet_name, df):
    if (sheet_name == 'courses'):
        insert_courses_to_db(df)
    elif (sheet_name == 'emplois'):
        insert_emplois_to_db(df)
    elif (sheet_name == 'scholars_fellowships_internship'):
        insert_scholars_fellowships_internship_to_db(df)
    elif (sheet_name == 'entrep'):
        insert_entrep_to_db(df)


def insert_courses_to_db(dataframe):
    try:
        # Establish the connection
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()

        # Loop through each row in the dataframe
        for _, row in dataframe.iterrows():
            # Prepare the query with placeholders for the values
            insert_query = f"""
                INSERT INTO courses (link, available_courses, fields, registration, financial_aid_available)
                VALUES (%s, %s, %s, %s, %s)
            """

            # Map the values to the query
            values = (
                row['الرابط'],
                row['الدورات المتوفرة'],
                row['المجالات'],
                row['التسجيل'],
                row['الدعم المالي المتاح']
            )

            # Execute the insert query for each row
            cursor.execute(insert_query, values)

        # Commit the transaction
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to insert data into the database: {e}")


def insert_entrep_to_db(dataframe):
    try:
        # Establish the connection
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()

        # Loop through each row in the dataframe
        for _, row in dataframe.iterrows():
            # Prepare the query with placeholders for the values
            insert_query = f"""
                INSERT INTO entrep (location, representative, website, current_opportunities, services_tasks, institution_name, available_courses, fields, phase, registration, financial_support)
                VALUES (%s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s)
            """

            # Map the values to the query
            values = (
                row['المكان'],
                row['الممثل'],
                row['موقع الواب'],
                row['الفرص الحالية'],
                row['الخدمات / المهام '],
                row['اسم المؤسسة/ الهيكل/ طرف ممول/ برامج'],
                row['الدورات المتوفرة'],
                row['المجالات'],
                row['المرحلة'],
                row['التسجيل'],
                row['الدعم المالي المتاح']
            )

            # Execute the insert query for each row
            cursor.execute(insert_query, values)

        # Commit the transaction
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to insert data into the database: {e}")


def insert_emplois_to_db(dataframe):
    try:
        # Establish the connection
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()

        # Loop through each row in the dataframe
        for _, row in dataframe.iterrows():
            # Prepare the query with placeholders for the values
            insert_query = f"""
                INSERT INTO emplois (link, description, site_name, type)
                VALUES (%s, %s, %s, %s)
            """

            # Map the values to the query
            values = (
                row['الرابط'],
                row['شنوة فيه'],
                row['اسم الموقع'],
                row['النوع']
            )

            # Execute the insert query for each row
            cursor.execute(insert_query, values)

        # Commit the transaction
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to insert data into the database: {e}")


def insert_scholars_fellowships_internship_to_db(dataframe):
    try:
        # Establish the connection
        connection = mysql.connector.connect(**config.dbconfig)
        cursor = connection.cursor()

        # Loop through each row in the dataframe
        for _, row in dataframe.iterrows():
            # Prepare the query with placeholders for the values
            insert_query = f"""
                INSERT INTO scholars_fellowships_internships (link, financial_support, qualifications, fields, program_name, opportunity_type)
                VALUES (%s, %s, %s, %s, %s , %s)
            """

            # Map the values to the query
            values = (
                row['الرابط'],
                row['الدعم المالي المتاح'],
                row['المؤهلات'],
                row['المجالات'],
                row['اسم البرنامج'],
                row['نوع الفرصة'],
            )

            # Execute the insert query for each row
            cursor.execute(insert_query, values)

        # Commit the transaction
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to insert data into the database: {e}")

