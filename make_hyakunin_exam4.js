const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, Header, PageBreak
} = require('docx');
const fs = require('fs');

const JP = "MS Mincho";
const B = 22, S = 20, L = 26;

const t  = (text, o={}) => new TextRun({ text, font:JP, size:B, ...o });
const tS = (text, o={}) => new TextRun({ text, font:JP, size:S, ...o });
const tR = (text)       => new TextRun({ text, font:JP, size:B, color:"CC0000", bold:true });

const p = (ch, o={}) => {
  if (typeof ch === 'string') ch = [t(ch)];
  return new Paragraph({ children:ch, spacing:{ before:60, after:60 }, ...o });
};
const pIn = (ch, left=480) => {
  if (typeof ch === 'string') ch = [t(ch)];
  return new Paragraph({ children:ch, indent:{ left }, spacing:{ before:40, after:40 } });
};
const pAns = (ch) => {
  if (typeof ch === 'string') ch = [tR(ch)];
  return new Paragraph({ children:ch, indent:{ left:480 }, spacing:{ before:40, after:40 } });
};
const h = (text, color="000000") => new Paragraph({
  children: [new TextRun({ text, font:JP, size:24, bold:true, color })],
  spacing:{ before:220, after:100 },
  border:{ bottom:{ style:BorderStyle.SINGLE, size:6, color } }
});
const qt = (text) => new Paragraph({
  children:[new TextRun({ text, font:JP, size:B, bold:true })],
  spacing:{ before:160, after:80 }
});
const waka = (l1,l2) => [
  new Paragraph({ children:[t(l1)], indent:{ left:720 }, spacing:{ before:40, after:0 } }),
  new Paragraph({ children:[t(l2)], indent:{ left:720 }, spacing:{ before:0, after:60 } }),
];
const sp = (before=100) => new Paragraph({ children:[], spacing:{ before, after:0 } });

const bdr  = { style:BorderStyle.SINGLE, size:4, color:"000000" };
const bdrs = { top:bdr, bottom:bdr, left:bdr, right:bdr };
const noBdr = { style:BorderStyle.NONE, size:0, color:"FFFFFF" };
const noBdrs = { top:noBdr, bottom:noBdr, left:noBdr, right:noBdr };

const cell = (text, w, {bold=false, center=false, shade=false, red=false, size=S}={}) =>
  new TableCell({
    borders: bdrs,
    width:{ size:w, type:WidthType.DXA },
    margins:{ top:80, bottom:80, left:120, right:120 },
    shading: shade ? { fill:"EEEEEE", type:"clear" } : undefined,
    children:[new Paragraph({
      children:[new TextRun({ text, font:JP, size, bold, color: red?"CC0000":"000000" })],
      alignment: center ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing:{ before:20, after:20 }
    })]
  });

const writeBox = (rows=3) => new Table({
  width:{ size:8000, type:WidthType.DXA }, columnWidths:[8000],
  rows: Array(rows).fill(null).map(()=>new TableRow({ children:[new TableCell({
    borders:bdrs, width:{ size:8000, type:WidthType.DXA },
    margins:{ top:60, bottom:60, left:120, right:120 },
    children:[new Paragraph({ children:[t("　")], spacing:{ before:60, after:60 } })]
  })] }))
});

const ansRow = (labels) => {
  const w = Math.floor(8000/labels.length);
  return new Table({
    width:{ size:8000, type:WidthType.DXA },
    columnWidths: Array(labels.length).fill(w),
    rows:[new TableRow({ children: labels.map(lbl => new TableCell({
      borders:bdrs, width:{ size:w, type:WidthType.DXA },
      margins:{ top:60, bottom:60, left:60, right:60 },
      children:[
        new Paragraph({ children:[tS(lbl)], alignment:AlignmentType.CENTER }),
        new Paragraph({ children:[t("　")], spacing:{ before:180, after:0 } })
      ]
    })) })]
  });
};

