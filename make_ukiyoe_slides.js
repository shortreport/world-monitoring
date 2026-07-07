const pptxgen = require("pptxgenjs");
const path = require("path");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = '浮世絵版画の世界';

const IMG = (f) => path.resolve(__dirname, "img_ukiyoe", f);

// ── カラーパレット ──────────────────────────────────────────
const C = {
  dark:     "0F0C08",   // 漆黒
  navy:     "1A2640",   // 藍（浮世絵の藍色）
  indigo:   "1B3A6B",   // 深藍
  prussian: "003153",   // プルシアンブルー
  red:      "8B1A1A",   // 朱
  gold:     "B8860B",   // 金
  copper:   "9B6B3A",   // 銅
  parchment:"F5EFE0",   // 和紙
  cream:    "FDFAF4",
  midBrown: "7A5C3A",
  lightBrown:"C4A882",
  slate:    "607080",
  darkText: "1C1408",
  white:    "FFFFFF",
};

function makeShadow() {
  return { type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.20 };
}

function setupLight(s) {
  s.background = { color: C.cream };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.3, y: 0.42, w: 0.05, h: 4.82,
    fill: { color: C.navy }, line: { color: C.navy }
  });
}

function slideTitle(s, title, sub) {
  s.addText(title, {
    x: 0.55, y: 0.28, w: 9.1, h: 0.56,
    fontSize: 24, bold: true, fontFace: "Georgia",
    color: C.darkText, align: "left", margin: 0
  });
  if (sub) s.addText(sub, {
    x: 0.55, y: 0.86, w: 9.1, h: 0.28,
    fontSize: 12, fontFace: "Calibri",
    color: C.midBrown, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 0.55, y: sub ? 1.15 : 0.92, w: 9.0, h: 0,
    line: { color: C.lightBrown, width: 0.8 }
  });
}

function addArtwork(s, imgFile, caption, x, y, w, h, borderColor) {
  s.addImage({ path: IMG(imgFile), x, y, w, h, sizing: { type: "contain", w, h } });
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: borderColor || C.lightBrown, width: 0.8 }
  });
  if (caption) s.addText(caption, {
    x, y: y + h + 0.04, w, h: 0.24,
    fontSize: 9, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });
}

function addCard(s, x, y, w, h, title, body, accent) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h, fill: { color: accent || C.navy }, line: { color: accent || C.navy } });
  if (title) s.addText(title, {
    x: x + 0.16, y: y + 0.1, w: w - 0.22, h: 0.36,
    fontSize: 13, bold: true, fontFace: "Calibri", color: accent || C.navy, align: "left", margin: 0
  });
  s.addText(body, {
    x: x + 0.16, y: y + (title ? 0.5 : 0.12), w: w - 0.22, h: h - (title ? 0.58 : 0.18),
    fontSize: 12, fontFace: "Calibri", color: C.darkText, align: "left", valign: "top", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド1: タイトル
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: C.dark };

  // 藍色ブロック（右半分）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.8, y: 0, w: 4.2, h: 5.625,
    fill: { color: C.navy }, line: { color: C.navy }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.78, y: 0, w: 0.04, h: 5.625,
    fill: { color: C.gold }, line: { color: C.gold }
  });

  // 左テキスト
  s.addText("浮世絵版画", {
    x: 0.5, y: 0.65, w: 5.1, h: 1.3,
    fontSize: 54, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });
  s.addText("の　世　界", {
    x: 0.5, y: 1.9, w: 5.1, h: 0.7,
    fontSize: 30, fontFace: "Georgia",
    color: C.lightBrown, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 0.5, y: 2.75, w: 5.0, h: 0,
    line: { color: C.gold, width: 1.2 }
  });
  s.addText([
    { text: "変遷・技法・著名作品と作者", options: { breakLine: true } },
    { text: "Ukiyo-e : History, Technique & Masters", options: {} },
  ], {
    x: 0.5, y: 2.9, w: 5.1, h: 0.95,
    fontSize: 16, fontFace: "Calibri", color: C.lightBrown, align: "left", margin: 0, paraSpaceAfter: 6
  });
  s.addText("中学校 美術 ／ 江戸の視覚文化", {
    x: 0.5, y: 4.72, w: 5.1, h: 0.38,
    fontSize: 13, fontFace: "Calibri", color: C.slate, align: "left", margin: 0
  });

  // 右ブロック内
  s.addText("17–19世紀", {
    x: 5.95, y: 0.9, w: 3.85, h: 0.42,
    fontSize: 14, fontFace: "Calibri", color: C.gold, align: "center", margin: 0
  });
  s.addText("江戸", {
    x: 5.95, y: 1.4, w: 3.85, h: 1.0,
    fontSize: 48, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", margin: 0
  });
  s.addText("時代", {
    x: 5.95, y: 2.45, w: 3.85, h: 0.55,
    fontSize: 24, fontFace: "Georgia", color: C.lightBrown, align: "center", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 6.2, y: 3.12, w: 3.35, h: 0,
    line: { color: C.gold, transparency: 40, width: 1 }
  });
  s.addText("浮世絵師　6名\n代表作　8点\n版画技法を完全解説", {
    x: 5.95, y: 3.25, w: 3.85, h: 1.5,
    fontSize: 14, fontFace: "Calibri", color: "CCCCCC", align: "center", margin: 0, paraSpaceAfter: 8
  });
}

