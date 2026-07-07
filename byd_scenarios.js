const pptxgen = require("pptxgenjs");

// ============================================================
// BYD 次なる進出先シナリオ分析
// ============================================================
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "経営企画部";
pres.title = "BYD 次なる進出先シナリオ分析";

const C = {
  navy:     "1E2761",
  blue:     "2E5EAA",
  iceblue:  "CADCFC",
  red:      "C0392B",
  amber:    "E67E22",
  green:    "27AE60",
  white:    "FFFFFF",
  offwhite: "F7F8FC",
  gray:     "64748B",
  darkgray: "334155",
  lightgray:"E2E8F0",
  teal:     "0891B2",
};

function ms() { return { type:"outer", blur:7, offset:2, angle:135, color:"000000", opacity:0.10 }; }

// スコア表示・色定義
const SYM = { 5:"◎", 4:"○", 3:"△", 2:"▲", 1:"×" };
const SFILL = { 5:"1A7F4B", 4:"1D4ED8", 3:"B45309", 2:"D97706", 1:"B91C1C" };
const STEXT = { 5:"FFFFFF", 4:"FFFFFF", 3:"FFFFFF", 2:"FFFFFF", 1:"FFFFFF" };

// ============================================================
// スライド 1: 表紙
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0, w:0.22, h:5.625,
    fill:{color:C.amber}, line:{color:C.amber}
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.22, y:0, w:9.78, h:0.05,
    fill:{color:C.iceblue}, line:{color:C.iceblue}
  });

  s.addText("BYD 次なる進出先シナリオ分析", {
    x:0.6, y:0.9, w:8.8, h:0.9,
    fontSize:38, bold:true, color:C.white, fontFace:"Meiryo", margin:0
  });
  s.addText("6つの論点による優先国スコアリング", {
    x:0.6, y:1.9, w:8.8, h:0.6,
    fontSize:20, color:C.iceblue, fontFace:"Meiryo", margin:0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x:0.6, y:2.7, w:3.5, h:0.04,
    fill:{color:C.amber}, line:{color:C.amber}
  });

  const pts = [
    "論点①：関税・貿易障壁の低さ（ユーザー提示）",
    "論点②：BEV普及を急ぐ政府・首脳の意向（ユーザー提示）",
    "論点③：現地資本OEM委託先の存在（ユーザー提示）",
    "論点④：EU関税迂回路としての地政学価値（追加）",
    "論点⑤：右ハンドル輸出ハブ戦略（追加）",
    "論点⑥：地政学的アライメント・BRI（追加）",
  ];
  s.addText(pts.map((p,i)=>({
    text:p, options:{bullet:true, breakLine:i<pts.length-1, paraSpaceAfter:4}
  })), {
    x:0.6, y:2.85, w:8.8, h:1.85,
    fontSize:12, color:C.iceblue, fontFace:"Meiryo", valign:"top"
  });

  s.addText("2026年6月　経営企画部", {
    x:0.6, y:5.15, w:8.8, h:0.35,
    fontSize:11, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 2: 分析フレームワーク
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("分析フレームワーク：6つの評価論点", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  const items = [
    { num:"①", title:"関税・貿易障壁", body:"中国からの輸出・現地生産品に対する輸入関税率。FTA（ASEAN-中国・EU等）による優遇措置。反ダンピング圧力の有無。", color:C.blue },
    { num:"②", title:"BEV普及を推進する政府意向", body:"首脳・閣僚レベルのEV宣言。国家EV目標年（2030・2035）。政府フリート調達実績。補助金・減税策の整備状況。", color:C.green },
    { num:"③", title:"現地資本OEM委託先", body:"BYDの依頼に応じて組立生産できる現地大手財閥・産業グループの存在。HUBCO(パキスタン)・Sime Motors(マレーシア)が先例。", color:C.amber },
    { num:"④", title:"EU関税迂回路【追加】", body:"中国製EVへのEU追加関税（27〜35%）を回避するため、EU-FTA国（トルコ・モロッコ等）に工場を置き欧州向けを生産する戦略価値。", color:C.red },
    { num:"⑤", title:"右ハンドル輸出ハブ【追加】", body:"パキスタン工場がバングラデシュ・スリランカ・アフリカ右ハンドル市場向け輸出拠点となるモデルの展開可能性。低コスト組立→近隣輸出の経済性。", color:C.teal },
    { num:"⑥", title:"地政学アライメント【追加】", body:"BRI（一帯一路）・CPEC・上海協力機構（SCO）加盟国は中国企業への投資障壁が低い。政治リスクの逓減がBYD進出の背景要因。", color:C.navy },
  ];

  items.forEach((item, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.35 + col * 3.15;
    const y = 1.0 + row * 2.15;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:3.0, h:1.95,
      fill:{color:C.white}, line:{color:C.lightgray, pt:1},
      shadow: ms()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:3.0, h:0.08,
      fill:{color:item.color}, line:{color:item.color}
    });
    s.addText(item.num + "  " + item.title, {
      x:x+0.12, y:y+0.12, w:2.76, h:0.38,
      fontSize:13, bold:true, color:item.color, fontFace:"Meiryo", margin:0
    });
    s.addText(item.body, {
      x:x+0.12, y:y+0.52, w:2.76, h:1.35,
      fontSize:10.5, color:C.darkgray, fontFace:"Meiryo", margin:0, valign:"top"
    });
  });
}