// ========= 全首データ =========
const PMS = [
  { no:"74", num:"七十四番", au:"源俊頼朝臣",              l1:"うかりける　人を初瀬の　山おろしよ",    l2:"はげしかれとは　祈らぬものを",    season:"（なし・恋）" },
  { no:"75", num:"七十五番", au:"藤原基俊",                l1:"契りおきし　させもが露を　命にて",      l2:"あはれ今年の　秋もいぬめり",      season:"秋" },
  { no:"76", num:"七十六番", au:"法性寺入道前関白太政大臣", l1:"わたの原　漕ぎ出でて見れば　ひさかたの",l2:"雲居にまがふ　沖つ白波",          season:"（なし・海景）" },
  { no:"77", num:"七十七番", au:"崇徳院",                  l1:"瀬をはやみ　岩にせかるる　滝川の",     l2:"われても末に　あはむとぞ思ふ",    season:"（なし・恋）" },
  { no:"78", num:"七十八番", au:"源兼昌",                  l1:"淡路島　かよふ千鳥の　鳴く声に",       l2:"幾夜寝覚めぬ　須磨の関守",        season:"冬" },
  { no:"79", num:"七十九番", au:"左京大夫顕輔",            l1:"秋風に　たなびく雲の　絶え間より",     l2:"もれ出づる月の　影のさやけさ",    season:"秋" },
  { no:"80", num:"八十番",   au:"待賢門院堀河",            l1:"長からむ　心も知らず　黒髪の",         l2:"乱れてけさは　ものをこそ思へ",    season:"（なし・恋）" },
  { no:"81", num:"八十一番", au:"後徳大寺左大臣",          l1:"ほととぎす　鳴きつる方を　ながむれば", l2:"ただ有明の　月ぞ残れる",          season:"夏" },
  { no:"82", num:"八十二番", au:"道因法師",                l1:"思ひわびさても　命は　あるものを",     l2:"憂きにたへぬは　涙なりけり",      season:"（なし・恋）" },
];

