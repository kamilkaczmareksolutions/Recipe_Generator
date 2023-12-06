import pandas as pd
import os

EXCEL_PATH = "recipes.xlsx"

def save_recipes_to_excel(recipes):
    """Saves the list of recipe dictionaries to an Excel file."""
    
    # Convert to dataframe
    df_new = pd.DataFrame(recipes)

    # Rename columns if necessary
    if "Meal Name" in df_new.columns:
        df_new = df_new.rename(columns={"Meal Name": "Meal_Name"})
    if "Meal Type" in df_new.columns:
        df_new = df_new.rename(columns={"Meal Type": "Meal_Type"})

    # If Excel file already exists, read it and append new data
    if os.path.exists(EXCEL_PATH):
        df_existing = pd.read_excel(EXCEL_PATH)

        # Handle the Meal_ID assignment
        if not df_existing.empty:
            max_existing_id = int(df_existing["Meal_ID"].max())
            df_new["Meal_ID"] = range(max_existing_id + 1, max_existing_id + 1 + len(df_new))
        else:
            df_new["Meal_ID"] = range(1, 1 + len(df_new))
        
        df_combined = pd.concat([df_existing, df_new])
        df_combined.to_excel(EXCEL_PATH, index=False)
    else:
        # If Excel file doesn't exist, just save the new data
        df_new["Meal_ID"] = range(1, 1 + len(df_new))
        df_new.to_excel(EXCEL_PATH, index=False)

    print(f"Recipes saved to {EXCEL_PATH}")

