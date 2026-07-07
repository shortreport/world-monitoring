const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "円安の現状と見通し";

// Color palette - deep navy/gold financial theme
const C = {
  navy:    "0D1B3E",
  navy2:   "1A2F5C",
  blue:    "2563EB",
  lblue:   "DBEAFE",
  gold:    "D97706",
  lgold:   "FEF3C7",
  white:   "FFFFFF",
  offwhite:"F8FAFC",
  gray:    "64748B",
  lgray:   "E2E8F0",
  red:     "DC2626",
  green:   "16A34A",
  text:    "1E293B",
};

const makeShadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.12 });

// ─── SLIDE 1: Title ─────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // Gold accent circle (decorative)
  s.addShape(pres.shapes.OVAL, { x: 7.5, y: -0.8, w: 4, h: 4, fill: { color: C.gold, transparency: 80 }, line: { color: C.gold, width: 0 } });
  s.addShape(pres.shapes.OVAL, { x: -1, y: 3.5, w: 3, h: 3, fill: { color: C.blue, transparency: 75 }, line: { color: C.blue, width: 0 } });

  // ¥ symbol large watermark
  s.addText("¥", { x: 7.2, y: 0.5, w: 2.5, h: 2.5, fontSize: 180, color: C.white, bold: true, align: "center", transparency: 85 });

  // Tag
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.0, w: 2.2, h: 0.35, fill: { color: C.gold }, rectRadius: 0.05, line: { color: C.gold, width: 0 } });
  s.addText("金融解説 2026.06", { x: 0.6, y: 1.0, w: 2.2, h: 0.35, fontSize: 10, color: C.white, bold: true, align: "center", valign: "middle", margin: 0 });

  // Main title
  s.addText("円安の現状と\n今後の見通し", {
    x: 0.6, y: 1.6, w: 8.0, h: 2.2,
    fontSize: 52, color: C.white, bold: true, align: "left", valign: "top",
    lineSpacingMultiple: 1.15
  });

  // Subtitle
  s.addText("なぜ円安が続くのか、どこへ向かうのか", {
    x: 0.6, y: 3.85, w: 7, h: 0.5,
    fontSize: 17, color: C.lblue, align: "left"
  });

  // Bottom info
  s.addShape(pres.shapes.LINE, { x: 0.6, y: 4.9, w: 8.8, h: 0, line: { color: C.blue, width: 0.5 } });
  s.addText("Prepared for Executive Briefing  |  USD/JPY ・ 金利差 ・ 日銀政策 ・ シナリオ分析", {
    x: 0.6, y: 4.98, w: 8.8, h: 0.35,
    fontSize: 9, color: C.gray, align: "left"
  });
}

// ─── SLIDE 2: 現状 ──────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  // Header bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.0, fill: { color: C.navy }, line: { color: C.navy, width: 0 } });
  s.addText("現状：円はどこまで下落したか", { x: 0.5, y: 0, w: 9, h: 1.0, fontSize: 24, color: C.white, bold: true, align: "left", valign: "middle" });

  // 3 big KPI cards
  const cards = [
    { label: "USD/JPY（2026年6月）", value: "~145円", sub: "2020年比 ▲30%超の円安", color: C.red },
    { label: "ピーク水準（2022年10月）", value: "151.9円", sub: "32年ぶりの円安水準", color: C.gold },
    { label: "黒田緩和前（2021年初）", value: "103円", sub: "わずか5年で40円超の下落", color: C.blue },
  ];
  cards.forEach((c, i) => {
    const x = 0.4 + i * 3.1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.25, w: 2.9, h: 1.7, fill: { color: C.white }, rectRadius: 0.12, line: { color: C.lgray, width: 1 }, shadow: makeShadow() });
    s.addText(c.value, { x, y: 1.38, w: 2.9, h: 0.85, fontSize: 34, color: c.color, bold: true, align: "center" });
    s.addText(c.label, { x, y: 2.2, w: 2.9, h: 0.35, fontSize: 10, color: C.gray, align: "center" });
    s.addText(c.sub, { x, y: 2.55, w: 2.9, h: 0.32, fontSize: 9, color: C.text, align: "center", italic: true });
  });

  // USD/JPY line chart
  s.addChart(pres.charts.LINE, [{
    name: "USD/JPY",
    labels: ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"],
    values: [109, 106, 110, 132, 141, 153, 149, 145]
  }], {
    x: 0.4, y: 3.15, w: 9.2, h: 2.1,
    chartColors: [C.blue],
    lineSize: 3, lineSmooth: true,
    chartArea: { fill: { color: C.white }, roundedCorners: true },
    catAxisLabelColor: C.gray, valAxisLabelColor: C.gray,
    valGridLine: { color: C.lgray, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: false,
    showValue: false,
    valAxisMinVal: 95,
    valAxisMaxVal: 165,
    showTitle: true, title: "USD/JPY 推移（年次平均）",
    titleColor: C.text, titleFontSize: 11,
  });
}

