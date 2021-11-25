from aiohttp import web
import aiosqlite
from utils.utils import verify

DATABASE = './db/aluraflix.db'




class Videos_id:
    '''Classe de handlers do endpoint /videos/{video_id}'''

    routes = web.RouteTableDef()
    
    @routes.get('/videos/{videos_id}')
    async def single_video(self,request):
        '''Endpoint que retorna video por id'''
        try:
            async with aiosqlite.connect(DATABASE) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(f'''SELECT DISTINCT * FROM videos WHERE id ={request.match_info['video_id']}''') as cursor:
                    async for row in cursor:
                        response=dict(row)
            return(web.json_response(response))
        except:
            return(web.Response(status=404))

    @routes.delete('/videos/{videos_id}')
    async def delete_video(self,request):
        '''Endpoint que deleta um video por id'''
        try:
            async with aiosqlite.connect(DATABASE) as db:
                await db.execute(f"DELETE FROM videos WHERE id={request.match_info['video_id']}")
                await db.commit()
            return(web.Response(status=200))
        except:
            return(web.Response(status=400))
