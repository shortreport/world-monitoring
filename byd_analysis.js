const pptxgen = require("pptxgenjs");

// ============================================================
// BYD財務リスク分析プレゼンテーション
// ============================================================

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "経営企画部";
pres.title = "BYD財務リスク分析：流動負債とサプライヤー問題";

// ---- カラーパレット ----
const C = {
  navy:    "1E2761",  // プライマリ（タイトル・強調）
  blue:    "2E5EAA",  // セカンダリ
  iceblue: "CADCFC",  // ライトアクセント
  red:     "C0392B",  // リスク警告色
  amber:   "E67E22",  // 注意色
  white:   "FFFFFF",
  offwhite:"F7F8FC",
  gray:    "64748B",
  darkgray:"334155",
  lightgray:"E2E8F0",
};

// ---- ヘルパー関数 ----
function makeShadow() {
  return { type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.12 };
}

// ============================================================
// スライド 1: 表紙
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // 左サイドアクセントバー
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.25, h: 5.625,
    fill: { color: C.amber }, line: { color: C.amber }
  });

  // 上部装飾
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.25, y: 0, w: 9.75, h: 0.06,
    fill: { color: C.iceblue }, line: { color: C.iceblue }
  });

  // メインタイトル
  s.addText("BYD財務リスク分析", {
    x: 0.7, y: 1.0, w: 8.6, h: 1.0,
    fontSize: 40, bold: true, color: C.white, fontFace: "Meiryo",
    align: "left", margin: 0
  });

  // サブタイトル
  s.addText("流動負債の業界比較とサプライヤー支払い問題", {
    x: 0.7, y: 2.1, w: 8.6, h: 0.7,
    fontSize: 22, bold: false, color: C.iceblue, fontFace: "Meiryo",
    align: "left", margin: 0
  });

  // 区切り線
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 3.0, w: 4.0, h: 0.04,
    fill: { color: C.amber }, line: { color: C.amber }
  });

  // 比較対象
  s.addText("比較対象：Toyota / Tesla / Geely　　分析期間：2022〜2024年度", {
    x: 0.7, y: 3.15, w: 8.6, h: 0.5,
    fontSize: 14, color: C.iceblue, fontFace: "Meiryo",
    align: "left", margin: 0
  });

  // 日付・部署
  s.addText("2026年6月　経営企画部", {
    x: 0.7, y: 4.8, w: 8.6, h: 0.4,
    fontSize: 12, color: C.gray, fontFace: "Meiryo",
    align: "left", margin: 0
  });

  // BYDロゴ代替テキスト（右下装飾）
  s.addText("社外秘", {
    x: 8.5, y: 4.8, w: 1.2, h: 0.4,
    fontSize: 11, color: C.amber, fontFace: "Meiryo",
    align: "center", margin: 0,
    bold: true
  });
}

