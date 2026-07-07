const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = '水墨画入門';

// Color palette — sumi-e inspired
const C = {
  black:    "1A1A1A",  // ほぼ黒（背景用）
  ink:      "2C2C2C",  // 墨色
  darkGray: "4A4A4A",
  midGray:  "888888",
  lightGray:"D8D8D8",
  paleGray: "F0F0F0",
  white:    "FFFFFF",
  seal:     "8B1A1A",  // 印鑑の赤
  sepia:    "A08060",  // 和紙っぽい黄褐色
};

// ── ヘルパー ──────────────────────────────────────────────────
function makeShadow() {
  return { type: "outer", blur: 5, offset: 2, angle: 135, color: "000000", opacity: 0.18 };
}

// 左側に縦の墨ストライプアクセントを追加（コンテンツスライド共通モチーフ）
function addInkAccent(slide) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 0.5, w: 0.05, h: 4.6,
    fill: { color: C.ink }, line: { color: C.ink }
  });
}

// タイトルバーなしのシンプルスライドタイトル
function addSlideTitle(slide, title, y = 0.32) {
  slide.addText(title, {
    x: 0.6, y, w: 9.2, h: 0.55,
    fontSize: 26, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  // 薄いセパレータ
  slide.addShape(pres.shapes.LINE, {
    x: 0.6, y: y + 0.6, w: 8.8, h: 0,
    line: { color: C.lightGray, width: 1 }
  });
}

// ── スライド1: タイトル ──────────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.black };

  // 右側に薄い墨wash矩形
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.5, y: 0, w: 3.5, h: 5.625,
    fill: { color: "252525" }, line: { color: "252525" }
  });

  // 印鑑風アクセント（右下）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.8, y: 4.6, w: 0.9, h: 0.7,
    fill: { color: C.seal }, line: { color: C.seal }
  });
  s.addText("入門", {
    x: 8.8, y: 4.6, w: 0.9, h: 0.7,
    fontSize: 16, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", valign: "middle", margin: 0
  });

  s.addText("水墨画", {
    x: 0.7, y: 1.1, w: 6.0, h: 1.4,
    fontSize: 64, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });
  s.addText("入門", {
    x: 0.7, y: 2.4, w: 6.0, h: 1.0,
    fontSize: 48, bold: false, fontFace: "Georgia",
    color: C.lightGray, align: "left", margin: 0
  });
  s.addText("〜筆と墨で描く日本の美〜", {
    x: 0.7, y: 3.35, w: 6.0, h: 0.5,
    fontSize: 18, fontFace: "Georgia",
    color: C.midGray, align: "left", margin: 0
  });
  s.addText("中学校 美術", {
    x: 0.7, y: 4.8, w: 4.0, h: 0.4,
    fontSize: 13, fontFace: "Calibri",
    color: "606060", align: "left", margin: 0
  });
}

// ── スライド2: 水墨画とは？ ───────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "水墨画とは？");

  // 左コンテンツ
  s.addText([
    { text: "墨（すみ）と水だけで描く絵画", options: { bullet: true, breakLine: true } },
    { text: "中国から伝わり、日本で独自の発展を遂げた", options: { bullet: true, breakLine: true } },
    { text: "代表的な画家：雪舟（室町時代）", options: { bullet: true, breakLine: true } },
    { text: "余白（ネガティブスペース）を活かす美学", options: { bullet: true, breakLine: true } },
    { text: "色彩を使わないことで想像力を引き出す", options: { bullet: true } },
  ], {
    x: 0.7, y: 1.15, w: 5.0, h: 3.8,
    fontSize: 16, fontFace: "Calibri", color: C.ink,
    paraSpaceAfter: 8
  });

  // 右：キーワードカード
  const keywords = [
    { label: "墨", sub: "sumi" },
    { label: "筆", sub: "fude" },
    { label: "硯", sub: "suzuri" },
    { label: "余白", sub: "yohaku" },
  ];
  keywords.forEach((kw, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 6.1 + col * 1.85;
    const y = 1.2 + row * 1.9;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 1.6, h: 1.5,
      fill: { color: C.paleGray }, line: { color: C.lightGray },
      shadow: makeShadow()
    });
    s.addText(kw.label, {
      x, y: y + 0.1, w: 1.6, h: 0.9,
      fontSize: 36, bold: true, fontFace: "Georgia",
      color: C.ink, align: "center", valign: "middle", margin: 0
    });
    s.addText(kw.sub, {
      x, y: y + 1.05, w: 1.6, h: 0.35,
      fontSize: 11, fontFace: "Calibri",
      color: C.midGray, align: "center", margin: 0
    });
  });
}

