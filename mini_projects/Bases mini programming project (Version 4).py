import re

menuChoice = 0

def display_menu():

    # display menu options and ask user which option they wish to select

    print("\n1.Binary to Denary\n2.Denary to Binary\n3.Hexadecimal to Denary\n4.Denary to Hexadecimal\n5.Hexadecimal to Binary\n6.Binary to Hexadecimal\n7.Exit")
    return input("\nWhat conversion option would you like to choose?: ")

def binary_to_denary():

    binaryValue = input("Enter your binary value: ")
    validValue = validate_binary_input(binaryValue)
    if validValue == True:
        denary = 0
        for digit in binaryValue:
          # left shift in binary means x2  
          denary = denary*2 + int(digit)
        print("\nYour denary number is: " + str(denary))
    else:
        print("\nYou entered an incorrect binary value")

def validate_binary_input(value):

    # set function convert string
    # into set of characters .
    p = set(value)

    # declare set of '0', '1' .
    s = {'0', '1'}

    # check set p is same as set s
    # or set p contains only '0'
    # or set p contains only '1'
    # or not, if any one condition
    # is true then string is accepted
    
    # otherwise not.
    if s == p or p == {'0'} or p == {'1'}:
        return True
    else:
        return False

def denary_to_binary():

    inputValue = input("Input a denary number: ")
    validValue = validate_denary_input(inputValue)
    if validValue == True:
        denary = int(inputValue)
        binary = ""
        while denary > 0:
            binary = str(denary % 2) + binary
            denary = denary // 2

        print("\nYour binary number is: " + binary)


def validate_denary_input(value):

    try:
        denaryValue = int(value)
        validValue = True
    except ValueError:
        validValue = False

    if validValue == True and denaryValue < 0:
        print("\nNegative denary values are unsupported")
        validValue = False
    elif validValue == False:
        print("\nYou entered an incorrect denary value")

    return validValue


def hexadecimal_to_denary():

    hexadecimalInput = input("\nInput your hexadecimal value: ").upper()
    validValue = validate_hexadecimal_input(hexadecimalInput)
    if validValue == True:
        hexToDenaryDict = {'0': 0,'1': 1,'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'A': 10,'B': 11,'C': 12,'D': 13,'E': 14,'F': 15}
        denary = 0
        power = len(hexadecimalInput) - 1
        for digit in hexadecimalInput:
            denary += hexToDenaryDict[digit] * 16 ** power
            power -= 1
        print("\nYour denary value is: " + str(denary))
    else:
        print("\nYou entered an incorrect hexadecimal value")
        
            
def validate_hexadecimal_input(value):
    #pattern = '[0-9a-fA-F]+'
    #match = re.match(pattern, value)
    #print("\nRegex hexadecimal match: ", match)
    #if match:
    #    return True
    #else:
    #    return False
    try:
        int(value, 16)
        return True
    except ValueError:
        return False

def denary_to_hexadecimal():

    conversionTable = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A' , 'B', 'C', 'D', 'E', 'F']

    inputValue = input("\nEnter your denary value: ")
    validValue = validate_denary_input(inputValue)
    if validValue == True:
        denary = int(inputValue)
        hexadecimal = ''
        while denary > 0:
            remainder = denary % 16
            hexadecimal = conversionTable[remainder] + hexadecimal
            denary = denary // 16
        print("\nYour hexadecimal value is: ",hexadecimal)

def hexadecimal_to_binary():

    inputValue = input("\nEnter your hexadecimal value: ")
    validValue = validate_hexadecimal_input(inputValue)
    if validValue == True:
        x = 1
        

# Main program

while True:
    menuChoice = display_menu()

    if menuChoice == "7":
        break
    elif menuChoice == "1":
        binary_to_denary()
    elif menuChoice == "2":
        denary_to_binary()
    elif menuChoice == "3":
        hexadecimal_to_denary()
    elif menuChoice == "4":
        denary_to_hexadecimal()
    elif menuChoice == "5":
        hexadecimal_to_binary()
    elif menuChoice == "6":
        print("Option 6 selected")
    else:
        print("Please choose a valid menu option.\n")