// ─── SLIDE 3: 3大要因 ────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.0, fill: { color: C.navy }, line: { color: C.navy, width: 0 } });
  s.addText("円安の3大要因", { x: 0.5, y: 0, w: 9, h: 1.0, fontSize: 24, color: C.white, bold: true, align: "left", valign: "middle" });

  const factors = [
    {
      num: "01",
      title: "日米金利差",
      icon: "%",
      body: "米連邦準備制度（Fed）が積極利上げを実施する一方、日銀は超低金利を長期維持。2022〜23年の金利差は過去最大水準に拡大し、円売り・ドル買いを誘発した。",
      color: C.blue,
    },
    {
      num: "02",
      title: "貿易・経常収支の悪化",
      icon: "↓",
      body: "エネルギー価格高騰と輸入増加により、日本の貿易赤字が拡大。エネルギーをドルで買う構造が恒常的な円売り圧力となっている。",
      color: C.gold,
    },
    {
      num: "03",
      title: "円キャリートレード",
      icon: "⇄",
      body: "低金利の円を借りて高利回り資産に投資する「円キャリー」が拡大。市場リスクが低い局面では大量の円売りが発生し、円安を加速させる。",
      color: C.red,
    },
  ];

  factors.forEach((f, i) => {
    const x = 0.35 + i * 3.12;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.2, w: 2.95, h: 4.1, fill: { color: C.white }, rectRadius: 0.14, line: { color: C.lgray, width: 1 }, shadow: makeShadow() });
    // Color top band
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.2, w: 2.95, h: 1.1, fill: { color: f.color }, rectRadius: 0.14, line: { color: f.color, width: 0 } });
    // Cover bottom rounded corners of top band
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.9, w: 2.95, h: 0.4, fill: { color: f.color }, line: { color: f.color, width: 0 } });
    // Number
    s.addText(f.num, { x, y: 1.22, w: 2.95, h: 0.45, fontSize: 11, color: C.white, bold: true, align: "center", transparency: 40 });
    // Icon
    s.addText(f.icon, { x, y: 1.5, w: 2.95, h: 0.7, fontSize: 30, color: C.white, bold: true, align: "center" });
    // Title
    s.addText(f.title, { x: x + 0.1, y: 2.38, w: 2.75, h: 0.55, fontSize: 14, color: f.color, bold: true, align: "center" });
    // Body
    s.addText(f.body, { x: x + 0.15, y: 2.98, w: 2.65, h: 2.15, fontSize: 11, color: C.text, align: "left", valign: "top" });
  });
}