// ── スライド3: 必要な道具（一覧） ────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "必要な道具");

  const tools = [
    { name: "筆（ふで）",     desc: "大・中・小の3本セットが基本。毛の種類により表現が変わる" },
    { name: "墨（すみ）",     desc: "固形墨と墨液がある。初心者には墨液が便利" },
    { name: "硯（すずり）",   desc: "固形墨を磨って墨液を作る石の道具" },
    { name: "和紙（わし）",   desc: "にじみやすい「半紙」が練習に最適" },
    { name: "下敷き",         desc: "和紙がずれないよう敷く。フェルト製が一般的" },
    { name: "水差し・水入れ", desc: "墨の濃さを調整するための水" },
  ];

  tools.forEach((t, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.7 + col * 4.6;
    const y = 1.2 + row * 1.35;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.2, h: 1.2,
      fill: { color: C.paleGray }, line: { color: C.lightGray }
    });
    // 左アクセントバー
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.2,
      fill: { color: C.ink }, line: { color: C.ink }
    });
    s.addText(t.name, {
      x: x + 0.15, y: y + 0.1, w: 3.9, h: 0.38,
      fontSize: 15, bold: true, fontFace: "Calibri",
      color: C.ink, align: "left", margin: 0
    });
    s.addText(t.desc, {
      x: x + 0.15, y: y + 0.5, w: 3.9, h: 0.62,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkGray, align: "left", margin: 0
    });
  });
}

// ── スライド4: 硯と墨の使い方 ────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "硯と墨の使い方");

  // 左：手順
  const steps = [
    "硯の「海」（くぼみ）に少量の水を入れる",
    "固形墨を立て、ゆっくり円を描くように磨る",
    "磨りすぎず、適度な濃さになったら止める",
    "筆で濃淡を調整しながら使う",
    "使用後は硯をよく洗い、乾かす",
  ];
  steps.forEach((step, i) => {
    const y = 1.2 + i * 0.75;
    s.addShape(pres.shapes.OVAL, {
      x: 0.7, y: y + 0.02, w: 0.38, h: 0.38,
      fill: { color: C.ink }, line: { color: C.ink }
    });
    s.addText(String(i + 1), {
      x: 0.7, y: y + 0.02, w: 0.38, h: 0.38,
      fontSize: 13, bold: true, fontFace: "Calibri",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
    s.addText(step, {
      x: 1.2, y, w: 4.8, h: 0.55,
      fontSize: 14, fontFace: "Calibri",
      color: C.ink, align: "left", valign: "middle", margin: 0
    });
  });

  // 右：ポイントBox
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.4, y: 1.15, w: 3.3, h: 4.1,
    fill: { color: "F8F4EE" }, line: { color: C.sepia }
  });
  s.addText("ポイント", {
    x: 6.4, y: 1.15, w: 3.3, h: 0.45,
    fontSize: 14, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", valign: "middle", margin: 0,
    fill: { color: C.sepia }
  });
  s.addText([
    { text: "✦ 墨を磨る速さ = 気持ちを整える時間", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "✦ 「濃い墨」= 少量の水で磨る", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "✦ 「薄い墨」= 水を多めに混ぜる", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "✦ 墨液を使う場合も、水で薄めて濃淡を出す", options: { breakLine: true } },
  ], {
    x: 6.55, y: 1.7, w: 3.0, h: 3.4,
    fontSize: 12, fontFace: "Calibri",
    color: C.ink, align: "left", valign: "top", margin: 0,
    paraSpaceAfter: 4
  });
}

