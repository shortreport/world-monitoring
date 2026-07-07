import urllib.request, os, time

headers = {'User-Agent': 'Mozilla/5.0 (compatible; educational/research use)'}
os.makedirs('img_ukiyoe', exist_ok=True)

images = {
    # 菱川師宣
    'moronobu_bijin.jpg': 'https://upload.wikimedia.org/wikipedia/commons/7/7f/Beauty_looking_back.jpg',
    # 鈴木春信
    'harunobu_asakusa.jpg': 'https://upload.wikimedia.org/wikipedia/commons/0/06/Parody_of_Eight_Sceneries_of_Edo_Fine_Day_at_Asakusa-by_Suzuki_Harunobu-Tokyo_National_Museum.jpg',
    # 喜多川歌麿
    'utamaro_okita.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/27/Utamaro_Naniwaya_Okita.JPG',
    # 東洲斎写楽
    'sharaku_oniji.jpg': 'https://upload.wikimedia.org/wikipedia/commons/0/0e/Toshusai_Sharaku-_Otani_Oniji%2C_1794.jpg',
    # 葛飾北斎
    'hokusai_wave.jpg': 'https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg',
    'hokusai_fuji.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/1280px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg',
    # 歌川広重
    'hiroshige_shower.jpg': 'https://upload.wikimedia.org/wikipedia/commons/7/72/Hiroshige%2C_Sudden_shower_over_Shin-%C5%8Chashi_bridge_and_Atake%2C_1857.jpg',
}

for name, url in images.items():
    path = f'img_ukiyoe/{name}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r, open(path, 'wb') as f:
            f.write(r.read())
        print(f'OK  {name}: {os.path.getsize(path):,} bytes')
    except Exception as e:
        print(f'FAIL {name}: {e}')
    time.sleep(2)
