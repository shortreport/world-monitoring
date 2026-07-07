base = r"C:\Users\shondo\Desktop\agent_project\img_emaki" + "\\"

with open("make_emaki_slides.js", "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Illustrated_Handscroll_of_The_Tale_of_Genji.jpg/900px-Illustrated_Handscroll_of_The_Tale_of_Genji.jpg": base + "genji.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Sigisanengi_tobikura.jpg/1280px-Sigisanengi_tobikura.jpg": base + "shigisan1.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/People_following_the_rice.jpg/1280px-People_following_the_rice.jpg": base + "shigisan2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Chouju_1st_scroll-02.jpg/1280px-Chouju_1st_scroll-02.jpg": base + "choju1.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Chouju_1st_scroll-01.jpg/1280px-Chouju_1st_scroll-01.jpg": base + "choju2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Ban_Dainagon_-_ox_cart_people.jpg/1280px-Ban_Dainagon_-_ox_cart_people.jpg": base + "ban1.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Ban_Dainagon_-_exile_A.jpg/1280px-Ban_Dainagon_-_exile_A.jpg": base + "ban2.jpg",
}

for url, local in replacements.items():
    local_js = local.replace("\\", "\\\\")
    content = content.replace(url, local_js)

with open("make_emaki_slides.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