// ============================================================
// スライド 2: エグゼクティブサマリー
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("エグゼクティブサマリー", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  const cards = [
    {
      icon: "①",
      title: "業界最長水準の買掛金回転日数",
      body: "BYDのサプライヤー支払い日数（DPO）は平均275日。トヨタの44日、テスラの85日と比較して突出して高く、業界中央値66日の約4倍。",
      color: C.red,
    },
    {
      icon: "②",
      title: "急膨張する流動負債・買掛金",
      body: "買掛金は2022年の1,438億元から2024年には2,440億元へ70%増加。GMTリサーチは実質純負債を3,230億元（約4.4兆円）と推計。",
      color: C.blue,
    },
    {
      icon: "③",
      title: "サプライヤーへの深刻な影響",
      body: "タイ・中国で部品メーカーへの支払い遅延が常態化。2025年6月、中国政府が60日支払い義務化を施行——この事実自体が問題の深刻さを示す。",
      color: C.amber,
    },
  ];

  cards.forEach((c, i) => {
    const x = 0.4 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.15, w: 2.9, h: 3.8,
      fill: { color: C.white }, line: { color: C.lightgray, pt: 1 },
      shadow: makeShadow()
    });
    // アクセントバー（上）
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.15, w: 2.9, h: 0.12,
      fill: { color: c.color }, line: { color: c.color }
    });
    // 番号
    s.addText(c.icon, {
      x: x + 0.15, y: 1.35, w: 0.5, h: 0.5,
      fontSize: 26, bold: true, color: c.color, fontFace: "Meiryo", margin: 0
    });
    // タイトル
    s.addText(c.title, {
      x: x + 0.15, y: 1.9, w: 2.6, h: 0.7,
      fontSize: 13, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
    });
    // 本文
    s.addText(c.body, {
      x: x + 0.15, y: 2.65, w: 2.6, h: 2.15,
      fontSize: 11.5, color: C.darkgray, fontFace: "Meiryo", margin: 0, valign: "top"
    });
  });

  // フッター
  s.addText("出所：GMT Research、Bloomberg、BYD Annual Report、Fortune Asia（2025年6月）", {
    x: 0.4, y: 5.2, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 3: BYD財務概要
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("BYD財務概要（2022〜2024年）", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  // KPIカード（上段）
  const kpis = [
    { label: "売上高（2024）", value: "7,771億元", sub: "前年比+23%", color: C.blue },
    { label: "純利益（2024）", value: "402億元", sub: "前年比+34%", color: C.blue },
    { label: "総資産（2024）", value: "8,837億元", sub: "2年で+79%", color: C.navy },
    { label: "総負債（2024）", value: "6,252億元", sub: "総資産比71%", color: C.red },
  ];

  kpis.forEach((k, i) => {
    const x = 0.4 + i * 2.35;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.1, w: 2.2, h: 1.4,
      fill: { color: k.color }, line: { color: k.color },
      shadow: makeShadow()
    });
    s.addText(k.value, {
      x: x + 0.1, y: 1.2, w: 2.0, h: 0.6,
      fontSize: 22, bold: true, color: C.white, fontFace: "Meiryo",
      align: "center", margin: 0
    });
    s.addText(k.label, {
      x: x + 0.1, y: 1.82, w: 2.0, h: 0.35,
      fontSize: 10.5, color: C.iceblue, fontFace: "Meiryo",
      align: "center", margin: 0
    });
    s.addText(k.sub, {
      x: x + 0.1, y: 2.15, w: 2.0, h: 0.28,
      fontSize: 10, color: C.white, fontFace: "Meiryo",
      align: "center", bold: true, margin: 0
    });
  });

  // 流動負債推移グラフ
  s.addText("流動負債・買掛金の推移（単位：億元）", {
    x: 0.5, y: 2.75, w: 5, h: 0.4,
    fontSize: 13, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  s.addChart(pres.charts.BAR, [
    { name: "流動負債合計", labels: ["2022", "2023", "2024"], values: [3334, 4537, 4960] },
    { name: "買掛金",       labels: ["2022", "2023", "2024"], values: [1438, 1985, 2440] },
  ], {
    x: 0.4, y: 3.15, w: 5.8, h: 2.2,
    barDir: "col",
    barGrouping: "clustered",
    chartColors: [C.blue, C.amber],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.darkgray,
    valAxisLabelColor: C.darkgray,
    valGridLine: { color: C.lightgray, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: true,
    legendPos: "b",
    legendFontSize: 10,
    showValue: true,
    dataLabelFontSize: 9,
    dataLabelColor: C.darkgray,
  });

  // 右側補足テキスト
  const bullets = [
    "買掛金は2年間で約70%増加（1,438→2,440億元）",
    "流動負債の買掛金比率：2022年43%→2024年49%に拡大",
    "GMTリサーチ推計による実質純負債：3,230億元（BYD公表値27億元の120倍）",
    "「ディリアン（迪链）」手形システムで4,000億元超の支払手形を発行（2023年5月時点）",
  ];

  s.addText(bullets.map((b, i) => ({
    text: b, options: { bullet: true, breakLine: i < bullets.length - 1, paraSpaceAfter: 8 }
  })), {
    x: 6.5, y: 3.1, w: 3.2, h: 2.3,
    fontSize: 11, color: C.darkgray, fontFace: "Meiryo", valign: "top"
  });

  s.addText("出所：BYD Annual Report 2024、GMT Research 2024", {
    x: 0.4, y: 5.25, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 4: 流動負債 業界比較
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("流動負債比率：業界他社との比較（2024年）", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  // 買掛金 / 総資産 比率
  // BYD: 2440/8837 = 27.6%
  // Toyota: AP ~13T JPY / Total Assets ~88T JPY ≈ 14.8%
  // Tesla: AP $12.5B / Total Assets $106B ≈ 11.8%
  // Geely: AP ~HKD 130B / Total Assets ~HKD 530B ≈ 24.5% (estimated)

  // Let me use absolute accounts payable amounts in their local currencies converted to USD billions for comparison
  // BYD: $33.6B (244B CNY @ 7.27)
  // Toyota: ~$86B JPY accounts payable in FY2024 ≈ ~$57B USD (approximate from macrotrends)
  //   Actually Toyota's AP is about 7-8 trillion yen ≈ $52-57B USD, which is larger in absolute terms
  //   but Toyota's revenue is much larger too
  // Let me use DPO comparison instead, which is clearer

  // Left chart: DPO comparison bar
  s.addText("買掛金回転日数（DPO）比較", {
    x: 0.5, y: 1.0, w: 5.5, h: 0.4,
    fontSize: 14, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  s.addChart(pres.charts.BAR, [
    {
      name: "支払日数（日）",
      labels: ["業界中央値", "トヨタ", "テスラ", "ジーリー", "BYD"],
      values: [66, 44, 80, 168, 275]
    }
  ], {
    x: 0.4, y: 1.4, w: 5.5, h: 3.7,
    barDir: "bar",
    chartColors: [C.lightgray, C.blue, C.blue, C.amber, C.red],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.darkgray,
    valAxisLabelColor: C.darkgray,
    valGridLine: { color: C.lightgray, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: false,
    showValue: true,
    dataLabelPosition: "outEnd",
    dataLabelFontSize: 11,
    dataLabelColor: C.darkgray,
    valAxisMaxVal: 320,
    valAxisMinVal: 0,
  });

  // Right: commentary cards
  const insights = [
    { color: C.red,   icon: "!", label: "BYD", text: "275日（業界中央値の4.2倍）。サプライヤーは平均9ヶ月間、売掛金を回収できない。" },
    { color: C.amber, icon: "△", label: "Geely", text: "168日。BYDより短いが、同じく中国メーカーとして業界平均を大きく超えている。" },
    { color: C.blue,  icon: "○", label: "Toyota", text: "44日。長期的なサプライヤー関係重視のJIT調達を反映した水準。" },
    { color: C.blue,  icon: "○", label: "Tesla", text: "80日。急成長フェーズにしては管理された水準。近年改善傾向。" },
  ];

  insights.forEach((item, i) => {
    const y = 1.0 + i * 1.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.15, y, w: 3.5, h: 0.95,
      fill: { color: C.white }, line: { color: C.lightgray, pt: 1 },
      shadow: makeShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.15, y, w: 0.07, h: 0.95,
      fill: { color: item.color }, line: { color: item.color }
    });
    s.addText(`${item.icon} ${item.label}`, {
      x: 6.3, y: y + 0.05, w: 3.2, h: 0.3,
      fontSize: 13, bold: true, color: item.color, fontFace: "Meiryo", margin: 0
    });
    s.addText(item.text, {
      x: 6.3, y: y + 0.35, w: 3.2, h: 0.55,
      fontSize: 10.5, color: C.darkgray, fontFace: "Meiryo", margin: 0, valign: "top"
    });
  });

  s.addText("出所：Bloomberg、GuruFocus、GMT Research（2023〜2024年データ）", {
    x: 0.4, y: 5.25, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 5: DPO推移（3年比較）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("買掛金残高と支払日数のトレンド比較（2022〜2024年）", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 24, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  // Left: AP balance trend
  s.addText("BYD買掛金残高推移（億元）", {
    x: 0.5, y: 1.1, w: 4.5, h: 0.4,
    fontSize: 13, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  s.addChart(pres.charts.LINE, [
    { name: "買掛金（億元）", labels: ["2022", "2023", "2024"], values: [1438, 1985, 2440] },
  ], {
    x: 0.4, y: 1.5, w: 4.5, h: 2.8,
    lineSize: 4,
    lineSmooth: false,
    chartColors: [C.red],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.darkgray,
    valAxisLabelColor: C.darkgray,
    valGridLine: { color: C.lightgray, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: false,
    showValue: true,
    dataLabelFontSize: 11,
    dataLabelColor: C.red,
  });

  // Right: DPO trend comparison
  s.addText("各社DPO比較（日）", {
    x: 5.2, y: 1.1, w: 4.5, h: 0.4,
    fontSize: 13, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  s.addChart(pres.charts.LINE, [
    { name: "BYD",    labels: ["2022", "2023", "2024"], values: [220, 275, 270] },
    { name: "Geely",  labels: ["2022", "2023", "2024"], values: [158, 204, 168] },
    { name: "Tesla",  labels: ["2022", "2023", "2024"], values: [76, 79, 80] },
    { name: "Toyota", labels: ["2022", "2023", "2024"], values: [50, 47, 44] },
  ], {
    x: 5.1, y: 1.5, w: 4.5, h: 2.8,
    lineSize: 3,
    lineSmooth: true,
    chartColors: [C.red, C.amber, C.blue, "27AE60"],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.darkgray,
    valAxisLabelColor: C.darkgray,
    valGridLine: { color: C.lightgray, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: true,
    legendPos: "b",
    legendFontSize: 10,
    showValue: false,
  });

  // Bottom annotation
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 4.55, w: 9.2, h: 0.85,
    fill: { color: "FEF3C7" }, line: { color: "F59E0B", pt: 1 }
  });
  s.addText(
    "⚠️  注目点：BYDは2023年に275日のピークに達した後も改善傾向は見られず、競合他社との格差が拡大。「60日規制」施行（2025年6月）の実効性が今後の焦点。",
    {
      x: 0.6, y: 4.6, w: 8.8, h: 0.75,
      fontSize: 12, color: "92400E", fontFace: "Meiryo", margin: 0, valign: "middle"
    }
  );

  s.addText("出所：Bloomberg DPO推計、StockAnalysis、GuruFocus", {
    x: 0.4, y: 5.25, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 6: サプライヤー支払い遅延の実態
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("サプライヤー支払い遅延の実態", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  // Timeline visual
  const timelineItems = [
    { month: "納品\n（0日）",       desc: "部品をBYDへ納入。\nサプライヤーの資金\n拘束が始まる。",        color: C.blue },
    { month: "3〜6ヶ月後",         desc: "「ディリアン」電子手形\nを受領（現金ではない）。\n換金には割引手数料が必要。", color: C.amber },
    { month: "6〜9ヶ月後",         desc: "手形の支払期限到来。\nようやく代金受取りの\n可能性が生じる。",     color: C.amber },
    { month: "最長275日後",         desc: "平均的な最終回収日。\n原材料費・人件費は\n既に支払済み。",       color: C.red },
  ];

  timelineItems.forEach((item, i) => {
    const x = 0.4 + i * 2.35;
    // Circle
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.7, y: 1.1, w: 0.7, h: 0.7,
      fill: { color: item.color }, line: { color: item.color }
    });
    s.addText(`${i + 1}`, {
      x: x + 0.7, y: 1.1, w: 0.7, h: 0.7,
      fontSize: 18, bold: true, color: C.white, fontFace: "Meiryo",
      align: "center", valign: "middle", margin: 0
    });
    // Arrow (except last)
    if (i < 3) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x + 1.55, y: 1.4, w: 0.75, h: 0.07,
        fill: { color: C.lightgray }, line: { color: C.lightgray }
      });
    }
    // Label
    s.addText(item.month, {
      x, y: 1.85, w: 2.2, h: 0.6,
      fontSize: 11, bold: true, color: item.color, fontFace: "Meiryo",
      align: "center", margin: 0
    });
    // Description box
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 2.5, w: 2.2, h: 1.5,
      fill: { color: C.white }, line: { color: C.lightgray, pt: 1 },
      shadow: makeShadow()
    });
    s.addText(item.desc, {
      x: x + 0.1, y: 2.55, w: 2.0, h: 1.4,
      fontSize: 10.5, color: C.darkgray, fontFace: "Meiryo", valign: "top", margin: 0
    });
  });

  // Key facts row
  const facts = [
    { num: "3,230億元", label: "GMT推計の実質純負債額\nBYD公表値の約120倍", color: C.red },
    { num: "4,000億元", label: "「ディリアン」手形\n発行残高（2023年5月）", color: C.amber },
    { num: "10%", label: "2025年向けに\nサプライヤーへ要求した値下げ幅", color: C.amber },
  ];

  facts.forEach((f, i) => {
    const x = 0.5 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.2, w: 2.9, h: 0.9,
      fill: { color: f.color }, line: { color: f.color },
      shadow: makeShadow()
    });
    s.addText(f.num, {
      x: x + 0.1, y: 4.22, w: 1.2, h: 0.85,
      fontSize: 22, bold: true, color: C.white, fontFace: "Meiryo",
      align: "center", valign: "middle", margin: 0
    });
    s.addText(f.label, {
      x: x + 1.3, y: 4.22, w: 1.5, h: 0.85,
      fontSize: 9.5, color: C.white, fontFace: "Meiryo",
      valign: "middle", margin: 0
    });
  });

  s.addText("出所：GMT Research、Fortune Asia、Bloomberg、newfortunetimes.com", {
    x: 0.4, y: 5.25, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 7: タイ自動車産業への影響
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("タイ自動車産業への影響", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  // Left: map/text area
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.1, w: 4.4, h: 4.2,
    fill: { color: C.white }, line: { color: C.lightgray, pt: 1 },
    shadow: makeShadow()
  });

  s.addText("タイの自動車産業の構図", {
    x: 0.55, y: 1.2, w: 4.1, h: 0.45,
    fontSize: 14, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  const thaiPoints = [
    "タイはASEAN最大の自動車生産拠点（年間約200万台）",
    "従来は日本メーカーが市場の約9割を占有",
    "中国EVは2023年から本格進出、2024年には市場シェア1割以上を奪取",
    "BYDはラヨーン県に工場開設（2024年7月）、雇用1万人予定",
    "BYD EV販売は中国製部品を優先——タイの現地部品は価格で約30%高く、現地調達が進まない",
    "日系サプライヤーの証言：「契約書も連絡も中国語。平気で買いたたき、支払期日も守らない」",
  ];

  s.addText(thaiPoints.map((p, i) => ({
    text: p, options: { bullet: true, breakLine: i < thaiPoints.length - 1, paraSpaceAfter: 6 }
  })), {
    x: 0.55, y: 1.7, w: 4.1, h: 3.4,
    fontSize: 11, color: C.darkgray, fontFace: "Meiryo", valign: "top"
  });

  // Right: impact metrics
  s.addText("タイへの経済的インパクト", {
    x: 5.1, y: 1.1, w: 4.5, h: 0.45,
    fontSize: 14, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  const impacts = [
    { num: "10万人以上", label: "自動車関連雇用の\n削減リスク（2025〜2026年）", color: C.red },
    { num: "30%", label: "タイ現地調達コストの\n中国輸入品比割高率", color: C.amber },
    { num: "70%超", label: "中国ブランドが占める\nタイのBEV市場シェア", color: C.blue },
    { num: "14億ドル", label: "中国EVメーカーの\nタイへの累計投資額", color: C.blue },
  ];

  impacts.forEach((item, i) => {
    const row = Math.floor(i / 2);
    const col = i % 2;
    const x = 5.1 + col * 2.2;
    const y = 1.65 + row * 1.75;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.1, h: 1.55,
      fill: { color: item.color }, line: { color: item.color },
      shadow: makeShadow()
    });
    s.addText(item.num, {
      x: x + 0.08, y: y + 0.1, w: 1.94, h: 0.7,
      fontSize: 18, bold: true, color: C.white, fontFace: "Meiryo",
      align: "center", margin: 0
    });
    s.addText(item.label, {
      x: x + 0.08, y: y + 0.8, w: 1.94, h: 0.68,
      fontSize: 10, color: C.white, fontFace: "Meiryo",
      align: "center", valign: "top", margin: 0
    });
  });

  s.addText("出所：Marketplace（2025年1月）、日経ビジネス（2024年）、Thailand EV Industry Report 2025", {
    x: 0.4, y: 5.25, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 8: 中国政府の規制対応
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("規制当局の対応と今後の課題", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  // Timeline: regulatory actions
  const events = [
    {
      date: "2023年\n〜2024年",
      title: "問題の顕在化",
      desc: "GMT ResearchがBYDの実質純負債を3,230億元と推計。Bloomberg調査でDPO275日が確認される。中小サプライヤーの資金繰り悪化が深刻化。",
      color: C.amber
    },
    {
      date: "2024年\n11月",
      title: "BYDが10%値下げ要求",
      desc: "BYDが全サプライヤーに対して2025年向けに10%のコスト削減を要求する内部通達。品質劣化への懸念が表面化。",
      color: C.amber
    },
    {
      date: "2025年\n3月",
      title: "中国政府が規制発表",
      desc: "大企業による中小企業への支払いを60日以内とする「中小企業代金支払保障条例」を公布。6月1日施行を決定。",
      color: C.blue
    },
    {
      date: "2025年\n6月",
      title: "17社が60日宣言",
      desc: "BYD、Geely、奇瑞、小鵬ら17社が支払い期間60日以内を表明。ただし手形払い禁止の実効性についてサプライヤーは懐疑的。",
      color: C.blue
    },
  ];

  events.forEach((ev, i) => {
    const x = 0.4 + i * 2.35;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.1, w: 2.2, h: 3.8,
      fill: { color: C.white }, line: { color: C.lightgray, pt: 1 },
      shadow: makeShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.1, w: 2.2, h: 0.1,
      fill: { color: ev.color }, line: { color: ev.color }
    });
    s.addText(ev.date, {
      x: x + 0.1, y: 1.25, w: 2.0, h: 0.55,
      fontSize: 13, bold: true, color: ev.color, fontFace: "Meiryo",
      align: "center", margin: 0
    });
    s.addText(ev.title, {
      x: x + 0.1, y: 1.82, w: 2.0, h: 0.5,
      fontSize: 12, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.1, y: 2.35, w: 1.9, h: 0.03,
      fill: { color: C.lightgray }, line: { color: C.lightgray }
    });
    s.addText(ev.desc, {
      x: x + 0.1, y: 2.45, w: 2.0, h: 2.35,
      fontSize: 10.5, color: C.darkgray, fontFace: "Meiryo", valign: "top", margin: 0
    });
  });

  // Bottom note
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 4.65, w: 9.2, h: 0.5,
    fill: { color: "EFF6FF" }, line: { color: C.blue, pt: 1 }
  });
  s.addText(
    "課題：BYDは手形（ディリアン）によるファイナンスを通じて実質的な支払い延長を継続。現金60日ルールの抜け穴となる可能性があり、実効性に疑問が残る。",
    {
      x: 0.6, y: 4.67, w: 8.8, h: 0.46,
      fontSize: 11, color: C.blue, fontFace: "Meiryo", margin: 0, valign: "middle"
    }
  );

  s.addText("出所：中国国務院、JETRO（2025年6月）、CnEVPost、東洋経済オンライン", {
    x: 0.4, y: 5.22, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 9: 財務リスクの示唆
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("財務リスクと投資・事業上の示唆", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Meiryo", margin: 0
  });

  const risks = [
    {
      category: "財務リスク",
      color: C.red,
      items: [
        "純負債の過小表示：BYD公表値と第三者推計値に最大120倍の乖離",
        "規制施行で買掛金ファイナンスが縮小→運転資本需要が急増するリスク",
        "格付機関・投資家による財務透明性への疑念が高まりつつある",
      ]
    },
    {
      category: "サプライチェーンリスク",
      color: C.amber,
      items: [
        "中小サプライヤーの経営悪化→部品品質低下・供給停止リスク",
        "10%値下げ圧力による技術投資余力の喪失",
        "タイ等海外でのサプライヤー確保困難（現地調達率の低さ）",
      ]
    },
    {
      category: "戦略・競合リスク",
      color: C.blue,
      items: [
        "中国政府規制による低コスト調達モデルの持続可能性に疑問符",
        "トヨタ・VW等の安定したサプライヤー関係との競争力格差",
        "海外展開（タイ・欧州）でのレピュテーションリスク上昇",
      ]
    },
  ];

  risks.forEach((r, i) => {
    const x = 0.4 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.1, w: 2.95, h: 4.1,
      fill: { color: C.white }, line: { color: r.color, pt: 1.5 },
      shadow: makeShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.1, w: 2.95, h: 0.55,
      fill: { color: r.color }, line: { color: r.color }
    });
    s.addText(r.category, {
      x: x + 0.1, y: 1.13, w: 2.75, h: 0.5,
      fontSize: 14, bold: true, color: C.white, fontFace: "Meiryo",
      align: "center", valign: "middle", margin: 0
    });
    s.addText(r.items.map((item, j) => ({
      text: item, options: { bullet: true, breakLine: j < r.items.length - 1, paraSpaceAfter: 10 }
    })), {
      x: x + 0.12, y: 1.75, w: 2.72, h: 3.35,
      fontSize: 11, color: C.darkgray, fontFace: "Meiryo", valign: "top"
    });
  });

  s.addText("出所：本分析を通じた各種公開情報の統合", {
    x: 0.4, y: 5.25, w: 9.2, h: 0.3,
    fontSize: 9, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 10: 結論
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // 左アクセント
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.25, h: 5.625,
    fill: { color: C.amber }, line: { color: C.amber }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.25, y: 0, w: 9.75, h: 0.06,
    fill: { color: C.iceblue }, line: { color: C.iceblue }
  });

  s.addText("結論", {
    x: 0.7, y: 0.35, w: 8.5, h: 0.65,
    fontSize: 34, bold: true, color: C.white, fontFace: "Meiryo", margin: 0
  });

  const conclusions = [
    {
      num: "1",
      text: "BYDの流動負債・買掛金はトヨタ・テスラを大幅に上回り、DPO275日は業界中央値（66日）の4倍超。この「隠れた負債」モデルが成長を支えてきた。",
      color: C.amber
    },
    {
      num: "2",
      text: "サプライヤーへの実害は深刻——323億ドル超の支払い遅延、10%の値下げ強要、手形によるファイナンス転嫁は中小企業の存続を脅かす水準。",
      color: C.red
    },
    {
      num: "3",
      text: "タイを含む海外でも同様の圧力が現地サプライヤーに及んでいる。中国製部品優先により現地調達が進まず、産業空洞化を加速するリスク。",
      color: "27AE60"
    },
    {
      num: "4",
      text: "中国政府の60日規制（2025年6月施行）は一歩前進だが、手形払いの抜け穴への懸念は残る。財務モデルの持続可能性を引き続き注視すべき。",
      color: "00B4D8"
    },
  ];

  conclusions.forEach((c, i) => {
    const y = 1.15 + i * 1.05;
    s.addShape(pres.shapes.OVAL, {
      x: 0.6, y: y + 0.05, w: 0.45, h: 0.45,
      fill: { color: c.color }, line: { color: c.color }
    });
    s.addText(c.num, {
      x: 0.6, y: y + 0.05, w: 0.45, h: 0.45,
      fontSize: 16, bold: true, color: C.navy, fontFace: "Meiryo",
      align: "center", valign: "middle", margin: 0
    });
    s.addText(c.text, {
      x: 1.2, y, w: 8.2, h: 0.95,
      fontSize: 12.5, color: C.white, fontFace: "Meiryo", valign: "middle", margin: 0
    });
  });

  s.addText("2026年6月　経営企画部", {
    x: 0.7, y: 5.15, w: 8.5, h: 0.35,
    fontSize: 11, color: C.gray, fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// 生の声スライド共通ヘルパー
// ============================================================
function qBlock(slide, y, quote, attrib, borderColor, qH, gap) {
  if (gap === undefined) gap = 0.15;
  const totalH = qH + 0.28;
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: y, w: 0.04, h: totalH,
    fill: { color: borderColor }, line: { color: borderColor }
  });
  slide.addText(quote, {
    x: 0.58, y: y + 0.03, w: 9.08, h: qH,
    fontSize: 12, color: "1E293B", fontFace: "Meiryo", margin: 0, valign: "top"
  });
  slide.addText(attrib, {
    x: 0.58, y: y + qH + 0.05, w: 9.08, h: 0.24,
    fontSize: 9, color: "94A3B8", fontFace: "Meiryo", margin: 0
  });
  return y + totalH + gap;
}

function voiceSlideTitle(slide, num, title) {
  slide.addText("生の声 " + num + "　" + title, {
    x: 0.4, y: 0.2, w: 9.2, h: 0.38,
    fontSize: 13, bold: true, color: "334155", fontFace: "Meiryo", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.58, w: 9.2, h: 0.02,
    fill: { color: "E2E8F0" }, line: { color: "E2E8F0" }
  });
}

function voiceFooter(slide, source) {
  slide.addText("出所：" + source, {
    x: 0.4, y: 5.3, w: 9.2, h: 0.25,
    fontSize: 8.5, color: "94A3B8", fontFace: "Meiryo", margin: 0
  });
}

// ============================================================
// スライド 11: 生の声① 中国 大手・業界首脳（実名）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  voiceSlideTitle(s, "①", "中国：大手サプライヤー・業界首脳（実名発言）");

  let y = 0.72;

  y = qBlock(s, y,
    "「BYDの現在のやり方は商業倫理に反するだけでなく、中国の労働者の勤勉さと底力、そして国内サプライヤーの生存能力を底なしに消耗させている」",
    "Sensata Technologies（センサー大手）｜ 腾讯ニュース 2024年12月 ｜ BYDの10%値下げ要求に対する公開反論",
    "C0392B", 0.60
  );

  y = qBlock(s, y,
    "「常軌を逸したコスト削減は、一部のメーカーに手抜きや偽装を強いることになる」",
    "魏建軍（長城汽車 董事長）｜ 2024年12月 ｜ 業界の価格戦争を公開批判",
    "64748B", 0.40
  );

  y = qBlock(s, y,
    "「価格戦争が続くほど（価格が）安くなり、品質が悪くなり、サービス体験も劣化する」",
    "李書福（吉利汽車 董事長）｜ 2024年 ｜ 業界全体の価格競争を警告",
    "64748B", 0.40
  );

  y = qBlock(s, y,
    "\"Everybody's suffering.\" ——「誰もが苦しんでいる」。支払い遅延は3次・4次サプライヤーにまで波及しており、彼らにはコストをさらに下に転嫁する力すらない。",
    "Jochen Siebert（JSC Automotive Consultancy 代表）｜ Caixin Global 2024年5月",
    "64748B", 0.60
  );

  voiceFooter(s, "腾讯ニュース（2024/12）、Caixin Global（2024/5）");
}

// ============================================================
// スライド 12: 生の声② 中国 匿名・仮名サプライヤーの証言
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  voiceSlideTitle(s, "②", "中国：匿名・仮名サプライヤーの証言（取材・調査報道より）");

  let y = 0.72;

  y = qBlock(s, y,
    "「以前、合弁ブランド（日系等）は四半期ごとに期日通りに払ってくれた。国内ブランドはもともと支払いが遅いが、今や私たちは強制的に長い回収サイクルを受け入れるしかない」",
    "匿名サプライヤー｜ Bloomberg調査取材 2024年",
    "E67E22", 0.58, 0.12
  );

  y = qBlock(s, y,
    "「サプライヤーは現金決済を望んでいる。商業手形への切り替えは（ディリアン廃止と比べて）『スープは変わったが中身は同じ』だ。ただ法的保障と透明性の点ではましになる」",
    "李云氏（自動車照明サプライヤー・仮名）｜ Sina Finance 2025年11月 ｜ BYDのディリアン廃止に際しての発言",
    "E67E22", 0.58, 0.12
  );

  y = qBlock(s, y,
    "「最も直接的で速いコスト削減方法は、材料の品質を下げることだ」",
    "匿名材料サプライヤー｜ Sina Finance 2024年11月 ｜ BYDの10%値下げ要求を受けて",
    "E67E22", 0.38, 0.12
  );

  y = qBlock(s, y,
    "「材料コストの限界まで削減すれば、製品品質が保証できるかどうかは言えなくなる」",
    "（同上）匿名材料サプライヤー｜ Sina Finance 2024年11月",
    "E67E22", 0.38, 0.12
  );

  y = qBlock(s, y,
    "「ディリアンは確かに使われなくなった。契約も変更した。ただしこれは中小零細向けの話で、大口取引先はまだ（旧来の）手形扱いのままだ」",
    "匿名サプライヤー｜ Sina Finance 2025年11月 ｜ BYDのディリアン廃止発表後",
    "E67E22", 0.55
  );

  voiceFooter(s, "Bloomberg調査（2024）、Sina Finance（2024/11・2025/11）");
}

// ============================================================
// スライド 13: 生の声③ タイ 消費者・現地の声
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  voiceSlideTitle(s, "③", "タイ：消費者・エンドユーザーの声（SNS・掲示板）");

  let y = 0.72;

  y = qBlock(s, y,
    "「BYD Atto3を納車6ヶ月でPDC部品の交換が必要になった。バンコクのサービスセンターが『部品を購入する資金がない』と回答。BYDタイランド社に5〜6回連絡したが10日経っても返事なし。ディーラーとメーカー間の内部問題が原因だと言う」",
    "Pantip掲示板ユーザー「Adios2nd」（BYD Atto3オーナー）｜ topic/43266071",
    "2E8B57", 0.78
  );

  y = qBlock(s, y,
    "「BYDのクレーム対応に心底うんざりした。フロントガラスを3ヶ月待ち、次はサンルーフをさらに4ヶ月待ち中。今後は一生BYDは購入しない（個人の強い意志）」",
    "Pantip掲示板ユーザー（匿名・BYD Dolphinオーナー）｜ topic/43580243（スレッドタイトルより）",
    "2E8B57", 0.58
  );

  y = qBlock(s, y,
    "\"The customer service department in head office in Bangkok is dreadful.\"（バンコク本社のカスタマーサービス部門はひどい）",
    "BYD Thailand Facebookグループ（公開投稿）｜ posts/1178376214269158",
    "2E8B57", 0.45
  );

  y = qBlock(s, y,
    "「（BYDの工場があるのに）アフターマーケット部品のほとんどは中国からの輸入品。事故で損傷した高電圧部品・ブレードバッテリーは入荷がバッチ制で、修理を数ヶ月待つことになる。代車の待ち行列まで発生している」",
    "Pantip・SuperBikeMag（複数ユーザーのコメント集約）｜ 2025〜2026年",
    "2E8B57", 0.75
  );

  voiceFooter(s, "Pantip.com（2024〜2026）、Facebook BYD Thailandグループ、SuperBikeMag（2026/1）");
}

// ============================================================
// スライド 14: 生の声④ 日系企業・業界専門家・業界団体
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  voiceSlideTitle(s, "④", "日系企業・業界専門家・業界団体の声");

  let y = 0.72;

  y = qBlock(s, y,
    "「普段のやりとりも契約書も中国語。平気で買いたたいてくるし、支払期日も守らない」",
    "日系企業駐在員（タイ在籍）｜ 日経ビジネス 2024年8月 ｜ BYDタイランドとの取引について",
    "1E2761", 0.42
  );

  y = qBlock(s, y,
    "「サプライヤーへの支払い期間は（自動車メーカーの）財務的健全性の指標だ。支払いサイクルの延長は流動性の問題を抱えており、現金フロー管理を調整せざるを得ない状況を示している」",
    "David Zhang（WDEF デジタル自動車国際協力研究センター 所長）｜ Caixin Global 2024年5月",
    "1E2761", 0.60
  );

  y = qBlock(s, y,
    "「一部の自動車メーカーは独自のサプライチェーンファイナンスプラットフォームを使い、約束手形で決済することで実質的にサプライヤーへの支払いを何ヶ月も遅らせている。利益余地はほとんどなく、流動性の圧力は増大している」",
    "中国鉄鋼工業協会（CISA）｜ 声明 2025年 ｜ 自動車メーカーへの鉄鋼価格10%以上引き下げ要求も合わせて批判",
    "1E2761", 0.78
  );

  y = qBlock(s, y,
    "「国際的な自動車メーカー、特に日本のメーカーは、長期的・緊密・安定したサプライヤーとのパートナーシップを確立している。コストをコントロールしながら、サプライヤーに合理的な利益余地を残している」",
    "中国鉄鋼工業協会（CISA）｜ 日系・欧州系メーカーとの比較として言及",
    "1E2761", 0.65
  );

  voiceFooter(s, "日経ビジネス（2024/8）、Caixin Global（2024/5）、中国鉄鋼工業協会（2025）");
}

// ============================================================
// スライド 15: 最近の話題（2025年末〜2026年）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };

  s.addText("最近の話題　2025年末〜2026年現在", {
    x:0.4, y:0.15, w:9.2, h:0.38,
    fontSize:13, bold:true, color:"334155", fontFace:"Meiryo", margin:0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.4, y:0.53, w:9.2, h:0.02,
    fill:{color:"E2E8F0"}, line:{color:"E2E8F0"}
  });
  s.addText("財務リスク関連の主要動向を時系列で整理。規制・業績悪化・サプライヤー問題が同時進行中。", {
    x:0.4, y:0.57, w:9.2, h:0.22,
    fontSize:9.5, color:"64748B", fontFace:"Meiryo", margin:0
  });

  const topics = [
    {
      date:"2025.01", tag:"GMT調査", tagC:"DC2626",
      title:"「隠れ負債3,230億元（6.6兆円）」警告",
      body:"GMT Research報告書。公式純負債27.7億元（0.4兆円）に対し、Dチェーン等のオフバランス項目を加算すると実態約3,230億元と指摘。乖離は約117倍。「中国の恒大と同じ道」と警告。",
      src:"GMT Research / Bloomberg 2025.01.19",
    },
    {
      date:"2025.06", tag:"政府規制", tagC:"1D4ED8",
      title:"「60日以内支払い」義務化が施行",
      body:"中国国務院「中小企業代金支払保障条例」が6/1施行。大企業→中小サプライヤーへの支払いを60日以内に義務化。BYD仕入れ債務は約5兆円規模で、60日化により年最大4,000億円のコスト増との試算も。",
      src:"中国国務院 / 日本経済新聞 2025.06",
    },
    {
      date:"2025.06", tag:"サプライヤー", tagC:"D97706",
      title:"17社が60日宣言、現場はなお懐疑的",
      body:"BYDを含む17社が60日支払いを連名表明（6/10〜11）。ただし「60日現金払い＋SCファイナンス180日」の組み合わせで実質支払いを先送りできる抜け穴の存在を専門家が指摘。Bloomberg「仕入れ先はなお懐疑的」。",
      src:"Bloomberg 2025.06.17 / CnEVPost 2025.06.11",
    },
    {
      date:"2025.Q3", tag:"業績悪化", tagC:"7C3AED",
      title:"22四半期ぶりの減収減益",
      body:"2025年7〜9月期：純利益 前年比33%減（78億元）、売上高 同3.1%減。粗利益率は21.9%→17.6%（▲4.3pt）に急低下。中国国内の価格競争激化＋研究開発費31%急増が同時に利益を圧迫。",
      src:"BYD決算発表 / 東洋経済・日経 2025.10",
    },
    {
      date:"2025.11", tag:"Dチェーン廃止", tagC:"059669",
      title:"迪链（Dチェーン）を段階的停止へ",
      body:"BYDが累計発行4,000億元（5.5兆円）超のDチェーンを段階的に廃止すると発表。中小向けから銀行振込・商業手形に移行開始。「大口取引先は依然として旧方式」との匿名サプライヤーの声（Caixin 12月）。",
      src:"Caixin Global 2025.12.05 / Seeking Alpha 2025.11",
    },
    {
      date:"2026", tag:"現在進行中", tagC:"475569",
      title:"構造問題は継続、不確実性は解消せず",
      body:"Dチェーン廃止で「表向きの支払い改善」は進むも、巨額仕入れ債務・価格競争・収益圧縮は未解決。2026/5報告では275日待機または6%早期換金ペナルティという実態がなお存在。",
      src:"Fingerlakes1.com 2026.05.05 / BCR Publishing 2026",
    },
  ];

  topics.forEach((t, i) => {
    const col = i%2, row = Math.floor(i/2);
    const x = 0.25 + col*4.88;
    const y = 0.83 + row*1.58;
    const w = 4.65, h = 1.48;

    // カード背景
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h,
      fill:{color:"F8FAFC"}, line:{color:"E2E8F0", pt:0.75}
    });
    // 左カラーバー
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:0.04, h,
      fill:{color:t.tagC}, line:{color:t.tagC}
    });
    // 日付バッジ
    s.addShape(pres.shapes.RECTANGLE, {
      x:x+0.09, y:y+0.08, w:0.72, h:0.22,
      fill:{color:t.tagC}, line:{color:t.tagC}
    });
    s.addText(t.date, {
      x:x+0.09, y:y+0.08, w:0.72, h:0.22,
      fontSize:8, bold:true, color:"FFFFFF", fontFace:"Meiryo",
      align:"center", margin:0
    });
    // タグ
    s.addText(t.tag, {
      x:x+0.86, y:y+0.09, w:1.5, h:0.20,
      fontSize:8, bold:true, color:t.tagC, fontFace:"Meiryo", margin:0
    });
    // タイトル
    s.addText(t.title, {
      x:x+0.09, y:y+0.33, w:w-0.18, h:0.24,
      fontSize:10, bold:true, color:"1E293B", fontFace:"Meiryo", margin:0
    });
    // 本文
    s.addText(t.body, {
      x:x+0.09, y:y+0.59, w:w-0.18, h:0.64,
      fontSize:8.5, color:"334155", fontFace:"Meiryo", margin:0, valign:"top"
    });
    // 出所
    s.addText(t.src, {
      x:x+0.09, y:y+1.26, w:w-0.18, h:0.20,
      fontSize:7.5, color:"94A3B8", fontFace:"Meiryo", margin:0
    });
  });
}

// ============================================================
// 出力
// ============================================================
pres.writeFile({ fileName: "BYD財務リスク分析_v2.pptx" }).then(() => {
  console.log("✅ 作成完了: BYD財務リスク分析_v2.pptx");
}).catch(err => {
  console.error("❌ エラー:", err);
});
