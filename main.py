from dotenv import load_dotenv
import os
import openai
import tkinter as tk
from tkinter import ttk
from excel_handler import save_recipes_to_excel
from recipe_parser import parse_recipe
import threading
import random
import time

# ===============================
# User Configuration Section
# ===============================

# OpenAI Configuration
openai_model = "gpt-4"
openai_temperature = 0.7

# GUI Configuration
window_title = "1000 kcal Recipe Generator"

# Meal types and cuisines
meal_types = ["Breakfast", "Lunch", "Dinner", "Snack", "Liquid"]
cuisines = ["Italian", "Indian", "Chinese", "Mediterranean", "American", "Polish"]

# Protein sources
protein_sources = [
    "Chicken breast", "turkey", "beef steak", "salmon", "tuna", "eggs", 
    "chickpeas", "lentils", "tofu", "tempeh", "Greek yogurt", "cottage cheese", 
    "whey protein", "peanut butter", "almonds", "milk", "pork tenderloin", 
    "mackerel", "cod", "beans", "trout", "milk soy", "cashew nuts", "mozzarella cheese"
]

# Inappropriate ingredients for liquid meals
inappropriate_ingredients = [
    "Chicken breast", "turkey", "beef steak", "salmon", "tuna", "eggs", 
    "chickpeas", "lentils", "tofu", "tempeh", "Greek yogurt", "pork tenderloin", 
    "mackerel", "cod", "beans", "trout", "mozzarella cheese"
]

# =================================
# End of User Configuration Section
# =================================

# Set the OpenAI API key
load_dotenv()  # Load the environment variables from .env file

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

# Function to update the estimated remaining time
def update_time(feedback_label, start_time, idx, num_recipes):
    elapsed_time = time.time() - start_time
    average_time_per_recipe = elapsed_time / idx
    remaining_recipes = num_recipes - idx
    remaining_time = average_time_per_recipe * remaining_recipes

    mins, secs = divmod(remaining_time, 60)
    feedback_label.config(text=f"Generated {idx} out of {num_recipes} recipes... \n Estimated remaining time: {int(mins)} minutes {int(secs)} seconds")

# Function to generate recipes
def generate_recipes(root, num_recipes_entry, progress_bar, feedback_label, save_func):
    num_recipes = int(num_recipes_entry.get())
    print(f"Number of recipes requested: {num_recipes}")
    feedback_label.config(text="Starting recipe generation...")
    root.update_idletasks()
    
    recipes_to_save = []
    
    start_time = time.time()
    
    for idx in range(1, num_recipes + 1):
        recipe_text = generate_recipe(idx)
        print(f"Model Output: {recipe_text}")
        
        if recipe_text:  # Ensure the model output is not None before processing
            parsed_recipe = parse_recipe(recipe_text)
            if parsed_recipe:  # Check if the parsing returned a valid recipe
                recipes_to_save.append(parsed_recipe)
                print(f"Recipe after parsing: {parsed_recipe}")
                print(f"Total recipes to save now: {len(recipes_to_save)}")
            else:
                print(f"Failed to parse: {recipe_text}")
        
        progress_bar["value"] += (1/num_recipes) * 100
        update_time(feedback_label, start_time, idx, num_recipes)
        root.update_idletasks()
    
    save_func(recipes_to_save)
    feedback_label.config(text=f"Recipes generation completed! Total recipes generated: {len(recipes_to_save)}")
    progress_bar["value"] = 0  # Reset progress bar
    print(f"Total recipes generated: {len(recipes_to_save)}")

# Function to check if an ingredient is appropriate for a liquid meal
def is_appropriate_for_liquid(main_ingredient):
    return main_ingredient not in inappropriate_ingredients

# Function to generate a recipe prompt and call the OpenAI API
def generate_recipe(idx):
    meal_type = random.choice(meal_types)
    cuisine = random.choice(cuisines)
    main_ingredient = random.choice(protein_sources)
    
    # Generate the prompt
    prompt = f"Create a unique {cuisine} {meal_type.lower()} meal centered around {main_ingredient} that is small in volume but high in calories (between 950-1050 kcal). The meal should not include mushrooms or seafoods (except for fishes). Provide measurements in grams or milliliters. Exclude any instructions and only provide meal details in the following format:\n"
    
    if meal_type == "Liquid":
        while not is_appropriate_for_liquid(main_ingredient):
            main_ingredient = random.choice(protein_sources)
        prompt += "Meal Name: [Meal Name]\nCalories: [Calories]\nProtein: [Protein]\nCarbs: [Carbs]\nFats: [Fats]\nIngredients:\n- [Ingredient 1]\n- [Ingredient 2]\n...\nMeal_Type: Liquid"
    else:
        prompt += "Meal Name: [Meal Name]\nCalories: [Calories]\nProtein: [Protein]\nCarbs: [Carbs]\nFats: [Fats]\nIngredients:\n- [Ingredient 1]\n- [Ingredient 2]\n...\nMeal_Type: " + meal_type
    
    # Making API call
    response = openai.ChatCompletion.create(
      model=openai_model,
      temperature=openai_temperature,
      messages=[
            {"role": "system", "content": "You are a sports dietitian who knows about weight gain and perfectly understands that if the meal volume is small and the caloric content is high, it is easier to eat it."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Function to run the recipe generation in a separate thread
def threaded_generate_recipes(root, num_recipes_entry, progress_bar, feedback_label, save_recipes_to_excel):
    t = threading.Thread(target=generate_recipes, args=(root, num_recipes_entry, progress_bar, feedback_label, save_recipes_to_excel))
    t.start()

# Main function to set up and run the GUI
def main():
    root = tk.Tk()
    root.title(window_title)

    label = tk.Label(root, text="Enter number of recipes to generate:")
    label.pack(padx=20, pady=10)

    num_recipes_entry = tk.Entry(root)
    num_recipes_entry.pack(padx=20, pady=5)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(padx=20, pady=10)

    feedback_label = tk.Label(root, text="")
    feedback_label.pack(padx=20, pady=10)

    generate_button = tk.Button(root, text="Generate Recipes", command=lambda: threaded_generate_recipes(root, num_recipes_entry, progress_bar, feedback_label, save_recipes_to_excel))
    generate_button.pack(padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