// ── スライド5: 筆の種類 ──────────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "筆の種類と特徴");

  const brushes = [
    { name: "大筆（だいふで）", color: "2C2C2C", desc: "太い線・広い面・背景に\n毛が長く弾力がある" },
    { name: "中筆（ちゅうふで）", color: "4A4A4A", desc: "木や竹の幹など中程度の表現\n最も汎用的な筆" },
    { name: "小筆（こふで）", color: "707070", desc: "細かい線・葉脈・落款に\n先が鋭くコントロールしやすい" },
  ];

  brushes.forEach((b, i) => {
    const x = 0.7 + i * 3.1;

    // 筆の絵（シンプルな図形で表現）
    const bx = x + 1.05;
    // 穂先
    s.addShape(pres.shapes.OVAL, {
      x: bx - 0.06, y: 1.15, w: 0.12 + i * 0.06, h: 0.5 + i * 0.2,
      fill: { color: b.color }, line: { color: b.color }
    });
    // 軸
    s.addShape(pres.shapes.RECTANGLE, {
      x: bx - 0.03, y: 1.65 + i * 0.2, w: 0.06, h: 1.5,
      fill: { color: "8B6914" }, line: { color: "8B6914" }
    });

    s.addText(b.name, {
      x, y: 3.3, w: 2.8, h: 0.45,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.ink, align: "center", margin: 0
    });
    s.addText(b.desc, {
      x, y: 3.78, w: 2.8, h: 1.5,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkGray, align: "center", margin: 0
    });
  });

  // 下部ヒント
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.65, y: 5.0, w: 8.7, h: 0.4,
    fill: { color: C.paleGray }, line: { color: C.lightGray }
  });
  s.addText("💡 筆は使う前に水でよく湿らせ、使った後はすぐに洗って穂先を整えておこう", {
    x: 0.8, y: 5.0, w: 8.4, h: 0.4,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkGray, align: "left", valign: "middle", margin: 0
  });
}

// ── スライド6: 紙（和紙）について ────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "紙（和紙）について");

  // 2カラム
  s.addText("練習用：半紙（はんし）", {
    x: 0.7, y: 1.1, w: 4.3, h: 0.45,
    fontSize: 17, bold: true, fontFace: "Calibri",
    color: C.ink, align: "left", margin: 0
  });
  s.addText([
    { text: "最も手軽で安価な和紙", options: { bullet: true, breakLine: true } },
    { text: "水分を吸収しやすく「にじみ」が出やすい", options: { bullet: true, breakLine: true } },
    { text: "書道の練習にも使われる", options: { bullet: true, breakLine: true } },
    { text: "薄いため下敷きが必須", options: { bullet: true } },
  ], {
    x: 0.7, y: 1.6, w: 4.3, h: 2.0,
    fontSize: 14, fontFace: "Calibri",
    color: C.ink, paraSpaceAfter: 6
  });

  s.addText("本画用：画仙紙（がせんし）", {
    x: 0.7, y: 3.55, w: 4.3, h: 0.45,
    fontSize: 17, bold: true, fontFace: "Calibri",
    color: C.ink, align: "left", margin: 0
  });
  s.addText([
    { text: "厚みがあり強度が高い", options: { bullet: true, breakLine: true } },
    { text: "にじみが少なく繊細な表現が可能", options: { bullet: true, breakLine: true } },
    { text: "作品制作に適している", options: { bullet: true } },
  ], {
    x: 0.7, y: 4.02, w: 4.3, h: 1.4,
    fontSize: 14, fontFace: "Calibri",
    color: C.ink, paraSpaceAfter: 6
  });

  // 右：にじみの仕組み
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.4, y: 1.1, w: 4.2, h: 4.2,
    fill: { color: "F8F4EE" }, line: { color: C.lightGray }
  });
  s.addText("にじみの仕組み", {
    x: 5.55, y: 1.2, w: 3.9, h: 0.4,
    fontSize: 15, bold: true, fontFace: "Georgia",
    color: C.ink, align: "center", margin: 0
  });

  // 視覚的にじみ表現（同心円）
  [1.0, 0.7, 0.4].forEach((r, i) => {
    const alpha = [20, 40, 70][i];
    const gray = ["CCCCCC", "888888", "2C2C2C"][i];
    s.addShape(pres.shapes.OVAL, {
      x: 7.5 - r, y: 2.5 - r * 0.9,
      w: r * 2, h: r * 1.8,
      fill: { color: gray, transparency: alpha },
      line: { color: "AAAAAA", width: 0.5 }
    });
  });
  s.addText([
    { text: "和紙の繊維が毛細管現象で\n墨を広げる = にじみ", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "水分量が多いほど\nにじみが大きくなる", options: {} },
  ], {
    x: 5.55, y: 4.0, w: 3.9, h: 1.2,
    fontSize: 12, fontFace: "Calibri",
    color: C.darkGray, align: "center", margin: 0, paraSpaceAfter: 4
  });
}

