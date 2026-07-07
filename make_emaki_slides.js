const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = '四大絵巻入門';

// ── カラーパレット（和紙・朱・金）──────────────────────────
const C = {
  dark:      "1F1A15",   // 深い茶黒（タイトル背景）
  brown:     "3D2B1A",   // 茶色
  parchment: "F5EFE0",   // 和紙色（ライト背景）
  cream:     "FDFAF4",   // ほぼ白
  crimson:   "8B1A1A",   // 朱色（アクセント）
  gold:      "B8860B",   // 金色
  midBrown:  "7A5C3A",   // 中間色
  lightBrown:"C4A882",   // 薄い茶
  midGray:   "888888",
  darkText:  "2A1F0E",   // 本文色
  white:     "FFFFFF",
};

function makeShadow() {
  return { type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.20 };
}

// 共通：コンテンツスライドの和紙背景 + 左縦ライン
function setupContentSlide(s) {
  s.background = { color: C.cream };
  // 左アクセント
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.32, y: 0.45, w: 0.05, h: 4.75,
    fill: { color: C.crimson }, line: { color: C.crimson }
  });
}

function addSlideTitle(s, title, sub) {
  s.addText(title, {
    x: 0.58, y: 0.3, w: 9.1, h: 0.55,
    fontSize: 24, bold: true, fontFace: "Georgia",
    color: C.darkText, align: "left", margin: 0
  });
  if (sub) {
    s.addText(sub, {
      x: 0.58, y: 0.86, w: 9.1, h: 0.28,
      fontSize: 12, fontFace: "Calibri",
      color: C.midBrown, align: "left", margin: 0
    });
  }
  s.addShape(pres.shapes.LINE, {
    x: 0.58, y: sub ? 1.14 : 0.9, w: 9.0, h: 0,
    line: { color: C.lightBrown, width: 0.8 }
  });
}

// セクションヘッダースライド（各絵巻の冒頭）
function addSectionSlide(number, title, titleEn, period, collection, color) {
  let s = pres.addSlide();
  s.background = { color: C.dark };

  // 右側カラーパネル
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.2, y: 0, w: 2.8, h: 5.625,
    fill: { color: color }, line: { color: color }
  });

  // 番号
  s.addText(number, {
    x: 0.5, y: 0.35, w: 1.2, h: 1.2,
    fontSize: 72, bold: true, fontFace: "Georgia",
    color: color, align: "left", margin: 0
  });

  s.addText(title, {
    x: 0.5, y: 1.4, w: 6.5, h: 0.9,
    fontSize: 40, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });
  s.addText(titleEn, {
    x: 0.5, y: 2.35, w: 6.5, h: 0.45,
    fontSize: 18, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0
  });

  s.addShape(pres.shapes.LINE, {
    x: 0.5, y: 2.9, w: 6.5, h: 0,
    line: { color: color, width: 1.2 }
  });

  s.addText("制作年代：" + period, {
    x: 0.5, y: 3.05, w: 6.5, h: 0.38,
    fontSize: 14, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0
  });
  s.addText("所　　蔵：" + collection, {
    x: 0.5, y: 3.48, w: 6.5, h: 0.38,
    fontSize: 14, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0
  });

  // 右パネル内テキスト
  s.addText("国宝", {
    x: 7.2, y: 2.3, w: 2.8, h: 0.6,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", valign: "middle", margin: 0
  });
  s.addText("絵巻物", {
    x: 7.2, y: 3.0, w: 2.8, h: 0.45,
    fontSize: 14, fontFace: "Calibri",
    color: "DDDDDD", align: "center", margin: 0
  });
  return s;
}