// ======================================================================
//  問題部分
// ======================================================================
const MONDAI = [

  new Paragraph({
    children:[new TextRun({ text:"百人一首　試験問題（第四回）", font:JP, size:32, bold:true })],
    alignment:AlignmentType.CENTER, spacing:{ before:0, after:80 }
  }),
  new Paragraph({
    children:[tS("（出題範囲：七十四番〜八十二番）")],
    alignment:AlignmentType.CENTER, spacing:{ before:0, after:200 }
  }),

  // 歌一覧
  h("【参考】出題範囲の短歌一覧"),
  ...PMS.flatMap(pm=>[
    p([t(`${pm.num}　${pm.au}`, { bold:true })]),
    ...waka(pm.l1, pm.l2)
  ]),
  sp(200),

  // ===== 大問一：穴埋め =====
  h("大問一　穴埋め問題"),
  qt("問一　次の短歌の（　　）に当てはまる語句を答えなさい。（各１点）"),

  p([t("１．七十四番")]),
  ...waka("うかりける　人を（　　　）の　山おろしよ","はげしかれとは　祈らぬものを"),
  p("　　→（　　　　　　　）"),

  p([t("２．七十五番")]),
  ...waka("契りおきし　させもが（　　）を　命にて","あはれ今年の　秋もいぬめり"),
  p("　　→（　　　　　　　）"),

  p([t("３．七十七番")]),
  ...waka("瀬をはやみ　岩にせかるる　滝川の","われても（　　）に　あはむとぞ思ふ"),
  p("　　→（　　　　　　　）"),

  p([t("４．七十九番")]),
  ...waka("秋風に　たなびく雲の　絶え間より","もれ出づる月の　（　　）のさやけさ"),
  p("　　→（　　　　　　　）"),

  p([t("５．八十一番")]),
  ...waka("ほととぎす　鳴きつる方を　ながむれば","ただ（　　　　）の　月ぞ残れる"),
  p("　　→（　　　　　　　）"),

  p([t("６．八十二番")]),
  ...waka("思ひわびさても　命は　あるものを","憂きにたへぬは　（　　）なりけり"),
  p("　　→（　　　　　　　）"),
  sp(200),

  // ===== 大問二：語句の意味 =====
  h("大問二　語句の意味"),
  qt("問二　次の語句の意味として最も適切なものをイ〜ニから選びなさい。（各１点）"),

  p("１．七十四番「うかりける」"),
  pIn("イ　うれしそうな　　ロ　つれない・冷たい　　ハ　悲しそうな　　ニ　愛しい"),
  p("２．七十五番「いぬめり」"),
  pIn("イ　眠るようだ　　ロ　来るようだ　　ハ　行ってしまうようだ　　ニ　消えていくようだ"),
  p("３．七十六番「まがふ」"),
  pIn("イ　漂う　　ロ　見間違えるほど似ている　　ハ　混ざる　　ニ　消える"),
  p("４．七十八番「かよふ」"),
  pIn("イ　飛んでいる　　ロ　集まる　　ハ　行き来している　　ニ　鳴いている"),
  p("５．八十一番「ながむれば」"),
  pIn("イ　歌を詠むと　　ロ　泣くと　　ハ　思うと　　ニ　眺めると・見渡すと"),
  p("６．八十一番「有明の月」"),
  pIn("イ　夕暮れの赤い月　　ロ　真夜中の満月　　ハ　夜明けごろ残る月　　ニ　冬の冷たい月"),
  p("７．八十二番「憂き」"),
  pIn("イ　嬉しい　　ロ　美しい　　ハ　激しい　　ニ　つらい・憂鬱な"),
  p("８．八十番「ものをこそ思へ」の「こそ」"),
  pIn("イ　格助詞（〜を）　　ロ　係助詞（強調）　　ハ　副助詞（〜ほど）　　ニ　接続助詞"),
  sp(80),
  p("【解答欄】"),
  ansRow(["１","２","３","４","５","６","７","８"]),
  sp(200),

  // ===== 大問三：文法 =====
  h("大問三　文法事項"),
  qt("問三　次の問いに答えなさい。（各２点）"),

  p("１．七十四番「祈らぬものを」の「ぬ」の品詞・意味として正しいものを選びなさい。"),
  pIn("イ　完了の助動詞「ぬ」の連体形"),
  pIn("ロ　打消の助動詞「ず」の連体形"),
  pIn("ハ　完了の助動詞「ぬ」の終止形"),
  pIn("ニ　打消の助動詞「ず」の已然形"),
  sp(60),
  p("２．七十五番「あはれ今年の秋もいぬめり」の「めり」の品詞と意味を答えなさい。"),
  pIn("品詞：（　　　　　　　　　　）　　　意味：（　　　　　　　　　　　　）"),
  sp(60),
  p("３．七十七番「われても末にあはむとぞ思ふ」について答えなさい。"),
  pIn("（１）「ぞ」は係助詞である。結びの語「思ふ」の活用形を答えなさい。　→（　　　　　）形"),
  pIn("（２）「あはむ」の「む」の意味を選びなさい。"),
  pIn("　　　イ　推量　　ロ　意志　　ハ　婉曲　　ニ　勧誘", 720),
  sp(60),
  p("４．八十一番「月ぞ残れる」の「る」（助動詞「り」の連体形）の意味として正しいものを選びなさい。"),
  pIn("イ　受身（〜される）　　ロ　存続（〜ている）　　ハ　完了（〜してしまった）　　ニ　可能（〜できる）"),
  sp(60),
  p("５．八十番「ものをこそ思へ」の「思へ」の活用形を答えなさい。"),
  pIn("→（　　　　　　　）形"),
  sp(60),
  p("６．八十二番「涙なりけり」の「けり」の意味・用法を選びなさい。"),
  pIn("イ　過去（〜た）　　ロ　詠嘆（〜だなあ）　　ハ　伝聞（〜ということだ）　　ニ　推量（〜だろう）"),
  sp(200),

  // ===== 大問四：修辞技法 =====
  h("大問四　修辞技法"),
  qt("問四　次の問いに答えなさい。（各２点）"),

  p("１．七十六番「ひさかたの　雲居にまがふ　沖つ白波」の「ひさかたの」は枕詞である。何にかかるか。"),
  pIn("→（　　　　　　）にかかる"),
  sp(60),
  p("２．七十七番「瀬をはやみ　岩にせかるる　滝川の」は序詞である。"),
  pIn("（１）「序詞」とはどのような修辞技法か、１行で説明しなさい。"),
  writeBox(2),
  pIn("（２）この序詞が直接導く語を歌の中から抜き出しなさい。　→（　　　　　　）"),
  sp(60),
  p("３．七十四番「山おろしよ」で、山風を人に見立てて呼びかけている技法の名称を答えなさい。"),
  pIn("→（　　　　　　　　　）法"),
  sp(60),
  p("４．八十番「長からむ心も知らず黒髪の」の「黒髪の」の「の」の用法を選びなさい。"),
  pIn("イ　主格（〜が）　　ロ　連体修飾（〜の）　　ハ　同格（〜で）　　ニ　比喩（〜のような）"),
  sp(200),

  // ===== 大問五：現代語訳 =====
  h("大問五　現代語訳"),
  qt("問五　次の短歌を現代語訳しなさい。（各３点）"),

  p("１．七十五番"),
  ...waka("契りおきし　させもが露を　命にて","あはれ今年の　秋もいぬめり"),
  sp(40), p("現代語訳："), writeBox(3),
  sp(120),
  p("２．八十二番"),
  ...waka("思ひわびさても　命は　あるものを","憂きにたへぬは　涙なりけり"),
  sp(40), p("現代語訳："), writeBox(3),
  sp(200),

  // ===== 大問六：内容理解 =====
  h("大問六　内容理解・作者背景"),
  qt("問六　次の問いに答えなさい。（各２点）"),

  p("１．次の説明に当てはまる歌の番号を書きなさい。"),
  pIn("（１）川の流れが二手に分かれても合流するように、離れても再会を誓う恋の歌。　→（　　）番"),
  pIn("（２）ほととぎすが鳴いた方を見ると、姿はなく有明の月だけが残っていた夏の歌。　→（　　）番"),
  pIn("（３）大海原に漕ぎ出すと、空の雲と見間違えるほどの沖の白波が広がる歌。　→（　　）番"),
  pIn("（４）黒髪の乱れたまま、男の真意もわからず思い悩む女心を詠んだ歌。　→（　　）番"),
  sp(60),
  p("２．次のうち「恋」を主題とする歌の番号をすべて選びなさい。"),
  pIn("74　75　76　77　78　79　80　81　82"),
  p("　　→（　　　　　　　　　　　　　　）番"),
  sp(60),
  p("３．崇徳院（七十七番）について正しいものを選びなさい。"),
  pIn("イ　平安時代後期の天皇で、保元の乱に敗れ讃岐に流された"),
  pIn("ロ　鎌倉幕府を開いた武将で和歌を好んだ"),
  pIn("ハ　奈良時代の貴族で三十六歌仙の一人"),
  pIn("ニ　平安時代の女流歌人"),
  sp(60),
  p("４．百人一首を撰んだ人物は誰か。"),
  pIn("イ　紀貫之　　ロ　藤原定家　　ハ　藤原道長　　ニ　在原業平"),
  sp(60),
  p("５．「ほととぎす」（八十一番）が詠まれる季節と、その理由を簡潔に書きなさい。"),
  pIn("季節：（　　　）　　理由："),
  writeBox(2),
  sp(240),

  // 得点欄
  h("【得点集計欄】"),
  new Table({
    width:{ size:9000, type:WidthType.DXA },
    columnWidths:[1285,1286,1286,1286,1286,1286,1285],
    rows:[
      new TableRow({ children:
        ["大問一（６点）","大問二（８点）","大問三（１２点）","大問四（８点）","大問五（６点）","大問六（１０点）","合計（５０点）"]
        .map((label,i)=>new TableCell({
          borders:bdrs, width:{ size:1285, type:WidthType.DXA },
          margins:{ top:80, bottom:80, left:80, right:80 },
          children:[new Paragraph({ children:[tS(label,{ bold:i===6 })], alignment:AlignmentType.CENTER })]
        }))
      }),
      new TableRow({ children:
        Array(7).fill("　")
        .map((_,i)=>new TableCell({
          borders:bdrs, width:{ size:1285, type:WidthType.DXA },
          margins:{ top:80, bottom:80, left:80, right:80 },
          children:[new Paragraph({ children:[t("　")], spacing:{ before:200, after:200 } })]
        }))
      })
    ]
  }),
];

