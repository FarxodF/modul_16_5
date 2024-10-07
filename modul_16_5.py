from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()
# Инициализация Jinja2Templates
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users, 'user_detail': None})


@app.get('/users/{user_id}', response_class=HTMLResponse)
async def read_user(request: Request, user_id: Annotated[int, Path(description='Введите ID пользователя', ge=1)]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'users': users, 'user_detail': user})
    raise HTTPException(status_code=404, detail='Пользователь не найден')


@app.post('/user/{username}/{age}')
def create_user(username: Annotated[str, Path(description='Введите имя пользователя', min_length=5, max_length=20)],
                age: Annotated[int, Path(description='Введите возраст', ge=18, le=120)]):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user
