
print("="*30)
print("""
Ardyn Low - S395694
Theo Rothmann - S366484
Anupama Regmi - S390132
""")
print("="*30)

print("""
Assignment 2 - Q1""")
print()

#read file from this file directory
import os
print("Running from:", os.getcwd())
print("This script:", os.path.abspath(__file__))
print()
#caesar shift to solve the loop problem, adjust initial formulas
def caesar_shift(encode:int,shift:int,total_chars:int,min_char:int) ->str:
    shift %= total_chars
    o = chr(min_char + (encode + shift - min_char) % total_chars)
    return o
#decrypt caesarshift
def inverse_caesar_shift(decode:int,shift:int,total_chars:int,min_char:int)->str:
    shift %= total_chars
    c = chr(min_char + (decode - shift - min_char + total_chars) % total_chars)
    return c

def encrypt():
    with open("raw_text.txt", "r") as f:
        text = f.read()


    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))
#Container
    Complete = ""
#Encrypt Ruleset
    for i in text:
        if i.islower() and 'a' <= i <= 'm':
            hidden = caesar_shift(ord(i),shift1*shift2,13,ord('a'))
        elif i.islower() and 'n' <= i <= 'z':
            hidden = caesar_shift(ord(i),-(shift1+shift2),13,ord('n'))
        elif i.isupper() and 'A' <= i <= 'M':
            hidden = caesar_shift(ord(i),-(shift1),13,ord('A'))
        elif i.isupper() and 'N' <= i <= 'Z':
            hidden = caesar_shift(ord(i),(shift2**2),13,ord('N'))
        else:
            hidden = i

        Complete += str(hidden) #check if output is string
#Write Function
    with open("encrypted_text.txt", "w") as f:
        f.write(Complete)
    with open("key.txt","w") as f:
        f.write(f"{shift1}\n{shift2}")

def decrypt():
    with open("encrypted_text.txt", "r") as g:
        text2 = g.read()
    option = input("Use key file? (y/n):")
    
    if option == "y": # For Convinience if user forget their key. 
        with open("key.txt","r")as k:
            key = k.read()
            shift1, shift2 = map(int, key.strip().split("\n"))
    elif option == "n":
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
    else:
        print("Invalid input")
        return
    Decode = ""
#Decrypt Rules
    for i in text2:
        undo=i

        if i.islower() and 'a' <= i <= 'm':
            undo = inverse_caesar_shift(ord(i),shift1* shift2,13,ord('a'))
        elif i.islower() and 'n' <= i <= 'z':
            undo = inverse_caesar_shift(ord(i),-(shift1+shift2),13,ord('n'))
        elif i.isupper() and 'A' <= i <= 'M':
            undo = inverse_caesar_shift(ord(i),-(shift1),13,ord('A'))
        elif i.isupper() and 'N' <= i <= 'Z':
            undo = inverse_caesar_shift(ord(i),(shift2**2),13,ord('N'))

        Decode += undo


    with open("decrypted_text.txt", "w") as g:

        g.write(Decode)
 
def verify():
    with open("raw_text.txt", "r") as raw:
        original = raw.read()

    with open("decrypted_text.txt", "r") as dec:
        decrypted = dec.read()

    if original == decrypted:
        print("Decryption successful")
    else:
        print("Decryption failed")    
#Code Start
while True:
    Q1 = input("Enter e (encrypt), d (decrypt), v (verify): p (exit): ")
    if Q1 == "e":
        encrypt()
    elif Q1 == "d":
        decrypt()
    elif Q1 == "v":
        verify()
    elif Q1 == "p":
        print("Program ended.")
        break
    else:
        print("Invalid input")
