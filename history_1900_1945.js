const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = '20世紀前半の世界と日本 (1900-1945)';

const NAVY    = "1C3557";
const GOLD    = "C8A951";
const CREAM   = "F4F0E8";
const BURG    = "7A1F2E";
const LTBG    = "F4F0E8";
const WHITE   = "FFFFFF";
const DTXT    = "1C2433";
const MGRAY   = "64748B";

const makeShadow = () => ({ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.15 });

// ============================================================
// SLIDE 1: Title
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: GOLD } });

  s.addText("20世紀前半の世界と日本", {
    x: 0.7, y: 0.9, w: 8.8, h: 1.5,
    fontSize: 40, fontFace: "Georgia", bold: true, color: GOLD, align: "left", margin: 0
  });
  s.addText("1900年代〜1945年", {
    x: 0.7, y: 2.55, w: 8, h: 0.7,
    fontSize: 24, fontFace: "Calibri", color: CREAM, align: "left", margin: 0
  });
  s.addText([
    { text: "第一次世界大戦　｜　ロシア革命とアメリカの繁栄", options: { breakLine: true } },
    { text: "ヴェルサイユ体制　｜　日本の大正デモクラシー" }
  ], {
    x: 0.7, y: 3.4, w: 8.8, h: 0.9,
    fontSize: 14, fontFace: "Calibri", color: "A8B8C8", align: "left", margin: 0
  });
  s.addText("中学社会科　歴史", {
    x: 0.7, y: 5.1, w: 8, h: 0.35,
    fontSize: 11, fontFace: "Calibri", color: "6A8FAF", align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 2: 目次
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("目　次", {
    x: 0.5, y: 0.25, w: 9, h: 0.75,
    fontSize: 36, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  const chapters = [
    { num: "01", title: "第一次世界大戦", desc: "同盟関係による紛争の連鎖、新兵器と総力戦、そして終結" },
    { num: "02", title: "ロシア革命とアメリカの繁栄", desc: "それぞれの経過と、自由・平等の兼ね合い" },
    { num: "03", title: "ヴェルサイユ体制", desc: "概要・敗者への賠償・民族自決と人種差別撤廃法案" },
    { num: "04", title: "大戦景気と大正デモクラシー", desc: "成金・米騒動から政党内閣へ、普通選挙法と治安維持法" },
  ];
  chapters.forEach((ch, i) => {
    const y = 1.25 + i * 1.0;
    s.addShape(pres.shapes.OVAL, { x: 0.5, y: y, w: 0.55, h: 0.55, fill: { color: NAVY } });
    s.addText(ch.num, { x: 0.5, y: y + 0.03, w: 0.55, h: 0.5, fontSize: 13, fontFace: "Calibri", bold: true, color: GOLD, align: "center", margin: 0 });
    s.addText(ch.title, { x: 1.2, y: y, w: 8.3, h: 0.33, fontSize: 17, fontFace: "Calibri", bold: true, color: NAVY, align: "left", margin: 0 });
    s.addText(ch.desc, { x: 1.2, y: y + 0.35, w: 8.3, h: 0.3, fontSize: 12, fontFace: "Calibri", color: MGRAY, align: "left", margin: 0 });
  });
}

// ============================================================
// SLIDE 3: Chapter 1 Divider – 第一次世界大戦
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: "5A1520" };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: GOLD } });

  s.addText("Chapter 01", { x: 0.7, y: 1.1, w: 8, h: 0.55, fontSize: 18, fontFace: "Calibri", color: GOLD, align: "left", margin: 0 });
  s.addText("第一次世界大戦", {
    x: 0.7, y: 1.75, w: 8.8, h: 1.3,
    fontSize: 46, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0
  });
  s.addText("1914 — 1918", {
    x: 0.7, y: 3.15, w: 6, h: 0.65, fontSize: 24, fontFace: "Calibri", color: GOLD, align: "left", margin: 0
  });
  s.addText("同盟関係による紛争の連鎖　｜　新兵器と総力戦による長期化", {
    x: 0.7, y: 3.95, w: 8.8, h: 0.5, fontSize: 14, fontFace: "Calibri", color: "DDBBBB", align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 4: WWI – Alliance Systems
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("同盟関係による紛争の連鎖", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 30, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Left box: 三国同盟
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.2, h: 3.6, fill: { color: "2E4A7A" }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.2, h: 0.5, fill: { color: "1A2E5A" } });
  s.addText("三国同盟", { x: 0.4, y: 1.0, w: 4.2, h: 0.5, fontSize: 18, fontFace: "Georgia", bold: true, color: GOLD, align: "center", margin: 0 });
  s.addText([
    { text: "ドイツ", options: { breakLine: true } },
    { text: "オーストリア＝ハンガリー", options: { breakLine: true } },
    { text: "イタリア（のち離脱）" }
  ], { x: 0.6, y: 1.62, w: 3.8, h: 1.1, fontSize: 16, fontFace: "Calibri", bold: true, color: WHITE, align: "left", margin: 0 });
  s.addText([
    { text: "サラエヴォ事件（1914年6月）をきっかけに、", options: { breakLine: true } },
    { text: "オーストリアがセルビアへ宣戦布告。", options: { breakLine: true } },
    { text: "各国が条約に基づき次々と参戦し、", options: { breakLine: true } },
    { text: "一地域の紛争が世界大戦に拡大した。" }
  ], { x: 0.6, y: 2.85, w: 3.8, h: 1.6, fontSize: 12, fontFace: "Calibri", color: "BBCCDD", align: "left", margin: 0 });

  // VS
  s.addShape(pres.shapes.OVAL, { x: 4.55, y: 2.35, w: 0.9, h: 0.9, fill: { color: GOLD } });
  s.addText("VS", { x: 4.55, y: 2.37, w: 0.9, h: 0.86, fontSize: 17, fontFace: "Calibri", bold: true, color: NAVY, align: "center", margin: 0 });

  // Right box: 三国協商
  s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 1.0, w: 4.2, h: 3.6, fill: { color: "2A6040" }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 1.0, w: 4.2, h: 0.5, fill: { color: "1A4028" } });
  s.addText("三国協商", { x: 5.4, y: 1.0, w: 4.2, h: 0.5, fontSize: 18, fontFace: "Georgia", bold: true, color: GOLD, align: "center", margin: 0 });
  s.addText([
    { text: "イギリス", options: { breakLine: true } },
    { text: "フランス", options: { breakLine: true } },
    { text: "ロシア" }
  ], { x: 5.6, y: 1.62, w: 3.8, h: 1.1, fontSize: 16, fontFace: "Calibri", bold: true, color: WHITE, align: "left", margin: 0 });
  s.addText([
    { text: "連合国側にはのちに", options: { breakLine: true } },
    { text: "日本・イタリア・アメリカも参戦。", options: { breakLine: true } },
    { text: "戦争は世界規模に拡大。", options: { breakLine: true } },
    { text: "1917年のアメリカ参戦が戦局を決定づけた。" }
  ], { x: 5.6, y: 2.85, w: 3.8, h: 1.6, fontSize: 12, fontFace: "Calibri", color: "BBDDCC", align: "left", margin: 0 });

  // Bottom callout
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 4.78, w: 9.2, h: 0.65, fill: { color: "3A1020" } });
  s.addText("★ サラエヴォ事件：オーストリア皇太子夫妻がセルビア人青年に暗殺（1914年6月）→「バルカンは欧州の火薬庫」", {
    x: 0.5, y: 4.85, w: 9.0, h: 0.45, fontSize: 12, fontFace: "Calibri", color: "FFDDAA", align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 5: WWI – New Weapons & End
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("新兵器・総力戦・戦争の終結", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 30, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Left: New weapons
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.4, h: 3.85, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.4, h: 0.48, fill: { color: NAVY } });
  s.addText("主な新兵器と塹壕戦", { x: 0.4, y: 1.0, w: 4.4, h: 0.48, fontSize: 15, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });

  const weapons = [
    ["戦車（タンク）", "塹壕を突破するために英国が開発"],
    ["毒ガス", "塩素・マスタードガスで大量殺傷"],
    ["飛行機", "偵察・爆撃に初めて実戦使用"],
    ["潜水艦（Uボート）", "ドイツが海上封鎖に投入"],
    ["機関銃", "防御側有利＝戦線が膠着"],
  ];
  weapons.forEach(([name, desc], i) => {
    const y = 1.58 + i * 0.62;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 0.08, h: 0.4, fill: { color: BURG } });
    s.addText(name, { x: 0.65, y: y, w: 1.9, h: 0.28, fontSize: 13, fontFace: "Calibri", bold: true, color: BURG, align: "left", margin: 0 });
    s.addText(desc, { x: 0.65, y: y + 0.28, w: 4.0, h: 0.25, fontSize: 11, fontFace: "Calibri", color: DTXT, align: "left", margin: 0 });
  });

  // Right: Timeline to end
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 1.0, w: 4.5, h: 3.85, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 1.0, w: 4.5, h: 0.48, fill: { color: BURG } });
  s.addText("終戦への経過", { x: 5.1, y: 1.0, w: 4.5, h: 0.48, fontSize: 15, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });

  const events = [
    ["1914", "6月：サラエヴォ事件→8月に大戦勃発"],
    ["1915", "イタリアが協商側（連合国）に寝返り"],
    ["1917", "アメリカ参戦・ロシア革命でロシア離脱"],
    ["1918\n11月", "ドイツが休戦協定に調印→終戦"],
    ["結果", "死者約1,000万人。前例なき被害"],
  ];
  events.forEach(([year, desc], i) => {
    const y = 1.6 + i * 0.65;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: y, w: 0.85, h: 0.48, fill: { color: NAVY } });
    s.addText(year, { x: 5.2, y: y, w: 0.85, h: 0.48, fontSize: 10, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });
    s.addText(desc, { x: 6.15, y: y + 0.08, w: 3.3, h: 0.38, fontSize: 12, fontFace: "Calibri", color: DTXT, align: "left", margin: 0 });
  });

  // Bottom concept
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 5.02, w: 9.2, h: 0.45, fill: { color: GOLD } });
  s.addText("総力戦：軍人だけでなく、国民全体・産業・経済・女性労働まで動員される近代的な戦争形態", {
    x: 0.5, y: 5.05, w: 9.0, h: 0.38, fontSize: 12, fontFace: "Calibri", bold: true, color: NAVY, align: "center", margin: 0
  });
}

