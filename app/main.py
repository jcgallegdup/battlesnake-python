import bottle
import os
import random

taunts = ["YOU'RE the silent killer", 
          "I hate so much about the things that you choose to be", 
          "you're the worst",
          "why are you the way that you are?"]

counter = 0    # used in getTaunt()

# game board dim defined in index()
height = -1     
width = -1

our_snake = None    # init in sort_snakes

snake_id = "05d4b1a6-ce15-4298-abc1-2be9718d9c20"   # to find our snake from snake list

snake_name = "onomatopoeia"


def getTaunt():
    global taunts, counter
    counter += 1
    return (taunts[counter%len(taunts)])


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # response
    return {
        'color': '#ffffff',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    global height, width

    height = data["height"]
    width = data["width"]

    # response
    return {
        'taunt': getTaunt()
    }


@bottle.post('/move')
def move():
    # get data
    data = bottle.request.json
    # indicate scope of vars
    global our_snake, counter

    valid_moves = ['east', 'west', 'north', 'south']

    print "**********************"
    print "turn #", str(data["turn"])

    # call function to define 'our_snake' Snake object & 'all_live_snakes' Snake object list
    sort_snakes(data["snakes"])

    # prevent inverting on itself
    last_move = findLastMove(our_snake['coords'])

    print "last choice:", last_move

    if last_move != None:
        valid_moves.remove(last_move)

    # find pos of our snake's head
    our_snake_head = our_snake['coords'][0]

    print "initial list ", valid_moves


    # returns a potentially altered list of valid moves
    valid_moves = avoidWalls(our_snake_head, valid_moves)


    print "after avoid walls ", valid_moves

    # returns a potentially altered list of valid moves
    valid_moves = avoidSnakes(data["snakes"], our_snake_head, valid_moves)

    print "after avoid snakes ", valid_moves

    # selec random move out of valid
    move = random.choice( valid_moves )

    print "we chose", move
    print "**********************"

    # response
    return {
        'move': move,
        'taunt': getTaunt()
    }

def findLastMove(coordslist):

    if coordslist[1][0] > coordslist[0][0]:
        return "west"
    if coordslist[1][0] < coordslist[0][0]:
        return "east"
    if coordslist[1][1] > coordslist[0][1]:
        return "north"
    if coordslist[1][1] < coordslist[0][1]: 
        return "south"

def sort_snakes(snake_list):
    global our_snake
    for snake in snake_list:
        if snake["id"] == snake_id:
            our_snake = snake


def avoidWalls(coords, valid_moves):
    global width, height
 
    if coords[0] >= width-1 and "east" in valid_moves:
        valid_moves.remove("east")
    if coords[0] == 0 and "west" in valid_moves:
        valid_moves.remove("west")
    if coords[1] >= height-1 and "south" in valid_moves:
        valid_moves.remove("south")
    if coords[1] == 0 and "north" in valid_moves:
        valid_moves.remove("north") 

    return valid_moves

## input: List of Snakes and the coordinates of our snakes head and list of possible directions (in that order)
def avoidSnakes(snakeList, ourHead, directions):
    
    for snake in snakeList:
        for coords in snake["coords"]:
            ##same x coordinates and they are right above/below us
            if ourHead[0] == coords[0] and ourHead[1] == coords[1]+1 and "north" in directions:
                directions.remove("north")
            if ourHead[0] == coords[0] and ourHead[1] == coords[1]-1 and "south" in directions:
                directions.remove("south")
            if ourHead[1] == coords[1] and ourHead[0] == coords[0]-1 and "east" in directions:
                directions.remove("east")
            if ourHead[1] == coords[0] and ourHead[0] == coords[0]+1 and "west" in directions:
                directions.remove("west")
    return directions


def getOppositeDir(str):
    if str == 'west':
        return 'east'
    elif str == 'east':
        return 'west'
    elif str == 'south':
        return 'north'
    else:
        return 'south'


@bottle.post('/end')
def end():
    data = bottle.request.json

    # game over
    return {}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