// ======================================================================
//  解答部分（改ページ後）
// ======================================================================
const KAITOU = [

  new Paragraph({ children:[new PageBreak()] }),

  new Paragraph({
    children:[new TextRun({ text:"百人一首　試験問題（第四回）　【解答・解説】", font:JP, size:32, bold:true, color:"CC0000" })],
    alignment:AlignmentType.CENTER, spacing:{ before:0, after:80 }
  }),
  new Paragraph({
    children:[tS("（出題範囲：七十四番〜八十二番）")],
    alignment:AlignmentType.CENTER, spacing:{ before:0, after:200 }
  }),

  // ===== 大問一 解答 =====
  h("大問一　解答　（各１点　計６点）","CC0000"),
  new Table({
    width:{ size:8000, type:WidthType.DXA },
    columnWidths:[800,2000,2200,3000],
    rows:[
      new TableRow({ children:[cell("問",800,{bold:true,shade:true,center:true}), cell("空欄の位置",2000,{bold:true,shade:true}), cell("正答",2200,{bold:true,shade:true,red:true}), cell("補足",3000,{bold:true,shade:true})] }),
      ...[ ["１","「人を（　）の山おろしよ」","初瀬","初瀬＝大和国（奈良県）の長谷寺。恋を祈った場所。"],
           ["２","「させもが（　）を命にて」","露","させも草（よもぎ）の露。清水観音の言葉への信頼の象徴。"],
           ["３","「われても（　）にあはむとぞ」","末","末＝下流・末来のこと。いつかまた逢う日を指す。"],
           ["４","「もれ出づる月の（　）のさやけさ」","影","影＝光・輝きの意。現代語の「影」（陰）とは異なる。"],
           ["５","「ただ（　　）の月ぞ残れる」","有明","有明の月＝夜明けごろ空に残る月。"],
           ["６","「憂きにたへぬは（　）なりけり」","涙","耐えられないのは涙だ、という詠嘆の結句。"],
      ].map(([no,pos,ans,note])=>new TableRow({ children:[cell(no,800,{center:true}),cell(pos,2000),cell(ans,2200,{red:true,bold:true}),cell(note,3000)] }))
    ]
  }),
  sp(200),

  // ===== 大問二 解答 =====
  h("大問二　解答　（各１点　計８点）","CC0000"),
  new Table({
    width:{ size:8000, type:WidthType.DXA },
    columnWidths:[500,2500,1200,3800],
    rows:[
      new TableRow({ children:[cell("問",500,{bold:true,shade:true,center:true}),cell("語句",2500,{bold:true,shade:true}),cell("正答",1200,{bold:true,shade:true,center:true}),cell("解説",3800,{bold:true,shade:true})] }),
      ...[["１","うかりける","ロ","「うかり」は形容詞「うし（憂し）」の連用形＋過去の助動詞「けり」。つれない・冷たいの意。"],
          ["２","いぬめり","ハ","「いぬ」はナ行変格活用「往ぬ」。行ってしまうの意。「めり」は推量の助動詞。"],
          ["３","まがふ","ロ","見間違えるほど似ているの意。白波が空の雲と紛らわしいほど似ていることを言う。"],
          ["４","かよふ","ハ","「通ふ」＝行き来する。千鳥が淡路島と須磨の間を往来している情景。"],
          ["５","ながむれば","ニ","「ながむ」は「眺む」＝じっと見る・見渡す。「詠む（歌を詠む）」と混同注意。"],
          ["６","有明の月","ハ","夜明けごろ、まだ空に白く残っている月。夏の夜明けの余情を表す語。"],
          ["７","憂き","ニ","形容詞「憂し（うし）」の連体形。つらい・苦しいの意。"],
          ["８","こそ","ロ","係助詞で強調を表す。文末を已然形（思へ）に結ぶ「こそ〜已然形」の係り結び。"],
      ].map(([no,go,ans,ex])=>new TableRow({ children:[cell(no,500,{center:true}),cell(go,2500),cell(ans,1200,{red:true,bold:true,center:true}),cell(ex,3800)] }))
    ]
  }),
  sp(200),

  // ===== 大問三 解答 =====
  h("大問三　解答　（各２点　計１２点）","CC0000"),

  qt("１．「祈らぬものを」の「ぬ」"),
  pAns("ロ　打消の助動詞「ず」の連体形"),
  pIn([t("【解説】"), t("「祈ら（未然形）」に続く「ぬ」は打消の助動詞「ず」の連体形。「ものを」の前に来るので連体形が必要。完了の「ぬ」は連用形接続・終止形が「ぬ」。")]),

  sp(80),
  qt("２．「めり」の品詞と意味"),
  pAns("品詞：推量の助動詞　　　意味：〜ようだ・〜と見える（視覚による推量）"),
  pIn([t("【解説】"), t("「めり」は目に見える様子から推量する助動詞。「行ってしまうように見える」という意味合い。")]),

  sp(80),
  qt("３．「われても末にあはむとぞ思ふ」"),
  pAns("（１）活用形：連体形　　（２）「む」の意味：ロ　意志"),
  pIn([t("【解説】"), t("「ぞ」は係助詞で文末を連体形に結ぶ。「あはむ」の「む」は一人称主語（自分）の意志を表す。「逢おう」と誓う気持ち。")]),

  sp(80),
  qt("４．「月ぞ残れる」の「る」（助動詞「り」の連体形）"),
  pAns("ロ　存続（〜ている）"),
  pIn([t("【解説】"), t("「残れる」は「月がまだ残っている」という状態の継続を表す。「ぞ〜連体形」の係り結び。")]),

  sp(80),
  qt("５．「ものをこそ思へ」の「思へ」の活用形"),
  pAns("已然形"),
  pIn([t("【解説】"), t("係助詞「こそ」は文末を已然形に結ぶ。「思ふ」（ハ行四段）の已然形は「思へ」。")]),

  sp(80),
  qt("６．「涙なりけり」の「けり」の意味・用法"),
  pAns("ロ　詠嘆（〜だなあ・〜であることよ）"),
  pIn([t("【解説】"), t("和歌の末尾に置かれた「けり」は詠嘆の用法が多い。「涙なのだなあ」と感慨を込めて述べている。")]),
  sp(200),

  // ===== 大問四 解答 =====
  h("大問四　解答　（各２点　計８点）","CC0000"),

  qt("１．「ひさかたの」がかかる語"),
  pAns("雲居（または「空・天」「雲」も可）"),
  pIn([t("【解説】"), t("「ひさかたの」は天・空・月・雲・光などにかかる枕詞。七十六番では「雲居（雲のある空）」にかかる。")]),

  sp(80),
  qt("２．序詞について"),
  p([t("（１）序詞の説明（模範例）")]),
  pAns("特定の語句を導くために、その前に置かれる長めの比喩・情景描写の言葉。枕詞より長く、独自に作られる。"),
  p([t("（２）序詞が導く語")]),
  pAns("われても（「我が身が離れても」の「われ」にかかる）"),
  pIn([t("【解説】"), t("「瀬をはやみ〜滝川の」が序詞で、川が二手に分かれる情景を「われても（離れても）」という人間の恋情に重ねる。")]),

  sp(80),
  qt("３．「山おろしよ」の技法"),
  pAns("擬人（法）"),
  pIn([t("【解説】"), t("無生物の山風に「よ」と呼びかけることで、意志を持つ存在のように扱う擬人法。「よ」は呼びかけの感動詞。")]),

  sp(80),
  qt("４．「黒髪の」の「の」の用法"),
  pAns("イ　主格（〜が）"),
  pIn([t("【解説】"), t("「黒髪の乱れてけさは」は「黒髪が乱れて、今朝は」の意。連体修飾でなく主格の「の」。古典では「が」の代わりに「の」が主格を示すことがある。")]),
  sp(200),

  // ===== 大問五 解答 =====
  h("大問五　解答　（各３点　計６点）","CC0000"),

  qt("１．七十五番（模範解答）"),
  ...waka("契りおきし　させもが露を　命にて","あはれ今年の　秋もいぬめり"),
  sp(40),
  pAns("（あなたが）「させも草の露（＝なほたのめという観音の言葉）」を頼りにせよと約束してくださったその言葉を命のよりどころにしていたのに、ああ、今年の秋もむなしく過ぎていくようだ。"),
  pIn([t("【採点ポイント】"), t("「させもが露」＝約束の言葉 / 「命にて」＝命のよりどころとして / 「いぬめり」＝行ってしまうようだ（秋が過ぎる）を押さえること。")]),

  sp(120),
  qt("２．八十二番（模範解答）"),
  ...waka("思ひわびさても　命は　あるものを","憂きにたへぬは　涙なりけり"),
  sp(40),
  pAns("（恋に）思い悩んでも、それでも命は続いているものを、このつらさに耐えられないのは（この）涙なのだなあ。"),
  pIn([t("【採点ポイント】"), t("「思ひわびさても」＝悩んでもそれでも / 「あるものを」＝あるのに（逆接の詠嘆）/ 「憂きにたへぬ」＝つらさに耐えられない / 「なりけり」の詠嘆を反映。")]),
  sp(200),

  // ===== 大問六 解答 =====
  h("大問六　解答　（各２点　計１０点）","CC0000"),

  new Table({
    width:{ size:9000, type:WidthType.DXA },
    columnWidths:[600,1600,6800],
    rows:[
      new TableRow({ children:[cell("問",600,{bold:true,shade:true,center:true}),cell("正答",1600,{bold:true,shade:true,center:true}),cell("解説",6800,{bold:true,shade:true})] }),
      ...[ ["１（１）","77番","「瀬をはやみ〜われても末にあはむとぞ思ふ」川が分かれても合流するように、離れても再会を誓う恋歌。"],
           ["１（２）","81番","「ほととぎす鳴きつる方をながむれば　ただ有明の月ぞ残れる」姿なく月だけが残る夏の歌。"],
           ["１（３）","76番","「わたの原漕ぎ出でて見ればひさかたの　雲居にまがふ沖つ白波」白波と雲を見間違う海景。"],
           ["１（４）","80番","「長からむ心も知らず黒髪の　乱れてけさはものをこそ思へ」黒髪乱れたまま思い悩む女心。"],
           ["２","74・77・80・82番","74番（冷たい人への恋の祈り）、77番（再会を誓う恋）、80番（男心を知らず悩む女）、82番（恋に思い悩む述懐）。75番は息子の出世を嘆く歌で恋には含まない。"],
           ["３","イ","崇徳院（1119〜1164）は第75代天皇。保元の乱（1156年）で後白河天皇側に敗れ讃岐に流された。死後は怨霊として恐れられた。"],
           ["４","ロ（藤原定家）","小倉百人一首は鎌倉時代初期に藤原定家が撰んだ。紀貫之は古今和歌集（905年）の撰者。"],
           ["５","夏 / ほととぎすは夏を代表する鳥（夏の季語）であるため。","ホトトギスはカッコウ目の鳥で初夏に渡来し鳴く。和歌・俳句では夏の代表的な季語・季題。"],
      ].map(([no,ans,ex])=>new TableRow({ children:[cell(no,600,{center:true}),cell(ans,1600,{red:true,bold:true,center:true}),cell(ex,6800)] }))
    ]
  }),
  sp(200),

  // 配点まとめ
  h("【配点まとめ】","CC0000"),
  new Table({
    width:{ size:9000, type:WidthType.DXA },
    columnWidths:[1285,1286,1286,1286,1286,1286,1285],
    rows:[
      new TableRow({ children:
        ["大問一（６点）","大問二（８点）","大問三（１２点）","大問四（８点）","大問五（６点）","大問六（１０点）","合計（５０点）"]
        .map((label,i)=>new TableCell({
          borders:bdrs, width:{ size:1285, type:WidthType.DXA },
          margins:{ top:80, bottom:80, left:80, right:80 },
          shading:{ fill:"EEEEEE", type:"clear" },
          children:[new Paragraph({ children:[tS(label,{ bold:true, color: i===6?"CC0000":"000000" })], alignment:AlignmentType.CENTER })]
        }))
      }),
      new TableRow({ children:
        ["6","8","12","8","6","10","50"].map((n,i)=>new TableCell({
          borders:bdrs, width:{ size:1285, type:WidthType.DXA },
          margins:{ top:80, bottom:80, left:80, right:80 },
          children:[new Paragraph({
            children:[new TextRun({ text:n+"点", font:JP, size:S, bold:true, color: i===6?"CC0000":"000000" })],
            alignment:AlignmentType.CENTER, spacing:{ before:80, after:80 }
          })]
        }))
      })
    ]
  }),
];

// ======= ドキュメント生成 =======
const doc = new Document({
  sections:[{
    properties:{
      page:{
        size:{ width:11906, height:16838 },
        margin:{ top:1134, right:1134, bottom:1134, left:1134 }
      }
    },
    headers:{
      default: new Header({
        children:[new Paragraph({
          children:[tS("百人一首試験（第四回）　七十四番〜八十二番")],
          alignment:AlignmentType.RIGHT
        })]
      })
    },
    children:[...MONDAI, ...KAITOU]
  }]
});

Packer.toBuffer(doc).then(buf=>{
  fs.writeFileSync("hyakunin_exam4.docx", buf);
  console.log("Done: hyakunin_exam4.docx");
});
