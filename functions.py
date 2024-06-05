"""A collection of function for my chatbot."""

# Import all the necessary items
import pandas as pd
import numpy as np
import random

# Load my dataset imported externally from 
# https://www.kaggle.com/datasets/shuyangli94/foodcom-recipes-with-search-terms-and-tags
df = pd.read_csv('data/recipes.csv')

# convert all the NaN in 'total_time' column to 0 for future use
df['total_time'] = df['total_time'].fillna('0 mins')


def clean_directions(text):
    """
    Cleans the directions text by removing excessive newline characters and leading/trailing whitespace.

    Parameters
    ----------
    text : str
        The text containing the cooking directions with possible formatting issues.

    Returns
    -------
    str
        Cleaned text with unnecessary blank spaces and newlines removed.
    """
    
    # Split the text into lines
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # Strip the line of leading/trailing whitespace and check if it's not just empty space
        stripped_line = line.strip() 
        
        if stripped_line != '':
            # If the stripped line is not empty, add it to cleaned_lines
            cleaned_lines.append(stripped_line)

    # Join the cleaned lines back into a single string with newlines between each line
    return '\n'.join(cleaned_lines)


# delete all the blank spaces in 'directions' column to make it cleaner
df['directions'] = df['directions'].apply(clean_directions)


def convert_time_to_minutes(time_str):
    """
    Converts a formatted time string into total minutes.

    Parameters
    ----------
    time_str : str
        A string representing the time duration, formatted like "1 hr 20 mins".

    Returns
    -------
    int
        Total number of minutes calculated from the input string.
    """
    
    total_minutes = 0
    converter = time_str.split()
    
    if 'hrs' in converter or 'hr' in converter:
        if 'hrs' in converter:
            hours_index = converter.index('hrs') 
        else:
            hours_index = converter.index('hr')
        total_minutes += int(converter[hours_index-1]) * 60  # Convert hours to minutes
        
    if 'mins' in converter or 'min' in converter:
        if 'mins' in converter:
            minutes_index = converter.index('mins') 
        else:
            minutes_index = converter.index('min')
        total_minutes += int(converter[minutes_index-1])
        
    return total_minutes


def suggest_random_recipe(df):
    """
    Suggests a random recipe from a DataFrame and handles user interaction for additional suggestions.

    Parameters
    ----------
    df : DataFrame
        The pandas DataFrame containing recipes.

    Returns
    -------
    None
        This function does not return a value but prints details about the suggested recipe.
    """
    
    while True:
    # Select a random recipe
        recipe = df.sample(n=1).iloc[0]

        # Assuming the DataFrame has columns 'name', 'ingredients', and 'instructions'
        print()
        print("Here's a random recipe suggestion for you:")
        print()
        print(f"[Name]: \n{recipe['recipe_name']}")
        print()
        print(f"[Ingredients]: \n{recipe['ingredients']}")
        print()
        print(f"[Instructions]: \n{recipe['directions']}")
        print()   
        print(f"[Total Prepartion Time]: \n{recipe['total_time']}")
        print('-------------------------------------------------------------------------------------------')

        # Ask the user for continuous interaction
        user_input = input("\nWould you like another random suggestion? (yes/quit): ").lower()
        if user_input == 'quit':
            print("\nThanks and have a great meal!")
            break
            
        elif user_input == 'yes':
            print("\nLet's find another delicious recipe for you!")
            
        else:
            print("\nPlease enter a valid input")
            break
            
            
def suggest_highly_rated_recipe(df):
    """
    Suggests a random recipe from the DataFrame that has a rating of at least 4.8 on food.com.

    Parameters
    ----------
    df : DataFrame
        The pandas DataFrame containing recipes with a 'rating' column.

    Returns
    -------
    str
        A message with the name of the randomly selected highly rated recipe, 
        or a message indicating no such recipes are available.
    """
    
    # Filter the DataFrame to include only recipes with ratings of 4.8 or higher
    high_rating_df = df[df['rating'] >= 4.8]

    # Randomly select one recipe from the filtered DataFrame
    selected_recipe = high_rating_df.sample(n=1).iloc[0]

    # Construct the suggestion message
    suggestion_message = (
    f"Here's a highly rated recipe for you: {selected_recipe['recipe_name']}\n\n"
    f"[Name]: \n{selected_recipe['recipe_name']}\n\n"
    f"[Ingredients]: \n{selected_recipe['ingredients']}\n\n"
    f"[Instructions]: \n{selected_recipe['directions']}\n\n"
    f"[Total Preparation Time]: \n{selected_recipe['total_time']}\n\n"
    f"[Rating]: \n{selected_recipe['rating']}\n"
    "-------------------------------------------------------------------------------------------"
)
    return suggestion_message
            
    
