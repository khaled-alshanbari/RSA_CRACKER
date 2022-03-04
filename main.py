import math
import random
import base64
import os
from tkinter import filedialog

die = random.SystemRandom()  # A single dice.

def get_Desktop():
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    return desktop


def single_test(n, a):
    exp = n - 1

    while not exp & 1:
        exp >>= 1

    if pow(a, exp, n) == 1:

        return True

    while exp < n - 1:
        if pow(a, exp, n) == n - 1:

            return True
        exp <<= 1


    return False


def miller_rabin(n, k=50):
    for i in range(k):
        a = die.randrange(2, n - 1)
        if not single_test(n, a):
            return False

    return True


def multiplicativeInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x
    return -1

def EuclidExtended(mod, b):
    # Base Case
    if mod == 0:
        return b, 0, 1

    gcd, x1, y1 = EuclidExtended(b % mod, mod)
    x = y1 - (b // mod) * x1
    y = x1
    return gcd, x, (y%mod)

def gcd(a,b):
    if(b==0):
        return a
    else:
        return gcd(b,a%b)

def RSAEnc(message,N,e):
    CipherText=""
    for i in message:
        c = pow(ord(i),e,N)
        CipherText+=chr(c)


    return CipherText

def RSADec(message,p,q,d):

    N=q*p

    PlainText=""
    for i in message:
        m = pow(ord(i), d, N)
        PlainText+=chr(m)


    return PlainText

def PivKey(e,p,q):
    phi = (p-1)*(q-1)
    return multiplicativeInverse(e,int(phi))





def KeyGen():
    Proceed=False
    print("Generating P , Q ,E, and D ......")
    while(True):
        p=random.getrandbits(8)
        if miller_rabin(p):
            Proceed = True
        if Proceed == True:
                Proceed = False
                break
    while (True):
        q = random.getrandbits(8)
        if miller_rabin(q):
                Proceed = True
        if Proceed == True:
                Proceed = False
                break
    phi = (p-1)*(q-1)
    while(True):
        e = random.getrandbits(8)
        if gcd(e,phi) == 1:
            Proceed = True
        if Proceed == True:
            break

    return p,q,e
def isRoot(N,b):
    number = 3*N+pow(b,2)
    root = math.sqrt(number)
    if int(root + 0.5) ** 2 == number:
        return True,root
    else:
        return False,root

def DifferenceOfSquares(N):
    a = 1
    b = 1
    perfectSquare = False
    for i in range(1,100):

        perfectSquare,a = isRoot(N,i)
        if perfectSquare == True:
            b = i
            break

    p = gcd(N,a-b)
    q = gcd(N,a+b)
    if perfectSquare == True:
        return p,q
    elif perfectSquare == False:
        print("Cannot crack it")


def RSACrack(message,p,q,e):
    print("Cracking....")
    d = PivKey(e,p,q)
    return RSADec(message,p,q,d)




Greeting_Message="hello, this is a program to Encrypt and decrypt using RSA algorithm.\n[+] Enter 1 to generate RSA encryption Keys\n[+] Enter 2 to encrypt a message\n[+] Enter 3 to encrypt a file\n[+] Enter 4 to decrypt a message\n[+] Enter 5 to decrypt a file\n[+] Enter 6 show public & private Keys\n[+] Enter 7 to crack RSA"
Deskpath = get_Desktop()

while(True):
    print(Greeting_Message)
    choice = int(input("-> "))
    if choice == 1:
        try:
            path = os.getcwd()
            p,q,e = KeyGen()
            with open('RSA Private Kyes.txt','w+') as file:
                file.write(str(p))
                file.write('\n\n')
                file.write(str(q))
                file.write('\n\n')
                file.write(str(e))
                file.write('\n\n')
                file.write(str((p-1)*(q-1)))
                file.write('\n\n')
                file.write(str(p*q))
                file.write('\n\n')
                file.write(str(PivKey(e,p,q)))
                print("RSA Keys was generated Successfuly")

                with open('RSA Public Kyes.txt', 'w+') as Pubfile:

                    Pubfile.write(str(e))
                    Pubfile.write('\n\n')
                    Pubfile.write(str(p*q))
        except Exception as e:
            print(e)
    elif choice ==2:
        with open('RSA Public Kyes.txt','r') as file:
            Keys = file.read().split('\n\n')
            print("Encrypted Message: ", RSAEnc(input("enter a message: "),int(Keys[1]),int(Keys[0])))
        pass
    elif choice == 3:
        with open('RSA Public Kyes.txt', 'r') as file:
            Keys = file.read().split('\n\n')

        path = str(filedialog.askopenfilename(initialdir=Deskpath, title='Select a file to Encrypt')).strip()
        with open(path,'r') as file:
            data = file.read()
            CipherText = RSAEnc(data,int(Keys[1]),int(Keys[0]))
            with open(path,'w') as file2:
                file2.write(CipherText)
        print("Ecnryption Process Completed")
    elif choice == 4:
        with open('RSA Private Kyes.txt', 'r') as file:
            Keys = file.read().split('\n\n')
            PlainText = RSADec(input("Enter a message: "), int(Keys[0]), int(Keys[1]), int(Keys[5]))
        print("Decrypted Massage: ",PlainText)
        pass
    elif choice == 5:
        with open('RSA Private Kyes.txt', 'r') as file:
            Keys = file.read().split('\n\n')
            path = str(filedialog.askopenfilename(initialdir=Deskpath, title='Select a file to Encrypt')).strip()
        with open(path,'r') as file:
            data = file.read()
            PlainText = RSADec(data,int(Keys[0]),int(Keys[1]),int(Keys[5]))
            with open(path,'w') as file2:
                file2.write(PlainText)
        print("Deryption Process Completed")
    elif choice == 6:
        with open('RSA Public Kyes.txt', 'r') as file:
            Keys = file.read().split('\n\n')
            print("[+] Public Keys [+]")
            print("e :",Keys[0])
            print("N :", Keys[1])
        with open('RSA Private Kyes.txt', 'r') as file:
            Keys = file.read().split('\n\n')
            print("[+] Private Keys [+]")
            print("p :",Keys[0])
            print("q :", Keys[1])
            print("phi :", Keys[3])
            print("d :", Keys[5])
    elif choice == 7:
        p,q=DifferenceOfSquares(int(input("Enter public Key (N) : ")))
        PlainText = RSACrack(input("Enter the encrypted message -> : "),int(p),int(q),int(input("Enter Public key (e) : ")))
        print("Cracked Message: ",PlainText)
        pass
    else:
        exit(1)
