const pptxgen = require("pptxgenjs");
const path = require("path");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = '琳派の系譜';

const IMG = (f) => path.resolve(__dirname, "img_rinpa", f);

// ── カラーパレット（金・墨・藍・深緑）──────────────────────
const C = {
  dark:     "14110D",   // 漆黒
  ink:      "1C1C1C",   // 墨
  gold:     "B8860B",   // 金
  goldLight:"E8C85A",   // 薄金
  indigo:   "1B2A4A",   // 藍（江戸琳派）
  green:    "1A3328",   // 深緑
  crimson:  "8B1A1A",   // 朱
  parchment:"F5EFE0",   // 和紙
  cream:    "FDFAF4",   // 薄和紙
  midBrown: "7A5C3A",
  lightBrown:"C4A882",
  darkText: "1C1408",
  white:    "FFFFFF",
  silver:   "C0C0C0",
};

function makeShadow() {
  return { type: "outer", blur: 5, offset: 2, angle: 135, color: "000000", opacity: 0.18 };
}

function setupLight(s) {
  s.background = { color: C.cream };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.3, y: 0.42, w: 0.05, h: 4.82,
    fill: { color: C.gold }, line: { color: C.gold }
  });
}

function slideTitle(s, title, sub) {
  s.addText(title, {
    x: 0.55, y: 0.28, w: 9.1, h: 0.56,
    fontSize: 24, bold: true, fontFace: "Georgia",
    color: C.darkText, align: "left", margin: 0
  });
  if (sub) s.addText(sub, {
    x: 0.55, y: 0.85, w: 9.1, h: 0.28,
    fontSize: 12, fontFace: "Calibri",
    color: C.midBrown, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 0.55, y: sub ? 1.15 : 0.92, w: 9.0, h: 0,
    line: { color: C.lightBrown, width: 0.8 }
  });
}

// ── セクション扉（各画家） ────────────────────────────────────
function sectionSlide(num, name, era, kana, color, bgColor) {
  let s = pres.addSlide();
  s.background = { color: bgColor || C.dark };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.0, y: 0, w: 3.0, h: 5.625,
    fill: { color: color }, line: { color: color }
  });

  s.addText(num, {
    x: 0.45, y: 0.3, w: 1.0, h: 1.0,
    fontSize: 60, bold: true, fontFace: "Georgia",
    color: color, align: "left", margin: 0
  });
  s.addText(name, {
    x: 0.45, y: 1.28, w: 6.4, h: 0.9,
    fontSize: 40, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });
  s.addText(kana, {
    x: 0.45, y: 2.22, w: 6.4, h: 0.4,
    fontSize: 16, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 0.45, y: 2.75, w: 6.3, h: 0,
    line: { color: color, width: 1.5 }
  });
  s.addText(era, {
    x: 0.45, y: 2.92, w: 6.3, h: 0.42,
    fontSize: 15, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0
  });

  s.addText("琳派", {
    x: 7.0, y: 2.2, w: 3.0, h: 0.6,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", margin: 0
  });
  s.addText("Rinpa School", {
    x: 7.0, y: 2.9, w: 3.0, h: 0.38,
    fontSize: 12, fontFace: "Calibri",
    color: "DDDDDD", align: "center", margin: 0
  });
}

// ── 作品ビューア（画像 + キャプション + 解説カード） ─────────
function addArtwork(s, imgFile, caption, x, y, w, h, borderColor) {
  s.addImage({
    path: IMG(imgFile), x, y, w, h,
    sizing: { type: "contain", w, h }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: borderColor || C.lightBrown, width: 0.8 }
  });
  if (caption) s.addText(caption, {
    x, y: y + h + 0.04, w, h: 0.26,
    fontSize: 9, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });
}

