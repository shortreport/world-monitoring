const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, Header
} = require('docx');
const fs = require('fs');

const JP = "MS Mincho";
const B = 22;   // 11pt
const S = 20;   // 10pt
const L = 26;   // 13pt

function t(text, opts = {}) {
  return new TextRun({ text, font: JP, size: B, ...opts });
}
function tS(text, opts = {}) {
  return new TextRun({ text, font: JP, size: S, ...opts });
}
function p(children, opts = {}) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({ children, spacing: { before: 60, after: 60 }, ...opts });
}
function pIn(children, left = 480) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({ children, indent: { left }, spacing: { before: 40, after: 40 } });
}
function h(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP, size: 24, bold: true })],
    spacing: { before: 220, after: 100 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000" } }
  });
}
function qt(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP, size: B, bold: true })],
    spacing: { before: 160, after: 80 }
  });
}
function waka(l1, l2) {
  return [
    new Paragraph({ children: [t(l1)], indent: { left: 720 }, spacing: { before: 40, after: 0 } }),
    new Paragraph({ children: [t(l2)], indent: { left: 720 }, spacing: { before: 0, after: 60 } })
  ];
}
function sp(before = 100) {
  return new Paragraph({ children: [], spacing: { before, after: 0 } });
}
const bdr = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const bdrs = { top: bdr, bottom: bdr, left: bdr, right: bdr };
const noBdr = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBdrs = { top: noBdr, bottom: noBdr, left: noBdr, right: noBdr };

function cell(text, w, opts = {}) {
  const { bold = false, center = false, shade = false } = opts;
  return new TableCell({
    borders: bdrs,
    width: { size: w, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    shading: shade ? { fill: "EEEEEE", type: "clear" } : undefined,
    children: [new Paragraph({
      children: [new TextRun({ text, font: JP, size: S, bold })],
      alignment: center ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { before: 20, after: 20 }
    })]
  });
}
function writeBox(rows = 3) {
  return new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: [8000],
    rows: Array(rows).fill(null).map(() =>
      new TableRow({ children: [new TableCell({
        borders: bdrs,
        width: { size: 8000, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({ children: [t("　")], spacing: { before: 60, after: 60 } })]
      })] })
    )
  });
}
function answerRow(labels) {
  const w = Math.floor(8000 / labels.length);
  return new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: Array(labels.length).fill(w),
    rows: [
      new TableRow({ children: labels.map(lbl => new TableCell({
        borders: bdrs,
        width: { size: w, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 60, right: 60 },
        children: [
          new Paragraph({ children: [tS(lbl)], alignment: AlignmentType.CENTER }),
          new Paragraph({ children: [t("　")], spacing: { before: 180, after: 0 } })
        ]
      })) })
    ]
  });
}

// ============================
// 全9首データ
// ============================
const poems = [
  { no:"74", num:"七十四番", au:"源俊頼朝臣",          yomi:"みなもとのとしよりあそん",              l1:"うかりける　人を初瀬の　山おろしよ",      l2:"はげしかれとは　祈らぬものを",    season:"なし（恋）" },
  { no:"75", num:"七十五番", au:"藤原基俊",              yomi:"ふじわらのもととし",                    l1:"契りおきし　させもが露を　命にて",        l2:"あはれ今年の　秋もいぬめり",      season:"秋" },
  { no:"76", num:"七十六番", au:"法性寺入道前関白太政大臣", yomi:"ほっしょうじにゅうどうさきのかんぱく", l1:"わたの原　漕ぎ出でて見れば　ひさかたの",  l2:"雲居にまがふ　沖つ白波",          season:"なし（海景）" },
  { no:"77", num:"七十七番", au:"崇徳院",                yomi:"すとくいん",                            l1:"瀬をはやみ　岩にせかるる　滝川の",       l2:"われても末に　あはむとぞ思ふ",    season:"なし（恋）" },
  { no:"78", num:"七十八番", au:"源兼昌",                yomi:"みなもとのかねまさ",                    l1:"淡路島　かよふ千鳥の　鳴く声に",         l2:"幾夜寝覚めぬ　須磨の関守",        season:"冬" },
  { no:"79", num:"七十九番", au:"左京大夫顕輔",          yomi:"さきょうのだいぶあきすけ",              l1:"秋風に　たなびく雲の　絶え間より",       l2:"もれ出づる月の　影のさやけさ",    season:"秋" },
  { no:"80", num:"八十番",   au:"待賢門院堀河",          yomi:"たいけんもんいんのほりかわ",            l1:"長からむ　心も知らず　黒髪の",           l2:"乱れてけさは　ものをこそ思へ",    season:"なし（恋）" },
  { no:"81", num:"八十一番", au:"後徳大寺左大臣",        yomi:"ごとくだいじのさだいじん（藤原実定）",  l1:"ほととぎす　鳴きつる方を　ながむれば",   l2:"ただ有明の　月ぞ残れる",          season:"夏" },
  { no:"82", num:"八十二番", au:"道因法師",              yomi:"どういんほうし",                        l1:"思ひわびさても　命は　あるものを",       l2:"憂きにたへぬは　涙なりけり",      season:"なし（恋・述懐）" },
];