// ============================================================
// SLIDE 6: Chapter 2 Divider
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: "1A3A2A" };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: GOLD } });

  s.addText("Chapter 02", { x: 0.7, y: 1.1, w: 8, h: 0.55, fontSize: 18, fontFace: "Calibri", color: GOLD, align: "left", margin: 0 });
  s.addText("ロシア革命と\nアメリカの繁栄", {
    x: 0.7, y: 1.75, w: 8.8, h: 2.1,
    fontSize: 42, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0
  });
  s.addText("自由と平等の兼ね合い", {
    x: 0.7, y: 4.0, w: 8.8, h: 0.55, fontSize: 20, fontFace: "Calibri", color: GOLD, align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 7: Russian Revolution
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("ロシア革命の経過", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 30, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  const events = [
    { year: "1905", title: "第一次ロシア革命", desc: "「血の日曜日」事件。ニコライ２世が立憲を認めるが専制維持。", color: "8B2635" },
    { year: "1917\n2月", title: "二月革命（三月革命）", desc: "ロマノフ王朝崩壊。臨時政府成立もWWI継続→国民の不満。", color: "2E4A7A" },
    { year: "1917\n10月", title: "十月革命（十一月革命）", desc: "レーニン率いるボリシェヴィキが政権掌握。「平和・土地・パン」。", color: "1A5C36" },
    { year: "1918", title: "ブレスト＝リトフスク条約", desc: "ドイツと単独講和し第一次大戦から離脱。内戦（赤vs白）が続く。", color: "7A6028" },
    { year: "1922", title: "ソヴィエト社会主義共和国連邦（ソ連）成立", desc: "世界初の社会主義国家。計画経済・一党独裁体制へ。", color: "3A2070" },
  ];

  events.forEach((ev, i) => {
    const y = 1.0 + i * 0.88;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: y, w: 0.9, h: 0.7, fill: { color: ev.color } });
    s.addText(ev.year, { x: 0.4, y: y, w: 0.9, h: 0.7, fontSize: 11, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 1.3, y: y + 0.3, w: 0.25, h: 0.08, fill: { color: ev.color } });
    s.addText(ev.title, { x: 1.65, y: y, w: 4.2, h: 0.32, fontSize: 14, fontFace: "Calibri", bold: true, color: NAVY, align: "left", margin: 0 });
    s.addText(ev.desc, { x: 1.65, y: y + 0.34, w: 7.9, h: 0.32, fontSize: 12, fontFace: "Calibri", color: DTXT, align: "left", margin: 0 });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 5.2, w: 9.2, h: 0.32, fill: { color: "DDDACC" } });
  s.addText("★ 「平等」（社会主義）を優先するあまり、個人の自由・政治的権利が制限される体制へと変化していった。", {
    x: 0.5, y: 5.22, w: 9.0, h: 0.28, fontSize: 11, fontFace: "Calibri", color: "5A3020", align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 8: American Prosperity
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("アメリカの繁栄と自由・平等の課題", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 28, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Left column: Prosperity
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.35, h: 4.3, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.35, h: 0.48, fill: { color: "1C5A8A" } });
  s.addText("繁栄（1920年代）", { x: 0.4, y: 1.0, w: 4.35, h: 0.48, fontSize: 16, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });

  const prosperity = [
    "大戦中の物資供給で世界最大の経済大国に",
    "自動車（フォード）・電化製品が急速に普及",
    "大量生産・大量消費の「消費社会」が誕生",
    "「黄金の20年代」（ジャズ・映画・ラジオ）",
    "国際連盟には不参加（孤立主義的外交）",
    "禁酒法（1920〜33年）の試みと失敗",
  ];
  prosperity.forEach((item, i) => {
    s.addText(item, {
      x: 0.55, y: 1.58 + i * 0.54, w: 4.1, h: 0.44,
      fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0
    });
  });

  // Right column: Contradictions
  s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y: 1.0, w: 4.35, h: 4.3, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y: 1.0, w: 4.35, h: 0.48, fill: { color: BURG } });
  s.addText("自由と平等の矛盾", { x: 5.25, y: 1.0, w: 4.35, h: 0.48, fontSize: 16, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });

  const contradictions = [
    "黒人差別：KKK（白人至上主義）の台頭",
    "移民制限法（1924年）：アジア系を事実上排除",
    "「自由の国」でも人種・民族差別が深刻",
    "ウィルソンの14か条：民族自決を提唱するが",
    "有色人種・植民地には適用されず",
    "「自由」は白人・資本家のためのものという現実",
  ];
  contradictions.forEach((item, i) => {
    s.addText(item, {
      x: 5.4, y: 1.58 + i * 0.54, w: 4.1, h: 0.44,
      fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0
    });
  });
}

