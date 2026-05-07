# For hashing the record 
import hashlib 

# This initalises the key parameters e.g. [p, q, e]
keys_A = {
          'p':1210613765735147311106936311866593978079938707,
          'q':1247842850282035753615951347964437248190231863,
          'e':815459040813953176289801
         }
keys_B = {
          'p':787435686772982288169641922308628444877260947,
          'q':1325305233886096053310340418467385397239375379,
          'e':692450682143089563609787
         }
keys_C = {
          'p':1014247300991039444864201518275018240361205111,
          'q':904030450302158058469475048755214591704639633,
          'e':1158749422015035388438057
         }
keys_D = {
          'p':1287737200891425621338551020762858710281638317,
          'q':1330909125725073469794953234151525201084537607,
          'e':33981230465225879849295979
         }

# This gets the record from the inventory and formats like so: 
# ID|QUANTITY|PRICE|LOCATION --> 01|32|12|D to then later be hashed, etc...
def get_record(filename):
    inventory = {}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if ":" in line:
                cat, val = line.split(":")
                inventory[cat.strip().upper()] = val.strip()
    
    formatted_rec = f"{inventory['ID']}|{inventory['QUANTITY']}|{inventory['PRICE']}|{inventory['LOCATION']}"
    return formatted_rec

# This calculates 'n' public key parameter
def calc_n(p, q):
    n_param = p * q
    return n_param

# This calculates phi of n (totient)
def calc_totient(p, q):
    totient_param = (p - 1) * (q - 1)
    return totient_param

# This calculates 'd' private key 
def calc_priv_key(e, totient_param):
    d_param = pow(e, -1, totient_param) #pow(e, -1, totient_param) == d = e^-1 mod totient
    return d_param

# This encrypts the record
def encrypt_rec(record, e, n_param):
    ciphertext = pow(record, e, n_param) #pow(m, e, n_param) == c = m^e mod n
    return ciphertext

# This signs the record
def sign(ciphertext, d_param, n_param):
    signed_record = pow(ciphertext, d_param, n_param)
    return signed_record

# This verifies the record
def verify(ciphertext, signed_record, e, n_param):
    verified_record = pow(signed_record, e, n_param)
    
    if verified_record == ciphertext:
        print("The record is verified and has NOT been tampered with.\n")
        return verified_record
    else:
        return print("The record is unverified thus tampered.\n")

# This decrypts the record
def decrypt_rec(verified_record, d_param, n_param):
    dec_verif_rec = pow(verified_record, d_param, n_param)
    return dec_verif_rec


# THIS IS JUST TESTING IF ALL WORKS:
while True:
    input = input("Select the number for which inventory the new record is from: \n"
        "1. inv_A.txt\n"
        "2. inv_B.txt\n"
        "3. inv_C.txt\n"
        "4. inv_D.txt\n")
    if input == "1":
        print("\nInventory A has been selected.")
        filename = "inv_A.txt"
        break
    elif input == "2":
        print("\nInventory B has been selected.")
        filename = "inv_B.txt"
        break
    elif input == "3":
        print("\nInventory C has been selected.")
        filename = "inv_C.txt"
        break
    elif input == "4":
        print("\nInventory D has been selected.")
        filename = "inv_D.txt"
        break

