import random

# Read in the menu from the rolls.txt file
with open('rolls.txt', 'r') as reader:
    menu = reader.readline()

# Read in the last order from the last_order.txt file
with open('ordered.txt', 'r+') as reader:
    ordered = reader.readline()
    reader.truncate()


# Make a list of the rolls and remove the ones that were ordered last time
rolls_list = menu.split(",")
ordered_list = ordered.split(",")

# Need a new list to hold the options to avoid the issue of removing from the first list
# that we encountered earlier
options = []
for item in rolls_list:
    for order in ordered_list:
        if order != item:
            options.append(item)

# Get the 6 rolls to order today
to_order = []
for roll in range(0,6):
    to_order.append(random.choice(options))

print('Today, you should order these 6 rolls\n')
for i, roll in enumerate(to_order):
    print(f"{i + 1}. {roll}\n")

# Write the latest order to the order file 
with open('ordered.txt', 'w') as writer:
    for item in to_order:
        writer.write(item + ",")
    print('Finished Writing Order')



