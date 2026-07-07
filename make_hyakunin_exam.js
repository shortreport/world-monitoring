const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageNumber, Header, Footer, HeadingLevel
} = require('docx');
const fs = require('fs');

// ====== スタイル定義 ======
const JP_FONT = "MS Mincho";
const TITLE_SIZE = 28;   // 14pt
const BODY_SIZE = 22;    // 11pt
const SMALL_SIZE = 20;   // 10pt

function t(text, opts = {}) {
  return new TextRun({ text, font: JP_FONT, size: BODY_SIZE, ...opts });
}

function para(children, opts = {}) {
  if (typeof children === 'string') {
    children = [t(children)];
  }
  return new Paragraph({ children, spacing: { before: 60, after: 60 }, ...opts });
}

function heading(text, level = 1) {
  const size = level === 1 ? 28 : 24;
  return new Paragraph({
    children: [new TextRun({ text, font: JP_FONT, size, bold: true })],
    spacing: { before: 200, after: 100 },
    border: level === 1 ? {
      bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000" }
    } : undefined
  });
}

function questionTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP_FONT, size: 24, bold: true })],
    spacing: { before: 200, after: 80 }
  });
}

function indent(children, indentLeft = 480) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({
    children,
    indent: { left: indentLeft },
    spacing: { before: 40, after: 40 }
  });
}

function waka(line1, line2) {
  return [
    new Paragraph({
      children: [t(line1)],
      indent: { left: 720 },
      spacing: { before: 40, after: 0 }
    }),
    new Paragraph({
      children: [t(line2)],
      indent: { left: 720 },
      spacing: { before: 0, after: 60 }
    })
  ];
}

const border1 = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border1, bottom: border1, left: border1, right: border1 };

function boxedText(lines) {
  const rows = lines.map(line =>
    new TableRow({
      children: [new TableCell({
        borders,
        width: { size: 8000, type: WidthType.DXA },
        margins: { top: 80, bottom: 80, left: 160, right: 160 },
        children: [new Paragraph({ children: [t(line)], spacing: { before: 30, after: 30 } })]
      })]
    })
  );
  return new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: [8000],
    rows
  });
}

// ====== 歌のデータ ======
const poems = [
  {
    num: "七十四番",
    author: "源俊頼朝臣",
    yomi: "みなもとのとしよりあそん",
    line1: "うかりける　人を初瀬の　山おろしよ",
    line2: "はげしかれとは　祈らぬものを"
  },
  {
    num: "七十五番",
    author: "藤原基俊",
    yomi: "ふじわらのもととし",
    line1: "契りおきし　させもが露を　命にて",
    line2: "あはれ今年の　秋もいぬめり"
  },
  {
    num: "七十六番",
    author: "法性寺入道前関白太政大臣",
    yomi: "ほっしょうじにゅうどうさきのかんぱくだいじょうだいじん（藤原忠通）",
    line1: "わたの原　漕ぎ出でて見れば　ひさかたの",
    line2: "雲居にまがふ　沖つ白波"
  },
  {
    num: "七十七番",
    author: "崇徳院",
    yomi: "すとくいん",
    line1: "瀬をはやみ　岩にせかるる　滝川の",
    line2: "われても末に　あはむとぞ思ふ"
  },
  {
    num: "七十八番",
    author: "源兼昌",
    yomi: "みなもとのかねまさ",
    line1: "淡路島　かよふ千鳥の　鳴く声に",
    line2: "幾夜寝覚めぬ　須磨の関守"
  },
  {
    num: "七十九番",
    author: "左京大夫顕輔",
    yomi: "さきょうのだいぶあきすけ（藤原顕輔）",
    line1: "秋風に　たなびく雲の　絶え間より",
    line2: "もれ出づる月の　影のさやけさ"
  },
  {
    num: "八十番",
    author: "待賢門院堀河",
    yomi: "たいけんもんいんのほりかわ",
    line1: "長からむ　心も知らず　黒髪の",
    line2: "乱れてけさは　ものをこそ思へ"
  }
];

