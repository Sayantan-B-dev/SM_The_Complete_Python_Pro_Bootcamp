# Morse code dictionary
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

def text_to_morse(text):
    """Convert a string to Morse code."""
    text = text.upper()
    morse_parts = []
    unsupported_chars = []
    
    for char in text:
        if char in morse_code_dict:
            morse_parts.append(morse_code_dict[char])
        else:
            # Handle unsupported characters with a placeholder
            morse_parts.append('?')
            if char not in unsupported_chars:  # Avoid duplicate warnings
                unsupported_chars.append(char)
    
    # Print warning if there were unsupported characters
    if unsupported_chars:
        print(f"Warning: The following character(s) are not supported and were replaced with '?': {', '.join(unsupported_chars)}")
    
    return ' '.join(morse_parts)

def display_supported_characters():
    """Display all supported characters to help users."""
    letters = [char for char in morse_code_dict.keys() if char.isalpha()]
    numbers = [char for char in morse_code_dict.keys() if char.isdigit()]
    punctuation = [char for char in morse_code_dict.keys() if not char.isalnum() and char != ' ']
    
    print("\n--- Supported Characters ---")
    print(f"Letters: {', '.join(letters)}")
    print(f"Numbers: {', '.join(numbers)}")
    print(f"Punctuation: {', '.join(punctuation)}")
    print("Space: (space bar)")
    print("----------------------------\n")

def main():
    print("Welcome to the Morse Code Converter!")
    print("Enter your message (letters, numbers, and basic punctuation).")
    print("Type 'help' to see all supported characters.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Your message: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'help':
            display_supported_characters()
            continue
        elif user_input == "":
            print("Please enter a message.")
            continue
            
        morse_output = text_to_morse(user_input)
        print(f"Morse Code: {morse_output}\n")

if __name__ == "__main__":
    main()