from aiohttp import web
import aiosqlite
from utils.utils import verify



DATABASE = './db/aluraflix.db'


class Videos:
    '''Classe de Handlers das urls /videos'''

    routes = web.RouteTableDef()

    @routes.get('/videos')
    async def get_all_videos(request):
        '''End point que retorna todos os videos'''
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('''SELECT * FROM videos''') as cursor:
                response={}
                async for row in cursor:
                    new=dict(row)
                    response[new['id']]= new

            return(web.json_response(response))
            
   
    @routes.post('/videos')
    async def post_new_video(request):
        ''' Insert a new video in the table, id imposto no backend  '''
        video =  await request.json()
        async with aiosqlite.connect(DATABASE) as db:
            if await verify(video):    
                await db.execute(f'''INSERT INTO videos {tuple(video.keys())} VALUES {tuple(video.values())}''')
                await db.commit()
                return(web.Response(status=200))
            else:
                return(web.Response(status=400))

    @routes.patch('/videos')
    async def patch_video(request):
        '''Endpoint de edição da base de dados'''
        return(await post_update_video(request))

    @routes.put('/videos')
    async def put_video(request):
        '''Endpoint de edição da base de dados'''
        return(await post_update_video(request))

    @routes.get('/videos/?page={page_id}')
    async def get_videos_by_page(request):
        '''Retorna 5 videos por pagina'''
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory= aiosqlite.Row
            start=(request.match_info["page_id"]-1)*5
            async with db.execute(f'SELECT * FROM videos WHERE id BETWEEN {start} AND {(start+4)}') as cursor:
                response = [dict(row) for row in cursor]
        return(web.json_response({'videos':response}))


async def post_update_video(request):
        '''Método que efetivamente muda os videos na base de dados'''

        
        new_video = await request.json()
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            try:
                async with db.execute(f'SELECT * FROM videos WHERE id={new_video["id"]}') as cursor:
                        async for row in cursor:
                            old=dict(row)
            except aiosqlite.Error:
                return(web.Response(status=400))

            for key in old:
                if key not in new_video:
                    new_video[key]=old[key]
        
            if await verify(new_video):
                async for key in new_video:
                    if key !=['id']:
                        await db.execute(f'UPDATE videos SET {key}={new_video[key]} WHERE id={new_video["id"]}')
                        await db.commit()
                return(web.Response(status=200))    
                
            else: return(web.Response(status=400))



