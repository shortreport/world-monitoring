const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Financial Analysis";
pres.title = "ステーブルコイン完全解説";

// ── Color palette ──────────────────────────────────────
const NAVY   = "0D1B4B";
const GOLD   = "C9A227";
const BLUE   = "1A9BE8";
const WHITE  = "FFFFFF";
const LIGHT  = "F5F8FE";
const CARD   = "EEF3FC";
const DARK   = "1A2340";
const MUTED  = "5A6A8A";
const TEAL   = "028090";
const RED    = "C00000";
const GREEN  = "2A8A4A";
const ORANGE = "E07000";
const MAROON = "8B0000";
const PURPLE = "5A4A8A";

function hdr(slide, text, bg) {
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.0, fill: { color: bg || NAVY }, line: { color: bg || NAVY } });
  slide.addText(text, { x: 0.5, y: 0.1, w: 9, h: 0.8, fontSize: 26, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0 });
}

function card(slide, x, y, w, h, opts) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: opts.fill || WHITE }, line: { color: opts.border || "E0E8F0" }, shadow: { type: "outer", blur: 5, offset: 3, angle: 135, color: "000000", opacity: 0.1 } });
}

// ════════════════════════════════════════════════════════
// SLIDE 1 ─ タイトル
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: NAVY };

  // Decorative circles
  s.addShape(pres.shapes.OVAL, { x: 7.2, y: -1.2, w: 5.5, h: 5.5, fill: { color: GOLD, transparency: 87 }, line: { color: GOLD, transparency: 87 } });
  s.addShape(pres.shapes.OVAL, { x: 8.5, y: 3.0, w: 3.0, h: 3.0, fill: { color: BLUE, transparency: 90 }, line: { color: BLUE, transparency: 90 } });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.5, w: 0.07, h: 2.5, fill: { color: GOLD }, line: { color: GOLD } });

  s.addText("ステーブルコイン完全解説", { x: 0.75, y: 1.35, w: 8.5, h: 1.3, fontSize: 42, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0 });
  s.addText("3メガバンクの挑戦  ／  トランプの野望  ／  円の主権", { x: 0.75, y: 2.75, w: 8.5, h: 0.65, fontSize: 17, fontFace: "Calibri", color: GOLD, align: "left", margin: 0 });
  s.addText("2026年6月  |  経済・金融解説レポート", { x: 0.75, y: 4.9, w: 8.5, h: 0.38, fontSize: 11, fontFace: "Calibri", color: "CADCFC", align: "left", margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 2 ─ ステーブルコインとは？
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "ステーブルコインとは何か？");

  // Left card
  card(s, 0.35, 1.15, 4.6, 4.15, { fill: CARD, border: "C8D8F0" });
  s.addText([
    { text: "デジタルなお金の新形態", options: { bold: true, fontSize: 16, color: NAVY, breakLine: true } },
    { text: " ", options: { fontSize: 7, breakLine: true } },
    { text: "価格が大きく動かないように設計されたデジタル資産。1単位＝ほぼ1円（または1ドル）と法定通貨に価値が連動するよう設計されています。", options: { fontSize: 12, color: DARK, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "ビットコインとの違い", options: { bold: true, fontSize: 14, color: NAVY, breakLine: true } },
    { text: "ビットコイン：価格が大きく変動（投機性が高い）", options: { fontSize: 12, color: MUTED, bullet: true, breakLine: true } },
    { text: "ステーブルコイン：価格が安定（決済に使いやすい）", options: { fontSize: 12, color: MUTED, bullet: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "仕組み", options: { bold: true, fontSize: 14, color: NAVY, breakLine: true } },
    { text: "法定通貨（円・ドル）や国債を裏付け資産として保有し、その価値と1対1で連動するデジタルトークンを発行する。ブロックチェーン上で即時・低コストに送受信できる。", options: { fontSize: 12, color: DARK } },
  ], { x: 0.55, y: 1.3, w: 4.2, h: 3.9, valign: "top", margin: 10 });

  // Right top: market stat
  s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.15, w: 4.45, h: 1.65, fill: { color: NAVY }, line: { color: NAVY } });
  s.addText([
    { text: "世界のステーブルコイン市場規模（2026年初）", options: { fontSize: 11, color: "CADCFC", breakLine: true } },
    { text: "約3,000億ドル", options: { fontSize: 30, bold: true, color: WHITE, breakLine: true } },
    { text: "うち99.76%がドル建て　円建てはわずか0.24%", options: { fontSize: 11, color: GOLD } },
  ], { x: 5.3, y: 1.2, w: 4.25, h: 1.55, valign: "middle", margin: 10 });

  // Right middle: main coins
  s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 2.95, w: 2.1, h: 2.35, fill: { color: GOLD }, line: { color: GOLD } });
  s.addText([
    { text: "主要コイン", options: { fontSize: 11, color: NAVY, breakLine: true } },
    { text: "USDT", options: { fontSize: 20, bold: true, color: NAVY, breakLine: true } },
    { text: "USDC", options: { fontSize: 16, bold: true, color: NAVY, breakLine: true } },
    { text: "USD1", options: { fontSize: 16, bold: true, color: NAVY, breakLine: true } },
    { text: "JPYC（円）", options: { fontSize: 14, bold: true, color: NAVY } },
  ], { x: 5.25, y: 3.0, w: 2.0, h: 2.25, valign: "middle", align: "center", margin: 5 });

  // Right bottom: features
  card(s, 7.45, 2.95, 2.2, 2.35, { fill: CARD, border: "C8D8F0" });
  s.addText([
    { text: "利用者のメリット", options: { bold: true, fontSize: 11, color: NAVY, breakLine: true } },
    { text: "価格安定", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "24時間取引可能", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "低コスト送金", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "即時決済", options: { fontSize: 12, color: DARK, bullet: true } },
  ], { x: 7.55, y: 3.05, w: 2.0, h: 2.15, valign: "top", margin: 8 });

  s.addText("※ 日本では改正資金決済法（2023年施行）により「電子決済手段」として法的定義", { x: 0.35, y: 5.27, w: 9.3, h: 0.28, fontSize: 9, color: MUTED, margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 3 ─ ステーブルコインの種類
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "ステーブルコインの種類と比較");

  const cols = [
    { x: 0.25, color: BLUE, title: "資金移動業型", ex: "代表例：JPYC（円建て）", rows: [["発行体","資金移動業者"],["送金上限","1回100万円"],["用途","個人・小口決済"],["裏付け","預貯金と国債"],["開始","2025年10月"],["特徴","手軽・低コスト"]] },
    { x: 3.55, color: GOLD, title: "信託型（3メガ）", ex: "2026年度中 共同発行予定", rows: [["発行体","三菱UFJ信託銀行"],["送金上限","上限なし ★"],["用途","証券・企業間決済"],["裏付け","信託の倒産隔離"],["開始","2026年度中"],["特徴","高額・高信頼性"]] },
    { x: 6.85, color: GREEN, title: "グローバル型（ドル建て）", ex: "代表：USDT / USDC / USD1", rows: [["発行体","民間企業（Tether等）"],["送金上限","実質上限なし"],["用途","国際送金・DeFi"],["裏付け","ドル資産・米国債"],["流通規模","約3,000億ドル"],["特徴","国境なし即時決済"]] },
  ];

  cols.forEach(c => {
    card(s, c.x, 1.15, 3.05, 4.3, { fill: WHITE, border: "E0E8F0" });
    s.addShape(pres.shapes.RECTANGLE, { x: c.x, y: 1.15, w: 3.05, h: 0.55, fill: { color: c.color }, line: { color: c.color } });
    s.addText(c.title, { x: c.x + 0.05, y: 1.17, w: 2.95, h: 0.5, fontSize: 14, bold: true, color: c.color === GOLD ? NAVY : WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(c.ex, { x: c.x + 0.1, y: 1.75, w: 2.85, h: 0.32, fontSize: 11, bold: true, color: DARK, margin: 0 });

    c.rows.forEach(([label, val], i) => {
      const rowY = 2.12 + i * 0.5;
      s.addShape(pres.shapes.RECTANGLE, { x: c.x + 0.1, y: rowY, w: 1.05, h: 0.38, fill: { color: c.color, transparency: 80 }, line: { color: c.color, transparency: 60 } });
      s.addText(label, { x: c.x + 0.1, y: rowY, w: 1.05, h: 0.38, fontSize: 9, color: DARK, align: "center", valign: "middle", margin: 0 });
      s.addText(val, { x: c.x + 1.2, y: rowY, w: 1.75, h: 0.38, fontSize: 11, color: DARK, valign: "middle", margin: 0 });
    });
  });

  s.addText("★ 送金上限なしが信託型の最大の強み ─ 高額取引に対応可能", { x: 0.25, y: 5.33, w: 9.5, h: 0.22, fontSize: 9, color: MUTED, margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 4 ─ なぜ今注目されるのか？
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: LIGHT };
  hdr(s, "なぜ今、ステーブルコインが注目されるのか？");

  const reasons = [
    {
      num: "01", color: NAVY, title: "制度整備の完成",
      items: ["2023年：改正資金決済法施行→電子決済手段として法的定義", "2025年：再改正で裏付け資産に国債を解禁、仲介業を新設", "金融庁が3メガの実証実験を支援案件に採択", "法的安全性の確保が民間投資の呼び水に"]
    },
    {
      num: "02", color: GOLD, title: "日銀利上げの追い風",
      items: ["金利上昇→裏付け資産（国債等）の運用益増加", "野村総合研究所（2025年10月）：「運用益が決済手数料収入の減少を相殺する効果が期待」", "利上げが進むほど発行の経済的動機が強まる構造", "かつてゼロ金利では成り立ちにくかったビジネスモデルが変化"]
    },
    {
      num: "03", color: BLUE, title: "海外の急速な進展",
      items: ["米国：GENIUS法（2025年7月）成立→ドル建て整備を加速", "ブラックロックがトークン化短期運用商品を急拡大", "「出遅れると海外資金が日本市場を素通りする」という危機感", "グローバルな競争で日本だけ周回遅れになるリスク"]
    },
  ];

  reasons.forEach((r, i) => {
    const x = 0.3 + i * 3.22;
    card(s, x, 1.15, 3.08, 4.25, { fill: WHITE, border: "E0E8F0" });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.15, w: 3.08, h: 0.72, fill: { color: r.color }, line: { color: r.color } });
    s.addText(r.num, { x: x + 0.08, y: 1.17, w: 0.72, h: 0.68, fontSize: 28, bold: true, color: "FFFFFF", align: "left", margin: 0, transparency: 40 });
    s.addText(r.title, { x: x + 0.1, y: 1.3, w: 2.9, h: 0.5, fontSize: 14, bold: true, color: r.color === GOLD ? NAVY : WHITE, align: "right", margin: 5 });

    r.items.forEach((item, j) => {
      s.addShape(pres.shapes.RECTANGLE, { x: x + 0.1, y: 2.0 + j * 0.82, w: 0.07, h: 0.55, fill: { color: r.color }, line: { color: r.color } });
      s.addText(item, { x: x + 0.25, y: 1.98 + j * 0.82, w: 2.73, h: 0.58, fontSize: 11, color: DARK, valign: "middle", margin: 0 });
    });
  });
}

// ════════════════════════════════════════════════════════
// SLIDE 5 ─ 3メガバンクの発表
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "3メガバンク共同発行：信託型ステーブルコイン");

  // Announcement bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 1.08, w: 9.3, h: 1.0, fill: { color: NAVY }, line: { color: NAVY } });
  s.addText("2026年6月10日発表　三菱UFJ・みずほ・三井住友が信託型ステーブルコインを共同発行。2026年度中に実取引開始へ。", { x: 0.55, y: 1.1, w: 9.0, h: 0.96, fontSize: 14, color: WHITE, align: "center", valign: "middle", margin: 8 });

  // Left: Scheme
  card(s, 0.35, 2.18, 4.55, 3.15, { fill: CARD, border: "C8D8F0" });
  s.addText("発行スキームの概要", { x: 0.5, y: 2.28, w: 4.3, h: 0.38, fontSize: 15, bold: true, color: NAVY, margin: 0 });

  const scheme = [
    ["発行体", "三菱UFJ信託銀行"],
    ["委託者", "三菱UFJ・みずほ・三井住友"],
    ["協議体制", "共同協議会を設置"],
    ["開始目標", "2026年度中（実取引）"],
    ["初期用途", "株式・投資信託の決済"],
    ["参加機関", "野村証券・大和証券を含む5社"],
  ];
  scheme.forEach(([lbl, val], i) => {
    const y = 2.72 + i * 0.41;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 1.2, h: 0.32, fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(lbl, { x: 0.5, y, w: 1.2, h: 0.32, fontSize: 9, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(val, { x: 1.78, y, w: 2.85, h: 0.32, fontSize: 11, color: DARK, valign: "middle", margin: 0 });
  });

  // Right: Trust isolation
  card(s, 5.15, 2.18, 4.55, 3.15, { fill: "FFF8E8", border: "E8D080" });
  s.addText("最大の特徴：倒産隔離", { x: 5.3, y: 2.28, w: 4.25, h: 0.38, fontSize: 15, bold: true, color: NAVY, margin: 0 });
  s.addText([
    { text: "倒産隔離とは？", options: { bold: true, fontSize: 13, color: NAVY, breakLine: true } },
    { text: "関係会社が破綻しても、信託された裏付け資産は他の財産と法的に分離され、利用者の取り分として100%確保される仕組み。", options: { fontSize: 11, color: DARK, breakLine: true } },
    { text: " ", options: { fontSize: 7, breakLine: true } },
    { text: "他のステーブルコインとの比較", options: { bold: true, fontSize: 12, color: NAVY, breakLine: true } },
    { text: "USDT/USDC/JPYC：発行会社が自ら管理→倒産リスクあり", options: { fontSize: 11, color: MUTED, bullet: true, breakLine: true } },
    { text: "3メガ信託型：信託構造で法的に資産を隔離・保護", options: { fontSize: 11, bold: true, color: GREEN, bullet: true, breakLine: true } },
    { text: " ", options: { fontSize: 7, breakLine: true } },
    { text: "→ 高額・重要決済に最適な設計", options: { bold: true, fontSize: 13, color: GOLD } },
  ], { x: 5.3, y: 2.72, w: 4.25, h: 2.5, valign: "top", margin: 8 });
}

// ════════════════════════════════════════════════════════
// SLIDE 6 ─ 証券即時決済（DVP）
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "証券即時決済（DVP）が変えること");

  // BEFORE
  card(s, 0.3, 1.08, 4.45, 4.35, { fill: "FFF0F0", border: "F0B0B0" });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 1.08, w: 4.45, h: 0.52, fill: { color: RED }, line: { color: RED } });
  s.addText("現在（旧来の仕組み）", { x: 0.35, y: 1.1, w: 4.35, h: 0.48, fontSize: 15, bold: true, color: WHITE, align: "center", margin: 0 });

  const beforeSteps = ["株を売買・約定", "↓", "数日待つ（T+2日）", "↓", "資金と証券の受け渡し"];
  beforeSteps.forEach((st, i) => {
    s.addText(st, { x: 0.45, y: 1.7 + i * 0.37, w: 4.2, h: 0.35, fontSize: st === "↓" ? 16 : 13, bold: st !== "↓", color: st === "↓" ? MUTED : (i === 2 ? RED : DARK), align: "center", margin: 0 });
  });

  s.addText([
    { text: "問題点", options: { bold: true, fontSize: 13, color: RED, breakLine: true } },
    { text: "お金を払ったのに証券はまだ手元にない", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "担保として資金が数日間拘束される", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "休日・祝日は決済が止まる", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "ブロックチェーン取引への対応不可", options: { fontSize: 12, color: DARK, bullet: true } },
  ], { x: 0.45, y: 3.6, w: 4.2, h: 1.7, valign: "top", margin: 8 });

  // Arrow
  s.addShape(pres.shapes.RECTANGLE, { x: 4.77, y: 2.85, w: 0.46, h: 0.46, fill: { color: GOLD }, line: { color: GOLD } });
  s.addText("→", { x: 4.77, y: 2.85, w: 0.46, h: 0.46, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });

  // AFTER
  card(s, 5.25, 1.08, 4.45, 4.35, { fill: "F0FFF0", border: "80C080" });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y: 1.08, w: 4.45, h: 0.52, fill: { color: GREEN }, line: { color: GREEN } });
  s.addText("ステーブルコイン導入後", { x: 5.3, y: 1.1, w: 4.35, h: 0.48, fontSize: 15, bold: true, color: WHITE, align: "center", margin: 0 });

  s.addText("株を売買", { x: 5.4, y: 1.7, w: 4.2, h: 0.35, fontSize: 13, bold: true, color: GREEN, align: "center", margin: 0 });
  s.addText("↓", { x: 5.4, y: 2.07, w: 4.2, h: 0.35, fontSize: 16, color: MUTED, align: "center", margin: 0 });
  s.addText("即時（DVP）決済", { x: 5.4, y: 2.42, w: 4.2, h: 0.52, fontSize: 22, bold: true, color: GREEN, align: "center", margin: 0 });
  s.addText("証券と資金を同時受け渡し", { x: 5.4, y: 2.97, w: 4.2, h: 0.35, fontSize: 13, color: DARK, align: "center", margin: 0 });

  s.addText([
    { text: "メリット", options: { bold: true, fontSize: 13, color: GREEN, breakLine: true } },
    { text: "取りはぐれリスクがゼロに", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "担保資金の効率化が可能", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "24時間・休日も稼働（原理上）", options: { fontSize: 12, color: DARK, bullet: true, breakLine: true } },
    { text: "海外投資家が参加しやすい市場に", options: { fontSize: 12, color: DARK, bullet: true } },
  ], { x: 5.4, y: 3.6, w: 4.2, h: 1.7, valign: "top", margin: 8 });

  s.addText("DVP（Delivery versus Payment）= 証券の受け渡しと資金決済を同時に行う仕組み　基盤：Progmat（三菱UFJ信託銀行系）", { x: 0.3, y: 5.35, w: 9.4, h: 0.22, fontSize: 9, color: MUTED, align: "center", margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 7 ─ トランプ家族とUSD1
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "トランプ大統領家族の野望：USD1とWorld Liberty Financial", MAROON);

  // Left: Timeline
  card(s, 0.3, 1.08, 5.1, 4.45, { fill: CARD, border: "D0DFF0" });
  s.addText("World Liberty Financial（WLF）とは？", { x: 0.45, y: 1.18, w: 4.8, h: 0.4, fontSize: 15, bold: true, color: NAVY, margin: 0 });
  s.addText("トランプ大統領の家族が主導する暗号資産・DeFi事業体。ドル連動ステーブルコイン「USD1」を発行。", { x: 0.45, y: 1.6, w: 4.8, h: 0.5, fontSize: 12, color: DARK, margin: 0 });

  const timeline = [
    { date: "2026年1月", text: "DeFi貸付・借入プラットフォーム「World Liberty Markets」を開設" },
    { date: "2026年4月", text: "USD1を2,500万ドル新規鋳造。流通残高は46億ドル規模に拡大" },
    { date: "2026年6月", text: "ホワイトハウスの芝生でUFCイベントを開催。USD1で賞金25万ドル分を支払い" },
    { date: "申請中", text: "World Liberty TrustがOCC（通貨監督局）に国法銀行設立を申請。認可されればUSD1の発行・管理を一体化" },
  ];

  timeline.forEach((t, i) => {
    const y = 2.2 + i * 0.82;
    s.addShape(pres.shapes.OVAL, { x: 0.45, y: y + 0.12, w: 0.38, h: 0.38, fill: { color: MAROON }, line: { color: MAROON } });
    s.addText(t.date, { x: 0.92, y: y + 0.08, w: 1.3, h: 0.28, fontSize: 10, bold: true, color: MAROON, margin: 0 });
    s.addText(t.text, { x: 0.92, y: y + 0.36, w: 4.3, h: 0.38, fontSize: 11, color: DARK, margin: 0 });
  });

  // Right: Goals
  card(s, 5.65, 1.08, 4.05, 4.45, { fill: "FFF8F0", border: "F0C080" });
  s.addText("何を目論んでいるのか？", { x: 5.8, y: 1.18, w: 3.8, h: 0.4, fontSize: 15, bold: true, color: NAVY, margin: 0 });

  const goals = [
    { n: "1", t: "政治力との相乗効果", b: "大統領権限でGENIUS法など規制緩和を推進しつつ、自社のステーブルコインが有利な環境で拡大する" },
    { n: "2", t: "米国債需要を創出", b: "USD1の裏付けは米国債等。ステーブルコインが普及するほど米国債の買い手が増え、財政的にも有利" },
    { n: "3", t: "ドル基軸の維持・拡張", b: "デジタル時代でもドルが世界の基軸通貨であり続けるよう、ドル建てステーブルコインで先行する" },
    { n: "4", t: "金融ビジネスの本体化", b: "DeFi→銀行免許申請と段階的に拡大。デジタル金融の生態系を構築し巨大な収益源を確保する" },
  ];

  goals.forEach((g, i) => {
    const y = 1.65 + i * 0.95;
    s.addShape(pres.shapes.OVAL, { x: 5.75, y: y + 0.08, w: 0.42, h: 0.42, fill: { color: MAROON }, line: { color: MAROON } });
    s.addText(g.n, { x: 5.75, y: y + 0.08, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(g.t, { x: 6.24, y: y + 0.04, w: 3.3, h: 0.3, fontSize: 12, bold: true, color: MAROON, margin: 0 });
    s.addText(g.b, { x: 6.24, y: y + 0.36, w: 3.3, h: 0.5, fontSize: 10, color: DARK, margin: 0 });
  });
}

// ════════════════════════════════════════════════════════
// SLIDE 8 ─ GENIUS法とドル基軸
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "GENIUS法とドル基軸通貨戦略", "1A4A8A");

  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 1.08, w: 9.4, h: 0.88, fill: { color: "1A4A8A" }, line: { color: "1A4A8A" } });
  s.addText("GENIUS法（2025年7月18日成立）：米国初の包括的なステーブルコイン規制法。発行体に1対1での高品質ドル建て資産の保有を義務付け。", { x: 0.5, y: 1.1, w: 9.1, h: 0.84, fontSize: 13, color: WHITE, valign: "middle", margin: 8 });

  const pillars = [
    { t: "ドル需要の維持・拡大", color: "1A4A8A", pts: ["ドル建てステーブルコインが増えるほど米国債需要が増加", "Tether・Circleはすでに米国短期国債の主要保有者", "外国の中央銀行を介さず世界中でドルを流通させる"] },
    { t: "外国の競合を事実上排除", color: MAROON, pts: ["全ステーブルコインの99.76%がドル建て（2026年初）", "円・ユーロなど非ドルはわずか0.24%", "規制の先行でグローバル標準を事実上確立"] },
    { t: "米国債市場の安定化", color: GREEN, pts: ["スタンダードチャータード予測：市場が2028年に2兆ドルへ", "2兆ドルのステーブルコイン＝2兆ドルの米国債需要", "財政赤字を補う民間ドル需要を創出"] },
  ];

  pillars.forEach((p, i) => {
    const x = 0.3 + i * 3.23;
    card(s, x, 2.06, 3.08, 3.18, { fill: WHITE, border: "E0E8F0" });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 2.06, w: 3.08, h: 0.5, fill: { color: p.color }, line: { color: p.color } });
    s.addText(p.t, { x: x + 0.05, y: 2.07, w: 2.98, h: 0.48, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    const items = p.pts.map((pt, j) => ({ text: pt, options: { fontSize: 11, color: DARK, bullet: true, breakLine: j < p.pts.length - 1 } }));
    s.addText(items, { x: x + 0.1, y: 2.62, w: 2.88, h: 2.45, valign: "top", margin: 8 });
  });

  card(s, 0.3, 5.1, 9.4, 0.38, { fill: LIGHT, border: "D0DFF0" });
  s.addText("「ステーブルコインが普及するほど米国債が買われる──ドル覇権のデジタル版」  (Columbia Economic Review)", { x: 0.45, y: 5.13, w: 9.1, h: 0.32, fontSize: 10, color: MUTED, italic: true, align: "center", margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 9 ─ 製造業・企業への影響
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "製造業・企業への影響：サプライチェーンと国際決済", TEAL);

  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 1.08, w: 9.4, h: 0.8, fill: { color: TEAL }, line: { color: TEAL } });
  s.addText([
    { text: "B2B（企業間）のステーブルコイン決済は2035年に", options: { fontSize: 13, color: WHITE } },
    { text: " 5兆ドル ", options: { fontSize: 22, bold: true, color: GOLD } },
    { text: "規模に達すると予測　（Juniper Research 2026年4月）", options: { fontSize: 13, color: WHITE } },
  ], { x: 0.5, y: 1.1, w: 9.1, h: 0.76, align: "center", valign: "middle", margin: 5 });

  const impacts = [
    { x: 0.3, y: 2.0, color: TEAL, title: "クロスボーダー決済のコスト削減", body: "従来のSWIFTなど銀行間ネットワーク不要。ブロックチェーン上で直接決済。三菱商事がクロスボーダー決済での活用を実証中。手数料を大幅削減し、為替コストも圧縮。" },
    { x: 5.15, y: 2.0, color: "1A7A5A", title: "サプライチェーンの資金効率化", body: "部品調達から納品まで、スマートコントラクトで自動執行する決済が可能に。担保として拘束される資金を最小化し、企業の資金繰りと運転資本効率が改善。" },
    { x: 0.3, y: 3.7, color: "1A4A8A", title: "24時間365日の決済インフラ", body: "土日・祝日・夜間の決済が可能に。グローバルなサプライチェーンで時差を問わず即時に代金支払いが実現。納期短縮・在庫削減にも直結する可能性がある。" },
    { x: 5.15, y: 3.7, color: MAROON, title: "高額な企業間決済に対応", body: "3メガ信託型は送金上限なし。数十億円規模の取引も瞬時に決済可能。製造業の設備投資・大型資材調達・M&A関連取引での活用が期待される。" },
  ];

  impacts.forEach(item => {
    card(s, item.x, item.y, 4.65, 1.55, { fill: WHITE, border: "E0E8F0" });
    s.addShape(pres.shapes.RECTANGLE, { x: item.x, y: item.y, w: 0.08, h: 1.55, fill: { color: item.color }, line: { color: item.color } });
    s.addText(item.title, { x: item.x + 0.18, y: item.y + 0.1, w: 4.35, h: 0.34, fontSize: 13, bold: true, color: item.color, margin: 0 });
    s.addText(item.body, { x: item.x + 0.18, y: item.y + 0.48, w: 4.35, h: 0.97, fontSize: 11, color: DARK, valign: "top", margin: 0 });
  });

  s.addText("コスト削減(52%)・クロスボーダー高速化(45%)が企業導入意欲の主因（EY調査）　　B2B支払いが全体の85%を占める見通し", { x: 0.3, y: 5.38, w: 9.4, h: 0.22, fontSize: 9, color: MUTED, align: "center", margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 10 ─ 円の主権
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "円の主権：デジタル時代の通貨競争");

  // Left: Problem
  card(s, 0.3, 1.08, 4.55, 4.4, { fill: "FFF0F0", border: "F0B0B0" });
  s.addText("ドル一強の現実", { x: 0.45, y: 1.18, w: 4.3, h: 0.38, fontSize: 16, bold: true, color: RED, margin: 0 });

  // Visual stat
  s.addShape(pres.shapes.OVAL, { x: 0.5, y: 1.65, w: 2.7, h: 2.7, fill: { color: "1A4A8A" }, line: { color: "1A4A8A" } });
  s.addText("99.76%\nドル建て", { x: 0.5, y: 2.25, w: 2.7, h: 1.5, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });

  s.addShape(pres.shapes.OVAL, { x: 3.0, y: 3.85, w: 1.1, h: 1.1, fill: { color: RED }, line: { color: RED } });
  s.addText("0.24%\n円建て", { x: 3.0, y: 3.85, w: 1.1, h: 1.1, fontSize: 9, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });

  s.addText([
    { text: "このまま放置すれば、デジタル決済の世界でドルが圧倒的優位を確立し、円の国際的な役割が縮小する。", options: { fontSize: 11, color: DARK, breakLine: true } },
    { text: " ", options: { fontSize: 6, breakLine: true } },
    { text: "2028年には市場が2兆ドルに達する見通し（スタンダードチャータード銀行）。その99%がドル建てなら、円の存在感は消える。", options: { fontSize: 11, color: DARK } },
  ], { x: 3.25, y: 1.65, w: 1.45, h: 2.0, valign: "top", margin: 3 });

  // Right: Solution
  card(s, 5.1, 1.08, 4.6, 4.4, { fill: CARD, border: "C8D8F0" });
  s.addText("円建てステーブルコインの意義", { x: 5.25, y: 1.18, w: 4.35, h: 0.38, fontSize: 16, bold: true, color: NAVY, margin: 0 });

  const yenPts = [
    { t: "証券決済の国際競争力向上", b: "トークン化金融商品の即時決済で、海外投資家が日本市場に参加しやすくなる" },
    { t: "クロスボーダー円建て決済", b: "三菱商事が実証中。海外への支払いを銀行間ネットワーク不要で即時・低コストに" },
    { t: "円建て決済圏の構築", b: "アジアでの円建て取引を増やし、円の国際的プレゼンスを維持・拡大する" },
    { t: "通貨主権の防衛", b: "ドルやデジタル人民元に対抗する通貨政策上の重要手段となりうる" },
  ];

  yenPts.forEach((pt, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.65 + i * 0.9, w: 0.07, h: 0.68, fill: { color: GOLD }, line: { color: GOLD } });
    s.addText(pt.t, { x: 5.35, y: 1.65 + i * 0.9, w: 4.2, h: 0.32, fontSize: 13, bold: true, color: NAVY, margin: 0 });
    s.addText(pt.b, { x: 5.35, y: 1.99 + i * 0.9, w: 4.2, h: 0.38, fontSize: 11, color: DARK, margin: 0 });
  });

  s.addText("「身近な株決済の話が、たどっていくと通貨の主権の話につながる」（聞く経済ニュース 2026年6月15日）", { x: 0.3, y: 5.33, w: 9.4, h: 0.25, fontSize: 10, color: MUTED, italic: true, align: "center", margin: 0 });
}

