// 文京区 保健・健康サービス詳細スライド v2
// 区民の目線で：誰が・いくらで・何を
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaSearch, FaRunning, FaSwimmer, FaBaby, FaUserMd, FaBrain,
  FaLeaf, FaHome, FaHeartbeat, FaMoneyBillWave, FaChartPie,
  FaDumbbell, FaTableTennis, FaFutbol, FaSyringe
} = require("react-icons/fa");
const { MdSportsGymnastics, MdElderly } = require("react-icons/md");

// ── Color palette ───────────────────────────────────────────────────
const C = {
  navy:     "1A3A5C",
  blue:     "1B6CA8",
  skyBlue:  "D6EAF8",
  white:    "FFFFFF",
  off:      "F5F8FB",
  green:    "1A7F5A",
  lGreen:   "D5F0E5",
  gold:     "C97B10",
  orange:   "D9681A",
  lOrange:  "FDE8D3",
  purple:   "6B3FA0",
  lPurple:  "EDE0FF",
  red:      "B71C1C",
  lRed:     "FFEBEE",
  dark:     "1C1C2E",
  gray:     "5D6D7E",
  light:    "ECF0F1",
};

const mkShadow = () => ({ type:"outer", color:"000000", blur:8, offset:3, angle:45, opacity:0.11 });

async function iconPng(IC, color="#FFFFFF", size=256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IC, { color, size: String(size) })
  );
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ── 料金バッジ helper ────────────────────────────────────────────────
function addFeeTag(s, x, y, w, text, bgColor) {
  s.addShape(s.pres ? s.pres.shapes.ROUNDED_RECTANGLE : pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h: 0.28, fill: { color: bgColor }, rectRadius: 0.08
  });
  s.addText(text, {
    x, y, w, h: 0.28, fontSize: 9.5, color: C.white, fontFace: "Arial",
    bold: true, align: "center", margin: 0
  });
}