// ─── SLIDE 4: 日米金利差 チャート ────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.0, fill: { color: C.navy }, line: { color: C.navy, width: 0 } });
  s.addText("最大の要因：日米政策金利の差", { x: 0.5, y: 0, w: 9, h: 1.0, fontSize: 24, color: C.white, bold: true, align: "left", valign: "middle" });

  // Combo chart: Fed rate, BOJ rate
  const labels = ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"];
  s.addChart(pres.charts.LINE, [
    { name: "Fed政策金利（%）", labels, values: [2.4, 0.1, 0.1, 2.5, 5.3, 4.6, 4.4, 4.3] },
    { name: "日銀政策金利（%）", labels, values: [-0.1, -0.1, -0.1, -0.1, -0.1, 0.1, 0.5, 0.75] },
  ], {
    x: 0.4, y: 1.15, w: 5.8, h: 4.0,
    chartColors: ["2563EB", "D97706"],
    lineSize: 3, lineSmooth: true,
    chartArea: { fill: { color: C.white }, roundedCorners: true },
    catAxisLabelColor: C.gray, valAxisLabelColor: C.gray,
    valGridLine: { color: C.lgray, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: true, legendPos: "b", legendColor: C.text, legendFontSize: 10,
    showTitle: true, title: "日米政策金利の推移",
    titleColor: C.text, titleFontSize: 11,
  });

  // Key insights cards on right
  const points = [
    { val: "~3.5%", desc: "現在の日米金利差", color: C.blue },
    { val: "2022年", desc: "円安急加速の起点", color: C.gold },
    { val: "2024〜", desc: "日銀がようやく利上げ開始", color: C.green },
  ];
  points.forEach((p, i) => {
    const y = 1.25 + i * 1.35;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.5, y, w: 3.1, h: 1.15, fill: { color: C.white }, rectRadius: 0.1, line: { color: C.lgray, width: 1 }, shadow: makeShadow() });
    s.addText(p.val, { x: 6.5, y: y + 0.08, w: 3.1, h: 0.55, fontSize: 28, color: p.color, bold: true, align: "center" });
    s.addText(p.desc, { x: 6.5, y: y + 0.63, w: 3.1, h: 0.35, fontSize: 11, color: C.gray, align: "center" });
  });

  // Note
  s.addText("※ 金利差が大きいほど、低金利通貨（円）が売られやすくなる（金利平価）", {
    x: 0.4, y: 5.2, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, align: "left", italic: true
  });
}

// ─── SLIDE 5: 今後の見通し ───────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.0, fill: { color: C.navy }, line: { color: C.navy, width: 0 } });
  s.addText("今後の見通し：3つのシナリオ", { x: 0.5, y: 0, w: 9, h: 1.0, fontSize: 24, color: C.white, bold: true, align: "left", valign: "middle" });

  const scenarios = [
    {
      label: "ベースケース",
      prob: "50%",
      range: "140〜150円",
      title: "緩やかな円高復帰",
      points: [
        "日銀が2026年内に追加利上げ（0.75→1.0%）",
        "Fedは緩やかな利下げを継続",
        "金利差縮小で円は段階的に戻す",
        "年末目標：142〜146円"
      ],
      color: C.blue, bg: C.lblue
    },
    {
      label: "円安継続シナリオ",
      prob: "30%",
      range: "150〜160円",
      title: "構造的円安の定着",
      points: [
        "日銀が利上げに慎重姿勢を維持",
        "米景気が底堅くFed利下げ遅延",
        "貿易赤字が高止まり",
        "円キャリー再拡大で円安加速"
      ],
      color: C.red, bg: "FEE2E2"
    },
    {
      label: "急速円高シナリオ",
      prob: "20%",
      range: "130〜135円",
      title: "キャリー巻き戻し",
      points: [
        "米景気後退・リスクオフで円買い",
        "日銀の予想外の利上げ加速",
        "キャリートレード一斉解消",
        "2024年8月型の急騰再来"
      ],
      color: C.green, bg: "DCFCE7"
    },
  ];

  scenarios.forEach((sc, i) => {
    const x = 0.25 + i * 3.22;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.15, w: 3.05, h: 4.25, fill: { color: sc.bg }, rectRadius: 0.14, line: { color: sc.color, width: 1.5 }, shadow: makeShadow() });

    // Label + prob row
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.1, y: 1.25, w: 1.4, h: 0.3, fill: { color: sc.color }, rectRadius: 0.05, line: { color: sc.color, width: 0 } });
    s.addText(sc.label, { x: x + 0.1, y: 1.25, w: 1.4, h: 0.3, fontSize: 9, color: C.white, bold: true, align: "center", valign: "middle", margin: 0 });
    s.addText(`確率 ${sc.prob}`, { x: x + 1.6, y: 1.25, w: 1.35, h: 0.3, fontSize: 9, color: sc.color, bold: true, align: "right" });

    // Range
    s.addText(sc.range, { x, y: 1.6, w: 3.05, h: 0.65, fontSize: 26, color: sc.color, bold: true, align: "center" });

    // Title
    s.addText(sc.title, { x: x + 0.1, y: 2.25, w: 2.85, h: 0.38, fontSize: 12, color: C.text, bold: true, align: "center" });

    // Bullet points
    sc.points.forEach((pt, j) => {
      s.addText([{ text: pt, options: { bullet: true } }], {
        x: x + 0.15, y: 2.68 + j * 0.52, w: 2.75, h: 0.48,
        fontSize: 10, color: C.text, align: "left", valign: "top"
      });
    });
  });
}

