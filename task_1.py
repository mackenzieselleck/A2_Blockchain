# This initalises the key parameters e.g. [p, q, e]
keys_A = [1210613765735147311106936311866593978079938707, 
          1247842850282035753615951347964437248190231863, 
          815459040813953176289801]

keys_B = [787435686772982288169641922308628444877260947, 
          1325305233886096053310340418467385397239375379, 
          692450682143089563609787]

keys_C = [1014247300991039444864201518275018240361205111, 
          904030450302158058469475048755214591704639633, 
          1158749422015035388438057]

keys_D = [1287737200891425621338551020762858710281638317, 
          1330909125725073469794953234151525201084537607, 
          33981230465225879849295979]

# This
def calc_n(p, q):
    n_param = p * q
    return n_param

def calc_totient(p, q):
    totient_param = (p - 1) * (q - 1)
    return totient_param

def calc_priv_key(e, totient_param): # d = e^-1 mod totient
    d_param = pow(e, -1, totient_param) # if not allowed pow() then do it likw this 
    return d_param

def encrypt_rec():
    return

 





'''
get key values (A, B, C, D) from A2_Blockchain/A2_ListOfKeys.txt and assign them to variables:
in_A_p, in_A_q, in_A_e
in_B_p, in_B_q, in_B_e
in_C_p, in_C_q, in_C_e
in_D_p, in_D_q, in_D_e

Part 1
Inventory A
p = 1210613765735147311106936311866593978079938707
q = 1247842850282035753615951347964437248190231863
e = 815459040813953176289801
Inventory B
p = 787435686772982288169641922308628444877260947
q = 1325305233886096053310340418467385397239375379
e = 692450682143089563609787
Inventory C
p = 1014247300991039444864201518275018240361205111
q = 904030450302158058469475048755214591704639633
e = 1158749422015035388438057

Inventory D
p = 1287737200891425621338551020762858710281638317
q = 1330909125725073469794953234151525201084537607
e = 33981230465225879849295979

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



# RSA components 
# def pub_param_n
# def totient
# def private_key
# def ciphertext
# def plaintext
