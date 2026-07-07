const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = '漢詩鑑賞 — 李白・杜甫';

const C = {
  ink:       "1C1C1C",
  darkGray:  "333333",
  midGray:   "666666",
  lightGray: "BBBBBB",
  white:     "FFFFFF",
  offWhite:  "FAFAFA",
  cream:     "F5F0E8",
  parchment: "EDE5D0",
  gold:      "8B6914",   // darkened for print contrast
  goldLight: "A07A18",
  crimson:   "8B1A1A",
  deepRed:   "6B1010",
  border:    "C8B89A",
  softBlue:  "1B3A6B",
  softGreen: "2C5F3A",
  brown:     "5C3D1E",
};

// ════════════════════════════════════════════════════════════
// スライド 1 ― タイトル
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: C.white };

  // 上下の太帯
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0,    w: 10, h: 0.45, fill: { color: C.ink },    line: { color: C.ink } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.18, w: 10, h: 0.45, fill: { color: C.ink },    line: { color: C.ink } });

  // 上帯テキスト
  s.addText("中学校 国語・漢文", {
    x: 0.4, y: 0.07, w: 9.2, h: 0.3,
    fontSize: 13, fontFace: "Calibri", color: C.white, align: "right", margin: 0
  });

  // 縦分割線
  s.addShape(pres.shapes.LINE, { x: 5.0, y: 0.45, w: 0, h: 4.73, line: { color: C.lightGray, width: 0.8 } });

  // 左：タイトル
  s.addText("漢詩鑑賞", {
    x: 0.5, y: 0.75, w: 4.3, h: 1.0,
    fontSize: 54, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.5, y: 1.85, w: 4.2, h: 0, line: { color: C.gold, width: 2 } });
  s.addText([
    { text: "李　白", options: { breakLine: true } },
    { text: "杜　甫", options: {} },
  ], {
    x: 0.5, y: 2.05, w: 4.2, h: 1.5,
    fontSize: 32, fontFace: "Georgia",
    color: C.darkGray, align: "left", margin: 0, paraSpaceAfter: 12
  });
  s.addText("唐代の二大詩人", {
    x: 0.5, y: 3.72, w: 4.2, h: 0.38,
    fontSize: 15, fontFace: "Calibri",
    color: C.midGray, align: "left", margin: 0
  });

  // 右：詩人情報カード
  const poets = [
    { name: "李　白", dates: "701–762", title: "詩仙", note: "「酒と月と旅」を愛した浪漫派の天才", accent: C.gold },
    { name: "杜　甫", dates: "712–770", title: "詩聖", note: "社会と民衆の苦しみを描いた写実の巨人", accent: C.crimson },
  ];
  poets.forEach((p, i) => {
    const y = 0.65 + i * 2.28;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y, w: 4.45, h: 2.05, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 5.25, y, w: 0.08, h: 2.05, fill: { color: p.accent }, line: { color: p.accent } });
    s.addText(p.name, { x: 5.42, y: y + 0.1, w: 2.2, h: 0.7, fontSize: 36, bold: true, fontFace: "Georgia", color: C.ink, align: "left", margin: 0 });
    s.addText(p.title, { x: 7.6, y: y + 0.15, w: 1.98, h: 0.55, fontSize: 22, bold: true, fontFace: "Georgia", color: p.accent, align: "right", margin: 0 });
    s.addShape(pres.shapes.LINE, { x: 5.42, y: y + 0.88, w: 4.1, h: 0, line: { color: C.border, width: 0.7 } });
    s.addText(p.dates, { x: 5.42, y: y + 0.98, w: 4.1, h: 0.28, fontSize: 12, fontFace: "Calibri", color: C.midGray, align: "left", margin: 0 });
    s.addText(p.note, { x: 5.42, y: y + 1.32, w: 4.1, h: 0.58, fontSize: 13, fontFace: "Calibri", color: C.darkGray, align: "left", margin: 0 });
  });
}

// ════════════════════════════════════════════════════════════
// 【第一部】李白 ― 春夜宴従弟桃花園序
// ════════════════════════════════════════════════════════════