// ════════════════════════════════════════════════════════════
// スライド2: 浮世絵とは
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "浮世絵（うきよえ）とは？");

  s.addText([
    { text: "17〜19世紀の江戸時代に栄えた大衆絵画・版画の様式", options: { bullet: true, breakLine: true } },
    { text: "「浮世（うきよ）」= 現世・今の世の楽しみや流行を描く", options: { bullet: true, breakLine: true } },
    { text: "歌舞伎役者・遊女・相撲取り・名所・風景など庶民が好む題材", options: { bullet: true, breakLine: true } },
    { text: "版画技術により大量生産が可能になり、庶民が買える「メディア」となった", options: { bullet: true, breakLine: true } },
    { text: "明治以降、ヨーロッパに輸出され「ジャポニスム」ブームを引き起こした", options: { bullet: true } },
  ], {
    x: 0.6, y: 1.25, w: 5.1, h: 2.8,
    fontSize: 13.5, fontFace: "Calibri", color: C.darkText, paraSpaceAfter: 7
  });

  // 右：ジャンル一覧カード
  const genres = [
    { label: "美人画", en: "bijin-ga", desc: "遊女・町娘の美を描く" },
    { label: "役者絵", en: "yakusha-e", desc: "歌舞伎俳優の劇中姿" },
    { label: "名所絵", en: "meisho-e", desc: "江戸・東海道の風景" },
    { label: "武者絵", en: "musha-e", desc: "武将・英雄の活躍" },
  ];
  genres.forEach((g, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 6.0 + col * 1.88, y = 1.25 + row * 1.85;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 1.7, h: 1.65,
      fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 1.7, h: 0.45,
      fill: { color: C.navy }, line: { color: C.navy }
    });
    s.addText(g.label, {
      x, y, w: 1.7, h: 0.45,
      fontSize: 16, bold: true, fontFace: "Georgia",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
    s.addText(g.en, {
      x, y: y + 0.5, w: 1.7, h: 0.3,
      fontSize: 10, fontFace: "Calibri", color: C.slate, align: "center", margin: 0
    });
    s.addText(g.desc, {
      x, y: y + 0.85, w: 1.7, h: 0.7,
      fontSize: 12, fontFace: "Calibri", color: C.darkText, align: "center", margin: 0
    });
  });

  // 下：ジャポニスム補足
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 5.0, w: 9.12, h: 0.38,
    fill: { color: C.parchment }, line: { color: C.lightBrown }
  });
  s.addText("🌍  ゴッホ・モネ・ドガら印象派の画家が浮世絵に影響を受けた。「ジャポニスム」という西洋美術の潮流が生まれた", {
    x: 0.7, y: 5.0, w: 8.9, h: 0.38,
    fontSize: 11.5, fontFace: "Calibri", color: C.midBrown, align: "left", valign: "middle", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド3: 変遷・時代別ポイント
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "浮世絵版画の変遷", "17世紀後半〜19世紀 ／ 4つの時代");

  const eras = [
    {
      period: "初期（17C後半）", color: C.copper,
      tech: "墨摺絵（すみずりえ）\n墨一色の版画",
      art: "菱川師宣が浮世絵の\n基本様式を確立",
      key: "菱川師宣"
    },
    {
      period: "中期①（18C前半）", color: "5A7A3A",
      tech: "丹絵・紅絵・漆絵\n手で彩色を加える",
      art: "鳥居清信・西村重長\n演劇・美人画の確立",
      key: "鳥居清信"
    },
    {
      period: "中期②（18C後半）", color: C.navy,
      tech: "錦絵（にしきえ）\n多色摺版画の完成",
      art: "春信・歌麿・写楽が\n活躍した黄金期",
      key: "鈴木春信"
    },
    {
      period: "後期（19C）", color: C.indigo,
      tech: "ベロ藍（プルシアンブルー）\n輸入顔料で鮮烈な青",
      art: "北斎・広重が風景画で\n浮世絵を世界へ",
      key: "葛飾北斎"
    },
  ];

  eras.forEach((era, i) => {
    const x = 0.55 + i * 2.35;
    // 縦バー
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.9, y: 1.25, w: 0.08, h: 4.0,
      fill: { color: era.color, transparency: 70 }, line: { color: era.color, transparency: 70 }
    });
    // 時代ラベル
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.25, w: 2.15, h: 0.5,
      fill: { color: era.color }, line: { color: era.color }
    });
    s.addText(era.period, {
      x, y: 1.25, w: 2.15, h: 0.5,
      fontSize: 12, bold: true, fontFace: "Calibri",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
    // 技法
    s.addText("技法", {
      x, y: 1.88, w: 2.15, h: 0.3,
      fontSize: 11, bold: true, fontFace: "Calibri",
      color: era.color, align: "left", margin: 0
    });
    s.addText(era.tech, {
      x, y: 2.2, w: 2.15, h: 0.7,
      fontSize: 11, fontFace: "Calibri", color: C.darkText, margin: 0
    });
    // 芸術
    s.addText("特徴", {
      x, y: 3.05, w: 2.15, h: 0.3,
      fontSize: 11, bold: true, fontFace: "Calibri",
      color: era.color, align: "left", margin: 0
    });
    s.addText(era.art, {
      x, y: 3.38, w: 2.15, h: 0.75,
      fontSize: 11, fontFace: "Calibri", color: C.darkText, margin: 0
    });
    // 代表
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.28, w: 2.15, h: 0.42,
      fill: { color: era.color, transparency: 80 }, line: { color: era.color }
    });
    s.addText("代表：" + era.key, {
      x, y: 4.28, w: 2.15, h: 0.42,
      fontSize: 11, fontFace: "Calibri", color: era.color,
      align: "center", valign: "middle", bold: true, margin: 0
    });
  });
}

