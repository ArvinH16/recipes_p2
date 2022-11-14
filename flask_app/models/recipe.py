from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe(self, data):
    self.id = data['id']
    self.name = data['name']
    self.description = data['description']
    self.instructions = data['instructions']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.creator = None

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recipes_P2').query_db(query)

        all_recipes = []

        for recipe in results:
            one_recipe = cls(recipe)

            recipe_creator = {
                'id': recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['created_at'],
                'updated_at': recipe['updated_at']
            }

            creator = user.User(recipe_creator)
            one_recipe.creator = creator
            all_recipes.append(one_recipe)
            
        return all_recipes

