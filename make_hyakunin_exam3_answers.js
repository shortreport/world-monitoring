const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, Header
} = require('docx');
const fs = require('fs');

const JP = "MS Mincho";
const B = 22;
const S = 20;
const L = 26;

function t(text, opts = {}) {
  return new TextRun({ text, font: JP, size: B, ...opts });
}
function tS(text, opts = {}) {
  return new TextRun({ text, font: JP, size: S, ...opts });
}
function tRed(text) {
  return new TextRun({ text, font: JP, size: B, color: "CC0000", bold: true });
}
function p(children, opts = {}) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({ children, spacing: { before: 60, after: 60 }, ...opts });
}
function pAns(children, opts = {}) {
  // 解答行（インデント付き、赤字）
  if (typeof children === 'string') children = [tRed(children)];
  return new Paragraph({ children, indent: { left: 480 }, spacing: { before: 40, after: 40 }, ...opts });
}
function pIn(children, left = 480) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({ children, indent: { left }, spacing: { before: 40, after: 40 } });
}
function h(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP, size: 24, bold: true })],
    spacing: { before: 220, after: 100 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "CC0000" } }
  });
}
function qt(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP, size: B, bold: true })],
    spacing: { before: 160, after: 80 }
  });
}
function sp(before = 100) {
  return new Paragraph({ children: [], spacing: { before, after: 0 } });
}
const bdr = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const bdrs = { top: bdr, bottom: bdr, left: bdr, right: bdr };

function cell(text, w, opts = {}) {
  const { bold = false, center = false, shade = false, red = false } = opts;
  return new TableCell({
    borders: bdrs,
    width: { size: w, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    shading: shade ? { fill: "EEEEEE", type: "clear" } : undefined,
    children: [new Paragraph({
      children: [new TextRun({ text, font: JP, size: S, bold, color: red ? "CC0000" : "000000" })],
      alignment: center ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { before: 20, after: 20 }
    })]
  });
}

function scoreTable(items) {
  // items: [{label, score}]
  const w = Math.floor(9000 / items.length);
  return new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: Array(items.length).fill(w),
    rows: [
      new TableRow({ children: items.map(it => new TableCell({
        borders: bdrs,
        width: { size: w, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 80, right: 80 },
        shading: { fill: "EEEEEE", type: "clear" },
        children: [new Paragraph({ children: [tS(it.label, { bold: true })], alignment: AlignmentType.CENTER })]
      })) }),
      new TableRow({ children: items.map(it => new TableCell({
        borders: bdrs,
        width: { size: w, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 80, right: 80 },
        children: [new Paragraph({
          children: [new TextRun({ text: it.score, font: JP, size: S, color: "CC0000", bold: true })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 60, after: 60 }
        })]
      })) })
    ]
  });
}

// ===========================
// 解答表（大問一）
// ===========================
const daiichiData = [
  { no:"74", au:"源俊頼朝臣",              season:"なし（恋）" },
  { no:"75", au:"藤原基俊",                season:"ウ（秋）" },
  { no:"76", au:"法性寺入道前関白太政大臣", season:"なし（海景）" },
  { no:"77", au:"崇徳院",                  season:"なし（恋）" },
  { no:"78", au:"源兼昌",                  season:"エ（冬）" },
  { no:"79", au:"左京大夫顕輔",            season:"ウ（秋）" },
  { no:"80", au:"待賢門院堀河",            season:"なし（恋）" },
  { no:"81", au:"後徳大寺左大臣",          season:"イ（夏）" },
  { no:"82", au:"道因法師",                season:"なし（恋・述懐）" },
];

