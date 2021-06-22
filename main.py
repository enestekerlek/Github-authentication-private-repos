import requests
import wget
from github import Github
import json
from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel

class personalAccessToken(BaseModel):

    PAT: str

app=FastAPI()


@app.get('/repos/{token}')
def getRepos(tokenn: Optional[str]=Header(None)):
    d=[]
    g = Github(tokenn)
    repo_list = [i for i in g.get_user().get_repos()]
    for i in repo_list:
        repo_name = str(i).replace('Repository(full_name="', '')
        repo_name = str(repo_name).replace('")', '')
        print('https://www.github.com/'+repo_name)
        d.append('https://www.github.com/'+repo_name)
    return {"List of all Repositories" : d}


#OWNER = 'enestekerlek'
#REPO  = 'privteko'

@app.get('/downloadRepo/{Owner_name}/{Repo_name}')
def downloadRepo(Repo_name:str, Owner_name:str, token: Optional[str]=Header(None)):

    REF = 'main'
    EXT = 'zip'

    # EXT  = 'tar'
    url = f'https://api.github.com/repos/{Owner_name}/{Repo_name}/{EXT}ball/{REF}'
    print('url:', url)

    headers = {
        "Authorization": 'token '+ token,
        "Accept": 'application/vnd.github.v3+json'
        #    "Accept": '*.*',
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        print('size:', len(r.content))
        with open(f'{Repo_name}.{EXT}', 'wb') as fh:
            fh.write(r.content)
        print(r.content[:10])  # display only some part
    else:
        print(r.text)
    return {"File is downloaded from ": url}
    wget.download(url)



#getRepos()
#OWNER=createOwner()
#REPO=getRepo_name()
#   downloadRepo(REPO)