// ── ポイントカード ───────────────────────────────────────────
function addCard(s, x, y, w, h, title, body, accentColor) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.parchment }, line: { color: C.lightBrown },
    shadow: makeShadow()
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.07, h,
    fill: { color: accentColor || C.gold }, line: { color: accentColor || C.gold }
  });
  if (title) s.addText(title, {
    x: x + 0.16, y: y + 0.1, w: w - 0.22, h: 0.36,
    fontSize: 13, bold: true, fontFace: "Calibri",
    color: accentColor || C.gold, align: "left", margin: 0
  });
  s.addText(body, {
    x: x + 0.16, y: y + (title ? 0.48 : 0.14), w: w - 0.22, h: h - (title ? 0.55 : 0.2),
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, align: "left", valign: "top", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド1: タイトル
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: C.dark };

  // 左上から右下に金の斜めストライプ風（2本の細い矩形）
  s.addShape(pres.shapes.RECTANGLE, {
    x: -0.5, y: 4.8, w: 11, h: 0.06,
    fill: { color: C.gold }, line: { color: C.gold }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: -0.5, y: 5.2, w: 11, h: 0.02,
    fill: { color: C.gold, transparency: 60 }, line: { color: C.gold, transparency: 60 }
  });

  // 右側パネル
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.2, y: 0, w: 2.8, h: 4.8,
    fill: { color: "1A1208" }, line: { color: "1A1208" }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.18, y: 0, w: 0.04, h: 4.8,
    fill: { color: C.gold }, line: { color: C.gold }
  });

  s.addText("琳派の系譜", {
    x: 0.45, y: 0.7, w: 6.6, h: 1.4,
    fontSize: 56, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });
  s.addText("The Rinpa School Lineage", {
    x: 0.45, y: 2.15, w: 6.6, h: 0.45,
    fontSize: 18, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 0.45, y: 2.72, w: 6.5, h: 0,
    line: { color: C.gold, width: 1.2 }
  });
  s.addText([
    { text: "本阿弥光悦・俵屋宗達 ", options: { breakLine: true } },
    { text: "→  尾形光琳・乾山 ", options: { breakLine: true } },
    { text: "→  酒井抱一・鈴木其一", options: {} },
  ], {
    x: 0.45, y: 2.9, w: 6.6, h: 1.35,
    fontSize: 17, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0, paraSpaceAfter: 8
  });
  s.addText("中学校 美術 ／ 日本近世絵画", {
    x: 0.45, y: 4.55, w: 6.6, h: 0.35,
    fontSize: 13, fontFace: "Calibri",
    color: C.midBrown, align: "left", margin: 0
  });

  // 右パネル内容
  s.addText("17〜19世紀", {
    x: 7.25, y: 0.9, w: 2.7, h: 0.45,
    fontSize: 13, fontFace: "Calibri",
    color: C.gold, align: "center", margin: 0
  });
  s.addText("江戸", {
    x: 7.25, y: 1.4, w: 2.7, h: 1.0,
    fontSize: 44, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", margin: 0
  });
  s.addText("時代の美", {
    x: 7.25, y: 2.5, w: 2.7, h: 0.42,
    fontSize: 16, fontFace: "Georgia",
    color: C.lightBrown, align: "center", margin: 0
  });
  s.addText("国宝・重要文化財\n多数を擁する流派", {
    x: 7.25, y: 3.1, w: 2.7, h: 0.8,
    fontSize: 12, fontFace: "Calibri",
    color: "AAAAAA", align: "center", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド2: 琳派とは・系譜概観
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "琳派とは？ — その特徴と系譜");

  s.addText([
    { text: "17世紀初め、京都で生まれた日本絵画の流派", options: { bullet: true, breakLine: true } },
    { text: "「師弟関係」ではなく「私淑（ししゅく）」で受け継がれた異色の流派", options: { bullet: true, breakLine: true } },
    { text: "金銀箔・鮮やかな色彩・大胆なデザイン性が特徴", options: { bullet: true, breakLine: true } },
    { text: "自然をモチーフに、装飾と抽象を融合した独自の美学", options: { bullet: true, breakLine: true } },
    { text: "屏風・蒔絵・陶芸・染織など多分野にまたがる総合芸術", options: { bullet: true } },
  ], {
    x: 0.6, y: 1.25, w: 4.8, h: 2.7,
    fontSize: 13, fontFace: "Calibri", color: C.darkText, paraSpaceAfter: 7
  });

  // 系譜フロー（右側）
  const artists = [
    { name: "本阿弥光悦", note: "書・蒔絵", color: C.gold },
    { name: "俵屋宗達", note: "絵画の創始", color: C.gold },
    { name: "尾形光琳", note: "100年後に私淑", color: C.crimson },
    { name: "尾形乾山", note: "光琳の弟・陶芸", color: C.crimson },
    { name: "酒井抱一", note: "江戸で再興", color: C.indigo },
    { name: "鈴木其一", note: "抱一の弟子", color: C.indigo },
  ];

  artists.forEach((a, i) => {
    const x = 5.7;
    const y = 1.22 + i * 0.69;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.0, h: 0.55,
      fill: { color: C.parchment }, line: { color: C.lightBrown }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 0.55,
      fill: { color: a.color }, line: { color: a.color }
    });
    s.addText(a.name, {
      x: x + 0.17, y, w: 2.2, h: 0.55,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.darkText, valign: "middle", margin: 0
    });
    s.addText(a.note, {
      x: x + 2.45, y, w: 1.45, h: 0.55,
      fontSize: 11, fontFace: "Calibri",
      color: a.color, align: "right", valign: "middle", margin: 0
    });
    // 矢印（最後以外）
    if (i < artists.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x: x + 2.0, y: y + 0.55, w: 0, h: 0.14,
        line: { color: C.lightBrown, width: 1 }
      });
    }
  });

  // 凡例
  [{ color: C.gold, label: "京琳派（桃山〜江戸初期）" },
   { color: C.crimson, label: "光琳派（元禄期）" },
   { color: C.indigo, label: "江戸琳派（文化・文政期）" }
  ].forEach((leg, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 4.08 + i * 0.42, w: 0.18, h: 0.28,
      fill: { color: leg.color }, line: { color: leg.color }
    });
    s.addText(leg.label, {
      x: 0.88, y: 4.08 + i * 0.42, w: 4.3, h: 0.28,
      fontSize: 11, fontFace: "Calibri",
      color: C.midBrown, valign: "middle", margin: 0
    });
  });
}

