import numpy as np
#import math
# A number is Prime or Not
# Return True or False
def isPrime(number):
    if number > 1:
    	for i in range(2, number):
    		if (number % i) == 0:
    			return False
    			break
    	else:
    		return True
    else:
    	return False


# Python program to display all the prime numbers within an interval
def PrimeBtwInterval(lower, upper):
    lst=[]
    for num in range(lower, upper + 1):
       if num > 1:
           for i in range(2, num):
               if (num % i) == 0:
                   break
           else:
               lst.append(num)
    return lst

# String is Palindrome or not
def isPalindrome(num):
    Temp = num
    Rev = 0
    while(num > 0):
        dig = num % 10
        revrev = rev * 10 + dig
        numnum = num // 10
    if(temp == rev):
        reurn True
    else:
        return False


# Number is Armstrong or not
def isArmstrong(num):
    order = len(str(num))
    sum = 0
    temp = num
    while temp > 0:
       digit = temp % 10
       sum += digit ** order
       temp //= 10
    if num == sum:
       return True
    else:
       return False

# PATTERNS
# Half pyramid pattern
def halfPyramidpattern(n):
    myList = []
    for i in range(1,n+1):
        myList.append("*"*i)
    return (" \n".join(myList))

# Left Half-Pyramid Pattern
def leftHalfPyramidpattern(rows):
    k = 2 * rows - 2
    for i in range(0, rows):
        for j in range(0, k):
            print(end=" ")
        k = k - 2
        for j in range(0, i + 1):
            print("* ", end="")
        print("")
    return ""

# Downward Half-Pyramid Pattern
def downwardHalfPyramidpattern(rows):
    for i in range(rows + 1, 0, -1):
        for j in range(0, i - 1):
            print("*", end=' ')
        print(" ")
    return " "

# Equilateral triangle pattern
def equilateralTrianglepattern(size):
    m = (2 * size) - 2
    for i in range(0, size):
        for j in range(0, m):
            print(end=" ")
        m = m - 1  # decrementing m after each loop
        for j in range(0, i + 1):
            # printing full Triangle pyramid using stars
            print("* ", end=' ')
        print(" ")
    return " "


# Right start Pattern
def rightStartTrianglepattern(rows):
    for i in range(0, rows):
        for j in range(0, i + 1):
            print("*", end=' ')
        print("\r")

    for i in range(rows, 0, -1):
        for j in range(0, i - 1):
            print("*", end=' ')
        print("\r")
    return " "


# Downward star Pattern
def downEquilateralTrianglepattern(rows):
    k = 2 * rows - 2
    for i in range(rows, -1, -1):
        for j in range(k, 0, -1):
            print(end=" ")
        k = k + 1
        for j in range(0, i + 1):
            print("*", end=" ")
        print("")
    return " "

# Filled Diamond PATTERN
def filledDiamondpattern(rows):
    k = 2 * rows - 2
    for i in range(0, rows):
        for j in range(0, k):
            print(end=" ")
        k = k - 1
        for j in range(0, i + 1):
            print("* ", end="")
        print("")

    k = rows - 2

    for i in range(rows, -1, -1):
        for j in range(k, 0, -1):
            print(end=" ")
        k = k + 1
        for j in range(0, i + 1):
            print("* ", end="")
        print("")
    return " "