// ── スライド1：タイトル ────────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.dark };

  // 上部ゴールドライン
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.12,
    fill: { color: C.gold }, line: { color: C.gold }
  });
  // 下部ゴールドライン
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.5, w: 10, h: 0.12,
    fill: { color: C.gold }, line: { color: C.gold }
  });

  // 右側縦分割（ゴールド）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.4, y: 0.12, w: 0.04, h: 5.38,
    fill: { color: C.gold }, line: { color: C.gold }
  });

  s.addText("日本の四大絵巻", {
    x: 0.5, y: 0.8, w: 6.8, h: 1.1,
    fontSize: 48, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });
  s.addText([
    { text: "源氏物語絵巻", options: { breakLine: true } },
    { text: "信貴山縁起絵巻", options: { breakLine: true } },
    { text: "鳥獣戯画", options: { breakLine: true } },
    { text: "伴大納言絵詞", options: {} },
  ], {
    x: 0.5, y: 1.95, w: 6.7, h: 2.3,
    fontSize: 22, fontFace: "Calibri",
    color: C.lightBrown, align: "left", margin: 0, paraSpaceAfter: 10
  });

  s.addShape(pres.shapes.LINE, {
    x: 0.5, y: 4.35, w: 6.7, h: 0,
    line: { color: C.gold, width: 1 }
  });
  s.addText("中学校 美術 ／ 絵巻物の世界", {
    x: 0.5, y: 4.5, w: 6.7, h: 0.4,
    fontSize: 14, fontFace: "Calibri",
    color: C.midBrown, align: "left", margin: 0
  });

  // 右側テキスト
  s.addText("平安〜鎌倉", {
    x: 7.55, y: 1.5, w: 2.3, h: 0.45,
    fontSize: 14, fontFace: "Calibri",
    color: C.gold, align: "center", margin: 0
  });
  s.addText("12世紀", {
    x: 7.55, y: 2.1, w: 2.3, h: 0.9,
    fontSize: 36, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", margin: 0
  });
  s.addText("国宝 全4作品", {
    x: 7.55, y: 3.1, w: 2.3, h: 0.4,
    fontSize: 13, fontFace: "Calibri",
    color: C.lightBrown, align: "center", margin: 0
  });
}

// ── スライド2：絵巻物とは ───────────────────────────────────
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "絵巻物（えまきもの）とは？");

  // 左：定義・特徴
  s.addText([
    { text: "紙や絹を横につないだ「巻物」形式の絵画", options: { bullet: true, breakLine: true } },
    { text: "右から左へ開きながらストーリーが展開する", options: { bullet: true, breakLine: true } },
    { text: "絵と詞書（ことばがき）が交互に配置される", options: { bullet: true, breakLine: true } },
    { text: "平安〜鎌倉時代（11〜13世紀）に最盛期を迎えた", options: { bullet: true, breakLine: true } },
    { text: "貴族・寺社が発注した「映像メディア」の役割", options: { bullet: true } },
  ], {
    x: 0.65, y: 1.25, w: 5.1, h: 2.8,
    fontSize: 14, fontFace: "Calibri", color: C.darkText, paraSpaceAfter: 8
  });

  // 右：三要素カード
  const elements = [
    { label: "絵（え）", desc: "物語の場面を\n色彩豊かに描く" },
    { label: "詞書（ことばがき）", desc: "場面の説明文\n漢字・仮名で記す" },
    { label: "料紙（りょうし）", desc: "和紙や絹に\n金銀で装飾する" },
  ];
  elements.forEach((el, i) => {
    const y = 1.22 + i * 1.35;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.1, y, w: 3.6, h: 1.15,
      fill: { color: C.parchment }, line: { color: C.lightBrown },
      shadow: makeShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.1, y, w: 0.07, h: 1.15,
      fill: { color: C.gold }, line: { color: C.gold }
    });
    s.addText(el.label, {
      x: 6.25, y: y + 0.1, w: 3.3, h: 0.4,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.darkText, align: "left", margin: 0
    });
    s.addText(el.desc, {
      x: 6.25, y: y + 0.52, w: 3.3, h: 0.55,
      fontSize: 12, fontFace: "Calibri",
      color: C.midBrown, align: "left", margin: 0
    });
  });

  // 下部：時代注記
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.58, y: 4.98, w: 8.6, h: 0.38,
    fill: { color: C.parchment }, line: { color: C.lightBrown }
  });
  s.addText("📜  四大絵巻はすべて12世紀制作の国宝。現在も博物館で大切に保管されている", {
    x: 0.7, y: 4.98, w: 8.4, h: 0.38,
    fontSize: 12, fontFace: "Calibri",
    color: C.midBrown, align: "left", valign: "middle", margin: 0
  });
}