// スライド 2 ― セクション扉（李白）
{
  let s = pres.addSlide();
  s.background = { color: C.cream };

  // 左の太ストライプ
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 3.0, h: 5.625, fill: { color: C.parchment }, line: { color: C.parchment } });
  s.addShape(pres.shapes.RECTANGLE, { x: 2.98, y: 0, w: 0.06, h: 5.625, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("李", { x: 0.3, y: 0.38, w: 2.45, h: 0.9, fontSize: 60, bold: true, fontFace: "Georgia", color: C.gold, align: "center", margin: 0 });
  s.addText("白", { x: 0.3, y: 1.22, w: 2.45, h: 0.9, fontSize: 60, bold: true, fontFace: "Georgia", color: C.gold, align: "center", margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 0.45, y: 2.2, w: 2.1, h: 0, line: { color: C.gold, width: 1.5 } });
  s.addText("詩　仙", { x: 0.3, y: 2.32, w: 2.45, h: 0.45, fontSize: 20, fontFace: "Georgia", color: C.darkGray, align: "center", margin: 0 });
  s.addText("701–762", { x: 0.3, y: 2.85, w: 2.45, h: 0.32, fontSize: 13, fontFace: "Calibri", color: C.midGray, align: "center", margin: 0 });

  // 右：作品名
  s.addText("春夜宴従弟桃花園序", {
    x: 3.25, y: 0.5, w: 6.4, h: 0.88,
    fontSize: 32, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addText("しゅんやえんじゅうていとうかえんのじょ", {
    x: 3.25, y: 1.42, w: 6.4, h: 0.35,
    fontSize: 13, fontFace: "Calibri",
    color: C.midGray, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 3.25, y: 1.85, w: 6.4, h: 0, line: { color: C.gold, width: 1.5 } });
  s.addText([
    { text: "形式：散文詩（序文）", options: { breakLine: true } },
    { text: "制作：744年頃（唐・玄宗の時代）", options: { breakLine: true } },
    { text: "内容：従兄弟たちと桃の花の庭で宴を開く春の夜を詠んだ序文", options: {} },
  ], {
    x: 3.25, y: 2.02, w: 6.4, h: 1.35,
    fontSize: 14.5, fontFace: "Calibri",
    color: C.darkGray, align: "left", margin: 0, paraSpaceAfter: 8
  });
  s.addShape(pres.shapes.LINE, { x: 3.25, y: 3.46, w: 6.4, h: 0, line: { color: C.border, width: 0.7 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.25, y: 3.62, w: 6.4, h: 0.65, fill: { color: C.parchment }, line: { color: C.border } });
  s.addText("人生の短さを悟りながら、今この瞬間の宴の喜びを謳い上げた李白の代表的散文詩", {
    x: 3.38, y: 3.72, w: 6.15, h: 0.48,
    fontSize: 13.5, fontFace: "Calibri",
    color: C.darkGray, align: "left", margin: 0
  });
}

// スライド 3 ― 原文 全文（漢文）
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.4, w: 0.06, h: 4.88, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("春夜宴従弟桃花園序 — 原文", {
    x: 0.55, y: 0.25, w: 9.1, h: 0.55,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.55, y: 0.88, w: 9.0, h: 0, line: { color: C.gold, width: 1 } });

  const text1 = [
    "夫　天　地　者　、　萬　物　之　逆　旅　也　、",
    "光　陰　者　、　百　代　之　過　客　也　。",
    "而　浮　生　若　夢　、　爲　驩　幾　何　。",
    "古　人　秉　燭　夜　遊　、　良　有　以　也　。",
  ];
  const text2 = [
    "況　陽　春　召　我　以　煙　景　、",
    "大　塊　假　我　以　文　章　。",
    "會　桃　花　之　芳　園　、　序　天　倫　之　樂　事　。",
    "群　季　俊　秀　、　皆　爲　惠　連　。",
    "吾　人　詠　歌　、　獨　慙　康　樂　。",
    "幽　賞　未　已　、　高　談　轉　淸　。",
    "開　瓊　筵　以　坐　花　、　飛　羽　觴　而　醉　月　。",
    "不　有　佳　詠　、　何　伸　雅　懐　。",
    "如　詩　不　成　、　罰　依　金　谷　酒　數　。",
  ];

  s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 1.0, w: 4.4, h: 4.2, fill: { color: C.cream }, line: { color: C.border } });
  text1.forEach((line, i) => {
    s.addText(line, {
      x: 0.65, y: 1.12 + i * 0.96, w: 4.2, h: 0.86,
      fontSize: 15.5, fontFace: "Georgia",
      color: C.ink, align: "left", valign: "top", margin: 0
    });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.12, y: 1.0, w: 4.53, h: 4.2, fill: { color: C.cream }, line: { color: C.border } });
  text2.forEach((line, i) => {
    s.addText(line, {
      x: 5.22, y: 1.1 + i * 0.45, w: 4.33, h: 0.42,
      fontSize: 12.5, fontFace: "Georgia",
      color: C.ink, align: "left", valign: "top", margin: 0
    });
  });

  s.addText("李　白　撰", {
    x: 8.3, y: 5.25, w: 1.35, h: 0.32,
    fontSize: 11, fontFace: "Georgia",
    color: C.midGray, align: "right", margin: 0
  });
}

// スライド 4 ― 冒頭句のクローズアップ＋書き下し文
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: C.gold }, line: { color: C.gold } });

  // 漢文（大きく）
  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 0.22, w: 9.1, h: 1.72, fill: { color: C.cream }, line: { color: C.gold } });
  s.addText("夫　天　地　者　、　萬　物　之　逆　旅　也", {
    x: 0.55, y: 0.32, w: 8.9, h: 0.75,
    fontSize: 30, bold: true, fontFace: "Georgia",
    color: C.ink, align: "center", margin: 0
  });
  s.addText("光　陰　者　、　百　代　之　過　客　也", {
    x: 0.55, y: 1.08, w: 8.9, h: 0.7,
    fontSize: 27, fontFace: "Georgia",
    color: C.darkGray, align: "center", margin: 0
  });

  // 書き下し文
  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 2.05, w: 9.1, h: 0.6, fill: { color: C.parchment }, line: { color: C.border } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 2.05, w: 0.07, h: 0.6, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("【書き下し文】　夫れ、天地は万物の逆旅にして、光陰は百代の過客なり。", {
    x: 0.62, y: 2.12, w: 8.8, h: 0.46,
    fontSize: 14.5, fontFace: "Georgia",
    color: C.gold, align: "left", margin: 0
  });

  // 語釈（3列）
  const glosses = [
    { word: "夫れ（それ）", mean: "感嘆の発語詞。「そもそも」「いったい」" },
    { word: "逆旅（げきりょ）", mean: "旅人を逆（むか）える宿。旅籠・宿屋のこと" },
    { word: "光陰（こういん）", mean: "時間・歳月のこと。「光」は日、「陰」は月" },
    { word: "百代（ひゃくだい）", mean: "はるかな長い年月・時代のこと" },
    { word: "過客（かかく）", mean: "通り過ぎる旅人。一時的にそこにいる者" },
    { word: "也（なり）", mean: "断定の助字。「〜である」を強調する" },
  ];
  glosses.forEach((g, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.45 + col * 3.05, y = 2.82 + row * 1.22;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.9, h: 1.1, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h: 1.1, fill: { color: C.gold }, line: { color: C.gold } });
    s.addText(g.word, { x: x + 0.14, y: y + 0.1, w: 2.65, h: 0.36, fontSize: 14, bold: true, fontFace: "Georgia", color: C.gold, margin: 0 });
    s.addText(g.mean, { x: x + 0.14, y: y + 0.5, w: 2.65, h: 0.52, fontSize: 11.5, fontFace: "Calibri", color: C.darkGray, margin: 0 });
  });
}