// ════════════════════════════════════════════════════════════
// 第1章: 本阿弥光悦 + 俵屋宗達（創始期）
// ════════════════════════════════════════════════════════════
sectionSlide("一", "本阿弥光悦 と 俵屋宗達",
  "Hon'ami Kōetsu ＆ Tawaraya Sōtatsu — 17世紀初頭",
  "創始期 ／ 京琳派の誕生", C.gold, C.dark);

// 光悦・宗達 概要
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "本阿弥光悦 と 俵屋宗達 — 概要", "書と絵画の奇跡のコラボレーション");

  const left = [
    { name: "本阿弥光悦（1558–1637）", color: C.gold,
      items: ["刀剣鑑定・書・蒔絵の三道の達人","徳川家康から鷹峯（たかがみね）の地を拝領","書・蒔絵・陶芸で琳派の美意識を確立","宗達に絵を描かせ書を入れる「コラボ」作品を多数制作"] },
    { name: "俵屋宗達（生没年不詳・17世紀前半）", color: C.crimson,
      items: ["扇絵師として出発した謎多き天才","「たらし込み」技法を創案・完成させた","金銀箔の上に絵具をたらして奥行きを生む","風神雷神図屏風・松島図屏風などの超大作を制作"] },
  ];

  left.forEach((block, bi) => {
    const y = bi === 0 ? 1.25 : 3.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.55, y, w: 0.07, h: 1.62,
      fill: { color: block.color }, line: { color: block.color }
    });
    s.addText(block.name, {
      x: 0.75, y: y + 0.05, w: 5.3, h: 0.4,
      fontSize: 15, bold: true, fontFace: "Georgia",
      color: block.color, margin: 0
    });
    block.items.forEach((item, ii) => {
      s.addText("・" + item, {
        x: 0.78, y: y + 0.5 + ii * 0.28, w: 5.2, h: 0.28,
        fontSize: 12, fontFace: "Calibri",
        color: C.darkText, margin: 0
      });
    });
  });

  // 右：たらし込み解説
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.3, y: 1.25, w: 3.38, h: 4.0,
    fill: { color: C.parchment }, line: { color: C.lightBrown },
    shadow: makeShadow()
  });
  s.addText("「たらし込み」技法", {
    x: 6.3, y: 1.25, w: 3.38, h: 0.5,
    fontSize: 14, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", valign: "middle", margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.3, y: 1.25, w: 3.38, h: 0.5,
    fill: { color: C.gold }, line: { color: C.gold }
  });
  s.addText("「たらし込み」技法", {
    x: 6.3, y: 1.25, w: 3.38, h: 0.5,
    fontSize: 14, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", valign: "middle", margin: 0
  });

  // たらし込みの視覚的説明（円形で表現）
  [[6.8, 2.0, 0.9, 0.7, "87CEEB", 50], [7.3, 2.3, 0.8, 0.6, "4682B4", 30], [7.8, 2.1, 0.7, 0.55, "1C3A6E", 10]].forEach(([x, y, w, h, c, t]) => {
    s.addShape(pres.shapes.OVAL, { x, y, w, h, fill: { color: c, transparency: t }, line: { color: "AAAAAA", width: 0.3 } });
  });

  s.addText([
    { text: "① 金箔・銀箔を下地に貼る", options: { breakLine: true } },
    { text: "② 絵具を置く（乾かす前に）", options: { breakLine: true } },
    { text: "③ 別の絵具や水を「たらす」", options: { breakLine: true } },
    { text: "④ 自然ににじんで広がる", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "→ 偶然性が生む独特の奥行き・柔らかさ", options: {} },
  ], {
    x: 6.45, y: 3.05, w: 3.1, h: 2.1,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, align: "left", margin: 0, paraSpaceAfter: 4
  });
}