// ============================================================
// スライド 3: BYD海外展開の現状（確認済み拠点）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("BYD海外製造拠点の現状（2026年6月時点）", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  s.addText("次の分析は、これら「確認済み拠点」を除いた「次の候補国」を対象とする", {
    x:0.4, y:0.82, w:9.2, h:0.35,
    fontSize:12, color:C.gray, fontFace:"Meiryo", margin:0, italic:true
  });

  const regions = [
    {
      region:"東南アジア",
      color: C.green,
      plants:[
        { country:"タイ（ラヨーン）", status:"稼働中", cap:"15万台/年", partner:"100%BYD" },
        { country:"インドネシア（スバン）", status:"建設中・2025年完成予定", cap:"15万台/年", partner:"100%BYD 投資$13億" },
        { country:"マレーシア（タンジュンマリム）", status:"CKD 2026年開始予定", cap:"未公表", partner:"Sime Motors（現地資本）" },
      ]
    },
    {
      region:"南アジア・中央アジア",
      color: C.amber,
      plants:[
        { country:"パキスタン（カラチ近郊）", status:"建設開始 2026年7月稼働予定", cap:"2.5万台/年（初期）", partner:"Mega Motor / HUBCO（現地資本）" },
        { country:"ウズベキスタン", status:"稼働中", cap:"未公表（PHEV2モデル）", partner:"現地パートナーあり" },
      ]
    },
    {
      region:"欧州・中東欧",
      color: C.blue,
      plants:[
        { country:"ハンガリー（セゲド）", status:"試験生産開始 2026年上半期", cap:"15万台/年", partner:"100%BYD" },
        { country:"トルコ（マニサ県）", status:"計画中・不確実", cap:"15万台/年（計画）", partner:"100%BYD 投資$10億（進捗遅延報告あり）" },
      ]
    },
    {
      region:"中南米",
      color: C.teal,
      plants:[
        { country:"ブラジル（カマサリ）", status:"建設中", cap:"15万台/年", partner:"旧フォード工場転用" },
      ]
    },
  ];

  const tableData = [
    ["地域", "国・都市", "稼働状況", "規模", "資本・パートナー"],
    ["東南アジア", "タイ（ラヨーン）",         "稼働中",            "15万台/年",     "100%BYD"],
    ["",           "インドネシア（スバン）",    "建設中・2025年末完工","15万台/年",    "100%BYD（投資$13億）"],
    ["",           "マレーシア（タンジュンマリム）","CKD 2026年開始予定","未公表",     "Sime Motors（現地資本）"],
    ["南・中央アジア","パキスタン（カラチ近郊）","2026年7月稼働予定","2.5万台（初期）","Mega Motor / HUBCO（現地資本）"],
    ["",           "ウズベキスタン",            "稼働中",            "未公表（PHEV）", "現地パートナーあり"],
    ["欧州・中東欧","ハンガリー（セゲド）",     "試験生産中（2026年上半期）","15万台/年","100%BYD"],
    ["",           "トルコ（マニサ県）",        "計画中・進捗遅延あり","15万台/年（計画）","100%BYD（$10億）"],
    ["中南米",     "ブラジル（カマサリ）",      "建設中",            "15万台/年",     "旧フォード工場転用"],
  ];

  s.addTable(tableData, {
    x:0.35, y:1.22, w:9.3, h:3.9,
    border:{pt:0.5, color:"D1D5DB"},
    fontFace:"Meiryo",
    colW:[1.35, 2.3, 1.85, 1.15, 2.65],
    rowH:0.43,
    fill:{color:C.white},
    color:C.darkgray,
    fontSize:9.5,
    align:"left",
    autoPage:false,
  });

  s.addText("出所：Caixin Global、CnEVPost、Automotive World（2025〜2026年）", {
    x:0.4, y:5.2, w:9.2, h:0.26,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 4: 論点① 関税・貿易環境
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("論点①　関税・貿易障壁の比較（候補国）", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  // Bar chart: tariff rates
  s.addChart(pres.charts.BAR, [{
    name:"中国製EV輸入関税率（%）",
    labels:["バングラデシュ", "ベトナム\n(ACFTA)", "フィリピン\n(ACFTA)", "モロッコ\n(BYD SKD)", "サウジアラビア\n(GCC)", "インド\n(フル輸入)", "南アフリカ\n(MFN)"],
    values:[15, 0, 0, 2.5, 5, 100, 25]
  }], {
    x:0.4, y:1.0, w:5.8, h:3.8,
    barDir:"bar",
    chartColors:["1A7F4B","1A7F4B","1A7F4B","1D4ED8","1D4ED8","B91C1C","B45309"],
    chartArea:{fill:{color:C.white}, roundedCorners:false},
    catAxisLabelColor:C.darkgray,
    valAxisLabelColor:C.darkgray,
    valGridLine:{color:C.lightgray, size:0.5},
    catGridLine:{style:"none"},
    showLegend:false,
    showValue:true,
    dataLabelFontSize:10,
    dataLabelColor:C.darkgray,
    valAxisMinVal:0,
    valAxisMaxVal:120,
  });

  // 右側解説
  const notes = [
    { country:"ベトナム・フィリピン", rate:"0%", note:"ASEAN-中国FTA（ACFTA）。中国製EVは原産地規則を満たせば関税免除。中国の最大武器。", color:C.green },
    { country:"サウジアラビア・UAE（GCC）", rate:"5%", note:"GCC統一関税。製造業の集積はないが、輸入コストは最低水準。EVへの優遇政策も追加あり。", color:C.blue },
    { country:"モロッコ", rate:"〜2.5%（SKD）", note:"EU-モロッコ連合協定により現地組立品はEU向け0%。中国からのCKD輸入も低率。EU迂回の要。", color:C.blue },
    { country:"インド", rate:"100〜110%", note:"最大の障壁。SKD組立（30%）かローカル生産のみ現実的。政治リスクも重なる。", color:C.red },
    { country:"南アフリカ", rate:"25%（MFN）", note:"中国との特別FTAなし。ただしAFCFTA（アフリカ大陸FTA）でのEV優遇は今後検討課題。", color:C.amber },
  ];

  notes.forEach((n, i) => {
    const y = 1.0 + i * 0.82;
    s.addShape(pres.shapes.RECTANGLE, {
      x:6.4, y, w:0.04, h:0.7,
      fill:{color:n.color}, line:{color:n.color}
    });
    s.addText(n.country + "　" + n.rate, {
      x:6.55, y:y+0.02, w:3.1, h:0.28,
      fontSize:11, bold:true, color:n.color, fontFace:"Meiryo", margin:0
    });
    s.addText(n.note, {
      x:6.55, y:y+0.3, w:3.1, h:0.38,
      fontSize:9.5, color:C.darkgray, fontFace:"Meiryo", margin:0, valign:"top"
    });
  });

  s.addText("出所：Fastmarkets EV Tariff Tracker 2024、ASEAN-China FTA、各国税務当局", {
    x:0.4, y:5.28, w:9.2, h:0.26,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 5: 論点② EV政策・政府の推進意欲
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("論点②　各国のEV政策・政府推進意欲", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  const countries = [
    {
      name:"サウジアラビア", leader:"MBS（皇太子）", score:"◎◎",
      policy:"Vision 2030でEV普及加速。「2035年までに新車販売の30%をEV/HEV」を目標。PIF（政府系ファンド）がLucidに$1Bを投資済み。BYDには官民レベルで熱烈招致。",
      color:C.green
    },
    {
      name:"インド", leader:"モディ首相", score:"◎◎",
      policy:"FAME-II補助金制度、PLI電池生産奨励金。テランガナ州がBYDに500エーカーを提供（2026年計画）。PM自らEV普及を旗振り。",
      color:C.green
    },
    {
      name:"フィリピン", leader:"マルコス大統領", score:"◎",
      policy:"EV産業開発法（2022年）制定。政府公用車のEV化義務化。2027年までに輸入EV税控除延長。マルコス大統領が2023・24年に習近平と会談、EV協力を明言。",
      color:C.green
    },
    {
      name:"モロッコ", leader:"ムハンマド6世国王", score:"○",
      policy:"Green Morocco Planと再生可能エネルギー52%目標（2030年）。国王主導の産業多角化。Gotion（中国）が$5.6B電池工場に投資。EV向け産業政策が整いつつある。",
      color:C.blue
    },
    {
      name:"南アフリカ", leader:"ラマポーザ大統領", score:"△",
      policy:"「Just Energy Transition Partnership」でEV転換を宣言。ただし政府のEV義務化は不明確。停電（ロードシェディング）が皮肉にも太陽光+自家充電でEV需要を押し上げ。",
      color:C.amber
    },
    {
      name:"バングラデシュ", leader:"ユヌス暫定首相", score:"△",
      policy:"三輪EV（リキシャ）普及は進む。乗用車EVは政策形成段階。2024年政変後の政策継続性に不確実性あり。",
      color:C.amber
    },
  ];

  countries.forEach((c, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.35 + col * 4.75;
    const y = 1.0 + row * 1.5;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.55, h:1.35,
      fill:{color:C.white}, line:{color:C.lightgray, pt:1},
      shadow:ms()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.55, h:0.07,
      fill:{color:c.color}, line:{color:c.color}
    });
    s.addText(c.name + "　" + c.score + "　" + c.leader, {
      x:x+0.12, y:y+0.1, w:4.3, h:0.32,
      fontSize:12, bold:true, color:c.color, fontFace:"Meiryo", margin:0
    });
    s.addText(c.policy, {
      x:x+0.12, y:y+0.42, w:4.3, h:0.88,
      fontSize:10, color:C.darkgray, fontFace:"Meiryo", margin:0, valign:"top"
    });
  });

  s.addText("出所：各国政府声明、Arabia News、Business Standard、Manila Bulletin（2024〜2026年）", {
    x:0.4, y:5.28, w:9.2, h:0.26,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 6: 論点③ 現地資本OEM委託先
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("論点③　現地資本OEM委託先の存在と先例", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  // 先例ボックス（上段）
  s.addText("BYD OEM委託の先例（既確定）", {
    x:0.4, y:0.9, w:9.2, h:0.35,
    fontSize:12, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  const examples = [
    { country:"マレーシア", partner:"Sime Motors\n（Sime Darby系・上場）", why:"政府が現地調達40%・輸出80%を条件として要求。BYDは条件と折衝中。", color:C.blue },
    { country:"パキスタン", partner:"Mega Motor / HUBCO\n（電力大手・現地上場）", why:"CPECの文脈で中国側と交渉実績のある財閥。資金力・政府コネを持つ。", color:C.amber },
  ];
  examples.forEach((e, i) => {
    const x = 0.4 + i * 4.7;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.25, w:4.5, h:0.72,
      fill:{color:e.color}, line:{color:e.color}, shadow:ms()
    });
    s.addText(e.country + "：" + e.partner, {
      x:x+0.15, y:1.27, w:4.2, h:0.32,
      fontSize:12, bold:true, color:C.white, fontFace:"Meiryo", margin:0
    });
    s.addText(e.why, {
      x:x+0.15, y:1.59, w:4.2, h:0.35,
      fontSize:9.5, color:C.white, fontFace:"Meiryo", margin:0, valign:"top"
    });
  });

  // 候補国別テーブル（下段）
  s.addText("候補国別：現地OEM委託先の評価", {
    x:0.4, y:2.04, w:9.2, h:0.28,
    fontSize:12, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  const oems = [
    ["国","候補企業","特徴（短評）","評価"],
    ["サウジアラビア","PIF / SABIC","資金力最大だが製造経験なし。NEOM新都市との連携が鍵","△ 資金あり・経験なし"],
    ["フィリピン","Ayala Corporation","既存BYDディストリビュータ。多角化財閥でCKD実績あり","○ 最も現実的"],
    ["インド","Megha Engineering","2023年MOU後、政府が安保審査で難色。代替先を模索中","▲ 政治障壁"],
    ["南アフリカ","Motus / Imperial Holdings","南ア最大の自動車流通グループ。製造参入意欲は未確認","△ 流通○・製造△"],
    ["モロッコ","ONA/SNI系列 or 欧州工場活用","RenaultがTanger工場保有。地場財閥の参加意欲は不明","△ 欧州資本が先行"],
    ["バングラデシュ","Walton Hi-Tech","冷蔵庫・バイク生産実績あり。EV4輪は未経験","▲〜△ 技術的課題"],
  ];

  s.addTable(oems, {
    x:0.4, y:2.36, w:9.2, h:2.52,
    border:{pt:0.5, color:"D1D5DB"},
    fontFace:"Meiryo",
    colW:[1.55, 1.95, 3.75, 1.95],
    rowH:0.36,
    fill:{color:C.white},
    color:C.darkgray,
    fontSize:9.5,
    align:"left",
    autoPage:false,
  });

  s.addText("出所：AutomobileWorld、Dawn（Pakistan）、Automotive World Malaysia、各社IR情報", {
    x:0.4, y:4.95, w:9.2, h:0.26,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 7: 追加論点A EU関税迂回路
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("追加論点④　EU関税迂回路としての戦略価値", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  // ロジック図（テキスト + シェイプ）
  // 中国直輸出 → EU: 27-35%
  // 中国→ハンガリー工場→EU: 0%
  // 中国CKD→トルコ工場→EU: 0%
  // 中国CKD→モロッコ工場→EU: 0%

  const flows = [
    { from:"中国から\n直接輸出", arrow:"→", to:"EU", tariff:"関税27〜35%\n（EV追加課税）", color:C.red },
    { from:"中国CKD\n→ハンガリー", arrow:"→", to:"EU", tariff:"関税0%\n（EU域内）", color:C.green },
    { from:"中国CKD\n→トルコ", arrow:"→", to:"EU", tariff:"関税0%\n（EU関税同盟）", color:C.green },
    { from:"中国CKD\n→モロッコ", arrow:"→", to:"EU", tariff:"関税0%\n（EU-モロッコFTA）", color:C.blue },
  ];

  flows.forEach((f, i) => {
    const y = 1.05 + i * 1.08;
    // FROM box
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.4, y, w:2.2, h:0.8,
      fill:{color:i===0?C.red:C.navy}, line:{color:i===0?C.red:C.navy},
      shadow:ms()
    });
    s.addText(f.from, {
      x:0.4, y, w:2.2, h:0.8,
      fontSize:11, bold:true, color:C.white, fontFace:"Meiryo",
      align:"center", valign:"middle", margin:0
    });
    // Arrow
    s.addShape(pres.shapes.RECTANGLE, {
      x:2.65, y:y+0.37, w:1.3, h:0.05,
      fill:{color:C.lightgray}, line:{color:C.lightgray}
    });
    // TARIFF label
    s.addText(f.tariff, {
      x:2.6, y:y+0.04, w:1.4, h:0.35,
      fontSize:9.5, color:f.color, fontFace:"Meiryo",
      align:"center", bold:true, margin:0
    });
    // TO box
    s.addShape(pres.shapes.RECTANGLE, {
      x:4.05, y, w:1.2, h:0.8,
      fill:{color:f.color}, line:{color:f.color},
      shadow:ms()
    });
    s.addText("EU市場", {
      x:4.05, y, w:1.2, h:0.8,
      fontSize:11, bold:true, color:C.white, fontFace:"Meiryo",
      align:"center", valign:"middle", margin:0
    });
    // Commentary
    s.addText(i===0 ? "① 直接輸出：EU追加関税により競争力が著しく低下" :
              i===1 ? "② ハンガリー：試験生産開始（2026年上半期）。EU域内として扱われる" :
              i===2 ? "③ トルコ：EU関税同盟加盟。進捗遅延報告あり。最終的な欧州戦略の要" :
                      "④ モロッコ：EU-モロッコ連合協定で0%。Gotion電池工場も建設中。ダークホース",
    {
      x:5.4, y:y+0.1, w:4.2, h:0.65,
      fontSize:11, color:C.darkgray, fontFace:"Meiryo", margin:0, valign:"middle"
    });
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x:0.4, y:4.92, w:9.2, h:0.24,
    fill:{color:"FEF3C7"}, line:{color:"F59E0B", pt:0.5}
  });
  s.addText("⚠️  トルコの進捗遅延により、モロッコが「第2の欧州ゲートウェイ」として浮上している。中国のGotion電池工場投資もモロッコの戦略的価値を高める。",
  {
    x:0.55, y:4.94, w:9.0, h:0.2,
    fontSize:9.5, color:"92400E", fontFace:"Meiryo", margin:0, valign:"middle"
  });

  s.addText("出所：Electrive、Caixin Global、欧州委員会EV関税決定（2024/11）、EU-Morocco Association Agreement", {
    x:0.4, y:5.22, w:9.2, h:0.25,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 8: 追加論点B 右ハンドル輸出ハブ
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("追加論点⑤　右ハンドル輸出ハブ戦略（パキスタン軸）", {
    x:0.4, y:0.25, w:9.2, h:0.55,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  // Hub circle
  s.addShape(pres.shapes.OVAL, {
    x:3.8, y:1.6, w:2.4, h:1.5,
    fill:{color:C.amber}, line:{color:C.amber},
    shadow:ms()
  });
  s.addText("パキスタン\nカラチ工場\n（2026年〜）", {
    x:3.8, y:1.6, w:2.4, h:1.5,
    fontSize:12, bold:true, color:C.white, fontFace:"Meiryo",
    align:"center", valign:"middle", margin:0
  });

  // Spoke: 中国
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.55, y:2.25, w:1.5, h:0.55,
    fill:{color:C.navy}, line:{color:C.navy}, shadow:ms()
  });
  s.addText("中国\nCKD供給", {
    x:0.55, y:2.25, w:1.5, h:0.55,
    fontSize:10, color:C.white, fontFace:"Meiryo",
    align:"center", valign:"middle", margin:0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:2.1, y:2.47, w:1.7, h:0.04,
    fill:{color:C.lightgray}, line:{color:C.lightgray}
  });
  s.addText("CKDキット", {
    x:2.1, y:2.27, w:1.65, h:0.25,
    fontSize:9, color:C.gray, fontFace:"Meiryo",
    align:"center", margin:0
  });

  // Export markets (4 markets, stacked on right, no overflow note text)
  const exports = [
    { name:"バングラデシュ（175M人）", note:"南アジア最大の低所得国市場。右ハンドル。FTA優遇あり", x:6.4, y:0.82 },
    { name:"スリランカ（22M人）",     note:"経済危機後のEV需要。右ハンドル。中国との関係修復中",  x:6.4, y:1.75 },
    { name:"ケニア（57M人）",         note:"アフリカ東部ハブ。右ハンドル。BYDアフリカシェア35%",  x:6.4, y:2.68 },
    { name:"南アフリカ（65M人）",     note:"アフリカ最大の自動車市場。右ハンドル。BYD急成長中",  x:6.4, y:3.6 },
  ];

  exports.forEach((e) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:e.x, y:e.y, w:3.2, h:0.55,
      fill:{color:C.teal}, line:{color:C.teal}, shadow:ms()
    });
    s.addText(e.name, {
      x:e.x+0.1, y:e.y+0.03, w:3.0, h:0.28,
      fontSize:10.5, bold:true, color:C.white, fontFace:"Meiryo", margin:0
    });
    s.addText(e.note, {
      x:e.x+0.1, y:e.y+0.3, w:3.0, h:0.22,
      fontSize:8.5, color:C.white, fontFace:"Meiryo", margin:0
    });
  });

  // BYD Pakistan note
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.4, y:4.4, w:9.2, h:0.62,
    fill:{color:"EFF6FF"}, line:{color:C.blue, pt:0.5}
  });
  s.addText("パキスタン政府はカラチ工場をバングラデシュ・スリランカ・東アフリカ向け輸出拠点として位置づけることを奨励（財務相Aurangzeb発言、2025年7月）。低コスト組立→右ハンドル隣接国輸出というビジネスモデルは、BYDの負債制約下でも成立しうる最小投資型の海外展開パターン。",
  {
    x:0.55, y:4.43, w:9.0, h:0.55,
    fontSize:10, color:C.blue, fontFace:"Meiryo", margin:0, valign:"middle"
  });

  s.addText("出所：AnewZ（Pakistan 2025/7）、Dawn、EcofinAgency Africa 2025", {
    x:0.4, y:5.1, w:9.2, h:0.25,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 9: 追加論点C 地政学アライメント（BRI/CPEC）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("追加論点⑥　地政学的アライメント（BRI・CPEC・SCO）", {
    x:0.4, y:0.2, w:9.2, h:0.62,
    fontSize:22, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  s.addText("BYDの進出先は偶然でなく、中国の外交インフラ（BRI・CPEC・SCO）と高い相関がある", {
    x:0.4, y:0.82, w:9.2, h:0.3,
    fontSize:12, color:C.gray, fontFace:"Meiryo", margin:0, italic:true
  });

  const rows = [
    ["国","BRI加盟","CPEC","SCO/その他FTA","影響"],
    ["パキスタン","◎（主要投資先）","◎（$60B）","SCO正式加盟","政府・企業の対中ハードル最低。工場・インフラ支援あり"],
    ["ウズベキスタン","◎","—","SCO加盟","既にBYD工場稼働。旧ソ連圏で中国の影響力拡大中"],
    ["モロッコ","◎（2017年署名）","—","アラブ連盟","GotionがBYD電池工場を併設投資。連動した産業進出"],
    ["サウジアラビア","実質連携","—","アラブ連盟","2022年習近平訪問で包括戦略パートナーシップ締結"],
    ["フィリピン","◎","—","ASEAN-China FTA","マルコス大統領が中国と14協定締結（2023〜24年）"],
    ["インド","×（参加拒否）","▲（懐疑的）","SCO加盟","BRI不参加・国境紛争。中国投資に安保審査が必要"],
    ["南アフリカ","◎","—","BRICs","ANC政権は歴史的に親中。ブリクス議長国（2023年）"],
    ["バングラデシュ","◎","—","—","ハシナ前首相が親中路線。2024年政変後も維持傾向"],
    ["ベトナム","△（参加も競合）","—","ASEAN-China FTA","ASEAN内で中国との領土問題あり。経済協力は継続"],
  ];

  s.addTable(rows, {
    x:0.35, y:1.15, w:9.3, h:4.1,
    border:{pt:0.5, color:"D1D5DB"},
    fontFace:"Meiryo",
    colW:[1.5, 1.1, 0.9, 1.5, 4.3],
    rowH:0.43,
    fill:{color:C.white},
    color:C.darkgray,
    fontSize:9.5,
    align:"left",
    autoPage:false,
  });

  s.addText("出所：中国商務部BRI公式サイト、各国政府発表、SCMP、Global Times", {
    x:0.4, y:5.28, w:9.2, h:0.26,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 10: 総合スコアリングマトリクス
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("総合評価マトリクス（6論点 × 7候補国）", {
    x:0.4, y:0.22, w:9.2, h:0.5,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  // スコア凡例
  const legend = [
    {sym:"◎ 5点",fill:"1A7F4B"},{sym:"○ 4点",fill:"1D4ED8"},
    {sym:"△ 3点",fill:"B45309"},{sym:"▲ 2点",fill:"D97706"},
    {sym:"× 1点",fill:"B91C1C"},
  ];
  legend.forEach((l, i) => {
    const x = 0.4 + i * 1.8;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:0.77, w:0.3, h:0.22,
      fill:{color:l.fill}, line:{color:l.fill}
    });
    s.addText(l.sym, {
      x:x+0.34, y:0.77, w:1.3, h:0.22,
      fontSize:9, color:C.darkgray, fontFace:"Meiryo", margin:0
    });
  });

  // スコアデータ
  // 列: 国名 | ①貿易 | ②EV政策 | ③OEM先 | ④EU迂回 | ⑤右ハンドル | ⑥BRI | 合計 | 優先度
  const countries = [
    { name:"サウジアラビア", scores:[5,5,3,3,1,4] },  // 21
    { name:"モロッコ",       scores:[5,4,4,5,1,4] },  // 23
    { name:"フィリピン",     scores:[5,4,4,1,5,4] },  // 23
    { name:"南アフリカ",     scores:[3,3,4,1,5,4] },  // 20
    { name:"インド",         scores:[1,5,2,1,5,2] },  // 16
    { name:"バングラデシュ", scores:[4,3,3,1,5,4] },  // 20
    { name:"ベトナム",       scores:[5,3,2,1,5,3] },  // 19
  ];

  const colLabels = ["①貿易環境","②EV政策","③OEM先","④EU迂回","⑤右ハンドル","⑥BRI"];
  const fillMap = { 5:"1A7F4B", 4:"1D4ED8", 3:"B45309", 2:"D97706", 1:"B91C1C" };
  const symMap  = { 5:"◎", 4:"○", 3:"△", 2:"▲", 1:"×" };
  const rankMap = {
    "サウジアラビア": { rank:"A", color:"1A7F4B" },
    "モロッコ":       { rank:"A", color:"1A7F4B" },
    "フィリピン":     { rank:"A", color:"1A7F4B" },
    "南アフリカ":     { rank:"B", color:"1D4ED8" },
    "インド":         { rank:"B+ 難", color:"B45309" },
    "バングラデシュ": { rank:"B-", color:"1D4ED8" },
    "ベトナム":       { rank:"C+", color:"B45309" },
  };

  // ヘッダー行
  const headerY = 1.05;
  const colWidths = [1.5, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 0.65, 0.8];
  const startX = 0.35;
  const headers = ["候補国", ...colLabels, "合計", "優先度"];

  // ヘッダー背景
  s.addShape(pres.shapes.RECTANGLE, {
    x:startX, y:headerY, w:9.3, h:0.38,
    fill:{color:C.navy}, line:{color:C.navy}
  });
  let hx = startX;
  headers.forEach((h, i) => {
    s.addText(h, {
      x:hx, y:headerY, w:colWidths[i], h:0.38,
      fontSize:9, bold:true, color:C.white, fontFace:"Meiryo",
      align:"center", valign:"middle", margin:0
    });
    hx += colWidths[i];
  });

  // データ行
  countries.forEach((c, ri) => {
    const rowY = headerY + 0.38 + ri * 0.52;
    const total = c.scores.reduce((a,b)=>a+b, 0);
    const rm = rankMap[c.name];

    // 国名セル
    s.addShape(pres.shapes.RECTANGLE, {
      x:startX, y:rowY, w:colWidths[0], h:0.52,
      fill:{color:ri%2===0?"F8FAFC":C.white}, line:{color:C.lightgray, pt:0.5}
    });
    s.addText(c.name, {
      x:startX+0.05, y:rowY, w:colWidths[0]-0.05, h:0.52,
      fontSize:10, bold:true, color:C.darkgray, fontFace:"Meiryo",
      valign:"middle", margin:0
    });

    // スコアセル
    let cx = startX + colWidths[0];
    c.scores.forEach((sc, ci) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x:cx, y:rowY, w:colWidths[ci+1], h:0.52,
        fill:{color:fillMap[sc]}, line:{color:C.lightgray, pt:0.3}
      });
      s.addText(symMap[sc], {
        x:cx, y:rowY, w:colWidths[ci+1], h:0.52,
        fontSize:13, bold:true, color:"FFFFFF", fontFace:"Meiryo",
        align:"center", valign:"middle", margin:0
      });
      cx += colWidths[ci+1];
    });

    // 合計
    s.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:rowY, w:colWidths[7], h:0.52,
      fill:{color:C.darkgray}, line:{color:C.lightgray, pt:0.5}
    });
    s.addText(total + "/30", {
      x:cx, y:rowY, w:colWidths[7], h:0.52,
      fontSize:11, bold:true, color:C.white, fontFace:"Meiryo",
      align:"center", valign:"middle", margin:0
    });
    cx += colWidths[7];

    // 優先度
    s.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:rowY, w:colWidths[8], h:0.52,
      fill:{color:rm.color}, line:{color:C.lightgray, pt:0.5}
    });
    s.addText(rm.rank, {
      x:cx, y:rowY, w:colWidths[8], h:0.52,
      fontSize:9.5, bold:true, color:C.white, fontFace:"Meiryo",
      align:"center", valign:"middle", margin:0
    });
  });

  s.addText("注：各論点5点満点、合計30点。EU迂回価値のない国は①に低得点。インドは市場潜在性◎だが貿易・政治障壁で最低水準。", {
    x:0.4, y:5.28, w:9.2, h:0.26,
    fontSize:8.5, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 11: 最有力3市場の深掘り
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("最有力3市場の詳細分析（評価A）", {
    x:0.4, y:0.22, w:9.2, h:0.5,
    fontSize:26, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  const top3 = [
    {
      name:"サウジアラビア",
      sub:"スコア21/30　GCCハブ×Vision 2030",
      color: C.amber,
      upsides:[
        "GCC関税5%・欧米制裁リスクなし",
        "MBS主導のVision 2030で政府が積極招致",
        "BYDは既に3都市にショールーム展開・5,000台/年目標（2026年）",
        "PIF（政府系ファンド）が出資者として関与可能性",
        "GCC5カ国（ UAE・クウェート・カタール・バーレーン・オマーン）への波及効果",
      ],
      risks:[
        "製造経験のある現地OEMパートナーが存在しない",
        "現時点では輸入モデル主体（製造工場は未発表）",
        "猛暑・砂漠環境でのEVバッテリー性能問題",
      ]
    },
    {
      name:"モロッコ",
      sub:"23/30　EUゲートウェイ×電池エコシステム",
      color: C.blue,
      upsides:[
        "EU-モロッコ連合協定で製造品のEU輸出が関税0%",
        "中国Gotion High-Techが20GWhバッテリー工場を建設中（$5.6B投資）",
        "RenaultがTanger工場を運営（製造人材・インフラ活用可能）",
        "国王主導のGreen Morocco Plan・再エネ52%目標（2030）",
        "トルコ工場の遅延を受けた「第2EU迂回拠点」としての浮上",
      ],
      risks:[
        "地場OEM（自動車製造の現地資本）は限定的",
        "市場規模（38M人）が小さく投資回収に輸出前提が必要",
        "Renaultとの競合関係",
      ]
    },
    {
      name:"フィリピン",
      sub:"スコア23/30　ASEAN×Ayala×115M人",
      color: C.green,
      upsides:[
        "ASEAN-中国FTAで関税ほぼ0%",
        "EV産業開発法（2022）・輸入税控除・政府フリート義務化",
        "Ayala Corporationが既存のBYD正規ディストリビュータ（CKD転換が最短経路）",
        "マルコス大統領が習近平と2度会談、EVを明示的に協力議題に",
        "充電インフラ整備はBYDが共同投資する余地あり",
      ],
      risks:[
        "南シナ海領土問題が突発的な政治リスクを生む可能性",
        "充電インフラが現時点で極めて不足",
        "可処分所得が低く高額EVの普及に時間がかかる",
      ]
    },
  ];

  top3.forEach((m, i) => {
    const x = 0.35 + i * 3.15;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:0.85, w:3.0, h:4.65,
      fill:{color:C.white}, line:{color:m.color, pt:1.5},
      shadow:ms()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:0.85, w:3.0, h:0.6,
      fill:{color:m.color}, line:{color:m.color}
    });
    s.addText(m.name, {
      x:x+0.1, y:0.87, w:2.8, h:0.28,
      fontSize:14, bold:true, color:C.white, fontFace:"Meiryo", margin:0
    });
    s.addText(m.sub, {
      x:x+0.1, y:1.13, w:2.8, h:0.28,
      fontSize:9, color:C.white, fontFace:"Meiryo", margin:0
    });

    s.addText("【強み】", {
      x:x+0.1, y:1.52, w:2.8, h:0.28,
      fontSize:10, bold:true, color:m.color, fontFace:"Meiryo", margin:0
    });
    s.addText(m.upsides.map((u,j)=>({
      text:u, options:{bullet:true, breakLine:j<m.upsides.length-1, paraSpaceAfter:3}
    })), {
      x:x+0.1, y:1.8, w:2.8, h:2.0,
      fontSize:9.5, color:C.darkgray, fontFace:"Meiryo", valign:"top"
    });

    s.addText("【リスク】", {
      x:x+0.1, y:3.82, w:2.8, h:0.25,
      fontSize:10, bold:true, color:C.red, fontFace:"Meiryo", margin:0
    });
    s.addText(m.risks.map((r,j)=>({
      text:r, options:{bullet:true, breakLine:j<m.risks.length-1, paraSpaceAfter:2}
    })), {
      x:x+0.1, y:4.07, w:2.8, h:1.3,
      fontSize:9.5, color:C.darkgray, fontFace:"Meiryo", valign:"top"
    });
  });
}

// ============================================================
// スライド 12: OEM→自社工場への段階的移行パターン
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("補足：BYDの「段階的進出パターン」とOEM委託の位置づけ", {
    x:0.4, y:0.22, w:9.2, h:0.5,
    fontSize:22, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  // 3段階 timeline
  const stages = [
    {
      n:"STEP 1", title:"輸入販売\n＋現地ディストリビュータ",
      desc:"FTAを活用した低関税輸入。現地財閥・商社が輸入・販売を担当。BYDの資本負担は最小。",
      ex:"サウジ・南ア・フィリピン（現在）",
      color: C.blue
    },
    {
      n:"STEP 2", title:"CKD/SKD組立\n＋現地資本OEM",
      desc:"中国からCKDキットを輸出し、現地パートナーが組立。BYDの投資最小化・現地雇用創出・関税軽減を同時達成。",
      ex:"マレーシア（Sime）・パキスタン（HUBCO）",
      color: C.amber
    },
    {
      n:"STEP 3", title:"自社工場\n（100%BYD）",
      desc:"市場規模が正当化できる段階で独自工場を建設。このステップはBYDの負債制約と競合するため、大市場のみ実行。",
      ex:"タイ・ハンガリー・ブラジル・インドネシア",
      color: C.green
    },
  ];

  stages.forEach((st, i) => {
    const x = 0.35 + i * 3.15;
    // Arrow between stages
    if (i < 2) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x + 3.0, y:2.2, w:0.15, h:0.05,
        fill:{color:C.lightgray}, line:{color:C.lightgray}
      });
      s.addText("→", {
        x: x + 3.0, y:2.0, w:0.15, h:0.4,
        fontSize:20, color:C.lightgray, fontFace:"Meiryo",
        align:"center", margin:0
      });
    }
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.05, w:3.0, h:3.3,
      fill:{color:C.white}, line:{color:st.color, pt:1.5},
      shadow:ms()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.05, w:3.0, h:0.55,
      fill:{color:st.color}, line:{color:st.color}
    });
    s.addText(st.n + "　" + st.title, {
      x:x+0.1, y:1.07, w:2.8, h:0.52,
      fontSize:13, bold:true, color:C.white, fontFace:"Meiryo",
      align:"center", valign:"middle", margin:0
    });
    s.addText(st.desc, {
      x:x+0.12, y:1.65, w:2.76, h:1.7,
      fontSize:11.5, color:C.darkgray, fontFace:"Meiryo", margin:0, valign:"top"
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:x+0.1, y:3.35, w:2.8, h:0.02,
      fill:{color:C.lightgray}, line:{color:C.lightgray}
    });
    s.addText("実例：" + st.ex, {
      x:x+0.12, y:3.4, w:2.76, h:0.75,
      fontSize:10.5, color:st.color, fontFace:"Meiryo", margin:0, bold:true, valign:"top"
    });
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x:0.4, y:4.55, w:9.2, h:0.72,
    fill:{color:"FEF3C7"}, line:{color:"F59E0B", pt:0.5}
  });
  s.addText([
    {text:"⚠️  注目点：", options:{bold:true, color:"92400E"}},
    {text:"OEM委託（STEP 2）は一時的措置ではなく、BYDの負債制約が続く限り優先される戦略。ただし「現地OEMがBYDの支払い遅延に耐えられるか」が隠れたリスク。マレーシア・パキスタンの交渉難航がそれを示唆する。", options:{color:"92400E"}},
  ], {
    x:0.55, y:4.6, w:8.9, h:0.65,
    fontSize:11, fontFace:"Meiryo", margin:0, valign:"middle"
  });
}

// ============================================================
// スライド 13: 結論
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0, w:0.22, h:5.625,
    fill:{color:C.amber}, line:{color:C.amber}
  });

  s.addText("結論：次なる進出先の優先シナリオ", {
    x:0.55, y:0.3, w:9.0, h:0.6,
    fontSize:30, bold:true, color:C.white, fontFace:"Meiryo", margin:0
  });

  const concl = [
    {
      rank:"最優先", countries:"フィリピン・モロッコ",
      text:"ASEAN-中国FTA（関税ゼロ）×政府EV法×現地財閥OEM先の三拍子が揃う。フィリピンはAyala、モロッコはGotion電池との連動が鍵。特にモロッコはトルコ不確実性の受け皿としてEU迂回路の主役に浮上。",
      color: C.green
    },
    {
      rank:"並行優先", countries:"サウジアラビア（GCC）",
      text:"製造はSTEP 1（輸入販売）のまましばらく継続するが、Vision 2030×PIF資金があれば一気にSTEP 3（自社工場）に飛ぶシナリオも。GCC5カ国への波及効果が大きい。",
      color: C.amber
    },
    {
      rank:"中期注目", countries:"南アフリカ（アフリカHUB）",
      text:"アフリカ大陸全体への波及拠点。BYDはアフリカEVシェア35%を既に確保。南アでの製造が実現すれば、パキスタン軸（東アフリカ）との二極体制でアフリカを覆う。",
      color: C.teal
    },
    {
      rank:"高難度・長期", countries:"インド",
      text:"最大の潜在市場だが政治障壁（安保審査・BRI不参加・China skepticism）が続く。SKD経路で突破口を開く動きが2026年以降の最大の注目点。",
      color: C.red
    },
  ];

  concl.forEach((c, i) => {
    const y = 1.05 + i * 1.07;
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.5, y, w:0.08, h:0.85,
      fill:{color:c.color}, line:{color:c.color}
    });
    s.addText(c.rank + "　" + c.countries, {
      x:0.72, y:y+0.02, w:8.5, h:0.32,
      fontSize:14, bold:true, color:c.color, fontFace:"Meiryo", margin:0
    });
    s.addText(c.text, {
      x:0.72, y:y+0.35, w:8.5, h:0.52,
      fontSize:11, color:C.white, fontFace:"Meiryo", margin:0, valign:"top"
    });
  });

  s.addText("2026年6月　経営企画部", {
    x:0.55, y:5.22, w:9.0, h:0.3,
    fontSize:11, color:C.gray, fontFace:"Meiryo", margin:0
  });
}