// ── スライド7: 墨の濃淡（墨色の5段階）──────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "墨の濃淡（ぼくしょく）— 5つの調子");

  const shades = [
    { label: "焦墨", sub: "ショウボク", color: "0A0A0A", desc: "最も濃い\n墨そのまま" },
    { label: "濃墨", sub: "ノウボク",  color: "2C2C2C", desc: "濃い墨\n輪郭・主線に" },
    { label: "中墨", sub: "チュウボク", color: "636363", desc: "中間の濃さ\n幹・岩などに" },
    { label: "淡墨", sub: "タンボク",  color: "A0A0A0", desc: "薄い墨\n遠景・霧に" },
    { label: "清墨", sub: "セイボク",  color: "D8D8D8", desc: "最も薄い\nほのかな表現" },
  ];

  shades.forEach((sh, i) => {
    const x = 0.7 + i * 1.72;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.2, w: 1.5, h: 2.2,
      fill: { color: sh.color }, line: { color: "BBBBBB" },
      shadow: makeShadow()
    });
    s.addText(sh.label, {
      x, y: 3.5, w: 1.5, h: 0.45,
      fontSize: 16, bold: true, fontFace: "Georgia",
      color: C.ink, align: "center", margin: 0
    });
    s.addText(sh.sub, {
      x, y: 3.97, w: 1.5, h: 0.3,
      fontSize: 10, fontFace: "Calibri",
      color: C.midGray, align: "center", margin: 0
    });
    s.addText(sh.desc, {
      x, y: 4.32, w: 1.5, h: 0.9,
      fontSize: 11, fontFace: "Calibri",
      color: C.darkGray, align: "center", margin: 0
    });
  });

  s.addText("水の量を調整するだけで豊かな表現が生まれる — これが水墨画の醍醐味！", {
    x: 0.7, y: 5.15, w: 8.6, h: 0.35,
    fontSize: 12, fontFace: "Calibri italic",
    color: C.seal, align: "center", margin: 0
  });
}

// ── スライド8: 基本の筆使い ──────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "基本の筆使い（運筆）");

  const techniques = [
    { name: "中鋒（ちゅうほう）",  desc: "筆を立て、穂先を中央に保ちながら引く。均一な線になる" },
    { name: "側鋒（そくほう）",    desc: "筆を傾け、穂の側面で描く。かすれた広い線が出る" },
    { name: "逆筆（ぎゃくひつ）",  desc: "穂先と逆方向に押すように動かす。力強い荒々しい線" },
    { name: "渇筆（かっぴつ）",    desc: "墨が少ない筆でかすれた線。枯れ木・岩肌の表現に" },
    { name: "破墨（はぼく）",      desc: "濃い墨の上に薄い墨（または水）を重ねてにじませる技法" },
    { name: "積墨（せきぼく）",    desc: "乾いた上に墨を重ね塗りして深みを出す技法" },
  ];

  techniques.forEach((t, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.7 + col * 4.6;
    const y = 1.15 + row * 1.35;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.2, h: 1.2,
      fill: { color: C.paleGray }, line: { color: C.lightGray }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.2,
      fill: { color: C.seal }, line: { color: C.seal }
    });
    s.addText(t.name, {
      x: x + 0.18, y: y + 0.1, w: 3.9, h: 0.38,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.ink, align: "left", margin: 0
    });
    s.addText(t.desc, {
      x: x + 0.18, y: y + 0.5, w: 3.9, h: 0.62,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkGray, align: "left", margin: 0
    });
  });
}

