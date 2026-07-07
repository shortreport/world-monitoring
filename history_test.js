const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
        LevelFormat, HeadingLevel, PageBreak } = require('docx');
const fs = require('fs');

// ────────────────────────────────────────────
// ヘルパー
// ────────────────────────────────────────────
const noBorder  = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const thinBorder  = { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" };
const thinBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };

function heading(text, level = 1) {
  const sizes = { 1: 32, 2: 28, 3: 24 };
  const bgColors = { 1: "1C3557", 2: "3A6090", 3: "6B8EAF" };
  const fgColors = { 1: "FFFFFF", 2: "FFFFFF", 3: "FFFFFF" };
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      borders: noBorders,
      shading: { fill: bgColors[level], type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 200, right: 100 },
      width: { size: 9360, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({
        text, bold: true, size: sizes[level], font: "MS Gothic", color: fgColors[level]
      })] })]
    })] })]
  });
}

function spacer(lines = 1) {
  return Array.from({ length: lines }, () =>
    new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })
  );
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 22, font: "MS Gothic", ...opts })]
  });
}

function questionText(num, text) {
  return new Paragraph({
    spacing: { before: 120, after: 80 },
    children: [new TextRun({ text: `問${num}　${text}`, size: 22, font: "MS Gothic" })]
  });
}

function choiceRow(label, text) {
  return new Paragraph({
    spacing: { after: 60 },
    indent: { left: 480 },
    children: [new TextRun({ text: `${label}　${text}`, size: 22, font: "MS Gothic" })]
  });
}

function blankLine(label) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3600, 5760],
    rows: [new TableRow({ children: [
      new TableCell({
        borders: noBorders,
        margins: { top: 60, bottom: 60, left: 0, right: 200 },
        width: { size: 3600, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: label, size: 22, font: "MS Gothic" })] })]
      }),
      new TableCell({
        borders: { ...noBorders, bottom: thinBorder },
        margins: { top: 60, bottom: 60, left: 200, right: 0 },
        width: { size: 5760, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: "　", size: 22 })] })]
      }),
    ]})]
  });
}

function answerRow(q, a) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new TableRow({ children: [
    new TableCell({
      borders,
      shading: { fill: "EEF2F8", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 150, right: 150 },
      width: { size: 1440, type: WidthType.DXA },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: q, bold: true, size: 22, font: "MS Gothic" })] })]
    }),
    new TableCell({
      borders,
      margins: { top: 80, bottom: 80, left: 150, right: 150 },
      width: { size: 7920, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text: a, size: 22, font: "MS Gothic" })] })]
    }),
  ]});
}

