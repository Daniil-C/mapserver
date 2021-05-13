import json
from http.client import HTTPException

import uvicorn
from fastapi import FastAPI

HOST = "0.0.0.0"
PORT = 8000

app = FastAPI(debug=True)

datafile = "data.json"


@app.get("/load")
async def load():
    try:
        with open(datafile, "r") as fin:
            return json.loads(fin.read())
    except FileNotFoundError as exc:
        raise HTTPException(500, exc) from exc


@app.post("/test")
async def load(data: dict):
    print(data["login"])
    with open(datafile, "r") as fin:
        base = json.loads(fin.read())
        base["6fl_nodes_cont"] = data["login"]
    with open(datafile, "w") as fout:
        fout.write(json.dumps(base))
    return {}


@app.post("/change")
async def change_status(data: dict):
    print(dict)
    try:
        with open(datafile, "r") as fin:
            base = json.loads(fin.read())

            floor = data["floor"]
            name = data["name"]
            st = data["status"]

            c = json.loads(base[str(floor) + "fl_marks"])
            for i in c:
                if i["name"] == name:
                    i["status"] = st

            base[str(floor) + "fl_marks"] = json.dumps(c)

        with open(datafile, "w") as fout:
            fout.write(json.dumps(base))
    except (KeyError, FileNotFoundError) as exc:
        raise HTTPException(404, exc) from exc
    return 0


if __name__ == "__main__":
    uvicorn.run("__main__:app", host=HOST, port=PORT, reload=True)