// ── スライド9: 筆の持ち方・姿勢 ──────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "筆の持ち方と姿勢");

  // 左：持ち方
  s.addText("正しい筆の持ち方", {
    x: 0.7, y: 1.15, w: 4.5, h: 0.4,
    fontSize: 17, bold: true, fontFace: "Calibri",
    color: C.ink, align: "left", margin: 0
  });
  s.addText([
    { text: "① 親指・人差し指・中指の3本で軸を軽く持つ", options: { breakLine: true } },
    { text: "② 薬指・小指は軽く添える（力を入れない）", options: { breakLine: true } },
    { text: "③ 筆は鉛筆より立て気味に持つ", options: { breakLine: true } },
    { text: "④ 手首を固定せず、腕全体で動かす", options: { breakLine: true } },
    { text: "⑤ 力を抜いてリラックス！", options: {} },
  ], {
    x: 0.7, y: 1.65, w: 4.5, h: 3.0,
    fontSize: 14, fontFace: "Calibri",
    color: C.ink, paraSpaceAfter: 8, margin: 0
  });

  // 中央：簡易図（筆のシンボル）
  s.addShape(pres.shapes.OVAL, {
    x: 4.5, y: 2.2, w: 0.18, h: 0.7,
    fill: { color: C.ink }, line: { color: C.ink }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 4.55, y: 2.9, w: 0.08, h: 2.0,
    fill: { color: "8B6914" }, line: { color: "8B6914" }
  });
  s.addShape(pres.shapes.OVAL, {
    x: 4.37, y: 4.78, w: 0.44, h: 0.22,
    fill: { color: "6B5010" }, line: { color: "6B5010" }
  });

  // 右：姿勢ポイント
  s.addText("描くときの姿勢", {
    x: 5.2, y: 1.15, w: 4.5, h: 0.4,
    fontSize: 17, bold: true, fontFace: "Calibri",
    color: C.ink, align: "left", margin: 0
  });
  const postures = [
    "背筋をまっすぐ伸ばす",
    "机から少し離れて座る",
    "紙全体を見渡せる位置に",
    "非利き手で紙を軽く押さえる",
    "深呼吸して気持ちを落ち着ける",
  ];
  postures.forEach((p, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.2, y: 1.65 + i * 0.7, w: 0.22, h: 0.4,
      fill: { color: C.sepia }, line: { color: C.sepia }
    });
    s.addText(String(i + 1), {
      x: 5.2, y: 1.65 + i * 0.7, w: 0.22, h: 0.4,
      fontSize: 11, bold: true, fontFace: "Calibri",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
    s.addText(p, {
      x: 5.5, y: 1.65 + i * 0.7, w: 4.1, h: 0.4,
      fontSize: 14, fontFace: "Calibri",
      color: C.ink, valign: "middle", margin: 0
    });
  });
}

// ── スライド10: 練習① 基本の線 ──────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "練習① 基本の線を引いてみよう");

  const lineExercises = [
    { title: "縦線", tip: "上から下へ、一息で引く" },
    { title: "横線", tip: "左から右へ、腕を使って動かす" },
    { title: "斜め線", tip: "力強く引く・細く引くの両方を試す" },
    { title: "曲線",  tip: "筆の角度を変えながらゆっくりと" },
    { title: "太細線", tip: "筆圧を途中で変えて強弱をつける" },
    { title: "点（ちょん）", tip: "筆先で素早くタッチする" },
  ];

  lineExercises.forEach((ex, i) => {
    const col = i % 3;
    const row = Math.floor(i / 2);
    const x = 0.7 + col * 3.1;
    const y = 1.15 + (i < 3 ? 0 : 2.1);

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.8, h: 1.85,
      fill: { color: C.paleGray }, line: { color: C.lightGray },
      shadow: makeShadow()
    });

    // ラベルエリア
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.8, h: 0.4,
      fill: { color: C.ink }, line: { color: C.ink }
    });
    s.addText(ex.title, {
      x, y, w: 2.8, h: 0.4,
      fontSize: 14, bold: true, fontFace: "Calibri",
      color: C.white, align: "center", valign: "middle", margin: 0
    });

    // 白い練習スペース
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.08, y: y + 0.48, w: 2.64, h: 0.9,
      fill: { color: C.white }, line: { color: C.lightGray }
    });

    s.addText(ex.tip, {
      x: x + 0.08, y: y + 1.42, w: 2.64, h: 0.38,
      fontSize: 10, fontFace: "Calibri",
      color: C.midGray, align: "center", margin: 0
    });
  });
}

