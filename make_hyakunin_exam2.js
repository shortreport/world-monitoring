const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageNumber, Header, Footer, HeadingLevel
} = require('docx');
const fs = require('fs');

const JP_FONT = "MS Mincho";
const BODY_SIZE = 22;
const SMALL_SIZE = 20;

function t(text, opts = {}) {
  return new TextRun({ text, font: JP_FONT, size: BODY_SIZE, ...opts });
}
function para(children, opts = {}) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({ children, spacing: { before: 60, after: 60 }, ...opts });
}
function heading(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP_FONT, size: 24, bold: true })],
    spacing: { before: 200, after: 100 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000" } }
  });
}
function qTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: JP_FONT, size: BODY_SIZE, bold: true })],
    spacing: { before: 160, after: 80 }
  });
}
function indent(children, left = 480) {
  if (typeof children === 'string') children = [t(children)];
  return new Paragraph({ children, indent: { left }, spacing: { before: 40, after: 40 } });
}
function waka(line1, line2) {
  return [
    new Paragraph({ children: [t(line1)], indent: { left: 720 }, spacing: { before: 40, after: 0 } }),
    new Paragraph({ children: [t(line2)], indent: { left: 720 }, spacing: { before: 0, after: 60 } })
  ];
}
function sp(before = 100) {
  return new Paragraph({ children: [t("")], spacing: { before, after: 0 } });
}

const border1 = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border1, bottom: border1, left: border1, right: border1 };

function answerTable(labels) {
  const w = Math.floor(8000 / labels.length);
  return new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: Array(labels.length).fill(w),
    rows: [
      new TableRow({
        children: labels.map(lbl =>
          new TableCell({
            borders,
            width: { size: w, type: WidthType.DXA },
            margins: { top: 60, bottom: 60, left: 80, right: 80 },
            children: [
              new Paragraph({ children: [new TextRun({ text: lbl, font: JP_FONT, size: SMALL_SIZE })], alignment: AlignmentType.CENTER }),
              new Paragraph({ children: [t("　")], spacing: { before: 200, after: 0 } })
            ]
          })
        )
      })
    ]
  });
}

function writeBox(rows = 3) {
  return new Table({
    width: { size: 8000, type: WidthType.DXA },
    columnWidths: [8000],
    rows: Array(rows).fill(null).map(() =>
      new TableRow({
        children: [new TableCell({
          borders,
          width: { size: 8000, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 160, right: 160 },
          children: [new Paragraph({ children: [t("　")], spacing: { before: 60, after: 60 } })]
        })]
      })
    )
  });
}

