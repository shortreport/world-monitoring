import urllib.request, os, time

headers = {'User-Agent': 'Mozilla/5.0 (compatible; educational/research use)'}
os.makedirs('img_rinpa', exist_ok=True)

images = {
    'sotatsu_fujin.png':  'https://upload.wikimedia.org/wikipedia/commons/a/af/Wind-God-Fujin-and-Thunder-God-Raijin-by-Tawaraya-Sotatsu.png',
    'sotatsu_matsushima.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Tawaraya_Sotatsu_-_Waves_at_Matsushima_-_Google_Art_Project.jpg/1280px-Tawaraya_Sotatsu_-_Waves_at_Matsushima_-_Google_Art_Project.jpg',
    'koetsu_sotatsu.jpg': 'https://upload.wikimedia.org/wikipedia/commons/c/c1/Flowers_Grasses_Four_Seasons_%28Sotatsu_Koetsu%29.jpg',
    'korin_fujin.jpg':    'https://upload.wikimedia.org/wikipedia/commons/b/b4/Korin_Fujin_Raijin.jpg',
    'korin_plum.jpg':     'https://upload.wikimedia.org/wikipedia/commons/e/e8/Ogata_Korin_-_Red_And_White_Plum_Trees_%28National_Treasure%29.jpg',
    'korin_iris1.jpg':    'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Irises_screen_1.jpg/1280px-Irises_screen_1.jpg',
    'korin_iris2.jpg':    'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Irises_screen_2.jpg/1280px-Irises_screen_2.jpg',
    'kiitsu_asagao.jpg':  'https://upload.wikimedia.org/wikipedia/commons/7/7c/Asagao-zu_By%C5%8Dbu_by_Kiitsu_Suzuki.jpg',
}

for name, url in images.items():
    path = f'img_rinpa/{name}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r, open(path, 'wb') as f:
            f.write(r.read())
        print(f'OK  {name}: {os.path.getsize(path):,} bytes')
    except Exception as e:
        print(f'FAIL {name}: {e}')
    time.sleep(2)