// ════════════════════════════════════════════════════════════
// スライド4: 版画の作り方（製作工程）
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "浮世絵版画の作り方", "絵師・彫師・摺師の分業体制");

  // 工程フロー（6ステップ）
  const steps = [
    { num: "①", role: "絵師（えし）", title: "下絵を描く", desc: "筆と墨で版下絵（はんしたえ）を和紙に描く。色の指示も書き込む" },
    { num: "②", role: "彫師（ほりし）", title: "版木を彫る", desc: "山桜の板に下絵を貼り、輪郭を彫刻刀で彫る（墨版）" },
    { num: "③", role: "彫師", title: "色版を彫る", desc: "色ごとに板を分けて彫る。錦絵では10〜20版になることも" },
    { num: "④", role: "摺師（すりし）", title: "見当を合わせる", desc: "「見当（けんとう）」という目印で紙の位置を正確に合わせる" },
    { num: "⑤", role: "摺師", title: "色を摺る", desc: "墨版→薄い色→濃い色の順に重ねて摺る。絶妙なぼかしも職人技" },
    { num: "⑥", role: "版元（はんもと）", title: "出版・販売", desc: "版元（出版社）が企画・販売。江戸の書店で庶民が購入した" },
  ];

  steps.forEach((st, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.55 + col * 3.12, y = 1.25 + row * 2.0;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.9, h: 1.8,
      fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow()
    });
    // 番号バッジ
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.12, y: y + 0.16, w: 0.48, h: 0.48,
      fill: { color: C.navy }, line: { color: C.navy }
    });
    s.addText(st.num, {
      x: x + 0.12, y: y + 0.16, w: 0.48, h: 0.48,
      fontSize: 14, bold: true, fontFace: "Georgia",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
    s.addText(st.title, {
      x: x + 0.7, y: y + 0.2, w: 2.05, h: 0.38,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.darkText, align: "left", margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.7, y: y + 0.6, w: 1.5, h: 0.24,
      fill: { color: C.navy, transparency: 80 }, line: { color: C.navy, transparency: 60 }
    });
    s.addText(st.role, {
      x: x + 0.7, y: y + 0.6, w: 1.5, h: 0.24,
      fontSize: 9, fontFace: "Calibri", color: C.navy,
      align: "center", valign: "middle", margin: 0
    });
    s.addText(st.desc, {
      x: x + 0.12, y: y + 1.0, w: 2.66, h: 0.73,
      fontSize: 11, fontFace: "Calibri", color: C.darkText, margin: 0
    });
  });
}

