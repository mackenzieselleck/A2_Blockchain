def task_2():

    #hard coded example - will replace once Task 1 is complete
    inv = "01|32|12|D"
    sig = "0123456789abcdef"
    ver = True


    #perform Byzantine Fault Tolerance
    return bft(inv, sig, ver)

def bft(inv, sig, ver, sender):

    #hard code variables will replace once Task 1 is complete
    nodes = ["A", "B", "C", "D"]
    #fault tolerance algorithms
    n = len(nodes)
    f = (n - 1) // 3
    t = 2 * f + 1
    #initialise vote
    v = 0

    #get malicious nodes - prove BFT
    bft_opt = mal_input(n)
    

    #simulates node voting based on whether verification result
    for i, node in enumerate(nodes):
        #if malicious node - reject verified inv, accept tampered inv
        if i < bft_opt:
            if ver:
                
                print(node + " REJECTS inventory entry")
            else:
                v += 1
                print(node + " ACCEPTS inventory entry")
        #if trustworthy node - accept verified inv, reject tampered inv
        else:
            if ver:
                v += 1
                print(node + " ACCEPTS inventory entry")
            else:
                
                print(node + " REJECTS inventory entry")

    #if accept votes are meet threshold, accept inventory and append databases
    if v >= t:
        print("inventory was ACCEPTED and entered into databases")
        append_database(inv)
    else:
        print("inventory was REJECTED")

    #reminder of accurate results based on malicious nodes (for demo)
    if bft_opt >= f:
        print("Reminder: malicious nodes is outside of fault tolerance - consensus results aren't accurate")

    return 0

#for demo, change malicious node amount to show BFT
def mal_input(max_nodes):
    while True:
        try:
            #ensure malicious node input is within node range
            value = int(input(f"Enter number of malicious nodes (0–{max_nodes}): "))

            if 0 <= value <= max_nodes:
                return value
            else:
                print(f"Please enter a number between 0 and {max_nodes}")
        #ensure malicious node input is an integer
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return value

#adds inventory to databases
def append_database(inv):
    #databases for demo
    databases = ['inv_A.txt', 'inv_B.txt', 'inv_C.txt', 'inv_D.txt']
    #split inv entry
    item_id, quantity, price, location = inv.split("|")

    #append inventory to each database
    for database in databases:
        with open(database, 'a') as f:
            f.write(f"ID: {item_id}\n")
            f.write(f"Quantity: {quantity}\n")
            f.write(f"Price: {price}\n")
            f.write(f"Location: {location}\n\n")
        f.close

    return 0

task_2()

            



        






