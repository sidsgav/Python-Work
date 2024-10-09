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
            
            
        

numberArray = [1, 2, 4, 5, 7, 8, 9]
print(numberArray)
targetValue = int(input("\nWhat value are you searching for? "))
binary_search(numberArray, targetValue)
continuePlaying = input("\nWould you like to go again(Y/N) ")
if continuePlaying == 'Y':
    numberArray = [1, 2, 4, 5, 7, 8, 9]
    print(numberArray)
    targetValue = int(input("\nWhat value are you searching for? "))
    binary_search(numberArray, targetValue)
else:
    print("\nOk bye.")

    


