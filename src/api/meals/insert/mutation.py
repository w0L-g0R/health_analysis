INSERT_MEAL: str = """
        INSERT INTO meals 
        (time, meal_id, user_id, meal_name, calories) 
        VALUES (%s, %s, %s, %s, %s);
        """
