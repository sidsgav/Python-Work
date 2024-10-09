menuChoice = 0

def display_menu():

    print("1.Linear Search\n2.Binary Search\n3.Bubble Sort\n4.Merge Sort\n5.Insertion Sort\n6.Exit")
    return input("\nWhat conversion option would you like to choose?: ")


def linear_search():
    numberArray = [1, 7, 4, 5, 2, 8, 6, 9]
    print("\n",numberArray)
    targetFound = False
    targetValue = int(input("\nWhat value are you searching for? "))
    for value in range(len(numberArray)):
        if numberArray[value] == targetValue:
            targetFound = True
            print("\nTarget found at position,", value,".")
            break
    if targetFound == False:
        print("\nTarget not found.")
        


def binary_search(numberArray, targetValue):
    startOfListIndex = 0
    endOfListIndex = len(numberArray) - 1
    targetFound = False
    while startOfListIndex <= endOfListIndex and not targetFound:
        midpoint = (endOfListIndex + startOfListIndex) // 2
        if targetValue == numberArray[midpoint]:
            targetFound = True
        elif targetValue > numberArray[midpoint]:
            startOfListIndex = midpoint + 1
        else:
            endOfListIndex = midpoint - 1
    if targetFound == True:
        print("\nThe target value has been found at position ",midpoint)
    else:
        print("\nTarget value has not been found.")


def bubble_sort(numberArray):
    arraySorted = False
    while arraySorted == False:
        swapMade = False

        for element in range(len(numberArray) - 1):
            if numberArray[element] > numberArray[element + 1]:
                temporarySwap = numberArray[element]
                numberArray[element] = numberArray[element + 1]
                numberArray[element + 1] = temporarySwap
                swapMade = True
                print("\n",numberArray)

        if swapMade is False:
            arraySorted = True


def merge_sort(arrayInput):
        
        if len(arrayInput) > 1:
            middle = len(arrayInput) // 2
        
            leftSide = arrayInput[:middle]
            rightSide = arrayInput[middle:]
        
            merge_sort(leftSide)
            merge_sort(rightSide)
        
            i = j = k = 0
        
            while i < len(leftSide) and j < len(rightSide):
                leftSide[i] < rightSide[j]
                arrayInput[k] = leftSide[i]
                i += 1
            else:
                 arrayInput[k] = rightSide[j]
                 j += 1
                 k += 1
        
            while i < len(leftSide):
                arrayInput[k] = leftSide[i]
                i += 1
                k += 1
            
            while j < len(rightSide):
                arrayInput[k] = rightSide[j]
                j += 1
                k += 1


def insertion_sort(arrayInp):    
    
    for i in range(1, len(arrayInp)):
        key = arrayInp[i]
        j = i - 1
        
        # Move elements of arr[0..i-1] that are greater than the key
        # to one position ahead of their current position
        while j >= 0 and key < arrayInp[j]:
            arrayInp[j + 1] = arrayInp[j]
            j -= 1
        
        # Place the key at the correct position
        arrayInp[j + 1] = key


    
while True:
    menuChoice = display_menu()
    if menuChoice == "6":
        break

    elif menuChoice == "1":
        linear_search()

    elif menuChoice == "2":
        numberArray = [1, 2, 4, 5, 7, 8, 9]
        print("\n",numberArray)
        targetValue = int(input("\nWhat value are you searching for? "))
        binary_search(numberArray, targetValue)
        continueSearching = input("\nWould you like to go again(Y/N) ")
        if continueSearching == 'Y':
            numberArray = [1, 2, 4, 5, 7, 8, 9]
            print(numberArray)
            targetValue = int(input("\nWhat value are you searching for? "))
            binary_search(numberArray, targetValue)
        else:
            print("\nOk bye.")

    elif menuChoice == "3":
        numberArray = list(map(int,input("\nEnter your list: ").strip().split()))
        print("\nThe list you have entered is - ", numberArray)
        sortList = input("\nWould you like to sort this list? (Y/N) ")
        if sortList == 'Y':
            bubble_sort(numberArray)
        else:
            continue

    elif menuChoice == "4":
        arrayInput = [38, 27, 43, 3, 9, 82, 10]
        merge_sort(arrayInput)

    elif menuChoice == "5":
        arrayInp = [93, 47, 34, 47, 31]
        insertion_sort(arrayInp)

    else:
        print("Please choose a valid menu option.\n") 