// ==================== 本文 ====================
const children = [

  // タイトル
  new Paragraph({
    children: [new TextRun({ text: "百人一首　試験問題（第二回）", font: JP_FONT, size: 32, bold: true })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 80 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "（出題範囲：七十四番～八十番）", font: JP_FONT, size: SMALL_SIZE })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 200 }
  }),

  // ======= 大問一：穴埋め =======
  heading("大問一　短歌の穴埋め"),
  qTitle("問一　次の短歌の（　）に入る語句を答えなさい。（各１点）"),

  para("１．七十四番　源俊頼朝臣"),
  ...waka("うかりける　人を（　　　）の　山おろしよ", "はげしかれとは　祈らぬものを"),
  para("　　答え：（　　　　　　　）"),

  para("２．七十五番　藤原基俊"),
  ...waka("契りおきし　させもが（　　）を　命にて", "あはれ今年の　秋もいぬめり"),
  para("　　答え：（　　　　　　　）"),

  para("３．七十六番　法性寺入道前関白太政大臣"),
  ...waka("わたの原　漕ぎ出でて見れば　ひさかたの", "雲居に（　　　）　沖つ白波"),
  para("　　答え：（　　　　　　　）"),

  para("４．七十七番　崇徳院"),
  ...waka("瀬をはやみ　岩にせかるる　（　　　）の", "われても末に　あはむとぞ思ふ"),
  para("　　答え：（　　　　　　　）"),

  para("５．七十九番　左京大夫顕輔"),
  ...waka("秋風に　たなびく雲の（　　　）より", "もれ出づる月の　影のさやけさ"),
  para("　　答え：（　　　　　　　）"),

  sp(200),

  // ======= 大問二：語句の意味 =======
  heading("大問二　語句の意味"),
  qTitle("問二　次の語句の意味として最も適切なものを、イ～ニから選びなさい。（各１点）"),

  para("１．七十四番「はげしかれとは祈らぬものを」の「ものを」の意味・用法"),
  indent("イ　〜なのに（逆接の詠嘆）　　ロ　〜だから　　ハ　〜のようだ　　ニ　〜しよう"),

  para("２．七十五番「契りおきし」の「おきし」（おく）の意味"),
  indent("イ　置いておく　　ロ　〜しておく（補助動詞）　　ハ　起きる　　ニ　決める"),

  para("３．七十八番「幾夜寝覚めぬ」の「ぬ」の文法的説明"),
  indent("イ　打消の助動詞「ず」の連体形　　ロ　完了の助動詞「ぬ」の終止形"),
  indent("ハ　打消の助動詞「ず」の終止形　　ニ　完了の助動詞「ぬ」の連体形"),

  para("４．七十九番「さやけさ」の意味"),
  indent("イ　寂しさ　　ロ　清らかさ・澄んだ明るさ　　ハ　激しさ　　ニ　遠さ"),

  para("５．八十番「乱れてけさは」の「けさ」が指す時間帯"),
  indent("イ　昨晩　　ロ　今朝　　ハ　今夜　　ニ　昼"),

  sp(80),
  para("【解答欄】"),
  answerTable(["１", "２", "３", "４", "５"]),

  sp(200),

  // ======= 大問三：修辞技法 =======
  heading("大問三　修辞技法"),
  qTitle("問三　次の問いに答えなさい。（各２点）"),

  para("１．七十六番「ひさかたの　雲居にまがふ　沖つ白波」について答えなさい。"),
  indent("（１）「ひさかたの」は枕詞である。何にかかっているか。"),
  indent("　　→（　　　　）にかかる", 720),
  indent("（２）「雲居」とはどういう意味か。"),
  indent("　　イ　海　　ロ　空・雲のある所　　ハ　霞　　ニ　波", 720),

  sp(60),
  para("２．七十七番「瀬をはやみ　岩にせかるる　滝川の」は序詞である。"),
  indent("（１）序詞とはどのような修辞技法か、簡潔に説明しなさい。"),
  writeBox(2),
  indent("（２）この序詞が導く語（本来言いたい語）を歌の中から抜き出しなさい。"),
  indent("　　→（　　　　　　　　　）", 720),

  sp(60),
  para("３．次のうち、七十五番の歌に関係する人物・作品はどれか。"),
  indent("イ　清少納言『枕草子』の「なほたのめしめじが原のさせも草」という観音の言葉"),
  indent("ロ　紫式部『源氏物語』の須磨の場面"),
  indent("ハ　在原業平『伊勢物語』の東下り"),
  indent("ニ　松尾芭蕉『奥の細道』の序文"),

  sp(200),

  // ======= 大問四：文法 =======
  heading("大問四　文法事項"),
  qTitle("問四　次の問いに答えなさい。（各２点）"),

  para("１．七十四番「うかりける人を初瀬の山おろしよ」の「よ」の品詞と用法を答えなさい。"),
  indent("イ　終助詞（詠嘆・呼びかけ）　　ロ　格助詞（〜から）"),
  indent("ハ　接続助詞（〜ので）　　　　　ニ　副助詞（〜ほど）"),

  sp(60),
  para("２．七十五番「いぬめり」を語に分解し、それぞれの品詞名を答えなさい。"),
  indent("いぬ＝（　　　　　　　　　　）　　めり＝（　　　　　　　　）"),

  sp(60),
  para("３．七十七番「あはむとぞ思ふ」について、「ぞ〜思ふ」の係り結びを説明しなさい。"),
  indent("係助詞「ぞ」→ 結びの語「思ふ」の活用形（　　　　　　　）形"),

  sp(60),
  para("４．八十番「長からむ心も知らず黒髪の」の「黒髪の」の「の」の用法を答えなさい。"),
  indent("イ　主格（〜が）　　ロ　連体修飾（〜の）　　ハ　同格（〜で）　　ニ　比喩（〜のような）"),

  sp(200),

  // ======= 大問五：現代語訳 =======
  heading("大問五　現代語訳"),
  qTitle("問五　次の短歌を現代語訳しなさい。（各３点）"),

  para("１．七十四番"),
  ...waka("うかりける　人を初瀬の　山おろしよ", "はげしかれとは　祈らぬものを"),
  sp(40),
  para("現代語訳："),
  writeBox(3),

  sp(120),
  para("２．七十九番"),
  ...waka("秋風に　たなびく雲の　絶え間より", "もれ出づる月の　影のさやけさ"),
  sp(40),
  para("現代語訳："),
  writeBox(3),

  sp(200),

  // ======= 大問六：内容理解 =======
  heading("大問六　内容理解・鑑賞"),
  qTitle("問六　次の問いに答えなさい。（各２点）"),

  para("１．七十四番の作者・源俊頼朝臣について正しいものを選びなさい。"),
  indent("イ　平安時代後期の歌人で、金葉和歌集の撰者"),
  indent("ロ　鎌倉時代の武将で、和歌を嗜んだ"),
  indent("ハ　奈良時代の女流歌人"),
  indent("ニ　室町時代の連歌師"),

  sp(60),
  para("２．七十八番「淡路島　かよふ千鳥」の「かよふ」が表す情景として正しいものを選びなさい。"),
  indent("イ　千鳥が淡路島と須磨の間を行き来している"),
  indent("ロ　千鳥が一方向に飛んでいく"),
  indent("ハ　千鳥が空高く舞い上がっている"),
  indent("ニ　千鳥が海面に浮かんでいる"),

  sp(60),
  para("３．七十七番の崇徳院が詠んだ「われても末にあはむとぞ思ふ」のテーマとして最も適切なものを選びなさい。"),
  indent("イ　川の流れの美しさへの感動"),
  indent("ロ　今は離れていても、いつか再会を果たそうという強い想い"),
  indent("ハ　岩にぶつかる川の荒々しさへの恐怖"),
  indent("ニ　別れた恋人への恨み"),

  sp(60),
  para("４．八十番「長からむ心も知らず」の「長からむ」が修飾する名詞は何か、歌の中から抜き出しなさい。"),
  indent("→（　　　　　　）"),

  sp(60),
  para("５．七十六番の作者・法性寺入道前関白太政大臣の俗名を答えなさい。"),
  indent("イ　藤原道長　　ロ　藤原忠通　　ハ　藤原定家　　ニ　藤原頼長"),

  sp(60),
  para("６．七十九番の歌が詠む景色として最もふさわしいものを選びなさい。"),
  indent("イ　嵐のあとに晴れ渡る朝の空"),
  indent("ロ　秋風に流れる雲の合間から差し込む澄んだ月光"),
  indent("ハ　夕暮れに染まる海の水平線"),
  indent("ニ　春霞の中にぼんやり見える山の稜線"),

  sp(240),

  // ======= 得点集計欄 =======
  heading("【得点集計欄】"),
  new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [1500, 1500, 1500, 1500, 1500, 1500],
    rows: [
      new TableRow({
        children: ["大問一（５点）","大問二（５点）","大問三（８点）","大問四（８点）","大問五（６点）","大問六（１２点）"].map(label =>
          new TableCell({
            borders,
            width: { size: 1500, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 80, right: 80 },
            children: [new Paragraph({
              children: [new TextRun({ text: label, font: JP_FONT, size: SMALL_SIZE })],
              alignment: AlignmentType.CENTER
            })]
          })
        )
      }),
      new TableRow({
        children: Array(5).fill("").concat(["合計（４４点）"]).map((label, i) =>
          new TableCell({
            borders,
            width: { size: 1500, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 80, right: 80 },
            children: [new Paragraph({
              children: i === 5
                ? [new TextRun({ text: label, font: JP_FONT, size: SMALL_SIZE, bold: true })]
                : [t("　")],
              spacing: { before: 200, after: 200 },
              alignment: AlignmentType.CENTER
            })]
          })
        )
      })
    ]
  }),
];

// ======= ドキュメント生成 =======
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
          children: [new TextRun({ text: "百人一首試験（第二回）　七十四番～八十番", font: JP_FONT, size: SMALL_SIZE })],
          alignment: AlignmentType.RIGHT
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("hyakunin_exam2.docx", buffer);
  console.log("Done: hyakunin_exam2.docx");
});
