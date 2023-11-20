from flask import Flask, render_template, request
import random
from constraint import Problem

app = Flask(__name__)

def calculate_bmr(gender, weight, height, age):
    gender = gender.lower()
    if gender in ["female", "f"]:
        women = (weight * 10) + (height * 6.25) - (age * 5) - 161
        return int(women)
    elif gender in ["male", "m"]:
        men = (weight * 10) + (height * 6.25) - (age * 5) + 5
        return int(men)
    else:
        return None

def food_recommendation(bmr, food_dict):
    bmr_part = bmr // 3
    meals = ['Pagi', 'Siang', 'Malam']
    meal_plan = {}

    for meal in meals:
        problem = Problem()
        for food in food_dict:
            problem.addVariable(food, range(int(bmr_part / food_dict[food]) + 1))

        problem.addConstraint(lambda *foods: sum(food*food_dict[food_name] for food, food_name in zip(foods, food_dict)) <= bmr_part, food_dict.keys())

        solutions = problem.getSolutions()

        if solutions:
            meal_plan[meal] = ', '.join(f'{food} {quantity}' for food, quantity in random.choice(solutions).items())
        else:
            meal_plan[meal] = None

    return meal_plan

# Example dictionary of foods with calories
food_dict = {
    "Nasi": 200,
    "Ayam Goreng": 250,
    "Sayur Asem": 100,
    "Tahu": 50,
    "Tempe": 150
}

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gender = request.select["gender"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        age = int(request.form["age"])

        bmr = calculate_bmr(gender, weight, height, age)

        if bmr is not None:
            recommended_food = food_recommendation(bmr, food_dict)
            if all(meal is not None for meal in recommended_food.values()):
                return render_template("result.html", recommended_food=recommended_food)
            else:
                return "Maaf, tidak ada rekomendasi yang tersedia."
        else:
            return "Jenis kelamin tidak valid."

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
