import hashlib

def task_3():
    auth_keys = {
        'p': 1080954735722463992988394149602856332100628417,
        'q': 1158106283320086444890911863299879973542293243,
        'e': 106506253943651610547613
    }
    other_keys = {
        'p': 3497632264241549723202351321430484106991267637,
        'q': 5421985543494656130483668848617934086970432969,
        'e': 65537
    }
    user = 2

    query = get_query()
    if user == 1:
        sig = sign_query(query, auth_keys['p'], auth_keys['q'], auth_keys['e'])
    else:
        sig = sign_query(query, other_keys['p'], other_keys['q'], other_keys['e'])

    ver = verify_user(query, sig, auth_keys['p'], auth_keys['q'], auth_keys['e'])
    return

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
    
def sign_query(query, p, q, e):

    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = int(hashlib.sha256(query.encode()).hexdigest(), 16)
    s = pow(m, d, n)
   
    return s
    
def verify_user(query, sig, p, q, e):

    m = int(hashlib.sha256(query.encode()).hexdigest(), 16)
    n = p * q
    c = pow(sig, e, n)

    if c == m:
        ver = True
    else:
        ver = False

    return ver






task_3()