// ── スライド11: 練習② にじみ・暈し ─────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "練習② にじみと暈し（ぼかし）");

  s.addText("にじみ", {
    x: 0.7, y: 1.15, w: 4.3, h: 0.4,
    fontSize: 18, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addText([
    { text: "① 紙を水で軽く湿らせる（ぼかしたい部分）", options: { bullet: true, breakLine: true } },
    { text: "② 乾かないうちに濃い墨で描く", options: { bullet: true, breakLine: true } },
    { text: "③ 墨が自然ににじんで広がる", options: { bullet: true, breakLine: true } },
    { text: "④ 霧・水・空気感の表現に最適", options: { bullet: true } },
  ], {
    x: 0.7, y: 1.6, w: 4.3, h: 2.0,
    fontSize: 13, fontFace: "Calibri",
    color: C.ink, paraSpaceAfter: 6
  });

  s.addText("暈し（グラデーション）", {
    x: 0.7, y: 3.65, w: 4.3, h: 0.4,
    fontSize: 18, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addText([
    { text: "① 濃い墨で描いた部分に、すぐ濡れた筆を当てる", options: { bullet: true, breakLine: true } },
    { text: "② 引くように動かして墨を薄めていく", options: { bullet: true, breakLine: true } },
    { text: "③ 山の稜線・花びらの陰影表現に", options: { bullet: true } },
  ], {
    x: 0.7, y: 4.1, w: 4.3, h: 1.3,
    fontSize: 13, fontFace: "Calibri",
    color: C.ink, paraSpaceAfter: 6
  });

  // 右：グラデーションの視覚例
  s.addText("墨のグラデーション例", {
    x: 5.4, y: 1.15, w: 4.2, h: 0.4,
    fontSize: 15, bold: true, fontFace: "Georgia",
    color: C.ink, align: "center", margin: 0
  });
  const grads = ["111111", "2C2C2C", "555555", "888888", "AAAAAA", "CCCCCC", "E0E0E0"];
  grads.forEach((c, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.4 + i * 0.6, y: 1.65, w: 0.6, h: 3.0,
      fill: { color: c }, line: { color: "BBBBBB", width: 0.3 }
    });
  });
  s.addText("濃", { x: 5.4, y: 4.75, w: 0.6, h: 0.3, fontSize: 11, fontFace: "Calibri", color: C.ink, align: "center", margin: 0 });
  s.addText("薄", { x: 9.0, y: 4.75, w: 0.6, h: 0.3, fontSize: 11, fontFace: "Calibri", color: C.midGray, align: "center", margin: 0 });
}

// ── スライド12: 四君子 ──────────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "四君子（しくんし）— 水墨画の定番モチーフ");

  const shikkunshi = [
    { name: "梅（うめ）", season: "冬〜春", char: "忍耐・高潔", tip: "枝は折れ線で力強く。花は○で表す" },
    { name: "蘭（らん）", season: "春",     char: "清廉・優雅", tip: "葉は細い曲線で勢いよく。交差を意識" },
    { name: "菊（きく）", season: "秋",     char: "高潔・不屈", tip: "花びらは中心から放射状に" },
    { name: "竹（たけ）", season: "通年",   char: "節操・誠実", tip: "節を入れて、葉は「個」の字形に" },
  ];

  shikkunshi.forEach((item, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.65 + col * 4.65;
    const y = 1.15 + row * 2.15;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.3, h: 1.95,
      fill: { color: "FAFAFA" }, line: { color: C.lightGray },
      shadow: makeShadow()
    });
    // 左カラーバー
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.07, h: 1.95,
      fill: { color: C.sepia }, line: { color: C.sepia }
    });

    s.addText(item.name, {
      x: x + 0.2, y: y + 0.1, w: 2.5, h: 0.45,
      fontSize: 18, bold: true, fontFace: "Georgia",
      color: C.ink, align: "left", margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 2.75, y: y + 0.12, w: 1.35, h: 0.38,
      fill: { color: C.paleGray }, line: { color: C.lightGray }
    });
    s.addText(item.season, {
      x: x + 2.75, y: y + 0.12, w: 1.35, h: 0.38,
      fontSize: 11, fontFace: "Calibri",
      color: C.midGray, align: "center", valign: "middle", margin: 0
    });

    s.addText("象徴：" + item.char, {
      x: x + 0.2, y: y + 0.57, w: 3.9, h: 0.35,
      fontSize: 12, fontFace: "Calibri italic",
      color: C.seal, align: "left", margin: 0
    });
    s.addText("描き方のコツ：" + item.tip, {
      x: x + 0.2, y: y + 0.95, w: 3.9, h: 0.88,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkGray, align: "left", margin: 0
    });
  });
}