// ─── SLIDE 6: まとめ ─────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // Decorative
  s.addShape(pres.shapes.OVAL, { x: 7.8, y: -0.5, w: 3.5, h: 3.5, fill: { color: C.blue, transparency: 80 }, line: { color: C.blue, width: 0 } });
  s.addShape(pres.shapes.OVAL, { x: -0.8, y: 3.8, w: 2.5, h: 2.5, fill: { color: C.gold, transparency: 80 }, line: { color: C.gold, width: 0 } });

  s.addText("KEY TAKEAWAYS", { x: 0.6, y: 0.5, w: 4, h: 0.38, fontSize: 11, color: C.gold, bold: true, align: "left", charSpacing: 3 });
  s.addText("まとめ", { x: 0.6, y: 0.85, w: 8, h: 0.75, fontSize: 36, color: C.white, bold: true, align: "left" });

  const takeaways = [
    { num: "1", text: "円安の最大要因は「日米金利差」。Fedの急激な利上げに日銀が追いつけなかった構造的問題。" },
    { num: "2", text: "日銀は2024年以降ようやく正常化へ転換。ただし利上げペースは依然として慎重で、金利差は大きい。" },
    { num: "3", text: "ベースケースは140〜150円台での推移。2026年内の追加利上げが円高の鍵を握る。" },
    { num: "4", text: "急速な円高（キャリー巻き戻し）のリスクにも要注意。2024年8月の教訓を忘れずに。" },
  ];

  takeaways.forEach((t, i) => {
    const y = 1.85 + i * 0.88;
    s.addShape(pres.shapes.OVAL, { x: 0.55, y: y + 0.05, w: 0.42, h: 0.42, fill: { color: C.gold }, line: { color: C.gold, width: 0 } });
    s.addText(t.num, { x: 0.55, y: y + 0.05, w: 0.42, h: 0.42, fontSize: 13, color: C.navy, bold: true, align: "center", valign: "middle", margin: 0 });
    s.addText(t.text, { x: 1.1, y, w: 8.3, h: 0.75, fontSize: 13, color: C.white, align: "left", valign: "middle" });
  });

  // Footer
  s.addShape(pres.shapes.LINE, { x: 0.6, y: 5.25, w: 8.8, h: 0, line: { color: C.gray, width: 0.5 } });
  s.addText("本資料は一般的な解説を目的としており、投資助言ではありません。", {
    x: 0.6, y: 5.3, w: 8.8, h: 0.28,
    fontSize: 8.5, color: C.gray, align: "left"
  });
}

// ─── WRITE ───────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "yen_outlook.pptx" }).then(() => {
  console.log("Done: yen_outlook.pptx");
});