// ════════════════════════════════════════════════════════════
// スライド5: 技法詳細（錦絵・ぼかし・空摺）
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "浮世絵の主な技法", "職人の技が生む繊細な表現");

  const techs = [
    { t: "錦絵（にしきえ）",  color: C.red,
      b: "1765年、鈴木春信が完成させた多色摺版画。10〜20色以上を重ね摺りし、錦織物のように美しい仕上がりになることから命名された" },
    { t: "ぼかし摺（摺込暈）", color: C.navy,
      b: "版木に色を塗る際、端を薄くぼかして摺る技法。空・水・着物のグラデーションを表現するのに用いる。職人の感覚が物を言う難技" },
    { t: "空摺（からずり）",   color: C.copper,
      b: "色を使わず、版木を押しつけるだけで紙に凹凸の浮き彫りを作る技法。着物の生地感・雪の白さを表現するのに使われる" },
    { t: "雲母摺（きらずり）", color: "4A7A6A",
      b: "雲母（マイカ）を混ぜた絵具で摺ることで、背景がキラキラと光る効果を出す技法。歌麿の美人大首絵の背景で多用された" },
    { t: "見当（けんとう）",   color: C.indigo,
      b: "版木に刻んだ「L字型」と「縦線」の目印。紙を置く位置を正確に合わせるためのもので、「見当をつける」という言葉の語源" },
    { t: "摺込（すりこみ）",   color: "6B3A7A",
      b: "彫った版木に絵具を刷毛で均一に塗り、その上に和紙を置いてバレン（馬簾）で摩擦して転写する基本的な摺りの技法" },
  ];

  techs.forEach((t, i) => {
    const col = i % 2, row = Math.floor(i / 3);
    const x = 0.55 + col * 4.65, y = 1.25 + Math.floor(i / 2) * 1.35;
    addCard(s, x, y, 4.3, 1.18, t.t, t.b, t.color);
  });
}

