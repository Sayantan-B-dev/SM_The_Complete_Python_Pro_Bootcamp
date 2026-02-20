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
    for char in text:
        if char in morse_code_dict:
            morse_parts.append(morse_code_dict[char])
        else:
            # Handle unsupported characters by replacing with a placeholder
            morse_parts.append('?')
    return ' '.join(morse_parts)

def main():
    print("Welcome to the Morse Code Converter!")
    print("Enter your message (letters, numbers, and basic punctuation).")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Your message: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        if user_input == "":
            print("Please enter a message.")
            continue
        morse_output = text_to_morse(user_input)
        print(f"Morse Code: {morse_output}\n")

if __name__ == "__main__":
    main()