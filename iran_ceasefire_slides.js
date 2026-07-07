const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "米国・イラン休戦協定：分析と今後のリスク";

// Color palette - "Midnight Executive" adapted for geopolitics
const C = {
  navy:    "1A2B52",   // dominant dark
  midBlue: "2E4A82",   // secondary
  gold:    "C9A84C",   // accent
  lightBg: "F0F4FA",   // content slide bg
  white:   "FFFFFF",
  text:    "1A2B52",
  muted:   "5B6F8A",
  danger:  "C0392B",
  warn:    "D4850A",
  safe:    "1E7D4E",
  cardBg:  "FFFFFF",
};

const makeShadow = () => ({ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.12 });

// ─────────────────────────────────────────────
// SLIDE 1: Title
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // Gold accent stripe top
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.07, fill: { color: C.gold }, line: { color: C.gold } });

  // Subtle grid pattern via shapes
  for (let i = 0; i < 5; i++) {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0.07 + i * 1.1, w: 10, h: 0.5,
      fill: { color: "FFFFFF", transparency: 96 }, line: { color: C.navy }
    });
  }

  // Eyebrow
  s.addText("CONFIDENTIAL POLICY BRIEF", {
    x: 0.7, y: 1.2, w: 8.6, h: 0.4,
    fontSize: 11, fontFace: "Calibri", color: C.gold, bold: true, charSpacing: 4, align: "center", margin: 0
  });

  // Main title
  s.addText("米国・イラン休戦協定", {
    x: 0.5, y: 1.7, w: 9, h: 1.1,
    fontSize: 46, fontFace: "Georgia", color: C.white, bold: true, align: "center", margin: 0
  });

  // Subtitle
  s.addText("合意内容の分析・60日間交渉シナリオ・今後のリスク評価", {
    x: 0.5, y: 2.85, w: 9, h: 0.55,
    fontSize: 16, fontFace: "Calibri", color: "CADCFC", align: "center", margin: 0
  });

  // Divider
  s.addShape(pres.shapes.RECTANGLE, { x: 3.5, y: 3.5, w: 3, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });

  // Meta info
  s.addText("作成日：2026年6月18日　　分類：国際政治分析レポート", {
    x: 0.5, y: 3.65, w: 9, h: 0.35,
    fontSize: 12, fontFace: "Calibri", color: "8FA9D0", align: "center", margin: 0
  });

  // Bottom accent
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.55, w: 10, h: 0.075, fill: { color: C.gold }, line: { color: C.gold } });
}

// ─────────────────────────────────────────────
// SLIDE 2: 目次
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addText("目　次", {
    x: 0.6, y: 0.3, w: 8.8, h: 0.7,
    fontSize: 32, fontFace: "Georgia", color: C.white, bold: true, margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.05, w: 1.5, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });

  const items = [
    ["01", "休戦協定の背景と経緯"],
    ["02", "合意内容の主要条件"],
    ["03", "地政学的影響分析"],
    ["04", "60日間交渉シナリオ"],
    ["05", "リスク評価マトリクス"],
    ["06", "今後の展望と政策提言"],
  ];

  items.forEach(([num, title], i) => {
    const col = i < 3 ? 0 : 1;
    const row = i % 3;
    const x = col === 0 ? 0.6 : 5.3;
    const y = 1.25 + row * 1.3;

    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.3, h: 1.1, fill: { color: C.midBlue }, line: { color: C.midBlue }, shadow: makeShadow() });
    s.addText(num, { x: x + 0.15, y: y + 0.1, w: 0.7, h: 0.45, fontSize: 22, fontFace: "Georgia", color: C.gold, bold: true, margin: 0 });
    s.addText(title, { x: x + 0.9, y: y + 0.18, w: 3.2, h: 0.7, fontSize: 14, fontFace: "Calibri", color: C.white, bold: true, valign: "middle", margin: 0 });
  });
}