// スライド 5 ― 現代語訳と解説（冒頭句）
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.4, w: 0.06, h: 4.88, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("現代語訳と解説", {
    x: 0.55, y: 0.25, w: 9.1, h: 0.55,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.55, y: 0.88, w: 9.0, h: 0, line: { color: C.gold, width: 1 } });

  s.addText("夫天地者萬物之逆旅也、光陰者百代之過客也。", {
    x: 0.55, y: 0.98, w: 9.0, h: 0.38,
    fontSize: 14, fontFace: "Georgia",
    color: C.midGray, align: "center", margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 1.44, w: 9.12, h: 1.18, fill: { color: C.cream }, line: { color: C.gold } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 1.44, w: 0.07, h: 1.18, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("現代語訳", { x: 0.72, y: 1.5, w: 8.8, h: 0.28, fontSize: 12, bold: true, fontFace: "Calibri", color: C.gold, margin: 0 });
  s.addText("「そもそも天地とは、万物が宿る旅籠（はたごや）のようなものであり、\n　時の流れとは、永遠の歴史の中をただよう旅人のようなものである。」", {
    x: 0.72, y: 1.82, w: 8.8, h: 0.72,
    fontSize: 15, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });

  const points = [
    {
      title: "「逆旅（げきりょ）」の比喩",
      body: "宿屋・旅籠は旅人が一時的に休む場所。そこに天地（この世界）を例えることで、「人間も万物も、この世に一時的に宿っているだけ」という無常観を表す。仏教の「諸行無常」にも通じる東洋的な世界観。"
    },
    {
      title: "「過客（かかく）」の比喩",
      body: "通り過ぎる旅人。「光陰（時間）」を旅人に例えることで、時が人間を待たずに流れ去っていくイメージを生む。「光陰矢の如し」ということわざの典拠ともなっている。"
    },
    {
      title: "この句が言いたいこと",
      body: "人の一生は短く、時間は矢のように過ぎ去る。だから今この瞬間を大切に、花の下で宴を開き、詩を詠み、月を愛でようではないか——それが李白がこの序文で伝えたいメッセージ。"
    },
  ];

  points.forEach((p, i) => {
    const y = 2.78 + i * 0.88;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 9.12, h: 0.78, fill: { color: i % 2 === 0 ? C.cream : C.white }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 0.07, h: 0.78, fill: { color: C.crimson }, line: { color: C.crimson } });
    s.addText(p.title, { x: 0.72, y: y + 0.07, w: 8.8, h: 0.28, fontSize: 13, bold: true, fontFace: "Calibri", color: C.crimson, margin: 0 });
    s.addText(p.body, { x: 0.72, y: y + 0.38, w: 8.8, h: 0.36, fontSize: 11, fontFace: "Calibri", color: C.ink, margin: 0 });
  });
}

