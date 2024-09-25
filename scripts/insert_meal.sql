INSERT INTO public.meals (meal_id, user_id, meal_name, calories)
VALUES (
        uuid_generate_v4(),
        uuid_generate_v4(),
        'Chicken Salad',
        350
    );