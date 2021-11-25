from aiohttp import web
from utils.utils import *
from features import *
import os
import asyncio

import aiohttp_security 
import aiohttp_session

DATABASE = './db/aluraflix.db'

async def index(request):
    '''Basic web page just for reasons'''
    return(web.Response(text='Imundisse disse'))


def makeapp():
    
    middleware= ''

    app =web.Application()

    app.router.add_route(method='GET',path='/',handler=index)
    
    register_url(app,[Videos.routes,Videos_id.routes,Categorias.routes])
    #if 'aluraflix.db' not in os.listdir('./db'):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database(DATABASE))

    return(app)

if __name__ =='__main__':
    
    web.run_app(makeapp(),host='localhost')