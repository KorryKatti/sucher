from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


summary = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus dapibus efficitur bibendum. Pellentesque vitae venenatis orci. Etiam convallis est vel luctus tristique. Aliquam euismod dui vel orci ultricies, et vulputate massa pretium. Interdum et malesuada fames ac ante ipsum primis in faucibus. Proin mollis aliquam suscipit. Integer quis erat accumsan, maximus urna non, imperdiet nisi. Curabitur pharetra non elit vel convallis. Etiam at tellus turpis. Phasellus commodo nisl tortor, sit amet ultrices arcu elementum sit amet. Sed hendrerit, nisi non rutrum scelerisque, justo velit venenatis nibh, ac ultrices diam dolor sit amet orci. Morbi malesuada ex finibus, consectetur ante malesuada, auctor tellus. Morbi commodo metus sed lacus porttitor, nec tempor massa iaculis.

Sed pellentesque nisi purus, nec dignissim ligula tincidunt vel. Nunc elementum nulla et suscipit tristique. Pellentesque aliquam elit metus, at rutrum est tincidunt nec. Donec vel aliquam dolor. Sed tristique purus in efficitur finibus. Sed vel eleifend mauris. Vivamus a ornare leo, at rutrum quam.

Sed at nunc pulvinar, sollicitudin odio vel, cursus libero. Sed tincidunt sollicitudin faucibus. Donec a volutpat nibh, vitae dictum ex. Nam risus massa, porta vitae lectus et, efficitur vehicula lectus. Donec sed lobortis quam. In venenatis augue urna, eu molestie urna venenatis sollicitudin. Sed convallis est vitae nibh congue, id facilisis orci condimentum. Proin et elit finibus, eleifend lorem ac, luctus dolor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce maximus maximus dui sit amet consectetur.

Morbi viverra nisl vel turpis placerat, eget vestibulum metus commodo. Etiam malesuada ex elit, quis mattis sapien auctor et. Praesent a tincidunt leo. Nullam scelerisque metus non feugiat fringilla. Curabitur ipsum leo, blandit sit amet magna at, faucibus tempor massa. Donec nec tortor tortor. Morbi egestas tempus purus. Proin cursus bibendum nisi vitae aliquam. Nunc eget hendrerit nibh, eget luctus lectus. Nam ac tortor blandit, pellentesque orci posuere, sodales turpis.

Aenean sagittis ullamcorper risus eu mattis. Nulla a neque ut magna dictum tincidunt id in neque. Nulla euismod orci lacus, et porttitor ante vestibulum eget. Aenean consequat urna ut ornare facilisis. Nunc tincidunt nunc eget augue sodales, ut elementum lectus iaculis. Vivamus hendrerit leo augue, eu placerat libero interdum sit amet. Phasellus faucibus tellus enim, ac pharetra risus varius vitae. Donec facilisis aliquam nunc et semper. Sed sit amet tortor mi. Donec vel faucibus quam. Cras blandit orci efficitur, semper sem tempor, blandit eros. Ut faucibus molestie metus, eget dictum erat pellentesque vel. Pellentesque dignissim ex a ligula volutpat mollis."""

@app.get("/search")
async def search(q: str):
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)
        search_results = response.json()
    
    if "query" not in search_results or "search" not in search_results["query"]:
        return {"results": [], "error": "Invalid Wikipedia response"}

    results = []
    for item in search_results["query"]["search"]:
        title = item["title"]
        page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        snippet = item["snippet"]
        results.append({"title": title, "link": page_url, "snippet": snippet})
    
    return {"results": results, "summary": summary}
    print(results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