// ─────────────────────────────────────────────
// SLIDE 3: 背景と経緯
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };

  // Header bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.95, fill: { color: C.navy }, line: { color: C.navy } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.95, w: 10, h: 0.06, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("01　休戦協定の背景と経緯", { x: 0.4, y: 0.15, w: 9, h: 0.65, fontSize: 22, fontFace: "Georgia", color: C.white, bold: true, margin: 0 });

  // Timeline
  const events = [
    { year: "2025年", label: "イスラエル・ハマス停戦崩壊、イラン核施設への圧力強化" },
    { year: "2026年初頭", label: "米国・イラン間の秘密外交チャンネル再開（オマーン仲介）" },
    { year: "2026年3月", label: "イランの濃縮ウラン60%→20%への自主的削減発表" },
    { year: "2026年5月", label: "ジュネーブにて予備交渉開始、IAEA査察受入れ合意" },
    { year: "2026年6月", label: "休戦協定署名（ドーハ）―60日間包括協定交渉を開始" },
  ];

  events.forEach((ev, i) => {
    const y = 1.2 + i * 0.82;
    // Timeline dot
    s.addShape(pres.shapes.OVAL, { x: 0.5, y: y + 0.1, w: 0.28, h: 0.28, fill: { color: C.gold }, line: { color: C.gold } });
    // Connector line (except last)
    if (i < events.length - 1) {
      s.addShape(pres.shapes.RECTANGLE, { x: 0.625, y: y + 0.38, w: 0.03, h: 0.55, fill: { color: "CADCFC" }, line: { color: "CADCFC" } });
    }
    // Year badge
    s.addShape(pres.shapes.RECTANGLE, { x: 0.95, y: y + 0.04, w: 1.55, h: 0.3, fill: { color: C.navy }, line: { color: C.navy } });
    s.addText(ev.year, { x: 0.95, y: y + 0.04, w: 1.55, h: 0.3, fontSize: 10.5, fontFace: "Calibri", color: C.gold, bold: true, align: "center", valign: "middle", margin: 0 });
    // Description
    s.addText(ev.label, { x: 2.65, y: y + 0.03, w: 7.1, h: 0.38, fontSize: 13, fontFace: "Calibri", color: C.text, valign: "middle", margin: 0 });
  });

  // Key context box
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 5.15, w: 9.2, h: 0.38, fill: { color: C.midBlue }, line: { color: C.midBlue } });
  s.addText("背景：イランの経済制裁による外貨準備の枯渇と米国の中東戦略見直しが交渉の主要因", {
    x: 0.4, y: 5.15, w: 9.2, h: 0.38, fontSize: 12, fontFace: "Calibri", color: C.white, align: "center", valign: "middle", margin: 0
  });
}

// ─────────────────────────────────────────────
// SLIDE 4: 合意内容の主要条件
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.95, fill: { color: C.navy }, line: { color: C.navy } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.95, w: 10, h: 0.06, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("02　合意内容の主要条件", { x: 0.4, y: 0.15, w: 9, h: 0.65, fontSize: 22, fontFace: "Georgia", color: C.white, bold: true, margin: 0 });

  const cards = [
    { label: "核開発", icon: "☢", color: "C0392B", light: "FDECEA",
      items: ["ウラン濃縮を60%→20%に削減", "フォルドー施設の稼働停止", "IAEA査察員の常駐受入れ", "新型遠心分離機の開発凍結"] },
    { label: "経済制裁", icon: "💰", color: "1E7D4E", light: "E8F8EF",
      items: ["石油輸出制裁の段階的緩和（60日後）", "凍結資産の一部解放（70億ドル）", "SWIFT接続の部分的回復", "人道支援輸入の全面解禁"] },
    { label: "地域安全", icon: "🛡", color: "1A2B52", light: "EEF2FA",
      items: ["イエメン・フーシへの武器供与停止", "イラク駐留民兵への関与縮小", "ホルムズ海峡の航行自由保証", "米軍への直接攻撃指示禁止"] },
    { label: "捕虜・人質", icon: "🤝", color: "D4850A", light: "FEF9E7",
      items: ["米国人5名の即時解放", "イラン系米国人の出国許可", "学術交流プログラムの再開", "大使館連絡事務所設置（90日以内）"] },
  ];

  cards.forEach((card, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = col === 0 ? 0.3 : 5.2;
    const y = 1.1 + row * 2.2;

    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.6, h: 2.0, fill: { color: C.white }, line: { color: "E0E8F0", pt: 1 }, shadow: makeShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.6, h: 0.45, fill: { color: card.color }, line: { color: card.color } });
    s.addText(`${card.icon}  ${card.label}`, { x: x + 0.15, y: y + 0.07, w: 4.3, h: 0.32, fontSize: 14, fontFace: "Calibri", color: C.white, bold: true, margin: 0 });

    card.items.forEach((item, j) => {
      s.addText([{ text: "▸  " + item, options: {} }], {
        x: x + 0.2, y: y + 0.52 + j * 0.36, w: 4.2, h: 0.33,
        fontSize: 11.5, fontFace: "Calibri", color: C.text, margin: 0
      });
    });
  });
}