// ── スライド3：比較一覧表 ──────────────────────────────────
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "四大絵巻 比較一覧");

  const headers = ["作品名", "制作年代", "主なテーマ", "画風・特徴", "所蔵"];
  const rows = [
    ["源氏物語絵巻", "12世紀前半", "王朝文学・恋愛", "引目鉤鼻・俯瞰（ふかん）構図", "徳川美術館・五島美術館"],
    ["信貴山縁起絵巻", "12世紀後半", "仏教説話・奇跡", "躍動感・連続場面描写", "朝護孫子寺（奈良）"],
    ["鳥獣戯画", "12〜13世紀", "動物擬人化・諷刺", "水墨・軽妙な筆線", "高山寺（京都）"],
    ["伴大納言絵詞", "12世紀後半", "政争・庶民の群像", "群衆の動き・感情表現", "出光美術館（東京）"],
  ];

  const colW = [2.1, 1.5, 2.0, 2.5, 1.5];
  const colX = [0.55, 2.7, 4.25, 6.3, 8.85];

  // ヘッダー行
  headers.forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: colX[i], y: 1.2, w: colW[i] - 0.05, h: 0.45,
      fill: { color: C.brown }, line: { color: C.brown }
    });
    s.addText(h, {
      x: colX[i], y: 1.2, w: colW[i] - 0.05, h: 0.45,
      fontSize: 12, bold: true, fontFace: "Calibri",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
  });

  // データ行
  const rowColors = [C.cream, C.parchment, C.cream, C.parchment];
  const sectionColors = ["8B1A1A", "5C3D1E", "2C3E50", "4A3728"];
  rows.forEach((row, r) => {
    row.forEach((cell, c) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x: colX[c], y: 1.68 + r * 0.88, w: colW[c] - 0.05, h: 0.82,
        fill: { color: rowColors[r] }, line: { color: C.lightBrown, width: 0.5 }
      });
      if (c === 0) {
        s.addShape(pres.shapes.RECTANGLE, {
          x: colX[c], y: 1.68 + r * 0.88, w: 0.07, h: 0.82,
          fill: { color: sectionColors[r] }, line: { color: sectionColors[r] }
        });
      }
      s.addText(cell, {
        x: colX[c] + (c === 0 ? 0.12 : 0.06), y: 1.7 + r * 0.88, w: colW[c] - 0.15, h: 0.78,
        fontSize: c === 0 ? 13 : 11, bold: c === 0, fontFace: "Calibri",
        color: C.darkText, align: "left", valign: "middle", margin: 0
      });
    });
  });
}

// ═══════════════════════════════════════════════════════════
// 【第1巻】源氏物語絵巻
// ═══════════════════════════════════════════════════════════

addSectionSlide("一", "源氏物語絵巻", "Genji Monogatari Emaki", "12世紀前半（平安時代末期）",
  "徳川美術館（名古屋）・五島美術館（東京）", "8B1A1A");

