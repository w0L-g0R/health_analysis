class MealInsertQuery:
    def __call__(self):
        return """
        INSERT INTO meals (time, meal_id, user_id, meal_name, calories) VALUES ($1, $2, $3, $4, $5)
        """


class MealDeleteQuery:
    def __call__(self):
        return """
        DELETE FROM meals WHERE meal_id = $1 AND user_id = $2
        """
