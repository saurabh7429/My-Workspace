# question 1 

# def place_value(n):
#     num = list(str(n))
#     for d in num:
#         print(d, " * ", 10 ** (len(num)-num.index(d)-1), " = ", int(d)*( 10 ** (len(num)-num.index(d)-1)))

# num = int(input("Enter a number: "))
# place_value(num)


# questnion 2

# def aryabhata_pi():
#     return 3.1416
# print("Aryabhata's value of Pi:", aryabhata_pi())



# question 3

import math

def degre(d):
    rad = math.radians(d)
    print(round(math.sin(rad), 6))
    print(round(math.cos(rad), 6))
    print(round(math.tan(rad), 6))

deg = int(input("Enter degree :"))
degre(deg)













# def expansion(a, b):
#     return (a+b)**2

# print(expansion(1,1))