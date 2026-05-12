import hashlib

def task_3():
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

    #will change to input from HTML
    user = 1

    #retrieves query
    query = get_query()
    #authentic user sign with authentic keys
    if user == 1:
        sig = sign_query(query, auth_keys['p'], auth_keys['q'], auth_keys['e'])
    #unauthentic user sign with unauthentic keys
    else:
        sig = sign_query(query, other_keys['p'], other_keys['q'], other_keys['e'])

    #verify user before accepting query
    ver = verify_user(query, sig, auth_keys['p'], auth_keys['q'], auth_keys['e'])

    #if authentic respond
    if ver:
        multi_sig(query)
    #if unauthentic reject
    else:
        print("Unauthorised User. Cannot submit query")
    
    return

#retrieves query -> will change with HTML
def get_query():

    while True:

        query = input("For item quantity -> GET_QUANTITY <ItemID>: ")

        q = query.split()

        if len(q) != 2:
            print("Invalid format")
            continue

        prompt, item_id = q

        if prompt != "GET_QUANTITY":
            print("Invalid query")
            continue

        return query
    
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

    if c == m:
        ver = True
    else:
        ver = False

    return ver

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


    #submit ID to PKG
    for node in inventories:
        g = pow(node['id'], d, n)
        #return signed ID
        node['sig'] = g
        r = pow(node['ran_val'], e, n)
        t = r * t
    
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
    s = s % n
    multi_sig_1 = pow(s, e, n)
    #response and signature is sent
    print(f"{i_a}\nSignature: {multi_sig_1}")

    #verifies signature
    for node in inventories:
        g_n = g_n * node['id']
    
    multi_sig_2 = pow(g_n * t, m_a, n)

    if multi_sig_1 == multi_sig_2:
        print("Signature Verified, response accepted")
    else:
        print("Signature Invalid, response rejected")
    
    return
   

    
#searches the inventories for information
def search_inventory(inventory, query):
     
     prompt, item_id = query.split()

     with open(inventory, 'r') as f:
        records = f.read().split('\n\n')
        for record in records:
            if item_id in record:
                lines = record.split('\n')
                if "Quantity:" in lines[1]:
               
                    return lines[1].split(': ')[1]
        else:
            return "not found"


        f.close


task_3()