def task_1(actual, claim, quantity, price, location):
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

    
    # new record incoming to be signed/verified and sent off for consensus
    new_record = []   #['ID', 'Quantity', 'Price', 'Location']
    new_id = get_id()                         
    new_record.append(f"{new_id}")            #ID
    new_record.append(f"{quantity}")    #Quantity
    new_record.append(f"{price}")          #Price
    new_record.append(f"{location}") #Location

    output = ""
   
    # formatting rec for hashing 
    new_record = f"{new_record[0]}|{new_record[1]}|{new_record[2]}|{new_record[3]}"
    

    # hashing new rec using SHA-256
    hashed_new_rec = hashlib.sha256(new_record.encode()).hexdigest()

    # turning hash to decimal for signing an verifiying
    dec_new_rec = int(hashed_new_rec, 16)  # 16 bc hexadec is base 16
    
    # SIGNING: 
    # record signature calling signing function
    rec_sig = gen_sig(dec_new_rec, all_keys[actual]['p'], all_keys[actual]['q'], all_keys[actual]['e'])
    output += f"Signing new record using {actual}'s private key\n"
    output += f"Record Signature: {rec_sig}\n\n"

    # VERIFIYING:
    # verifying record signature calling verification function
    ver_sig, o = gen_ver(hashed_new_rec, dec_new_rec, rec_sig, all_keys[claim]['p'], all_keys[claim]['q'], all_keys[claim]['e'])
    output += o

    #authentic if true
    if ver_sig:
        output += f"Record from Inventory {actual} is authenticated\n\n"
    #unauthentic if false
    else:
        output += f"Inventory {actual} is claiming to be {claim}, but is NOT... Record is unauthentic\n\n"
        
    return ver_sig, output, new_record


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
    output = ""

    if dec_new_rec == decrypt_ver:            # Testing if decrypted signature is the same as record
        output += f"Signature Verificaiton VALID\nNew Record Hash: {hashed_new_rec}\nDecrypted Sig Hash: {hashed_decrypt_rec}\n\n" #Inputed New Record (dec): {dec_new_rec}\nDecrypted Verified New Record: {decrypt_ver}
        return True, output
    else:
        output += f"Signature Verificaiton INVALID\nNew Record Hash: {hashed_new_rec}\nDecrypted Sig Hash: {hashed_decrypt_rec}\n\n"
        return False, output


#calculating new record ID   
def get_id():

    highest = 0

    #finds latest iventory ID
    with open("inv_A.txt", 'r') as f:
        for line in f:
            if line.startswith("ID:"):
                current = int(line.split(": ")[1])
                if current > highest:
                    highest = current

    #returns latest iventory ID for new record
    return str(highest + 1).zfill(2)

