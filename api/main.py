from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware # TODO remove.
import html
import sys
sys.path.insert(0, "./sources")
from animixplay import Animix
from leetx import Leetx
from nyaa import Nyaa

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"]) # TODO remove.

animix = Animix()

@app.get("/animix/{title}")
async def animixSearch(title: str = Query(max_length=40)):
    query = html.escape(title)
    results = animix.search(query)
    return {"results":results}

@app.get("/animix/total/{title}/{index}")
async def animixTotalEpisodesByTitle(title: str, index: int):
    query = html.escape(title)
    results = animix.search(query)
    if index < 0 or index > len(results):
        return {"total":None}
    
    target = results[index]["url"]
    totalEpisodes = animix.getTotalEpisodes(target)

    return {"total": totalEpisodes}

@app.get("/animix/{title}/{index}/{episode}")
async def animixEpisodeByTitle(title: str, index: int, episode: int):
    query = html.escape(title)
    results = animix.search(query)
    if index < 0 or index > len(results) or episode < 1:
        return {"episode":None}
    
    target = results[index]["url"]
    totalEpisodes = animix.getTotalEpisodes(target)
    if episode > totalEpisodes:
        return {"episode":None}

    stream = animix.getEpisodeStream(target, episode)
    return {"stream": stream}

@app.get("/leetx/{title}")
async def leetxSearch(title: str):
    query = html.escape(title)
    leetx = Leetx()
    results = leetx.search(query)
    return {"results":results}

@app.get("/nyaa/{title}")
async def nyaaSearch(title: str):
    query = html.escape(title)
    nyaa = Nyaa()
    results = nyaa.search(query)
    return {"results":results}