// ============================================================
// SLIDE 9: Chapter 3 Divider
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: "2C2010" };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: GOLD } });

  s.addText("Chapter 03", { x: 0.7, y: 1.1, w: 8, h: 0.55, fontSize: 18, fontFace: "Calibri", color: GOLD, align: "left", margin: 0 });
  s.addText("ヴェルサイユ体制", {
    x: 0.7, y: 1.75, w: 8.8, h: 1.3,
    fontSize: 46, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0
  });
  s.addText("1919年　パリ講和会議", {
    x: 0.7, y: 3.2, w: 7, h: 0.6, fontSize: 22, fontFace: "Calibri", color: GOLD, align: "left", margin: 0
  });
  s.addText("概要　｜　賠償　｜　民族自決　｜　人種差別撤廃提案", {
    x: 0.7, y: 3.95, w: 8.8, h: 0.5, fontSize: 14, fontFace: "Calibri", color: "DDCC99", align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 10: Versailles – Overview & Reparations
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("ヴェルサイユ条約の概要と賠償", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 28, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Overview band
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 9.2, h: 1.2, fill: { color: WHITE }, shadow: makeShadow() });
  s.addText("ヴェルサイユ条約（1919年6月調印）の概要", {
    x: 0.55, y: 1.05, w: 6, h: 0.35, fontSize: 14, fontFace: "Calibri", bold: true, color: NAVY, margin: 0
  });
  const overview = [
    "ドイツの全植民地没収・領土縮小（ポーランド回廊など）・軍備制限（陸軍10万人以下）",
    "国際連盟の設立（ウィルソン大統領提唱）　／　ライン地方の非武装化",
  ];
  overview.forEach((item, i) => {
    s.addText(item, {
      x: 0.55, y: 1.42 + i * 0.3, w: 9.0, h: 0.28,
      fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0
    });
  });

  // Two columns below
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 2.35, w: 4.5, h: 2.95, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 2.35, w: 4.5, h: 0.45, fill: { color: BURG } });
  s.addText("敗者への賠償（ドイツ）", { x: 0.4, y: 2.35, w: 4.5, h: 0.45, fontSize: 15, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });
  const reparations = [
    "戦争責任はドイツにある（231条）と明記",
    "賠償金：1,320億金マルク（天文学的な額）",
    "経済壊滅・失業・ハイパーインフレが続く",
    "国民の屈辱感と怒り→後のナチズム台頭の土壌",
  ];
  reparations.forEach((item, i) => {
    s.addText(item, { x: 0.55, y: 2.9 + i * 0.56, w: 4.2, h: 0.46, fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0 });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.35, w: 4.5, h: 2.95, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.35, w: 4.5, h: 0.45, fill: { color: "1C5A8A" } });
  s.addText("ヴェルサイユ体制の特徴", { x: 5.1, y: 2.35, w: 4.5, h: 0.45, fontSize: 15, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });
  const features = [
    "国際連盟：平和維持機関（制裁手段は弱い）",
    "米・ソ・ドイツは発足時に不参加または排除",
    "「勝者の平和」＝敗国に一方的に不利な体制",
    "20年後の第二次大戦の遠因となった",
  ];
  features.forEach((item, i) => {
    s.addText(item, { x: 5.25, y: 2.9 + i * 0.56, w: 4.2, h: 0.46, fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0 });
  });
}

