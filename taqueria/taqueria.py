menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

total = 0.00

#Approach 1

# while True:
#     try:
#         item = input("Item: ").title() # item here is a string
#         if item in menu:
#             total += float(menu.get(item)) # make the price in string format with " "
#             print (f"Total: ${total:.2f}")
#         else:
#             raise KeyError
#         print (f"Total: {total}")
#         continue
#     except EOFError:
#         print()
#         break
#     except KeyError:
#         continue


#Approach 2:

while True:
    try:
        item = input("Item: ").title() # item here is a string
    except EOFError:
        print()
        break

    if item in menu:
                total += menu[item] # if statement fulfils, then key must be in the dic, thus won;t have keyerror
                print (f"Total: ${total:.2f}")