// 源氏 概要スライド
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "源氏物語絵巻 — 概要", "王朝文化の最高傑作");

  const points = [
    { title: "原作", body: "紫式部の小説『源氏物語』（11世紀初頭）を絵にしたもの" },
    { title: "現存数", body: "全54帖のうち、絵は19面・詞書は20段のみが現存" },
    { title: "技法", body: "「引目鉤鼻（ひきめかぎはな）」— 細い線で目・鼻を記号的に表現" },
    { title: "構図", body: "「吹抜屋台（ふきぬきやたい）」— 屋根を取り除いた俯瞰視点" },
    { title: "色彩", body: "金泥・銀泥・胡粉など豪華な顔料を多用した装飾的な画風" },
    { title: "意義", body: "日本最古の物語絵巻の一つ。王朝文学の「視覚化」の到達点" },
  ];

  points.forEach((p, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.55 + col * 4.65;
    const y = 1.25 + row * 1.28;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.3, h: 1.1,
      fill: { color: C.parchment }, line: { color: C.lightBrown }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.1,
      fill: { color: C.crimson }, line: { color: C.crimson }
    });
    s.addText(p.title, {
      x: x + 0.16, y: y + 0.08, w: 4.0, h: 0.36,
      fontSize: 13, bold: true, fontFace: "Calibri",
      color: C.crimson, align: "left", margin: 0
    });
    s.addText(p.body, {
      x: x + 0.16, y: y + 0.44, w: 4.0, h: 0.6,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkText, align: "left", margin: 0
    });
  });
}

// 源氏 図解スライド（実際の絵）
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "源氏物語絵巻 — 作品を見てみよう");

  // 左：画像
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\genji.jpg",
    x: 0.55, y: 1.25, w: 5.5, h: 3.8,
    sizing: { type: "contain", w: 5.5, h: 3.8 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 1.25, w: 5.5, h: 3.8,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });

  // 右：解説
  s.addText("「柏木（かしわぎ）」の場面", {
    x: 6.3, y: 1.3, w: 3.4, h: 0.45,
    fontSize: 15, bold: true, fontFace: "Georgia",
    color: C.crimson, align: "left", margin: 0
  });
  s.addText([
    { text: "注目ポイント", options: { bold: true, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "①  引目鉤鼻", options: { breakLine: true } },
    { text: "　細い横線＋カギ形の鼻で顔を表現", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "②  吹抜屋台", options: { breakLine: true } },
    { text: "　屋根を取り除き室内を俯瞰で見せる", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "③  平面的な表現", options: { breakLine: true } },
    { text: "　遠近法を使わず、身分の高い人物を大きく描く", options: {} },
  ], {
    x: 6.3, y: 1.82, w: 3.4, h: 3.2,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, align: "left", margin: 0, paraSpaceAfter: 3
  });
}

// ═══════════════════════════════════════════════════════════
// 【第2巻】信貴山縁起絵巻
// ═══════════════════════════════════════════════════════════

addSectionSlide("二", "信貴山縁起絵巻", "Shigisan Engi Emaki",
  "12世紀後半（平安時代末期）", "朝護孫子寺（奈良県）", "5C3D1E");

// 信貴山 概要
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "信貴山縁起絵巻 — 概要", "奇跡と笑いの仏教説話絵巻");

  const points = [
    { title: "内容", body: "信貴山の僧・命蓮（みょうれん）の霊験奇跡を3つの巻で描く" },
    { title: "三つの巻", body: "①飛倉巻（とびくらのまき）②延喜加持巻 ③尼公巻（あまぎみのまき）" },
    { title: "特徴①", body: "「異時同図法」— 同一場面に時間の異なるシーンを重ねて描く" },
    { title: "特徴②", body: "躍動感あふれる人物・動物の動きが生き生きと描かれている" },
    { title: "笑いの要素", body: "米俵が空を飛ぶ、人々が慌てふためく様子など、ユーモラスな場面が多い" },
    { title: "意義", body: "日本最古の「連続漫画的表現」。アニメーション技法の先駆けとも言われる" },
  ];

  points.forEach((p, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.55 + col * 4.65;
    const y = 1.25 + row * 1.28;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.3, h: 1.1,
      fill: { color: C.parchment }, line: { color: C.lightBrown }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.1,
      fill: { color: "5C3D1E" }, line: { color: "5C3D1E" }
    });
    s.addText(p.title, {
      x: x + 0.16, y: y + 0.08, w: 4.0, h: 0.36,
      fontSize: 13, bold: true, fontFace: "Calibri",
      color: "5C3D1E", align: "left", margin: 0
    });
    s.addText(p.body, {
      x: x + 0.16, y: y + 0.44, w: 4.0, h: 0.6,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkText, align: "left", margin: 0
    });
  });
}

