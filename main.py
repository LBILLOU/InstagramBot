import os
from bot import *
from tkinter import *

window = Tk()
window.title('Instagram Bot Launcher')
window.resizable(height=False,width=False)

# Login/Password Tile
loginPwdTile = Frame(window)
login = Entry(loginPwdTile,width=16)
login.grid(row=0,column=0)
pwd = Entry(loginPwdTile,show="*",width=16)
pwd.grid(row=0,column=1)
spacinglbl0 = Label(loginPwdTile)
spacinglbl0.grid(row=1,column=1)
loginPwdTile.pack(side=TOP)

# Hashtags Tile
hashtagsTile = Frame(window)
userPathLbl = Label(hashtagsTile, text=' UserPath ', anchor=W, width=8)
userPathLbl.grid(row=0,column=0)
userPathIn = Entry(hashtagsTile,width=15)
userPathIn.insert(END, '/Users/***')
userPathIn.grid(row=0,column=1)
hashtagsLbl = Label(hashtagsTile, text=' Hashtags ', anchor=W, width=8)
hashtagsLbl.grid(row=1,column=0)
hashtagsIn = Entry(hashtagsTile,width=15)
hashtagsIn.grid(row=1,column=1)
hashtagsTotal = Label(hashtagsTile, text='-', width=4)
hashtagsTotal.grid(row=1,column=2)
spacinglbl1 = Label(hashtagsTile)
spacinglbl1.grid(row=2,column=1)
hashtagsTile.pack(side=TOP, fill=X)

# Like line
likeLine = Frame(window)
likeVar = IntVar()
likeCheckBtn = Checkbutton(likeLine,variable=likeVar)
likeCheckBtn.grid(row=0,column=0)
likeLbl = Label(likeLine, text='Like', anchor=W, width=8)
likeLbl.grid(row=0,column=1)
likeFreq = Entry(likeLine,width=3,justify='right')
likeFreq.insert(END, 100)
likeFreq.grid(row=0,column=2)
likePrctg = Label(likeLine, text='%', anchor=W, width=2)
likePrctg.grid(row=0,column=3)
likeWait = Entry(likeLine,width=2,justify='right')
likeWait.insert(END, 10)
likeWait.grid(row=0,column=4)
likeSec = Label(likeLine, text='sec', anchor=W, width=4)
likeSec.grid(row=0,column=5)
likeCount = Label(likeLine, text='-', width=4)
likeCount.grid(row=0,column=6)
likeLine.pack(side=TOP)

# Comment line
commentLine = Frame(window)
commentVar = IntVar()
commentCheckBtn = Checkbutton(commentLine,variable=commentVar) #,state=DISABLED
commentCheckBtn.grid(row=0,column=0)
commentLbl = Label(commentLine, text='Comment', anchor=W, width=8)
commentLbl.grid(row=0,column=1)
commentFreq = Entry(commentLine,width=3,justify='right')
commentFreq.insert(END, 80)
commentFreq.grid(row=0,column=2)
commentPrctg = Label(commentLine, text='%', anchor=W, width=2)
commentPrctg.grid(row=0,column=3)
commentWait = Entry(commentLine,width=2,justify='right')
commentWait.insert(END, 10)
commentWait.grid(row=0,column=4)
commentSec = Label(commentLine, text='sec', anchor=W, width=4)
commentSec.grid(row=0,column=5)
commentCount = Label(commentLine, text='-', width=4)
commentCount.grid(row=0,column=6)
commentLine.pack(side=TOP)

# Follow line
followLine = Frame(window)
followVar = IntVar()
followCheckBtn = Checkbutton(followLine,variable=followVar)
followCheckBtn.grid(row=0,column=0)
followLbl = Label(followLine, text='Follow', anchor=W, width=8)
followLbl.grid(row=0,column=1)
followFreq = Entry(followLine,width=3,justify='right')
followFreq.insert(END, 10)
followFreq.grid(row=0,column=2)
followPrctg = Label(followLine, text='%', anchor=W, width=2)
followPrctg.grid(row=0,column=3)
followWait = Entry(followLine,width=2,justify='right')
followWait.insert(END, 10)
followWait.grid(row=0,column=4)
followSec = Label(followLine, text='sec', anchor=W, width=4)
followSec.grid(row=0,column=5)
followCount = Label(followLine, text='-', width=4)
followCount.grid(row=0,column=6)
followLine.pack(side=TOP)

