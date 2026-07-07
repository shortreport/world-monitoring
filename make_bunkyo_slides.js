const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaUniversity, FaLeaf, FaUsers, FaHeartbeat, FaHospital,
  FaBaby, FaUserMd, FaSearch, FaShieldAlt, FaHandHoldingHeart,
  FaSyringe, FaBrain, FaWalking, FaChartLine
} = require("react-icons/fa");
const { MdHealthAndSafety, MdElderly } = require("react-icons/md");

// ─── Color Palette ───────────────────────────────────────────────────
const C = {
  navy:     "1A3A5C",   // primary dark
  blue:     "1B6CA8",   // primary mid
  skyBlue:  "D6EAF8",   // light bg
  white:    "FFFFFF",
  offWhite: "F4F8FB",
  green:    "1A7F5A",   // health accent
  lightGreen: "D5F0E5",
  gold:     "D4A017",   // accent highlight
  dark:     "1C1C2E",
  gray:     "5D6D7E",
  lightGray:"ECF0F1",
};

// ─── Icon helper ────────────────────────────────────────────────────
async function iconPng(IconComp, color = "#FFFFFF", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComp, { color, size: String(size) })
  );
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ─── Shadow factory ──────────────────────────────────────────────────
const mkShadow = () => ({
  type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.12
});