// ════════════════════════════════════════════════════════════
// スライド6: 菱川師宣 ＋ 鈴木春信
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "菱川師宣 と 鈴木春信 — 浮世絵の誕生と多色摺の完成");

  // 左：師宣の作品
  addArtwork(s, "moronobu_bijin.jpg",
    "▲ 見返り美人図（菱川師宣・17世紀後半）東京国立博物館蔵",
    0.55, 1.25, 2.5, 3.9, C.copper);

  // 右上：春信の作品
  addArtwork(s, "harunobu_asakusa.jpg",
    "▲ 浅草金龍山の夕暮（鈴木春信・1768頃）東京国立博物館蔵",
    3.3, 1.25, 2.7, 3.0, C.navy);

  // 右解説カード2枚
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.2, y: 1.25, w: 3.46, h: 1.82,
    fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow()
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.2, y: 1.25, w: 0.07, h: 1.82, fill: { color: C.copper }, line: { color: C.copper } });
  s.addText("菱川師宣（1618–1694）", {
    x: 6.35, y: 1.3, w: 3.2, h: 0.38, fontSize: 13, bold: true, fontFace: "Calibri", color: C.copper, margin: 0
  });
  s.addText("浮世絵の創始者。版画と肉筆画の両方で人気を博した。「見返り美人図」は振り返る女性の後ろ姿を描いた傑作。墨一色の墨摺絵の時代を代表する", {
    x: 6.35, y: 1.72, w: 3.2, h: 1.28, fontSize: 11.5, fontFace: "Calibri", color: C.darkText, margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.2, y: 3.25, w: 3.46, h: 1.82,
    fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow()
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.2, y: 3.25, w: 0.07, h: 1.82, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("鈴木春信（1725–1770）", {
    x: 6.35, y: 3.3, w: 3.2, h: 0.38, fontSize: 13, bold: true, fontFace: "Calibri", color: C.navy, margin: 0
  });
  s.addText("錦絵（多色摺版画）を1765年に完成させた。細身で可憐な女性像が特徴。儚げで詩的な美人画を得意とし、短命ながらも後世に大きな影響を与えた", {
    x: 6.35, y: 3.72, w: 3.2, h: 1.28, fontSize: 11.5, fontFace: "Calibri", color: C.darkText, margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド7: 歌麿 ＋ 写楽
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "喜多川歌麿 と 東洲斎写楽 — 美人と役者の大首絵");

  // 歌麿作品
  addArtwork(s, "utamaro_okita.jpg",
    "▲ 難波屋おきた（喜多川歌麿・1793頃）雲母摺・大首絵の代表作",
    0.55, 1.25, 2.5, 3.8, "4A7A6A");

  // 写楽作品
  addArtwork(s, "sharaku_oniji.jpg",
    "▲ 三代目大谷鬼次の奴江戸兵衛（東洲斎写楽・1794）浮世絵の役者絵の最高峰",
    3.22, 1.25, 2.5, 3.8, C.red);

  // 歌麿解説
  s.addShape(pres.shapes.RECTANGLE, { x: 5.9, y: 1.25, w: 3.77, h: 1.82, fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.9, y: 1.25, w: 0.07, h: 1.82, fill: { color: "4A7A6A" }, line: { color: "4A7A6A" } });
  s.addText("喜多川歌麿（1753–1806）", { x: 6.05, y: 1.3, w: 3.5, h: 0.38, fontSize: 13, bold: true, fontFace: "Calibri", color: "4A7A6A", margin: 0 });
  s.addText("「美人大首絵」で一世を風靡した美人画の第一人者。雲母摺の背景に胸から上をアップで描く独自のスタイルを確立。女性の表情・仕草の微妙な心理を描き出した", {
    x: 6.05, y: 1.72, w: 3.5, h: 1.28, fontSize: 11.5, fontFace: "Calibri", color: C.darkText, margin: 0
  });

  // 写楽解説
  s.addShape(pres.shapes.RECTANGLE, { x: 5.9, y: 3.25, w: 3.77, h: 1.82, fill: { color: C.parchment }, line: { color: C.lightBrown }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.9, y: 3.25, w: 0.07, h: 1.82, fill: { color: C.red }, line: { color: C.red } });
  s.addText("東洲斎写楽（生没年不詳・1794–95活躍）", { x: 6.05, y: 3.3, w: 3.5, h: 0.38, fontSize: 12, bold: true, fontFace: "Calibri", color: C.red, margin: 0 });
  s.addText("わずか10ヶ月で140点余を発表した謎の絵師。役者の個性を誇張し内面まで描き出す大首絵が特徴。正体は能役者・斎藤十郎兵衛という説が有力", {
    x: 6.05, y: 3.72, w: 3.5, h: 1.28, fontSize: 11.5, fontFace: "Calibri", color: C.darkText, margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド8: 葛飾北斎 ①（神奈川沖浪裏）
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "葛飾北斎 — 神奈川沖浪裏", "冨嶽三十六景より ／ 世界で最も有名な版画");

  // 大きく見せる（全幅）
  addArtwork(s, "hokusai_wave.jpg",
    "▲ 神奈川沖浪裏（葛飾北斎・1831頃）冨嶽三十六景・大英博物館蔵ほか — プルシアンブルーが生む鮮烈な藍の波、背景の富士山との対比が圧倒的",
    0.55, 1.25, 9.1, 3.45, C.prussian);

  // 下：3枚の解説カード
  const cards = [
    { t: "構図の革新", b: "波を前景に配し富士山を小さく描く大胆な逆転構図。自然の力と人間の小ささを対比させた" },
    { t: "ベロ藍の効果", b: "1820年代に輸入されたプルシアンブルー（ベロ藍）を初めて積極的に使用。鮮烈な青が「北斎ブルー」に" },
    { t: "世界への影響", b: "ドビュッシー「海」、ゴッホの模写など。現代のロゴ・絵文字にも引用される世界的アイコン" },
  ];
  cards.forEach((c, i) => {
    addCard(s, 0.55 + i * 3.08, 4.92, 2.9, 0.6, null, c.t + " — " + c.b, C.prussian);
  });
}

// ════════════════════════════════════════════════════════════
// スライド9: 葛飾北斎 ②（凱風快晴） ＋ 北斎のプロフィール
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "葛飾北斎 — 凱風快晴（赤富士）と画業", "冨嶽三十六景 / 90年の生涯で3万点以上");

  // 左：赤富士
  addArtwork(s, "hokusai_fuji.jpg",
    "▲ 凱風快晴（葛飾北斎・1831頃）冨嶽三十六景 — 晩夏の夜明けの富士山。赤く染まる霊峰と青い空の対比",
    0.55, 1.25, 5.5, 3.55, C.red);

  // 右：プロフィールカード
  s.addText("葛飾北斎（1760–1849）", {
    x: 6.3, y: 1.25, w: 3.37, h: 0.45,
    fontSize: 15, bold: true, fontFace: "Georgia", color: C.prussian, margin: 0
  });

  const profile = [
    { k: "生涯", v: "89歳まで活動。生涯で30回以上も改名した" },
    { k: "代表作", v: "冨嶽三十六景・北斎漫画・百物語" },
    { k: "晩成", v: "70歳を超えてから最高傑作を生んだ「大器晩成」の画家" },
    { k: "名言", v: "「70歳以前の作は取るに足らず」と自ら語った" },
    { k: "海外評価", v: "「世界の芸術家上位100人」に唯一の日本人として選出された" },
  ];
  profile.forEach((p, i) => {
    const y = 1.82 + i * 0.65;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.3, y, w: 3.37, h: 0.58, fill: { color: i % 2 === 0 ? C.parchment : C.cream }, line: { color: C.lightBrown, width: 0.5 } });
    s.addText(p.k, { x: 6.35, y, w: 0.75, h: 0.58, fontSize: 11, bold: true, fontFace: "Calibri", color: C.prussian, align: "center", valign: "middle", margin: 0 });
    s.addText(p.v, { x: 7.15, y, w: 2.42, h: 0.58, fontSize: 11, fontFace: "Calibri", color: C.darkText, valign: "middle", margin: 0 });
  });
}