// スライド 6 ― 全文書き下し文 ＋ 詩全体の解説
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.4, w: 0.06, h: 4.88, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("春夜宴従弟桃花園序 — 全文書き下し文", {
    x: 0.55, y: 0.25, w: 9.1, h: 0.55,
    fontSize: 21, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.55, y: 0.88, w: 9.0, h: 0, line: { color: C.gold, width: 1 } });

  const kudashi = [
    "夫れ、天地は万物の逆旅にして、光陰は百代の過客なり。",
    "而して浮生夢の若く、驩を為すこと幾何ぞ。",
    "古人燭を秉りて夜遊ぶ、良に以有るなり。",
    "況んや陽春我を召すに煙景を以てし、",
    "大塊我に仮すに文章を以てするをや。",
    "桃花の芳園に会し、天倫の楽事を序す。",
    "群季俊秀にして、皆恵連と為す。",
    "吾人詠歌すれど、独り康楽に慙ず。",
    "幽賞未だ已まず、高談転た清し。",
    "瓊筵を開きて以て花に坐し、羽觴を飛ばして月に酔う。",
    "佳詠有らずんば、何ぞ雅懐を伸べん。",
    "詩成らずんば、罰は金谷の酒数に依らん。",
  ];

  s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 1.0, w: 5.5, h: 4.22, fill: { color: C.cream }, line: { color: C.border } });
  kudashi.forEach((line, i) => {
    s.addText(line, {
      x: 0.68, y: 1.12 + i * 0.34, w: 5.28, h: 0.32,
      fontSize: 12.5, fontFace: "Georgia",
      color: C.ink, align: "left", margin: 0
    });
  });

  s.addText("詩全体のテーマ", {
    x: 6.25, y: 1.0, w: 3.42, h: 0.42,
    fontSize: 15, bold: true, fontFace: "Georgia",
    color: C.gold, align: "left", margin: 0
  });

  const themes = [
    { t: "無常観と刹那の喜び", b: "人生の短さを嘆くのではなく、だからこそ今を楽しむ——李白らしい豪快な人生観" },
    { t: "詩と宴の一体化", b: "「詩を作らぬ者は酒罰」という粋な約束。詩・酒・月・花が渾然一体となる美の世界" },
    { t: "仙境としての桃園", b: "桃花源（陶淵明の理想郷）を借景に。日常から切り離されたユートピアの宴" },
  ];
  themes.forEach((t, i) => {
    const y = 1.55 + i * 1.22;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.25, y, w: 3.42, h: 1.1, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 6.25, y, w: 0.07, h: 1.1, fill: { color: C.gold }, line: { color: C.gold } });
    s.addText(t.t, { x: 6.42, y: y + 0.1, w: 3.15, h: 0.32, fontSize: 13, bold: true, fontFace: "Calibri", color: C.gold, margin: 0 });
    s.addText(t.b, { x: 6.42, y: y + 0.48, w: 3.15, h: 0.55, fontSize: 11.5, fontFace: "Calibri", color: C.darkGray, margin: 0 });
  });

  s.addText("李白 701-762 ／ 唐代 玄宗朝", {
    x: 6.25, y: 4.88, w: 3.42, h: 0.35,
    fontSize: 11, fontFace: "Calibri", color: C.midGray, align: "right", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// 【第二部】杜甫 ― 春望
// ════════════════════════════════════════════════════════════

// スライド 7 ― セクション扉（杜甫）
{
  let s = pres.addSlide();
  s.background = { color: C.cream };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 3.0, h: 5.625, fill: { color: C.parchment }, line: { color: C.parchment } });
  s.addShape(pres.shapes.RECTANGLE, { x: 2.98, y: 0, w: 0.06, h: 5.625, fill: { color: C.crimson }, line: { color: C.crimson } });

  s.addText("杜", { x: 0.3, y: 0.38, w: 2.45, h: 0.9, fontSize: 60, bold: true, fontFace: "Georgia", color: C.crimson, align: "center", margin: 0 });
  s.addText("甫", { x: 0.3, y: 1.22, w: 2.45, h: 0.9, fontSize: 60, bold: true, fontFace: "Georgia", color: C.crimson, align: "center", margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 0.45, y: 2.2, w: 2.1, h: 0, line: { color: C.crimson, width: 1.5 } });
  s.addText("詩　聖", { x: 0.3, y: 2.32, w: 2.45, h: 0.45, fontSize: 20, fontFace: "Georgia", color: C.darkGray, align: "center", margin: 0 });
  s.addText("712–770", { x: 0.3, y: 2.85, w: 2.45, h: 0.32, fontSize: 13, fontFace: "Calibri", color: C.midGray, align: "center", margin: 0 });

  s.addText("春　望", {
    x: 3.25, y: 0.5, w: 6.4, h: 0.95,
    fontSize: 50, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addText("しゅんぼう", {
    x: 3.25, y: 1.48, w: 6.4, h: 0.35,
    fontSize: 13, fontFace: "Calibri",
    color: C.midGray, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 3.25, y: 1.92, w: 6.4, h: 0, line: { color: C.crimson, width: 1.5 } });
  s.addText([
    { text: "形式：五言律詩（8句・56字）", options: { breakLine: true } },
    { text: "制作：757年（安禄山の乱の翌年）", options: { breakLine: true } },
    { text: "内容：戦乱で廃墟となった長安で、戦場にある家族を思う杜甫の心情", options: {} },
  ], {
    x: 3.25, y: 2.1, w: 6.4, h: 1.32,
    fontSize: 14.5, fontFace: "Calibri",
    color: C.darkGray, align: "left", margin: 0, paraSpaceAfter: 8
  });
  s.addShape(pres.shapes.LINE, { x: 3.25, y: 3.5, w: 6.4, h: 0, line: { color: C.border, width: 0.7 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.25, y: 3.65, w: 6.4, h: 0.65, fill: { color: C.parchment }, line: { color: C.border } });
  s.addText("戦乱・離別・老い——杜甫の代表作にして唐詩を代表する「社会詩」の最高傑作", {
    x: 3.38, y: 3.75, w: 6.15, h: 0.48,
    fontSize: 13.5, fontFace: "Calibri",
    color: C.darkGray, align: "left", margin: 0
  });
}

// スライド 8 ― 原文 ＋ 読み方
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: C.crimson }, line: { color: C.crimson } });

  s.addText("春望 — 原文・書き下し文", {
    x: 0.5, y: 0.22, w: 9.0, h: 0.48,
    fontSize: 20, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.5, y: 0.78, w: 9.0, h: 0, line: { color: C.crimson, width: 1 } });

  const verses = [
    { han: "國破山河在", yomi: "国破れて山河在り" },
    { han: "城春草木深", yomi: "城春にして草木深し" },
    { han: "感時花濺涙", yomi: "時に感じては花にも涙を濺ぎ" },
    { han: "恨別鳥驚心", yomi: "別れを恨みては鳥にも心を驚かす" },
    { han: "烽火連三月", yomi: "烽火三月に連なり" },
    { han: "家書抵萬金", yomi: "家書万金に抵る" },
    { han: "白頭掻更短", yomi: "白頭掻けばさらに短く" },
    { han: "渾欲不勝簪", yomi: "渾て簪に勝えざらんと欲す" },
  ];

  const ren = ["首聯", "頷聯", "頸聯", "尾聯"];

  verses.forEach((v, i) => {
    const row = Math.floor(i / 2), col = i % 2;
    const x = 0.5 + col * 4.72, y = 0.9 + row * 1.15;

    if (col === 0) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: 0.5, y: y + 0.1, w: 0.55, h: 0.92,
        fill: { color: C.crimson }, line: { color: C.crimson }
      });
      s.addText(ren[row], {
        x: 0.5, y: y + 0.15, w: 0.55, h: 0.82,
        fontSize: 10, fontFace: "Georgia", color: C.white, align: "center", valign: "middle", margin: 0
      });
    }

    const bx = col === 0 ? 1.15 : 0.5 + col * 4.72;
    const bw = col === 0 ? 4.0 : 4.6;

    s.addShape(pres.shapes.RECTANGLE, {
      x: bx, y: y + 0.1, w: bw, h: 0.92,
      fill: { color: C.cream }, line: { color: C.border }
    });
    s.addText(v.han, {
      x: bx + 0.15, y: y + 0.15, w: bw * 0.44, h: 0.4,
      fontSize: 20, bold: true, fontFace: "Georgia",
      color: C.ink, align: "left", margin: 0
    });
    s.addText(v.yomi, {
      x: bx + 0.15, y: y + 0.58, w: bw - 0.3, h: 0.35,
      fontSize: 12.5, fontFace: "Georgia",
      color: C.darkGray, align: "left", margin: 0
    });

    s.addShape(pres.shapes.OVAL, {
      x: bx + bw - 0.45, y: y + 0.15, w: 0.32, h: 0.32,
      fill: { color: C.crimson }, line: { color: C.crimson }
    });
    s.addText(String(i + 1), {
      x: bx + bw - 0.45, y: y + 0.15, w: 0.32, h: 0.32,
      fontSize: 10, bold: true, fontFace: "Calibri",
      color: C.white, align: "center", valign: "middle", margin: 0
    });
  });

  s.addText("杜甫 ／ 七五七年", {
    x: 8.2, y: 5.32, w: 1.65, h: 0.26,
    fontSize: 10, fontFace: "Calibri", color: C.midGray, align: "right", margin: 0
  });
}

