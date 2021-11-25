from aiohttp import web
import aiosqlite


DATABASE = './db/aluraflix'



class Users:

    '''Classe base dos endpoints de autenticação'''

    routes = web.RouteTableDef()


    @routes.get('/login')
    async def login_page(request):
        '''Retorna a a pagina de login '''

        return(web.Response(text='Login'))

    @routes.post('/login')
    async def login_handler(request):
        ''' Faz efetivamente o Login '''

        async with aiosqlite.connect(DATABASE) as db:
            pass
