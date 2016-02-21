import bottle
import os
import random

taunts = ["YOU'RE the silent killer", 
          "I hate so much about the things that you choose to be", 
          "you're the worst",
          "why are you the way that you are?"]

last_move = None

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
    global our_snake, counter, last_move

    valid_moves = ['east', 'west', 'north', 'south']

    print "**********************"
    print "turn #", str(data["turn"])

    print "last move", last_move

    # ensure snake does not invert & kill itself
    if last_move != None: 
        valid_moves.remove( getOppositeDir(last_move) )

        if len(valid_moves) > 3:
            return {
                'move': 'north',
                'taunt': 'oops'
            }

    # call function to define 'our_snake' Snake object & 'all_live_snakes' Snake object list
    sort_snakes(data["snakes"])

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

    last_move = move

    print "we chose", move
    print "**********************"

    # response
    return {
        'move': move,
        'taunt': getTaunt()
    }

def sort_snakes(snake_list):
    global our_snake
    for snake in snake_list:
        if snake["id"] == snake_id:
            our_snake = snake


def avoidWalls(coords, valid_moves):
    global width, height

    try:    
        if coords[0] >= width-1:
            valid_moves.remove("east")
    except:
        pass
    try:
        if coords[0] == 0:
            valid_moves.remove("west")
    except:
        pass
    try:
        if coords[1] >= height-1:
            valid_moves.remove("south")
    except:
        pass
    try:
        if coords[1] == 0:
            valid_moves.remove("north") 
    except:
        pass

    return valid_moves

## input: List of Snakes and the coordinates of our snakes head and list of possible directions (in that order)
def avoidSnakes(snakeList, ourHead, directions):
    
    for snake in snakeList:
        for coords in snake["coords"]:
            ##same x coordinates and they are right above/below us
            try:
                if ourHead[0] == coords[0] and ourHead[1] == coords[1]+1:
                    directions.remove("north")
            except:
                pass
            try:
                if ourHead[0] == coords[0] and ourHead[1] == coords[1]-1:
                    directions.remove("south")
            except:
                pass
            try:
                if ourHead[1] == coords[1] and ourHead[0] == coords[0]-1:
                    directions.remove("east")
            except:
                pass
            try:
                if ourHead[1] == coords[0] and ourHead[0] == coords[0]+1:
                    directions.remove("west")
            except:
                pass
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