// ────────────────────────────────────────────────────────────────────
async function main() {
  let pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = "文京区 保健・健康サービス完全ガイド（区民向け）";

  // ================================================================
  // Slide 1: Title
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.shapes.OVAL, { x:7.8, y:-1.2, w:4, h:4, fill:{color:C.blue, transparency:65}, line:{color:C.blue,width:0} });
    s.addShape(pres.shapes.OVAL, { x:8.8, y:-0.3, w:3, h:3, fill:{color:"2980B9", transparency:75}, line:{color:"2980B9",width:0} });

    s.addShape(pres.shapes.OVAL, { x:0.55, y:0.55, w:0.9, h:0.9, fill:{color:C.green} });
    const leafIcon = await iconPng(FaLeaf, "#FFFFFF");
    s.addImage({ data: leafIcon, x:0.72, y:0.72, w:0.55, h:0.55 });
    s.addText("文京区", { x:1.6, y:0.65, w:3, h:0.45, fontSize:15, color:"8FBFDF", fontFace:"Arial", bold:true, margin:0 });

    s.addText("区民のための", { x:0.6, y:1.5, w:9, h:0.6, fontSize:16, color:"8FBFDF", fontFace:"Arial", margin:0 });
    s.addText("保健・健康サービス", { x:0.6, y:2.05, w:9.2, h:0.85, fontSize:40, color:C.white, fontFace:"Arial", bold:true, margin:0 });
    s.addText("完全ガイド", { x:0.6, y:2.85, w:9.2, h:0.85, fontSize:40, color:C.white, fontFace:"Arial", bold:true, margin:0 });

    s.addShape(pres.shapes.RECTANGLE, { x:0.6, y:3.85, w:3, h:0.06, fill:{color:C.gold} });
    s.addText("誰が・いくらで・何を受けられるか", { x:0.6, y:3.98, w:9, h:0.35, fontSize:14, color:"CADCF0", fontFace:"Arial", margin:0 });
    s.addText("令和7年度予算：一般会計 1,470億円　令和8年度：1,605億円（過去最大）", {
      x:0.6, y:4.4, w:9, h:0.3, fontSize:11, color:"6A8EAE", fontFace:"Arial", margin:0
    });

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:5.1, w:10, h:0.525, fill:{color:C.green} });
    s.addText("文京区区長政策スタッフ資料　2026年7月", { x:0.5, y:5.15, w:9, h:0.42, fontSize:12, color:C.white, fontFace:"Arial", align:"center", margin:0 });

    s.addNotes("タイトルスライド。区民が実際に使えるサービスを具体的な料金・対象者・手続きとともに説明する資料。");
  }

  // ================================================================
  // Slide 2: サービス全体マップ
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:C.navy} });
    s.addText("どんなサービスが使えるか？ ─ 全体マップ", {
      x:0.5, y:0.1, w:9, h:0.58, fontSize:21, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    const cats = [
      { title:"① 健康診査・がん検診", color:C.blue,   items:["特定健診（メタボ）", "後期高齢者健診", "胃・大腸・肺がん", "乳・子宮がん", "肝炎ウイルス", "眼科健診"], fee:"すべて無料" },
      { title:"② スポーツ施設",       color:C.green,  items:["プール", "トレーニングルーム", "競技場・道場", "月謝制スクール", "屋外スポーツ施設", "卓球・弓道"], fee:"一般550円〜" },
      { title:"③ 地域スポーツ開放",   color:"1A7050", items:["学校体育館開放", "スポーツ交流ひろば", "卓球・バレー", "バドミントン", "太極拳", "テニス"], fee:"すべて無料" },
      { title:"④ 母子保健",           color:C.purple, items:["妊婦健診（14回）", "超音波（4回）", "産後訪問ケア", "乳幼児健診", "予防接種", "育児相談"], fee:"原則無料〜3,000円" },
      { title:"⑤ 高齢者サービス",     color:C.orange, items:["地域包括支援センター", "介護予防教室", "フレイル健診", "認知症支援", "訪問看護連携", "予防接種助成"], fee:"原則無料" },
      { title:"⑥ こころの健康",       color:C.red,    items:["精神保健相談", "認知症初期支援", "ひきこもり支援", "自殺予防相談", "アルコール相談", "依存症連携"], fee:"無料（要予約）" },
    ];

    const cw = 2.95, ch = 3.65;
    cats.forEach((cat, i) => {
      const cx = 0.28 + (i % 3) * (cw + 0.23);
      const cy = 0.95 + Math.floor(i / 3) * (ch + 0.25);

      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:cx, y:cy, w:cw, h:ch, fill:{color:C.white}, rectRadius:0.1, shadow:mkShadow()
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x:cx, y:cy, w:cw, h:0.42, fill:{color:cat.color}, line:{color:cat.color}
      });
      s.addText(cat.title, { x:cx+0.08, y:cy+0.05, w:cw-0.15, h:0.35, fontSize:11, color:C.white, fontFace:"Arial", bold:true, margin:0 });

      cat.items.forEach((item, j) => {
        s.addShape(pres.shapes.OVAL, { x:cx+0.18, y:cy+0.55+j*0.39, w:0.13, h:0.13, fill:{color:cat.color} });
        s.addText(item, { x:cx+0.37, y:cy+0.51+j*0.39, w:cw-0.48, h:0.34, fontSize:9.5, color:C.dark, fontFace:"Arial", margin:0 });
      });

      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:cx+0.15, y:cy+ch-0.42, w:cw-0.3, h:0.28, fill:{color:cat.color}, rectRadius:0.08
      });
      s.addText("💰 " + cat.fee, { x:cx+0.15, y:cy+ch-0.42, w:cw-0.3, h:0.28, fontSize:9.5, color:C.white, fontFace:"Arial", bold:true, align:"center", margin:0 });
    });

    s.addNotes("全サービスの俯瞰マップ。6カテゴリを一覧で提示。料金の概要を色付きタグで示す。");
  }

  // ================================================================
  // Slide 3: 健康診査・がん検診（具体的料金・対象）
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:C.blue} });
    s.addText("① 健康診査・がん検診　─　すべて無料で受けられる", {
      x:0.4, y:0.1, w:9.2, h:0.58, fontSize:20, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    // 共通注記
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:0.3, y:0.88, w:9.4, h:0.42, fill:{color:C.skyBlue}, rectRadius:0.08
    });
    s.addText("受診期間：令和8年6月15日〜令和9年1月30日　　受診方法：区内指定医療機関に電話予約（受診券不要の場合も）　　持参物：マイナ保険証 or 資格確認書", {
      x:0.4, y:0.92, w:9.2, h:0.32, fontSize:9, color:C.navy, fontFace:"Arial", margin:0
    });

    const items = [
      {
        name:"特定健康診査（メタボ健診）",
        who:"文京区国民健康保険加入・40〜74歳",
        fee:"無料",feeColor:C.green,
        detail:"腹囲・血圧・血液・尿検査＋問診。必要に応じ心電図・眼底・貧血も追加。大腸・肺がん検診と同時受診可。",
        note:"※国保加入者のみ。社保加入者は各保険者の健診へ"
      },
      {
        name:"後期高齢者健康診査",
        who:"後期高齢者医療制度加入者（75歳以上等）",
        fee:"無料",feeColor:C.green,
        detail:"問診・身体計測・血圧・血糖・脂質・腎機能等の血液・尿検査。かかりつけ医での受診も可。",
        note:""
      },
      {
        name:"胃がん検診",
        who:"40歳以上（内視鏡は50歳以上・偶数年齢）",
        fee:"無料",feeColor:C.green,
        detail:"X線（バリウム）は40歳以上毎年、内視鏡は50歳以上で偶数年齢に2年に1回。偶数年齢の方はどちらか選択。",
        note:""
      },
      {
        name:"大腸がん検診",
        who:"40歳以上の区民",
        fee:"無料",feeColor:C.green,
        detail:"便潜血反応検査（2日法）。区内指定医療機関に直接電話予約。受診券不要。年1回受診可。",
        note:""
      },
      {
        name:"肺がん検診",
        who:"40歳以上の区民",
        fee:"無料",feeColor:C.green,
        detail:"胸部X線検査。喫煙歴がある一定条件者には喀痰検査を追加。特定健診と同時受診で効率的。",
        note:""
      },
      {
        name:"乳がん検診",
        who:"40歳以上・偶数年齢の女性",
        fee:"無料",feeColor:C.green,
        detail:"マンモグラフィ検査（2年に1回）。偶数年齢の年度に受診。区内委託医療機関で実施。",
        note:"受診期間：4月10日〜翌3月31日"
      },
      {
        name:"子宮がん検診",
        who:"20歳以上・偶数年齢の女性",
        fee:"無料",feeColor:C.green,
        detail:"子宮頸がん細胞診。20歳からの早期受診が重要。偶数年齢の方が対象（2年に1回）。",
        note:""
      },
      {
        name:"肝炎ウイルス検査・眼科健診",
        who:"肝炎：40歳以上で未受診者　眼科：40/50/55/60/65/70歳",
        fee:"無料",feeColor:C.green,
        detail:"肝炎はB型・C型を一度だけ検査（既受診者は対象外）。眼科は緑内障等の早期発見を目的。",
        note:""
      },
    ];

    const rows = [0,1,2,3,4,5,6,7];
    const col1 = [0,1,2,3], col2 = [4,5,6,7];

    [[col1, 0.3], [col2, 5.1]].forEach(([idxs, cx]) => {
      idxs.forEach((idx, j) => {
        const item = items[idx];
        const cy = 1.4 + j * 1.04;
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx, y:cy, w:4.65, h:0.97, fill:{color:C.white}, rectRadius:0.09, shadow:mkShadow()
        });
        // 無料バッジ
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx+3.8, y:cy+0.05, w:0.7, h:0.24, fill:{color:item.feeColor}, rectRadius:0.06
        });
        s.addText(item.fee, { x:cx+3.8, y:cy+0.05, w:0.7, h:0.24, fontSize:9, color:C.white, fontFace:"Arial", bold:true, align:"center", margin:0 });

        s.addText(item.name, { x:cx+0.12, y:cy+0.05, w:3.6, h:0.28, fontSize:11, color:C.navy, fontFace:"Arial", bold:true, margin:0 });
        s.addText("対象：" + item.who, { x:cx+0.12, y:cy+0.34, w:4.45, h:0.22, fontSize:8.5, color:C.blue, fontFace:"Arial", margin:0 });
        s.addText(item.detail + (item.note ? " " + item.note : ""), { x:cx+0.12, y:cy+0.58, w:4.45, h:0.33, fontSize:8, color:C.gray, fontFace:"Arial", margin:0 });
      });
    });

    s.addNotes("健康診査・がん検診は区民・国保加入者向けにすべて無料。対象年齢・条件・内容を明記。受診率向上が課題。");
  }

  // ================================================================
  // Slide 4: 文京スポーツセンター（詳細料金）
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:C.green} });
    s.addText("② 文京スポーツセンター ─ 料金・施設・スクール", {
      x:0.4, y:0.1, w:9.2, h:0.58, fontSize:20, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    // 施設概要タグ
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:0.3, y:0.88, w:9.4, h:0.38, fill:{color:C.lGreen}, rectRadius:0.08
    });
    s.addText("場所：文京区大塚3-29-2（茗荷谷駅・護国寺駅徒歩5分）　　利用資格：文京区在住・在勤・在学の方（区外の方も一部利用可）　　営業：9:00〜22:30", {
      x:0.4, y:0.92, w:9.2, h:0.28, fontSize:9, color:C.navy, fontFace:"Arial", margin:0
    });

    // 左：個人利用料金表
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:0.28, y:1.35, w:4.2, h:4.0, fill:{color:C.white}, rectRadius:0.1, shadow:mkShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.28, y:1.35, w:4.2, h:0.42, fill:{color:C.green}, line:{color:C.green}
    });
    s.addText("個人利用料金（1回あたり）", { x:0.35, y:1.38, w:4.1, h:0.34, fontSize:12, color:C.white, fontFace:"Arial", bold:true, margin:0 });

    const feeRows = [
      ["施設", "一般", "65〜69歳", "中学生以下", "70歳以上"],
      ["プール（2時間）", "550円", "280円", "230円", "無料"],
      ["プール定期（月）", "4,600円", "─", "2,300円", "─"],
      ["トレーニングルーム（3h）", "600円", "300円", "─", "無料"],
      ["トレーニング定期（月）", "2,800円", "2,800円", "─", "─"],
      ["競技場・道場（1回）", "310円", "─", "160円", "─"],
    ];
    s.addTable(feeRows, {
      x:0.35, y:1.82, w:4.06, h:3.35,
      border:{ pt:0.5, color:"DCEEF6" },
      fontSize:9,
      fontFace:"Arial",
      color:C.dark,
      fill:[
        { type:"solid", color:"1A7F5A" },
        { type:"solid", color:C.white },
        { type:"solid", color:"F0FFF8" },
        { type:"solid", color:C.white },
        { type:"solid", color:"F0FFF8" },
        { type:"solid", color:C.white },
      ]
    });

    // 右上：スクール
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:4.72, y:1.35, w:4.95, h:2.18, fill:{color:C.white}, rectRadius:0.1, shadow:mkShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:4.72, y:1.35, w:4.95, h:0.42, fill:{color:"0E6B4A"}, line:{color:"0E6B4A"}
    });
    s.addText("スクール（月謝制）", { x:4.8, y:1.38, w:4.8, h:0.34, fontSize:12, color:C.white, fontFace:"Arial", bold:true, margin:0 });

    const schools = [
      { name:"子どもプールスクール", target:"乳幼児〜中学生", fee:"月 約5,000円〜", note:"レベル別コース。年齢・泳力で選択" },
      { name:"池田体操教室", target:"乳幼児〜中学生", fee:"月 約5,000円〜", note:"ローマ世界選手権金メダリスト監修" },
      { name:"竹早テニススクール", target:"小学生以上", fee:"月 約5,000円〜", note:"屋外テニスコート使用。7月期募集中" },
      { name:"サッカーひろば", target:"幼児〜小学生", fee:"参加費あり", note:"東京ユナイテッドFC指導" },
      { name:"成人スタジオコース", target:"15歳以上", fee:"月 5,000〜6,000円", note:"エアロビ・ヨガ等。プール込みで増額" },
    ];
    schools.forEach((sc, j) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:4.8, y:1.85 + j*0.32, w:4.78, h:0.28, fill:{color:j%2===0?"F0FFF8":C.white}, rectRadius:0.05
      });
      s.addText(sc.name, { x:4.88, y:1.87+j*0.32, w:1.8, h:0.23, fontSize:9, color:C.navy, fontFace:"Arial", bold:true, margin:0 });
      s.addText(sc.target, { x:6.65, y:1.87+j*0.32, w:1.1, h:0.23, fontSize:8, color:C.gray, fontFace:"Arial", margin:0 });
      s.addText(sc.fee, { x:7.72, y:1.87+j*0.32, w:1.0, h:0.23, fontSize:8.5, color:C.green, fontFace:"Arial", bold:true, margin:0 });
    });

    // 右下：特典・注意事項
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:4.72, y:3.64, w:4.95, h:1.71, fill:{color:C.lGreen}, rectRadius:0.1
    });
    s.addText("シニア特典と注意事項", { x:4.88, y:3.72, w:4.7, h:0.32, fontSize:11, color:C.green, fontFace:"Arial", bold:true, margin:0 });
    const notes2 = [
      "65〜69歳：事前登録でシルバー料金（約半額）が適用",
      "70〜79歳（セミゴールド）：プール・トレーニング室が無料",
      "80歳以上（ゴールド）：プール・トレーニング室が無料",
      "障がい者と付添人1名：利用料免除",
      "文京区外の方：一般料金で利用可（定期券不可の場合あり）",
    ];
    notes2.forEach((n, j) => {
      s.addShape(pres.shapes.OVAL, { x:4.85, y:4.1+j*0.33, w:0.12, h:0.12, fill:{color:C.green} });
      s.addText(n, { x:5.03, y:4.07+j*0.33, w:4.55, h:0.27, fontSize:9, color:C.dark, fontFace:"Arial", margin:0 });
    });

    s.addNotes("スポーツセンターの具体的料金。70歳以上はプールもトレーニングも無料という大きな特典がある。");
  }

  // ================================================================
  // Slide 5: 地域スポーツ（学校体育館開放・スポーツ交流ひろば）
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:"1A7050"} });
    s.addText("③ 地域スポーツ開放 ─ 学校体育館・校庭が無料で使える！", {
      x:0.4, y:0.1, w:9.2, h:0.58, fontSize:19, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    // スポーツ交流ひろば メイン
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:0.28, y:0.9, w:9.44, h:2.3, fill:{color:C.white}, rectRadius:0.12, shadow:mkShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.28, y:0.9, w:9.44, h:0.45, fill:{color:"1A7050"}, line:{color:"1A7050"}
    });
    s.addText("スポーツ交流ひろば", { x:0.42, y:0.93, w:5, h:0.38, fontSize:14, color:C.white, fontFace:"Arial", bold:true, margin:0 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:7.9, y:0.96, w:1.65, h:0.3, fill:{color:C.gold}, rectRadius:0.08
    });
    s.addText("参加費：無料", { x:7.9, y:0.96, w:1.65, h:0.3, fontSize:11, color:C.white, fontFace:"Arial", bold:true, align:"center", margin:0 });

    s.addText("対象：文京区在住・在勤・在学の方　　事前登録・申込み不要。時間内なら途中参加・退出自由。指導員が常駐。", {
      x:0.42, y:1.43, w:9.1, h:0.28, fontSize:9.5, color:C.blue, fontFace:"Arial", margin:0
    });

    const sports = [
      { s:"卓球", w:"月〜金 18:00〜21:00", p:"本郷小・文林中・第九中 等" },
      { s:"バレーボール", w:"火・木・金 18:30〜21:00", p:"第九中 等" },
      { s:"バドミントン", w:"月・水・土 など", p:"各校体育館" },
      { s:"ソフト・硬式テニス", w:"日 9:00〜15:30", p:"各校校庭" },
      { s:"バスケットボール", w:"週複数回", p:"各校体育館" },
      { s:"軽体操・太極拳", w:"月〜日 9:00〜21:00", p:"各校体育館" },
      { s:"ビーチボール", w:"週複数回", p:"各校体育館" },
      { s:"フライングディスク", w:"不定期", p:"校庭・公園" },
    ];
    const cols = [sports.slice(0,4), sports.slice(4,8)];
    cols.forEach((col, ci) => {
      col.forEach((sp, j) => {
        const cx = 0.38 + ci * 4.7;
        const cy = 1.78 + j * 0.33;
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx, y:cy, w:4.5, h:0.28, fill:{color: j%2===0 ? "F0FFF8" : C.white}, rectRadius:0.05
        });
        s.addText(sp.s, { x:cx+0.08, y:cy+0.04, w:1.1, h:0.22, fontSize:9.5, color:"1A7050", fontFace:"Arial", bold:true, margin:0 });
        s.addText(sp.w, { x:cx+1.2, y:cy+0.04, w:1.75, h:0.22, fontSize:8.5, color:C.dark, fontFace:"Arial", margin:0 });
        s.addText(sp.p, { x:cx+2.95, y:cy+0.04, w:1.5, h:0.22, fontSize:8, color:C.gray, fontFace:"Arial", margin:0 });
      });
    });

    // 学校施設開放
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:0.28, y:3.33, w:9.44, h:1.98, fill:{color:C.white}, rectRadius:0.12, shadow:mkShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.28, y:3.33, w:9.44, h:0.42, fill:{color:"2D6A4F"}, line:{color:"2D6A4F"}
    });
    s.addText("区立小・中学校　施設使用（団体登録制）", { x:0.42, y:3.36, w:6, h:0.35, fontSize:13, color:C.white, fontFace:"Arial", bold:true, margin:0 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:7.55, y:3.39, w:2.0, h:0.27, fill:{color:C.gold}, rectRadius:0.08
    });
    s.addText("使用料：概ね無料〜低額", { x:7.55, y:3.39, w:2.0, h:0.27, fontSize:9.5, color:C.white, fontFace:"Arial", bold:true, align:"center", margin:0 });

    const schoolItems = [
      ["対象団体", "文京区在住区民が主体のスポーツ・文化団体（5人以上）"],
      ["利用施設", "体育館・校庭・プール（一部）　区内26校（小15・中11）"],
      ["申込方法", "「文の京」施設予約ネットから申請　→　学校長許可"],
      ["利用時間", "平日：放課後〜20:00　土日祝：8:00〜20:00（学校行事優先）"],
    ];
    schoolItems.forEach(([k, v], j) => {
      s.addText(k + "：", { x:0.42, y:3.85+j*0.35, w:1.3, h:0.3, fontSize:10, color:"2D6A4F", fontFace:"Arial", bold:true, margin:0 });
      s.addText(v, { x:1.7, y:3.85+j*0.35, w:7.9, h:0.3, fontSize:10, color:C.dark, fontFace:"Arial", margin:0 });
    });

    s.addNotes("スポーツ交流ひろばは無料・申込不要。学校施設は団体登録制で使用可。地域スポーツを区が積極支援している。");
  }

  // ================================================================
  // Slide 6: 母子保健（妊娠〜育児の費用詳細）
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:C.purple} });
    s.addText("④ 母子保健 ─ 妊娠届から育児まで、いくらかかるか", {
      x:0.4, y:0.1, w:9.2, h:0.58, fontSize:19, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    const steps = [
      {
        phase: "妊娠初期", color: "7B3FA0", lc:"EDE0FF",
        services: [
          { name:"妊娠届・母子健康手帳", fee:"無料", who:"妊娠したら速やかに区役所へ（オンライン届出も可）" },
          { name:"妊婦健康診査（14回分）", fee:"助成あり", who:"受診票14枚を交付。受診費用の一定額を区が補助（医療機関で差額が生じる場合あり）" },
          { name:"妊婦超音波検査（4回分）", fee:"助成あり", who:"4回分の受診票を交付" },
          { name:"妊婦子宮頸がん検診（1回）", fee:"無料", who:"妊娠中に1回受診票を交付" },
        ]
      },
      {
        phase: "産後〜乳児期", color: "C62878", lc:"FCE4EC",
        services: [
          { name:"こんにちは赤ちゃん訪問", fee:"無料", who:"生後4ヶ月以内に保健師・助産師が全家庭を訪問" },
          { name:"訪問型産後ケア（助産師訪問）", fee:"3,000円/回（最大1年・3回）", who:"産後1年未満の方。非課税世帯は減免あり（2,500円/回×5回まで）" },
          { name:"産後ショートステイ・デイサービス", fee:"自己負担あり（所得応能）", who:"産後ケア施設での入院型・通院型ケア。施設により異なる" },
        ]
      },
      {
        phase: "乳幼児健診・予防接種", color: "1565C0", lc:"E3F2FD",
        services: [
          { name:"乳幼児健康診査", fee:"無料", who:"3〜4ヶ月・9〜10ヶ月・1歳6ヶ月・3歳。区保健センターで実施" },
          { name:"定期予防接種（国が定めるもの）", fee:"無料", who:"ヒブ・肺炎球菌・四種混合・BCG・MR・水痘・日本脳炎・HPV等。区内指定医療機関で実施" },
          { name:"発達相談・療育支援", fee:"無料", who:"言語・発達に気になる点があれば保健センターへ。専門職が相談対応" },
        ]
      },
      {
        phase: "保育・子育て支援", color: "2E7D32", lc:"E8F5E9",
        services: [
          { name:"保育所・認定こども園", fee:"3歳以上は無償化・0〜2歳は所得応能", who:"区内認可保育所・こども園。入所申請は毎年10月頃〜" },
          { name:"一時保育・緊急保育", fee:"1時間 300〜700円程度", who:"リフレッシュや緊急時に対応。保育所・施設による" },
          { name:"子ども食堂", fee:"無料〜100円", who:"区内複数箇所。孤食防止・地域交流が目的" },
        ]
      },
    ];

    const cw = 4.52;
    steps.forEach((step, i) => {
      const cx = 0.28 + (i % 2) * (cw + 0.24);
      const cy = 0.9 + Math.floor(i / 2) * 2.35;

      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:cx, y:cy, w:cw, h:2.25, fill:{color:C.white}, rectRadius:0.1, shadow:mkShadow()
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x:cx, y:cy, w:cw, h:0.4, fill:{color:step.color}, line:{color:step.color}
      });
      s.addText(step.phase, { x:cx+0.1, y:cy+0.06, w:cw-0.2, h:0.3, fontSize:12, color:C.white, fontFace:"Arial", bold:true, margin:0 });

      step.services.forEach((sv, j) => {
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx+0.1, y:cy+0.47+j*0.59, w:cw-0.2, h:0.54, fill:{color:j%2===0?step.lc:C.white}, rectRadius:0.07
        });
        s.addText(sv.name, { x:cx+0.18, y:cy+0.5+j*0.59, w:2.8, h:0.24, fontSize:9.5, color:step.color, fontFace:"Arial", bold:true, margin:0 });
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx+3.08, y:cy+0.5+j*0.59, w:1.14, h:0.22, fill:{color:sv.fee==="無料"?C.green:C.orange}, rectRadius:0.07
        });
        s.addText(sv.fee, { x:cx+3.08, y:cy+0.5+j*0.59, w:1.14, h:0.22, fontSize:8, color:C.white, fontFace:"Arial", bold:true, align:"center", margin:0 });
        s.addText(sv.who, { x:cx+0.18, y:cy+0.74+j*0.59, w:4.17, h:0.22, fontSize:7.5, color:C.gray, fontFace:"Arial", margin:0 });
      });
    });

    s.addNotes("母子保健は妊娠届から子育て支援まで。定期健診・予防接種は無料。産後ケアは1回3,000円で1年以内3回まで利用可。");
  }

  // ================================================================
  // Slide 7: 高齢者向けサービス
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:C.orange} });
    s.addText("⑤ 高齢者向けサービス ─ 65歳・75歳から使える、具体的な内容", {
      x:0.4, y:0.1, w:9.2, h:0.58, fontSize:18.5, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    const services = [
      {
        cat:"相談・総合支援",
        color:"B45309", lc:"FEF3C7",
        items:[
          { name:"高齢者あんしん相談センター（地域包括支援センター）", who:"区内在住の65歳以上（家族も可）", fee:"無料", detail:"区内6ヶ所。介護・医療・福祉の一元相談。月〜金 9:00〜19:00、土日祝 9:00〜17:30" },
          { name:"介護保険利用相談・ケアプラン作成", who:"要支援・要介護認定者", fee:"無料（ケアマネ費用は介護保険適用）", detail:"介護認定申請の窓口。ケアマネジャーを無料で紹介・マッチング" },
        ]
      },
      {
        cat:"健診・予防接種",
        color:"1A7F5A", lc:"D5F0E5",
        items:[
          { name:"後期高齢者健康診査", who:"75歳以上（後期高齢者医療加入者）", fee:"無料", detail:"年1回。血液・血圧・尿・問診。かかりつけ医での受診も可。" },
          { name:"フレイル健診（後期高齢者質問票）", who:"75歳以上", fee:"無料（健診と同時実施）", detail:"身体・栄養・口腔・社会参加の4分野をチェック。フレイル予防に活用。" },
          { name:"インフルエンザワクチン", who:"65歳以上", fee:"1,500円（区の助成後）", detail:"秋に1回接種。区が費用の大部分を助成。区内指定医療機関で受診。" },
          { name:"肺炎球菌ワクチン（定期接種）", who:"65歳（1回のみ）", fee:"2,000円（区助成後）", detail:"65歳の年度に1回の定期接種。区内指定医療機関で受診可。" },
          { name:"帯状疱疹ワクチン助成", who:"50歳以上", fee:"接種費用の一部助成あり", detail:"2種類（生ワクチン・不活化）ともに助成対象。詳細は保健センターへ。" },
        ]
      },
      {
        cat:"介護予防・社会参加",
        color:"1B6CA8", lc:"D6EAF8",
        items:[
          { name:"いきいき体操教室（転倒予防）", who:"区内在住65歳以上", fee:"無料", detail:"区内各地のコミュニティセンター等で開催。運動習慣の定着を支援。" },
          { name:"認知症カフェ・サポーター養成", who:"どなたでも", fee:"無料", detail:"認知症の方と家族が気軽に集える場。サポーター講座を年複数回開催。" },
          { name:"在宅医療・介護連携（ACP）", who:"在宅療養中の方・家族", fee:"無料（相談のみ）", detail:"かかりつけ医・訪問看護・ケアマネの連携コーディネート。人生会議（ACP）普及。" },
        ]
      },
    ];

    services.forEach((sec, si) => {
      const cx = 0.28 + si * 3.27;
      const ch = sec.items.length * 1.26 + 0.55;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:cx, y:0.9, w:3.1, h:4.5, fill:{color:C.white}, rectRadius:0.1, shadow:mkShadow()
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x:cx, y:0.9, w:3.1, h:0.42, fill:{color:sec.color}, line:{color:sec.color}
      });
      s.addText(sec.cat, { x:cx+0.1, y:0.93, w:2.9, h:0.34, fontSize:11, color:C.white, fontFace:"Arial", bold:true, margin:0 });

      sec.items.forEach((item, j) => {
        const iy = 1.38 + j * 1.02;
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx+0.1, y:iy, w:2.9, h:0.96, fill:{color:j%2===0?sec.lc:C.white}, rectRadius:0.07
        });
        s.addText(item.name, { x:cx+0.17, y:iy+0.05, w:2.5, h:0.34, fontSize:9, color:sec.color, fontFace:"Arial", bold:true, margin:0 });
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
          x:cx+0.17, y:iy+0.4, w:2.7, h:0.2, fill:{color:item.fee==="無料"?C.green:C.orange}, rectRadius:0.06
        });
        s.addText("💰 " + item.fee + "　対象：" + item.who, {
          x:cx+0.17, y:iy+0.4, w:2.7, h:0.2, fontSize:7.5, color:C.white, fontFace:"Arial", bold:true, margin:0
        });
        s.addText(item.detail, { x:cx+0.17, y:iy+0.64, w:2.7, h:0.28, fontSize:7.5, color:C.gray, fontFace:"Arial", margin:0 });
      });
    });

    s.addNotes("高齢者サービスは相談・健診・予防・介護予防の3本柱。後期高齢者健診は無料。インフル接種は1,500円（区助成後）。");
  }

  // ================================================================
  // Slide 8: こころの健康
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addText("⑥ こころの健康支援 ─ 誰でも・無料で相談できる", {
      x:0.5, y:0.18, w:9, h:0.58, fontSize:22, color:C.white, fontFace:"Arial", bold:true, margin:0
    });
    s.addText("一人で抱え込まず、まずは電話・来所相談を。すべて無料・要予約", {
      x:0.5, y:0.74, w:9, h:0.3, fontSize:12, color:"8FBFDF", fontFace:"Arial", margin:0
    });

    const mhServices = [
      { n:"精神保健福祉相談", who:"本人・家族どなたでも", fee:"無料（要予約）", detail:"保健師・精神保健福祉士が個別相談。うつ・不安障がい・統合失調症等。月〜金 保健所窓口", phone:"03-5803-1834（保健所）" },
      { n:"ひきこもり支援相談", who:"当事者・家族", fee:"無料", detail:"長期ひきこもり・8050問題に対応。アウトリーチ（訪問支援）あり。居場所情報も提供。", phone:"03-5803-1212（福祉部）" },
      { n:"自殺予防・ゲートキーパー講座", who:"区民・支援者", fee:"無料", detail:"いのちの電話・よりそいホットライン等の相談窓口を案内。年複数回ゲートキーパー養成研修。", phone:"いのちの電話：0120-783-556" },
      { n:"アルコール・依存症相談", who:"本人・家族", fee:"無料", detail:"アルコール・薬物・ギャンブル依存に対応。自助グループへの紹介、専門医療機関への連携。", phone:"03-5803-1834（保健所）" },
      { n:"認知症初期集中支援", who:"物忘れが心配な方・家族", fee:"無料", detail:"「認知症初期集中支援チーム」が家庭訪問。医師・看護師・社会福祉士が連携して早期支援。", phone:"地域包括支援センター6ヶ所" },
      { n:"育児・子育てメンタル相談", who:"育児に悩む保護者", fee:"無料（要予約）", detail:"産後うつ・育児不安・虐待予防。保健センターの保健師が面談。必要に応じて専門機関紹介。", phone:"03-5803-1834（保健センター）" },
    ];

    mhServices.forEach((sv, i) => {
      const cx = i % 2 === 0 ? 0.35 : 5.15;
      const cy = 1.15 + Math.floor(i / 2) * 1.52;

      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:cx, y:cy, w:4.55, h:1.38, fill:{color:"1E3A5F"}, rectRadius:0.1
      });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:cx+3.4, y:cy+0.1, w:1.0, h:0.25, fill:{color:C.green}, rectRadius:0.07
      });
      s.addText("無料", { x:cx+3.4, y:cy+0.1, w:1.0, h:0.25, fontSize:10, color:C.white, fontFace:"Arial", bold:true, align:"center", margin:0 });
      s.addText(sv.n, { x:cx+0.15, y:cy+0.1, w:3.2, h:0.34, fontSize:12, color:"93C5FD", fontFace:"Arial", bold:true, margin:0 });
      s.addText("対象：" + sv.who, { x:cx+0.15, y:cy+0.46, w:4.3, h:0.22, fontSize:9, color:"CADCF0", fontFace:"Arial", margin:0 });
      s.addText(sv.detail, { x:cx+0.15, y:cy+0.68, w:4.3, h:0.34, fontSize:8.5, color:"A0BBD4", fontFace:"Arial", margin:0 });
      s.addText("☎ " + sv.phone, { x:cx+0.15, y:cy+1.06, w:4.3, h:0.24, fontSize:9, color:"60B4E0", fontFace:"Arial", margin:0 });
    });

    s.addNotes("こころの健康支援は全て無料。精神保健・ひきこもり・自殺予防・依存症・認知症・育児メンタルの6本柱。");
  }

  // ================================================================
  // Slide 9: 予算配分（令和7年度実績＋令和8年度比較）
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.off };

    s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.78, fill:{color:"2C3E50"} });
    s.addText("区の予算はどう使われているか ─ 令和7年度 一般会計 款別内訳", {
      x:0.4, y:0.1, w:9.2, h:0.58, fontSize:19, color:C.white, fontFace:"Arial", bold:true, margin:0
    });

    // 円グラフ
    s.addChart(pres.charts.PIE, [{
      name:"予算構成",
      labels:["民生費（福祉）", "教育費", "総務費", "衛生費", "土木費", "資源環境費", "区民費", "その他"],
      values:[40.5, 18.1, 14.2, 4.4, 4.0, 3.3, 3.2, 12.3]
    }], {
      x:0.3, y:0.9, w:4.8, h:4.5,
      chartColors:["E74C3C","2980B9","8E44AD","27AE60","E67E22","16A085","F39C12","95A5A6"],
      showPercent:true,
      showLegend:true,
      legendPos:"b",
      legendFontSize:9,
      dataLabelPosition:"center",
      dataLabelColor:"FFFFFF",
      dataLabelFontSize:10,
      chartArea:{ fill:{ color:C.off }, roundedCorners:false },
    });

    // 右側：款別金額詳細
    const budgetItems = [
      { name:"民生費（福祉・介護・子育て）", amt:"653億円", pct:"40.5%", color:"E74C3C", note:"介護保険・生活保護・子ども家庭支援を含む最大費目" },
      { name:"教育費（学校・生涯学習）", amt:"292億円", pct:"18.1%", color:"2980B9", note:"学校運営・教員配置・給食・スポーツ施設を含む" },
      { name:"総務費（行政運営）", amt:"228億円", pct:"14.2%", color:"8E44AD", note:"庁舎・情報システム・選挙・区民サービス窓口等" },
      { name:"衛生費（保健・医療）", amt:"71億円", pct:"4.4%", color:"27AE60", note:"保健所・健診・がん検診・母子保健・精神保健等" },
      { name:"土木費（道路・公園）", amt:"64億円", pct:"4.0%", color:"E67E22", note:"道路・橋梁・公園整備・都市計画" },
      { name:"資源環境費（ごみ・環境）", amt:"53億円", pct:"3.3%", color:"16A085", note:"清掃・リサイクル・環境施策" },
      { name:"区民費（区民サービス）", amt:"51億円", pct:"3.2%", color:"F39C12", note:"文化センター・スポーツ施設・区民相談等" },
      { name:"その他（産業・議会・予備費等）", amt:"約57億円", pct:"3.6%", color:"95A5A6", note:"産業経済・都市整備・議会費・予備費" },
    ];

    budgetItems.forEach((bi, j) => {
      const cy = 0.9 + j * 0.57;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x:5.25, y:cy, w:4.52, h:0.51, fill:{color:C.white}, rectRadius:0.08, shadow:mkShadow()
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x:5.25, y:cy, w:0.18, h:0.51, fill:{color:bi.color}, line:{color:bi.color}
      });
      s.addText(bi.name, { x:5.5, y:cy+0.04, w:2.8, h:0.26, fontSize:10, color:C.navy, fontFace:"Arial", bold:true, margin:0 });
      s.addText(bi.amt, { x:8.25, y:cy+0.03, w:0.9, h:0.26, fontSize:13, color:bi.color, fontFace:"Arial", bold:true, align:"right", margin:0 });
      s.addText(bi.pct, { x:9.1, y:cy+0.05, w:0.58, h:0.22, fontSize:10, color:C.gray, fontFace:"Arial", margin:0 });
      s.addText(bi.note, { x:5.5, y:cy+0.3, w:4.18, h:0.17, fontSize:7.5, color:C.gray, fontFace:"Arial", margin:0 });
    });

    // 健康サービス注記
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:0.3, y:5.12, w:9.4, h:0.35, fill:{color:"D5F0E5"}, rectRadius:0.08
    });
    s.addText("▶ 健康・保健サービスに直接関わる費目：衛生費71億円＋民生費の一部（子育て・高齢者）＋教育費のスポーツ施設分。区民1人あたり年間約6万円を投じている計算。", {
      x:0.45, y:5.16, w:9.2, h:0.26, fontSize:8.5, color:"1A5A3A", fontFace:"Arial", margin:0
    });

    s.addNotes("令和7年度一般会計1,470億円の款別内訳。最大は民生費40.5%（653億円）。衛生費は4.4%（71億円）で保健・医療を担う。令和8年度は1,605億円に増加。");
  }

  // ================================================================
  // Slide 10: まとめ─区民が使えるサービス早見表
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addText("サービス早見表 ─ 自分に関係するものを探そう", {
      x:0.5, y:0.2, w:9, h:0.6, fontSize:22, color:C.white, fontFace:"Arial", bold:true, margin:0
    });
    s.addText("※利用条件・料金は変更の可能性あり。最新情報は文京区HP・各窓口で確認を", {
      x:0.5, y:0.78, w:9, h:0.28, fontSize:10.5, color:"8FBFDF", fontFace:"Arial", margin:0
    });

    s.addTable([
      [
        { text:"世代・状況", options:{ bold:true, color:C.white, fill:{color:C.navy}, fontSize:10, align:"center" } },
        { text:"主なサービス", options:{ bold:true, color:C.white, fill:{color:C.navy}, fontSize:10, align:"center" } },
        { text:"費用", options:{ bold:true, color:C.white, fill:{color:C.navy}, fontSize:10, align:"center" } },
        { text:"窓口・連絡先", options:{ bold:true, color:C.white, fill:{color:C.navy}, fontSize:10, align:"center" } },
      ],
      ["妊娠中の方", "妊婦健診（14回）・超音波（4回）・産後ケア（3回）", "健診：助成あり / 産後ケア：3,000円/回", "保健センター 03-5803-1834"],
      ["乳幼児のいる家庭", "乳幼児健診・定期予防接種・育児相談・子ども食堂", "健診・接種：無料 / 食堂：無料〜100円", "保健センター / 子育て支援課"],
      ["20歳以上の女性", "子宮がん検診（偶数年齢）", "無料", "区内委託医療機関へ電話予約"],
      ["40歳以上（国保）", "特定健診＋大腸・肺がん検診", "すべて無料", "区内指定医療機関へ電話予約"],
      ["40歳以上の女性", "乳がん検診（偶数年齢）", "無料", "区内委託医療機関"],
      ["スポーツしたい全員", "スポーツ交流ひろば（学校体育館）・各種目", "無料・申込不要", "直接会場へ / 文京区スポーツ振興課"],
      ["スポーツ施設利用者", "文京スポーツセンター プール・トレーニング", "一般550円〜 / 定期4,600円/月", "文京スポーツセンター 03-3946-6311"],
      ["65〜69歳", "プール280円・トレーニング300円（シルバー料金）", "約半額（事前登録要）", "文京スポーツセンター受付で登録"],
      ["70歳以上", "プール・トレーニングルーム利用", "無料", "文京スポーツセンター（登録証要）"],
      ["75歳以上", "後期高齢者健診・フレイル健診・介護予防教室", "無料", "担当医 / 保健センター / 包括支援センター"],
      ["65歳以上", "インフルエンザ接種・地域包括支援センター相談", "1,500円 / 相談無料", "区内指定医療機関 / センター6ヶ所"],
      ["悩みを抱える全員", "精神保健相談・ひきこもり・依存症・自殺予防", "無料（要予約）", "保健所 03-5803-1834"],
    ], {
      x:0.3, y:1.1, w:9.4,
      border:{ pt:0.5, color:"2C4A6E" },
      fontSize:8.5,
      fontFace:"Arial",
      color:C.white,
      rowH:0.31,
      fill:[
        { type:"solid", color:"1A3A5C" },
        { type:"solid", color:"1E3D60" },
        { type:"solid", color:"18365A" },
        { type:"solid", color:"1E3D60" },
        { type:"solid", color:"18365A" },
        { type:"solid", color:"1E3D60" },
        { type:"solid", color:"18365A" },
        { type:"solid", color:"1E3D60" },
        { type:"solid", color:"18365A" },
        { type:"solid", color:"1E3D60" },
        { type:"solid", color:"18365A" },
        { type:"solid", color:"1E3D60" },
        { type:"solid", color:"18365A" },
      ],
      colW:[2.2, 3.5, 1.8, 1.9]
    });

    s.addNotes("区民が自分に関係するサービスをすぐ見つけられる早見表。世代別・状況別に費用と窓口を整理。");
  }

  const outFile = "bunkyo_health_slides_v2.pptx";
  await pres.writeFile({ fileName: outFile });
  console.log("✅ Written:", outFile);
}

main().catch(err => { console.error(err); process.exit(1); });