// 信貴山 図解
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "信貴山縁起絵巻 — 作品を見てみよう");

  // 左上：「飛倉の巻」主要場面
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\shigisan1.jpg",
    x: 0.55, y: 1.28, w: 5.6, h: 2.2,
    sizing: { type: "contain", w: 5.6, h: 2.2 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 1.28, w: 5.6, h: 2.2,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });
  s.addText("▲ 飛倉の巻：米俵が空中を飛ぶ場面", {
    x: 0.55, y: 3.52, w: 5.6, h: 0.3,
    fontSize: 10, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });

  // 左下：人々が米を追う場面
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\shigisan2.jpg",
    x: 0.55, y: 3.9, w: 5.6, h: 1.5,
    sizing: { type: "contain", w: 5.6, h: 1.5 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 3.9, w: 5.6, h: 1.5,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });
  s.addText("▲ 人々が飛んでいく米俵を追う場面（異時同図法）", {
    x: 0.55, y: 5.42, w: 5.6, h: 0.18,
    fontSize: 10, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });

  // 右解説
  s.addText("「飛倉の巻（とびくらのまき）」", {
    x: 6.3, y: 1.3, w: 3.4, h: 0.45,
    fontSize: 14, bold: true, fontFace: "Georgia",
    color: "5C3D1E", align: "left", margin: 0
  });
  s.addText([
    { text: "あらすじ", options: { bold: true, breakLine: true } },
    { text: "命蓮の法力で、ある長者の米倉が\n空を飛んで信貴山まで運ばれてしまう。\n長者が取り返しを懇願する物語。", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "見どころ", options: { bold: true, breakLine: true } },
    { text: "✦ 空飛ぶ米俵の躍動感", options: { breakLine: true } },
    { text: "✦ 慌てふためく人々のリアルな表情", options: { breakLine: true } },
    { text: "✦ 異時同図法による場面転換", options: { breakLine: true } },
    { text: "✦ ユーモアと緊張感の絶妙なバランス", options: {} },
  ], {
    x: 6.3, y: 1.82, w: 3.4, h: 3.5,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, align: "left", margin: 0, paraSpaceAfter: 4
  });
}

// ═══════════════════════════════════════════════════════════
// 【第3巻】鳥獣戯画
// ═══════════════════════════════════════════════════════════

addSectionSlide("三", "鳥獣戯画", "Chōjū-jinbutsu-giga",
  "12〜13世紀（平安末〜鎌倉時代）", "高山寺（京都）", "2C3E50");

// 鳥獣戯画 概要
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "鳥獣戯画 — 概要", "動物が演じる人間社会の諷刺劇");

  const points = [
    { title: "構成", body: "甲（こう）乙（おつ）丙（へい）丁（てい）の4巻。甲巻が最も有名" },
    { title: "作者", body: "鳥羽僧正・覚猷（かくゆう）作と伝わるが、複数人の手による可能性が高い" },
    { title: "甲巻の内容", body: "カエル・ウサギ・サルなどが人間のように相撲・弓術・酒宴をする場面" },
    { title: "技法", body: "墨一色の線描のみ。色彩を一切使わないモノクロの表現" },
    { title: "漫画の起源", body: "コマ割りのない連続した動きの表現。「日本漫画の祖」とも呼ばれる" },
    { title: "意義", body: "仏教社会・貴族社会への諷刺と批判が込められているとも解釈される" },
  ];

  points.forEach((p, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.55 + col * 4.65;
    const y = 1.25 + row * 1.28;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.3, h: 1.1,
      fill: { color: C.parchment }, line: { color: C.lightBrown }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.1,
      fill: { color: "2C3E50" }, line: { color: "2C3E50" }
    });
    s.addText(p.title, {
      x: x + 0.16, y: y + 0.08, w: 4.0, h: 0.36,
      fontSize: 13, bold: true, fontFace: "Calibri",
      color: "2C3E50", align: "left", margin: 0
    });
    s.addText(p.body, {
      x: x + 0.16, y: y + 0.44, w: 4.0, h: 0.6,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkText, align: "left", margin: 0
    });
  });
}