// ────────────────────────────────────────────
// 問題用紙 コンテンツ
// ────────────────────────────────────────────
const questions = [

  // ── タイトルブロック ──
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      borders: noBorders,
      shading: { fill: "1C3557", type: ShadingType.CLEAR },
      margins: { top: 200, bottom: 200, left: 300, right: 300 },
      width: { size: 9360, type: WidthType.DXA },
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "20世紀前半の世界と日本", bold: true, size: 44, font: "MS Gothic", color: "C8A951" })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "歴史テスト　（100点満点）", size: 26, font: "MS Gothic", color: "DDDDDD" })] }),
      ]
    })] })]
  }),
  ...spacer(1),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [5000, 4360],
    rows: [new TableRow({ children: [
      new TableCell({
        borders: noBorders,
        width: { size: 5000, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 0, right: 0 },
        children: [new Paragraph({ children: [new TextRun({ text: "　", size: 22 })] })]
      }),
      new TableCell({
        borders: noBorders,
        width: { size: 4360, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 0, right: 0 },
        children: [new Paragraph({ children: [
          new TextRun({ text: "組　　　　番　　氏名：", size: 22, font: "MS Gothic" }),
        ]})]
      }),
    ]})]
  }),
  ...spacer(1),

  // ════════════════════════════════════════════
  // 第１問　選択問題（各2点×10問＝20点）
  // ════════════════════════════════════════════
  heading("第１問　選択問題　各2点　（計20点）"),
  ...spacer(1),
  bodyText("各問の（　）に入る最も適切なものをア～エから選び、記号で答えなさい。"),
  ...spacer(1),

  // Q1
  questionText(1, "第一次世界大戦の直接の引き金となった1914年の事件として正しいものはどれか。"),
  choiceRow("ア", "モロッコ事件"),
  choiceRow("イ", "サラエヴォ事件"),
  choiceRow("ウ", "クリミア戦争"),
  choiceRow("エ", "ベルリン会議"),
  ...spacer(1),

  // Q2
  questionText(2, "三国同盟に属していた国として正しいものはどれか。"),
  choiceRow("ア", "フランス"),
  choiceRow("イ", "イギリス"),
  choiceRow("ウ", "ドイツ"),
  choiceRow("エ", "ロシア"),
  ...spacer(1),

  // Q3
  questionText(3, "第一次世界大戦を長期化させた最大の要因として正しいものはどれか。"),
  choiceRow("ア", "核兵器が多数使用されたから"),
  choiceRow("イ", "機関銃と塹壕戦によって戦線が膠着したから"),
  choiceRow("ウ", "同盟国が少なく孤立したから"),
  choiceRow("エ", "戦争が海上のみで行われたから"),
  ...spacer(1),

  // Q4
  questionText(4, "「総力戦」の説明として最も正しいものはどれか。"),
  choiceRow("ア", "軍人だけが参加し、短期間で決着がつく戦争"),
  choiceRow("イ", "核兵器を用いる戦争"),
  choiceRow("ウ", "国民全体・産業・経済が動員される戦争形態"),
  choiceRow("エ", "植民地の兵士だけで戦う戦争"),
  ...spacer(1),

  // Q5
  questionText(5, "1917年の十月革命でボリシェヴィキを率いた指導者は誰か。"),
  choiceRow("ア", "スターリン"),
  choiceRow("イ", "ケレンスキー"),
  choiceRow("ウ", "トロツキー"),
  choiceRow("エ", "レーニン"),
  ...spacer(1),

  // Q6
  questionText(6, "1920年代のアメリカについて述べた文のうち、誤っているものはどれか。"),
  choiceRow("ア", "大量生産・大量消費の社会が誕生した"),
  choiceRow("イ", "国際連盟に参加し国際協調を主導した"),
  choiceRow("ウ", "ジャズや映画が流行し「黄金の20年代」と呼ばれた"),
  choiceRow("エ", "禁酒法が施行された"),
  ...spacer(1),

  // Q7
  questionText(7, "ヴェルサイユ条約でドイツに課された賠償金の額として正しいものはどれか。"),
  choiceRow("ア", "約130億金マルク"),
  choiceRow("イ", "約320億金マルク"),
  choiceRow("ウ", "約1,320億金マルク"),
  choiceRow("エ", "約3,200億金マルク"),
  ...spacer(1),

  // Q8
  questionText(8, "1919年のパリ講和会議で人種差別撤廃提案を行った国はどれか。"),
  choiceRow("ア", "中国"),
  choiceRow("イ", "インド"),
  choiceRow("ウ", "日本"),
  choiceRow("エ", "オーストラリア"),
  ...spacer(1),

  // Q9
  questionText(9, "1918年に米価の暴騰をきっかけに全国に広がった民衆の暴動を何というか。"),
  choiceRow("ア", "護憲運動"),
  choiceRow("イ", "五・四運動"),
  choiceRow("ウ", "米騒動"),
  choiceRow("エ", "三・一独立運動"),
  ...spacer(1),

  // Q10
  questionText(10, "1925年の普通選挙法によって選挙権が認められたのは誰か。"),
  choiceRow("ア", "25歳以上の全国民（男女）"),
  choiceRow("イ", "30歳以上の男子"),
  choiceRow("ウ", "25歳以上の男子"),
  choiceRow("エ", "20歳以上の男子"),
  ...spacer(2),

  // ════════════════════════════════════════════
  // 第２問　語句記入問題（各2点×15問＝30点）
  // ════════════════════════════════════════════
  heading("第２問　語句記入問題　各2点　（計30点）"),
  ...spacer(1),
  bodyText("（　　　）に適切な語句を記入しなさい。"),
  ...spacer(1),

  bodyText("【第一次世界大戦】"),
  ...spacer(),
  blankLine("１．第一次世界大戦の発端となった1914年の暗殺事件を（　　　　　　　　　）事件という。"),
  ...spacer(),
  blankLine("２．フランス・イギリス・ロシアが結んだ同盟関係を（　　　　　　　　　）という。"),
  ...spacer(),
  blankLine("３．機関銃の普及によって防御が優位となり、両軍が堀を掘って向き合う（　　　　　　　　　）戦という戦い方が広まった。"),
  ...spacer(),
  blankLine("４．軍人だけでなく国民・産業・経済全体が動員される戦争形態を（　　　　　　　　　）という。"),
  ...spacer(1),

  bodyText("【ロシア革命とアメリカ】"),
  ...spacer(),
  blankLine("５．1917年、ロマノフ王朝が崩壊した革命を（　　　　　　　　　）という（暦法に従い「三月革命」とも呼ばれる）。"),
  ...spacer(),
  blankLine("６．レーニンが率い、十月革命で権力を握った党を（　　　　　　　　　）という。"),
  ...spacer(),
  blankLine("７．1922年に成立した世界初の社会主義国家の正式名称を（　　　　　　　　　）という（略称ソ連）。"),
  ...spacer(),
  blankLine("８．ウィルソン大統領の「14か条」に含まれる、各民族が自らの国家の形を決める権利を（　　　　　　　　　）という。"),
  ...spacer(1),

  bodyText("【ヴェルサイユ体制】"),
  ...spacer(),
  blankLine("９．1919年に結ばれた第一次大戦の講和条約を（　　　　　　　　　）条約という。"),
  ...spacer(),
  blankLine("10．ヴェルサイユ条約に基づいて設立された国際平和機関を（　　　　　　　　　）という。"),
  ...spacer(1),

  bodyText("【日本の大戦景気と大正デモクラシー】"),
  ...spacer(),
  blankLine("11．第一次大戦中に日本が欧州向け物資の供給役となって経済が急成長したことを（　　　　　　　　　）という。"),
  ...spacer(),
  blankLine("12．大戦景気で急に大富豪となった新興資本家を（　　　　　　　　　）という。"),
  ...spacer(),
  blankLine("13．1918年、米価の高騰に怒った民衆が全国で起こした暴動を（　　　　　　　　　）という。"),
  ...spacer(),
  blankLine("14．吉野作造が唱えた、民意を政治に反映すべきとする考え方を（　　　　　　　　　）という。"),
  ...spacer(),
  blankLine("15．1925年に普通選挙法と同年制定された、社会主義運動・国体変革を取り締まる法律を（　　　　　　　　　）という。"),
  ...spacer(2),

  // ════════════════════════════════════════════
  // 第３問　短答問題（各5点×6問＝30点）
  // ════════════════════════════════════════════
  heading("第３問　短答問題　各5点　（計30点）"),
  ...spacer(1),
  bodyText("各問について、2〜4文程度で説明しなさい。"),
  ...spacer(1),

  bodyText("問１　サラエヴォ事件が、なぜヨーロッパ全体を巻き込む大戦争に発展したのか。「同盟」という語を使って説明しなさい。（5点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 4 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(1),

  bodyText("問２　ロシア革命の結果、ソ連では「平等」は実現されたか。また「自由」はどうなったか説明しなさい。（5点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 4 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(1),

  bodyText("問３　ヴェルサイユ条約がドイツにとって非常に厳しい内容であったのはなぜか。具体的な内容を挙げて説明しなさい。（5点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 4 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(1),

  bodyText("問４　「大戦景気」はなぜ起きたのか。第一次世界大戦と日本の関係を踏まえて説明しなさい。（5点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 4 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(1),

  bodyText("問５　普通選挙法（1925年）の内容とその意義を説明しなさい。（5点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 4 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(1),

  bodyText("問６　日本が人種差別撤廃提案を行った経緯と、その結果について説明しなさい。（5点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 4 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(2),

  // ════════════════════════════════════════════
  // 第４問　記述問題（各10点×2問＝20点）
  // ════════════════════════════════════════════
  heading("第４問　記述問題　各10点　（計20点）"),
  ...spacer(1),
  bodyText("各問について、200字以内で自分の考えを述べなさい。"),
  ...spacer(1),

  bodyText("問１　第一次世界大戦が「総力戦」と呼ばれる理由を、新兵器の登場と関連づけながら述べなさい。（10点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 8 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),
  ...spacer(1),

  bodyText("問２　「普通選挙法」と「治安維持法」が同じ1925年に成立したことについて、あなたはどのように考えるか。両方の法律の内容に触れながら述べなさい。（10点）"),
  new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "　", size: 22 })] }),
  ...Array.from({ length: 8 }, () => new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
    children: [new TextRun({ text: "　", size: 28 })]
  })),

];