# Save line
saveLine = Frame(window)
saveVar = IntVar()
saveCheckBtn = Checkbutton(saveLine,variable=saveVar)
saveCheckBtn.grid(row=0,column=0)
saveLbl = Label(saveLine, text='Save', anchor=W, width=8)
saveLbl.grid(row=0,column=1)
saveFreq = Entry(saveLine,width=3,justify='right')
saveFreq.insert(END, 100)
saveFreq.grid(row=0,column=2)
savePrctg = Label(saveLine, text='%', anchor=W, width=2)
savePrctg.grid(row=0,column=3)
saveWait = Entry(saveLine,width=2,justify='right')
saveWait.insert(END, 1)
saveWait.grid(row=0,column=4)
saveSec = Label(saveLine, text='sec', anchor=W, width=4)
saveSec.grid(row=0,column=5)
saveCount = Label(saveLine, text='-', width=4)
saveCount.grid(row=0,column=6)
saveLine.pack(side=TOP)

# Progress title
progressTile = Frame(window)
spacinglbl00 = Label(progressTile)
spacinglbl00.grid(row=0,column=0)
infoLbl = Label(progressTile, text='-', width=32)
infoLbl.grid(row=1,column=0,columnspan=16)
resetBtn = Button(progressTile,text='Reset',width=4,command=lambda:resetUI())
resetBtn.grid(row=2,column=7)
goBtn = Button(progressTile,text='Go',width=4,command=lambda:main())
goBtn.grid(row=2,column=8)
spacinglblend = Label(progressTile)
spacinglblend.grid(row=3,column=0)
progressTile.pack(side=TOP)


def resetUI():
    infoLbl['text'] = ''
    uiElemList = [hashtagsTotal, likeCount, commentCount, followCount, saveCount]
    for elem in uiElemList:
        elem['text'] = '-'
    uiUserEntries = [userPathIn, hashtagsIn, likeFreq, commentFreq, followFreq, saveFreq, likeWait, commentWait, followWait, saveWait]
    for elem in uiUserEntries:
        elem.delete(0, 'end')
    userPathIn.insert(END, '/Users/***')

def updateUI(reachedPosts, likeCountt, commentCountt, followCountt, savedCountt, elapsedTime):
    hashtagsTotal['text'] = str(reachedPosts)
    likeCount['text'] = str(likeCountt)
    commentCount['text'] = str(commentCountt)
    followCount['text'] = str(followCountt)
    saveCount['text'] = str(savedCountt)
    infoLbl['text'] = 'Finished in ' + str(elapsedTime)

def hashtagsToList():
    hashtagsRaw = hashtagsIn.get()
    hashtagsList = hashtagsRaw.split()
    for i in range(len(hashtagsList)):
        hashtagsList[i] = hashtagsList[i].replace('#', '').lower()
    return hashtagsList

def inputToDigit(inputVar):
    if not inputVar.isdigit():
        return 0
    else:
        return int(inputVar)

def initVarCheck():
    # Checking if all necessary variables have been provided by user
    if not login.get():
        infoLbl['text'] = 'No instagram username given.'
        return False
    if not pwd.get():
        infoLbl['text'] = 'No instagram password given.'
        return False
    if not userPathIn.get():
        infoLbl['text'] = 'No user path given : /Users/*yourname*'
        return False
    elif userPathIn.get() == "/Users/***":
        infoLbl['text'] = 'Specify you user path : /Users/*yourname*'
        return False
    if not hashtagsIn.get():
        infoLbl['text'] = 'No hashtag(s) given.'
        return False

    if likeVar.get() == 1:
        if not likeFreq.get():
            infoLbl['text'] = 'Like frequency percentage missing.'
            return False
        elif not likeFreq.get().isdigit():
            infoLbl['text'] = 'Like frequency is not a number.'
            return False
        elif not likeWait.get():
            infoLbl['text'] = 'Like wait time  missing.'
            return False
        elif not likeWait.get().isdigit():
            infoLbl['text'] = 'Like wait time is not a number.'
            return False
    if commentVar.get() == 1:
        if not commentFreq.get():
            infoLbl['text'] = 'Comment frequency percentage missing.'
            return False
        elif not commentFreq.get().isdigit():
            infoLbl['text'] = 'Comment frequency is not a number.'
            return False
        elif not commentWait.get():
            infoLbl['text'] = 'Comment wait time  missing.'
            return False
        elif not commentWait.get().isdigit():
            infoLbl['text'] = 'Comment wait time is not a number.'
            return False
    if followVar.get() == 1:
        if not followFreq.get():
            infoLbl['text'] = 'Follow frequency percentage missing.'
            return False
        elif not followFreq.get().isdigit():
            infoLbl['text'] = 'Follow frequency is not a number.'
            return False
        elif not followWait.get():
            infoLbl['text'] = 'Follow wait time  missing.'
            return False
        elif not followWait.get().isdigit():
            infoLbl['text'] = 'Follow wait time is not a number.'
            return False
    if saveVar.get() == 1:
        if not saveFreq.get():
            infoLbl['text'] = 'Save frequency percentage missing.'
            return False
        elif not saveFreq.get().isdigit():
            infoLbl['text'] = 'Save frequency is not a number.'
            return False
        elif not saveWait.get():
            infoLbl['text'] = 'Save wait time  missing.'
            return False
        elif not saveWait.get().isdigit():
            infoLbl['text'] = 'Save wait time is not a number.'
            return False
    if likeVar.get() == 0 and commentVar.get() == 0 and followVar.get() == 0 and saveVar.get() == 0:
        infoLbl['text'] = 'Choose to like, comment, follow and/or save.'
        return False
    infoLbl['text'] = ''
    return True