// ============================================================
// SLIDE 11: Self-Determination & Racial Equality Proposal
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("民族自決と人種差別撤廃提案", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 28, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Self-determination
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 9.2, h: 1.85, fill: { color: "E8F0E8" }, shadow: makeShadow() });
  s.addText("民族自決（ウィルソンの14か条・1918年）", {
    x: 0.55, y: 1.05, w: 8.5, h: 0.38, fontSize: 15, fontFace: "Calibri", bold: true, color: "1A5C36", margin: 0
  });
  s.addText([
    { text: "原則：", options: { bold: true } },
    { text: "各民族が自分たちの政府・国家の形を決める権利（民族自決権）を認める。", options: { breakLine: true } },
    { text: "成果：", options: { bold: true } },
    { text: "東欧・バルカンで新国家が誕生（ポーランド・チェコスロヴァキア・ユーゴスラヴィアなど）。", options: { breakLine: true } },
    { text: "限界：", options: { bold: true } },
    { text: "アジア・アフリカの植民地には適用されず。朝鮮（三・一独立運動）・中国（五・四運動）は強く反発した。", options: {} }
  ], {
    x: 0.55, y: 1.48, w: 9.0, h: 1.28,
    fontSize: 13, fontFace: "Calibri", color: DTXT, align: "left", margin: 0
  });

  // Racial equality
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 3.0, w: 9.2, h: 2.3, fill: { color: "F0E8E8" }, shadow: makeShadow() });
  s.addText("人種差別撤廃提案（日本・1919年パリ講和会議）", {
    x: 0.55, y: 3.08, w: 8.5, h: 0.38, fontSize: 15, fontFace: "Calibri", bold: true, color: BURG, margin: 0
  });
  s.addText([
    { text: "日本（全権：牧野伸顕）が国際連盟規約に「人種差別撤廃」を明記するよう提案。", options: { breakLine: true } },
    { text: "賛成多数（投票11カ国中11カ国が賛成）→ 議長ウィルソンが「全会一致が必要」として否決。", options: { breakLine: true } },
    { text: "英・豪・米が反対した背景：自国の有色人種差別政策（移民制限・植民地統治）と矛盾するため。", options: { breakLine: true } },
    { text: "★ 考えよう：「民族自決」も「人種平等」も、強者に都合よく使われた概念だったのでは？", options: { bold: true } }
  ], {
    x: 0.55, y: 3.52, w: 9.0, h: 1.65,
    fontSize: 13, fontFace: "Calibri", color: DTXT, align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 12: Chapter 4 Divider
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: "1E1A0A" };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: GOLD } });

  s.addText("Chapter 04", { x: 0.7, y: 0.9, w: 8, h: 0.55, fontSize: 18, fontFace: "Calibri", color: GOLD, align: "left", margin: 0 });
  s.addText("大戦景気と\n大正デモクラシー", {
    x: 0.7, y: 1.55, w: 8.8, h: 2.1,
    fontSize: 40, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0
  });
  s.addText("1910年代〜1920年代の日本", {
    x: 0.7, y: 3.75, w: 7.5, h: 0.6, fontSize: 20, fontFace: "Calibri", color: GOLD, align: "left", margin: 0
  });
  s.addText("成金の出現　｜　米騒動　｜　政党内閣　｜　普通選挙法と治安維持法", {
    x: 0.7, y: 4.45, w: 8.8, h: 0.5, fontSize: 13, fontFace: "Calibri", color: "DDCC88", align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 13: Japan's War Boom & Rice Riots
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("大戦景気・成金の出現・米騒動", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 28, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Left: War boom
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.35, h: 2.25, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.35, h: 0.45, fill: { color: NAVY } });
  s.addText("大戦景気（1914〜18年）", { x: 0.4, y: 1.0, w: 4.35, h: 0.45, fontSize: 14, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });
  const boom = [
    "欧州が戦場→日本が物資・輸出品を供給",
    "造船・化学・鉄鋼業が急成長",
    "貿易黒字拡大・債権国に転換",
    "「成金」：一気に富を得た新興資本家の出現",
  ];
  boom.forEach((item, i) => {
    s.addText(item, { x: 0.55, y: 1.53 + i * 0.41, w: 4.1, h: 0.36, fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0 });
  });

  // Right: Rice Riots
  s.addShape(pres.shapes.RECTANGLE, { x: 4.85, y: 1.0, w: 4.75, h: 2.25, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 4.85, y: 1.0, w: 4.75, h: 0.45, fill: { color: BURG } });
  s.addText("米騒動（1918年）", { x: 4.85, y: 1.0, w: 4.75, h: 0.45, fontSize: 14, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });
  const rice = [
    "好景気の一方で物価高騰・格差拡大",
    "富山の漁村女性が米価暴騰に抗議（火付け役）",
    "全国に波及：70万人が暴動・打ちこわし",
    "寺内内閣（藩閥内閣）が総辞職",
    "→ 原敬が初の本格的政党内閣を組閣",
  ];
  rice.forEach((item, i) => {
    s.addText(item, { x: 5.0, y: 1.53 + i * 0.33, w: 4.45, h: 0.3, fontSize: 12, fontFace: "Calibri", color: DTXT, bullet: true, margin: 0 });
  });

  // Bottom: 大正デモクラシー concept
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 3.38, w: 9.2, h: 1.92, fill: { color: "EEE8D5" }, shadow: makeShadow() });
  s.addText("大正デモクラシーとは", {
    x: 0.55, y: 3.45, w: 5, h: 0.38, fontSize: 15, fontFace: "Calibri", bold: true, color: NAVY, margin: 0
  });
  s.addText([
    { text: "吉野作造の「民本主義」（民意を政治に反映すべき）・美濃部達吉の「天皇機関説」（議会政治を正当化）", options: { breakLine: true } },
    { text: "護憲運動（藩閥政治打倒）が高まり、大学・新聞・労働運動・婦人運動が活発化。政党政治の時代へ。" }
  ], {
    x: 0.55, y: 3.9, w: 9.0, h: 1.25,
    fontSize: 13, fontFace: "Calibri", color: DTXT, align: "left", margin: 0
  });
}

