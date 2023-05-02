import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

    conn = sqlite3.connect('pokemon.sqlite')
    sql = f"""SELECT *
            FROM imported_pokemon_data
            WHERE pokedex_number = {arg}"""

    # Execute the SQL query and get the results
    cursor = conn.execute(sql)
    row = cursor.fetchone()
    if row is None:
        print(f"Could not find a Pokemon with pokedex number {arg}")
        sys.exit()

    name = row[29]
    type1 = row[35]
    type2 = row[36]
    against = [float(row[i]) for i in range(4,22)]

    # Analyze the strengths and weaknesses of the Pokemon
    strengths = []
    weaknesses = []

    for j, factor in enumerate(against):
        if factor > 1:
            strengths.append(types[j])
        elif factor < 1:
            weaknesses.append(types[j])

    # Print the results
    print(f"Analyzing {arg}")
    print(f"{name} ({type1} {type2}) is strong against {', '.join(strengths)} but weak against {', '.join(weaknesses)}")

    # Add the Pokemon to the team list
    team.append(name)

    # Close the database connection
    conn.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")