// 光悦・宗達 作品スライド
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "俵屋宗達 — 代表作品", "金箔と「たらし込み」が生む壮大なスケール");

  // 上段：風神雷神（全幅）
  addArtwork(s, "sotatsu_fujin.png",
    "▲ 風神雷神図屏風（俵屋宗達 作・国宝）建仁寺蔵 — 17世紀前半。躍動する二神を金地に大胆に配置",
    0.55, 1.25, 9.1, 2.0, C.gold);

  // 下左：松島
  addArtwork(s, "sotatsu_matsushima.jpg",
    "▲ 松島図屏風 — フリーア美術館（米国）蔵",
    0.55, 3.5, 4.5, 1.75, C.gold);

  // 下右：光悦コラボ
  addArtwork(s, "koetsu_sotatsu.jpg",
    "▲ 四季草花図巻（宗達画・光悦書）— 宗達の絵に光悦が和歌を揮毫",
    5.3, 3.5, 4.35, 1.75, C.gold);
}

// ════════════════════════════════════════════════════════════
// 第2章: 尾形光琳
// ════════════════════════════════════════════════════════════
sectionSlide("二", "尾形 光琳", "Ogata Kōrin — 1658–1716",
  "元禄期の天才 ／ 琳派様式の完成", C.crimson, C.dark);