// ============================================================
// スライド 14: BEV市場戦略マトリクス（バブルチャート）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  // ─ チャートエリア（LAYOUT_16x9: 10 x 5.625"）─
  const CX=1.35, CY=1.28, CW=7.2, CH=3.5;
  const CB=CY+CH; // 4.78
  const _px = g => CX + (g-0.8)/(5.2-0.8)*CW;
  // Y軸：平方根スケール（低普及帯を視覚的に広げる）
  const _py = p => CB - Math.sqrt(Math.max(0,p)/50)*CH;
  const qx=_px(3.0); // 成長3.0の位置
  const qy=_py(15);  // 普及率15%の位置（タイ14%を成長カテゴリに分類）

  // タイトル
  s.addText("BEV市場戦略マトリクス", {
    x:0.35, y:0.1, w:8.2, h:0.48,
    fontSize:22, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });
  s.addText("Y軸：BEV普及率（√スケール）　X軸：成長ポテンシャル（将来推計1〜5）　バブルサイズ：BYD販売台数　バブル色：BEV内BYDシェア", {
    x:0.35, y:0.59, w:9.0, h:0.2,
    fontSize:7.5, color:C.gray, fontFace:"Meiryo", margin:0
  });

  // 象限背景
  s.addShape(pres.shapes.RECTANGLE, { x:CX,  y:qy,  w:qx-CX,    h:CB-qy,  fill:{color:"E2E8F0"}, line:{type:"none"} }); // Q4
  s.addShape(pres.shapes.RECTANGLE, { x:qx,  y:qy,  w:CX+CW-qx, h:CB-qy,  fill:{color:"DBEAFE"}, line:{type:"none"} }); // Q3
  s.addShape(pres.shapes.RECTANGLE, { x:CX,  y:CY,  w:qx-CX,    h:qy-CY,  fill:{color:"FEF9C3"}, line:{type:"none"} }); // Q2
  s.addShape(pres.shapes.RECTANGLE, { x:qx,  y:CY,  w:CX+CW-qx, h:qy-CY,  fill:{color:"DCFCE7"}, line:{type:"none"} }); // Q1

  // チャートボーダー
  s.addShape(pres.shapes.RECTANGLE, { x:CX, y:CY, w:CW, h:CH, fill:{type:"none"}, line:{color:"94A3B8", pt:1} });

  // 象限区切り線（細いRECTANGLEで実線）
  s.addShape(pres.shapes.RECTANGLE, { x:CX,  y:qy-0.005, w:CW,   h:0.01, fill:{color:"6B7280"}, line:{type:"none"} });
  s.addShape(pres.shapes.RECTANGLE, { x:qx-0.005, y:CY, w:0.01, h:CH,   fill:{color:"6B7280"}, line:{type:"none"} });

  // Y軸グリッド＆ラベル（0,5,15,20,30,50%）
  for (const v of [0,5,15,20,30,50]) {
    const yy=_py(v);
    s.addShape(pres.shapes.RECTANGLE, { x:CX, y:yy-0.003, w:CW, h:0.006, fill:{color:"D1D5DB"}, line:{type:"none"} });
    s.addText(v+"%", { x:CX-0.62, y:yy-0.12, w:0.55, h:0.24, fontSize:8, color:C.gray, fontFace:"Meiryo", align:"right", margin:0 });
  }

  // X軸グリッド＆ラベル（1〜5）
  for (const v of [1,2,3,4,5]) {
    const xx=_px(v);
    s.addShape(pres.shapes.RECTANGLE, { x:xx-0.003, y:CY, w:0.006, h:CH, fill:{color:"D1D5DB"}, line:{type:"none"} });
    s.addText(String(v), { x:xx-0.2, y:CB+0.06, w:0.4, h:0.22, fontSize:8, color:C.gray, fontFace:"Meiryo", align:"center", margin:0 });
  }

  // 軸タイトル
  s.addText("← 成長ポテンシャル（将来推計）→", {
    x:CX, y:CB+0.3, w:CW, h:0.24,
    fontSize:8.5, color:C.darkgray, fontFace:"Meiryo", align:"center", margin:0
  });
  s.addText("BEV\n普及率\n（%）", {
    x:0.0, y:CY+CH/2-0.5, w:1.25, h:1.0,
    fontSize:8, color:C.darkgray, fontFace:"Meiryo", align:"center", margin:0
  });

  // 象限戦略ラベル（中国バブルと被らないよう配置）
  s.addText("シェア維持戦略",       { x:7.1,     y:CY+0.1,  w:1.4, h:0.26, fontSize:9.5, bold:true, color:"15803D", fontFace:"Meiryo", margin:0 });
  s.addText("シェアを奪う戦略",     { x:CX+0.12, y:CY+0.1,  w:2.0, h:0.26, fontSize:9.5, bold:true, color:"92400E", fontFace:"Meiryo", margin:0 });
  s.addText("市場を大きくする戦略", { x:qx+0.12, y:qy+0.1,  w:2.2, h:0.26, fontSize:9.5, bold:true, color:"1E40AF", fontFace:"Meiryo", margin:0 });
  s.addText("投資最小化戦略",       { x:CX+0.12, y:qy+0.1,  w:2.0, h:0.26, fontSize:9.5, bold:true, color:"475569", fontFace:"Meiryo", margin:0 });

  // 国データ（pen=BEV普及率%, gr=成長スコア, vol=BYD販売台数, sh=BEV内BYDシェア%)
  const m14 = [
    { jp:"中国",           pen:44.0, gr:4.0, vol:3750000, sh:32,  lb:"left",  dy:0     },
    { jp:"EU",             pen:17.0, gr:3.2, vol:50000,   sh:2,   lb:"left",  dy:0     },
    { jp:"UK",             pen:22.0, gr:2.8, vol:8700,    sh:1,   lb:"right", dy:-0.12 },
    { jp:"タイ",           pen:14.0, gr:4.2, vol:30000,   sh:40,  lb:"right", dy:0     },
    { jp:"オーストラリア", pen:7.2,  gr:3.0, vol:12438,   sh:14,  lb:"right", dy:0     },
    { jp:"米国",           pen:8.0,  gr:2.5, vol:500,     sh:0.1, lb:"left",  dy:0     },
    { jp:"ブラジル",       pen:5.0,  gr:3.2, vol:5000,    sh:5,   lb:"left",  dy:0     },
    { jp:"マレーシア",     pen:3.3,  gr:4.3, vol:8570,    sh:39,  lb:"right", dy:-0.22 },
    { jp:"日本",           pen:3.0,  gr:1.5, vol:2223,    sh:3,   lb:"right", dy:0     },
    { jp:"インドネシア",   pen:1.7,  gr:4.8, vol:7000,    sh:10,  lb:"right", dy:0.16  },
    { jp:"インド",         pen:2.0,  gr:5.0, vol:500,     sh:1,   lb:"left",  dy:-0.22 },
    { jp:"サウジ",         pen:1.0,  gr:3.8, vol:2000,    sh:5,   lb:"right", dy:-0.22 },
    { jp:"南ア",           pen:0.24, gr:2.0, vol:0,       sh:0,   lb:"left",  dy:0     },
    { jp:"モロッコ",       pen:0.5,  gr:3.5, vol:0,       sh:0,   lb:"left",  dy:0.22  },
  ];

  function bR14(vol) {
    if (vol<=0) return 0.07;
    return Math.min(0.48, 0.07+Math.sqrt(vol/100000)*0.11);
  }
  function shCol(sh) {
    if (sh<5)  return "BFDBFE";
    if (sh<15) return "3B82F6";
    if (sh<30) return "F59E0B";
    return "22C55E";
  }

  m14.forEach(m => {
    const cx=_px(m.gr), cy=_py(m.pen), r=bR14(m.vol), d=r*2;
    s.addShape(pres.shapes.OVAL, {
      x:cx-r, y:cy-r, w:d, h:d,
      fill:{color:shCol(m.sh)}, line:{color:"334155", pt:0.75}
    });
    const lw=1.15;
    const labelX = m.lb==="right" ? cx+r+0.05 : cx-r-0.05-lw;
    s.addText(m.jp, {
      x:labelX, y:cy-0.12+(m.dy||0), w:lw, h:0.24,
      fontSize:7.5, color:C.darkgray, fontFace:"Meiryo",
      align:m.lb==="right"?"left":"right", margin:0
    });
  });

  // 凡例（チャート右側）
  const LX=8.62, LY=CY;
  s.addText("BYDシェア", { x:LX, y:LY, w:1.3, h:0.22, fontSize:8, bold:true, color:C.darkgray, fontFace:"Meiryo", margin:0 });
  [
    { c:"BFDBFE", l:"0〜5%"   },
    { c:"3B82F6", l:"5〜15%"  },
    { c:"F59E0B", l:"15〜30%" },
    { c:"22C55E", l:"30%超"   },
  ].forEach((item,i) => {
    const y=LY+0.26+i*0.28;
    s.addShape(pres.shapes.OVAL, { x:LX+0.02, y:y+0.03, w:0.17, h:0.17, fill:{color:item.c}, line:{color:"334155",pt:0.5} });
    s.addText(item.l, { x:LX+0.24, y, w:1.05, h:0.24, fontSize:7.5, color:C.darkgray, fontFace:"Meiryo", margin:0 });
  });
  s.addText("販売台数\n（大＝多）", { x:LX, y:LY+1.42, w:1.3, h:0.44, fontSize:7.5, bold:true, color:C.darkgray, fontFace:"Meiryo", margin:0 });
  s.addText("大：中国375万台\n中：EU・タイ\n小：日本・南ア他", { x:LX, y:LY+1.90, w:1.3, h:0.60, fontSize:7, color:C.gray, fontFace:"Meiryo", margin:0 });
}

