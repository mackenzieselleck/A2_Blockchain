# For hashing the record
import hashlib 

# This initalises the key parameters
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

# putting all the keys in one variable for simplicity
all_keys = {'A':keys_A, 'B':keys_B, 'C':keys_C, 'D':keys_D}

# SIGNING FUNCTION
def gen_sig(record, p, q, e):
    n = p * q                          # calc-ing 'n' pub-key parameter
    totient = (p - 1) * (q - 1)        # calc-ing 'totient' for private key gen
    d = pow(e, -1, totient)            # calc-ing 'd' private key for signing pow(e, -1, totient_param) == d = e^-1 mod totient
    signed_record = pow(record, d, n)  # calc-ing 's' signed record pow(record, d, n) == s = hash_rec^d mod n
    return signed_record

# VERIFYING FUNCTION
def gen_ver(hashed_new_rec, dec_new_rec, signed_recored, p, q, e):
    n = p * q                                 # calc-ing senders 'n' pub-key parameter
    decrypt_ver = pow(signed_recored, e, n)   # decrypting signature
    hashed_decrypt_rec = hex(decrypt_ver)[2:] # gets rid of '0x' + THIS IS SHOWING THAT THE OG HASH OF THE RECORD IS tHE SAME AS IF decrypted sig WAS HASHED

    if dec_new_rec == decrypt_ver:            # Testing if decrypted signature is the same as record
        print(f"Signature Verificaiton VALID\nNew Record Hash: {hashed_new_rec}\nDecrypted Sig Hash: {hashed_decrypt_rec}") #Inputed New Record (dec): {dec_new_rec}\nDecrypted Verified New Record: {decrypt_ver}
        return True
    else:
        print(f"Signature Verificaiton INVALID")
        return False

# Simulating a new record coming in (through user input)
# (new record incoming to be signed/verified and sent off for consensus)
new_record = []                                #['ID', 'Quantity', 'Price', 'Location']
new_record.append(input("ID: "))               #ID
new_record.append(input("Quantity: "))         #Quantity
new_record.append(input("Price: "))            #Price
new_record.append(input("Location: ").upper()) #Location

# This simulates if a inventory claims to be from a 
# different location compared to its TRUE location\
actual = new_record[3] # because [3] = ['0 ID', '1 Quantity', '2 Price', '3 Location']
while True: 
    claim = input("What inventory are you claiming to be: \n1. A\n2. B\n3. C\n4. D\n")
    if claim == '1':
        claim = 'A'
        break
    elif claim == '2':
        claim = 'B'
        break
    elif claim == '3':
        claim = 'C'
        break
    elif claim == '4':
        claim = 'D'
        break

# formatting rec for hashing 
new_record = f"{new_record[0]}|{new_record[1]}|{new_record[2]}|{new_record[3]}"
print(f"New record inputed: {new_record}")
print(f"Actal Inventory: {actual}\nClaiming to be: {claim}") # showing claimed location vs actial 

# hashing new rec using SHA-256
hashed_new_rec = hashlib.sha256(new_record.encode('utf-8')).hexdigest()
print(f"Hashed new record: {hashed_new_rec}")

# turning hash to decimal for signing an verifiying
dec_new_rec = int(hashed_new_rec, 16)  # 16 bc hexadec is base 16
print(f"Hash to decimal: {dec_new_rec}")

# SIGNING: 
# record signature calling signing function
rec_sig = gen_sig(dec_new_rec, all_keys[actual]['p'], all_keys[actual]['q'], all_keys[actual]['e'])
print(f"Signing new record using {actual}'s private key")
print(f"Record Signature: {rec_sig}")

# VERIFIYING:
# verifying record signature calling verification function
ver_sig = gen_ver(hashed_new_rec, dec_new_rec, rec_sig, all_keys[claim]['p'], all_keys[claim]['q'], all_keys[claim]['e'])

if claim != actual:
    print(f"Inventory {actual} is claiming to be {claim}, but is NOT... Rejected!")
elif ver_sig == True:
    print(f"Record from Inventory {actual} is authenticated and ready for consensus")
 

'''
# Ignore:
# Old version without claim vs actual

# seeing what keys to use based off of the claimed lcoation the new record is from
# record locaiton category means *where the record has been added and sent from*
if new_record.endswith("A"):     
    rec_sig = gen_sig(dec_new_rec, keys_A['p'], keys_A['q'], keys_A['e'])
    ver_sig = gen_ver(hashed_new_rec, dec_new_rec, rec_sig, keys_A['p'], keys_A['q'], keys_A['e'])
    inv = new_record  #ID|Quantity|Price|Location
    print(f"Record Signature: {rec_sig}") # see if worked

elif new_record.endswith("B"):
    rec_sig = gen_sig(dec_new_rec, keys_B['p'], keys_B['q'], keys_B['e'])
    ver_sig = gen_ver(hashed_new_rec, dec_new_rec, rec_sig, keys_B['p'], keys_B['q'], keys_B['e'])
    inv = new_record  #ID|Quantity|Price|Location
    print(f"Record Signature: {rec_sig}") # see if worked

elif new_record.endswith("C"):
    rec_sig = gen_sig(dec_new_rec, keys_C['p'], keys_C['q'], keys_C['e'])
    ver_sig = gen_ver(hashed_new_rec, dec_new_rec, rec_sig, keys_C['p'], keys_C['q'], keys_C['e'])
    inv = new_record  #ID|Quantity|Price|Location
    print(f"Record Signature: {rec_sig}") # see if worked

elif new_record.endswith("D"):
    rec_sig = gen_sig(dec_new_rec, keys_D['p'], keys_D['q'], keys_D['e'])
    ver_sig = gen_ver(hashed_new_rec, dec_new_rec, rec_sig, keys_D['p'], keys_D['q'], keys_D['e'])
    inv = new_record  #ID|Quantity|Price|Location
    print(f"Record Signature: {rec_sig}") # see if worked


TASK SPECS:

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