// スライド 9 ― 首聯・頷聯 の詳細解説
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.4, w: 0.06, h: 4.88, fill: { color: C.crimson }, line: { color: C.crimson } });

  s.addText("首聯・頷聯 — 詳細解説", {
    x: 0.55, y: 0.25, w: 9.1, h: 0.55,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.55, y: 0.88, w: 9.0, h: 0, line: { color: C.crimson, width: 1 } });

  const stanzas = [
    {
      han: "國破山河在 ／ 城春草木深",
      yomi: "国破れて山河在り　／　城春にして草木深し",
      label: "首聯",
      trans: "国（長安の都）は戦乱で滅んでしまったが、山と川だけはもとのまま残っている。城（都）に春が来て、草木だけが生い茂っている。",
      points: [
        "「国破れて山河在り」— 人の営みは滅んでも自然は変わらないという対比の妙",
        "廃墟と生命力の対比。戦乱の痛みを直接言わず景色で表す「情景融合」",
        "「草木深し」— 誰も手入れしない廃城に生い茂る草のわびしさ",
      ]
    },
    {
      han: "感時花濺涙 ／ 恨別鳥驚心",
      yomi: "時に感じては花にも涙を濺ぎ　／　別れを恨みては鳥にも心を驚かす",
      label: "頷聯",
      trans: "時世を嘆いては、花を見ても涙がこぼれ落ちる。離別を悲しんでは、鳥の鳴き声にさえ心が乱される。",
      points: [
        "「感時」＝戦乱の世への嘆き　「恨別」＝家族との別れへの恨み",
        "花も鳥も普通は喜びの象徴。それさえも悲しみに変えてしまう深刻さを表す",
        "対句（ついく）の美 — 感時↔恨別、花↔鳥、涙↔驚心が完璧に対応している",
      ]
    },
  ];

  stanzas.forEach((st, i) => {
    const y = 1.02 + i * 2.28;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 9.12, h: 0.52, fill: { color: C.cream }, line: { color: C.crimson } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 0.8, h: 0.52, fill: { color: C.crimson }, line: { color: C.crimson } });
    s.addText(st.label, { x: 0.55, y, w: 0.8, h: 0.52, fontSize: 13, bold: true, fontFace: "Georgia", color: C.white, align: "center", valign: "middle", margin: 0 });
    s.addText(st.han, { x: 1.45, y: y + 0.06, w: 4.5, h: 0.22, fontSize: 14, bold: true, fontFace: "Georgia", color: C.ink, margin: 0 });
    s.addText(st.yomi, { x: 1.45, y: y + 0.28, w: 7.1, h: 0.2, fontSize: 11, fontFace: "Georgia", color: C.midGray, margin: 0 });

    s.addText(st.trans, {
      x: 0.55, y: y + 0.6, w: 9.12, h: 0.52,
      fontSize: 13, fontFace: "Calibri",
      color: C.darkGray, align: "left", margin: 0
    });
    st.points.forEach((pt, j) => {
      s.addText("▶ " + pt, {
        x: 0.65, y: y + 1.18 + j * 0.3, w: 8.9, h: 0.28,
        fontSize: 12, fontFace: "Calibri",
        color: C.ink, align: "left", margin: 0
      });
    });
  });
}