// ====== 解答欄表 ======
function answerTable(labels) {
  const cells = labels.map(lbl =>
    new TableCell({
      borders,
      width: { size: Math.floor(8000 / labels.length), type: WidthType.DXA },
      margins: { top: 60, bottom: 60, left: 80, right: 80 },
      children: [
        new Paragraph({ children: [t(lbl, { size: SMALL_SIZE })], alignment: AlignmentType.CENTER }),
        new Paragraph({ children: [t("　")], spacing: { before: 200, after: 0 } })
      ]
    })
  );
  return new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: Array(labels.length).fill(Math.floor(8000 / labels.length)),
    rows: [new TableRow({ children: cells })]
  });
}

// ====== 本文 ======
const children = [

  // タイトル
  new Paragraph({
    children: [new TextRun({ text: "百人一首　試験問題", font: JP_FONT, size: 32, bold: true })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 100 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "（出題範囲：七十四番～八十番）", font: JP_FONT, size: SMALL_SIZE })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 200 }
  }),

  // === 歌一覧 ===
  heading("【参考】出題範囲の短歌一覧"),
  ...poems.flatMap(p => [
    para([t(`${p.num}　${p.author}`, { bold: true })]),
    ...waka(p.line1, p.line2)
  ]),

  // 区切り
  new Paragraph({ children: [t("")], spacing: { before: 100, after: 100 } }),

  // === 大問一 ===
  heading("大問一　作者と短歌の対応"),
  questionTitle("問一　次の（ア）～（キ）の短歌を詠んだ作者を、下のA～Gからそれぞれ選び、記号で答えなさい。（各１点）"),

  para([t("（ア）", { bold: true })]),
  ...waka("うかりける　人を初瀬の　山おろしよ", "はげしかれとは　祈らぬものを"),
  para([t("（イ）", { bold: true })]),
  ...waka("契りおきし　させもが露を　命にて", "あはれ今年の　秋もいぬめり"),
  para([t("（ウ）", { bold: true })]),
  ...waka("わたの原　漕ぎ出でて見れば　ひさかたの", "雲居にまがふ　沖つ白波"),
  para([t("（エ）", { bold: true })]),
  ...waka("瀬をはやみ　岩にせかるる　滝川の", "われても末に　あはむとぞ思ふ"),
  para([t("（オ）", { bold: true })]),
  ...waka("淡路島　かよふ千鳥の　鳴く声に", "幾夜寝覚めぬ　須磨の関守"),
  para([t("（カ）", { bold: true })]),
  ...waka("秋風に　たなびく雲の　絶え間より", "もれ出づる月の　影のさやけさ"),
  para([t("（キ）", { bold: true })]),
  ...waka("長からむ　心も知らず　黒髪の", "乱れてけさは　ものをこそ思へ"),

  new Paragraph({ spacing: { before: 80, after: 40 }, children: [] }),
  indent("A　源俊頼朝臣　　B　藤原基俊　　C　法性寺入道前関白太政大臣"),
  indent("D　崇徳院　　　　E　源兼昌　　　F　左京大夫顕輔　　G　待賢門院堀河"),

  new Paragraph({ spacing: { before: 80, after: 40 }, children: [] }),
  para("【解答欄】"),
  answerTable(["（ア）", "（イ）", "（ウ）", "（エ）", "（オ）", "（カ）", "（キ）"]),

  new Paragraph({ spacing: { before: 200, after: 40 }, children: [] }),

  // === 大問二 ===
  heading("大問二　語句の意味"),
  questionTitle("問二　次の語句の意味として最も適切なものを、イ～ニからそれぞれ選びなさい。（各１点）"),

  para("１．七十四番「うかりける」の意味"),
  indent("イ　うれしそうな　　ロ　つれない・冷たい　　ハ　悲しそうな　　ニ　愛しい"),

  para("２．七十五番「いぬめり」の意味"),
  indent("イ　眠るようだ　　ロ　去らないようだ　　ハ　行ってしまうようだ　　ニ　来るようだ"),

  para("３．七十六番「まがふ」の意味"),
  indent("イ　混じりあう　　ロ　見間違えるほど似ている　　ハ　集まる　　ニ　消えていく"),

  para("４．七十七番「せかるる」の意味"),
  indent("イ　流れる　　ロ　落ちる　　ハ　せき止められる　　ニ　砕ける"),

  para("５．八十番「長からむ」の「む」の意味"),
  indent("イ　推量　　ロ　意志　　ハ　婉曲　　ニ　仮定"),

  new Paragraph({ spacing: { before: 80, after: 40 }, children: [] }),
  para("【解答欄】"),
  answerTable(["１", "２", "３", "４", "５"]),

  new Paragraph({ spacing: { before: 200, after: 40 }, children: [] }),

  // === 大問三 ===
  heading("大問三　文法事項"),
  questionTitle("問三　次の問いに答えなさい。（各２点）"),

  para("１．七十四番「祈らぬものを」の「ぬ」の文法的説明として正しいものを選びなさい。"),
  indent("イ　完了の助動詞「ぬ」の連体形"),
  indent("ロ　打消の助動詞「ず」の連体形"),
  indent("ハ　完了の助動詞「ぬ」の終止形"),
  indent("ニ　打消の助動詞「ず」の已然形"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("２．七十五番「させもが露を命にて」の「にて」の意味・用法を選びなさい。"),
  indent("イ　場所を示す　　ロ　手段・方法を示す　　ハ　原因・理由を示す　　ニ　状態を示す"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("３．七十七番「われても末にあはむとぞ思ふ」の係り結びを答えなさい。"),
  indent("係助詞：＿＿＿＿　　結びの活用形：＿＿＿＿形"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("４．八十番「ものをこそ思へ」の「こそ～思へ」について、「思へ」の活用形を答えなさい。"),
  indent("活用形：＿＿＿＿形"),

  new Paragraph({ spacing: { before: 200, after: 40 }, children: [] }),

  // === 大問四 ===
  heading("大問四　修辞技法"),
  questionTitle("問四　次の問いに答えなさい。（各２点）"),

  para("１．七十六番「ひさかたの」は枕詞である。何にかかるか答えなさい。"),
  indent("→　（　　　　　　　　　）にかかる"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("２．七十七番の歌に使われている修辞技法の名称を答え、その部分を抜き出しなさい。"),
  indent("修辞技法名：（　　　　　　　　　）"),
  indent("抜き出し：（　　　　　　　　　　　　　　　　　　）"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("３．七十九番「もれ出づる月の影のさやけさ」の「影」の意味を答えなさい。"),
  indent("イ　かげ（陰）　　ロ　光・輝き　　ハ　形・姿　　ニ　水面への映り込み"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("４．七十四番の歌で、「山おろし」に呼びかけている表現技法の名称を漢字で答えなさい。"),
  indent("技法名：（　　　　　　　　　）"),

  new Paragraph({ spacing: { before: 200, after: 40 }, children: [] }),

  // === 大問五 ===
  heading("大問五　現代語訳"),
  questionTitle("問五　次の短歌を現代語訳しなさい。（各３点）"),

  para("１．七十七番"),
  ...waka("瀬をはやみ　岩にせかるる　滝川の", "われても末に　あはむとぞ思ふ"),
  new Paragraph({ spacing: { before: 40, after: 0 }, children: [] }),
  para("現代語訳："),
  boxedText(["　", "　", "　"]),

  new Paragraph({ spacing: { before: 120, after: 0 }, children: [] }),
  para("２．八十番"),
  ...waka("長からむ　心も知らず　黒髪の", "乱れてけさは　ものをこそ思へ"),
  new Paragraph({ spacing: { before: 40, after: 0 }, children: [] }),
  para("現代語訳："),
  boxedText(["　", "　", "　"]),

  new Paragraph({ spacing: { before: 200, after: 40 }, children: [] }),

  // === 大問六 ===
  heading("大問六　内容理解・作者背景"),
  questionTitle("問六　次の問いに答えなさい。（各２点）"),

  para("１．七十四番の歌について、作者が「初瀬」（長谷寺）で祈ったのはどのような目的か、最も適切なものを選びなさい。"),
  indent("イ　武運長久を祈った"),
  indent("ロ　自分に冷たい相手の気持ちを変えようとした"),
  indent("ハ　雨が降らないように祈った"),
  indent("ニ　旅の安全を祈った"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("２．七十五番「させもが露」とは何を指すか、最も適切なものを選びなさい。"),
  indent("イ　よもぎ（させも草）の葉についた朝露そのもの"),
  indent("ロ　清水観音の言葉「なほたのめ」への信頼・約束"),
  indent("ハ　藤原忠通からもらった手紙の言葉"),
  indent("ニ　秋の霧のこと"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("３．七十七番の崇徳院について正しい説明を選びなさい。"),
  indent("イ　平安時代後期の天皇で、保元の乱に敗れ讃岐に流された"),
  indent("ロ　鎌倉幕府の将軍で、和歌を好んだ"),
  indent("ハ　奈良時代の貴族で、三十六歌仙の一人"),
  indent("ニ　平安時代の女流歌人で、源氏物語を書いた"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("４．七十八番の歌の舞台「須磨」について正しいものを選びなさい。"),
  indent("イ　現在の京都府にある地名"),
  indent("ロ　現在の兵庫県神戸市にある地名で、源氏物語にも登場する"),
  indent("ハ　現在の福岡県にある地名"),
  indent("ニ　淡路島にある地名"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("５．七十九番の歌の季節を答えなさい。また、その根拠となる語を歌の中から抜き出しなさい。"),
  indent("季節：（　　　）　　根拠となる語：（　　　　　　　）"),

  new Paragraph({ spacing: { before: 60, after: 0 }, children: [] }),
  para("６．八十番の作者「待賢門院堀河」はどのような立場の人物か、正しいものを選びなさい。"),
  indent("イ　貴族の女性で、天皇に仕えた女房歌人"),
  indent("ロ　武家の妻"),
  indent("ハ　尼僧"),
  indent("ニ　宮廷の男性歌人"),

  new Paragraph({ spacing: { before: 240, after: 100 }, children: [] }),

  // === 解答欄まとめ ===
  heading("【得点集計欄】"),
  new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: [1600, 1600, 1600, 1600, 1600],
    rows: [
      new TableRow({
        children: ["大問一（７点）", "大問二（５点）", "大問三（８点）", "大問四（８点）", "大問五（６点）"].map(label =>
          new TableCell({
            borders,
            width: { size: 1600, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({
              children: [new TextRun({ text: label, font: JP_FONT, size: SMALL_SIZE })],
              alignment: AlignmentType.CENTER
            })]
          })
        )
      }),
      new TableRow({
        children: Array(5).fill("").map(() =>
          new TableCell({
            borders,
            width: { size: 1600, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ children: [t("　")], spacing: { before: 200, after: 200 } })]
          })
        )
      })
    ]
  }),

  new Paragraph({ spacing: { before: 80, after: 0 }, children: [] }),
  new Table({
    width: { size: 4000, type: WidthType.DXA },
    columnWidths: [2000, 2000],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders,
            width: { size: 2000, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({
              children: [new TextRun({ text: "大問六（１２点）", font: JP_FONT, size: SMALL_SIZE })],
              alignment: AlignmentType.CENTER
            })]
          }),
          new TableCell({
            borders,
            width: { size: 2000, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({
              children: [new TextRun({ text: "合計（４６点）", font: JP_FONT, size: SMALL_SIZE, bold: true })],
              alignment: AlignmentType.CENTER
            })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            borders,
            width: { size: 2000, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ children: [t("　")], spacing: { before: 200, after: 200 } })]
          }),
          new TableCell({
            borders,
            width: { size: 2000, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ children: [t("　")], spacing: { before: 200, after: 200 } })]
          })
        ]
      })
    ]
  }),
];

// ====== ドキュメント生成 ======
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [
            new TextRun({ text: "百人一首試験　七十四番～八十番", font: JP_FONT, size: SMALL_SIZE }),
          ],
          alignment: AlignmentType.RIGHT
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("hyakunin_exam.docx", buffer);
  console.log("Done: hyakunin_exam.docx");
});
