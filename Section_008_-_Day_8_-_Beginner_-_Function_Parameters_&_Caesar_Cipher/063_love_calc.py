def calculate_love_score(name1, name2):
    """
    Calculates and prints a detailed love score based on the letters
    in the words TRUE and LOVE.

    Steps:
    1. Combine both names and convert to uppercase
    2. Count occurrences of letters from TRUELOVE
    3. Print detailed counts for TRUE
    4. Print detailed counts for LOVE
    5. Print final love score as concatenation of totals
    """

    # Combine names and normalize case
    combined_name = (name1 + name2).upper()

    word1 = "TRUE"
    word2 = "LOVE"

    # Dictionary to store letter counts
    letter_dict = {}

    # Count only letters that appear in TRUELOVE
    for letter in combined_name:
        if letter in word1 + word2:
            letter_dict[letter] = letter_dict.get(letter, 0) + 1

    # TRUE calculation
    total1 = 0
    for l in word1:
        count = letter_dict.get(l, 0)

        # Grammar handling: time vs times
        if count == 1:
            print(f"{l} occurs {count} time")
        else:
            print(f"{l} occurs {count} times")

        total1 += count

    print(f"Total = {total1}\n")

    # LOVE calculation
    total2 = 0
    for l in word2:
        count = letter_dict.get(l, 0)

        if count == 1:
            print(f"{l} occurs {count} time")
        else:
            print(f"{l} occurs {count} times")

        total2 += count

    print(f"Total = {total2}\n")

    # Final love score
    love_score = int(str(total1) + str(total2))
    print(f"Love Score = {love_score}")


# ---- USER INPUT ----
name1 = input("Enter first name: ")
name2 = input("Enter second name: ")

calculate_love_score(name1, name2)