# Men’s pant style pattern
def menPantShapedpattern(rows):
    print("*" * rows, end="\n")
    i = (rows // 2) - 1
    j = 2
    while i != 0:
        while j <= (rows - 2):
            print("*" * i, end="")
            print("_" * j, end="")
            print("*" * i, end="\n")
            i = i - 1
            j = j + 2
    return " "

# Hollow pyramid pattern
def hollowPyramidpattern( n) :
    k = 0
    for i in range(1,n+1) :
        for j in range(i,n) :
            print(' ', end='')
        while (k != (2 * i - 1)) :
            if (k == 0 or k == 2 * i - 2) :
                print('*', end='')
            else :
                print(' ', end ='')
            k = k + 1
        k = 0;
        print ("")
    for i in range(0, 2 * n -1) :
        print ('*', end = '')
    return " "

# Hollow inverted pyramid pattern
def hollowPyramidpattern(n) :
	for i in range(1,n+1) :
		for j in range(1,i) :
			print (" ",end="")
		for j in range(1,(n * 2 - (2 * i - 1)) +1) :
			if (i == 1 or j == 1 or
			j == (n * 2 - (2 * i - 1))) :
				print ("*", end="")
			else :
				print(" ", end="")
		print (""),
    return " "


# Hollow diamond pattern
def hollowDiamondpattern(n) :
	k = 0;
	for i in range(1,n+1) :
		for j in range(1,n-i+1) :
			print(" ",end="")
		while (k != (2 * i - 1)) :
			if (k == 0 or k == 2 * i - 2) :
				print("*",end="")
			else :
				print(" ",end="")
			k = k + 1
		k = 0
		print(""),

	n = n - 1
	for i in range (n,0,-1) :
		for j in range(0,n-i+1) :
			print(" ",end="")

		k = 0
		while (k != (2 * i - 1)) :
			if (k == 0 or k == 2 * i - 2) :
				print("*",end="")
			else :
				print(" ",end="")
			k = k + 1
		print(""),
    return " "


# Flag shaped pattern
def Flagpattern(row):
    def triangleShape(n):
        for i in range(n):
            for k in range(i+1):
                print('*',end=' ')
            print()

    # Generating Pole Shape
    def poleShape(n):
        for i in range(n):
            print('*')

    triangleShape(row)
    poleShape(row)
    return " "


# Pascal Triangle pattern
def PascalTrianglepattern(row):
    space = 40
    a = [0] * 20
    for i in range(row):

        for spi in range(1,space+1):
            print(" ", end="")

        a[i] = 1

        for j in range(i+1):
            print('%6d' %(a[j]), end = "")

        for j in range(i,0,-1):
            a[j] = a[j] + a[j-1]

        space = space - 3

        print()
    return " "


# Christmas Tree Pattern
def ChristmasTreepattern(row):
    def triangleShape(n):
        for i in range(n):
            for j in range(n-i):
                print(' ', end=' ')
            for k in range(2*i+1):
                print('*',end=' ')
            print()

    # Generating Pole Shape
    def poleShape(n):
        for i in range(n):
            for j in range(n-1):
                print(' ', end=' ')
            print('* * *')

    triangleShape(row)
    triangleShape(row)
    poleShape(row)
    return " "

# Asterisk pattern
def Starpattern(n):
    for i in range(1,2*n):
        for j in range(1,2*n):
            if j==n or i==j or i+j==2*n:
                print('*', end=' ')
            else:
                print(' ', end=' ')
        print()
    return " "








#Factorial
def factorial(n):
 factorial = 1
 if int(n) >= 1:
    for i in range (1,int(n)+1):
        factorial = factorial * i

 return factorial


#Magic Number
#Check
'''def isMagicNumber(n):
    digitCount = int(math.log10(n))+1
    sumOfDigits = 0

    temp = n

    while( digitCount > 1):

      sumOfDigits = 0

      while(temp > 0):
        sumOfDigits += temp%10
        temp = temp//10

      temp = sumOfDigits

      digitCount = int(math.log10(sumOfDigits))+1

    if(sumOfDigits == 1):
        return "True"
    else:
        return "False"
        '''


#Simple and Compound Interest
def interest(p,t,r): #principle, time period, rate
    si = (p * t * r)/100

    A = p * (pow((1 + r / 100), t))
    ci = A - p

    print ("Simple Interest= ",si)
    print ("Compound Interest= ",ci)
    return " "


#AP,GP,HP
def progression(a,d,n): #start, difference/rate, no of terms
     tmp=a
     print("AP: ")
     for i in range(1,n+1):
        print(a, end=' ')
        a =a + d

     print("\n")
     print("HP: ")
     a=tmp
     for i in range(1,n+1):
        print(1/a, end=' ')
        a =a + d

     print("\n")
     print("GP: ")
     a=tmp
     for i in range(0, n):
        curr_term = a * pow(d, i)
        print(curr_term, end =" ")

     return " "


#Matrix Summary
def matSummary(m1): # Pass matrix as numpy array
    print("Summary of Matrix")
    print("Dimensions ",m1.ndim)
    print("Type ",m1.dtype)
    print("Shape ",m1.shape)
    print("Max: ",np.amax(m1))
    print("Min: ",np.amin(m1))
    print("Diagnol elements ",np.diag(m1))
    print("Transpose ",np.transpose(m1))
    return " "


# 2 Matrix
def matsumprod(m1,m2):
    print("Sum ",m1+m2)
    print("Product ",m1*m2)
    return " "
