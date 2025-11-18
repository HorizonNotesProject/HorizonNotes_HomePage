import os
import re
from pathlib import Path

# --- 設定 ---
# 1. あなたのサイトのベースURL（最後のが / で終わらないように）
BASE_URL = "https://horizonnotes.netlify.app"

# 2. スクリプトを実行するフォルダ（このファイルがある場所）
#    プロジェクトのルートフォルダに置いていれば変更不要
ROOT_DIR = Path('.')

# 3. 置換するcanonicalタグの正規表現
#    <link rel="canonical" href="..." /> を丸ごと見つけます
#    (スペースの有無や " /" がなくても動くようにしています)
CANONICAL_REGEX = re.compile(
    r'<link\s+rel="canonical"\s+href=".*?"\s*/?>'
)
# --- 設定ここまで ---

def update_canonical_tags():
    """
    ROOT_DIR以下のすべてのHTMLファイルを探し、
    canonicalタグをファイルパスに基づいた正しいURLに書き換えます。
    """
    print(f"'{ROOT_DIR.resolve()}' 以下のHTMLファイルをスキャンします...")
    
    file_count = 0
    updated_count = 0

    # .rglob('*.html') は、全サブフォルダを再帰的に探して .html ファイルを見つけます
    for html_file in ROOT_DIR.rglob('*.html'):
        
        # 実行スクリプト自体は無視
        if html_file.name == 'fix_canonical.py':
            continue

        file_count += 1
        
        try:
            # 1. ファイルパスから、サイトの相対パスを計算
            #    例: SpellCard/001_Preparing.html
            #    （WindowsでもURLフレンドリーな '/' 区切りにします）
            relative_path = html_file.relative_to(ROOT_DIR).as_posix()
            
            # index.html の場合は、末尾の "index.html" を削除して "/" にする
            if relative_path.endswith('index.html'):
                # ルートの index.html 以外 (例: /cards/index.html) も考慮
                relative_path = relative_path[:-len('index.html')]
            
            # 2. 新しいURLとタグを作成
            new_url = f"{BASE_URL}/{relative_path}"
            new_tag = f'<link rel="canonical" href="{new_url}" />'

            # 3. ファイルを読み込む
            content = html_file.read_text(encoding='utf-8')
            
            # 4. 古いcanonicalタグを、新しいタグで置換
            #    re.sub() は、見つからなければ何もせず、見つかれば置換します
            new_content, num_replacements = CANONICAL_REGEX.subn(new_tag, content)

            # 5. もし置換が発生したら、ファイルを書き戻す
            if num_replacements > 0:
                html_file.write_text(new_content, encoding='utf-8')
                print(f"[更新] {html_file.relative_to(ROOT_DIR)} -> {new_url}")
                updated_count += 1
            else:
                # canonicalタグが元々なかったファイル（無視）
                print(f"[スキップ] {html_file.relative_to(ROOT_DIR)} (canonicalタグ見つからず)")

        except Exception as e:
            print(f"[エラー] {html_file.relative_to(ROOT_DIR)} の処理中にエラー: {e}")

    print("\n--- 完了 ---")
    print(f"スキャンしたHTMLファイル数: {file_count}")
    print(f"更新したファイル数: {updated_count}")

if __name__ == "__main__":
    update_canonical_tags()