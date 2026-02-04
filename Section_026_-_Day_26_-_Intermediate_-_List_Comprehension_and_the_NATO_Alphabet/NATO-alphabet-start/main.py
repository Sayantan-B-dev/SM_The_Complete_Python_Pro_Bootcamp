import pandas as pd

def line(prompt,line_element="="):
    print(10*line_element,prompt,10*line_element)

with open("nato_phonetic_alphabet.csv", "r") as file:
    data = pd.read_csv(file)
df = pd.DataFrame(data)
data_dictionary={row.letter:row.code for _,row in df.iterrows()}
line("NATO Phonetic Alphabet")
while True:
    user_input=input("Enter a word: ").upper()
    try:
        result_list=[data_dictionary[letter] for letter in user_input]
    except KeyError:
        print("Please enter a valid word.")
    else:
        print(result_list)
        line("Continue or type 'exit'",line_element="-")
        will_continue=input("")
        if will_continue.lower() == "exit":
            break