// ─────────────────────────────────────────────
// SLIDE 5: 地政学的影響分析
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.95, fill: { color: C.navy }, line: { color: C.navy } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.95, w: 10, h: 0.06, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("03　地政学的影響分析", { x: 0.4, y: 0.15, w: 9, h: 0.65, fontSize: 22, fontFace: "Georgia", color: C.white, bold: true, margin: 0 });

  // Three columns: 歓迎/懸念/注目
  const cols = [
    { title: "歓迎する立場", color: C.safe, items: ["🇮🇶 イラク：地域安定化期待", "🇶🇦 カタール：LNG輸出拡大", "🇪🇺 EU：対イラン投資再開", "🇨🇳 中国：ホルムズ安定化", "🛢️ 原油市場：供給増加期待"] },
    { title: "懸念する立場", color: C.danger, items: ["🇮🇱 イスラエル：安保の空白", "🇸🇦 サウジ：シーア派台頭", "🇦🇪 UAE：フーシへの不信", "🇺🇸 強硬派：検証不足批判", "🇮🇷 保守派：主権侵害と主張"] },
    { title: "注目すべき変数", color: C.warn, items: ["🔍 IAEA査察の実効性", "🗓️ イラン大統領選（2027）", "💣 代理勢力の独自判断", "📊 制裁解除のスピード", "🔗 ロシアの対イラン関与"] },
  ];

  cols.forEach((col, i) => {
    const x = 0.3 + i * 3.2;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.15, w: 3.0, h: 0.42, fill: { color: col.color }, line: { color: col.color } });
    s.addText(col.title, { x, y: 1.15, w: 3.0, h: 0.42, fontSize: 13, fontFace: "Calibri", color: C.white, bold: true, align: "center", valign: "middle", margin: 0 });

    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.57, w: 3.0, h: 3.9, fill: { color: C.white }, line: { color: "E0E8F0" }, shadow: makeShadow() });

    col.items.forEach((item, j) => {
      s.addText(item, {
        x: x + 0.12, y: 1.65 + j * 0.74, w: 2.76, h: 0.62,
        fontSize: 12, fontFace: "Calibri", color: C.text, valign: "middle", margin: 0
      });
      if (j < col.items.length - 1) {
        s.addShape(pres.shapes.RECTANGLE, { x: x + 0.1, y: 2.27 + j * 0.74, w: 2.8, h: 0.01, fill: { color: "E0E8F0" }, line: { color: "E0E8F0" } });
      }
    });
  });

  // Bottom note
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 5.2, w: 9.4, h: 0.33, fill: { color: "FEF9E7" }, line: { color: C.warn } });
  s.addText("★ 最大の不確定要因：イラン革命防衛隊（IRGC）が協定を支持するか否か", {
    x: 0.3, y: 5.2, w: 9.4, h: 0.33, fontSize: 12, fontFace: "Calibri", color: C.warn, bold: true, align: "center", valign: "middle", margin: 0
  });
}

// ─────────────────────────────────────────────
// SLIDE 6: 60日間交渉シナリオ
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addText("04　60日間交渉シナリオ", { x: 0.4, y: 0.2, w: 9, h: 0.65, fontSize: 22, fontFace: "Georgia", color: C.white, bold: true, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.88, w: 2.2, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });

  const scenarios = [
    {
      label: "A　包括合意成立", prob: "30%", color: C.safe,
      conditions: ["IAEA査察受入れの完全合意", "制裁解除ロードマップ確定", "地域代理勢力の活動抑制確認"],
      outcome: "イラン核問題の外交的解決。中東安定化の第一歩となるが、イスラエルとの摩擦は継続。"
    },
    {
      label: "B　部分合意・延長", prob: "45%", color: C.warn,
      conditions: ["核問題のみ先行合意", "制裁は段階的緩和に限定", "地域問題は継続協議に先送り"],
      outcome: "最も可能性の高いシナリオ。合意の実効性は低く、再交渉が繰り返されるリスク大。"
    },
    {
      label: "C　交渉決裂・敵対再燃", prob: "25%", color: C.danger,
      conditions: ["IRGCによる代理攻撃の継続", "米議会による制裁法強化", "イスラエルによる軍事行動"],
      outcome: "ホルムズ海峡閉鎖リスク。原油価格急騰・地域紛争拡大の可能性。"
    },
  ];

  scenarios.forEach((sc, i) => {
    const y = 1.05 + i * 1.52;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 9.4, h: 1.42, fill: { color: "FFFFFF", transparency: 6 }, line: { color: sc.color, pt: 2 } });

    // Label + prob
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 2.8, h: 0.45, fill: { color: sc.color }, line: { color: sc.color } });
    s.addText(sc.label, { x: 0.35, y: y + 0.04, w: 1.9, h: 0.37, fontSize: 13, fontFace: "Calibri", color: C.white, bold: true, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 3.15, y, w: 1.1, h: 0.45, fill: { color: "FFFFFF", transparency: 15 }, line: { color: "FFFFFF", transparency: 50 } });
    s.addText(`確率 ${sc.prob}`, { x: 3.15, y: y + 0.05, w: 1.1, h: 0.35, fontSize: 12, fontFace: "Calibri", color: C.gold, bold: true, align: "center", margin: 0 });

    // Conditions
    sc.conditions.forEach((c, j) => {
      s.addText(`▸  ${c}`, { x: 0.45, y: y + 0.52 + j * 0.27, w: 4.1, h: 0.25, fontSize: 10.5, fontFace: "Calibri", color: "CADCFC", margin: 0 });
    });

    // Outcome
    s.addShape(pres.shapes.RECTANGLE, { x: 4.75, y: y + 0.45, w: 4.8, h: 0.9, fill: { color: "FFFFFF", transparency: 10 }, line: { color: sc.color } });
    s.addText("結果予測：" + sc.outcome, { x: 4.85, y: y + 0.5, w: 4.6, h: 0.82, fontSize: 11, fontFace: "Calibri", color: C.white, valign: "middle", margin: 0 });
  });
}

