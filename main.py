from api.routes import user

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/",response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title style="color:red">ND fastAPI</title>
    <style>
        h1 {
        color: #ffff;
        font-size: 55px;
        }
        body {
            background-color: #023047;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        a {
            text-decoration: none;
            color: #ffff;
            font-size: 20px;
        }
        a {
           padding: 20px;
           border:none;
           background-color: #127047;
           color: #fff;
           font-weight: bold;
           font-size: 25px;
           margin-top: 35px;
           cursor: pointer;
        }
  </style>
        </head>
        <body>
            <h1>Bienvenue au ND fastAPI</h1>
            <a  id="redi" onclick="handleClick()">Lire la documentation</a>

            <script>
            handleClick = function(event){
            var url=window.location.href + "docs"
                var ancre=document.getElementById('redi').setAttribute("href",url)
               } 
             function getCurrentURL () {
                return window.location.href
                    }
            </script>
        </body>
    </html>
    """


app.include_router(user.router, tags=['users'] ,prefix="/api/user")




# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


    

