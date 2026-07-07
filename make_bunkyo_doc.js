// 文京区 保健・健康サービス完全ガイド Word文書
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, LevelFormat, PageBreak,
  TableOfContents,
} = require("docx");
const fs = require("fs");

// ── 定数 ─────────────────────────────────────────────────────────────
// A4: 11906 x 16838 DXA, margin 1440 (1 inch) → content width = 8426 DXA
const PW = 8426; // content width in DXA
const MARGIN = 1134; // ~0.79 inch (20mm)
const FULL = 11906 - MARGIN * 2; // full content width

// ── 色 ───────────────────────────────────────────────────────────────
const NAVY   = "1A3A5C";
const BLUE   = "1B6CA8";
const GREEN  = "1A7F5A";
const ORANGE = "D9681A";
const PURPLE = "6B3FA0";
const RED    = "B71C1C";
const LGRAY  = "F2F5F8";
const LGREEN = "EBF7F0";
const LBLUE  = "EBF3FC";
const LORANGE= "FEF3E6";
const LPURPLE= "F3EDF9";
const LRED   = "FEF0F0";
const WHITE  = "FFFFFF";
const GRAY   = "5D6D7E";

// ── ヘルパー ──────────────────────────────────────────────────────────
const border1 = (color) => ({ style: BorderStyle.SINGLE, size: 4, color });
const borders = (color = "CCCCCC") => ({
  top: border1(color), bottom: border1(color),
  left: border1(color), right: border1(color),
});
const noBorder = () => ({
  top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
  left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
});
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };
const shading = (fill) => ({ fill, type: ShadingType.CLEAR });

// ── 段落ファクトリ ────────────────────────────────────────────────────
function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.before ?? 60, after: opts.after ?? 60 },
    alignment: opts.align ?? AlignmentType.LEFT,
    children: [
      new TextRun({
        text: text ?? "",
        bold: opts.bold ?? false,
        italics: opts.italic ?? false,
        size: opts.size ?? 20,
        font: "Arial",
        color: opts.color ?? "000000",
      }),
    ],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: false,
    spacing: { before: 320, after: 120 },
    children: [new TextRun({ text, bold: true, size: 36, font: "Arial", color: WHITE })],
    shading: shading(NAVY),
    indent: { left: 120 },
  });
}

function h2(text, color = BLUE) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color } },
    children: [new TextRun({ text, bold: true, size: 28, font: "Arial", color })],
  });
}

function h3(text, color = NAVY) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 160, after: 60 },
    children: [new TextRun({ text, bold: true, size: 24, font: "Arial", color })],
  });
}

function bullet(text, indent = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level: indent },
    spacing: { before: 30, after: 30 },
    children: [new TextRun({ text, size: 20, font: "Arial" })],
  });
}

function note(text) {
  return new Paragraph({
    spacing: { before: 40, after: 40 },
    indent: { left: 200 },
    children: [new TextRun({ text: "※ " + text, size: 18, font: "Arial", color: GRAY, italics: true })],
  });
}

function space(n = 1) {
  return new Paragraph({ spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "", size: 20 * n })] });
}

// ── テーブルファクトリ ─────────────────────────────────────────────────
function makeCell(content, opts = {}) {
  const { fill = WHITE, bold = false, color = "000000", colSpan, vAlign, width } = opts;
  const children = Array.isArray(content)
    ? content
    : [new Paragraph({
        alignment: opts.align ?? AlignmentType.LEFT,
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: content, bold, size: 19, font: "Arial", color })],
      })];
  const cell = {
    borders: borders(opts.borderColor ?? "BBCFE0"),
    shading: shading(fill),
    margins: cellMargins,
    verticalAlign: vAlign ?? VerticalAlign.TOP,
    children,
  };
  if (colSpan) cell.columnSpan = colSpan;
  if (width) cell.width = { size: width, type: WidthType.DXA };
  return new TableCell(cell);
}

function headerCell(text, width, color = NAVY) {
  return makeCell(text, { fill: color, bold: true, color: WHITE, width, align: AlignmentType.CENTER });
}

function makeTable(rows, colWidths) {
  const total = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: colWidths,
    rows,
  });
}

// ── 料金バッジ（インラインテキスト） ──────────────────────────────────
function feeRun(text) {
  return new TextRun({ text: `【${text}】`, bold: true, size: 19, font: "Arial", color: GREEN });
}
function targetRun(text) {
  return new TextRun({ text: `対象：${text}`, size: 18, font: "Arial", color: BLUE });
}