// ============================================================
// SLIDE 14: Universal Suffrage & Peace Preservation Law
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: LTBG };

  s.addText("普通選挙法と治安維持法（1925年）", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 28, fontFace: "Georgia", bold: true, color: NAVY, align: "left", margin: 0
  });

  // Left: Universal Suffrage
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.35, h: 3.95, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.0, w: 4.35, h: 0.48, fill: { color: "1A5C36" } });
  s.addText("普通選挙法（1925年）", { x: 0.4, y: 1.0, w: 4.35, h: 0.48, fontSize: 15, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });

  s.addText("25歳以上の男子全員に選挙権", { x: 0.55, y: 1.57, w: 4.1, h: 0.38, fontSize: 14, fontFace: "Calibri", bold: true, color: "1A5C36", margin: 0 });
  s.addText([
    { text: "それ以前：高額納税者のみ選挙権（制限選挙）", options: { breakLine: true } },
    { text: "有権者数：約300万人 → 約1,240万人に拡大", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "意義：", options: { bold: true, breakLine: false } },
    { text: "民意の反映が広がり、労働者・農民の", options: { breakLine: true } },
    { text: "政治参加が初めて可能になった。", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "課題：", options: { bold: true, breakLine: false } },
    { text: "女性の選挙権は認められなかった", options: { breakLine: true } },
    { text: "（女性参政権は戦後1945年まで待つ）" }
  ], {
    x: 0.55, y: 2.02, w: 4.1, h: 2.8,
    fontSize: 12, fontFace: "Calibri", color: DTXT, align: "left", margin: 0
  });

  // Right: Peace Preservation Law
  s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y: 1.0, w: 4.35, h: 3.95, fill: { color: WHITE }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y: 1.0, w: 4.35, h: 0.48, fill: { color: BURG } });
  s.addText("治安維持法（1925年）", { x: 5.25, y: 1.0, w: 4.35, h: 0.48, fontSize: 15, fontFace: "Calibri", bold: true, color: WHITE, align: "center", margin: 0 });

  s.addText("社会主義運動・国体変更を取り締まり", { x: 5.4, y: 1.57, w: 4.1, h: 0.38, fontSize: 13, fontFace: "Calibri", bold: true, color: BURG, margin: 0 });
  s.addText([
    { text: "「国体を変革・私有財産制を否認する運動」", options: { breakLine: true } },
    { text: "をした者を最高死刑に処する法律。", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "問題点：", options: { bold: true, breakLine: true } },
    { text: "言論・思想の自由を法律で制限。", options: { breakLine: true } },
    { text: "左翼・労働運動が一斉に弾圧された。", options: { breakLine: true } },
    { text: "戦時中は解釈が拡大し、一般市民も", options: { breakLine: true } },
    { text: "逮捕・拷問の対象となった。", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "★ 普通選挙法と同年成立：", options: { bold: true, breakLine: true } },
    { text: "「アメとムチ」の政策という見方もある。" }
  ], {
    x: 5.4, y: 2.02, w: 4.1, h: 2.8,
    fontSize: 12, fontFace: "Calibri", color: DTXT, align: "left", margin: 0
  });

  // Bottom callout
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 5.1, w: 9.2, h: 0.4, fill: { color: GOLD } });
  s.addText("自由（選挙権の拡大）と制限（思想統制）が同時に進んだ――大正デモクラシーの「限界」", {
    x: 0.5, y: 5.13, w: 9.0, h: 0.34, fontSize: 12, fontFace: "Calibri", bold: true, color: NAVY, align: "center", margin: 0
  });
}