// ─────────────────────────────────────────────
// SLIDE 7: リスク評価マトリクス
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.95, fill: { color: C.navy }, line: { color: C.navy } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.95, w: 10, h: 0.06, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("05　リスク評価マトリクス", { x: 0.4, y: 0.15, w: 9, h: 0.65, fontSize: 22, fontFace: "Georgia", color: C.white, bold: true, margin: 0 });

  // Matrix grid
  const gridX = 1.3, gridY = 1.1, cellW = 2.7, cellH = 1.1;
  const cols2 = ["短期（0-6ヶ月）", "中期（6-18ヶ月）", "長期（18ヶ月以上）"];
  const rows = ["高リスク", "中リスク", "低リスク"];
  const rowColors = [C.danger, C.warn, C.safe];

  // Column headers
  cols2.forEach((label, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: gridX + i * cellW, y: gridY, w: cellW, h: 0.4, fill: { color: C.navy }, line: { color: C.white } });
    s.addText(label, { x: gridX + i * cellW, y: gridY, w: cellW, h: 0.4, fontSize: 12, fontFace: "Calibri", color: C.white, bold: true, align: "center", valign: "middle", margin: 0 });
  });

  // Row headers + cells
  const data = [
    ["代理勢力の\n逸脱攻撃", "核技術情報\nの漏洩", "地域覇権\n争いの再燃"],
    ["IAEA査察\nの形骸化", "米議会の\n制裁法強化", "イスラエルの\n単独軍事行動"],
    ["石油輸出\n回復の遅延", "人権問題\nの摩擦", "体制変換\nへの圧力"],
  ];

  rows.forEach((row, r) => {
    const y = gridY + 0.4 + r * cellH;
    // Row header
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 0.95, h: cellH, fill: { color: rowColors[r] }, line: { color: C.white } });
    s.addText(row, { x: 0.3, y, w: 0.95, h: cellH, fontSize: 11, fontFace: "Calibri", color: C.white, bold: true, align: "center", valign: "middle", margin: 0 });
    // Cells
    data[r].forEach((cell, c) => {
      const bgAlpha = r === 0 ? "FDECEA" : r === 1 ? "FEF9E7" : "E8F8EF";
      s.addShape(pres.shapes.RECTANGLE, { x: gridX + c * cellW, y, w: cellW, h: cellH, fill: { color: bgAlpha }, line: { color: "CCCCCC" } });
      s.addText(cell, { x: gridX + c * cellW + 0.1, y: y + 0.1, w: cellW - 0.2, h: cellH - 0.2, fontSize: 12, fontFace: "Calibri", color: C.text, align: "center", valign: "middle", margin: 0 });
    });
  });

  // Legend
  s.addText("＊ マトリクスは発生確率（縦）×時間軸（横）で整理。高リスク領域（赤）の早期モニタリングが重要。", {
    x: 0.3, y: 5.2, w: 9.4, h: 0.33, fontSize: 11, fontFace: "Calibri", color: C.muted, align: "center", margin: 0
  });
}

