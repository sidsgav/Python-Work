import random

slotChoices = ['Cherry', 'Bell', 'Lemon', 'Orange', 'Star', 'Skull']
totalCredit = 1.0
costOfPlay = 0.2

def play_slot_round():
    global totalCredit

    totalCredit -= costOfPlay

    rollNo1 = random.choice(slotChoices)
    print("\nYour first roll is: ", rollNo1)
    rollNo2 = random.choice(slotChoices)
    print("\nYour second roll is: ", rollNo2)
    rollNo3 = random.choice(slotChoices)
    print("\nYour third roll is: ", rollNo3)
    if (rollNo1 == rollNo2) and (rollNo1 == rollNo3):
        if rollNo1 == slotChoices[5]:
            print("\nYou have unfortunately ran out of credits. Better luck next time.")
            totalCredit = 0.0
        elif rollNo1 == slotChoices[1]:
            totalCredit += 5.0
        else:
            totalCredit += 1.0
    elif (rollNo1 == slotChoices[5] or rollNo2 == slotChoices[5] or rollNo3 == slotChoices[5]) and (get_skull_count(rollNo1, rollNo2, rollNo3) == 2):
        skullCount = get_skull_count(rollNo1, rollNo2, rollNo3)
        totalCredit -= 1.0
    elif rollNo1 == rollNo2 or rollNo1 == rollNo3 or rollNo2 == rollNo3:
        totalCredit += 0.5

    if totalCredit > 0.0:
        print("\nYour current credit amount is: ", round(totalCredit, 2))

def get_skull_count(rollNo1, rollNo2, rollNo3):
    skullCount = 0
    if rollNo1 == slotChoices[5]:
        skullCount += 1
    if rollNo2 == slotChoices[5]:
        skullCount += 1
    if rollNo3 == slotChoices[5]:
        skullCount += 1
    return skullCount

def get_input_choice(value):
    try:
        choice = int(value)
        validValue = True
    except ValueError:
        validValue = False

    if validValue == False:
        print("\nYou entered an incorrect option")
        return 0

    return choice


print("Your starting credit is: £1 and the cost of each play is 20p")
while totalCredit > 0.0:
    play_slot_round()
    if totalCredit <= 0.0:
        break
    else:
        while True:
            continuePlaying = get_input_choice(input("\nIf you wish to carry on playing choose option 1 or option 2 to withdraw your earnings: "))
            if (continuePlaying == 1 or continuePlaying == 2):
                break
        if continuePlaying == 2:
            break

print("\nYour remaining credit is: ", round(totalCredit, 2))    





        
    
    
    
          
