def task_2(mal):

    #hard coded example - will replace once Task 1 is complete
    inv = "01|32|12|D"
    sig = "0123456789abcdef"
    ver = True


    #perform Byzantine Fault Tolerance
    return bft(inv, sig, ver, mal)

def bft(inv, sig, ver, mal):

    #hard code variables will replace once Task 1 is complete
    nodes = ["A", "B", "C", "D"]
    #fault tolerance algorithms
    n = len(nodes)
    f = (n - 1) // 3
    t = 2 * f + 1
    #initialise vote
    v = 0

    
    output = ""
    #simulates node voting based on whether verification result
    for i, node in enumerate(nodes):
        #if malicious node - reject verified inv, accept tampered inv
        if i < mal:
            if ver:
                
                output += f"{node} REJECTS inventory entry\n"
            else:
                v += 1
                output += f"{node} ACCEPTS inventory entry\n"
        #if trustworthy node - accept verified inv, reject tampered inv
        else:
            if ver:
                v += 1
                output += f"{node} ACCEPTS inventory entry\n"
            else:
                
                output += f"{node} REJECTS inventory entry\n"

    #if accept votes are meet threshold, accept inventory and append databases
    if v >= t:
        output += "Inventory entry was ACCEPTED and entered into databases"
        append_database(inv)
    else:
        output += "Inventory entry was REJECTED"

   
    return output

#for demo, change malicious node amount to show BFT
def mal_input(value):
    while True:
        try:
            #ensure malicious node input is within node range
            value = int(value)

            if 0 <= value <= 4:
                return True, value
            else:
                return False, "Invalid input. Please enter a number between 0 and 4\n"
        #ensure malicious node input is an integer
        except ValueError:
            return False, "Invalid input. Please enter an integer\n"
    
    

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

    return


            



        