// ════════════════════════════════════════════════════════════
// スライド10: 歌川広重（大はし夕立）
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "歌川広重 — 大はしあたけの夕立", "名所江戸百景 ／ ゴッホが模写した「雨の傑作」");

  // 画像（縦位置なので左寄り）
  addArtwork(s, "hiroshige_shower.jpg",
    "▲ 大はしあたけの夕立（歌川広重・1857）名所江戸百景 — 橋を渡る人々に突然の夕立。縦線の雨が舞台効果的な緊張感を生む",
    0.55, 1.25, 4.0, 3.95, C.indigo);

  // 右：解説＋比較
  s.addText("歌川広重（1797–1858）", {
    x: 4.75, y: 1.25, w: 4.92, h: 0.42,
    fontSize: 15, bold: true, fontFace: "Georgia", color: C.indigo, margin: 0
  });
  s.addText([
    { text: "東海道五十三次・名所江戸百景などの風景版画で名声を博した", options: { bullet: true, breakLine: true } },
    { text: "旅の情緒・自然の移ろい・季節感の表現に卓越した能力", options: { bullet: true, breakLine: true } },
    { text: "プルシアンブルーを「広重ブルー」と呼ばれるほど多用した", options: { bullet: true, breakLine: true } },
    { text: "ゴッホがこの作品を油絵で模写したことで世界的に有名になった", options: { bullet: true } },
  ], {
    x: 4.75, y: 1.75, w: 4.92, h: 2.0,
    fontSize: 12.5, fontFace: "Calibri", color: C.darkText, paraSpaceAfter: 6
  });

  // 北斎 vs 広重 比較
  s.addText("北斎 vs 広重", {
    x: 4.75, y: 3.88, w: 4.92, h: 0.4,
    fontSize: 14, bold: true, fontFace: "Georgia", color: C.indigo, margin: 0
  });
  const vs = [
    { k: "視点", a: "動的・劇的な瞬間", b: "叙情的・旅情感" },
    { k: "構図", a: "斜線・対角線", b: "縦線・細雨・靄" },
    { k: "人物", a: "小さい（添景）", b: "旅人・市井の人" },
  ];
  vs.forEach((row, i) => {
    const y = 4.38 + i * 0.38;
    s.addShape(pres.shapes.RECTANGLE, { x: 4.75, y, w: 4.92, h: 0.34, fill: { color: i % 2 === 0 ? C.parchment : C.cream }, line: { color: C.lightBrown, width: 0.4 } });
    s.addText(row.k, { x: 4.77, y, w: 0.65, h: 0.34, fontSize: 10, bold: true, fontFace: "Calibri", color: C.gold, align: "center", valign: "middle", margin: 0 });
    s.addText("北斎：" + row.a, { x: 5.45, y, w: 1.95, h: 0.34, fontSize: 10, fontFace: "Calibri", color: C.prussian, valign: "middle", margin: 0 });
    s.addText("広重：" + row.b, { x: 7.45, y, w: 2.1, h: 0.34, fontSize: 10, fontFace: "Calibri", color: C.indigo, valign: "middle", margin: 0 });
  });
}