// ════════════════════════════════════════════════════════
// SLIDE 11 ─ リスクと課題
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: WHITE };
  hdr(s, "リスクと課題：冷静に見るべき論点", PURPLE);

  const risks = [
    { t: "預金流出リスク", sev: "高", sc: RED, b: "お金がステーブルコインに移れば銀行の預金基盤が細る。メガバンクが様子見だった主因。信託にお金を移しつつグループ内に資金を留める設計が鍵になる。" },
    { t: "大手連合 vs 独立勢力", sev: "中", sc: ORANGE, b: "SBIホールディングス北尾氏が「画一的で競争を制限する」と大手連合への参加を拒否。オールジャパン路線 vs 独自路線の対立が生まれている。" },
    { t: "AML・コンプライアンス", sev: "中", sc: ORANGE, b: "マネーロンダリング対策や実務ルールの整備が本格普及の前提。規制対応コストが発行体の負担になり、普及の速度を左右する可能性がある。" },
    { t: "移行期の複雑さ", sev: "中", sc: ORANGE, b: "既存の決済インフラと並存する移行期はシステムの複雑さが増す。地方銀行・信用金庫は自前発行より「利用・流通側」での関わり方が課題となる。" },
    { t: "初期の用途限定", sev: "低", sc: GREEN, b: "当初は証券・企業間決済に限定。個人・小売への普及には時間がかかる見込みで、当面は一般消費者が恩恵を感じにくい段階が続く。" },
    { t: "円の対ドル劣勢", sev: "高", sc: RED, b: "円建ては全体の0.24%のみ。GENIUS法成立でドル先行がさらに加速しており、後発の円建てステーブルコインが追いつく余地は限られる可能性がある。" },
  ];

  const grid = [[0.3, 1.08], [3.57, 1.08], [6.84, 1.08], [0.3, 3.08], [3.57, 3.08], [6.84, 3.08]];

  risks.forEach((r, i) => {
    const [x, y] = grid[i];
    card(s, x, y, 3.12, 1.88, { fill: WHITE, border: "E0E8F0" });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 3.12, h: 0.1, fill: { color: r.sc }, line: { color: r.sc } });
    s.addText(r.t, { x: x + 0.1, y: y + 0.15, w: 2.5, h: 0.32, fontSize: 12, bold: true, color: r.sc, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 2.72, y: y + 0.12, w: 0.32, h: 0.28, fill: { color: r.sc }, line: { color: r.sc } });
    s.addText(r.sev, { x: x + 2.72, y: y + 0.12, w: 0.32, h: 0.28, fontSize: 9, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(r.b, { x: x + 0.1, y: y + 0.52, w: 2.95, h: 1.28, fontSize: 10, color: DARK, valign: "top", margin: 0 });
  });

  // Legend
  [[RED, "高リスク"], [ORANGE, "中リスク"], [GREEN, "低リスク"]].forEach(([c, label], i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3 + i * 1.6, y: 5.22, w: 0.22, h: 0.22, fill: { color: c }, line: { color: c } });
    s.addText(label, { x: 0.55 + i * 1.6, y: 5.22, w: 1.2, h: 0.22, fontSize: 10, color: MUTED, margin: 0 });
  });
}

