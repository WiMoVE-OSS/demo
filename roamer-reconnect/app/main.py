from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()
wlan_iface = "wlp13s0"

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

def roam_to(bssid):
    result = subprocess.run(["wpa_cli", "-i", wlan_iface, "bssid", "1", bssid], stdout=subprocess.PIPE)
    print(result.returncode)
    print(result.stdout.decode("utf-8"))
    result = subprocess.run(["wpa_cli", "-i", wlan_iface, "disconnect"], stdout=subprocess.PIPE)
    print(result.returncode)
    print(result.stdout.decode("utf-8"))
    result = subprocess.run(["wpa_cli", "-i", wlan_iface, "reconnect"], stdout=subprocess.PIPE)
    print(result.stdout.decode("utf-8"))
    print(result.returncode)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/acs2", response_class=RedirectResponse)
async def acs2(request: Request):
    roam_to("00:25:9c:13:a2:c4")
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/acs3", response_class=RedirectResponse)
async def acs3(request: Request):
    roam_to("00:25:9c:13:e9:a2")
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/acs6", response_class=RedirectResponse)
async def acs6(request: Request):
    roam_to("00:25:9c:13:e9:a3")
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
