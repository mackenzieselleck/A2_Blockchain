def task_2():

    #hard coded example
    inv = "01|32|12|D"
    sig = "0123456789abcdef"
    ver = True
    sender = "D"

    return bft(inv, sig, ver, sender)

def bft(inv, sig, ver, sender):

    nodes = ["A", "B", "C", "D", "E", "F"]
    x = len(nodes)
    f = (x - 1) // 3
    t = 2 * f + 1
    n = 0
    y = 0

    bft_opt = get_malicious_input(x)
    

    for i, node in enumerate(nodes):
        if i < bft_opt:
            if ver:
                
                print(node + " REJECTS inventory entry")
            else:
                y += 1
                print(node + " ACCEPTS inventory entry")
        else:
            if ver:
                y += 1
                print(node + " ACCEPTS inventory entry")
            else:
                
                print(node + " REJECTS inventory entry")

    
    if y >= t:
        print("inventory was ACCEPTED and entered into databases")
    else:
        print("inventory was REJECTED")

    if bft_opt >= f:
        print("Reminder: malicious nodes is outside of fault tolerance - consensus results aren't accurate")

    return 0

def get_malicious_input(max_nodes):
    while True:
        try:
            value = int(input(f"Enter number of malicious nodes (0–{max_nodes}): "))

            if 0 <= value <= max_nodes:
                return value
            else:
                print(f"Please enter a number between 0 and {max_nodes}")

        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return value

task_2()

            



        






