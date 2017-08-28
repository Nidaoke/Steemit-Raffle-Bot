#Import dependencies
from steem import Steem
from steem.account import Account
from random import randint
from datetime import datetime

#Create steem commit usage and account generator
s = Steem()
account = Account('raffle')
#set some variables
lastMinute = -1 #Last minute that was checked
checkedThisHour = False #Have we checked this hour
candidates = [] #Who paid
pot = 0 #How much money in total
price = 2 #How much does a ticket cost
lastIndex = 31 #What's the last accountgen we checked

def adduser(username, tickets): #Add a user to the candidates
    global candidates
    global pot
    global s
    global lastIndex
    for x in range(0, tickets):
        print("Added share for " + username)
        candidates.append(username)
    return (tickets * price)

def iterateGenerator(genny): #Iterate through the accountgen
    global candidates
    global pot
    global s
    global lastIndex
    if lastIndex < genny['index']: #Make sure we're only checking things we haven't before
        lastIndex = genny['index']
    if genny['type'] == 'transfer': #If someone paid us money
        if genny['from'] != 'raffle': #That's not us
            amountss = genny['amount'] #Get the value they paid us 
            decLoc = amountss.index('.')
            substr = amountss[:decLoc]
            actualvalue = int(int(substr) / price) #Amount of tickets
            global pot
            pot += adduser(genny['from'], actualvalue) #Adjust the money pool
            print("Added " + genny['from'] + " for " + str(actualvalue) + " tickets for " + str(pot) + " pot.")
    else:
        print("Index " + str(genny['index']) + ": paid us nothing!")

def checkMinute(): #Check this every minute
    print('Checked Minute: ' + str(lastMinute))
    everyMinute()

def checkHour(): #Check the hour (For 12 and 0)
    global candidates
    global pot
    global s
    global lastIndex
    global lastMinute
    print('checked hour')
    checkedThisHour = True

    if datetime.now().time().hour == 4 or datetime.now().time().hour == 16:
        candidateLength = len(candidates)
        if candidateLength > 0:
            randomInteger = randint(0, candidateLength - 1)
            print("Send " + str(pot * (3/4)) + " sbd to " + candidates[randomInteger] + ", who bought " + str(candidates.count(candidates[randomInteger])) + " tickets!")
            s.commit.transfer(candidates[randomInteger], (pot * (3/4)), 'SBD', 'Congratulations!', 'raffle')
        candidates.clear() #Reset values
        pot = 0
    lastMinute = -1

def everyMinute(): #Checked every minute
    global candidates
    global pot
    global s
    global lastIndex
    '''file = open('indexfile.txt', 'r') #Adjust index to look for
    readint = int(file.read())
    if readint > lastIndex:
        lastIndex = readint
    else:
        file.close
        file = open('indexfile.txt', 'w')
        file.write(str(lastIndex))
    file.close()'''

    if checkedThisHour == True:
        checkedThisHour = False
    
    #Generate out account history
    gen = account.get_account_history(10000, 10000, (lastIndex + 1), None, -1, None, False)

    while True: #Iterate through the account history
        try:
            print("Iterating")
            nex = next(gen)
            iterateGenerator(nex)
        except StopIteration:
            print("Nothing here!")
            break

while True:
    if datetime.now().time().minute == 0:
        if checkedThisHour == False:
            checkHour()
    else:
        if datetime.now().time().minute > lastMinute:
            lastMinute = datetime.now().time().minute
            checkMinute()
        
'''while True: #ALways occur
    #If it's every 12 hours
    if datetime.now().time().hour == 0 or datetime.now().time().hour == 12:
        if checkedThisHour == False:
            checkHour()
    else:
        if checkedThisHour == True:
            checkedThisHour = False;
    #Check every minute
    if datetime.now().time().minute > lastMinute:
        lastMinute = datetime.now().time().minute
        checkMinute()
    
 '''       