// ─── Main ────────────────────────────────────────────────────────────
async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = "文京区 保健医療・健康サービス概要";

  // ================================================================
  // Slide 1: Title
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Decorative arc shape top-right
    s.addShape(pres.shapes.OVAL, {
      x: 7.5, y: -1.5, w: 4.5, h: 4.5,
      fill: { color: C.blue, transparency: 60 },
      line: { color: C.blue, width: 0 }
    });
    s.addShape(pres.shapes.OVAL, {
      x: 8.5, y: -0.5, w: 3.5, h: 3.5,
      fill: { color: "2980B9", transparency: 70 },
      line: { color: "2980B9", width: 0 }
    });

    // 文京区ロゴ的な緑の丸
    s.addShape(pres.shapes.OVAL, {
      x: 0.55, y: 0.55, w: 1.0, h: 1.0,
      fill: { color: C.green }
    });
    const leafIcon = await iconPng(FaLeaf, "#FFFFFF", 256);
    s.addImage({ data: leafIcon, x: 0.7, y: 0.68, w: 0.5, h: 0.5 });

    s.addText("文京区", {
      x: 1.7, y: 0.55, w: 3, h: 0.55,
      fontSize: 16, color: "8FBFDF", fontFace: "Arial", bold: true, margin: 0
    });

    // Main title
    s.addText("文京区の概要と", {
      x: 0.6, y: 1.45, w: 9, h: 0.8,
      fontSize: 38, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });
    s.addText("保健医療・健康サービス", {
      x: 0.6, y: 2.2, w: 9, h: 0.8,
      fontSize: 38, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 3.15, w: 2.5, h: 0.06,
      fill: { color: C.gold }
    });

    s.addText("文京区長 政策スタッフ資料", {
      x: 0.6, y: 3.35, w: 7, h: 0.35,
      fontSize: 14, color: "8FBFDF", fontFace: "Arial", margin: 0
    });
    s.addText("2026年7月", {
      x: 0.6, y: 3.75, w: 7, h: 0.3,
      fontSize: 12, color: "6A8EAE", fontFace: "Arial", margin: 0
    });

    // Bottom green strip
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 5.1, w: 10, h: 0.525,
      fill: { color: C.green }
    });
    s.addText("文教・健康・共生のまちづくり", {
      x: 0.5, y: 5.15, w: 9, h: 0.42,
      fontSize: 13, color: C.white, fontFace: "Arial", italic: true, align: "center", margin: 0
    });

    s.addNotes("タイトルスライド。文京区の全般的特徴と保健医療サービスの概要を説明する資料です。");
  }

  // ================================================================
  // Slide 2: 文京区プロフィール
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };

    // Header bar
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: C.navy }
    });
    s.addText("文京区 基本プロフィール", {
      x: 0.5, y: 0.1, w: 9, h: 0.65,
      fontSize: 22, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    // 4 stat cards
    const stats = [
      { label: "面積", value: "11.29", unit: "km²", sub: "東京23区中20位" },
      { label: "人口", value: "24.3", unit: "万人", sub: "(2025年推計)" },
      { label: "高齢化率", value: "20.4", unit: "%", sub: "65歳以上の割合" },
      { label: "大学・大学院", value: "15", unit: "校", sub: "都内有数の文教地区" },
    ];
    const cardW = 2.1, cardH = 1.6, startX = 0.3, startY = 1.0;
    stats.forEach((st, i) => {
      const cx = startX + i * (cardW + 0.18);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx, y: startY, w: cardW, h: cardH,
        fill: { color: C.white },
        rectRadius: 0.1,
        shadow: mkShadow()
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: startY, w: cardW, h: 0.38,
        fill: { color: C.navy },
        line: { color: C.navy }
      });
      s.addText(st.label, {
        x: cx, y: startY + 0.04, w: cardW, h: 0.32,
        fontSize: 12, color: C.white, fontFace: "Arial", bold: true, align: "center", margin: 0
      });
      s.addText(st.value, {
        x: cx, y: startY + 0.45, w: cardW, h: 0.65,
        fontSize: 36, color: C.blue, fontFace: "Arial", bold: true, align: "center", margin: 0
      });
      s.addText(st.unit, {
        x: cx, y: startY + 0.95, w: cardW, h: 0.3,
        fontSize: 13, color: C.gray, fontFace: "Arial", align: "center", margin: 0
      });
      s.addText(st.sub, {
        x: cx, y: startY + 1.25, w: cardW, h: 0.28,
        fontSize: 9, color: C.gray, fontFace: "Arial", align: "center", margin: 0
      });
    });

    // 特徴説明
    s.addText("区の主な特徴", {
      x: 0.5, y: 2.8, w: 9, h: 0.38,
      fontSize: 15, color: C.navy, fontFace: "Arial", bold: true, margin: 0
    });

    const features = [
      "東京大学・東京医科歯科大学・順天堂大学など、国内有数の医療・教育機関が集積する「文教都市」",
      "小石川・六義園などの庭園や護国寺・湯島聖堂などの歴史的資産が豊富",
      "23区のなかでも犯罪率が低く、良好な住環境と住民の高い生活満足度が特徴",
      "区民の年収・学歴水準が相対的に高く、健康意識の高いコミュニティが形成されている",
    ];
    features.forEach((f, i) => {
      s.addShape(pres.shapes.OVAL, {
        x: 0.4, y: 3.3 + i * 0.5, w: 0.22, h: 0.22,
        fill: { color: C.green }
      });
      s.addText(f, {
        x: 0.72, y: 3.28 + i * 0.5, w: 9.0, h: 0.35,
        fontSize: 11, color: C.dark, fontFace: "Arial", margin: 0
      });
    });

    s.addNotes("文京区の基本的な統計と特徴。人口約24万人、面積11.29km²の比較的小さな区ですが、大学・医療機関が集積し教育・文化水準が高い。");
  }

  // ================================================================
  // Slide 3: 文京区の3つの強み
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addText("文京区の３つの強み", {
      x: 0.5, y: 0.2, w: 9, h: 0.6,
      fontSize: 26, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });
    s.addText("教育・学術・緑のまちが生み出す高い生活・健康水準", {
      x: 0.5, y: 0.78, w: 9, h: 0.35,
      fontSize: 13, color: "8FBFDF", fontFace: "Arial", margin: 0
    });

    const uniIcon  = await iconPng(FaUniversity, "#FFFFFF", 256);
    const leafIcon = await iconPng(FaLeaf, "#FFFFFF", 256);
    const userIcon = await iconPng(FaUsers, "#FFFFFF", 256);

    const cols = [
      {
        title: "学術・医療の集積",
        icon: uniIcon,
        color: C.blue,
        items: [
          "東京大学（本郷・弥生）",
          "東京医科歯科大学",
          "順天堂大学・病院",
          "東洋大学・日本大学など",
          "医学・理工学・法学の拠点"
        ]
      },
      {
        title: "緑・歴史・文化",
        icon: leafIcon,
        color: C.green,
        items: [
          "小石川植物園・後楽園",
          "六義園・播磨坂さくら並木",
          "湯島聖堂・護国寺",
          "根津神社・湯島天神",
          "都内有数の公園面積率"
        ]
      },
      {
        title: "住みやすい生活環境",
        icon: userIcon,
        color: "B87333",
        items: [
          "低犯罪率の安全なまち",
          "充実した商業・交通網",
          "高い区民満足度",
          "活発な地域コミュニティ",
          "子育て・高齢者支援も充実"
        ]
      }
    ];

    const cw = 2.8, startX = 0.3, startY = 1.3;
    for (let i = 0; i < cols.length; i++) {
      const col = cols[i];
      const cx = startX + i * (cw + 0.25);

      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx, y: startY, w: cw, h: 4.0,
        fill: { color: "1E3A5F", transparency: 10 },
        rectRadius: 0.12,
        shadow: mkShadow()
      });

      // Icon circle
      s.addShape(pres.shapes.OVAL, {
        x: cx + (cw - 0.7) / 2, y: startY + 0.2, w: 0.7, h: 0.7,
        fill: { color: col.color }
      });
      s.addImage({ data: col.icon, x: cx + (cw - 0.45) / 2, y: startY + 0.32, w: 0.45, h: 0.45 });

      s.addText(col.title, {
        x: cx + 0.1, y: startY + 1.05, w: cw - 0.2, h: 0.45,
        fontSize: 14, color: C.white, fontFace: "Arial", bold: true, align: "center", margin: 0
      });

      col.items.forEach((item, j) => {
        s.addShape(pres.shapes.OVAL, {
          x: cx + 0.18, y: startY + 1.62 + j * 0.44, w: 0.14, h: 0.14,
          fill: { color: col.color }
        });
        s.addText(item, {
          x: cx + 0.38, y: startY + 1.58 + j * 0.44, w: cw - 0.48, h: 0.35,
          fontSize: 10.5, color: "D0E8FF", fontFace: "Arial", margin: 0
        });
      });
    }

    s.addNotes("文京区の3つの強みを紹介。学術・医療機関の集積、豊かな緑と歴史文化、そして住みやすい生活環境が区の特色。");
  }

  // ================================================================
  // Slide 4: 保健医療体制（概要）
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };

    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: C.green }
    });
    s.addText("保健医療サービス体制", {
      x: 0.5, y: 0.1, w: 9, h: 0.65,
      fontSize: 22, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    // Left: 文京区保健所
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.3, y: 1.0, w: 4.5, h: 4.4,
      fill: { color: C.white },
      rectRadius: 0.12,
      shadow: mkShadow()
    });
    const hospIcon = await iconPng(FaHospital, "#1A7F5A", 256);
    s.addShape(pres.shapes.OVAL, {
      x: 0.7, y: 1.15, w: 0.65, h: 0.65,
      fill: { color: C.lightGreen }
    });
    s.addImage({ data: hospIcon, x: 0.82, y: 1.27, w: 0.42, h: 0.42 });

    s.addText("文京区保健所・保健センター", {
      x: 1.45, y: 1.2, w: 3.2, h: 0.6,
      fontSize: 13, color: C.navy, fontFace: "Arial", bold: true, margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 1.92, w: 4.1, h: 0.03,
      fill: { color: C.lightGreen }
    });

    const hoItems = [
      "感染症対策・食品衛生・環境衛生",
      "精神保健福祉相談",
      "難病患者支援",
      "保健センター（茗荷谷）での健康相談",
      "区民健康診査の実施・委託管理",
      "母子保健（妊婦・乳児訪問など）",
    ];
    hoItems.forEach((item, j) => {
      s.addShape(pres.shapes.OVAL, {
        x: 0.5, y: 2.07 + j * 0.48, w: 0.15, h: 0.15,
        fill: { color: C.green }
      });
      s.addText(item, {
        x: 0.75, y: 2.03 + j * 0.48, w: 3.9, h: 0.38,
        fontSize: 10.5, color: C.dark, fontFace: "Arial", margin: 0
      });
    });

    // Right: 区内医療機関
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 5.1, y: 1.0, w: 4.55, h: 4.4,
      fill: { color: C.white },
      rectRadius: 0.12,
      shadow: mkShadow()
    });
    const mdIcon = await iconPng(FaUserMd, "#1B6CA8", 256);
    s.addShape(pres.shapes.OVAL, {
      x: 5.5, y: 1.15, w: 0.65, h: 0.65,
      fill: { color: C.skyBlue }
    });
    s.addImage({ data: mdIcon, x: 5.62, y: 1.27, w: 0.42, h: 0.42 });

    s.addText("区内の医療資源", {
      x: 6.25, y: 1.2, w: 3.2, h: 0.6,
      fontSize: 13, color: C.navy, fontFace: "Arial", bold: true, margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.25, y: 1.92, w: 4.25, h: 0.03,
      fill: { color: C.skyBlue }
    });

    const medItems = [
      ["大学病院", "東京医科歯科大・順天堂大・東大附属"],
      ["総合病院", "日本医科大学付属・富士見台病院 等"],
      ["診療所", "区内に約600施設（内科・小児科等）"],
      ["歯科", "区内約280施設"],
      ["薬局", "区内約180施設"],
      ["訪問看護", "ステーション複数、在宅医療に対応"],
    ];
    medItems.forEach(([title, desc], j) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 5.2, y: 2.07 + j * 0.49, w: 4.3, h: 0.42,
        fill: { color: C.offWhite },
        rectRadius: 0.06
      });
      s.addText(title + "　", {
        x: 5.3, y: 2.1 + j * 0.49, w: 1.1, h: 0.35,
        fontSize: 9.5, color: C.blue, fontFace: "Arial", bold: true, margin: 0
      });
      s.addText(desc, {
        x: 6.35, y: 2.1 + j * 0.49, w: 3.0, h: 0.35,
        fontSize: 9.5, color: C.dark, fontFace: "Arial", margin: 0
      });
    });

    s.addNotes("文京区の保健医療体制の全体像。保健所・保健センターが公的サービスを担い、大学病院を含む豊富な医療資源が民間で補完している。");
  }

  // ================================================================
  // Slide 5: 健康診査・がん検診
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };

    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: C.navy }
    });
    s.addText("健康診査・がん検診事業", {
      x: 0.5, y: 0.1, w: 9, h: 0.65,
      fontSize: 22, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    // 特定健診
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.3, y: 1.0, w: 4.4, h: 2.0,
      fill: { color: C.white }, rectRadius: 0.1, shadow: mkShadow()
    });
    const searchIcon = await iconPng(FaSearch, "#1B6CA8", 256);
    s.addShape(pres.shapes.OVAL, { x: 0.55, y: 1.13, w: 0.6, h: 0.6, fill: { color: C.skyBlue } });
    s.addImage({ data: searchIcon, x: 0.67, y: 1.25, w: 0.38, h: 0.38 });
    s.addText("特定健康診査（メタボ健診）", {
      x: 1.25, y: 1.12, w: 3.35, h: 0.55, fontSize: 12,
      color: C.navy, fontFace: "Arial", bold: true, margin: 0
    });
    const tokItems = [
      "対象：40〜74歳の国保加入者",
      "内容：腹囲・血液・尿・血圧・問診",
      "受診率向上のため個別通知・電話勧奨",
      "区内委託医療機関で受診可能",
    ];
    tokItems.forEach((t, j) => {
      s.addText("・" + t, {
        x: 0.55, y: 1.75 + j * 0.29, w: 4.0, h: 0.27,
        fontSize: 10, color: C.dark, fontFace: "Arial", margin: 0
      });
    });

    // がん検診
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 5.1, y: 1.0, w: 4.55, h: 2.0,
      fill: { color: C.white }, rectRadius: 0.1, shadow: mkShadow()
    });
    const shieldIcon = await iconPng(FaShieldAlt, "#1A7F5A", 256);
    s.addShape(pres.shapes.OVAL, { x: 5.35, y: 1.13, w: 0.6, h: 0.6, fill: { color: C.lightGreen } });
    s.addImage({ data: shieldIcon, x: 5.47, y: 1.25, w: 0.38, h: 0.38 });
    s.addText("がん検診（無料・低額）", {
      x: 6.05, y: 1.12, w: 3.45, h: 0.55, fontSize: 12,
      color: C.navy, fontFace: "Arial", bold: true, margin: 0
    });
    const cancerItems = [
      "胃がん・肺がん・大腸がん（毎年）",
      "子宮頸がん・乳がん（2年に1回）",
      "前立腺がん検診（50歳以上男性）",
      "区内集団検診＋医療機関個別検診",
    ];
    cancerItems.forEach((t, j) => {
      s.addText("・" + t, {
        x: 5.3, y: 1.75 + j * 0.29, w: 4.2, h: 0.27,
        fontSize: 10, color: C.dark, fontFace: "Arial", margin: 0
      });
    });

    // 受診率グラフ（棒グラフ）
    s.addText("特定健診 受診率の推移（国保加入者）", {
      x: 0.5, y: 3.15, w: 9, h: 0.35,
      fontSize: 13, color: C.navy, fontFace: "Arial", bold: true, margin: 0
    });
    s.addChart(pres.charts.BAR, [{
      name: "受診率(%)",
      labels: ["2020年度", "2021年度", "2022年度", "2023年度", "2024年度"],
      values: [38.2, 36.8, 40.1, 42.3, 44.5]
    }], {
      x: 0.4, y: 3.55, w: 5.5, h: 1.85,
      barDir: "col",
      chartColors: [C.blue],
      chartArea: { fill: { color: C.white }, roundedCorners: true },
      catAxisLabelColor: C.gray,
      valAxisLabelColor: C.gray,
      valGridLine: { color: "E2E8F0", size: 0.5 },
      catGridLine: { style: "none" },
      showValue: true,
      dataLabelColor: "1E293B",
      showLegend: false,
    });

    // 目標と課題
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 6.1, y: 3.55, w: 3.6, h: 1.85,
      fill: { color: C.lightGreen }, rectRadius: 0.1
    });
    s.addText("目標・課題", {
      x: 6.25, y: 3.65, w: 3.3, h: 0.35,
      fontSize: 12, color: C.green, fontFace: "Arial", bold: true, margin: 0
    });
    const goals = [
      "国目標：特定健診受診率60%",
      "文京区現状：44.5%（改善中）",
      "受診勧奨の強化が喫緊の課題",
      "若年・現役世代への働きかけ",
    ];
    goals.forEach((g, j) => {
      s.addText("▶ " + g, {
        x: 6.2, y: 4.08 + j * 0.32, w: 3.4, h: 0.28,
        fontSize: 9.5, color: C.dark, fontFace: "Arial", margin: 0
      });
    });

    s.addNotes("健康診査・がん検診事業の概要。受診率は改善傾向にあるが、国目標の60%には届いていない。勧奨強化が課題。");
  }

  // ================================================================
  // Slide 6: 母子保健・子育て支援
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };

    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: "7B4FA6" }  // purple for maternal health
    });
    s.addText("母子保健・子育て支援", {
      x: 0.5, y: 0.1, w: 9, h: 0.65,
      fontSize: 22, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    const babyIcon = await iconPng(FaBaby, "#7B4FA6", 256);
    const heartIcon = await iconPng(FaHandHoldingHeart, "#7B4FA6", 256);

    // 左カラム：妊娠・出産
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.3, y: 1.0, w: 4.4, h: 4.35,
      fill: { color: C.white }, rectRadius: 0.12, shadow: mkShadow()
    });
    s.addShape(pres.shapes.OVAL, { x: 1.9, y: 1.12, w: 0.7, h: 0.7, fill: { color: "F3E5F5" } });
    s.addImage({ data: babyIcon, x: 2.02, y: 1.24, w: 0.46, h: 0.46 });
    s.addText("妊娠・出産サポート", {
      x: 0.4, y: 1.9, w: 4.2, h: 0.4,
      fontSize: 14, color: "7B4FA6", fontFace: "Arial", bold: true, align: "center", margin: 0
    });
    const birthItems = [
      ["妊娠届・母子手帳交付", "区役所・保健センターで対応"],
      ["妊婦健診費助成", "14回分の健診費を全額補助"],
      ["両親学級・出産準備教室", "プレパパ・プレママ向け"],
      ["産後ケア事業", "ショートステイ・デイサービス"],
      ["乳児全戸訪問（こんにちは赤ちゃん）", "生後4ヶ月以内に保健師が訪問"],
      ["育児不安相談", "保健センターに専任スタッフ"],
    ];
    birthItems.forEach(([title, desc], j) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.45, y: 2.4 + j * 0.47, w: 4.1, h: 0.4,
        fill: { color: "FAF5FF" }, rectRadius: 0.07
      });
      s.addText(title, {
        x: 0.6, y: 2.43 + j * 0.47, w: 2.4, h: 0.32,
        fontSize: 9.5, color: "6B21A8", fontFace: "Arial", bold: true, margin: 0
      });
      s.addText(desc, {
        x: 2.95, y: 2.43 + j * 0.47, w: 1.5, h: 0.32,
        fontSize: 8.5, color: C.gray, fontFace: "Arial", margin: 0
      });
    });

    // 右カラム：乳幼児〜学童
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 5.1, y: 1.0, w: 4.55, h: 4.35,
      fill: { color: C.white }, rectRadius: 0.12, shadow: mkShadow()
    });
    s.addShape(pres.shapes.OVAL, { x: 7.0, y: 1.12, w: 0.7, h: 0.7, fill: { color: "FCE4EC" } });
    s.addImage({ data: heartIcon, x: 7.12, y: 1.24, w: 0.46, h: 0.46 });
    s.addText("乳幼児・学童期の支援", {
      x: 5.2, y: 1.9, w: 4.3, h: 0.4,
      fontSize: 14, color: "C62828", fontFace: "Arial", bold: true, align: "center", margin: 0
    });
    const childItems = [
      ["乳幼児健診", "3〜4ヶ月・9〜10ヶ月・1歳6ヶ月・3歳"],
      ["予防接種", "定期接種を原則無料で実施"],
      ["発達相談・療育支援", "専門職による早期支援体制"],
      ["保育所・認定こども園", "待機児童ゼロ継続を目指す"],
      ["小児科医療連携", "区内診療所との緊密な連携"],
      ["子ども食堂・地域支援", "孤食防止・食育の推進"],
    ];
    childItems.forEach(([title, desc], j) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 5.25, y: 2.4 + j * 0.47, w: 4.25, h: 0.4,
        fill: { color: "FFF3F3" }, rectRadius: 0.07
      });
      s.addText(title, {
        x: 5.38, y: 2.43 + j * 0.47, w: 2.2, h: 0.32,
        fontSize: 9.5, color: "B71C1C", fontFace: "Arial", bold: true, margin: 0
      });
      s.addText(desc, {
        x: 7.5, y: 2.43 + j * 0.47, w: 1.75, h: 0.32,
        fontSize: 8.5, color: C.gray, fontFace: "Arial", margin: 0
      });
    });

    s.addNotes("母子保健サービスは妊娠届から学童期まで一貫したサポートを実施。産後ケア事業と全戸訪問が孤立育児の防止に重要。");
  }

  // ================================================================
  // Slide 7: 高齢者・介護予防
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };

    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: "B45309" }
    });
    s.addText("高齢者保健・介護予防サービス", {
      x: 0.5, y: 0.1, w: 9, h: 0.65,
      fontSize: 22, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    const walkIcon = await iconPng(FaWalking, "#B45309", 256);
    const brainIcon = await iconPng(FaBrain, "#1B6CA8", 256);
    const syringeIcon = await iconPng(FaSyringe, "#1A7F5A", 256);
    const chartIcon = await iconPng(FaChartLine, "#C62828", 256);

    // 4象限カード
    const cards = [
      {
        title: "地域包括支援センター",
        icon: walkIcon,
        color: "FEF3C7",
        iconBg: "FDE68A",
        textColor: "92400E",
        items: [
          "区内6ヶ所に設置",
          "介護・医療・福祉の総合相談窓口",
          "ケアマネジャーの支援・指導",
          "認知症初期集中支援",
        ]
      },
      {
        title: "介護予防事業",
        icon: brainIcon,
        color: "DBEAFE",
        iconBg: "BFDBFE",
        textColor: "1E3A8A",
        items: [
          "いきいき体操教室（転倒予防）",
          "認知症予防プログラム",
          "社会参加・就労支援",
          "フレイル健診（75歳以上）",
        ]
      },
      {
        title: "予防接種（高齢者）",
        icon: syringeIcon,
        color: "DCFCE7",
        iconBg: "BBF7D0",
        textColor: "14532D",
        items: [
          "インフルエンザワクチン（65歳以上）",
          "肺炎球菌ワクチン（定期接種）",
          "帯状疱疹ワクチン（50歳以上助成）",
          "新型コロナ（最新情報に準拠）",
        ]
      },
      {
        title: "在宅医療・介護連携",
        icon: chartIcon,
        color: "FCE7F3",
        iconBg: "FBCFE8",
        textColor: "831843",
        items: [
          "文京区在宅療養推進協議会",
          "かかりつけ医・訪問看護との連携",
          "24時間対応の在宅医療体制整備",
          "ACP（人生会議）普及啓発",
        ]
      },
    ];

    const cw = 4.5, ch = 2.2;
    cards.forEach((card, i) => {
      const cx = i % 2 === 0 ? 0.3 : 5.2;
      const cy = i < 2 ? 1.0 : 3.3;

      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx, y: cy, w: cw, h: ch,
        fill: { color: card.color }, rectRadius: 0.12, shadow: mkShadow()
      });

      s.addShape(pres.shapes.OVAL, {
        x: cx + 0.2, y: cy + 0.2, w: 0.6, h: 0.6,
        fill: { color: card.iconBg }
      });
      s.addImage({ data: card.icon, x: cx + 0.32, y: cy + 0.32, w: 0.38, h: 0.38 });

      s.addText(card.title, {
        x: cx + 0.9, y: cy + 0.22, w: cw - 1.0, h: 0.55,
        fontSize: 12, color: card.textColor, fontFace: "Arial", bold: true, margin: 0
      });

      card.items.forEach((item, j) => {
        s.addText("▶ " + item, {
          x: cx + 0.2, y: cy + 0.88 + j * 0.31, w: cw - 0.35, h: 0.27,
          fontSize: 9.5, color: C.dark, fontFace: "Arial", margin: 0
        });
      });
    });

    s.addNotes("高齢者向けサービス。地域包括支援センターを中心に、介護予防・在宅医療連携・予防接種を総合的に展開している。");
  }

  // ================================================================
  // Slide 8: 精神保健・こころの健康
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addText("こころの健康支援・精神保健", {
      x: 0.5, y: 0.2, w: 9, h: 0.6,
      fontSize: 24, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });
    s.addText("メンタルヘルスの課題に地域全体で向き合う", {
      x: 0.5, y: 0.78, w: 9, h: 0.35,
      fontSize: 13, color: "8FBFDF", fontFace: "Arial", margin: 0
    });

    // 主な施策
    const services = [
      {
        num: "01",
        title: "精神保健福祉相談",
        desc: "保健所の専門相談員（保健師・精神保健福祉士）による個別相談。本人だけでなく家族からの相談も受け付け。予約制・無料。"
      },
      {
        num: "02",
        title: "アルコール・依存症支援",
        desc: "アルコール問題・薬物・ギャンブル依存に関する相談窓口を設置。自助グループへのつなぎ・専門機関紹介を実施。"
      },
      {
        num: "03",
        title: "自殺予防・ゲートキーパー研修",
        desc: "区内自殺者数の削減を目標に、ゲートキーパー養成研修を毎年実施。「いのちの電話」等相談機関との連携強化。"
      },
      {
        num: "04",
        title: "ひきこもり支援",
        desc: "8050問題・ひきこもり長期化に対応。訪問支援・居場所づくり・社会復帰に向けた段階的サポート体制を整備。"
      },
      {
        num: "05",
        title: "認知症支援",
        desc: "認知症初期集中支援チーム（地域包括支援センター）による早期発見・介入。認知症サポーター養成講座を区内全域で展開。"
      },
    ];

    services.forEach((sv, i) => {
      const cy = 1.3 + i * 0.87;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.4, y: cy, w: 9.2, h: 0.78,
        fill: { color: "1E3A5F", transparency: 10 },
        rectRadius: 0.1
      });
      s.addShape(pres.shapes.OVAL, {
        x: 0.55, y: cy + 0.14, w: 0.5, h: 0.5,
        fill: { color: C.blue }
      });
      s.addText(sv.num, {
        x: 0.55, y: cy + 0.14, w: 0.5, h: 0.5,
        fontSize: 11, color: C.white, fontFace: "Arial", bold: true, align: "center", valign: "middle", margin: 0
      });
      s.addText(sv.title + "　", {
        x: 1.15, y: cy + 0.1, w: 2.3, h: 0.55,
        fontSize: 12, color: "93C5FD", fontFace: "Arial", bold: true, margin: 0
      });
      s.addText(sv.desc, {
        x: 3.35, y: cy + 0.1, w: 6.1, h: 0.55,
        fontSize: 9.5, color: "D0E8FF", fontFace: "Arial", margin: 0
      });
    });

    s.addNotes("精神保健サービス。相談窓口・依存症対応・自殺予防・ひきこもり・認知症の5本柱で展開。全世代のこころの健康を支える。");
  }

  // ================================================================
  // Slide 9: 生活習慣病対策・健康増進
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };

    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: C.green }
    });
    s.addText("生活習慣病対策・健康増進施策", {
      x: 0.5, y: 0.1, w: 9, h: 0.65,
      fontSize: 22, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });

    // 3コラム
    const cols = [
      {
        title: "食育・栄養改善",
        color: "F0FFF4",
        borderColor: C.green,
        items: [
          "栄養相談（個別・グループ）",
          "食育推進計画に基づく啓発",
          "学校給食との連携",
          "糖尿病予防食事指導",
          "減塩・野菜摂取推進キャンペーン",
          "食品表示・食の安全普及",
        ]
      },
      {
        title: "運動・身体活動",
        color: "EFF6FF",
        borderColor: C.blue,
        items: [
          "区立体育館・スポーツ施設の活用",
          "ウォーキングマップの配布",
          "運動教室（高齢者・成人向け）",
          "eスポーツ・ラジオ体操推進",
          "区内公園を活用した健康増進",
          "企業健康経営との連携",
        ]
      },
      {
        title: "たばこ・飲酒対策",
        color: "FFF7ED",
        borderColor: "D97706",
        items: [
          "禁煙外来への助成制度",
          "区内分煙・禁煙エリアの拡大",
          "妊婦・若者への喫煙啓発",
          "節度ある飲酒（適正飲酒）指導",
          "未成年飲酒防止啓発",
          "COPD予防の普及活動",
        ]
      },
    ];

    const cw = 2.95;
    cols.forEach((col, i) => {
      const cx = 0.3 + i * (cw + 0.22);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx, y: 1.0, w: cw, h: 4.4,
        fill: { color: col.color }, rectRadius: 0.12,
        shadow: mkShadow()
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: 1.0, w: cw, h: 0.5,
        fill: { color: col.borderColor },
        line: { color: col.borderColor }
      });
      s.addText(col.title, {
        x: cx, y: 1.05, w: cw, h: 0.4,
        fontSize: 12, color: C.white, fontFace: "Arial", bold: true, align: "center", margin: 0
      });
      col.items.forEach((item, j) => {
        s.addShape(pres.shapes.OVAL, {
          x: cx + 0.2, y: 1.65 + j * 0.49, w: 0.14, h: 0.14,
          fill: { color: col.borderColor }
        });
        s.addText(item, {
          x: cx + 0.42, y: 1.62 + j * 0.49, w: cw - 0.55, h: 0.42,
          fontSize: 10, color: C.dark, fontFace: "Arial", margin: 0
        });
      });
    });

    s.addNotes("生活習慣病予防の3本柱：食育、運動、禁煙・適正飲酒。地域全体でのアプローチが重要。企業・学校との連携も推進中。");
  }

  // ================================================================
  // Slide 10: まとめ・ビジョン
  // ================================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent
    s.addShape(pres.shapes.OVAL, {
      x: -1, y: -1, w: 4, h: 4,
      fill: { color: C.blue, transparency: 75 }
    });

    s.addText("文京区が目指す健康のまち", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.65,
      fontSize: 26, color: C.white, fontFace: "Arial", bold: true, margin: 0
    });
    s.addText("〜すべての区民が健やかに暮らせる文京区へ〜", {
      x: 0.6, y: 0.9, w: 8.8, h: 0.38,
      fontSize: 13, color: "8FBFDF", fontFace: "Arial", italic: true, margin: 0
    });

    // 5本柱
    const pillars = [
      { no: "1", label: "予防と早期発見",  desc: "健診・がん検診の受診率向上、\n個別勧奨の強化" },
      { no: "2", label: "切れ目のない支援", desc: "妊娠〜高齢期まで一貫した\n保健サービスの連続性" },
      { no: "3", label: "こころの健康",    desc: "精神保健・認知症・\nひきこもりへの包括支援" },
      { no: "4", label: "地域連携の強化",  desc: "医療機関・大学・企業と\n行政が一体となった体制" },
      { no: "5", label: "データ活用と評価", desc: "PHR・健康データを活用した\n施策の効果測定と改善" },
    ];

    pillars.forEach((p, i) => {
      const cx = 0.3 + i * 1.9;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx, y: 1.5, w: 1.75, h: 3.8,
        fill: { color: "1E3A5F" }, rectRadius: 0.12,
        shadow: mkShadow()
      });
      s.addShape(pres.shapes.OVAL, {
        x: cx + 0.53, y: 1.65, w: 0.7, h: 0.7,
        fill: { color: C.green }
      });
      s.addText(p.no, {
        x: cx + 0.53, y: 1.65, w: 0.7, h: 0.7,
        fontSize: 20, color: C.white, fontFace: "Arial", bold: true,
        align: "center", valign: "middle", margin: 0
      });
      s.addText(p.label, {
        x: cx + 0.1, y: 2.45, w: 1.55, h: 0.6,
        fontSize: 11, color: "93C5FD", fontFace: "Arial", bold: true,
        align: "center", margin: 0
      });
      s.addText(p.desc, {
        x: cx + 0.1, y: 3.12, w: 1.55, h: 1.2,
        fontSize: 9, color: "D0E8FF", fontFace: "Arial",
        align: "center", margin: 0
      });
    });

    // Bottom quote
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 5.1, w: 9.0, h: 0.4,
      fill: { color: C.green, transparency: 20 }, rectRadius: 0.08
    });
    s.addText(
      "文京区の豊かな医療・学術資源を地域の健康づくりに最大限活用し、「健康長寿・共生社会」を実現します",
      {
        x: 0.5, y: 5.13, w: 9.0, h: 0.34,
        fontSize: 10, color: C.white, fontFace: "Arial", align: "center", margin: 0
      }
    );

    s.addNotes("まとめスライド。予防・切れ目のない支援・こころの健康・地域連携・データ活用の5本柱で文京区の健康施策を推進する。");
  }

  // ─── Output ───────────────────────────────────────────────────────
  const outFile = "bunkyo_health_slides.pptx";
  await pres.writeFile({ fileName: outFile });
  console.log("✅ Written:", outFile);
}

main().catch(err => { console.error(err); process.exit(1); });
