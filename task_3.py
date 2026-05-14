import hashlib

def task_3(user, query):
    #procurement officer keys
    auth_keys = {
        'p': 1080954735722463992988394149602856332100628417,
        'q': 1158106283320086444890911863299879973542293243,
        'e': 106506253943651610547613
    }
    #nonauthorised keys for demo purposes
    other_keys = {
        'p': 3497632264241549723202351321430484106991267637,
        'q': 5421985543494656130483668848617934086970432969,
        'e': 65537
    }

    output = ""

    user = int(user)

    #authentic user sign with authentic keys
    if user == 1:
        sig = sign_query(query, auth_keys['p'], auth_keys['q'], auth_keys['e'])
        output += f"Query Signature:\n{sig}\n\n"
    #unauthentic user sign with unauthentic keys
    else:
        sig = sign_query(query, other_keys['p'], other_keys['q'], other_keys['e'])
        output += f"Query Signature:\n{sig}\n\n"
    #verify user before accepting query
    ver, o_2 = verify_user(query, sig, auth_keys['p'], auth_keys['q'], auth_keys['e'])
    output += o_2

    #if authentic respond
    if ver:
        output += "User Authentication:\n User verified. Query accepted\n\n"
        output += multi_sig(query)
    #if unauthentic reject
    else:
        output += "Unauthorised User. Cannot submit query\n\n"
    
    return output

#retrieves query -> will change with HTML
def get_query(value):

    while True:


        q = value.split()

        if len(q) != 2:
            return False, "Invalid format. Please use correct formatting\n"
            

        prompt, item_id = q

        if prompt != "GET_QUANTITY":
            return False, "Invalid query. Please use the query prompt 'GET_QUANTITY'\n"
            

        return True, value
    
#signs query 
def sign_query(query, p, q, e):

    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = int(hashlib.sha256(query.encode()).hexdigest(), 16)
    s = pow(m, d, n)
   
    return s

#verifies user   
def verify_user(query, sig, p, q, e):

    m = int(hashlib.sha256(query.encode()).hexdigest(), 16)
    n = p * q
    c = pow(sig, e, n)
    output = ""

    if c == m:
        ver = True
        output += f"Hashed query: {m} is equal to Decrypted Signature: {c}\n\n"
    else:
        ver = False
        output += f"Hashed query: {m} is not equal to Decrypted Signature: {c}\n\n"

    return ver, output

# retrieves response and simulates all inventory signatures
def multi_sig(query):

    #PKG values
    p = 1004162036461488639338597000466705179253226703
    q = 950133741151267522116252385927940618264103623
    e = 973028207197278907211

    #inventory ID and random value
    inventories = [{'inv': 'A', 'id': 126, 'ran_val': 621, 'sig': 0},
                   {'inv': 'B', 'id': 127, 'ran_val': 721, 'sig': 0},
                   {'inv': 'C', 'id': 128, 'ran_val': 821, 'sig': 0},
                   {'inv': 'D', 'id': 129, 'ran_val': 921, 'sig': 0}]


    #calculate PKG keys
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    t = 1
    g_n = 1

    output = ""


    #each inventory submits ID to PKG
    for node in inventories:
        #PKG signs ID using PKG keys
        g = pow(node['id'], d, n)
        #return signed ID to each inventory and save it for later
        node['sig'] = g
        #each inventory then signs their random value using PKG public keys
        r = pow(node['ran_val'], e, n)
        #multiply all signed random numbers
        t = r * t
    #calculate modulus of multiplied signed random numbers
    t = t % n

    #each inventory retrieves response from their database and sign it
    for node in inventories:
        if node['inv'] == 'A':
           i_a = search_inventory('inv_A.txt', query)
           message = str(t) + ', ' + i_a
           m_a = int(hashlib.sha256(message.encode()).hexdigest(), 16)
           s_a = pow(node['ran_val'] * node['sig'], m_a, n)
          
        elif node['inv'] == 'B':
           i_b = search_inventory('inv_B.txt', query)
           message = str(t) + ', ' + i_b
           m_b = int(hashlib.sha256(message.encode()).hexdigest(), 16)
           s_b = pow(node['ran_val'] * node['sig'], m_b, n)
           
        elif node['inv'] == 'C':
           i_c = search_inventory('inv_C.txt', query)
           message = str(t) + ', ' + i_c
           m_c = int(hashlib.sha256(message.encode()).hexdigest(), 16)
           s_c = pow(node['ran_val'] * node['sig'], m_c, n)
           
        elif node['inv'] == 'D':
           i_d = search_inventory('inv_D.txt', query)
           message = str(t) + ', ' + i_d
           m_d = int(hashlib.sha256(message.encode()).hexdigest(), 16)
           s_d = pow(node['ran_val'] * node['sig'], m_d, n)
    
    #signatures and combined to create multi signature
    s = s_a * s_b * s_c * s_d
    #calculate s mod n
    s = s % n
    #signing multi signature
    multi_sig_1 = pow(s, e, n)
    #response and signature is sent to user
    output += f"Query Response: {i_a}\nSignature: {multi_sig_1}\n\n"

    #user verifies signature
    #calculate inventory ID multiplied all together
    for node in inventories:
        g_n = g_n * node['id']
    
    #multiply that with t and sign using hash of result and t mod n
    multi_sig_2 = pow(g_n * t, m_a, n)
    output += f"Verification Signature Calculated: {multi_sig_2}\n\n"

    #if the recieved signature matches the verification signature then it is valid
    if multi_sig_1 == multi_sig_2:
        output += f"{multi_sig_1} is equal to {multi_sig_2}\n"
        output += "Signature Verified, response can be accepted\n"
    else:
        output += f"{multi_sig_1} is not equal to {multi_sig_2}\n"
        output += "Signature Invalid, response should be rejected\n"
    
    return output
   

    
#searches the inventories for information
def search_inventory(inventory, query):
     
     prompt, item_id = query.split()
     find_id = f"ID: {item_id}" 

     with open(inventory, 'r') as f:
        records = f.read().split('\n\n')
        for record in records:
            if find_id in record:
                lines = record.split('\n')
                if "Quantity:" in lines[1]:
               
                    return lines[1].split(': ')[1]
        else:
            return "Item ID not found"


        f


