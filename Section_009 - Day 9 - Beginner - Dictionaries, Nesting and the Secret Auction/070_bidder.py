# ================================
# SECRET SILENT AUCTION PROGRAM
# ================================
# This program allows multiple bidders to place bids secretly.
# Each bidder enters their name and bid amount.
# After all bids are entered, the program determines the highest bidder.
# No bids are shown during entry (silent auction behavior).


# Function to safely get a valid bid amount
def get_valid_bid():
    while True:
        bid = input("Enter your bid amount (numbers only): ₹ ")
        if bid.isdigit():
            return int(bid)
        else:
            print("❌ Invalid input. Please enter a numeric value.")

# Function to find the highest bidder
def find_highest_bidder(bids):
    highest_bid = 0
    winner = ""

    # Loop through dictionary keys (bidder names)
    for bidder in bids:
        bid_amount = bids[bidder]

        # Compare each bid with current highest
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder

    return winner, highest_bid


# ================================
# MAIN PROGRAM LOGIC
# ================================

print("🏷️  WELCOME TO THE SECRET SILENT AUCTION 🏷️")
print("-------------------------------------------")

bids = {}          # Dictionary to store bidder_name : bid_amount
auction_active = True

while auction_active:
    name = input("\nEnter bidder name: ").strip()

    # Prevent empty names
    if not name:
        print("❌ Name cannot be empty.")
        continue

    # Get validated bid
    amount = get_valid_bid()

    # Store bid in dictionary
    bids[name] = amount

    # Ask if more bidders are there
    choice = input("\nAre there any other bidders? (yes/no): ").lower()

    if choice == "no":
        auction_active = False
    elif choice == "yes":
        pass
    else:
        print("⚠️ Invalid choice. Assuming more bidders.")
        pass

# Determine winner
winner, winning_bid = find_highest_bidder(bids)

# Final result display
print("🏆 AUCTION RESULT 🏆")
print("--------------------")
print(f"Winner: {winner}")
print(f"Winning Bid: ₹ {winning_bid}")
