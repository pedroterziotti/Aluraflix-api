from aiohttp import web
import aiosqlite


DATABASE = './db/aluraflix'

def register_url(app:web.Application, routers:list):
    '''Registra as urs de uma classe em um app'''

    for router in routers:
        app.add_routes(router)


async def create_database(DATABASE):
    '''Cria a Base de dados'''

    async with aiosqlite.connect(DATABASE) as db:
        with open('./db/create_database.sql') as file:
            await db.executescript(file.read())

async def verify(video:dict):
    '''Método para verificar e validar videos com o modelo da base de dados'''
    return(True)
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('''SELECT 0 FROM videos''') as test:
            db.row_factory = aiosqlite.Row
            async with db.execute('''SELECT * FROM videos''') as cursor:
                async for row in cursor:
                    new=dict(row)
            if new.keys() != video.keys():
                return False
            #Checagem de id único foi configirado na base de dados com 'CREATE UNIQUE INDEX id ON videos (id)' em sql
            elif type(video['id']) != int:
                return False
            elif type(video['titulo']) != str:
                return False
            elif type(video['descricao']) != str:
                return False            
            #elif (await aiohttp.request('get',url=video['url'])).status != 200:
            #    return False
            else: return True