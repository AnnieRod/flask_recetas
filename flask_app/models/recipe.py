from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_name = data['first_name']

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes(name, description, instructions, under, date_cooked, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under)s, %(date_cooked)s, NOW(), NOW(), %(user_id)s);"
        new_recipe = connectToMySQL('recipes_schema').query_db(query, data)
        return new_recipe

    ##Recupera info de user para nombre en la main
    @classmethod
    def get_recipe(cls, id):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        data = {"id": id}
        result = connectToMySQL('recipes_schema').query_db(query, data)
        recipes = []
        for recipe in result:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def recipes_with_users(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under=%(under)s, date_cooked=%(date_cooked)s WHERE id=%(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)
    
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        today_date = datetime.today().strftime('%Y-%m-%d')
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters long", "recipe")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters long", "recipe")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long", "recipe")
            is_valid = False
        if data['date_cooked'] == "":
            flash("A date must be entered", "recipe")
            is_valid = False
        if data["date_cooked"] > today_date:
            flash("You can't cook in the future, right? Select a valid date", "recipe")
            is_valid = False
        return is_valid

            
    # @classmethod      NO ESTA EN USO PERO PUEDE NECESITARSE PARA FUNCIONES FUTURAS
    # def get_all(cls):
    #     query = "SELECT * FROM recipes;"
    #     results = connectToMySQL('recipes_schema').query_db(query)
    #     recipes = []
    #     for recipe in results:
    #         recipes.append(cls(recipe))
    #     return recipes