# start calc-ing key components based off chosen inventory
# printing to check if working
if filename == "inv_A.txt":
    print(
        "The key parameters are:\n"
        f"p = {keys_A['p']}\n"
        f"q = {keys_A['q']}\n"
        f"e = {keys_A['e']}\n"
        )
        
    # getting key components
    n_param = calc_n(keys_A['p'], keys_A['q'])
    print(f"This is the public key parameter 'n' : {n_param}\n")
    totient_param = calc_totient(keys_A['p'], keys_A['q'])
    print(f"This is the totient parameter: {totient_param}\n")
    d_param = calc_priv_key(keys_A['e'], totient_param)
    print(f"This is the private key: {d_param}\n") # obvs keep this secret
    
    # initialising record + formating
    record = get_record(filename)
    print(f"This is the record: {record}\n")
    hashed_record = hashlib.md5(record.encode('utf-8')).hexdigest()
    print(f"This is the hashed record: {hashed_record}\n")
    decimal_record = int(hashed_record, 16)
    print(f"This is the hashed record in decimal format: {decimal_record}\n")

    # encrypting record
    ciphertext = encrypt_rec(decimal_record, keys_A['e'], n_param)
    print(f"This is the encrypted record: {ciphertext}\n")

    # signing record
    signed_record = sign(ciphertext, d_param, n_param)
    print(f"This is the signed record: {signed_record}\n")

    # verifying record
    verified_record = verify(ciphertext, signed_record, keys_A['e'], n_param)
    print(f"This is the encrypted verified record: {verified_record}\n")

    # decrypting verified record
    dec_verif_rec = decrypt_rec(verified_record, d_param, n_param)
    print(f"This the decrypted verified record in decimal: {dec_verif_rec}\n")
    print(f"This is the decrypted verified record in hex: {hex(dec_verif_rec)}\n")
    print(f"This is the hashed record to compare to the decrypted one: {hashed_record}\n")



'''
keeping just incase:

    # see if entered inventory is valid
    if filename != "inv_A.txt" or "inv_B.txt" or "inv_C.txt" or "inv_D.txt":
        print("ERROR: Inventory not presents. Choose either:\n" 
              "inv_A.txt\ninv_B.txt\ninv_C.txt\ninv_D.txt")
        
    else:
        filename = filename
        break
'''

'''

def verify(ciphertext, signed_record, e, n_param):
    verified_record = pow(signed_record, e, n_param)
    
    if verified_record == ciphertext:
        return print("The record is verified and has NOT been tampered with")
    else:
        return print("The record is unverified thus tampered")

# This decrypts the record
def decrypt_rec(verified_record, d_param, n_param):
    dec_verif_rec = pow(verified_record, d_param, n_param)
    return dec_verif_rec

'''




'''
keys_A = {
          'p':1210613765735147311106936311866593978079938707,
          'q':1247842850282035753615951347964437248190231863,
          'e':815459040813953176289801
         }
keys_B = {
          'p':787435686772982288169641922308628444877260947,
          'q':1325305233886096053310340418467385397239375379,
          'e':692450682143089563609787
         }
keys_C = {
          'p':1014247300991039444864201518275018240361205111,
          'q':904030450302158058469475048755214591704639633,
          'e':1158749422015035388438057
         }
keys_D = {
          'p':1287737200891425621338551020762858710281638317,
          'q':1330909125725073469794953234151525201084537607,
          'e':33981230465225879849295979
         }
'''










'''
hash = "098f6bcd4621d373cade4e832627b4f6" #means 'test' in md5
hashhex_to_dec_ = int(hash, 16)
print(f'This is the hash (hexadecimal): {hash}')
print(f'This is the decimal of the hex: {hashhex_to_dec_}')
'''
 


'''
def RSA_components(record, p, q, e):

    def calc_n(p, q):
        n_param = p * q

    def calc_totient(p, q):
        totient_param = (p - 1) * (q - 1)

    def calc_priv_key(e):
        d_param = pow(e, -1, calc_totient())  #pow(e, -1, calc_totient()) == d = e^-1 mod totient

    def encrypt_rec(record, e, n):
        ciphertext = pow(record, e, n)            #pow(m, e, n) == c = m^e mod n

    return
'''

'''
Task 1: Digital Signature-Based Record Authentication (10 Marks)
Each inventory node generates a new inventory record representing a recent item update. Before the record
is broadcast to the distributed inventory system, the originating node must apply a digital signature to ensure
the authenticity and integrity of the submitted data.

What You Need to Do
1. Initialise the cryptographic parameters required for digital signature operations using the values
provided in the List of Keys document.

2. Derive any additional key components required for the digital signature process from the provided
parameters, and ensure all required values are explicitly defined in your code.

3. Implement a mechanism that enables an inventory node to digitally sign a newly generated inventory
record prior to submission.

4. Implement a verification process that allows other inventory nodes to validate the authenticity and
integrity of the received record before it proceeds to the consensus stage.

5. In your report, explain how digital signatures contribute to secure record submission in a distributed
inventory environment.
'''