"""모든 페이지와 사진을 HTML 한 파일로 묶는다 (내려받아 보기용).

실행: python tools/bundle.py   ->  dist/blueprint_all_in_one.html
"""
import io, json, base64, os, sys

R = sys.argv[1] if len(sys.argv) > 1 else "."
names = ['index', 'overview', 'taewon', 'seho', 'yoonmo', 'juhyun', 'wbs']
pages = {}
for n in names:
    pages[n] = io.open(f'{R}/{n}.html', encoding='utf-8').read()

png = base64.b64encode(open(f'{R}/infra_v2.png', 'rb').read()).decode()
pages['juhyun'] = (pages['juhyun']
                   .replace('<a href="infra_v2.png">', '<a href="#fig">')
                   .replace('src="infra_v2.png"', 'src="data:image/png;base64,' + png + '"'))
for n in names:
    assert 'infra_v2.png' not in pages[n], n

data = json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')

shell = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>뉴스 추천 공동 청사진</title>
<style>
html,body{margin:0;height:100%;background:#f4f6f5}
iframe{display:block;width:100%;height:100%;border:0}
</style>
</head>
<body>
<iframe id="view" title="공동 청사진"></iframe>
<script>
var PAGES = DATA;
var view = document.getElementById('view');
function go(name, anchor, push) {
  if (!PAGES[name]) name = 'index';
  view.onload = function () {
    var d = view.contentDocument;
    document.title = d.title || '뉴스 추천 공동 청사진';
    d.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a) return;
      var m = a.getAttribute('href').match(/^([a-z]+)\\.html(#.*)?$/);
      if (m) { e.preventDefault(); go(m[1], m[2] ? m[2].slice(1) : '', true); }
    });
    if (anchor) { var t = d.getElementById(anchor); if (t) t.scrollIntoView(); }
  };
  view.srcdoc = PAGES[name];
  var h = '#' + name + (anchor ? '/' + anchor : '');
  if (push) history.pushState(null, '', h); else history.replaceState(null, '', h);
}
function fromHash() {
  var p = location.hash.slice(1).split('/');
  go(p[0] || 'index', p[1] || '', false);
}
window.addEventListener('popstate', fromHash);
fromHash();
</script>
</body>
</html>
'''.replace('DATA', data)
os.makedirs(f'{R}/dist', exist_ok=True)
io.open(f'{R}/dist/blueprint_all_in_one.html', 'w', encoding='utf-8').write(shell)
print(len(shell))
