# STAR WARS MISSION!
# User is instructed to assemble a team of four people to help them to destroy the Death Star
# Data from the Star Wars API is called on to provide a list of characters available to recruit to team
# The user has an option to select random characters or select their own choices
# The DOB of each character is returned from the SWAPI
# The user is reminded that they need to recruit Leia to continue on their mission
# The user is given details of the Death Star from the SWAPI
# The app writes the mission details to a new file

import requests
import random


# Function to get character data from the Star Wars API
def get_character_data(character_name):
    endpoint = f'https://swapi.dev/api/people/?search={character_name}'
    response = requests.get(endpoint)
    data = response.json()
    if data['count'] == 1:
        return data['results'][0]
    else:
        return None


# Function to assemble the team for the mission
def assemble_team():
    team = []
    for n in range(4):
        choice = input(
            "Do you want to select your own character (1) or generate a random character (2)? Enter 1 or 2: ")
        if choice == '1':
            selected_character = input("Enter the name of a Star Wars character to recruit them to your mission: ")
        elif choice == '2':
            endpoint = 'https://swapi.dev/api/people/'
            response = requests.get(endpoint)
            data = response.json()
            random_character = random.choice(data['results'])['name']
            print(f"Randomly selected character: {random_character}")
            selected_character = random_character
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue

        character_data = get_character_data(selected_character)
        if character_data:
            team.append(character_data)
            print(f"You have selected {character_data['name']} who was born {character_data['birth_year']}")
        else:
            print("Character not found. Please try again.")
    return team


# Function to check if Princess Leia is in the team
def check_for_leia(team):
    for character in team:
        if character['name'].lower() == 'leia organa':
            return True
    return False


# Function to inform the user about the Death Star
def death_star():
    # Endpoint for Death Star data in SWAPI
    endpoint = 'https://swapi.dev/api/starships/9/'

    # Retrieving data from SWAPI
    response = requests.get(endpoint)
    data = response.json()

    # Checking if Death Star data is available
    print(f"This will be a dangerous mission! Good luck! Here are some details of the Death Star:")
    print(f"Name: {data['name']}")
    print(f"Model: {data['model']}")
    print(f"Manufacturer: {data['manufacturer']}")
    print(f"Passengers: {data['passengers']}")


# Star Wars mission setup and introduction
enter_name = input("Welcome to the world of Star Wars!\n"
                   "You have received the mission to defeat Darth Vader and destroy the Death Star...\n"
                   "You need to select four Star Wars characters to recruit to your mission.\n"
                   "But first you need a Star Wars name! Enter your full name: ")

star_wars_name = enter_name[::3].upper()
print("Your new Star Wars name is: ", star_wars_name)

print("Here is a list of all people available to join your mission:")

# Retrieving and displaying character list
endpoint = 'https://swapi.dev/api/people/'
response = requests.get(endpoint)
data = response.json()
for result in data['results']:
    print(result['name'])

# Assembling the team
team = assemble_team()

# Checking for Princess Leia in the team
has_leia = check_for_leia(team)
if not has_leia:
    print("Princess Leia has not been selected for the mission... You need her!")
    leia_choice = input("Would you like to add Princess Leia to your team? (Y/N): ")
    if leia_choice.lower() == 'y':
        leia_data = get_character_data('leia organa')
        if leia_data:
            team.append(leia_data)
            print(f"Princess Leia has been added to your team.")
        else:
            print("Error: Princess Leia not found.")
    else:
        print("Your mission will fail without Princess Leia...")

# Displaying names of team selected
print("Your team for the mission:")
for character in team:
    print(character['name'])

# Death Star details
death_star()

# Writing results to file
with open('mission_details.txt', 'w') as file:
    file.write("Mission Team:\n")
    file.write(f"{star_wars_name}\n")
    for character in team:
        file.write(f"{character['name']}\n")