// ============================
// 本文
// ============================
const children = [

  // ---- タイトル ----
  new Paragraph({
    children: [new TextRun({ text:"百人一首　試験問題（第三回）", font:JP, size:32, bold:true })],
    alignment: AlignmentType.CENTER,
    spacing: { before:0, after:80 }
  }),
  new Paragraph({
    children: [tS("（出題範囲：七十四番～八十二番）")],
    alignment: AlignmentType.CENTER,
    spacing: { before:0, after:200 }
  }),

  // ---- 参考：歌一覧 ----
  h("【参考】出題範囲の短歌一覧（七十四番〜八十二番）"),
  ...poems.flatMap(pm => [
    p([t(`${pm.num}　${pm.au}`, { bold:true })]),
    ...waka(pm.l1, pm.l2)
  ]),
  sp(200),

  // ========== 大問一：総合マッチング表 ==========
  h("大問一　短歌・作者・内容の対応"),
  qt("問一　次の表の空欄①〜⑨に入る作者名を答えなさい。また、各歌の季節を下のア〜エから選びなさい。（各１点、計１８点）"),

  // 大きな表
  new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [800, 2800, 2200, 1600, 1600],
    rows: [
      new TableRow({ children: [
        cell("番号", 800, { bold:true, center:true, shade:true }),
        cell("短　歌（上の句）", 2800, { bold:true, shade:true }),
        cell("作　者", 2200, { bold:true, center:true, shade:true }),
        cell("作者名（①〜⑨）", 1600, { bold:true, center:true, shade:true }),
        cell("季節（ア〜エ）", 1600, { bold:true, center:true, shade:true }),
      ] }),
      ...poems.map((pm, i) =>
        new TableRow({ children: [
          cell(pm.no, 800, { center:true }),
          cell(pm.l1, 2800),
          cell(pm.au, 2200),
          cell(`（　${i+1}　）`, 1600, { center:true }),
          cell("（　　）", 1600, { center:true }),
        ] })
      )
    ]
  }),

  sp(80),
  p([t("【季節の選択肢】　ア　春　　イ　夏　　ウ　秋　　エ　冬（または「なし」も選択肢に含む）")]),
  sp(200),

  // ========== 大問二：語句の意味 ==========
  h("大問二　語句の意味"),
  qt("問二　次の語句の意味として最も適切なものをイ〜ニから選びなさい。（各１点）"),

  p("１．七十五番「あはれ今年の秋もいぬめり」の「あはれ」の品詞と意味"),
  pIn("イ　形容動詞（哀れな）　　　ロ　感動詞（ああ・嘆き）"),
  pIn("ハ　名詞（哀愁）　　　　　 ニ　副詞（しみじみと）"),

  p("２．七十八番「幾夜寝覚めぬ」の「幾夜」の意味"),
  pIn("イ　一晩だけ　　ロ　何夜も　　ハ　長い夜　　ニ　静かな夜"),

  p("３．八十一番「鳴きつる方をながむれば」の「ながむれば」の意味"),
  pIn("イ　歌を詠むと　　ロ　眺めると・見渡すと　　ハ　泣くと　　ニ　思うと"),

  p("４．八十一番「ただ有明の月ぞ残れる」の「有明」とは"),
  pIn("イ　夕暮れどきの赤い空　　　ロ　夜明けごろ空に残る月"),
  pIn("ハ　明け方の暗い空　　　　　ニ　明るい真昼の空"),

  p("５．八十二番「思ひわびさても命はあるものを」の「さても」の意味"),
  pIn("イ　それでも・そうはいっても　　ロ　ますます　　ハ　なぜか　　ニ　やはり"),

  p("６．八十二番「憂きにたへぬは涙なりけり」の「憂き」の意味"),
  pIn("イ　美しい　　ロ　つらい・憂鬱な　　ハ　激しい　　ニ　楽しい"),

  sp(80),
  p("【解答欄】"),
  answerRow(["１","２","３","４","５","６"]),
  sp(200),

  // ========== 大問三：文法事項 ==========
  h("大問三　文法事項"),
  qt("問三　次の問いに答えなさい。（各２点）"),

  p("１．八十一番「月ぞ残れる」の係り結びについて答えなさい。"),
  pIn("（１）係助詞は何か。→（　　　）"),
  pIn("（２）「残れる」の活用形は何か。→（　　　　　）形"),
  pIn("（３）この「る」（完了・存続）の助動詞の意味として正しいものを選びなさい。"),
  pIn("　　　イ　完了（〜した）　　ロ　存続（〜ている）　　ハ　受身　　ニ　可能", 960),

  sp(60),
  p("２．八十二番「涙なりけり」の「けり」の意味・用法を選びなさい。"),
  pIn("イ　過去（〜た）　　ロ　詠嘆（〜だなあ・〜であったことよ）"),
  pIn("ハ　伝聞推定（〜ということだ）　　ニ　比況（〜のようだ）"),

  sp(60),
  p("３．七十七番「われても末にあはむとぞ思ふ」の「む」の意味を選びなさい。"),
  pIn("イ　推量　　ロ　意志　　ハ　婉曲　　ニ　勧誘"),

  sp(60),
  p("４．八十番「ものをこそ思へ」の係り結びで、「こそ」に呼応する活用形は何か。"),
  pIn("→（　　　　　　　）形"),

  sp(60),
  p("５．七十五番「いぬめり」の「めり」の品詞と意味を答えなさい。"),
  pIn("品詞：（　　　　　　　　　　）　　　意味：（　　　　　　　　　　　　）"),

  sp(200),

  // ========== 大問四：修辞技法 ==========
  h("大問四　修辞技法・表現"),
  qt("問四　次の問いに答えなさい。（各２点）"),

  p("１．次のうち、枕詞と被修飾語の組み合わせとして正しいものをすべて選びなさい。"),
  pIn("ア　ひさかたの→雲居（七十六番）"),
  pIn("イ　たらちねの→母"),
  pIn("ウ　あしびきの→山"),
  pIn("エ　ほととぎす→月（八十一番）"),
  p("　　→正しいものの記号：（　　　　　）"),

  sp(60),
  p("２．七十七番「瀬をはやみ岩にせかるる滝川の」は序詞である。「われても」以降の本意（本来言いたいこと）を現代語で簡潔に説明しなさい。"),
  writeBox(2),

  sp(60),
  p("３．八十一番の歌の表現上の特徴として最も適切なものを選びなさい。"),
  pIn("イ　ほととぎすの声が聞こえたのに姿は見えず、残るのは月だけという余情を詠む"),
  pIn("ロ　ほととぎすと月を対比させ、夏の景色の明るさを詠む"),
  pIn("ハ　ほととぎすの声の美しさを直接的に称える"),
  pIn("ニ　有明の月の輝きの激しさを詠む"),

  sp(60),
  p("４．七十四番「山おろしよ」の「よ」は、山おろし（山から吹きおろす風）に呼びかける表現である。このような技法の名称を漢字で答えなさい。"),
  pIn("→（　　　　　　　　　）法"),

  sp(200),

  // ========== 大問五：現代語訳 ==========
  h("大問五　現代語訳"),
  qt("問五　次の短歌を現代語訳しなさい。（各３点）"),

  p("１．八十一番　後徳大寺左大臣"),
  ...waka("ほととぎす　鳴きつる方を　ながむれば","ただ有明の　月ぞ残れる"),
  sp(40),
  p("現代語訳："),
  writeBox(3),

  sp(120),
  p("２．八十二番　道因法師"),
  ...waka("思ひわびさても　命は　あるものを","憂きにたへぬは　涙なりけり"),
  sp(40),
  p("現代語訳："),
  writeBox(3),

  sp(200),

  // ========== 大問六：内容理解・総合 ==========
  h("大問六　内容理解・作者背景"),
  qt("問六　次の問いに答えなさい。（各２点）"),

  p("１．「ほととぎす」は何の象徴として和歌で多く詠まれるか、最も適切なものを選びなさい。"),
  pIn("イ　夏の到来・初夏の訪れ　　ロ　春の終わり　　ハ　冬の寂しさ　　ニ　秋の夕暮れ"),

  sp(60),
  p("２．八十二番の作者・道因法師について正しいものを選びなさい。"),
  pIn("イ　平安時代後期の僧で、和歌を詠むことに情熱を持ち続けた歌人"),
  pIn("ロ　室町時代の連歌師"),
  pIn("ハ　奈良時代の宮廷歌人"),
  pIn("ニ　鎌倉時代の武家出身の歌人"),

  sp(60),
  p("３．七十四番から八十二番の歌のうち、「恋」を主題とする歌はどれか。番号をすべて答えなさい。"),
  p("　　→（　　　　　　　　　　　　　　　　　　　　　　　　　）番"),

  sp(60),
  p("４．次の説明に当てはまる歌の番号を答えなさい。"),
  pIn("（１）千鳥の声に何度も夜が明けるまで目が覚めてしまう、須磨の関守の情景を詠んだ歌。→（　　）番"),
  pIn("（２）雲の切れ目から漏れ出る月光の清らかさを詠んだ秋の歌。→（　　）番"),
  pIn("（３）川の流れが二手に分かれてもいつか合流するように、離れても再会を誓う恋の歌。→（　　）番"),
  pIn("（４）鳴いたはずのほととぎすの姿はなく、有明の月だけが残っていた夏の歌。→（　　）番"),

  sp(60),
  p("５．百人一首を撰んだ人物として正しいものを選びなさい。"),
  pIn("イ　藤原定家　　ロ　紀貫之　　ハ　藤原道長　　ニ　在原業平"),

  sp(240),

  // ---- 得点集計欄 ----
  h("【得点集計欄】"),
  new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [1500, 1500, 1500, 1500, 1500, 1500],
    rows: [
      new TableRow({ children: [
        "大問一（１８点）","大問二（６点）","大問三（１０点）","大問四（８点）","大問五（６点）","大問六（１０点）"
      ].map((label, i) =>
        new TableCell({
          borders: bdrs,
          width: { size: 1500, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 80, right: 80 },
          children: [new Paragraph({ children: [tS(label, { bold: i===5 })], alignment: AlignmentType.CENTER })]
        })
      ) }),
      new TableRow({ children: [
        "　","　","　","　","　","合計（５８点）"
      ].map((label, i) =>
        new TableCell({
          borders: bdrs,
          width: { size: 1500, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 80, right: 80 },
          children: [new Paragraph({
            children: [new TextRun({ text: label, font: JP, size: S, bold: i===5 })],
            alignment: AlignmentType.CENTER,
            spacing: { before: 200, after: 200 }
          })]
        })
      ) })
    ]
  }),
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
          children: [tS("百人一首試験（第三回）　七十四番〜八十二番")],
          alignment: AlignmentType.RIGHT
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("hyakunin_exam3.docx", buf);
  console.log("Done: hyakunin_exam3.docx");
});
