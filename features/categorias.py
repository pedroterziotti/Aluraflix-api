from aiohttp import web
import aiosqlite
from utils.utils import verify

DATABASE = './db/aluraflix.db'

class Categorias:

    def __init__(self):
        pass

    routes = web.RouteTableDef()

    @routes.get('/categorias')
    async def get_all_catgerias(request):
        '''Exibe todas as categorias'''
        
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM categorias') as cursor:
                response=[]
                async for row in cursor:
                    response.append(dict(row))
        return(web.json_response({'videos':response}))

        
    @routes.get('/categorias/{categoriaId}')
    async def get_categoria_by_id(request):
        '''Exibe uma ctegoria dado um id'''
        
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f'SELECT * FROM categorias WHERE id = {request.match_info["categoriaId"]}') as cursor:
                response = []
                async for row in cursor:
                    response.append(dict(row))
        return(web.json_response({'categoria':response}))
    
    @routes.post('/categorias')
    async def create_new_categoria(request):
        '''Cria uma nova categoria caso todos os dados estejam validos'''
        nova_categoria= await request.json()
        if await verify(nova_categoria):
            async with aiosqlite.connect(DATABASE) as db:
                db.row_factory=aiosqlite.Row
                await db.execute(f'INSERT INTO categorias {tuple(nova_categoria.keys())} VALUES {tuple(nova_categoria.values())}')
                await db.commit()
                return(web.Response(status=200))
        else: return(web.Response(status=400))

    @routes.put('/categorias')
    async def put_categorias(request):
        '''Atualiza uma categoria'''
        nova_catgeoria = await request.json()
        if await verify(nova_catgeoria):
            async with aiosqlite.connect(DATABASE) as db:
                old= await db.execute(f'SELECT * FROM categorias WHERE id={nova_catgeoria["id"]}')
                await db.execute(f'INSER INTO categorias WHERE {tuple(nova_catgeoria.keys())} VALUES {tuple(nova_catgeoria.values())}')
                await db.commit()
                return(web.Response(status=200))
        else: return(web.Response(status=400))
    
    @routes.patch('/categorias')
    async def patch_categorias(request):
        '''Atualiza uma categoria'''
        nova_catgeoria = await request.json()
        if await verify(nova_catgeoria):
            async with aiosqlite.connect(DATABASE) as db:
                old= await db.execute(f'SELECT * FROM categorias WHERE id={nova_catgeoria["id"]}')
                for key in nova_catgeoria.keys():
                    if key != 'id':
                        await db.execute(f'UPDATE categorias SET {key} = "{nova_catgeoria[key]}" WHERE id={nova_catgeoria["id"]}')
                        await db.commit()
                return(web.Response(status=200))
        else: return(web.Response(status=400))

    @routes.delete('/categorias/{categoriaId}')
    async def delete_categoria(request):
        '''Deleta uma categoria dada um id'''
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute(f'DELETE FROM categorias WHERE id={request.match_info["categoriaId"]}')
        return(web.Response(status=200))

    @routes.get('/categorias/{categoriaId}/videos')
    async def get_videos_by_categoria(request):
        '''Retorna todos os videos de uma determinada categoria'''
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute( f'SELECT * FROM videos WHERE categoriaId={request.match_info["categoriaId"]}') as cursor:
                response=[]
                async for row in cursor:
                    response.append(dict(row))
        return(web.json_response({'videos':response}))

    @routes.get('/categorias/?page={categorias_id}')
    async def get_categorias_by_page(request):
        '''Retorna 5 categorias por pagina'''
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory= aiosqlite.Row
            start=(request.match_info["categorias_id"]-1)*5
            async with db.execute(f'SELECT * FROM categorias WHERE id BETWEEN {start} AND {(start+4)}') as cursor:
                response = [dict(row) for row in cursor]
        return(web.json_response({'categorias':response}))