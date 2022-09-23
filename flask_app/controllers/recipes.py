from flask import request, redirect, render_template,session

from flask_app import app

from flask_app.models.recipe import Recipe

from flask_app.models.user import User

##Formulario para crear receta
@app.route("/recipes/new")
def recipes_form():
    if 'user_id' not in session:
        return redirect ("/")
    return render_template("recipeform.html")

@app.route("/create", methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    else:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_cooked': request.form['date_cooked'],
            'under' : request.form['under'],
            'user_id' : session['user_id']
        }
    Recipe.save_recipe(data)
    return redirect("/recipes")

##Pagina para mostrar detalles de receta 
@app.route("/recipes/<int:id>")
def show_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id
    }
    return render_template("show.html", recipe = Recipe.get_recipe(data))

##Editar o actualiza receta ARREGLA TODO EL ID (NO logra editar valores y no muestra previos)
@app.route("/recipes/edit/<int:id>")
def edit_template(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe(id)[0]
    return render_template("edit.html", recipe = recipe)

@app.route("/update", methods = ['POST'])
def update_info(id):
    if not Recipe.validate_recipe(request.form):
        return redirect("recipes/edit/<int:id>")
    updated_recipe = {
            'id' : id,
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_cooked': request.form['date_cooked'],
            'under' : request.form['under'],
    }
    Recipe.update_recipe(updated_recipe)
    return redirect("/recipes")



## Eliminar receta
@app.route("/recipes/delete/<int:id>")
def delete(id):
    data = {
        "id" : id
    }
    Recipe.delete_recipe(data)
    return redirect ("/recipes")