def suggest_based_on_time(max_time):
    """
    Suggests recipes that can be prepared euqal to or within a given time frame specified by the user.

    Parameters
    ----------
    max_time : int
        Maximum preparation time in minutes the user is willing to spend on meal preparation.

    Returns
    -------
    None
        This function does not return a value but provides recipe suggestions and interacts with the user.
    """
    
    perfect_eligible_recipes = []
    eligible_recipes = []

    for index, row in df.iterrows():
        
        # Convert the 'total_time' of each recipe to minutes
        recipe_time = convert_time_to_minutes(row['total_time'])

    # Check if the converted time is less than or equal to the user's available time
        if recipe_time == 0:
            continue
        elif recipe_time == max_time:
            perfect_eligible_recipes.append(row)
        elif recipe_time < max_time:
            eligible_recipes.append(row)
            
    # Continuously suggest a random recipe until the user decides to quit
    while True:
        if perfect_eligible_recipes != []:
            suggestion = random.choice(perfect_eligible_recipes)
        elif eligible_recipes != []:
            suggestion = random.choice(eligible_recipes)
        else:
            print('Your time is not valid! Consider increase your time limit!')
            max_time = int(input("\nHow many minutes do you have for meal preparation? (integer only): "))
            suggest_based_on_time(max_time)
            break
            
        print("\nHere's a quick recipe suggestion for you:")
        print()   
        print(f"[Name]: {suggestion['recipe_name']}")
        print()
        print(f"[Ingredients]: {suggestion['ingredients']}")
        print()
        print(f"[Instructions]: {suggestion['directions']}")
        print()
        print(f"[Total Preparation Time]: {suggestion['total_time']}")
        print('-------------------------------------------------------------------------------------------')
                
        user_input = input("\nWould you like another suggestion with the same time limit? (yes/quit/different): ").lower()
        if user_input == 'quit':
            print("\nThanks and have a great meal!")
            break
            
        elif user_input == 'yes':
            print("\nLet's find another delicious recipe for you!")
            
        elif user_input == 'different':
            max_time = int(input("\nHow many minutes do you have for meal preparation? (integer only): "))
            suggest_based_on_time(max_time)
            
        else:
            print("\nPlease enter a valid input")
            break
       
                  
def suggest_w_preference(preference):
    """
    Suggests recipes based on the user's specified preference for a meal name or type.

    Parameters
    ----------
    preference : str
        User input describing their meal preference, which could be a name or a type of cuisine.

    Returns
    -------
    None
        This function does not return a value but allows the user to interactively search for recipes.
    """
    
    # Normalize the preference to match the dataset format
    normalized_preference = preference.lower().capitalize()

    # Filter recipes based on matching 'recipe_name' or keywords in 'cuisine_path'
    matched_recipes = df[df['recipe_name'].str.contains(normalized_preference, case=False) | 
                         df['cuisine_path'].str.contains(normalized_preference, case=False)]

    while True:
        if matched_recipes.empty:
            print("\nNo recipes found matching your preference. Try another search!")
            
        else:
            # Randomly pick a recipe from the matched recipes to suggest
            suggestion = matched_recipes.sample(n=1).iloc[0]
            print()
            print(f"How about trying ***{suggestion['recipe_name']}***? Here's a brief about it:")
            print()
            print(f"[Ingredients]: {suggestion['ingredients']}")
            print()
            print(f"[Instructions:] {suggestion['directions']}")
            print()
            print(f"[Total Preparation Time]: {suggestion['total_time']}")
            print('-------------------------------------------------------------------------------------------')

        user_input = input("\nWould you like another suggestion, search with another keyword, or quit?\n
                           (yes/another/quit): ").lower()
        
        if user_input == 'quit':
            print("\nThanks and have a great meal!")
            break
            
        elif user_input == 'yes':
            print("\nLet\'s find another delicious recipe for you!")
            
        elif user_input == 'another':
            preference = input("\nPlease specify another meal name or type: ")
            suggest_w_preference(preference)
            break 
            
        else:
            print("\nPlease enter a valid input.") 
            print("\nType \'yes\' for another suggestion, \'another\' for a new search, or \'quit\' to exit.")
            break                 
     
    
def chatbot():
    """
    Runs an interactive chatbot that assists users in deciding what to cook based on different criteria.

    Returns
    -------
    None
        This function operates indefinitely until the user decides to exit.
    """
    
    while True:
        
        # Ask the user to pick a function to start
        meal_type = input('''Hello! I'm your Recipe Chatbot:) \n
I can help you decide what to cook!\n
Do you have any idea about what to eat yet?\n
I can provide you with some ideas in the following ways!\n
1. The maximum amount of time willing to spend for meal preparation (answer '1')\n
2. Random suggestions (answer '2')\n
3. One random suggestion of a high rating recipe (answer '3')\n
4. Based on dish name/types (answer '4')\n
Or 'exit' to STOP! ''')
        print('-------------------------------------------------------------------------------------------')

        # If user wants to exit the function
        if meal_type.lower() == 'exit':
            print('Goodbye!')
            break
            
        # If user wants to choose based on time strains
        elif meal_type == '1':
            try:
                max_time = int(input('\nHow many minutes do you have for meal preparation? (integer only): '))
            except ValueError:
                print('\nPlease enter a valid number of minutes.')
                continue
            
            suggest_based_on_time(max_time)
            print('\nBye!!!')
            break

        # If user wants to choose randomly
        elif meal_type == '2':
            suggest_random_recipe(df)
            print('\nBye!!!')
            break
        
        # If user wants to choose a high rating recipe randomly
        elif meal_type == '3':
            message = suggest_highly_rated_recipe(df)
            print(message)
            print('\nBye!!!')
            break
        
        # If user wants to choose based on specific preference       
        elif meal_type == '4':
            preference = input('\nWhat do you have in mind? Please specify a meal name or type: ')
            suggest_w_preference(preference)
            print('\nBye!!!')
            break
        
        else:
            print('\nPlease enter a valid input!')