// 光琳 概要
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "尾形光琳 — 概要", "装飾性と抽象性を極めた元禄の天才");

  const points = [
    { t: "生涯",    b: "京都の呉服商・雁金屋の次男。遺産を使い果たすほどの放蕩生活の後、絵師として大成" },
    { t: "宗達への私淑", b: "宗達の作品を深く研究し、約100年後に独自のスタイルで琳派を再構築した" },
    { t: "様式の特徴①", b: "「型（かた）」の美学 — 自然のモチーフを大胆に単純化・記号化して表現する" },
    { t: "様式の特徴②", b: "金銀箔の大胆使用と、余白を生かした大画面構成。「光琳模様」として現代でも有名" },
    { t: "弟・乾山との協業", b: "弟の尾形乾山（陶芸家）が制作した器に光琳が絵を描くコラボ作品が多数ある" },
    { t: "三大傑作", b: "①燕子花図屏風（国宝）②紅白梅図屏風（国宝）③風神雷神図屏風（重要文化財）" },
  ];

  points.forEach((p, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.55 + col * 4.65, y = 1.25 + row * 1.28;
    addCard(s, x, y, 4.3, 1.1, p.t, p.b, C.crimson);
  });
}

// 光琳 作品①：燕子花図 + 紅白梅図
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "尾形光琳 — 代表作品①");

  // 上：燕子花図（2パネル並べる）
  addArtwork(s, "korin_iris1.jpg",
    "▲ 燕子花図屏風（左隻）— 尾形光琳 作・国宝 根津美術館蔵  18世紀初頭。金地に青紫の燕子花のみを描く極限の省略美",
    0.55, 1.25, 4.5, 1.9, C.crimson);
  addArtwork(s, "korin_iris2.jpg",
    "▲ 燕子花図屏風（右隻）— 同上",
    5.15, 1.25, 4.5, 1.9, C.crimson);

  // 下：紅白梅図（全幅）
  addArtwork(s, "korin_plum.jpg",
    "▲ 紅白梅図屏風（尾形光琳 作・国宝）MOA美術館蔵 — 18世紀前半。曲線の川と左右対称に配置された紅白の梅。光琳の最高傑作",
    0.55, 3.42, 9.1, 2.0, C.gold);
}

