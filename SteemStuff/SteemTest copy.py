from steem import Steem
from steem.account import Account
from random import randint
from datetime import datetime

s = Steem()
account = Account('raffle')
lastMinute = -1
checkedThisHour = False
candidates = []
pot = 0
price = 1
lastIndex = -1

def adduser(username, tickets):
    for x in range(0, tickets):
        print("Added share for " + username)
        candidates.append(username)
    return (tickets * price)

def iterateGenerator(genny):
    global lastIndex
    if lastIndex < genny['index']:
        lastIndex = genny['index']
    if genny['type'] == 'transfer':
        #print("Index " + str(genny['index']) + ": " + genny['from'] + " paid us " + str(genny['amount']) + "!")
        amountss = genny['amount']
        decLoc = amountss.index('.')
        substr = amountss[:decLoc]
        actualvalue = int(int(substr) / price)
        global pot
        pot += adduser(genny['from'], actualvalue)
    else:
        print("Index " + str(genny['index']) + ": paid us nothing!")

def checkMinute():
    print('Checked Minute: ' + str(lastMinute))

def checkHour():
    print('checked hour')
    checkedThisHour = True

def everyMinute():
    file = open('indexfile.txt', 'r')
    readint = int(file.read())
    if readint > lastIndex:
        lastIndex = readint
    else:
        file.close
        file = open('indexfile.txt', 'w')
        file.write(str(lastIndex))
    file.close()

while True:
    if datetime.now().time().minute > lastMinute:
        lastMinute = datetime.now().time().minute
        checkMinute()
    if datetime.now().time().hour == 12:
        if checkedThisHour = False:
            checkHour()
    else:
        checkedThisHour = False

    gen = account.get_account_history(10000, 10000, (lastIndex + 1), None, -1, None, False)

while True:
    try:
        nex = next(gen)
        iterateGenerator(nex)
    except StopIteration:
        print("Nothing here!")
        break

#Roll
candidateLength = len(candidates)
if candidateLength > 0:
    randomInteger = randint(0, candidateLength - 1)
    print("Send " + str(pot) + " sbd to " + candidates[randomInteger] + ", who bought " + str(candidates.count(candidates[randomInteger])) + " tickets!")

file = open('indexfile.txt', 'r')
readint = int(file.read())
if readint > lastIndex:
    lastIndex = readint
else:
    file.close
    file = open('indexfile.txt', 'w')
    file.write(str(lastIndex))
file.close()
