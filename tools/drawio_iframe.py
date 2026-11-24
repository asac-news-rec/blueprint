"""draw.io 파일을 yoonmo.html 안의 iframe으로 다시 넣는다.

청사진 사이트는 Cloudflare Access 뒤에 있어서 viewer.diagrams.net이 URL(#U)로 파일을 못 가져온다.
그래서 그림 XML을 압축해 iframe 주소의 #R 뒤에 넣는다. 그림을 고친 뒤 이 스크립트를 다시 돌린다.

실행: python tools/drawio_iframe.py            (기본: feast-flow.drawio → yoonmo.html)
      python tools/drawio_iframe.py <drawio> <html>
html 안의 <!-- drawio:<파일 이름> --> ... <!-- /drawio --> 사이를 바꾼다.
"""
import base64, html, re, sys, zlib
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "feast-flow.drawio"
page = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "yoonmo.html"


def compress(xml: str) -> str:
    """draw.io Graph.compress와 같다: encodeURIComponent → deflateRaw → base64."""
    raw = quote(xml, safe="-_.!~*'()").encode("ascii")
    deflater = zlib.compressobj(9, zlib.DEFLATED, -15)
    return base64.b64encode(deflater.compress(raw) + deflater.flush()).decode("ascii")


xml = src.read_text(encoding="utf-8").strip()
height = int(re.search(r'pageHeight="(\d+)"', xml).group(1)) + 40 if 'pageHeight="' in xml else 600
url = ("https://viewer.diagrams.net/?lightbox=0&nav=1&toolbar=zoom%20layers%20lightbox&title="
       + quote(src.name) + "#R" + quote(compress(xml), safe=""))
block = (f'<!-- drawio:{src.name} -->\n'
         f'  <div class="drawio"><iframe src="{html.escape(url)}" title="{html.escape(src.stem)}" '
         f'loading="lazy" style="width:100%;height:{height}px;border:1px solid var(--line);'
         f'border-radius:8px;background:#fff"></iframe></div>\n'
         f'  <!-- /drawio -->')
text = page.read_text(encoding="utf-8")
pattern = re.compile(rf"<!-- drawio:{re.escape(src.name)} -->.*?<!-- /drawio -->", re.S)
if not pattern.search(text):
    sys.exit(f"{page.name}에 <!-- drawio:{src.name} --> 표시가 없다")
page.write_text(pattern.sub(lambda m: block, text, count=1), encoding="utf-8")
print(f"{src.name} → {page.name} (주소 {len(url):,}자)")