// 鳥獣戯画 図解（2枚）
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "鳥獣戯画 — 作品を見てみよう（甲巻）");

  // 上段：有名なカエルとウサギ相撲場面
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\choju1.jpg",
    x: 0.55, y: 1.28, w: 9.1, h: 2.2,
    sizing: { type: "contain", w: 9.1, h: 2.2 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 1.28, w: 9.1, h: 2.2,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });
  s.addText("▲ カエルとウサギの相撲（甲巻 第2場面）— 人間さながらの相撲シーン。勝ち誇るカエルの表情に注目", {
    x: 0.55, y: 3.52, w: 9.1, h: 0.28,
    fontSize: 10, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });

  // 下段：弓術の場面
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\choju2.jpg",
    x: 0.55, y: 3.9, w: 4.4, h: 1.45,
    sizing: { type: "contain", w: 4.4, h: 1.45 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 3.9, w: 4.4, h: 1.45,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });
  s.addText("▲ 甲巻 第1場面（鹿・猿など）", {
    x: 0.55, y: 5.38, w: 4.4, h: 0.22,
    fontSize: 9, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });

  // 右下：見どころ
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 3.9, w: 4.45, h: 1.45,
    fill: { color: C.parchment }, line: { color: C.lightBrown }
  });
  s.addText([
    { text: "✦ 墨線だけで動きや表情を表現", options: { breakLine: true } },
    { text: "✦ 吹き出しなし・セリフなしでも伝わるユーモア", options: { breakLine: true } },
    { text: "✦ 動物たちは仏教僧・貴族・庶民のパロディ", options: { breakLine: true } },
    { text: "✦ 「日本最古の漫画」とも言われる所以", options: {} },
  ], {
    x: 5.3, y: 3.98, w: 4.25, h: 1.32,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, align: "left", valign: "top", margin: 0, paraSpaceAfter: 5
  });
}

// ═══════════════════════════════════════════════════════════
// 【第4巻】伴大納言絵詞
// ═══════════════════════════════════════════════════════════

addSectionSlide("四", "伴大納言絵詞", "Ban Dainagon Ekotoba",
  "12世紀後半（平安時代末期）", "出光美術館（東京）", "4A3728");

// 伴大納言 概要
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "伴大納言絵詞 — 概要", "政変を描いた群衆絵巻の傑作");

  const points = [
    { title: "史実の題材", body: "866年「応天門の変」—大納言・伴善男が放火の罪を着せられ流罪となった事件" },
    { title: "三巻構成", body: "①応天門炎上 ②犯人捜索・庶民の群衆 ③伴善男の逮捕・流罪" },
    { title: "群衆描写", body: "数十人の人物が一場面に登場。それぞれの表情・動作が精緻に描かれる" },
    { title: "感情表現", body: "火災を見る人々の恐怖・驚き・野次馬根性まで描き分けた心理描写" },
    { title: "技法", body: "細い流麗な線描と鮮やかな彩色を組み合わせた高度な技術" },
    { title: "意義", body: "個々の人物の心理を描いた「人間ドラマ」絵巻。庶民の姿を描いた先駆的作品" },
  ];

  points.forEach((p, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.55 + col * 4.65;
    const y = 1.25 + row * 1.28;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.3, h: 1.1,
      fill: { color: C.parchment }, line: { color: C.lightBrown }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.1,
      fill: { color: "4A3728" }, line: { color: "4A3728" }
    });
    s.addText(p.title, {
      x: x + 0.16, y: y + 0.08, w: 4.0, h: 0.36,
      fontSize: 13, bold: true, fontFace: "Calibri",
      color: "4A3728", align: "left", margin: 0
    });
    s.addText(p.body, {
      x: x + 0.16, y: y + 0.44, w: 4.0, h: 0.6,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkText, align: "left", margin: 0
    });
  });
}

