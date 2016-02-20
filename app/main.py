import bottle
import os

taunts = ["YOU'RE the silent killer", 
          "I hate so much about the things that you choose to be", 
          "you're the worst",
          "why are you the way that you are?"]

counter = 0

snake_id = "05d4b1a6-ce15-4298-abc1-2be9718d9c20"
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

    # TODO: Do things with data

    # response
    return {
        'taunt': getTaunt()
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data

    # response
    return {
        'move': 'north',
        'taunt': getTaunt()
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # game over
    return {}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
