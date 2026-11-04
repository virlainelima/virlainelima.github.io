#!/usr/bin/env python3
"""Gera a arte 1080x1920 do Stories e envia ao Telegram.
Uso: TG_TOKEN=... TG_CHAT=... python3 arte_stories.py "Nome" "R$ X" "R$ Y" Z "URL_DA_IMAGEM" saida.png
"""
import base64, html, json, os, subprocess, sys, urllib.parse, urllib.request
nome, de, por, desc, img, saida = sys.argv[1:7]
T, C = os.environ["TG_TOKEN"], os.environ["TG_CHAT"]
api = lambda m, **d: json.load(urllib.request.urlopen(f"https://api.telegram.org/bot{T}/{m}", urllib.parse.urlencode(d).encode(), timeout=60))
foto = ""
try:
    # O Telegram busca a foto; depois baixamos a cópia e apagamos a mensagem provisória.
    r = api("sendPhoto", chat_id=C, photo=img, disable_notification="true")["result"]
    p = api("getFile", file_id=r["photo"][-1]["file_id"])["result"]["file_path"]
    b = urllib.request.urlopen(f"https://api.telegram.org/file/bot{T}/{p}", timeout=60).read()
    api("deleteMessage", chat_id=C, message_id=r["message_id"])
    foto = '<img src="data:image/jpeg;base64,' + base64.b64encode(b).decode() + '">'
except Exception as e:
    print("sem foto:", type(e).__name__)
e = html.escape
pagina = f"""<!doctype html><meta charset=utf-8><style>
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1920px;background:#f8f2e9;color:#33261d;font-family:"Liberation Serif",Georgia,serif;text-align:center;padding:96px 72px 0}}
.t{{font:700 104px/1 "Liberation Sans",sans-serif;color:#a4502e}}
.f{{position:relative;margin:48px auto 0;width:800px;height:800px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.f img{{width:100%;height:100%;object-fit:contain}}
.s{{position:absolute;top:30px;left:30px;background:#a4502e;color:#fff;font:700 54px/1 "Liberation Sans",sans-serif;padding:20px 30px;border-radius:99px}}
.n{{font-size:54px;line-height:1.15;margin-top:42px}}
.d{{font:44px/1 "Liberation Sans",sans-serif;color:#76675b;text-decoration:line-through;margin-top:24px}}
.p{{font:700 104px/1.1 "Liberation Sans",sans-serif;color:#843c20;margin-top:12px}}
</style><div class=t>OFERTA DAS 19H</div><div class=f>{foto}<span class=s>-{e(desc)}%</span></div><div class=n>{e(nome)}</div><div class=d>De {e(de)}</div><div class=p>Por {e(por)}</div>"""
h = os.path.abspath(saida) + ".html"
open(h, "w", encoding="utf8").write(pagina)
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{h}');await p.screenshot({{path:{json.dumps(saida)}}});await b.close()}})()"
subprocess.run(["node", "-e", js], check=True)
subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "envio %{http_code}\n", f"https://api.telegram.org/bot{T}/sendDocument", "-F", f"chat_id={C}", "-F", f"document=@{saida}", "-F", "caption=📲 Stories das 19h"], check=True)
