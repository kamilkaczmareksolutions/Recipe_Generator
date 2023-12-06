# Recipe Generator for Customizable Bulking Diets

![GUI_screenshot](https://github.com/kamilkaczmareksolutions/Recipe_Generator/assets/95218485/96a2b42d-dc90-4516-bfb0-cc7b87426e4f)

## Introduction
The Recipe Generator is a GUI application that leverages the power of GPT-3.5 to generate 1000 kcal recipes, focusing on bulking diets. Designed to cater to specific dietary preferences and caloric requirements, it emphasizes variety and taste, offering a unique solution for managing dietary goals.

## Why Use the Recipe Generator?
- **High Customizability**: Tailor every aspect of your diet – from meal types to cuisines and protein sources. This allows for a personalized diet plan that caters to individual tastes and nutritional needs.
- **Bulk Recipe Generation**: Unlike manual methods, this application can generate a large number of recipes at once – even 100 or more. This is particularly useful for planning meals over an extended period or for those who prefer batch cooking.
- **Efficiency Over Manual Methods**: While you could use services like ChatGPT with careful prompt engineering for single recipes (or idk, 10 at once? 20?), this application streamlines the process, generating multiple recipes automatically and efficiently.

## Key Features
- **Customizable Caloric Intake**: Tailor your recipes to meet specific caloric goals, with a default setting of 1000kcal (Note: it's not in User Configuration Section, must be done inside prompts to OpenAI. Simply use ctrl + F "1000", and change as you wish).
- **Diverse Cuisine Options**: Choose from various cuisines to keep your diet interesting and varied.
- **Diet Flexibility**: Adjust the application for different dietary needs, including both bulking and reducing diets - must be done manually in prompts (regular prompt and system prompt).
- **Data Management**: Efficiently manage recipes through an integrated Excel file system.
- **User-Friendly GUI**: Easy to navigate interface for simple user experience.

## Technologies Used
- **Python**: The core language used for backend development.
- **OpenAI API**: Enables dynamic and variable-driven recipe generation.
- **Excel**: Utilized for storing and manipulating recipe data.

## How It Works
1. **Recipe Generation Process**:
   - The application randomly selects a meal type and a cuisine.
   - A main protein source is randomly chosen.
   - A prompt is dynamically created and sent to the OpenAI API to generate a unique recipe.

2. **Parsing and Storing Recipes**:
   - The generated recipes are parsed and formatted.
   - Valid recipes are collected and saved to an Excel file.

3. **User Feedback and Progress Tracking**:
   - Real-time feedback on the number of recipes generated and estimated time remaining (in console).

![Output_screenshot](https://github.com/kamilkaczmareksolutions/Recipe_Generator/assets/95218485/5e3bf655-2aa5-4f18-bf57-f4c126b9f1a9)

## Installation
1. Ensure Python is installed on your system.
2. Clone or download the Recipe Generator code.
3. Navigate to the directory of the downloaded code.
4. (Optional) Create a virtual environment and activate it.
5. Install the necessary dependencies with `pip install -r requirements.txt`.
6. Create a `.env` file in the root directory with your OpenAI API key like this: `OPENAI_API_KEY=sk-yourkey`.

## Configuration
1. Open `main.py` in your code editor.
2. Set the `openai_model` variable to your preferred model (e.g., `gpt-4-1106-preview` or `gpt-3.5-turbo-1106` - visit for info: https://platform.openai.com/docs/models/overview).
3. Customize the `window_title` to change how the GUI window is named.
4. Modify `meal_types` as needed. Note: Keep 'Liquid' for high-calorie, low-volume meals, especially useful for hardgainers.
5. Change `cuisines` and `protein_sources` to include your preferred options.
6. Update `inappropriate_ingredients` to exclude certain items from liquid recipes (this is important, otherwise it might produce bs like steak inside shake :P).
7. Comment out the 'Liquid' section in `generate_recipe` if focusing on weight reduction (you probably don't want low volume, high calorie, but totally opposition, and liquid calories are like this. You don't consume much volume, but you consume a lot of calories).

## Usage
Run the application by executing `main.py`. Input the desired number of recipes in the GUI, and the application will generate and display the progress.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to fork the repository and submit a pull request.

## Notes
- The best models for recipe generation are from 'GPT-4 family' but other like GPT-3.5 Turbo can also be effective.
- The estimated time for recipe generation is based on the time taken to create the first recipe and is adjusted as more recipes are generated.
- This thing is not generating instructions how you should prepare your meals, however you can add it to the prompt, if you want.