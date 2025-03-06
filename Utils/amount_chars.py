


def amount_chars(questions):
    """
    Calculate the total number of characters in a list of questions.
    Args:
        questions (list of str): A list of question strings.
    Returns:
        int: The total number of characters in all questions combined.
    """
    # Initialize a counter for the total number of characters
    char_count = 0
    
    # Iterate over each question in the list of questions
    for question in questions:
        # Add the length of the current question to the total character count
        char_count += len(question)
    
    # Return the total number of characters
    return char_count