// ────────────────────────────────────────────────────────────────────
// メインコンテンツ
// ────────────────────────────────────────────────────────────────────
function buildContent() {
  const children = [];
  const push = (...items) => items.forEach(i => children.push(i));

  // ── 表紙 ─────────────────────────────────────────────────────────
  push(
    new Paragraph({ spacing: { before: 1800, after: 200 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "文京区", size: 56, bold: true, font: "Arial", color: NAVY })] }),
    new Paragraph({ spacing: { before: 100, after: 100 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "保健・健康サービス完全ガイド", size: 64, bold: true, font: "Arial", color: NAVY })] }),
    new Paragraph({ spacing: { before: 200, after: 600 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "─ 誰が・いくらで・何を受けられるか ─", size: 28, italics: true, font: "Arial", color: GRAY })] }),

    makeTable([
      new TableRow({ children: [
        makeCell([
          new Paragraph({ spacing:{before:40,after:40}, alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "令和7年度 一般会計予算　1,470億円", bold: true, size: 22, font: "Arial", color: NAVY })] }),
          new Paragraph({ spacing:{before:20,after:40}, alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "令和8年度 当初予算　1,605億円（過去最大）", size: 20, font: "Arial", color: GRAY })] }),
        ], { fill: LBLUE, width: FULL })
      ] }),
    ], [FULL]),

    new Paragraph({ spacing:{before:200,after:80}, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "文京区長 政策スタッフ資料　2026年7月", size: 20, font: "Arial", color: GRAY })] }),

    new Paragraph({ children: [new PageBreak()] }),
  );

  // ── 目次 ─────────────────────────────────────────────────────────
  push(
    new TableOfContents("目　次", { hyperlink: true, headingStyleRange: "1-3" }),
    new Paragraph({ children: [new PageBreak()] }),
  );

  // ================================================================
  // 1. サービス全体マップ
  // ================================================================
  push(h1("1. 文京区の健康・保健サービス　全体マップ"));
  push(para("以下の6カテゴリのサービスが区民に提供されています。本資料では各サービスを「誰が・いくらで・何を」の視点で詳述します。", { before: 80, after: 100 }));

  const mapRows = [
    new TableRow({ children: [
      headerCell("カテゴリ", 1400),
      headerCell("主なサービス内容", 3400),
      headerCell("費用の目安", 1600),
      headerCell("主な窓口", 2026),
    ]}),
    ...([
      ["① 健康診査・がん検診", "特定健診・後期高齢者健診・各種がん検診・肝炎検査・眼科健診", "すべて無料", "区内指定医療機関"],
      ["② スポーツ施設", "文京スポーツセンター（プール・トレーニング・体育館・道場）・月謝制スクール", "一般 550円〜\n70歳以上 無料", "03-3946-6311"],
      ["③ 地域スポーツ開放", "学校体育館・校庭開放「スポーツ交流ひろば」（10種目）", "無料", "スポーツ振興課\n03-5803-1303"],
      ["④ 母子保健", "妊婦健診・産後ケア・乳幼児健診・予防接種・育児相談", "健診は無料〜助成\n産後ケア 3,000円/回", "保健センター\n03-5803-1834"],
      ["⑤ 高齢者サービス", "後期高齢者健診・フレイル健診・介護予防教室・地域包括支援センター", "相談・健診は無料\nインフル接種 1,500円", "包括支援センター\n（区内6ヶ所）"],
      ["⑥ こころの健康", "精神保健相談・ひきこもり支援・自殺予防・依存症相談・認知症支援", "すべて無料\n（要予約）", "保健所\n03-5803-1834"],
    ].map(([cat, svc, fee, desk]) =>
      new TableRow({ children: [
        makeCell(cat, { fill: LBLUE, bold: true, color: NAVY, width: 1400 }),
        makeCell(svc, { fill: WHITE, width: 3400 }),
        makeCell(fee, { fill: LGREEN, bold: true, color: GREEN, width: 1600, align: AlignmentType.CENTER }),
        makeCell(desk, { fill: WHITE, width: 2026 }),
      ] })
    )),
  ];
  push(makeTable(mapRows, [1400, 3400, 1600, 2026]));
  push(space(), note("利用条件・料金は変更の可能性があります。最新情報は文京区公式HP（city.bunkyo.lg.jp）または各窓口でご確認ください。"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 2. 健康診査・がん検診
  // ================================================================
  push(h1("2. 健康診査・がん検診　─ すべて無料で受けられる"));
  push(para("受診期間：令和8年6月15日（日）〜 令和9年1月30日（金）　※乳がん・子宮がん検診は4月10日〜翌3月31日", { color: BLUE, bold: true, before: 80, after: 40 }));
  push(para("受診方法：区内指定医療機関に直接電話予約　　持参物：マイナ保険証または資格確認書", { before: 20, after: 80 }));

  const kenshinRows = [
    new TableRow({ children: [
      headerCell("検診・健診の種類", 2200),
      headerCell("対象者", 2400),
      headerCell("費用", 700),
      headerCell("検査内容・備考", 3126),
    ]}),
    ...([
      {
        name: "特定健康診査（メタボ健診）",
        who: "文京区国民健康保険加入・40〜74歳",
        fee: "無料",
        detail: "腹囲・血圧・血液（脂質・血糖・肝機能）・尿検査・問診。必要に応じて心電図・眼底・貧血検査を追加。大腸がん・肺がん検診と同時受診可。",
      },
      {
        name: "後期高齢者健康診査",
        who: "後期高齢者医療制度加入者（75歳以上等）",
        fee: "無料",
        detail: "問診・身体計測・血圧・血液（血糖・脂質・腎機能等）・尿検査。かかりつけ医でも受診可。年1回。",
      },
      {
        name: "健康増進法による健康診査",
        who: "40歳以上で特定健診・後期高齢者健診の対象外の方（要申請）",
        fee: "無料",
        detail: "社会保険加入者など、他の健診を受ける機会がない方が対象。保健センターで受付。",
      },
      {
        name: "胃がん検診",
        who: "X線：40歳以上　内視鏡：50歳以上・偶数年齢",
        fee: "無料",
        detail: "X線（バリウム）は40歳以上毎年受診可。内視鏡は50歳以上で偶数年齢に2年に1回。どちらか一方を選択。",
      },
      {
        name: "大腸がん検診",
        who: "40歳以上の区民",
        fee: "無料",
        detail: "便潜血反応検査（2日法）。受診券不要。区内指定医療機関に電話で予約。特定健診と同時受診可。年1回。",
      },
      {
        name: "肺がん検診",
        who: "40歳以上の区民",
        fee: "無料",
        detail: "胸部X線検査。喫煙歴がある一定条件を満たす方には喀痰検査も追加。特定健診と同時受診を推奨。年1回。",
      },
      {
        name: "乳がん検診",
        who: "40歳以上・偶数年齢の女性",
        fee: "無料",
        detail: "マンモグラフィ検査（2年に1回）。40歳から偶数年齢の年度に受診。受診期間：4月10日〜翌年3月31日。",
      },
      {
        name: "子宮がん検診",
        who: "20歳以上・偶数年齢の女性",
        fee: "無料",
        detail: "子宮頸がん細胞診（2年に1回）。20歳から早期受診が重要。偶数年齢の方が対象。受診期間：4月10日〜翌年3月31日。",
      },
      {
        name: "肝炎ウイルス検査（B型・C型）",
        who: "40歳以上で過去に肝炎検査を受けたことがない方",
        fee: "無料",
        detail: "一生に一度の検査。B型肝炎ウイルス（HBs抗原）・C型肝炎ウイルス（HCV抗体）を血液検査で確認。",
      },
      {
        name: "眼科健診（緑内障等）",
        who: "40・50・55・60・65・70歳になる区民",
        fee: "無料",
        detail: "緑内障・眼底疾患等の早期発見を目的。対象年齢の方に受診案内を送付。眼科医療機関で受診。",
      },
    ].map(item =>
      new TableRow({ children: [
        makeCell(item.name, { fill: LBLUE, bold: true, color: NAVY, width: 2200 }),
        makeCell(item.who, { fill: WHITE, width: 2400 }),
        makeCell(item.fee, { fill: LGREEN, bold: true, color: GREEN, width: 700, align: AlignmentType.CENTER }),
        makeCell(item.detail, { fill: WHITE, width: 3126 }),
      ]})
    )),
  ];
  push(makeTable(kenshinRows, [2200, 2400, 700, 3126]));
  push(space(), note("受診の結果、精密検査が必要な場合は自己負担となります。社会保険加入者の特定健診は、各保険者（健保組合等）が実施する健診をご利用ください。"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 3. 文京スポーツセンター
  // ================================================================
  push(h1("3. 文京スポーツセンター　─ 料金・施設・スクール"));
  push(para("住所：文京区大塚3-29-2　　最寄駅：茗荷谷駅・護国寺駅（各徒歩約5分）", { bold: true, before: 80, after: 20 }));
  push(para("営業時間：9:00〜22:30（最終入場22:00）　　利用資格：文京区在住・在勤・在学の方（区外の方も一般料金で一部利用可）", { before: 20, after: 80 }));

  push(h2("（1）個人利用料金", GREEN));

  const feeRows = [
    new TableRow({ children: [
      headerCell("施設", 2000, GREEN),
      headerCell("一般（15歳以上）", 1200, GREEN),
      headerCell("シルバー\n（65〜69歳）", 1200, GREEN),
      headerCell("中学生以下", 1100, GREEN),
      headerCell("セミゴールド\n（70〜79歳）", 1200, GREEN),
      headerCell("ゴールド\n（80歳以上）", 1200, GREEN),
      headerCell("障がい者", 526, GREEN),
    ]}),
    ...([
      ["プール（1回2時間）", "550円", "280円", "230円", "無料", "無料", "免除"],
      ["プール定期券（1ヶ月）", "4,600円", "─", "2,300円", "─", "─", "─"],
      ["トレーニングルーム（3時間）", "600円", "300円", "─", "無料", "無料", "免除"],
      ["トレーニング定期券（1ヶ月）", "2,800円", "2,800円", "─", "─", "─", "─"],
      ["競技場・道場（1回）", "310円", "─", "160円", "─", "─", "免除"],
    ].map(([facility, gen, silver, youth, semi, gold, dis]) =>
      new TableRow({ children: [
        makeCell(facility, { fill: LGREEN, bold: true, color: NAVY, width: 2000 }),
        makeCell(gen, { fill: WHITE, width: 1200, align: AlignmentType.CENTER }),
        makeCell(silver, { fill: LGREEN, width: 1200, align: AlignmentType.CENTER }),
        makeCell(youth, { fill: WHITE, width: 1100, align: AlignmentType.CENTER }),
        makeCell(semi, { fill: LGREEN, bold: true, color: GREEN, width: 1200, align: AlignmentType.CENTER }),
        makeCell(gold, { fill: LGREEN, bold: true, color: GREEN, width: 1200, align: AlignmentType.CENTER }),
        makeCell(dis, { fill: LGREEN, width: 526, align: AlignmentType.CENTER }),
      ]})
    )),
  ];
  push(makeTable(feeRows, [2000, 1200, 1200, 1100, 1200, 1200, 526]));
  push(
    space(),
    note("65〜69歳のシルバー料金は事前に窓口での登録が必要です。"),
    note("障がい者とその介助者1名は利用料が免除されます（障害者手帳等を提示）。"),
    note("プールの使用時間は着替えを含む2時間（夏季は制限なしの場合あり）。"),
  );

  push(h2("（2）月謝制スクール", GREEN));
  const schoolRows = [
    new TableRow({ children: [
      headerCell("スクール名", 2000, GREEN),
      headerCell("対象", 1600, GREEN),
      headerCell("月謝目安", 1200, GREEN),
      headerCell("内容・特記事項", 3626, GREEN),
    ]}),
    ...([
      ["子どもプールスクール", "乳幼児〜中学生", "約5,000円〜", "レベル別コース。年齢・泳力に合わせて選択。随時入会受付。"],
      ["池田体操教室", "乳幼児〜中学生", "約5,000円〜", "ローマ世界体操競技選手権金メダリスト池田敬子氏監修。専任指導員が丁寧に指導。"],
      ["竹早テニススクール", "小学生以上", "約5,000円〜", "屋外テニスコートを使用。2026年7月期の新規募集中。"],
      ["サッカーひろば", "幼児〜小学生", "参加費あり", "東京ユナイテッドFCが指導。試合形式の練習も実施。"],
      ["成人スタジオコース（プール付）", "15歳以上", "5,000〜6,000円", "エアロビクス・ヨガ等のスタジオプログラム。プール込みの場合は増額。"],
      ["成人スタジオコース（スタジオのみ）", "15歳以上", "約5,000円", "スタジオプログラムのみ参加のコース。"],
    ].map(([name, target, fee, detail]) =>
      new TableRow({ children: [
        makeCell(name, { fill: LGREEN, bold: true, color: NAVY, width: 2000 }),
        makeCell(target, { fill: WHITE, width: 1600 }),
        makeCell(fee, { fill: LGREEN, bold: true, color: GREEN, width: 1200, align: AlignmentType.CENTER }),
        makeCell(detail, { fill: WHITE, width: 3626 }),
      ]})
    )),
  ];
  push(makeTable(schoolRows, [2000, 1600, 1200, 3626]));
  push(space(), note("スクール月謝は2026年4月より改定。最新金額は文京スポーツセンター（03-3946-6311）または公式HP（shisetsu-tds.jp/tokyo-bunkyo-sportscenter）でご確認ください。"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 4. 地域スポーツ開放
  // ================================================================
  push(h1("4. 地域スポーツ開放　─ 学校体育館・校庭が無料で使える"));

  push(h2("（1）スポーツ交流ひろば（無料・申込不要）", GREEN));
  push(para("文京区立の小・中学校体育館や校庭を定期的に開放。指導員が常駐し、事前登録・申込なしで参加できます。", { before: 60, after: 60 }));

  const hiroba = [
    new TableRow({ children: [
      headerCell("対象者", 1600, GREEN),
      headerCell("料金", 700, GREEN),
      headerCell("参加方法", 2000, GREEN),
      headerCell("注意事項", 4126, GREEN),
    ]}),
    new TableRow({ children: [
      makeCell("文京区在住・在勤・在学の方\n（どなたでも）", { fill: LGREEN, bold: true, color: NAVY, width: 1600 }),
      makeCell("無料", { fill: LGREEN, bold: true, color: GREEN, width: 700, align: AlignmentType.CENTER }),
      makeCell("開放予定日に直接会場へ。途中参加・退出自由。", { fill: WHITE, width: 2000 }),
      makeCell("学校・曜日ごとに種目が決まっています。指導員の指示に従ってください。", { fill: WHITE, width: 4126 }),
    ]}),
  ];
  push(makeTable(hiroba, [1600, 700, 2000, 4126]));

  push(space(), h3("開催種目・場所・時間帯（代表例）", GREEN));
  const hirobaRows = [
    new TableRow({ children: [
      headerCell("種目", 1400, GREEN),
      headerCell("主な開催曜日・時間", 2400, GREEN),
      headerCell("主な開催場所", 4626, GREEN),
    ]}),
    ...([
      ["卓球", "月〜金　18:00〜21:00", "本郷小学校・文林中学校・第九中学校 等"],
      ["バレーボール", "火・木・金　18:30〜21:00", "第九中学校 等（校により異なる）"],
      ["ソフトテニス・硬式テニス", "日曜日　9:00〜15:30", "区内各校 校庭"],
      ["バドミントン", "月・水・土 など", "区内各校 体育館"],
      ["バスケットボール", "週複数回", "区内各校 体育館"],
      ["軽体操・太極拳", "月〜日　9:00〜21:00", "区内各校 体育館"],
      ["ビーチボールバレー", "週複数回", "区内各校 体育館"],
      ["フライングディスク", "不定期", "校庭・区内公園"],
    ].map(([sport, time, place]) =>
      new TableRow({ children: [
        makeCell(sport, { fill: LGREEN, bold: true, color: NAVY, width: 1400 }),
        makeCell(time, { fill: WHITE, width: 2400 }),
        makeCell(place, { fill: WHITE, width: 4626 }),
      ]})
    )),
  ];
  push(makeTable(hirobaRows, [1400, 2400, 4626]));
  push(space(), note("開催日程・会場は区の広報紙・公式HPで毎月更新されます。お問合せ：文京区スポーツ振興課 03-5803-1303"));

  push(h2("（2）区立学校施設 団体利用（スポーツ・文化活動）", BLUE));
  push(para("区民を主体とした団体がスポーツ・文化活動のために学校体育館・校庭等を利用できます。", { before: 60, after: 60 }));
  const gakkoRows = [
    new TableRow({ children: [
      headerCell("項目", 1800, NAVY),
      headerCell("内容", 6626, NAVY),
    ]}),
    ...([
      ["対象団体", "文京区在住の区民が主体のスポーツ・文化団体（概ね5人以上）"],
      ["利用施設", "区内26校（小学校15校・中学校11校）の体育館・校庭（プールは一部校のみ）"],
      ["利用時間", "平日：放課後〜20:00　　土日祝：8:00〜20:00（学校行事・入試等により利用不可の日あり）"],
      ["使用料", "概ね無料〜低額（施設・時間帯により異なる場合あり）"],
      ["申込方法", "「文の京」施設予約ネット（オンライン）から申請→学校長の許可を経て使用"],
    ].map(([k, v]) =>
      new TableRow({ children: [
        makeCell(k, { fill: LBLUE, bold: true, color: NAVY, width: 1800 }),
        makeCell(v, { fill: WHITE, width: 6626 }),
      ]})
    )),
  ];
  push(makeTable(gakkoRows, [1800, 6626]));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 5. 母子保健
  // ================================================================
  push(h1("5. 母子保健　─ 妊娠届から育児まで、費用の詳細"));

  push(h2("（1）妊娠・出産サポート", PURPLE));
  const boshiRows1 = [
    new TableRow({ children: [
      headerCell("サービス名", 2000, PURPLE),
      headerCell("対象者", 1800, PURPLE),
      headerCell("費用（自己負担）", 1400, PURPLE),
      headerCell("内容・手続き", 3226, PURPLE),
    ]}),
    ...([
      {
        name: "妊娠届・母子健康手帳の交付",
        who: "妊娠した方",
        fee: "無料",
        detail: "区役所または保健センター窓口で届出。オンライン届出も可。手帳交付と同時に各種受診票を配布。",
      },
      {
        name: "妊婦健康診査（14回分）",
        who: "文京区に妊娠届を出した方",
        fee: "一定金額を助成\n（差額は自己負担）",
        detail: "受診票14枚を交付。東京都内の委託医療機関で受診可。検査内容：問診・体重・血圧・尿・血液（初回のみ）等。",
      },
      {
        name: "妊婦超音波検査（4回分）",
        who: "文京区に妊娠届を出した方",
        fee: "一定金額を助成",
        detail: "超音波検査受診票4枚を交付。胎児の発育確認などに使用。",
      },
      {
        name: "妊婦子宮頸がん検診（1回）",
        who: "文京区に妊娠届を出した方",
        fee: "無料（受診票を使用）",
        detail: "妊娠中に1回、子宮頸がん検診の受診票を交付。",
      },
      {
        name: "両親学級・出産準備教室",
        who: "妊婦および配偶者",
        fee: "無料",
        detail: "保健センターで開催。出産・育児の準備についての講座。プレパパ向けコースあり。事前予約が必要。",
      },
    ].map(item =>
      new TableRow({ children: [
        makeCell(item.name, { fill: LPURPLE, bold: true, color: PURPLE, width: 2000 }),
        makeCell(item.who, { fill: WHITE, width: 1800 }),
        makeCell(item.fee, { fill: LGREEN, bold: true, color: GREEN, width: 1400, align: AlignmentType.CENTER }),
        makeCell(item.detail, { fill: WHITE, width: 3226 }),
      ]})
    )),
  ];
  push(makeTable(boshiRows1, [2000, 1800, 1400, 3226]));

  push(h2("（2）産後・授乳期サポート", PURPLE));
  const boshiRows2 = [
    new TableRow({ children: [
      headerCell("サービス名", 2000, PURPLE),
      headerCell("対象者", 1800, PURPLE),
      headerCell("費用（自己負担）", 1400, PURPLE),
      headerCell("内容・手続き", 3226, PURPLE),
    ]}),
    ...([
      {
        name: "こんにちは赤ちゃん訪問（乳児全戸訪問）",
        who: "生後4ヶ月以内の赤ちゃんがいる家庭",
        fee: "無料",
        detail: "保健師または助産師が自宅を訪問。赤ちゃんの体重・発育確認、育児相談、地域サービスの案内を実施。",
      },
      {
        name: "訪問型産後ケア（助産師訪問）",
        who: "産後1年未満の方（1人3回まで）",
        fee: "3,000円/回\n非課税世帯は減免あり\n（2,500円/回×5回まで）",
        detail: "助産師が自宅を訪問し、乳房ケア・産後の心身ケア・育児全般の相談を行う。要予約：保健センター 03-5803-1834",
      },
      {
        name: "産後ケア（ショートステイ・デイサービス）",
        who: "産後1年未満の方",
        fee: "所得応能の自己負担あり\n（施設・利用形態により異なる）",
        detail: "区補助対象施設での宿泊型・通院型産後ケア。授乳指導・休息ケア等を提供。詳細は保健センターへ。",
      },
      {
        name: "育児不安・産後うつ相談",
        who: "育児に悩む保護者（産後うつ含む）",
        fee: "無料",
        detail: "保健センターの保健師が面談。専門機関への紹介も実施。産後うつスクリーニングを実施。要予約。",
      },
    ].map(item =>
      new TableRow({ children: [
        makeCell(item.name, { fill: LPURPLE, bold: true, color: PURPLE, width: 2000 }),
        makeCell(item.who, { fill: WHITE, width: 1800 }),
        makeCell(item.fee, { fill: LGREEN, bold: true, color: GREEN, width: 1400, align: AlignmentType.CENTER }),
        makeCell(item.detail, { fill: WHITE, width: 3226 }),
      ]})
    )),
  ];
  push(makeTable(boshiRows2, [2000, 1800, 1400, 3226]));

  push(h2("（3）乳幼児健診・予防接種・子育て支援", PURPLE));
  const boshiRows3 = [
    new TableRow({ children: [
      headerCell("サービス名", 2000, PURPLE),
      headerCell("対象者", 1800, PURPLE),
      headerCell("費用", 1400, PURPLE),
      headerCell("内容・備考", 3226, PURPLE),
    ]}),
    ...([
      ["乳幼児健康診査（4回）", "3〜4ヶ月・9〜10ヶ月・1歳6ヶ月・3歳の乳幼児", "無料", "区の保健センターで実施。身体計測・発育確認・保健指導。問診票を事前に記入。"],
      ["定期予防接種（国が定めるもの）", "各ワクチンの対象年齢の乳幼児・小児", "無料", "ヒブ・肺炎球菌・四種混合・BCG・MR（麻疹・風疹）・水痘・日本脳炎・HPV等。区内指定医療機関で受診。"],
      ["発達相談・療育支援", "言語・発達に気になる点のある乳幼児とその保護者", "無料", "保健センターで保健師・言語聴覚士等の専門職が相談対応。必要に応じて療育機関への紹介。"],
      ["保育所・認定こども園", "就学前の乳幼児", "3歳以上：原則無償\n0〜2歳：所得に応じた保育料", "区内認可保育所・こども園。入所申請は毎年10月頃〜翌年1月が主な受付期間。"],
      ["一時保育・緊急保育", "就労・育児疲れ・通院等の理由がある保護者", "1時間 300〜700円程度（施設による）", "リフレッシュ目的での利用も可。事前に施設への登録・予約が必要。"],
      ["子ども食堂", "区内在住の子どもおよびその家族", "無料〜100円", "区内複数箇所で開催。孤食防止・地域交流・食育が目的。NPO・地域団体が運営。"],
    ].map(([name, who, fee, detail]) =>
      new TableRow({ children: [
        makeCell(name, { fill: LPURPLE, bold: true, color: PURPLE, width: 2000 }),
        makeCell(who, { fill: WHITE, width: 1800 }),
        makeCell(fee, { fill: LGREEN, bold: true, color: GREEN, width: 1400, align: AlignmentType.CENTER }),
        makeCell(detail, { fill: WHITE, width: 3226 }),
      ]})
    )),
  ];
  push(makeTable(boshiRows3, [2000, 1800, 1400, 3226]));
  push(space(), note("母子保健に関するお問合せ：文京区保健センター 03-5803-1834（千駄木5-20-18）"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 6. 高齢者向けサービス
  // ================================================================
  push(h1("6. 高齢者向けサービス　─ 65歳・75歳から使える具体的な内容"));

  push(h2("（1）相談・総合支援", ORANGE));
  const korei1 = [
    new TableRow({ children: [
      headerCell("サービス名", 2000, ORANGE),
      headerCell("対象者", 1800, ORANGE),
      headerCell("費用", 1000, ORANGE),
      headerCell("内容・窓口・連絡先", 3626, ORANGE),
    ]}),
    ...([
      {
        name: "高齢者あんしん相談センター\n（地域包括支援センター）",
        who: "65歳以上の区民およびその家族",
        fee: "無料",
        detail: "区内6ヶ所に設置。保健師・社会福祉士・主任ケアマネジャーが常駐。介護・医療・生活上の悩みを一元対応。月〜金 9:00〜19:00、土日祝 9:00〜17:30。",
      },
      {
        name: "介護保険利用相談・\nケアプラン作成支援",
        who: "要支援・要介護認定を受けた方",
        fee: "相談：無料\nケアプラン作成：介護保険適用",
        detail: "要介護認定の申請代行、ケアマネジャーの紹介・マッチング。各地域包括支援センターが窓口。",
      },
    ].map(item =>
      new TableRow({ children: [
        makeCell(item.name, { fill: LORANGE, bold: true, color: ORANGE, width: 2000 }),
        makeCell(item.who, { fill: WHITE, width: 1800 }),
        makeCell(item.fee, { fill: LGREEN, bold: true, color: GREEN, width: 1000, align: AlignmentType.CENTER }),
        makeCell(item.detail, { fill: WHITE, width: 3626 }),
      ]})
    )),
  ];
  push(makeTable(korei1, [2000, 1800, 1000, 3626]));

  push(h2("（2）健診・予防接種", ORANGE));
  const korei2 = [
    new TableRow({ children: [
      headerCell("サービス名", 2000, ORANGE),
      headerCell("対象者", 1800, ORANGE),
      headerCell("費用（自己負担）", 1200, ORANGE),
      headerCell("内容・備考", 3426, ORANGE),
    ]}),
    ...([
      ["後期高齢者健康診査", "75歳以上（後期高齢者医療制度加入者）", "無料", "年1回。問診・身体計測・血圧・血液・尿検査。かかりつけ医でも受診可。6月〜翌年1月頃実施。"],
      ["フレイル健診\n（後期高齢者質問票）", "75歳以上", "無料\n（健診と同時実施）", "身体機能・栄養・口腔・認知・社会参加の5分野をチェック。結果に応じて介護予防プログラムを案内。"],
      ["インフルエンザワクチン\n（定期接種）", "65歳以上", "1,500円\n（区の助成後）", "秋（10月頃〜）に1回接種。区が費用の大部分を助成。区内指定医療機関で受診。生活保護受給者は無料。"],
      ["肺炎球菌ワクチン\n（23価：定期接種）", "65歳（のみ）", "2,000円\n（区の助成後）", "65歳の年度に1回の定期接種。区内指定医療機関で受診。過去に接種歴がある場合は要確認。"],
      ["帯状疱疹ワクチン助成", "50歳以上", "生ワクチン・不活化ワクチン\nともに助成あり（金額は要確認）", "2種類のワクチンいずれも助成対象。詳細は保健センターまたは区内指定医療機関へ。"],
    ].map(([name, who, fee, detail]) =>
      new TableRow({ children: [
        makeCell(name, { fill: LORANGE, bold: true, color: ORANGE, width: 2000 }),
        makeCell(who, { fill: WHITE, width: 1800 }),
        makeCell(fee, { fill: LGREEN, bold: true, color: GREEN, width: 1200, align: AlignmentType.CENTER }),
        makeCell(detail, { fill: WHITE, width: 3426 }),
      ]})
    )),
  ];
  push(makeTable(korei2, [2000, 1800, 1200, 3426]));

  push(h2("（3）介護予防・社会参加", ORANGE));
  const korei3 = [
    new TableRow({ children: [
      headerCell("サービス名", 2000, ORANGE),
      headerCell("対象者", 1800, ORANGE),
      headerCell("費用", 1000, ORANGE),
      headerCell("内容・実施場所", 3626, ORANGE),
    ]}),
    ...([
      ["いきいき体操教室\n（転倒予防）", "65歳以上の区民", "無料", "区内各地のコミュニティセンター・体育館等で定期開催。転倒予防・筋力維持を目的とした運動プログラム。"],
      ["認知症カフェ\n（オレンジカフェ）", "認知症の方・家族・どなたでも", "無料〜少額", "認知症の方と家族が気軽に集える居場所。ボランティアやスタッフが対応。区内複数ヶ所で開催。"],
      ["認知症サポーター養成講座", "区民・企業・団体どなたでも", "無料", "認知症への正しい理解と接し方を学ぶ1〜2時間の講座。区内全域で年複数回開催。修了者にオレンジリングを配布。"],
      ["在宅医療・介護連携相談\n（ACP普及）", "在宅療養中の方・家族", "無料（相談のみ）", "かかりつけ医・訪問看護・ケアマネジャーの連携コーディネート。「人生会議（ACP）」の普及啓発も実施。"],
    ].map(([name, who, fee, detail]) =>
      new TableRow({ children: [
        makeCell(name, { fill: LORANGE, bold: true, color: ORANGE, width: 2000 }),
        makeCell(who, { fill: WHITE, width: 1800 }),
        makeCell(fee, { fill: LGREEN, bold: true, color: GREEN, width: 1000, align: AlignmentType.CENTER }),
        makeCell(detail, { fill: WHITE, width: 3626 }),
      ]})
    )),
  ];
  push(makeTable(korei3, [2000, 1800, 1000, 3626]));
  push(space(), note("高齢者あんしん相談センター（地域包括支援センター）は区内6ヶ所：本郷・小石川・白山・根津・千駄木・駒込 エリアに設置。詳細は文京区HP参照。"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 7. こころの健康
  // ================================================================
  push(h1("7. こころの健康支援　─ 誰でも・無料で相談できる"));
  push(para("精神保健・メンタルヘルスに関する相談は、すべて無料です。一人で抱え込まず、まず電話・来所相談をご利用ください。", { bold: true, color: RED, before: 80, after: 80 }));

  const mentalRows = [
    new TableRow({ children: [
      headerCell("サービス名", 2200, RED),
      headerCell("対象者", 1800, RED),
      headerCell("費用", 700, RED),
      headerCell("内容・連絡先・受付時間", 3726, RED),
    ]}),
    ...([
      {
        name: "精神保健福祉相談",
        who: "精神的な悩みを抱える本人・家族（どなたでも）",
        fee: "無料（要予約）",
        detail: "文京区保健所にて保健師・精神保健福祉士が個別相談対応。うつ・不安障がい・統合失調症等。月〜金（祝休日除く）　TEL：03-5803-1834",
      },
      {
        name: "ひきこもり支援相談",
        who: "ひきこもり状態の本人・家族（8050問題含む）",
        fee: "無料",
        detail: "長期化・高齢化するひきこもりに対応。アウトリーチ（訪問支援）あり。居場所・自助グループの情報提供も実施。TEL：03-5803-1212（福祉部）",
      },
      {
        name: "自殺予防・ゲートキーパー講座",
        who: "区民・企業・支援者（だれでも）",
        fee: "無料",
        detail: "「いのちの電話（0120-783-556）」等の相談窓口を案内。自殺予防のゲートキーパー（気づき・声かけ役）養成研修を年複数回開催。",
      },
      {
        name: "アルコール・薬物・\nギャンブル依存症相談",
        who: "依存症の本人・家族",
        fee: "無料",
        detail: "保健所で個別相談を受付。自助グループ（断酒会・AA等）への紹介、専門医療機関への連携。TEL：03-5803-1834（保健所）",
      },
      {
        name: "認知症初期集中支援チーム",
        who: "物忘れが気になる方・認知症が疑われる方・家族",
        fee: "無料",
        detail: "地域包括支援センターに設置。医師・看護師・社会福祉士等が家庭訪問し、早期支援・医療機関への橋渡しを実施。",
      },
      {
        name: "育児・子育てメンタル相談\n（産後うつを含む）",
        who: "育児に悩む保護者・産後うつが心配な方",
        fee: "無料（要予約）",
        detail: "保健センターの保健師が面談。産後うつのスクリーニング（EPDS）実施。必要に応じて精神科・心療内科へ紹介。TEL：03-5803-1834",
      },
    ].map(item =>
      new TableRow({ children: [
        makeCell(item.name, { fill: LRED, bold: true, color: RED, width: 2200 }),
        makeCell(item.who, { fill: WHITE, width: 1800 }),
        makeCell(item.fee, { fill: LGREEN, bold: true, color: GREEN, width: 700, align: AlignmentType.CENTER }),
        makeCell(item.detail, { fill: WHITE, width: 3726 }),
      ]})
    )),
  ];
  push(makeTable(mentalRows, [2200, 1800, 700, 3726]));
  push(space(), note("24時間対応の相談窓口：よりそいホットライン 0120-279-338　いのちの電話 0120-783-556（無料）"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 8. 予算配分
  // ================================================================
  push(h1("8. 区の予算はどう使われているか　─ 令和7年度 款別内訳"));
  push(para("令和7年度 一般会計当初予算　総額：1,470億円（令和8年度は1,605億円・過去最大規模）", { bold: true, before: 80, after: 80 }));

  const yosanRows = [
    new TableRow({ children: [
      headerCell("款（分野）", 2400, NAVY),
      headerCell("予算額", 1200, NAVY),
      headerCell("構成比", 700, NAVY),
      headerCell("主な内容（健康・保健サービスとの関連）", 4126, NAVY),
    ]}),
    ...([
      ["民生費（福祉・介護・子育て）", "653億円", "40.5%", "生活保護・介護保険・障がい者支援・子ども家庭支援・高齢者施設等を含む。区の最大費目。", LRED],
      ["教育費（学校・生涯学習）", "292億円", "18.1%", "学校運営・教員・給食・スポーツセンター・学校体育館開放・生涯学習施設を含む。", LBLUE],
      ["総務費（行政運営）", "228億円", "14.2%", "庁舎・情報システム・選挙・区民サービス窓口等。補正後は大幅増（公共施設整備）。", LGRAY],
      ["衛生費（保健・医療）", "71億円", "4.4%", "保健所・保健センター運営・健診・がん検診・母子保健・精神保健・感染症対策等。", LGREEN],
      ["土木費（道路・公園）", "64億円", "4.0%", "道路・橋梁・公園整備・都市計画・緑化推進。", LGRAY],
      ["資源環境費（ごみ・環境）", "53億円", "3.3%", "清掃・リサイクル・環境施策・動植物公園。", LGRAY],
      ["区民費（区民サービス）", "51億円", "3.2%", "文化センター・スポーツ施設・区民相談・国際交流等。文京スポーツセンター補助も含む。", LORANGE],
      ["産業経済費", "20億円", "1.2%", "中小企業支援・観光・農林業。", LGRAY],
      ["その他（議会・都市整備・予備費等）", "約38億円", "約2.6%", "議会費・都市整備費・諸支出金・予備費。", LGRAY],
    ].map(([name, amt, pct, detail, fill]) =>
      new TableRow({ children: [
        makeCell(name, { fill, bold: true, color: NAVY, width: 2400 }),
        makeCell(amt, { fill, bold: true, color: "1A3A5C", width: 1200, align: AlignmentType.CENTER }),
        makeCell(pct, { fill, width: 700, align: AlignmentType.CENTER }),
        makeCell(detail, { fill: WHITE, width: 4126 }),
      ]})
    )),
  ];
  push(makeTable(yosanRows, [2400, 1200, 700, 4126]));

  push(space());
  push(para("【健康・保健サービスへの直接投資】", { bold: true, color: NAVY, before: 80, after: 40 }));
  push(makeTable([
    new TableRow({ children: [
      headerCell("費目", 3000, GREEN),
      headerCell("予算額", 1400, GREEN),
      headerCell("1人あたり年間換算（区民24万人）", 4026, GREEN),
    ]}),
    new TableRow({ children: [
      makeCell("衛生費（保健所・健診・母子保健・精神保健等）", { fill: LGREEN, bold: true, color: NAVY, width: 3000 }),
      makeCell("71億円", { fill: LGREEN, bold: true, color: GREEN, width: 1400, align: AlignmentType.CENTER }),
      makeCell("約 2,960円/人", { fill: LGREEN, width: 4026, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      makeCell("民生費のうち高齢者・子育て関連（推計）", { fill: LBLUE, bold: true, color: NAVY, width: 3000 }),
      makeCell("約400億円", { fill: LBLUE, width: 1400, align: AlignmentType.CENTER }),
      makeCell("約 16,700円/人", { fill: LBLUE, width: 4026, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      makeCell("教育費のうちスポーツ・生涯学習関連（推計）", { fill: LORANGE, bold: true, color: NAVY, width: 3000 }),
      makeCell("約30億円", { fill: LORANGE, width: 1400, align: AlignmentType.CENTER }),
      makeCell("約 1,250円/人", { fill: LORANGE, width: 4026, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      makeCell("健康・保健サービス合計（概算）", { fill: LGREEN, bold: true, color: GREEN, width: 3000 }),
      makeCell("約500億円以上", { fill: LGREEN, bold: true, color: GREEN, width: 1400, align: AlignmentType.CENTER }),
      makeCell("区民1人あたり 年間 約2万円以上を健康に投資", { fill: LGREEN, bold: true, color: GREEN, width: 4026, align: AlignmentType.CENTER }),
    ]}),
  ], [3000, 1400, 4026]));
  push(space(), note("款別予算額は令和7年度当初予算。令和8年度は総額1,605億円（前年比+9.2%）に増加。高齢者・子育て関連の推計値は民生費全体からの概算。"));
  push(new Paragraph({ children: [new PageBreak()] }));

  // ================================================================
  // 9. 早見表
  // ================================================================
  push(h1("9. 区民サービス早見表　─ 自分に合うサービスをすぐに探す"));
  push(para("年齢・状況ごとに利用できる主なサービスをまとめました。詳細は各窓口または文京区HP（city.bunkyo.lg.jp）でご確認ください。", { before: 60, after: 80 }));

  const hayamiRows = [
    new TableRow({ children: [
      headerCell("あなたの状況", 1900, NAVY),
      headerCell("使えるサービス", 2800, NAVY),
      headerCell("費用", 1200, NAVY),
      headerCell("窓口・連絡先", 2526, NAVY),
    ]}),
    ...([
      ["妊娠中", "妊婦健診14回・超音波4回・子宮頸がん検診1回・両親学級", "健診：助成あり（差額自己負担）/ 教室：無料", "保健センター 03-5803-1834"],
      ["産後（1年以内）", "訪問型産後ケア（助産師）・育児相談・産後ドゥーラ紹介", "3,000円/回（最大3回）/ 相談：無料", "保健センター 03-5803-1834"],
      ["乳幼児のいる家庭", "乳幼児健診4回・定期予防接種・発達相談・子ども食堂", "健診・接種：無料 / 食堂：0〜100円", "保健センター / 子育て支援課"],
      ["20歳以上の女性（偶数年齢）", "子宮がん検診（2年に1回）", "無料", "区内委託医療機関に電話予約"],
      ["40歳以上（国保加入）", "特定健診＋大腸がん・肺がん・胃がん検診（同時受診可）", "すべて無料", "区内指定医療機関に電話予約"],
      ["40歳以上の女性（偶数年齢）", "乳がん検診（マンモグラフィ）", "無料", "区内委託医療機関に電話予約"],
      ["スポーツをしたい全員", "スポーツ交流ひろば（学校体育館・10種目）", "無料・申込不要", "直接会場へ / スポーツ振興課 03-5803-1303"],
      ["スポーツ施設を利用したい", "文京スポーツセンター（プール・トレーニング等）", "一般：550円〜 / 定期：4,600円/月", "03-3946-6311"],
      ["65〜69歳（スポーツ施設）", "シルバー料金でプール・トレーニングルーム利用", "プール280円 / トレーニング300円（事前登録要）", "文京スポーツセンター窓口で登録"],
      ["70歳以上（スポーツ施設）", "プール・トレーニングルーム利用", "無料（登録証要）", "文京スポーツセンター 03-3946-6311"],
      ["65歳以上", "インフルエンザ接種・地域包括支援センター相談", "接種1,500円 / 相談：無料", "区内指定医療機関 / 包括支援センター"],
      ["75歳以上", "後期高齢者健診・フレイル健診・介護予防教室", "すべて無料", "かかりつけ医 / 保健センター"],
      ["介護が心配になってきた", "地域包括支援センターへ相談（要介護認定の申請代行も）", "相談：無料", "最寄りの包括支援センター（区内6ヶ所）"],
      ["こころの悩みがある", "精神保健相談・ひきこもり支援・依存症相談", "すべて無料（要予約）", "保健所 03-5803-1834"],
      ["認知症が心配", "認知症初期集中支援・認知症カフェ・サポーター講座", "無料", "地域包括支援センター"],
    ].map(([situation, service, fee, desk]) =>
      new TableRow({ children: [
        makeCell(situation, { fill: LBLUE, bold: true, color: NAVY, width: 1900 }),
        makeCell(service, { fill: WHITE, width: 2800 }),
        makeCell(fee, { fill: LGREEN, color: GREEN, bold: true, width: 1200 }),
        makeCell(desk, { fill: WHITE, width: 2526 }),
      ]})
    )),
  ];
  push(makeTable(hayamiRows, [1900, 2800, 1200, 2526]));
  push(space(), note("本資料に掲載の料金・対象要件は令和7〜8年度のものです。変更になる場合があります。"));

  return children;
}

// ────────────────────────────────────────────────────────────────────
// Document 組み立て
// ────────────────────────────────────────────────────────────────────
async function main() {
  const content = buildContent();

  const doc = new Document({
    numbering: {
      config: [{
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "●",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 560, hanging: 280 } } },
        }],
      }],
    },
    styles: {
      default: {
        document: { run: { font: "Arial", size: 20 } },
      },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 36, bold: true, font: "Arial", color: WHITE },
          paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 },
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, font: "Arial" },
          paragraph: { spacing: { before: 240, after: 80 }, outlineLevel: 1 },
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, font: "Arial" },
          paragraph: { spacing: { before: 160, after: 60 }, outlineLevel: 2 },
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },   // A4
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: NAVY } },
            spacing: { after: 60 },
            children: [new TextRun({ text: "文京区 保健・健康サービス完全ガイド　2026年7月", size: 16, font: "Arial", color: GRAY })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: NAVY } },
            spacing: { before: 60 },
            children: [
              new TextRun({ text: "文京区　政策スタッフ資料　　", size: 16, font: "Arial", color: GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, font: "Arial", color: GRAY }),
              new TextRun({ text: " / ", size: 16, font: "Arial", color: GRAY }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, font: "Arial", color: GRAY }),
            ],
          })],
        }),
      },
      children: content,
    }],
  });

  const buffer = await Packer.toBuffer(doc);
  const outFile = "bunkyo_health_guide.docx";
  fs.writeFileSync(outFile, buffer);
  console.log("✅ Written:", outFile);
}

main().catch(err => { console.error(err); process.exit(1); });