// 光琳 作品②：風神雷神（光琳版）+ 解説
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "尾形光琳 — 代表作品② ／ 宗達との比較");

  // 左：光琳の風神雷神
  addArtwork(s, "korin_fujin.jpg",
    "▲ 風神雷神図屏風（尾形光琳 作・重要文化財）東京国立博物館蔵 — 宗達作（建仁寺）を模しながら光琳流に再解釈",
    0.55, 1.25, 5.8, 2.6, C.crimson);

  // 右：比較解説
  s.addText("宗達 vs 光琳の違い", {
    x: 6.55, y: 1.25, w: 3.12, h: 0.42,
    fontSize: 14, bold: true, fontFace: "Georgia",
    color: C.crimson, align: "left", margin: 0
  });
  const diffs = [
    { label: "金箔", sot: "荒い箔継ぎ\n（ワイルド感）", kor: "均一で滑らか\n（整った美）" },
    { label: "神の体格", sot: "大きく力強い", kor: "やや小ぶり" },
    { label: "輪郭線", sot: "太く荒々しい", kor: "繊細で整然" },
  ];
  diffs.forEach((d, i) => {
    const y = 1.78 + i * 0.72;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.55, y, w: 3.12, h: 0.62, fill: { color: C.parchment }, line: { color: C.lightBrown } });
    s.addText(d.label, { x: 6.55, y, w: 0.7, h: 0.62, fontSize: 12, bold: true, fontFace: "Calibri", color: C.gold, align: "center", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.LINE, { x: 7.25, y: y + 0.1, w: 0, h: 0.42, line: { color: C.lightBrown, width: 0.5 } });
    s.addText("宗達：" + d.sot, { x: 7.3, y, w: 1.1, h: 0.62, fontSize: 10, fontFace: "Calibri", color: C.midBrown, align: "left", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.LINE, { x: 8.4, y: y + 0.1, w: 0, h: 0.42, line: { color: C.lightBrown, width: 0.5 } });
    s.addText("光琳：" + d.kor, { x: 8.45, y, w: 1.1, h: 0.62, fontSize: 10, fontFace: "Calibri", color: C.crimson, align: "left", valign: "middle", margin: 0 });
  });

  // 下：光琳様式の特徴まとめ
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 4.1, w: 9.12, h: 1.25,
    fill: { color: C.parchment }, line: { color: C.lightBrown }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 4.1, w: 0.07, h: 1.25,
    fill: { color: C.crimson }, line: { color: C.crimson }
  });
  s.addText("「光琳様式」のポイント", {
    x: 0.75, y: 4.15, w: 8.8, h: 0.38,
    fontSize: 13, bold: true, fontFace: "Calibri",
    color: C.crimson, margin: 0
  });
  s.addText("①モチーフの大胆な単純化・記号化　②金銀箔との融合　③左右対称・反復パターンの多用　④余白を最大限に生かした構成　⑤「型」への昇華", {
    x: 0.75, y: 4.55, w: 8.8, h: 0.7,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// 第3章: 酒井抱一 + 鈴木其一（江戸琳派）
// ════════════════════════════════════════════════════════════
sectionSlide("三", "酒井抱一 と 鈴木其一",
  "Sakai Hōitsu ＆ Suzuki Kiitsu — 18–19世紀",
  "江戸琳派 ／ 都市の優雅と季節の美", C.indigo, "0C111E");

// 江戸琳派 概要
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "酒井抱一 と 鈴木其一 — 概要", "江戸に琳派を再興させた師弟");

  const left = [
    { name: "酒井抱一（1761–1828）", color: C.indigo,
      items: ["姫路藩主・酒井家の次男という高貴な生まれ","31歳で出家し絵師の道に専念","光琳の100年忌に「光琳百回忌展覧会」を開催","「夏秋草図屏風」— 光琳の紅白梅図屏風の裏に描いた作品で有名","銀地に夏草・秋草を描く叙情的な江戸スタイルを確立"] },
    { name: "鈴木其一（1796–1858）", color: "2C6E8A",
      items: ["抱一の高弟。師のスタイルを継ぎながらさらに革新","「朝顔図屏風」など鮮やかな原色使いが特徴","抱一の柔らかさに対し、其一はよりダイナミックで現代的","メトロポリタン美術館など海外でも高く評価される"] },
  ];

  left.forEach((block, bi) => {
    const y = bi === 0 ? 1.25 : 3.2;
    const h = bi === 0 ? 1.78 : 1.52;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.55, y, w: 0.07, h,
      fill: { color: block.color }, line: { color: block.color }
    });
    s.addText(block.name, {
      x: 0.75, y: y + 0.04, w: 5.3, h: 0.4,
      fontSize: 14, bold: true, fontFace: "Georgia",
      color: block.color, margin: 0
    });
    block.items.forEach((item, ii) => {
      s.addText("・" + item, {
        x: 0.78, y: y + 0.48 + ii * 0.26, w: 5.2, h: 0.26,
        fontSize: 11.5, fontFace: "Calibri",
        color: C.darkText, margin: 0
      });
    });
  });

  // 右：京琳派 vs 江戸琳派
  s.addText("京琳派 vs 江戸琳派", {
    x: 6.3, y: 1.25, w: 3.38, h: 0.42,
    fontSize: 14, bold: true, fontFace: "Georgia",
    color: C.indigo, align: "center", margin: 0
  });
  const vs = [
    { k: "舞台", a: "京都（禁裏・寺社）", b: "江戸（武家・市民）" },
    { k: "地色", a: "金箔・金泥", b: "銀地・白地" },
    { k: "雰囲気", a: "豪壮・力強い", b: "繊細・叙情的" },
    { k: "モチーフ", a: "神・英雄・大木", b: "草花・虫・四季" },
    { k: "依頼主", a: "公家・寺院", b: "大名・富裕商人" },
  ];
  vs.forEach((row, i) => {
    const y = 1.77 + i * 0.58;
    const bg = i % 2 === 0 ? C.parchment : C.cream;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.3, y, w: 3.38, h: 0.52, fill: { color: bg }, line: { color: C.lightBrown, width: 0.5 } });
    s.addText(row.k, { x: 6.32, y, w: 0.7, h: 0.52, fontSize: 11, bold: true, fontFace: "Calibri", color: C.gold, align: "center", valign: "middle", margin: 0 });
    s.addText(row.a, { x: 7.05, y, w: 1.25, h: 0.52, fontSize: 10, fontFace: "Calibri", color: C.crimson, align: "center", valign: "middle", margin: 0 });
    s.addText(row.b, { x: 8.3, y, w: 1.25, h: 0.52, fontSize: 10, fontFace: "Calibri", color: C.indigo, align: "center", valign: "middle", margin: 0 });
  });
}