// ════════════════════════════════════════════════════════════
// スライド11: 西洋への影響（ジャポニスム）
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  setupLight(s);
  slideTitle(s, "浮世絵が世界を変えた — ジャポニスム", "西洋近代美術への影響");

  const influences = [
    { artist: "フィンセント・ファン・ゴッホ", desc: "広重の「大はし夕立」「亀戸梅屋鋪」を油絵で模写。浮世絵の輪郭線・平面性を印象派の筆致に融合させた", work: "「タンギー爺さん」の背景にも浮世絵が描かれている" },
    { artist: "クロード・モネ", desc: "「睡蓮」シリーズの構図・色使いに浮世絵の影響。自宅の「日本橋」（ジヴェルニー）を設計。250点以上の浮世絵を収集", work: "浮世絵の「余白」と「クローズアップ」が革命的だった" },
    { artist: "エドガー・ドガ", desc: "「踊り子」シリーズの大胆なトリミングと斜め構図は浮世絵の「見切り」技法から着想。上から見下ろす俯瞰視点も浮世絵譲り", work: "パリ万博（1867年）で大量の浮世絵が紹介されたことが転機" },
  ];

  influences.forEach((inf, i) => {
    const y = 1.25 + i * 1.38;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 9.12, h: 1.22, fill: { color: C.parchment }, line: { color: C.lightBrown } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 0.07, h: 1.22, fill: { color: C.navy }, line: { color: C.navy } });
    s.addText(inf.artist, { x: 0.72, y: y + 0.08, w: 3.0, h: 0.38, fontSize: 13, bold: true, fontFace: "Calibri", color: C.navy, margin: 0 });
    s.addText(inf.desc, { x: 0.72, y: y + 0.48, w: 4.8, h: 0.65, fontSize: 11.5, fontFace: "Calibri", color: C.darkText, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 5.7, y: y + 0.08, w: 3.85, h: 1.05, fill: { color: C.cream }, line: { color: C.lightBrown, width: 0.4 } });
    s.addText(inf.work, { x: 5.8, y: y + 0.12, w: 3.65, h: 0.95, fontSize: 11, fontFace: "Calibri italic", color: C.midBrown, align: "left", valign: "middle", margin: 0 });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 5.05, w: 9.12, h: 0.35, fill: { color: C.navy, transparency: 80 }, line: { color: C.navy, transparency: 50 } });
  s.addText("💡 浮世絵は明治初期まで「包み紙」として使われ、それが海外へ流出したことで世界的ブームが起きた", {
    x: 0.7, y: 5.05, w: 8.9, h: 0.35, fontSize: 11.5, fontFace: "Calibri", color: C.navy, align: "left", valign: "middle", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド12: まとめ
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: C.dark };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.1, fill: { color: C.gold }, line: { color: C.gold } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.52, w: 10, h: 0.1, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("今日のまとめ", {
    x: 0.5, y: 0.38, w: 5.2, h: 0.52,
    fontSize: 24, bold: true, fontFace: "Georgia", color: C.gold, margin: 0
  });

  const summary = [
    "浮世絵は江戸時代の大衆的な「視覚メディア」だった",
    "墨摺絵→手彩色→錦絵（多色摺）へと技術が進化した",
    "絵師・彫師・摺師・版元の分業体制で大量生産を実現",
    "歌麿＝美人画、写楽＝役者絵、北斎・広重＝風景画が代表",
    "ベロ藍（プルシアンブルー）が後期浮世絵の色調を一変させた",
    "ジャポニスムとして西洋近代美術（印象派）に多大な影響を与えた",
  ];
  summary.forEach((item, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.05 + i * 0.68, w: 0.06, h: 0.46, fill: { color: C.gold }, line: { color: C.gold } });
    s.addText(item, {
      x: 0.68, y: 1.05 + i * 0.68, w: 5.5, h: 0.46,
      fontSize: 13, fontFace: "Calibri", color: "DDDDDD", align: "left", valign: "middle", margin: 0
    });
  });

  // 右：絵師サマリー
  const artists = [
    { name: "菱川師宣", tag: "創始者", color: C.copper },
    { name: "鈴木春信", tag: "錦絵の父", color: "5A7A3A" },
    { name: "喜多川歌麿", tag: "美人画", color: "4A7A6A" },
    { name: "東洲斎写楽", tag: "役者絵", color: C.red },
    { name: "葛飾北斎", tag: "風景・世界へ", color: C.prussian },
    { name: "歌川広重", tag: "旅情の詩人", color: C.indigo },
  ];
  artists.forEach((a, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 6.3 + col * 1.75, y = 0.85 + row * 1.55;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 1.55, h: 1.3, fill: { color: a.color }, line: { color: a.color } });
    s.addText(a.name, { x, y: y + 0.18, w: 1.55, h: 0.55, fontSize: 14, bold: true, fontFace: "Georgia", color: C.white, align: "center", margin: 0 });
    s.addText(a.tag, { x, y: y + 0.75, w: 1.55, h: 0.38, fontSize: 11, fontFace: "Calibri", color: "DDDDDD", align: "center", margin: 0 });
  });

  s.addText("「今」を描くことが、時代を超える美を生んだ", {
    x: 0.5, y: 5.16, w: 9.0, h: 0.35,
    fontSize: 13, fontFace: "Calibri italic", color: C.gold, align: "center", margin: 0
  });
}

// ── 出力 ──────────────────────────────────────────────────
const outputPath = "C:\\Users\\shondo\\Desktop\\浮世絵版画の世界.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("✅ 完成: " + outputPath);
}).catch(e => console.error("❌ エラー:", e));