const children = [

  // ---- タイトル ----
  new Paragraph({
    children: [new TextRun({ text: "百人一首　試験問題（第三回）　解答・解説", font: JP, size: 32, bold: true, color: "CC0000" })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 80 }
  }),
  new Paragraph({
    children: [tS("（出題範囲：七十四番〜八十二番）")],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 200 }
  }),

  // ========== 大問一 ==========
  h("大問一　短歌・作者・内容の対応　（各１点　計１８点）"),
  qt("作者名①〜⑨および季節の解答"),

  new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [700, 700, 2600, 1800, 1700, 1500],
    rows: [
      new TableRow({ children: [
        cell("番号", 700, { bold:true, shade:true, center:true }),
        cell("問番号", 700, { bold:true, shade:true, center:true }),
        cell("作者名", 2600, { bold:true, shade:true }),
        cell("読み方", 1800, { bold:true, shade:true }),
        cell("季節（記号）", 1700, { bold:true, shade:true, center:true }),
        cell("配点", 1500, { bold:true, shade:true, center:true }),
      ] }),
      ...daiichiData.map((d, i) =>
        new TableRow({ children: [
          cell(d.no, 700, { center:true }),
          cell(`${i+1}`, 700, { center:true }),
          cell(d.au, 2600, { red:true, bold:true }),
          cell(["みなもとのとしよりあそん","ふじわらのもととし","ほっしょうじにゅうどう…","すとくいん","みなもとのかねまさ","さきょうのだいぶあきすけ","たいけんもんいんのほりかわ","ごとくだいじのさだいじん","どういんほうし"][i], 1800),
          cell(d.season, 1700, { red:true, bold:true, center:true }),
          cell("各1点×2", 1500, { center:true }),
        ] })
      )
    ]
  }),

  sp(60),
  p([t("※季節「なし」について：問題文に「なし」を選択肢に含む旨を明記しているため、"), tRed("「なし」も正答として認める。")]),
  sp(200),

  // ========== 大問二 ==========
  h("大問二　語句の意味　（各１点　計６点）"),

  new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [400, 2400, 1400, 4800],
    rows: [
      new TableRow({ children: [
        cell("番", 400, { bold:true, shade:true, center:true }),
        cell("問われた語句", 2400, { bold:true, shade:true }),
        cell("正答", 1400, { bold:true, shade:true, center:true }),
        cell("解説", 4800, { bold:true, shade:true }),
      ] }),
      ...[
        ["１","「あはれ」（七十五番）","ロ","感動詞として使われており、「ああ」という嘆きの意。形容動詞の「哀れなり」とは異なる。"],
        ["２","「幾夜」（七十八番）","ロ","「いく（幾）」は数の不確定を示し「何夜も・いったい何夜」の意。"],
        ["３","「ながむれば」（八十一番）","ロ","「ながむ」は「眺む」＝見渡す・じっと見る。「詠む」と混同しないこと。"],
        ["４","「有明」（八十一番）","ロ","夜明けごろ、まだ空に残っている月のこと。「有明の月」は古典の頻出語。"],
        ["５","「さても」（八十二番）","イ","「さ（そう）＋ても（〜ても）」で「それでも・そうであっても」の意。"],
        ["６","「憂き」（八十二番）","ロ","形容詞「憂し」の連体形。つらい・苦しいの意。「浮き」との掛詞にもなりやすい語。"],
      ].map(([no, ko, ans, ex]) =>
        new TableRow({ children: [
          cell(no, 400, { center:true }),
          cell(ko, 2400),
          cell(ans, 1400, { red:true, bold:true, center:true }),
          cell(ex, 4800),
        ] })
      )
    ]
  }),
  sp(200),

  // ========== 大問三 ==========
  h("大問三　文法事項　（各２点　計１０点）"),

  qt("１．八十一番「月ぞ残れる」の係り結び"),
  pAns("（１）係助詞：ぞ"),
  pAns("（２）「残れる」の活用形：連体形"),
  pAns("（３）「る」の意味：ロ　存続（〜ている）"),
  pIn([t("【解説】"), t("「ぞ」は係助詞で、文末を連体形に結ぶ。「残れる」の「る」は完了の助動詞「り」の連体形。この文脈では「残っている」という存続の意味で使われている。")]),

  sp(80),
  qt("２．「涙なりけり」の「けり」"),
  pAns("ロ　詠嘆（〜だなあ・〜であったことよ）"),
  pIn([t("【解説】"), t("「けり」は過去と詠嘆の二用法を持つ。和歌の末尾に置かれる場合は詠嘆が多い。「涙であったことよ」と感慨を込めた表現。")]),

  sp(80),
  qt("３．「あはむとぞ思ふ」の「む」"),
  pAns("ロ　意志（〜しよう・〜と思う）"),
  pIn([t("【解説】"), t("「あはむとぞ思ふ」は「逢おうと（私は）思う」という一人称の意志。「む」が一人称主語とともに使われる場合は意志の用法。")]),

  sp(80),
  qt("４．「ものをこそ思へ」のこそ〜の活用形"),
  pAns("已然形"),
  pIn([t("【解説】"), t("係助詞「こそ」は文末を已然形に結ぶ（こそ→已然形）。「思へ」はハ行四段活用「思ふ」の已然形。")]),

  sp(80),
  qt("５．「いぬめり」の「めり」"),
  pAns("品詞：推量の助動詞　　意味：〜ようだ・〜と見える（視覚的推量）"),
  pIn([t("【解説】"), t("「めり」は視覚を根拠とした推量を表す助動詞。「行ってしまうようだ」と目の前の様子から推量している。")]),

  sp(200),

  // ========== 大問四 ==========
  h("大問四　修辞技法・表現　（各２点　計８点）"),

  qt("１．枕詞と被修飾語の正しい組み合わせ"),
  pAns("正しいもの：ア・イ・ウ　（エは誤り）"),
  pIn([t("【解説】"), t("「ひさかたの」は空・天・雲・月などにかかる枕詞（ア○）。「たらちねの」は母にかかる（イ○）。「あしびきの」は山にかかる（ウ○）。「ほととぎす」は枕詞ではなく、単に情景を描く名詞（エ✕）。")]),

  sp(80),
  qt("２．七十七番の序詞が導く「本意」の説明"),
  p([t("（模範解答例）")]),
  pAns("（たとえ今は）あなたと離れてしまっても、いつか（末に）再び逢おうと思っている。"),
  pIn([t("【解説】"), t("「瀬をはやみ〜滝川の」が序詞で、「われても」以降の「（私が）離れても」という本意へとつながる。川が二手に分かれても下流で合流することを、男女の別れと再会に重ねた序詞。")]),

  sp(80),
  qt("３．八十一番の表現上の特徴"),
  pAns("イ　ほととぎすの声が聞こえたのに姿は見えず、残るのは月だけという余情を詠む"),
  pIn([t("【解説】"), t("ほととぎすの声に導かれて空を見渡すと、もう鳥の姿はなく有明の月だけが残っている。声と月の対比、不在の余韻が歌の魅力。")]),

  sp(80),
  qt("４．七十四番「山おろしよ」の呼びかける技法"),
  pAns("擬人（法）"),
  pIn([t("【解説】"), t("無生物の「山おろし（山風）」に「よ」と呼びかけることで、まるで意志を持つ存在のように扱っている。これを擬人法という。")]),

  sp(200),

  // ========== 大問五 ==========
  h("大問五　現代語訳　（各３点　計６点）"),

  qt("１．八十一番　後徳大寺左大臣"),
  p([t("ほととぎす　鳴きつる方を　ながむれば　ただ有明の　月ぞ残れる")]),
  sp(40),
  p([t("（模範解答）")]),
  pAns("ほととぎすが鳴いた方向を眺めてみると、（その姿はどこにもなく）ただ夜明けの月だけが（空に）残っていることよ。"),
  pIn([t("【採点のポイント】"), t("「鳴きつる方」＝鳴いていた方向 / 「ながむれば」＝眺めると / 「有明の月」＝夜明けの月 / 「ぞ〜残れる」の係り結びを反映した訳。")]),

  sp(120),
  qt("２．八十二番　道因法師"),
  p([t("思ひわびさても　命は　あるものを　憂きにたへぬは　涙なりけり")]),
  sp(40),
  p([t("（模範解答）")]),
  pAns("（恋に）思い悩んでも、それでも命だけはあり続けるものを、このつらさに耐えられないのは（この）涙なのだなあ。"),
  pIn([t("【採点のポイント】"), t("「思ひわびさても」＝思い悩んでも / 「あるものを」＝あるのに（逆接・詠嘆） / 「憂きにたへぬ」＝つらさに耐えられない / 「なりけり」の詠嘆を反映した訳。")]),

  sp(200),

  // ========== 大問六 ==========
  h("大問六　内容理解・作者背景　（各２点　計１０点）"),

  new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [400, 1200, 6800, 600],
    rows: [
      new TableRow({ children: [
        cell("問", 400, { bold:true, shade:true, center:true }),
        cell("正答", 1200, { bold:true, shade:true, center:true }),
        cell("解説", 6800, { bold:true, shade:true }),
        cell("配点", 600, { bold:true, shade:true, center:true }),
      ] }),
      ...[
        ["１", "イ",
         "「ほととぎす」は夏の鳥であり、和歌では初夏の到来を告げる存在として詠まれる。夏の代表的な季語・季題のひとつ。",
         "2点"],
        ["２", "イ",
         "道因法師（1090?〜1182?）は平安時代後期の歌人。俗名は藤原敦頼。晩年も和歌への情熱を衰えさせず、99歳まで歌を詠み続けたとされる。",
         "2点"],
        ["３", "74・77・80・82番",
         "74番（冷たい人への恋の祈り）、77番（離れても再会を誓う恋）、80番（男の心を知らず思い悩む女心）、82番（恋に思い悩む述懐）。75番は息子の昇任を嘆く歌であり「恋」には含めない。",
         "2点"],
        ["４（１）", "78番",
         "「淡路島かよふ千鳥の鳴く声に　幾夜寝覚めぬ須磨の関守」千鳥の声に何度も夜が明けてしまう須磨の情景。",
         "各\n0.5点"],
        ["４（２）", "79番",
         "「秋風にたなびく雲の絶え間より　もれ出づる月の影のさやけさ」雲の切れ間から月光が漏れる秋の情景。",
         ""],
        ["４（３）", "77番",
         "「瀬をはやみ〜われても末にあはむとぞ思ふ」川が分かれても合流するように再会を誓う恋。",
         ""],
        ["４（４）", "81番",
         "「ほととぎす鳴きつる方をながむれば　ただ有明の月ぞ残れる」姿なく月だけが残る夏の情景。",
         ""],
        ["５", "イ（藤原定家）",
         "百人一首（小倉百人一首）は鎌倉時代初期に藤原定家が撰んだ歌集。紀貫之は古今和歌集の撰者、藤原道長・在原業平は百人一首の撰者ではない。",
         "2点"],
      ].map(([no, ans, ex, pt]) =>
        new TableRow({ children: [
          cell(no, 400, { center:true }),
          cell(ans, 1200, { red:true, bold:true, center:true }),
          cell(ex, 6800),
          cell(pt, 600, { center:true }),
        ] })
      )
    ]
  }),

  sp(200),

  // ========== 配点まとめ ==========
  h("【配点まとめ】"),
  scoreTable([
    { label: "大問一", score: "18点" },
    { label: "大問二", score: "6点" },
    { label: "大問三", score: "10点" },
    { label: "大問四", score: "8点" },
    { label: "大問五", score: "6点" },
    { label: "大問六", score: "10点" },
    { label: "合　計", score: "58点" },
  ]),
];

// ============================
// 生成
// ============================
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: "【解答・解説】百人一首（第三回）　七十四番〜八十二番", font: JP, size: S, color: "CC0000" })],
          alignment: AlignmentType.RIGHT
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("hyakunin_exam3_answers.docx", buf);
  console.log("Done: hyakunin_exam3_answers.docx");
});