// 其一 作品
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "鈴木其一 — 代表作品 ／ 朝顔図屏風");

  // 其一の朝顔（全幅 大きく）
  addArtwork(s, "kiitsu_asagao.jpg",
    "▲ 朝顔図屏風（鈴木其一 作）メトロポリタン美術館蔵 — 19世紀。青紫の朝顔を大胆なアップで描いた其一の代表作",
    0.55, 1.25, 9.1, 2.9, C.indigo);

  // 下：解説カード3枚
  const cards = [
    { t: "大胆な拡大", b: "花を画面いっぱいに大きく描く「クローズアップ」手法。師・抱一の繊細さとは一線を画す" },
    { t: "色彩の革新", b: "青から紫のグラデーション。江戸琳派の銀地を捨て白地に変え、発色を最大化した" },
    { t: "師との継承", b: "「植物を主役にする」という琳派の伝統を受け継ぎながら、其一独自のダイナミズムを加えた" },
  ];
  cards.forEach((c, i) => {
    addCard(s, 0.55 + i * 3.08, 4.38, 2.9, 1.05, c.t, c.b, C.indigo);
  });
}

// ════════════════════════════════════════════════════════════
// 琳派の技法まとめ
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "琳派の技法・美意識まとめ");

  const techs = [
    { icon: "金", t: "金銀箔の使用", b: "屏風・料紙の下地に金箔・銀箔を貼り、光を反射させる豪華な空間を作り出す" },
    { icon: "た", t: "たらし込み", b: "乾く前の絵具に別の絵具や水を「たらして」にじませる宗達が創案した独自技法" },
    { icon: "型", t: "型の美学", b: "自然の形を大胆に単純化・抽象化する。「写実」ではなく「本質」を描き出す" },
    { icon: "余", t: "余白の美", b: "描かない部分（余白）が絵の一部として機能する。日本美術特有の空間感覚" },
    { icon: "繰", t: "繰り返しのリズム", b: "同じモチーフを反復することで、リズム感とパターン美を生み出す構成法" },
    { icon: "私", t: "私淑による継承", b: "師弟関係ではなく先人の作品を「自分で学ぶ」ことで流派が発展した特異な伝承方式" },
  ];

  techs.forEach((tech, i) => {
    const col = i % 3, row = Math.floor(i / 2);
    const x = 0.55 + col * 3.12, y = 1.25 + row * 1.95;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.9, h: 1.75,
      fill: { color: C.parchment }, line: { color: C.lightBrown },
      shadow: makeShadow()
    });
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.15, y: y + 0.2, w: 0.55, h: 0.55,
      fill: { color: C.gold }, line: { color: C.gold }
    });
    s.addText(tech.icon, {
      x: x + 0.15, y: y + 0.2, w: 0.55, h: 0.55,
      fontSize: 14, bold: true, fontFace: "Georgia",
      color: C.dark, align: "center", valign: "middle", margin: 0
    });
    s.addText(tech.t, {
      x: x + 0.8, y: y + 0.22, w: 1.95, h: 0.45,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.darkText, align: "left", valign: "middle", margin: 0
    });
    s.addText(tech.b, {
      x: x + 0.15, y: y + 0.85, w: 2.6, h: 0.82,
      fontSize: 11, fontFace: "Calibri",
      color: C.darkText, align: "left", valign: "top", margin: 0
    });
  });
}