// スライド 10 ― 頸聯・尾聯 の詳細解説
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.4, w: 0.06, h: 4.88, fill: { color: C.crimson }, line: { color: C.crimson } });

  s.addText("頸聯・尾聯 — 詳細解説", {
    x: 0.55, y: 0.25, w: 9.1, h: 0.55,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.55, y: 0.88, w: 9.0, h: 0, line: { color: C.crimson, width: 1 } });

  const stanzas2 = [
    {
      han: "烽火連三月 ／ 家書抵萬金",
      yomi: "烽火三月に連なり　／　家書万金に抵る",
      label: "頸聯",
      trans: "のろし（戦乱の合図）は三か月も絶えず上がり続け、家族からの手紙一通が黄金万両にも値するほど待ち望まれる。",
      points: [
        "「烽火（ほうか）」＝のろし。安禄山の乱が757年まで続いた史実が背景にある",
        "「三月」= 三か月間休みなく続く戦い。長期化する絶望感を表す",
        "「家書万金」— 通信が絶たれた戦時に届く手紙の価値を金に例えた名句",
      ]
    },
    {
      han: "白頭掻更短 ／ 渾欲不勝簪",
      yomi: "白頭掻けばさらに短く　／　渾て簪に勝えざらんと欲す",
      label: "尾聯",
      trans: "白髪の頭をかくたびに、さらに（髪が抜けて）短くなっていく。もはや簪（かんざし）もとまらないほどに。",
      points: [
        "「白頭」= 白髪になった自分の老いた頭。心労と老いを表す具体的なイメージ",
        "「簪（かんざし）」は冠をとめる具。かんざしも刺さらないほど白髪が薄い——老耄の悲哀",
        "詩の結末を「老いた自分の姿」で締める。「国の滅亡」から「一本の白髪」に収束する構造美",
      ]
    },
  ];

  stanzas2.forEach((st, i) => {
    const y = 1.02 + i * 2.28;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 9.12, h: 0.52, fill: { color: C.cream }, line: { color: C.crimson } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 0.8, h: 0.52, fill: { color: C.crimson }, line: { color: C.crimson } });
    s.addText(st.label, { x: 0.55, y, w: 0.8, h: 0.52, fontSize: 13, bold: true, fontFace: "Georgia", color: C.white, align: "center", valign: "middle", margin: 0 });
    s.addText(st.han, { x: 1.45, y: y + 0.06, w: 4.5, h: 0.22, fontSize: 14, bold: true, fontFace: "Georgia", color: C.ink, margin: 0 });
    s.addText(st.yomi, { x: 1.45, y: y + 0.28, w: 7.1, h: 0.2, fontSize: 11, fontFace: "Georgia", color: C.midGray, margin: 0 });
    s.addText(st.trans, { x: 0.55, y: y + 0.6, w: 9.12, h: 0.52, fontSize: 13, fontFace: "Calibri", color: C.darkGray, margin: 0 });
    st.points.forEach((pt, j) => {
      s.addText("▶ " + pt, { x: 0.65, y: y + 1.18 + j * 0.3, w: 8.9, h: 0.28, fontSize: 12, fontFace: "Calibri", color: C.ink, margin: 0 });
    });
  });
}

