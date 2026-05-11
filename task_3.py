import hashlib

def task_3():
    query = get_query()
    sig = sign_query(query, 1)

    
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
    
def sign_query(query, user):

    #authentic user keys -> procurement officer
    if user == 1:
        p = 1080954735722463992988394149602856332100628417
        q = 1158106283320086444890911863299879973542293243
        e = 106506253943651610547613
    #random key for non-authentic user for demo purposes
    else:
        p = 3497632264241549723202351321430484106991267637
        q = 5421985543494656130483668848617934086970432969
        e = 65537

    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = int(hashlib.sha256(query.encode()).hexdigest(), 16)
    s = pow(s, d, n)
   
    return s
    
    
task_3()