"""Test for my Cuisine Chatbot functions.

Note: I only created three test functions on three of the testable functions in my project. The rest are not simply testable due to existence of recursion, the use of user input, and the print statements instead of return. 
"""

from my_module.functions import convert_time_to_minutes, clean_directions, suggest_highly_rated_recipe

import pandas as pd
from unittest import mock
import pytest
    
def test_convert_time_to_minutes():
    """Tests for the `convert_time_to_minutes` function."""
    
    assert callable(convert_time_to_minutes)

    # Test converting hours and minutes to minutes
    assert convert_time_to_minutes('1 hr 20 mins') == 80
    assert convert_time_to_minutes('3 hrs 10 mins') == 190
    
    # Test converting just minutes
    assert convert_time_to_minutes('45 mins') == 45
    
    # Test converting just hours
    assert convert_time_to_minutes('2 hrs') == 120
    
    # Test input with no time
    assert convert_time_to_minutes('0 mins') == 0
    


def test_clean_directions():
    """Tests for the `clean_directions` function."""

    assert callable(clean_directions)
    
    # Test input with multiple newlines and excessive spaces
    text_with_newlines = "Preheat oven to 375 degrees. \n\n\nMix ingredients thoroughly.\n\n   Bake for 20 minutes."
    expected_clean = "Preheat oven to 375 degrees.\nMix ingredients thoroughly.\nBake for 20 minutes."
    assert clean_directions(text_with_newlines) == expected_clean, "Should remove extra newlines and trim spaces"

    # Test input with no newlines or excessive spaces - should remain unchanged
    already_clean_text = "Preheat oven to 375 degrees.\nMix ingredients.\nBake for 20 minutes."
    assert clean_directions(already_clean_text) == already_clean_text, "Should handle already clean text correctly"

    # Test input that is entirely whitespace - should return empty string
    whitespace_only_text = "   \n  \n \n   "
    assert clean_directions(whitespace_only_text) == "", "Should return an empty string for whitespace-only input"

    # Test empty string input - should return empty string
    empty_text = ""
    assert clean_directions(empty_text) == "", "Should return an empty string for empty input"


def test_suggest_highly_rated_recipe():
    """
    Tests the suggest_highly_rated_recipe function to ensure it returns correct recipe suggestions based on ratings.
    Because this type of testing is much more complicated and outside of the scope of the class, I have seeked help from
    ChatGPT in terms of what are available methods and functions that I could use. Furthermore, when I have encountered
    Assertion Errors, I also asked ChatGPT to help me figuring out how to make my test function work.
    """
    
    # Create a mock DataFrame
    data = {
        'recipe_name': ['Apple Pie', 'Banana Bread'],
        'ingredients': ['Apples, Sugar, Pie crust', 'Bananas, Flour, Sugar'],
        'directions': ['Bake at 350 for 20 minutes', 'Bake at 325 for 45 minutes'],
        'total_time': ['20 mins', '45 mins'],
        'rating': [4.9, 4.5]  # Only Apple Pie is eligible
    }
    df = pd.DataFrame(data)

    # Use pandas DataFrame's built-in capabilities to mock sample, since sample is a DataFrame method
    # This part of the code is coming from ChatGPT completely
    with mock.patch.object(pd.DataFrame, 'sample', return_value=df.iloc[0:1]):
        message = suggest_highly_rated_recipe(df)
        
        expected_message = (
            "Here's a highly rated recipe for you: Apple Pie\n\n"
            "[Name]: \nApple Pie\n\n"
            "[Ingredients]: \nApples, Sugar, Pie crust\n\n"
            "[Instructions]: \nBake at 350 for 20 minutes\n\n"
            "[Total Preparation Time]: \n20 mins\n\n"
            "[Rating]: \n4.9\n"
            "-------------------------------------------------------------------------------------------"
        )

        # Check if the function returns the correct message for a high-rated recipe
        assert message == expected_message