// ─────────────────────────────────────────────
// SLIDE 8: 今後の展望と政策提言
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addText("06　今後の展望と政策提言", { x: 0.4, y: 0.2, w: 9, h: 0.65, fontSize: 22, fontFace: "Georgia", color: C.white, bold: true, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.88, w: 2.5, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });

  // Two columns
  const leftItems = [
    { title: "外交モニタリング", body: "IAEA月次報告の精査と、オマーン・カタールを通じた\nバックチャンネルの維持が不可欠。" },
    { title: "制裁の段階的設計", body: "核コンプライアンスと連動した「スマート制裁」設計。\n一括解除ではなく段階的対話を促す仕組みが必要。" },
    { title: "同盟国との連携", body: "イスラエル・湾岸諸国の懸念を吸収する並行的安全\n保障枠組みの構築。NATO+中東安保対話の強化。" },
  ];
  const rightItems = [
    { title: "代理勢力への圧力", body: "フーシ・ヒズボラ・イラク民兵への資金追跡・\n制裁強化を継続。合意の「抜け穴」封鎖が鍵。" },
    { title: "国内政治リスク管理", body: "米国：議会強硬派への情報開示強化。\nイラン：改革派支持層の可視化と体制内調整。" },
    { title: "エネルギー安全保障", body: "ホルムズ海峡リスクへの備えとして、IEA緊急備蓄\n協議と代替ルート（アラビア半島横断パイプライン）を活性化。" },
  ];

  [[leftItems, 0.3], [rightItems, 5.2]].forEach(([items, x]) => {
    items.forEach((item, i) => {
      const y = 1.05 + i * 1.55;
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.6, h: 1.42, fill: { color: "FFFFFF", transparency: 8 }, line: { color: C.midBlue } });
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h: 1.42, fill: { color: C.gold }, line: { color: C.gold } });
      s.addText(item.title, { x: x + 0.2, y: y + 0.1, w: 4.3, h: 0.38, fontSize: 13.5, fontFace: "Calibri", color: C.gold, bold: true, margin: 0 });
      s.addText(item.body, { x: x + 0.2, y: y + 0.52, w: 4.3, h: 0.82, fontSize: 11.5, fontFace: "Calibri", color: "CADCFC", margin: 0 });
    });
  });
}

// ─────────────────────────────────────────────
// SLIDE 9: 結論
// ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.07, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("結　論", {
    x: 0.5, y: 0.5, w: 9, h: 0.7,
    fontSize: 36, fontFace: "Georgia", color: C.white, bold: true, align: "center", margin: 0
  });

  // Three key takeaways
  const points = [
    { num: "１", text: "今回の休戦協定は「外交的突破口」であるが、「恒久的平和」ではない。60日間交渉が成否の鍵を握る。" },
    { num: "２", text: "最も現実的なシナリオ（確率45%）は部分合意・延長。IAEA査察の実効性と制裁の連動設計が実質的な成果を左右する。" },
    { num: "３", text: "最大リスクはイラン革命防衛隊と地域代理勢力の「独走」。外交合意と軍事抑止の二本柱が不可欠。" },
  ];

  points.forEach((pt, i) => {
    const y = 1.4 + i * 1.3;
    s.addShape(pres.shapes.OVAL, { x: 0.5, y: y + 0.15, w: 0.6, h: 0.6, fill: { color: C.gold }, line: { color: C.gold } });
    s.addText(pt.num, { x: 0.5, y: y + 0.15, w: 0.6, h: 0.6, fontSize: 18, fontFace: "Georgia", color: C.navy, bold: true, align: "center", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 1.3, y, w: 8.3, h: 1.05, fill: { color: C.midBlue }, line: { color: C.midBlue } });
    s.addText(pt.text, { x: 1.45, y: y + 0.1, w: 8.0, h: 0.85, fontSize: 13.5, fontFace: "Calibri", color: C.white, valign: "middle", margin: 0 });
  });

  // Bottom bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.35, w: 10, h: 0.275, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("本資料は公開情報に基づく政策分析であり、機密情報を含むものではありません。　©2026 International Political Analysis", {
    x: 0, y: 5.35, w: 10, h: 0.275, fontSize: 10, fontFace: "Calibri", color: C.navy, align: "center", valign: "middle", margin: 0
  });
}

pres.writeFile({ fileName: "C:/Users/shondo/Desktop/agent_project/iran_ceasefire_analysis.pptx" })
  .then(() => console.log("✅ Done: iran_ceasefire_analysis.pptx"))
  .catch(e => console.error("Error:", e));