// ════════════════════════════════════════════════════════
// SLIDE 12 ─ まとめ
// ════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: NAVY };

  // Decorative elements
  s.addShape(pres.shapes.OVAL, { x: 6.8, y: -1.3, w: 5.5, h: 5.5, fill: { color: GOLD, transparency: 88 }, line: { color: GOLD, transparency: 88 } });
  s.addShape(pres.shapes.OVAL, { x: 8.5, y: 3.5, w: 3.0, h: 3.0, fill: { color: BLUE, transparency: 91 }, line: { color: BLUE, transparency: 91 } });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.28, w: 0.07, h: 1.0, fill: { color: GOLD }, line: { color: GOLD } });
  s.addText("まとめ：ステーブルコインが変える世界", { x: 0.7, y: 0.25, w: 8.5, h: 0.85, fontSize: 30, fontFace: "Georgia", bold: true, color: WHITE, align: "left", margin: 0 });

  const conclusions = [
    { n: "1", t: "日本の証券・金融インフラの革新", b: "3メガバンクの信託型ステーブルコインが2026年度中に始動。証券の即時決済（DVP）が実現し、担保効率・投資家利便が向上、日本市場の国際競争力が高まる。" },
    { n: "2", t: "米国の覇権維持とトランプ家の利益", b: "GENIUS法でドル建てステーブルコインが制度化。トランプ家のUSD1が政治力と相乗して拡大。ドル基軸通貨体制のデジタル版が形成されつつある。" },
    { n: "3", t: "円の主権と製造業の機会", b: "製造業のクロスボーダー決済コストが大幅削減。一方で円建てステーブルコインの拡大が遅れれば、円の国際的役割が縮小するリスクがある。" },
  ];

  conclusions.forEach((c, i) => {
    const y = 1.27 + i * 1.15;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 9.0, h: 1.05, fill: { color: "FFFFFF", transparency: 92 }, line: { color: GOLD, transparency: 60 } });
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: y + 0.28, w: 0.5, h: 0.5, fill: { color: GOLD }, line: { color: GOLD } });
    s.addText(c.n, { x: 0.6, y: y + 0.28, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: NAVY, align: "center", valign: "middle", margin: 0 });
    s.addText(c.t, { x: 1.2, y: y + 0.06, w: 8.2, h: 0.35, fontSize: 14, bold: true, color: GOLD, margin: 0 });
    s.addText(c.b, { x: 1.2, y: y + 0.44, w: 8.2, h: 0.52, fontSize: 11, color: "CADCFC", margin: 0 });
  });

  // Two scenarios
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.65, w: 4.35, h: 0.82, fill: { color: "FFFFFF", transparency: 91 }, line: { color: "CADCFC" } });
  s.addText([
    { text: "シナリオA：証券即時決済から普及", options: { bold: true, fontSize: 12, color: GOLD, breakLine: true } },
    { text: "決済即時化→海外資金流入→日本市場の復権", options: { fontSize: 11, color: "CADCFC" } },
  ], { x: 0.65, y: 4.68, w: 4.1, h: 0.76, valign: "middle", margin: 5 });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.15, y: 4.65, w: 4.35, h: 0.82, fill: { color: "FFFFFF", transparency: 91 }, line: { color: "CADCFC" } });
  s.addText([
    { text: "シナリオB：企業間・クロスボーダー主導", options: { bold: true, fontSize: 12, color: GOLD, breakLine: true } },
    { text: "円建て決済圏が育つ／ドル優位・預金流出リスクとの戦い", options: { fontSize: 11, color: "CADCFC" } },
  ], { x: 5.3, y: 4.68, w: 4.1, h: 0.76, valign: "middle", margin: 5 });
}

// ──────────────────────────────────────────────────────
pres.writeFile({ fileName: "C:\\Users\\shondo\\Desktop\\ステーブルコイン解説.pptx" });
console.log("Done!");