def main():
    if not initVarCheck():
        return False

    startTime = datetime.now()
    retrievedPosts = 0
    reachedPosts = 0
    likeCount = 0
    commentCount = 0
    followCount = 0
    savedCount = 0
    likeRate = inputToDigit(likeFreq.get())/100
    commentRate = inputToDigit(commentFreq.get())/100
    followRate = inputToDigit(followFreq.get())/100
    saveRate = inputToDigit(saveFreq.get())/100
    likeWaitTime = inputToDigit(likeWait.get()) # 3h LIKES 120 per hour max, 300 to 450 per day max (1,5x daily follow)
    commentWaitTime = inputToDigit(commentWait.get()) # 2h COMMENTS 120 per hour max, 250 per day max
    followWaitTime = inputToDigit(followWait.get()) # RULE...h FOLLOW/UNFOLLOW 30 per hour max
    saveWaitTime = inputToDigit(saveWait.get())

    userPath = userPathIn.get()
    filePath = userPath + '/desktop/InstagramBot-master/comments.csv'
    #filePath = str(os.path.join(userPath, '/desktop/comments.csv'))
    #commentsList = open('./comments.csv').readlines()
    commentsList = open(filePath).readlines()
    for i in range(len(commentsList)): commentsList[i] = commentsList[i][:-1]

    givenHashtags = hashtagsToList()

    botUsername = login.get()
    botPassword = pwd.get()

    infoLbl['text'] = 'An error occured.'

    driverPath = userPath + '/desktop/InstagramBot-master/chromedriver'
    bizgo = bot(botUsername, botPassword, driverPath)
    bizgo.login()

    for hashtag in givenHashtags:
        bizgoList = bizgo.retrievePostsFromHashtag(hashtag)
        retrievedPosts += len(bizgoList)

        for i in range(len(bizgoList)):
            print('-- ' + str(i+1) + '/' + str(len(bizgoList)) +' ---- ' + hashtag)
            reachedPosts += 1
            # LIKE
            if likeVar.get() == 1:
                if random.random() < likeRate:
                    if bizgo.likePost(bizgoList[i], likeWaitTime):
                        likeCount += 1
            # COMMENT
            if commentVar.get() == 1:
                if random.random() < commentRate:
                    if bizgo.commentPost(bizgoList[i], commentsList, commentWaitTime):
                        commentCount += 1
                    else:
                        print('No comment │')
            # FOLLOW
            if followVar.get() == 1:
                if random.random() < followRate:
                    if bizgo.followFromPost(bizgoList[i], followWaitTime):
                        followCount += 1
                    else: print('Following  │')
                else: print('No follow  │')
            # SAVE
            if saveVar.get() == 1:
                if random.random() < saveRate:
                    srcLink = bizgo.retrieveSrcFromPost(bizgoList[i])
                    if srcLink:
                        bizgo.saveImage(srcLink, saveWaitTime, userPath)
                        savedCount += 1
                    else: print('No src file│')

    elapsedTime = datetime.now() - startTime
    print('-----------')
    print('')
    print('Hashtags : [' + str(givenHashtags) + ']')
    print('Total  : ' + str(retrievedPosts) + ' -> ' + str(reachedPosts))
    print('')
    print('Likes : ' + str(likeCount) + ' │ ' + str(round(likeCount/reachedPosts, 2)*100) + '%')
    print('Comments : ' + str(commentCount) + ' │ ' + str(round(commentCount/reachedPosts, 2)*100) + '%')
    print('Follow : ' + str(followCount) + ' │ ' + str(round(followCount/reachedPosts, 2)*100) + '%')
    print('Saved : ' + str(savedCount) + ' │ ' + str(round(savedCount/reachedPosts, 2)*100) + '%')
    print('')
    print('Elapsed Time : ' + str(elapsedTime))
    print('Start : ' + str(startTime))
    print('End   : ' + str(datetime.now()))
    bizgo.closeBrowser()
    updateUI(reachedPosts, likeCount, commentCount, followCount, savedCount, elapsedTime)
    return True

window.mainloop()