// スライド 11 ― 春望 全体まとめ ＋ 詩の構造
{
  let s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.4, w: 0.06, h: 4.88, fill: { color: C.crimson }, line: { color: C.crimson } });

  s.addText("春望 — 詩の構造と鑑賞ポイント", {
    x: 0.55, y: 0.25, w: 9.1, h: 0.55,
    fontSize: 22, bold: true, fontFace: "Georgia",
    color: C.ink, align: "left", margin: 0
  });
  s.addShape(pres.shapes.LINE, { x: 0.55, y: 0.88, w: 9.0, h: 0, line: { color: C.crimson, width: 1 } });

  const structure = [
    { label: "首聯", scope: "景（風景）", verse: "國破山河在 ／ 城春草木深", color: C.softGreen },
    { label: "頷聯", scope: "情（感情）", verse: "感時花濺涙 ／ 恨別鳥驚心", color: C.crimson },
    { label: "頸聯", scope: "事（事実）", verse: "烽火連三月 ／ 家書抵萬金", color: C.softBlue },
    { label: "尾聯", scope: "情（感情）", verse: "白頭掻更短 ／ 渾欲不勝簪", color: C.brown },
  ];

  structure.forEach((st, i) => {
    const y = 1.02 + i * 0.97;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 5.5, h: 0.84, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 0.75, h: 0.84, fill: { color: st.color }, line: { color: st.color } });
    s.addText(st.label, { x: 0.55, y: y + 0.06, w: 0.75, h: 0.38, fontSize: 13, bold: true, fontFace: "Georgia", color: C.white, align: "center", margin: 0 });
    s.addText(st.scope, { x: 0.55, y: y + 0.46, w: 0.75, h: 0.3, fontSize: 9.5, fontFace: "Calibri", color: "EEEEEE", align: "center", margin: 0 });
    s.addText(st.verse, { x: 1.42, y: y + 0.22, w: 4.5, h: 0.4, fontSize: 13, fontFace: "Georgia", color: C.ink, margin: 0 });
  });

  s.addText("鑑賞のポイント", {
    x: 6.25, y: 1.02, w: 3.42, h: 0.38,
    fontSize: 14, bold: true, fontFace: "Georgia", color: C.crimson, margin: 0
  });
  const points = [
    { t: "景から情へ", b: "首聯の「廃墟の風景」から始まり、頷聯の「感情」へと視点が移動する。感情を直接語らず風景で暗示する" },
    { t: "対句の美", b: "「感時花濺涙 ／ 恨別鳥驚心」など、各句が意味・音・字数で完璧に呼応する対句が全篇を貫く" },
    { t: "巨視から微視へ", b: "「国が滅びた」という巨大な出来事から「白髪の一本一本」という極めて微細な描写へ収束する構造美" },
  ];
  points.forEach((p, i) => {
    const y = 1.52 + i * 1.15;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.25, y, w: 3.42, h: 1.02, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 6.25, y, w: 0.07, h: 1.02, fill: { color: C.crimson }, line: { color: C.crimson } });
    s.addText(p.t, { x: 6.42, y: y + 0.08, w: 3.15, h: 0.3, fontSize: 12, bold: true, fontFace: "Calibri", color: C.crimson, margin: 0 });
    s.addText(p.b, { x: 6.42, y: y + 0.42, w: 3.15, h: 0.54, fontSize: 11, fontFace: "Calibri", color: C.darkGray, margin: 0 });
  });

  s.addText("杜甫 712–770 ／ 七五七年（安史の乱中）", {
    x: 0.55, y: 5.08, w: 9.12, h: 0.32,
    fontSize: 11, fontFace: "Calibri", color: C.midGray, align: "center", margin: 0
  });
}