// 伴大納言 図解
{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "伴大納言絵詞 — 作品を見てみよう");

  // 上：牛車と群衆
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\ban1.jpg",
    x: 0.55, y: 1.28, w: 9.1, h: 2.4,
    sizing: { type: "contain", w: 9.1, h: 2.4 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 1.28, w: 9.1, h: 2.4,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });
  s.addText("▲ 第2巻：牛車と混雑する群衆の場面。数十人の人物それぞれに異なる表情が描かれている", {
    x: 0.55, y: 3.72, w: 9.1, h: 0.28,
    fontSize: 10, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });

  // 下左：流罪の場面
  s.addImage({
    path: "C:\\Users\\shondo\\Desktop\\agent_project\\img_emaki\\ban2.jpg",
    x: 0.55, y: 4.08, w: 4.4, h: 1.35,
    sizing: { type: "contain", w: 4.4, h: 1.35 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 4.08, w: 4.4, h: 1.35,
    fill: { color: C.parchment, transparency: 100 },
    line: { color: C.lightBrown, width: 1 }
  });
  s.addText("▲ 第3巻：伴善男の流罪の場面", {
    x: 0.55, y: 5.45, w: 4.4, h: 0.18,
    fontSize: 9, fontFace: "Calibri italic",
    color: C.midBrown, align: "center", margin: 0
  });

  // 下右：見どころ
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 4.08, w: 4.45, h: 1.35,
    fill: { color: C.parchment }, line: { color: C.lightBrown }
  });
  s.addText([
    { text: "✦ 火事を見る人々の「七情」を描き分け", options: { breakLine: true } },
    { text: "✦ 庶民の日常生活が詳細に記録されている", options: { breakLine: true } },
    { text: "✦ 子供の喧嘩から政変を明かす巧みな構成", options: {} },
  ], {
    x: 5.3, y: 4.15, w: 4.25, h: 1.22,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkText, align: "left", valign: "middle", margin: 0, paraSpaceAfter: 5
  });
}

// ═══════════════════════════════════════════════════════════
// まとめ：画風比較
// ═══════════════════════════════════════════════════════════

{
  let s = pres.addSlide();
  setupContentSlide(s);
  addSlideTitle(s, "四大絵巻 — 画風・表現の比較", "それぞれの「個性」を読み取ろう");

  const comparisons = [
    {
      name: "源氏物語絵巻", color: "8B1A1A",
      keywords: ["装飾的・華麗", "引目鉤鼻", "俯瞰視点"],
      style: "感情を「型」で表現。王朝の静的な美を追求"
    },
    {
      name: "信貴山縁起絵巻", color: "5C3D1E",
      keywords: ["躍動感・ユーモア", "異時同図法", "動きの表現"],
      style: "時間の流れを連続場面で表現。コミカルな筆致"
    },
    {
      name: "鳥獣戯画", color: "2C3E50",
      keywords: ["水墨・諷刺", "動物擬人化", "線のみ"],
      style: "色彩を捨て、線の力だけで表情と動きを表現"
    },
    {
      name: "伴大納言絵詞", color: "4A3728",
      keywords: ["群衆・心理描写", "個人の感情", "写実的"],
      style: "多数の人物を描き分け、感情の多様性を表現"
    },
  ];

  comparisons.forEach((c, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.55 + col * 4.7;
    const y = 1.22 + row * 2.1;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.35, h: 1.9,
      fill: { color: C.parchment }, line: { color: C.lightBrown },
      shadow: makeShadow()
    });
    // 上部カラーバー
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.35, h: 0.45,
      fill: { color: c.color }, line: { color: c.color }
    });
    s.addText(c.name, {
      x: x + 0.12, y, w: 4.1, h: 0.45,
      fontSize: 15, bold: true, fontFace: "Georgia",
      color: C.white, align: "left", valign: "middle", margin: 0
    });

    // キーワードタグ
    c.keywords.forEach((kw, ki) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x + 0.1 + ki * 1.38, y: y + 0.52, w: 1.3, h: 0.3,
        fill: { color: c.color, transparency: 75 }, line: { color: c.color, width: 0.5 }
      });
      s.addText(kw, {
        x: x + 0.1 + ki * 1.38, y: y + 0.52, w: 1.3, h: 0.3,
        fontSize: 10, fontFace: "Calibri",
        color: c.color, align: "center", valign: "middle", margin: 0
      });
    });

    s.addText(c.style, {
      x: x + 0.1, y: y + 0.9, w: 4.1, h: 0.9,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkText, align: "left", valign: "middle", margin: 0
    });
  });
}