// ── スライド13: 鑑賞のポイント ───────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  addInkAccent(s);
  addSlideTitle(s, "作品鑑賞のポイント");

  const points = [
    { num: "01", title: "余白を見る",   body: "描かれていない「空間」に注目。何を表しているか想像しよう" },
    { num: "02", title: "墨の濃淡",     body: "どこが濃く、どこが薄いか。立体感・遠近感を感じ取ろう" },
    { num: "03", title: "筆の勢い",     body: "力強い線か繊細な線か。作者の気持ちや技量が現れる" },
    { num: "04", title: "落款（らっかん）", body: "右下にある印鑑・署名。作者のサインと考えよう" },
    { num: "05", title: "構図を読む",   body: "重心はどこか。対角線・黄金分割を意識して見てみよう" },
  ];

  points.forEach((p, i) => {
    const y = 1.15 + i * 0.82;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.7, y, w: 9.0, h: 0.72,
      fill: { color: i % 2 === 0 ? C.paleGray : C.white },
      line: { color: C.lightGray }
    });
    s.addText(p.num, {
      x: 0.72, y, w: 0.7, h: 0.72,
      fontSize: 20, bold: true, fontFace: "Georgia",
      color: C.lightGray, align: "center", valign: "middle", margin: 0
    });
    s.addText(p.title, {
      x: 1.5, y: y + 0.07, w: 2.5, h: 0.35,
      fontSize: 15, bold: true, fontFace: "Calibri",
      color: C.ink, align: "left", margin: 0
    });
    s.addText(p.body, {
      x: 1.5, y: y + 0.38, w: 8.0, h: 0.28,
      fontSize: 12, fontFace: "Calibri",
      color: C.darkGray, align: "left", margin: 0
    });
  });
}

// ── スライド14: まとめ ──────────────────────────────────────
{
  let s = pres.addSlide();
  s.background = { color: C.black };

  // 右側明るいパネル
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.5, y: 0, w: 4.5, h: 5.625,
    fill: { color: "222222" }, line: { color: "222222" }
  });

  s.addText("今日のまとめ", {
    x: 0.6, y: 0.5, w: 4.7, h: 0.55,
    fontSize: 26, bold: true, fontFace: "Georgia",
    color: C.white, align: "left", margin: 0
  });

  const summary = [
    "墨・筆・硯・和紙が水墨画の4つの基本道具",
    "墨の濃淡（5段階）で豊かな表現が生まれる",
    "筆使いの基本（中鋒・側鋒・渇筆など）",
    "にじみ・暈しで奥行きと空気感を表現する",
    "四君子（梅・蘭・菊・竹）が定番の題材",
    "余白・濃淡・筆の勢いに注目して鑑賞する",
  ];
  summary.forEach((item, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 1.15 + i * 0.68, w: 0.06, h: 0.45,
      fill: { color: C.seal }, line: { color: C.seal }
    });
    s.addText(item, {
      x: 0.78, y: 1.15 + i * 0.68, w: 4.55, h: 0.45,
      fontSize: 13, fontFace: "Calibri",
      color: "DDDDDD", align: "left", valign: "middle", margin: 0
    });
  });

  // 右側：次回予告
  s.addText("次回の授業", {
    x: 5.75, y: 0.6, w: 3.9, h: 0.5,
    fontSize: 18, bold: true, fontFace: "Georgia",
    color: C.lightGray, align: "center", margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: 5.75, y: 1.18, w: 3.9, h: 0,
    line: { color: C.sepia, width: 1 }
  });
  s.addText([
    { text: "🖌  実際に筆を持って", options: { breakLine: true } },
    { text: "  基本の線を練習しよう", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "📄  半紙と筆・墨を", options: { breakLine: true } },
    { text: "  忘れずに持参すること", options: {} },
  ], {
    x: 5.75, y: 1.3, w: 3.9, h: 2.5,
    fontSize: 15, fontFace: "Calibri",
    color: C.lightGray, align: "center", valign: "top", margin: 0, paraSpaceAfter: 8
  });

  // 印鑑風サイン
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.9, y: 4.3, w: 1.0, h: 0.85,
    fill: { color: C.seal }, line: { color: C.seal }
  });
  s.addText("美術", {
    x: 5.9, y: 4.3, w: 1.0, h: 0.85,
    fontSize: 20, bold: true, fontFace: "Georgia",
    color: C.white, align: "center", valign: "middle", margin: 0
  });
  s.addText("水墨画入門", {
    x: 7.1, y: 4.55, w: 2.5, h: 0.4,
    fontSize: 13, fontFace: "Calibri",
    color: C.midGray, align: "left", valign: "middle", margin: 0
  });
}

// ── 出力 ────────────────────────────────────────────────────
const outputPath = "C:\\Users\\shondo\\Desktop\\水墨画入門.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("✅ 完成: " + outputPath);
}).catch(e => console.error("❌ エラー:", e));
