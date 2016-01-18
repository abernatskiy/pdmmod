import svgwrite
import sys
from routes import *
sys.path.append(routeHP)
import HPlibraryReader

###DATA###
'''
turn is one of:
    * 'U' - line goes up
    * 'R' - line gose to the right
    * 'L' - line goes to the left
    * 'D' - line goes down
    ex.: t = 'U'

turns is a string compose of turn elements
    ex: ts = 'URD'

drawing is a svgwrite.Drawing object
    ex: dwg = svgwrite.Drawing('test.svg', size=(100,100))

startPoint is a tuple:
    (x-coord,y-coord) -- represents beginning of the line
'''

def drawTurn(drawing,turn,startPoint,length=30):
    ''' 
    adds a line of fixed length in a direction give by "turn" to the drawing
    
    '''
    if turn=='U':
        endPoint = (startPoint[0],startPoint[1]-length)
    elif turn=='R':
        endPoint = (startPoint[0]+length,startPoint[1])
    elif turn=='L':
        endPoint = (startPoint[0]-length,startPoint[1])
    elif turn=='D':
        endPoint = (startPoint[0],startPoint[1]+length)
    else:
        raise ValueError('turn = '+turn+', but turns (directions) can be only "U","R","L","D"')
    drawing.add(
        drawing.line(startPoint,endPoint,
                    stroke=svgwrite.rgb(0, 0, 0, '%'),stroke_width=10
                    )
        )
    return endPoint


def drawBackbone(drawing,turns,startPoint,length=30):
    '''given a sequence of turns draws a pathe
    '''
    currStart = startPoint
    for turn in turns:
        endPoint = drawTurn(drawing,turn,currStart,length)
        currStart = endPoint
    return endPoint

def drawBalls(drawing,turns,sequence,startPoint,length=30):
    def getColor(letter):
        if letter == 'H':
            return 'red'
        elif letter == 'P':
            return 'blue'
        else:
            raise ValueError('letter is '+letter+', but letters can be only "P" and "H"')
    currStart = startPoint
    for i in range(len(turns)):
        turn = turns[i]
        letter = sequence[i]
        endPoint = drawTurn(drawing,turn,currStart,length)
        dwg.add(
            dwg.circle(
                center=currStart, 
                r=int(length/2-4),
                stroke='black',
                fill=getColor(letter)
                )
            )
        
        currStart = endPoint
    dwg.add(
        dwg.circle(
            center=currStart, 
            r=int(length/2-4),
            stroke='black',
            fill=getColor(sequence[-1])
            )
        )
    return endPoint

def getConfiguration(sequence):
    configuration = None
    chainDict = HPlibraryReader.HPlengthReader(len(sequence))
    for (conf, seqList) in chainDict.items():
        seqList = [theTuple[0] for theTuple in seqList]
        if sequence in seqList:
            configuration = conf
            return configuration
    if configuration == None:
        if not chainDict == {}:
            print(chainDict.keys())
            raise ValueError('configuration not found')
        else:
            raise FileNotFoundError('HP library reader didn\'t find sequece files')

def drawLinearChain(drawing,sequence,startPoint,length=30):
    N=len(sequence)
    turns = 'R'*(N-1)
    drawBalls(drawing,turns,sequence,startPoint,length)
    return None

dwg = svgwrite.Drawing('/tmp/test.svg', size=(1000,1000))

s1 = 'HHHPPPHHHPPHPH'
drawBalls(dwg,getConfiguration(s1),s1,(0,100))
drawLinearChain(dwg,s1,(0,200))

s2 = 'HHHHHHPPHHPHPH'
drawBalls(dwg,getConfiguration(s2),s2,(0,400))
drawLinearChain(dwg,s2,(0,500))

s3 = 'HPPHPHPHHHHPHH'
drawBalls(dwg,getConfiguration(s3),s3,(0,600))
drawLinearChain(dwg,s3,(0,700))

s4 = 'HHHPPHPPPHHPHPPH'
drawBalls(dwg,getConfiguration(s4),s4,(0,900))
drawLinearChain(dwg,s4,(0,1000))

s5 = 'HHHPPHPPPHPPHHHH'
drawBalls(dwg,getConfiguration(s5),s5,(0,1100))
drawLinearChain(dwg,s5,(0,1200))

dwg.save()