// ============================================================
// スライド 15: 市場別BYD戦略方針（4象限まとめ）
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.offwhite };

  s.addText("市場別BYD戦略方針", {
    x:0.35, y:0.08, w:9.0, h:0.48,
    fontSize:22, bold:true, color:C.navy, fontFace:"Meiryo", margin:0
  });

  const st15 = [
    {
      title:"シェア維持戦略",
      sub:"高普及×高成長×高シェア",
      mkts:"中国",
      acts:[
        "モデル更新速度と電池コストで価格競争力を維持",
        "PHEV・商用EV等で新カテゴリを開拓しシェア防衛",
        "補助金依存リスクを徹底したコスト削減で相殺",
      ],
      bg:"DCFCE7", border:"16A34A", tc:"15803D",
    },
    {
      title:"シェアを奪う戦略",
      sub:"高普及×成長期×低シェア",
      mkts:"EU・UK",
      acts:[
        "EU：ハンガリー工場（2026稼働）で関税25%を回避",
        "EV専業ブランドを訴求し欧州競合との差別化を図る",
        "UK：右ハンドル市場でのモデル拡充とディーラー網強化",
      ],
      bg:"FEF9C3", border:"E67E22", tc:"92400E",
    },
    {
      title:"市場を大きくする戦略",
      sub:"普及途上×高成長×BYD参入中",
      mkts:"タイ・マレーシア・インドネシア・インド・サウジ・モロッコ",
      acts:[
        "タイ：BEVシェア40%の足掛かりをASEAN拠点に転換",
        "現地OEM委託（CKD/SKD）で資本負担を最小化",
        "BEV市場そのものをBYDが育てる先行者利益を確立",
      ],
      bg:"DBEAFE", border:"2E5EAA", tc:"1E40AF",
    },
    {
      title:"投資最小化戦略",
      sub:"低普及×低成長×参入困難",
      mkts:"日本・米国・南ア",
      acts:[
        "モデル数を絞り最小コストでブランドプレゼンスを維持",
        "ショールーム・PR投資のみに限定、製造投資は行わない",
        "政策転換（補助金拡大・輸入関税緩和）を常時監視",
      ],
      bg:"F1F5F9", border:"64748B", tc:"475569",
    },
  ];

  st15.forEach((st, i) => {
    const col=i%2, row=Math.floor(i/2);
    const x=0.22+col*4.9, y=0.78+row*2.4, w=4.68, h=2.3;

    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill:{color:st.bg}, line:{color:st.border, pt:2}, shadow:ms() });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h:0.52, fill:{color:st.border}, line:{color:st.border} });

    s.addText(st.title, { x:x+0.12, y:y+0.04, w:w-0.24, h:0.26, fontSize:14, bold:true, color:C.white,    fontFace:"Meiryo", margin:0 });
    s.addText(st.sub,   { x:x+0.12, y:y+0.30, w:w-0.24, h:0.20, fontSize:8.5, color:C.white, italic:true, fontFace:"Meiryo", margin:0 });
    s.addText("対象市場："+st.mkts, { x:x+0.12, y:y+0.58, w:w-0.24, h:0.26, fontSize:9, bold:true, color:C.darkgray, fontFace:"Meiryo", margin:0 });

    st.acts.forEach((a, j) => {
      s.addText("・"+a, {
        x:x+0.12, y:y+0.88+j*0.44, w:w-0.24, h:0.42,
        fontSize:9, color:C.darkgray, fontFace:"Meiryo", margin:0, valign:"top"
      });
    });
  });
}

// ============================================================
// 出力
// ============================================================
pres.writeFile({ fileName: "BYD進出先シナリオ分析.pptx" }).then(() => {
  console.log("✅ 作成完了: BYD進出先シナリオ分析.pptx");
}).catch(err => {
  console.error("❌ エラー:", err);
});
