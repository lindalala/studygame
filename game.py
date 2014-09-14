from Tkinter import *
import random, copy
import main, dictionaries

                for q in Question.questions:
                    q.weight = 0
                    q.setWeight(1)
                self.flashY = {'char': 'charY'}
                self.flashG = {'char': 'charG'}
                self.flashB = {'char': 'charB'}

class Question(object):
    # This class keeps track of questions and their weights
    # so it's easier to generate the next question based on
    # whether user got question right or wrong before
    questions = []
    totalWeight = 0
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.rightCount = 0
        self.wrongCount = 0
        self.weight = 0
        # weights each start out as 1
        self.setWeight(1)
        Question.questions.append(self)

    def setWeight(self, n):
        Question.totalWeight += n
        self.weight += n

    def __str__(self):
        # override str function so stuff works properly
        return "%s" % (self.question)

class Game(object):
    # main class that runs game basically
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.flashY = {'char': 'charY'}
        self.flashG = {'char': 'charG'}
        self.flashB = {'char': 'charB'}
        self.currentDict = {}
        # go Button
        goButton = Button(self.canvas, compound = CENTER, bg="#deff00", bd = 3,                    text = "     C'mon Let's Play!         ", cursor = 'star',
                    font = "Helvetica 15",
                    overrelief=RIDGE, command=self.goButtonPressed)
        self.goButton = goButton
        self.getKeys()

    def timerFired(self):
        if ((self.isGameOver == False) and (self.isPaused == False)):
            # background image movement
            self.backLeft -= 50
            self.backLeft2 -= 50
            # if any of the backgrounds are totally to the left of canvas,
            # redraw it to the right of the canvas so it looks like the
            # background is neverending.
            if (self.backLeft < -2000):
                self.backLeft = 2000
            if (self.backLeft2 < -2000):
                self.backLeft2 = 2000
            # move lasers
            self.moveLasers()
            # if laser hit character, do stuff
            if 80 < self.laserLeft <= 100:
                self.toDieorNottoDie(self.laser1)
                self.laserCount += 1
            if 80 < self.laserLeft2 <= 100:
                self.toDieorNottoDie(self.laser2)
                self.laserCount +=1
            if 80 < self.laserLeft3 <= 100:
                self.toDieorNottoDie(self.laser3, p=1)
                self.laserCount +=1
            # char bounce
            if self.up == self.canvas.height-30:
                self.up = self.canvas.height-20
            else: self.up = self.canvas.height-30
            self.redrawAll()
    
    def moveLasers(self):
        # redraw lasers to the left
        self.laserLeft -= 50
        self.laserLeft2 -= 50
        # if laser passes and cards run out, or if laser passes and level
        # 20 is reached, game ends, user wins.
        if ((Question.totalWeight == 0 or self.curLevel == 20) and
            (self.laserLeft <= -100 or self.laserLeft2 <= -100 or
             self.laserLeft3 <= -100)):
            self.youWin()
        # generate new laser when laser moves to left of canvas
        if (self.laserLeft < -100):
            self.laserLeft = 2900
            self.laser1 = self.getRandomLaser()
            if self.curChar == 'charD' and self.lives > 0:
                # revive character if life is used
                self.curChar = self.prevChar
        if (self.laserLeft2 < -100):
            self.laserLeft2 = 2900
            self.laser2 = self.getRandomLaser()
            if self.curChar == 'charD' and self.lives > 0:
                # revive character if life is used
                self.curChar = self.prevChar
        if (self.curLevel==10 and
        (self.laserLeft3 == 500 + self.laserLeft)):
            # makes sure 3rd laser placement isn't too close to lasers
            # 1 or 2
            self.thirdLaser = True
        # 3rd laser is only in action if level is greater than 10
        # and it's at least 500px from other lasers
        if self.curLevel >= 10 and self.thirdLaser == True:
            self.laserLeft3 -= 50
            if (self.laserLeft3 < -100):
                while True:
                    randLeft = random.randint(2400, 3300)
                    if (abs(randLeft- self.laserLeft)>500 and
                       abs(randLeft - self.laserLeft2)>500):
                        self.laserLeft3 = randLeft
                        break
                self.laser3 = self.getRandomLaser()
                if self.curChar == 'charD' and self.lives > 0:
                    # revive character if life is used
                    self.curChar = self.prevChar

    def mousePressed(self,event):
        if self.isGameOver == False:
            PbuttonLeft = 913; PbuttonTop = 619
            PbuttonRight = 1002; PbuttonBottom = 700
            if ((event.x >= PbuttonLeft and event.x<= PbuttonRight) and
                (event.y >= PbuttonTop and event.y <= PbuttonBottom)):
                # Pause Pressed
                if self.isPaused == False:
                    self.isPaused = True
                else: self.isPaused = False
                self.redrawAll()
        if self.isGameOver==True or self.isPaused == True:
            RbuttonLeft = 425; RbuttonTop = 329
            RbuttonRight = 577; RbuttonBottom = 375
            MbuttonLeft = 425; MbuttonTop = 403
            MbuttonRight = 577; MbuttonBottom = 450
            if ((event.x >= RbuttonLeft and event.x<= RbuttonRight) and
                (event.y >= RbuttonTop and event.y <= RbuttonBottom)):
                # Restart pressed
                self.__init__(self.root,self.canvas)
                self.getCurrentDictionary()
                self.init()
            if ((event.x >= MbuttonLeft and event.x<= MbuttonRight) and
                (event.y >= MbuttonTop and event.y <= MbuttonBottom)):
                # Main Menu pressed
                self.buttonMPressed()

    def keyPressed(self,event):
        if self.isGameOver == False == self.isPaused:
            if (event.keysym in self.Y):
                self.flashAnswered(self.flashY, event.keysym)
            if (event.keysym in self.G):
                self.flashAnswered(self.flashG, event.keysym)
            if (event.keysym in self.B):
                if self.curLevel >= 4:
                    self.flashAnswered(self.flashB, event.keysym)
            # debug purposes
            if (event.keysym =='1'):
                self.score += 10

    def buttonMPressed(self):
        # clear stuff
        self.flashY.clear()
        self.flashG.clear()
        self.flashB.clear()
        Question.questions = []
        Question.totalWeight = 0
        self.flashcards.clear()
        # return to main menu
        self.canvas.current = self.canvas.main
        self.canvas.current.init(self.root, self.canvas)

    def getKeys(self):
        # set keysym values
        self.Y = ['a','s','d','f']; self.G = ['h','j','k','l'];
        self.B = ['q','w','e','r']
        self.flashB['0'] = 'q'; self.flashB['1'] = 'w';
        self.flashB['2'] = 'e'; self.flashB['3'] = 'r';
        self.flashY['0'] = 'a'; self.flashY['1'] = 's';
        self.flashY['2'] = 'd'; self.flashY['3'] = 'f';
        self.flashG['0'] = 'h'; self.flashG['1'] = 'j';
        self.flashG['2'] = 'k'; self.flashG['3'] = 'l'

    def flashAnswered(self, flash, key):
        # set currentFlash that is answered
        self.curFlash = flash
        # answer key is stored in flash in function setKeyValues()
        if flash[str(flash['index'])] == key:
            # answer is correct, so turn into flashcard Color
            self.curChar = flash['char']
            # increase some counts
            self.numRight += 1
            self.score+=10
            self.correctAnswer = True
            # reduce question weight
            for q in Question.questions:
                if str(q) == flash['question']:
                    if q.weight != 0: q.setWeight(-1)
                    break
            self.getNewQuestions(flash)
        else:
            # answer is wrong
            self.correctAnswer = False
            self.totalWrong += 1
            self.score -= 10
            # increase question weight
            for q in Question.questions:
                if str(q) == flash['question']:
                    q.setWeight(1)
                    break
        self.redrawAll()
    
    def implementFinalAnswer(self):
        ''' This function generates new flashcards when laser is close
        to character and answer is still wrong'''
        if ((200 < self.laserLeft < 300) or (200 < self.laserLeft2 < 300)  or
            (200 < self.laserLeft3 < 300)):
            # character kinda close to laser, so final answer is counted.
            # generate new flashcard
            if self.curFlash!= None: self.getNewQuestions(self.curFlash)

    def getRandomLaser(self):
        if self.curLevel < 4:
            # only 2 lasers are in action, so we generate 2 numbers
            randInt = random.randint(0,1)
        else:
            # 3 lasers in action yo
            randInt = random.randint(0,2)
        # makes sure each flashcard has a question to display
        if randInt == 0 and self.flashY['question'] != '':
            return "lasY"
        elif randInt == 1 and self.flashG['question'] != '':
            return "lasG"
        elif randInt == 2 and self.flashB['question'] != '':
            return "lasB"
        # if not, try again. Recursion!
        else:
            return self.getRandomLaser()

    def getQuestion(self):
        '''Generates a question so questions answered wrong havea higher
        chance of showing up'''
        # Each question has a weight. We change it to probability by taking
        # the weight and dividing by total sum.
        # First generate float between 0 and 1
        prob = random.random()
        cutoff = 0
        # Then loop through each question, and calculate the next cutoff
        for q in Question.questions:
            cutoff += (float(q.weight) / Question.totalWeight)
            # if we don't pass the next cutoff, the q was chosen as answer
            if prob <= cutoff:
                # need to str it because it's a Question object
                return str(q)

    def getNewQuestions(self, flash):
        '''gets Question and Answer of new Flashcard'''
        if Question.totalWeight != 0:
            # first get question using algorithm
            question = self.getQuestion()
            flash['question'] = question
            flash['answer'] = self.flashcards[question]
            # then get answer choices randomly
            answerCount = 1
            answers = []
            while True:
                randomAnswer = random.choice(self.possibleAnswers)
                # make sure you don't generate the right answer randomly
                # otherwise you may end up with 2 of the same answer choice
                if ((randomAnswer not in answers) and
                (randomAnswer != flash['answer'])):
                    answers.append(randomAnswer)
                    answerCount+=1
                if self.curLevel < 4:
                    # only 3 answer choices
                    if answerCount == 3:
                        randIndex = random.randint(0,2)
                        break
                else:
                    # there are 4 answer choices
                    if answerCount == 4:
                        randIndex = random.randint(0,3)
                        break
            # add right answer at randomly generated index
            answers.insert(randIndex, flash['answer'])
            # store these so we can know which answer is correct later
            flash['index'] = randIndex
            flash['allAnswers'] = answers
        else:
            # total Weight is 0 so no more questions can be generated
            flash['question'] = ""; flash['answer'] = None

    def drawCards(self):
        if self.curLevel < 4:
            # draw 2 cards
            self.canvas.create_image(75, 10, anchor = NW,
                                    image=self.canvas.data[self.card1])
            self.canvas.create_image(570, 10, anchor = NW,
                                    image=self.canvas.data[self.card2])
            # draw questions (yellow, then green)
            for flash in [self.flashY, self. flashG]:
                if flash == self.flashY: left = 75 + 20
                if flash == self.flashG: left = 575 + 20
                # width is restrained so text doesn't draw outside of flashcard
                self.canvas.create_text(left, 40, anchor = NW, width = 270,
                        text = flash['question'], font = 'Helvetica 20 bold')
                verticalShift = 0
                # draw answers
                if flash['answer'] != None:
                    for answer in flash['allAnswers']:
                        if verticalShift ==0: key = flash['0']
                        if verticalShift ==1: key = flash['1']
                        if verticalShift ==2: key = flash['2']
                        # draw key value, followed by answer
                        self.canvas.create_text(left, 97+verticalShift*50,
                            anchor = NW, text = '[' + key + ']  ',
                            font = 'Arial 20 bold')
                        self.canvas.create_text(left + 30, 100+verticalShift*50,
                                anchor = NW, width = 270,
                                text = answer, font = 'Helvatica 15 bold')
                        # increase verticalShift so answers aren't drawn on top of
                        # each other
                        verticalShift +=1
        else:
            # 3 draw cards of smaller size
            self.canvas.create_image(20, 10, anchor = NW,
                                    image=self.canvas.data[self.card1])
            self.canvas.create_image(self.canvas.width/2, 10, anchor = N,
                                    image=self.canvas.data[self.card2])
            self.canvas.create_image(self.canvas.width - 20, 10, anchor = NE,
                                    image=self.canvas.data[self.card3])
            # draw questions
            for flash in [self.flashY, self. flashG, self.flashB]:
                if flash == self.flashY: left = 25 + 30
                if flash == self.flashG: left = 350 + 30
                if flash == self.flashB: left = 680 + 30
                self.canvas.create_text(left, 40, anchor = NW, width = 250,
                            text = flash['question'], font = 'Helvetica 20 bold')
                verticalShift = 0
                if flash['answer'] != None:
                    for answer in flash['allAnswers']:
                        if verticalShift ==0: key = flash['0']
                        if verticalShift ==1: key = flash['1']
                        if verticalShift ==2: key = flash['2']
                        if verticalShift ==3: key = flash['3']
                        self.canvas.create_text(left, 97+verticalShift*50,
                                    anchor = NW,
                                    text = key, font = 'Arial 20 bold')
                        self.canvas.create_text(left + 25, 100+verticalShift*50,
                                    anchor = NW, width = 250,
                                    text = answer, font = 'Helvatica 15 bold')
                        # set text width so cards are drawn in flashcard
                        verticalShift +=1

    def toDieorNottoDie(self, laser):
        '''Decides what to do after character hits a laser'''
        if str(laser)[-1] == str(self.curChar)[-1]:
            # same color
            # get to live
            self.laserCount += 1
            self.score += 10
        else:
            # :( sad times
            self.prevChar = self.curChar
            self.curChar = 'charD'
            self.lives -=1
            self.score -= 10
            if self.lives == 0:
                # :(( even sadder times
                    self.isGameOver = True
                    # char dies
                    self.curChar = 'charD'
        self.redrawAll()

    def youWin(self):
        '''User Wins yo'''
        self.win = True
        self.isGameOver = True

    def gameOver(self):
        ''' Draws the Game Over Screen '''
        # Dude check out this self-made stipple!
        # Stippling doesn't work on a Mac, so I made my own. It's a checkerboard
        # of white tiles! Sweet sauce.
        sideLength = 4
        for x in xrange(sideLength,self.canvas.width + sideLength,2*sideLength):
            for y in xrange(sideLength,
                            self.canvas.height + sideLength,2*sideLength):
                if (x+y) %2 == 0:
                    self.canvas.create_rectangle(x, y, x+4, y+4,
                                        fill="white", width = 0)
        for x in xrange(2*sideLength,self.canvas.width + sideLength,2*sideLength):
            for y in xrange(2*sideLength,
                            self.canvas.height + sideLength,2*sideLength):
                if (x+y) %2 == 0:
                    self.canvas.create_rectangle(x, y, x+4, y+4,
                                        fill="white", width = 0)
        # draw Game Over or You Win depending on situation
        if self.win == False:
            self.canvas.create_text(self.canvas.width/2, self.canvas.height/3,
            fill = "red", text = "GAME OVER", font = 'Helvetica 100 bold')
        else:
            self.canvas.create_text(self.canvas.width/2, self.canvas.height/3,
            fill = "red", text = "YOU WIN!", font = 'Helvetica 100 bold')
        # Restart button
        self.canvas.create_image(self.canvas.width/2, self.canvas.height/2,
                        anchor = None, image=self.canvas.data["Mbutton"])
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2,
                        text="Restart", font = "Helvetica 20 bold")
        # Main Menu button
        self.canvas.create_image(self.canvas.width/2, self.canvas.height/2 + 75,
                        anchor = None, image=self.canvas.data["Mbutton"])
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 75,
                        text="Main Menu", font = "Helvetica 20 bold")
        # Stats
        self.canvas.create_rectangle(404,480,597,605, fill='white', width= 0)
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 150,
                        text="Score: "+str(self.score), font = "Helvetica 20 bold")
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 175,
                        text="Level: "+str(self.curLevel), font = "Helvetica 20 bold")
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 200,
        text="Lasers Passed Safely: "+str(self.laserCount), font = "Helvetica 15 bold")
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 220,
        text="Total Wrong Answers: "+str(self.totalWrong), font = "Helvetica 15 bold")
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 240,
        text="Total Right Answers: "+str(self.numRight), font = "Helvetica 15 bold")

    def drawPausedScreen(self):
        # self-made stipple, which is awesome!
        sideLength = 4
        for x in xrange(sideLength,self.canvas.width + sideLength,2*sideLength):
            for y in xrange(sideLength,
                            self.canvas.height + sideLength,2*sideLength):
                if (x+y) %2 == 0:
                    self.canvas.create_rectangle(x, y, x+4, y+4,
                                        fill="white", width = 0)
        for x in xrange(2*sideLength,self.canvas.width + sideLength,2*sideLength):
            for y in xrange(2*sideLength,
                            self.canvas.height + sideLength,2*sideLength):
                if (x+y) %2 == 0:
                    self.canvas.create_rectangle(x, y, x+4, y+4,
                                        fill="white", width = 0)
        # PAUSED text
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/3,
                fill='red', text = "PAUSED", font = 'Helvetica 100 bold')
        # Restart button
        self.canvas.create_image(self.canvas.width/2, self.canvas.height/2,
                        anchor = None, image=self.canvas.data["Mbutton"])
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2,
                        text="Restart", font = "Helvetica 20 bold")
        # Main Menu button
        self.canvas.create_image(self.canvas.width/2, self.canvas.height/2 + 75,
                        anchor = None, image=self.canvas.data["Mbutton"])
        self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 + 75,
                        text="Main Menu", font = "Helvetica 20 bold")
    
    def implementLevelChanges(self):
        ''' Calculates current Level and implements Level Changes '''
        # Level depends on score. If a score passes a certain cutoff, level
        # will increase.
        # The cutoff depends on the number of questions user gets right, so
        # the more questions user gets right, the harder it is to level up.
        # There is a cap on the cutoff number, otherwise it would be much too
        # difficult to level up if over 20 questions are answered correctly.
        if self.score >= (self.curLevel+1)*min(self.numRight+20,40):
            self.curLevel+=1
        if self.curLevel >= 4:
            # 3 colors are now used
            self.card1 = 'flashY'
            self.card2 = 'flashG'
            self.card3 = 'flashB'
        if self.curLevel>10:
            # faster game
            self.canvas.timerDelay = 200
        if self.curLevel>15:
            # even faster game
            self.canvas.timerDelay = 150

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.implementFinalAnswer()
        self.implementLevelChanges()
        # draw 2 backgroundsnext to each other
        self.canvas.create_image(self.backLeft, 0, anchor = NW,
                                 image=self.canvas.data["gameBackground"])
        self.canvas.create_image(self.backLeft2, 0, anchor = NW,
                                 image=self.canvas.data["gameBackground"])
        # draw character
        self.canvas.create_image(100, self.up, anchor = S,
                                 image=self.canvas.data[self.curChar])
        # draw lasers
        self.canvas.create_image(self.laserLeft, 0, anchor = NW,
                                 image=self.canvas.data[self.laser1])
        self.canvas.create_image(self.laserLeft2, 0, anchor = NW,
                                 image=self.canvas.data[self.laser2])
        if self.curLevel >= 10:
            # draw 3rd laser
            self.canvas.create_image(self.laserLeft3, 0, anchor = NW,
                                 image=self.canvas.data[self.laser3])
        # draw flashcards
        self.drawCards()
        # draw score and lives
        for i in xrange(self.lives):
            self.canvas.create_image(0 + i*30, self.canvas.height,
                        anchor = SW, image=self.canvas.data["life"])
        self.canvas.create_text(0, self.canvas.height, anchor = SW,
                           text = "Score: " + str(self.score) + "Level: "
                           + str(self.curLevel), font = 'Helvetica 20 bold')
        # draw check and x depending on whether answer was right or not
        if self.correctAnswer == True:
             self.canvas.create_image(self.canvas.width, 0,
                        anchor = NE, image=self.canvas.data["check"])
        if self.correctAnswer == False:
             self.canvas.create_image(self.canvas.width, 0,
                        anchor = NE, image=self.canvas.data["x"])
        # draw other things depending on whether or not game is paused
        if self.isPaused == True:
            # pause screen
            self.drawPausedScreen()
            # play button
            self.canvas.create_image(self.canvas.width, self.canvas.height,
                        anchor = SE, image=self.canvas.data["playbutton"])
        if self.isPaused == False:
            # pause button
            self.canvas.create_image(self.canvas.width, self.canvas.height,
                        anchor = SE, image=self.canvas.data["pausebutton"])
        # if score is negative, game over
        if self.score < 0:
            self.isGameOver = True
            # char dies
            self.curChar = 'charD'
        # draw game over screen if it's game over
        if self.isGameOver == True:
            self.gameOver()
    
    # below here is instruction screen
    def instruction(self):
        ''' Displays instruction Screen '''
        self.canvas.delete(ALL)
        self.isGameOver = True
        self.canvas.create_image(0, 0, anchor = NW,
                                 image=self.canvas.data["playBackground"])
        # text
        self.canvas.create_text(self.canvas.width/2,200,text=
            "Pass through lasers without getting burned! You get 5 lives.",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,240, text=
            "To pass through lasers safely, you must be the same color as the laser.",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,280, text=
            "Change colors by answering flashcard questions on your destination color.",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,320,text=
            "Your lives, levels, and score count are on the bottom right.",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,360,text=
            "Check if your answer was right by looking at the symbol on the top right.",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,400,text=
            "You get +10 points for each right answer, -10 points for burning in a laser",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,440,text=
            "The pause button is on the bottom right.",
            font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,490, text=
                        "Choose the flashcards you want to play with!",
                        font = 'Helvetica 20')
        # draw Radio Button
        self.v = StringVar()
        buttonOptions = []
        for flashcards in dictionaries.dictList:
            buttonOptions += [(flashcards,'dictionaries.'+flashcards)]
        self.i = 0
        self.radio = [0,1,2,3,4,5,6]
        for (txt, val) in buttonOptions:
            self.radio[self.i] = Radiobutton(self.canvas, text=txt, indicatoron = True,
                                    relief= SUNKEN, width = 20, padx = 20,
                    variable=self.v, value=val, bg="#deff00", bd = 10)
            self.i +=1
        self.v.set('dictionaries.Sample')  # initializing the choice
        for index in xrange(self.i):
            self.canvas.create_window(self.canvas.width/2, self.canvas.height*3/4 + index*20,
                                    window=self.radio[index])
        # go Button
        window = self.goButton
        self.canvas.create_window(self.canvas.width/2, 4 + self.canvas.height*3/4 + self.i*20,
                                  window=window)

    def goButtonPressed(self):
        global canvas # for button!
        self.curLevel = 0
        self.getCurrentDictionary()
        # destroy radio buttons >:[
        for i in xrange(self.i):
            self.radio[i].destroy()
        self.init()

    def getCurrentDictionary(self):
        '''Finds current dictionary and finds possible Questions and Answers'''
        self.currentDict = eval(self.v.get())
        self.flashcards = copy.deepcopy(self.currentDict)
        self.possibleAnswers =self.flashcards.values()
        for question, answer in self.currentDict.iteritems():
            # make Question objects
            Question(question, answer)
        self.getNewQuestions(self.flashY)
        self.getNewQuestions(self.flashG)
        self.getNewQuestions(self.flashB)

    def init(self):
        #initial image values
        self.backLeft = 0
        self.backLeft2 = 2000
        self.laserLeft = 1100
        self.laserLeft2 = 2600
        self.laserLeft3 = 2500
        self.thirdLaser = False
        self.curLevel = 1
        self.curChar = 'charY'
        self.cardLeft = 0
        self.up = self.canvas.height-30
        # generate 2 initial random cards
        self.card1= 'flashY0'
        self.card2= 'flashG0'
        self.card3 = 'flashB'
        self.laser1=self.getRandomLaser()
        self.laser2=self.getRandomLaser()
        self.laser3=self.getRandomLaser()
        # other crap
        self.score = 10
        self.isGameOver=False
        self.wrongCount = 0
        self.numRight = 0
        self.totalWrong = 0
        self.lives = 5
        self.laserCount = 0
        self.canvas.timerDelay = 250
        self.correctAnswer = None
        self.isPaused = False
        self.win = False
        self.curFlash = None
        self.redrawAll()