// ════════════════════════════════════════════════════════════
// まとめスライド
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: C.dark };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.1,
    fill: { color: C.gold }, line: { color: C.gold }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.52, w: 10, h: 0.1,
    fill: { color: C.gold }, line: { color: C.gold }
  });

  s.addText("今日のまとめ", {
    x: 0.5, y: 0.38, w: 5.2, h: 0.52,
    fontSize: 24, bold: true, fontFace: "Georgia",
    color: C.gold, align: "left", margin: 0
  });

  const summary = [
    "琳派は師弟でなく「私淑」で受け継がれた流派",
    "宗達が「たらし込み」と金銀箔の大画面構成を創始",
    "光悦は書・蒔絵で美意識の枠組みを作った",
    "光琳が宗達を私淑し「型の美学」として完成させた",
    "燕子花・梅・風神雷神が琳派の三大モチーフ",
    "抱一・其一が江戸で琳派を銀地・繊細な草花へと進化させた",
  ];
  summary.forEach((item, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 1.05 + i * 0.68, w: 0.06, h: 0.46,
      fill: { color: C.gold }, line: { color: C.gold }
    });
    s.addText(item, {
      x: 0.68, y: 1.05 + i * 0.68, w: 5.5, h: 0.46,
      fontSize: 13, fontFace: "Calibri",
      color: "DDDDDD", align: "left", valign: "middle", margin: 0
    });
  });

  // 右：系譜サマリーボックス
  const boxes = [
    { name: "宗達・光悦", period: "17世紀前半", color: C.gold },
    { name: "尾形光琳", period: "17〜18世紀", color: C.crimson },
    { name: "尾形乾山", period: "17〜18世紀", color: C.crimson },
    { name: "酒井抱一", period: "18〜19世紀", color: C.indigo },
    { name: "鈴木其一", period: "19世紀", color: "2C6E8A" },
  ];
  boxes.forEach((b, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.4, y: 0.85 + i * 0.88, w: 3.2, h: 0.72,
      fill: { color: b.color }, line: { color: b.color }
    });
    s.addText(b.name, {
      x: 6.55, y: 0.88 + i * 0.88, w: 2.2, h: 0.38,
      fontSize: 15, bold: true, fontFace: "Georgia",
      color: C.white, align: "left", margin: 0
    });
    s.addText(b.period, {
      x: 6.55, y: 1.24 + i * 0.88, w: 2.2, h: 0.28,
      fontSize: 11, fontFace: "Calibri",
      color: "DDDDDD", align: "left", margin: 0
    });
    if (i < boxes.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x: 8.0, y: 1.57 + i * 0.88, w: 0, h: 0.16,
        line: { color: C.lightBrown, width: 1 }
      });
    }
  });

  s.addText("自然を見つめ、型に昇華させる — これが琳派の精神", {
    x: 0.5, y: 5.18, w: 9.0, h: 0.35,
    fontSize: 13, fontFace: "Calibri italic",
    color: C.gold, align: "center", margin: 0
  });
}

// ── 出力 ────────────────────────────────────────────────────
const outputPath = "C:\\Users\\shondo\\Desktop\\琳派の系譜.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("✅ 完成: " + outputPath);
}).catch(e => console.error("❌ エラー:", e));