// ============================================================
// SLIDE 15: Summary
// ============================================================
{
  let s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: GOLD } });

  s.addText("まとめ：この時代から学ぶこと", {
    x: 0.7, y: 0.2, w: 8.8, h: 0.7,
    fontSize: 28, fontFace: "Georgia", bold: true, color: GOLD, align: "left", margin: 0
  });

  const summaries = [
    { num: "①", title: "同盟は平和を守るか？", desc: "同盟関係が連鎖的に戦争を拡大させた。相互防衛条約は安全を保障する一方で、戦争を自動的に拡大するリスクをはらむ。" },
    { num: "②", title: "革命の代償", desc: "「平等」を実現しようとしたソ連が「自由」を失った。理想と現実のジレンマ——どう両立させるかが政治の永遠の課題。" },
    { num: "③", title: "「勝者の平和」は長続きしない", desc: "ヴェルサイユ体制の報復的性格が次の大戦の温床となった。公正な秩序なしに、真の平和は築けない。" },
    { num: "④", title: "デモクラシーの条件", desc: "普通選挙法と治安維持法は表裏一体。選挙権の拡大と思想弾圧が同時に進んだ歴史は、自由の脆さを教える。" },
  ];

  summaries.forEach((s2, i) => {
    const y = 1.05 + i * 1.05;
    s.addShape(pres.shapes.OVAL, { x: 0.7, y: y, w: 0.55, h: 0.55, fill: { color: GOLD } });
    s.addText(s2.num, { x: 0.7, y: y + 0.03, w: 0.55, h: 0.5, fontSize: 14, fontFace: "Calibri", bold: true, color: NAVY, align: "center", margin: 0 });
    s.addText(s2.title, { x: 1.4, y: y, w: 8.1, h: 0.33, fontSize: 16, fontFace: "Calibri", bold: true, color: GOLD, align: "left", margin: 0 });
    s.addText(s2.desc, { x: 1.4, y: y + 0.34, w: 8.1, h: 0.62, fontSize: 12, fontFace: "Calibri", color: CREAM, align: "left", margin: 0 });
  });

  s.addText("歴史は繰り返す。私たちが学ぶのは、同じ過ちを繰り返さないため。", {
    x: 0.7, y: 5.2, w: 8.8, h: 0.3,
    fontSize: 12, fontFace: "Calibri", italic: true, color: GOLD, align: "center", margin: 0
  });
}

// ============================================================
// Output
// ============================================================
pres.writeFile({ fileName: "C:/Users/shondo/Desktop/agent_project/history_1900_1945.pptx" })
  .then(() => console.log("Done: history_1900_1945.pptx"))
  .catch(err => console.error(err));
