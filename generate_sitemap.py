import os
from pathlib import Path
from datetime import datetime
import html # URLに '&' などが含まれる場合のエスケープ処理用

# --- 設定 ---
# 1. あなたのサイトのベースURL（最後のが / で終わらないように）
BASE_URL = "https://horizonnotes.netlify.app"

# 2. スクリプトを実行するフォルダ（このファイルがある場所）
ROOT_DIR = Path('.')

# 3. 出力するサイトマップのファイル名
OUTPUT_FILE = ROOT_DIR / 'sitemap.xml'
# --- 設定ここまで ---

def generate_sitemap():
    """
    ROOT_DIR以下のすべてのHTMLファイルを探し、
    sitemap.xml を自動生成します。
    """
    print(f"'{ROOT_DIR.resolve()}' 以下のHTMLファイルをスキャンします...")
    
    url_list = []

    # 1. 全HTMLファイルを見つける (fix_canonical.py と同じロジック)
    for html_file in ROOT_DIR.rglob('*.html'):
        
        # GitやVSCodeなどの管理フォルダは無視
        if any(part.startswith('.') for part in html_file.parts):
            continue

        # _includes フォルダ（部品）は無視
        if '_includes' in html_file.parts:
            continue
        
        # 実行スクリプト自体も無視
        if html_file.name.endswith('.py'):
            continue

        # 2. 相対パスを計算 (fix_canonical.py と同じロジック)
        relative_path = html_file.relative_to(ROOT_DIR).as_posix()
        
        # 3. index.html の場合は / にする (fix_canonical.py と同じロジック)
        if relative_path.endswith('index.html'):
            relative_path = relative_path[:-len('index.html')]
        
        # 4. URLをリストに追加
        new_url = f"{BASE_URL}/{relative_path}"
        url_list.append(new_url)

    print(f"検出したURL数: {len(url_list)}")

    # 5. sitemap.xml の中身（文字列）を生成
    
    # XMLのヘッダー部分
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # <lastmod> (最終更新日) タグは、Googleに更新を伝えるのに役立ちます
    # 本来はファイルごとの更新日を見るべきですが、今回は簡易的に「今日」の日付を使います
    today_str = datetime.now().strftime('%Y-%m-%d')

    # 6. URLリストをXMLタグの形式に変換
    for url in url_list:
        # URLをエスケープ処理 (例: & -> &amp;)
        escaped_url = html.escape(url)
        
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{escaped_url}</loc>\n'
        xml_content += f'    <lastmod>{today_str}</lastmod>\n'
        # (優先度はオプションなので、今回はシンプルに省略)
        xml_content += '  </url>\n'

    xml_content += '</urlset>'

    # 7. ファイルに書き出す
    try:
        OUTPUT_FILE.write_text(xml_content, encoding='utf-8')
        print(f"\n--- 完了 ---")
        print(f"'{OUTPUT_FILE.resolve()}' にサイトマップを生成しました。")
    except Exception as e:
        print(f"\n[エラー] ファイルの書き込みに失敗しました: {e}")

if __name__ == "__main__":
    generate_sitemap()