import bottle
import os
import random

taunts = ["YOU'RE the silent killer", 
          "I hate so much about the things that you choose to be", 
          "you're the worst",
          "why are you the way that you are?"]

all_moves = ['east', 'north', 'west', 'south']

last_move = None

counter = 0    # used in getTaunt()

# game board dim defined in index()
height = -1     
width = -1

our_snake = None    # init in sort_snakes

enemies = []    # list of live enemy Snake Objects

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
        'color': '#00ffff',
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

# finds our snake & composes list of live enemies
def sort_snakes(snake_list):
    global our_snake, snake_id

    # find our snake & keep list of all live enemies
    for snake in snake_list:
        if snake["id"] == snake_id:
            our_snake = snake
        # ignore dead snakes (remove from list)
        elif snake["status"] == 'alive':
            enemies.append(snake)


@bottle.post('/move')
def move():
    global our_snake, all_moves
    move = None

    # get data
    data = bottle.request.json 

    # call function to define 'our_snake' Snake object & 'enemies' Snake object list
    sort_snakes(data["snakes"])

    # find pos of our snake's head
    our_snake_head = our_snake['coords'][0]

    # avoid moving 
    while True: 
        move = random.choice(all_moves)
        # do not invert on oneself
        if last_move == null or move == getOppositeDir(last_move):
            break
    

    # response
    return {
        'move': move,
        'taunt': getTaunt()
    }

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