// ════════════════════════════════════════════════════════════
// スライド 12 ― 李白 vs 杜甫 比較まとめ
// ════════════════════════════════════════════════════════════
{
  let s = pres.addSlide();
  s.background = { color: C.white };

  // 上下帯
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0,    w: 10, h: 0.45, fill: { color: C.ink }, line: { color: C.ink } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.18, w: 10, h: 0.45, fill: { color: C.ink }, line: { color: C.ink } });
  s.addText("李白 vs 杜甫 — まとめ", {
    x: 0.4, y: 0.08, w: 9.2, h: 0.3,
    fontSize: 15, bold: true, fontFace: "Georgia", color: C.white, align: "center", margin: 0
  });

  // 中央の縦分割線
  s.addShape(pres.shapes.LINE, { x: 5.0, y: 0.45, w: 0, h: 4.73, line: { color: C.lightGray, width: 1 } });

  // 左：李白
  s.addText("李　白", { x: 0.3, y: 0.58, w: 4.5, h: 0.62, fontSize: 34, bold: true, fontFace: "Georgia", color: C.gold, align: "center", margin: 0 });
  s.addText("詩　仙", { x: 0.3, y: 1.18, w: 4.5, h: 0.35, fontSize: 17, fontFace: "Georgia", color: C.midGray, align: "center", margin: 0 });

  const liData = [
    { k: "作風", v: "浪漫主義・雄大・自由奔放" },
    { k: "テーマ", v: "酒・月・旅・仙境・友情" },
    { k: "今回の詩", v: "春夜宴従弟桃花園序" },
    { k: "核心の句", v: "天地は万物の逆旅\n光陰は百代の過客" },
    { k: "メッセージ", v: "人生は短い。今この瞬間を\n大いに楽しもう" },
  ];
  liData.forEach((d, i) => {
    const y = 1.62 + i * 0.72;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 4.5, h: 0.62, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 0.07, h: 0.62, fill: { color: C.gold }, line: { color: C.gold } });
    s.addText(d.k, { x: 0.45, y, w: 1.0, h: 0.62, fontSize: 11, bold: true, fontFace: "Calibri", color: C.gold, align: "center", valign: "middle", margin: 0 });
    s.addText(d.v, { x: 1.5, y: y + 0.06, w: 3.12, h: 0.52, fontSize: 12, fontFace: "Calibri", color: C.darkGray, valign: "middle", margin: 0 });
  });

  // 右：杜甫
  s.addText("杜　甫", { x: 5.2, y: 0.58, w: 4.5, h: 0.62, fontSize: 34, bold: true, fontFace: "Georgia", color: C.crimson, align: "center", margin: 0 });
  s.addText("詩　聖", { x: 5.2, y: 1.18, w: 4.5, h: 0.35, fontSize: 17, fontFace: "Georgia", color: C.midGray, align: "center", margin: 0 });

  const duData = [
    { k: "作風", v: "写実主義・重厚・社会批判" },
    { k: "テーマ", v: "戦乱・民衆・老い・離別" },
    { k: "今回の詩", v: "春望（五言律詩）" },
    { k: "核心の句", v: "烽火連三月\n家書抵万金" },
    { k: "メッセージ", v: "戦乱の苦しみの中でも\n家族への思いは変わらない" },
  ];
  duData.forEach((d, i) => {
    const y = 1.62 + i * 0.72;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y, w: 4.5, h: 0.62, fill: { color: C.cream }, line: { color: C.border } });
    s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y, w: 0.07, h: 0.62, fill: { color: C.crimson }, line: { color: C.crimson } });
    s.addText(d.k, { x: 5.35, y, w: 1.0, h: 0.62, fontSize: 11, bold: true, fontFace: "Calibri", color: C.crimson, align: "center", valign: "middle", margin: 0 });
    s.addText(d.v, { x: 6.4, y: y + 0.06, w: 3.12, h: 0.52, fontSize: 12, fontFace: "Calibri", color: C.darkGray, valign: "middle", margin: 0 });
  });

  s.addText("唐代の二大詩人は、同じ時代に生き、互いを認め合った親友でもあった", {
    x: 0.5, y: 5.22, w: 9.0, h: 0.2,
    fontSize: 12, fontFace: "Calibri", color: C.white, align: "center", margin: 0
  });
}

// ── 出力 ──────────────────────────────────────────────────
const outputPath = "C:\\Users\\shondo\\Desktop\\漢詩鑑賞_李白と杜甫.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("✅ 完成: " + outputPath);
}).catch(e => console.error("❌ エラー:", e));