// ────────────────────────────────────────────
// 解答・解説コンテンツ（改ページ後）
// ────────────────────────────────────────────
const answers = [

  new Paragraph({ pageBreakBefore: true, children: [new TextRun({ text: "", size: 22 })] }),

  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      borders: noBorders,
      shading: { fill: "2C5F2D", type: ShadingType.CLEAR },
      margins: { top: 180, bottom: 180, left: 300, right: 300 },
      width: { size: 9360, type: WidthType.DXA },
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "解答・採点基準", bold: true, size: 40, font: "MS Gothic", color: "FFFFFF" })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "20世紀前半の世界と日本", size: 24, font: "MS Gothic", color: "DDEECC" })] }),
      ]
    })] })]
  }),
  ...spacer(2),

  // ── 第１問 選択 ──
  heading("第１問　選択問題　解答"),
  ...spacer(1),

  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1440, 7920],
    rows: [
      answerRow("問１", "イ　サラエヴォ事件（1914年6月、オーストリア皇太子夫妻がセルビア人青年に暗殺）"),
      answerRow("問２", "ウ　ドイツ（ドイツ・オーストリア＝ハンガリー・イタリアが三国同盟を結んでいた）"),
      answerRow("問３", "イ　機関銃と塹壕戦によって戦線が膠着したから"),
      answerRow("問４", "ウ　国民全体・産業・経済が動員される戦争形態"),
      answerRow("問５", "エ　レーニン（ボリシェヴィキを率いてソヴィエト政権を樹立）"),
      answerRow("問６", "イ　国際連盟に参加し国際協調を主導した ← 誤り（米国は国際連盟に不参加・孤立主義）"),
      answerRow("問７", "ウ　約1,320億金マルク（天文学的な額でドイツ経済を圧迫）"),
      answerRow("問８", "ウ　日本（全権・牧野伸顕が提案、多数が賛成したがウィルソンが否決）"),
      answerRow("問９", "ウ　米騒動（富山の漁村女性の抗議が全国70万人の暴動に発展）"),
      answerRow("問10", "ウ　25歳以上の男子（女性は対象外。女性参政権は1945年まで待つ）"),
    ]
  }),
  ...spacer(2),

  // ── 第２問 語句 ──
  heading("第２問　語句記入問題　解答"),
  ...spacer(1),

  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1440, 7920],
    rows: [
      answerRow("１", "サラエヴォ（バルカンは「ヨーロッパの火薬庫」と呼ばれた）"),
      answerRow("２", "三国協商（英・仏・露。対する三国同盟は独・墺・伊）"),
      answerRow("３", "塹壕（ざんごう）戦"),
      answerRow("４", "総力戦"),
      answerRow("５", "二月革命（三月革命）"),
      answerRow("６", "ボリシェヴィキ"),
      answerRow("７", "ソヴィエト社会主義共和国連邦（ソ連）"),
      answerRow("８", "民族自決"),
      answerRow("９", "ヴェルサイユ条約"),
      answerRow("10", "国際連盟"),
      answerRow("11", "大戦景気"),
      answerRow("12", "成金（なりきん）"),
      answerRow("13", "米騒動"),
      answerRow("14", "民本主義（みんぽんしゅぎ）"),
      answerRow("15", "治安維持法"),
    ]
  }),
  ...spacer(2),

  // ── 第３問 短答 ──
  heading("第３問　短答問題　採点基準"),
  ...spacer(1),

  bodyText("【問１　5点】サラエヴォ事件から大戦への拡大（同盟について言及があること）", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 120 }, children: [
    new TextRun({ text: "模範解答：", bold: true, size: 22, font: "MS Gothic" }),
    new TextRun({ text: "ヨーロッパ諸国は三国同盟・三国協商という同盟関係で結ばれていた。オーストリアがセルビアに宣戦すると、各国が条約上の義務に基づいて次々と参戦し、一地域の紛争が世界規模の大戦に拡大した。", size: 22, font: "MS Gothic" }),
  ]}),
  bodyText("採点のポイント：①同盟の存在に触れている　②連鎖的な参戦を説明している", { color: "1C3557" }),
  ...spacer(1),

  bodyText("【問２　5点】ロシア革命後の「平等」と「自由」", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 120 }, children: [
    new TextRun({ text: "模範解答：", bold: true, size: 22, font: "MS Gothic" }),
    new TextRun({ text: "ボリシェヴィキが権力を握り、私有財産の廃止・計画経済の導入によって「平等」を目指した。しかし一党独裁体制が強化され、反対派への弾圧や言論統制が行われ、個人の自由や政治的権利は大きく制限された。", size: 22, font: "MS Gothic" }),
  ]}),
  bodyText("採点のポイント：①平等（社会主義政策）に触れている　②自由の喪失について述べている", { color: "1C3557" }),
  ...spacer(1),

  bodyText("【問３　5点】ヴェルサイユ条約の内容とドイツへの影響", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 120 }, children: [
    new TextRun({ text: "模範解答：", bold: true, size: 22, font: "MS Gothic" }),
    new TextRun({ text: "ドイツには全植民地没収・領土縮小・軍備制限に加え、1,320億金マルクという巨額の賠償金が課された。これにより経済が壊滅し、ハイパーインフレや失業が続いた。国民の屈辱感と怒りが高まり、後のナチズム台頭の温床となった。", size: 22, font: "MS Gothic" }),
  ]}),
  bodyText("採点のポイント：①賠償金など具体的内容に触れている　②ドイツへの経済的・社会的影響を述べている", { color: "1C3557" }),
  ...spacer(1),

  bodyText("【問４　5点】大戦景気の要因", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 120 }, children: [
    new TextRun({ text: "模範解答：", bold: true, size: 22, font: "MS Gothic" }),
    new TextRun({ text: "第一次世界大戦でヨーロッパが主要な戦場となったため、欧州諸国は物資生産に手が回らなくなった。日本はアジアや欧州向けに物資・工業品（造船・化学・鉄鋼など）を大量に輸出する役割を担い、貿易黒字が急増して経済が急成長した。", size: 22, font: "MS Gothic" }),
  ]}),
  bodyText("採点のポイント：①欧州が戦場になったことで日本の輸出が増えた因果関係を説明している", { color: "1C3557" }),
  ...spacer(1),

  bodyText("【問５　5点】普通選挙法の内容と意義", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 120 }, children: [
    new TextRun({ text: "模範解答：", bold: true, size: 22, font: "MS Gothic" }),
    new TextRun({ text: "それまでの納税額による制限選挙を撤廃し、25歳以上の男子全員に選挙権を認めた法律。有権者数が約300万人から約1,240万人に拡大し、労働者や農民が初めて政治に参加できるようになった。大正デモクラシーの一つの到達点であった。", size: 22, font: "MS Gothic" }),
  ]}),
  bodyText("採点のポイント：①内容（25歳以上の男子）が正確　②制限選挙との違い・拡大の意義を述べている", { color: "1C3557" }),
  ...spacer(1),

  bodyText("【問６　5点】人種差別撤廃提案の経緯と結果", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 120 }, children: [
    new TextRun({ text: "模範解答：", bold: true, size: 22, font: "MS Gothic" }),
    new TextRun({ text: "日本全権の牧野伸顕が1919年のパリ講和会議で、国際連盟規約に人種差別撤廃の明記を提案した。投票では多数が賛成したが、議長のウィルソンが「全会一致が必要」として否決。英・豪・米が自国の有色人種差別政策と矛盾するとして反対したためであった。", size: 22, font: "MS Gothic" }),
  ]}),
  bodyText("採点のポイント：①提案者（日本/牧野）に触れている　②否決された経緯と理由を説明している", { color: "1C3557" }),
  ...spacer(2),

  // ── 第４問 記述 ──
  heading("第４問　記述問題　採点基準"),
  ...spacer(1),

  bodyText("【問１　10点】第一次世界大戦と総力戦・新兵器", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 80 }, children: [
    new TextRun({ text: "模範解答（例）：", bold: true, size: 22, font: "MS Gothic" }),
  ]}),
  new Paragraph({ spacing: { after: 120 }, children: [
    new TextRun({ text: "戦車・毒ガス・飛行機・潜水艦などの新兵器が登場したが、機関銃の普及により防御側が圧倒的に有利となり、両軍が塹壕を掘って向き合う塹壕戦が続いて戦線が膠着した。戦争が長期化するにつれ、軍需物資・食料・労働力を確保するため国民全体・産業・経済・女性労働まで動員されるようになった。これが「総力戦」であり、国家の総力が戦争に注ぎ込まれることで、史上最大の被害（死者約1,000万人）をもたらした。", size: 22, font: "MS Gothic" })
  ]}),

  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1440, 7920],
    rows: [
      answerRow("A（10点）", "新兵器と塹壕戦の長期化、総力戦の仕組みを正確に関連づけて述べている"),
      answerRow("B（7点）", "新兵器または総力戦のどちらかに触れているが、関連づけが不十分"),
      answerRow("C（4点）", "新兵器か総力戦の一方のみ述べている"),
      answerRow("D（0点）", "的外れな内容、または未記入"),
    ]
  }),
  ...spacer(2),

  bodyText("【問２　10点】普通選挙法と治安維持法の同年成立についての考察", { bold: true }),
  new Paragraph({ spacing: { before: 60, after: 80 }, children: [
    new TextRun({ text: "採点の観点：", bold: true, size: 22, font: "MS Gothic" }),
  ]}),
  new Paragraph({ spacing: { after: 120 }, children: [
    new TextRun({ text: "両法の内容を正確に把握した上で、自分の意見・考察が論拠とともに述べられているかを評価する。解答の方向性は問わない（「アメとムチ」「民主主義の限界」「時代の矛盾」など、根拠があれば可）。", size: 22, font: "MS Gothic" })
  ]}),

  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1440, 7920],
    rows: [
      answerRow("A（10点）", "両法の内容が正確で、自分の考えが論拠とともに200字以内で述べられている"),
      answerRow("B（7点）", "両法の内容に触れているが、考察・論拠がやや不十分"),
      answerRow("C（4点）", "内容説明にとどまり、自分の考えがほとんど述べられていない"),
      answerRow("D（0点）", "内容の誤り・的外れ・未記入"),
    ]
  }),
  ...spacer(2),

  // ── 点数集計表 ──
  heading("得点集計"),
  ...spacer(1),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2340, 2340, 2340, 2340],
    rows: [
      new TableRow({ children: ["第１問（/20）","第２問（/30）","第３問（/30）","第４問（/20）"].map((t, i) => new TableCell({
        borders: thinBorders,
        shading: { fill: "1C3557", type: ShadingType.CLEAR },
        margins: { top: 100, bottom: 100, left: 150, right: 150 },
        width: { size: 2340, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: t, bold: true, size: 22, font: "MS Gothic", color: "FFFFFF" })] })]
      })) }),
      new TableRow({ children: Array.from({length:4}, () => new TableCell({
        borders: thinBorders,
        margins: { top: 200, bottom: 200, left: 150, right: 150 },
        width: { size: 2340, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "　", size: 28 })] })]
      })) }),
    ]
  }),
  ...spacer(1),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [7020, 2340],
    rows: [
      new TableRow({ children: [
        new TableCell({
          borders: thinBorders,
          shading: { fill: "EEF2F8", type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 150, right: 150 },
          width: { size: 7020, type: WidthType.DXA },
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "合　計", bold: true, size: 24, font: "MS Gothic" })] })]
        }),
        new TableCell({
          borders: thinBorders,
          shading: { fill: "EEF2F8", type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 150, right: 150 },
          width: { size: 2340, type: WidthType.DXA },
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "　　／100", bold: true, size: 26, font: "MS Gothic" })] })]
        }),
      ]}),
    ]
  }),
];

// ────────────────────────────────────────────
// ドキュメント生成
// ────────────────────────────────────────────
const doc = new Document({
  numbering: { config: [] },
  styles: {
    default: { document: { run: { font: "MS Gothic", size: 22 } } },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } // 2cm margins
      }
    },
    children: [...questions, ...answers]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("C:/Users/shondo/Desktop/agent_project/history_test.docx", buffer);
  console.log("Done: history_test.docx");
}).catch(err => console.error(err));