// ── 最終スライド：まとめ ──────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.dark };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.1,
    fill: { color: C.gold }, line: { color: C.gold }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.525, w: 10, h: 0.1,
    fill: { color: C.gold }, line: { color: C.gold }
  });

  s.addText("今日のまとめ", {
    x: 0.55, y: 0.4, w: 5.0, h: 0.55,
    fontSize: 24, bold: true, fontFace: "Georgia",
    color: C.gold, align: "left", margin: 0
  });

  const summary = [
    "絵巻物は右から左に開く「映像メディア」だった",
    "源氏物語絵巻 — 引目鉤鼻・吹抜屋台の王朝絵巻",
    "信貴山縁起 — 異時同図法で奇跡の躍動感を描く",
    "鳥獣戯画 — 墨線だけで諷刺と笑いを生む漫画の祖",
    "伴大納言絵詞 — 群衆の感情を描いた人間ドラマ絵巻",
    "4作品とも12世紀制作・国宝で、現代にも愛され続けている",
  ];

  summary.forEach((item, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.55, y: 1.05 + i * 0.7, w: 0.06, h: 0.48,
      fill: { color: C.crimson }, line: { color: C.crimson }
    });
    s.addText(item, {
      x: 0.75, y: 1.05 + i * 0.7, w: 5.3, h: 0.48,
      fontSize: 13, fontFace: "Calibri",
      color: "DDDDDD", align: "left", valign: "middle", margin: 0
    });
  });

  // 右側：4作品のシンボル
  const symbols = [
    { label: "源氏", color: "8B1A1A" },
    { label: "信貴山", color: "5C3D1E" },
    { label: "鳥獣戯画", color: "2C3E50" },
    { label: "伴大納言", color: "4A3728" },
  ];
  symbols.forEach((sym, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 6.5 + col * 1.7;
    const y = 1.0 + row * 2.1;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 1.5, h: 1.8,
      fill: { color: sym.color }, line: { color: sym.color }
    });
    s.addText("国宝", {
      x, y: y + 0.18, w: 1.5, h: 0.38,
      fontSize: 11, fontFace: "Calibri",
      color: "AAAAAA", align: "center", margin: 0
    });
    s.addText(sym.label, {
      x, y: y + 0.65, w: 1.5, h: 0.8,
      fontSize: 16, bold: true, fontFace: "Georgia",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
    s.addText("12世紀", {
      x, y: y + 1.38, w: 1.5, h: 0.3,
      fontSize: 10, fontFace: "Calibri",
      color: "CCCCCC", align: "center", margin: 0
    });
  });

  s.addText("絵巻物を通して、平安・鎌倉時代の人々の想いを感じ取ろう", {
    x: 0.55, y: 5.1, w: 9.0, h: 0.35,
    fontSize: 13, fontFace: "Calibri italic",
    color: C.gold, align: "center", margin: 0
  });
}

// ── 出力 ────────────────────────────────────────────────────
const outputPath = "C:\\Users\\shondo\\Desktop\\四大絵巻入門.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("✅ 完成: " + outputPath);
}).catch(e => console.error("❌ エラー:", e));
