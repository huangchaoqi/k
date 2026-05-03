from pathlib import Path


html_path = Path("shanghai-house-price-kline.html")
data_path = Path("shanghai-house-price-data.js")
out_path = Path("shanghai-house-price-kline-single.html")
index_path = Path("index.html")

html = html_path.read_text(encoding="utf-8")
data = data_path.read_text(encoding="utf-8").strip()
external = '  <script src="./shanghai-house-price-data.js"></script>'
embedded = f"  <script>\n    {data}\n  </script>"

if external not in html:
    raise SystemExit("External data script tag not found.")

single_html = html.replace(external, embedded)
out_path.write_text(single_html, encoding="utf-8")
index_path.write_text(single_html, encoding="utf-8")
print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
print(f"Wrote {index_path} ({index_path.stat().st_size} bytes)")
