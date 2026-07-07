"use strict";
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "経営企画部";
pres.title = "中国国務院令第837号：対外投資規制分析";

const C = {
  navy:"1E2761", blue:"2E5EAA", ltblue:"DBEAFE", iceblue:"CADCFC",
  red:"C0392B",  ltred:"FEE2E2",
  amber:"E67E22", ltamber:"FEF9C3",
  green:"27AE60", ltgreen:"DCFCE7",
  teal:"0891B2",  ltteal:"CFFAFE",
  purple:"7C3AED", ltpurple:"EDE9FE",
  white:"FFFFFF", offwhite:"F7F8FC",
  gray:"64748B",  darkgray:"334155", lightgray:"E2E8F0",
};

function ms() { return {type:"outer",blur:6,offset:2,angle:135,color:"000000",opacity:0.10}; }
function box(s,x,y,w,h,fill,lc,lw) {
  s.addShape(pres.shapes.RECTANGLE,{x,y,w,h,fill:{color:fill||C.white},
    line:lc?{color:lc,pt:lw||1}:{type:"none"}});
}
function oval(s,x,y,r,fill) {
  s.addShape(pres.shapes.OVAL,{x:x-r,y:y-r,w:r*2,h:r*2,fill:{color:fill},line:{type:"none"}});
}
function tt(s,text,opts) {
  s.addText(text,{fontFace:"Meiryo",margin:0,...opts});
}
function footer(s,src) {
  tt(s,"出所："+src,{x:0.35,y:5.34,w:9.3,h:0.22,fontSize:7.5,color:"94A3B8"});
}
function titleBlock(s,title,sub) {
  box(s,0.35,0.15,0.05,0.46,C.amber);
  tt(s,title,{x:0.5,y:0.15,w:9.1,h:0.36,fontSize:20,bold:true,color:C.navy});
  if(sub) tt(s,sub,{x:0.5,y:0.52,w:9.1,h:0.22,fontSize:9.5,color:C.gray});
  box(s,0.35,0.76,9.3,0.018,C.lightgray);
}
function badge(s,text,x,y,w,color) {
  box(s,x,y,w,0.22,color);
  tt(s,text,{x:x+0.04,y,w:w-0.08,h:0.22,fontSize:7.5,bold:true,color:C.white,align:"center",valign:"middle"});
}

// ============================================================
// Slide 1: 表紙
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.navy};
  box(s,0,0,0.22,5.625,C.amber);
  box(s,0.22,0,9.78,0.06,C.iceblue);
  box(s,0.22,5.56,9.78,0.065,C.iceblue);

  tt(s,"中国 国務院令第837号",{x:0.55,y:0.65,w:9,h:0.7,fontSize:36,bold:true,color:C.white});
  tt(s,"対外投資規制の全体像と日本企業への影響",{x:0.55,y:1.45,w:9,h:0.55,fontSize:22,color:C.iceblue});
  box(s,0.55,2.15,4.5,0.04,C.amber);

  const pts=[
    "中国初の対外投資専門行政法規（国務院令）",
    "2026年6月1日公布　→　7月1日施行",
    "促進と規制の二面性：BRI推進 vs 機微技術管理強化",
    "中国資本増加が日本企業に与えるインパクト分析",
  ];
  pts.forEach((p,i)=>{
    oval(s,0.65,2.55+i*0.52,0.06,C.amber);
    tt(s,p,{x:0.8,y:2.43+i*0.52,w:8.5,h:0.4,fontSize:13,color:C.white});
  });

  tt(s,"2026年7月　経営企画部",{x:0.55,y:5.2,w:9,h:0.28,fontSize:11,color:C.gray});
}

// ============================================================
// Slide 2: エグゼクティブサマリー
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"エグゼクティブサマリー","国務院令第837号 — 経営幹部が今すぐ把握すべき3点");

  const cards=[
    {
      title:"① 中国初の「対外投資専門」行政法規",
      color:C.blue,bg:C.ltblue,
      pts:[
        "従来は発改委・商務部・外為局の部門規定が乱立",
        "今回初めて国務院令（法的拘束力の強い行政法規）として統合",
        "国家安全審査・禁止事項・罰則が一本化",
      ],
      tag:"法制度の転換"
    },
    {
      title:"② 「促進」と「規制」の二面性",
      color:C.amber,bg:C.ltamber,
      pts:[
        "【促進】投資自主権の保護、政府支援体制、BRI推進",
        "【規制】機微技術・データの国外移転禁止（第13・14条）",
        "【審査】国家安全に関わる投資は事前審査が必要（第15条）",
      ],
      tag:"双方向のリスク"
    },
    {
      title:"③ 日本企業への実質的影響",
      color:C.green,bg:C.ltgreen,
      pts:[
        "中国資本の対日投資は増加傾向 → 837号で制度的裏付けが強化",
        "技術・データを持つ日本企業は「中国側の規制対象」にも入り得る",
        "外為法（日本）× 国務院令837号（中国）の二重規制時代へ",
      ],
      tag:"今すぐ対応必要"
    },
  ];

  cards.forEach((c,i)=>{
    const x=0.3+i*3.24, y=1.02;
    box(s,x,y,2.9,4.22,c.bg,c.color);
    box(s,x,y,2.9,0.5,c.color);
    badge(s,c.tag,x+0.08,y+0.14,1.5,C.darkgray);
    tt(s,c.title,{x:x+0.1,y:y+0.6,w:2.72,h:0.52,fontSize:11,bold:true,color:C.darkgray});
    c.pts.forEach((p,j)=>{
      oval(s,x+0.22,y+1.22+j*0.82,0.05,c.color);
      tt(s,p,{x:x+0.35,y:y+1.1+j*0.82,w:2.5,h:0.7,fontSize:9,color:C.darkgray,valign:"top"});
    });
  });
}

// ============================================================
// Slide 3: 中国政府の最近の動き（対外投資政策の変遷）
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"中国政府の最近の動き","対外投資政策は「野放し→管理→法制化」の3段階で進化");

  const events=[
    {y:"2017",label:"資本流出規制強化",body:"急拡大する対外投資に対し不動産・娯楽等への規制を強化。企業の海外資産売却も加速。「走出去」の乱れを引き締め。",color:C.red},
    {y:"2021",label:"BRI・双循環戦略加速",body:"一帯一路（BRI）推進と国内外循環の補完政策として、対外投資の戦略的活用を打ち出し。製造業・インフラ・資源確保を優先。",color:C.blue},
    {y:"2023",label:"米中技術デカップリング深化",body:"米国の半導体・AI規制強化を受け、中国は技術の海外流出防止と国際競争力維持の両立が急務に。対外投資管理の空白が問題視される。",color:C.amber},
    {y:"2025.06",label:"60日支払い規制施行",body:"中小企業代金支払保障条例施行。BYD等大手のサプライチェーン金融問題が国際的に注目され、中国企業の「信用」管理が課題に浮上。",color:C.teal},
    {y:"2026.07",label:"国務院令第837号 施行",body:"中国初の対外投資専門行政法規として統合・格上げ。機微技術管理・安全審査・個人投資家規制を明示化。全過程監督体制が確立。",color:C.green},
  ];

  events.forEach((e,i)=>{
    const x=0.35, y=0.95+i*0.88;
    box(s,x,y+0.14,0.72,0.28,e.color);
    tt(s,e.y,{x:x+0.03,y:y+0.14,w:0.66,h:0.28,fontSize:9,bold:true,color:C.white,align:"center",valign:"middle"});
    if(i<4) box(s,x+0.32,y+0.42,0.08,0.6,"CBD5E1");
    box(s,x+0.85,y+0.08,0.04,0.44,e.color);
    tt(s,e.label,{x:x+0.98,y:y+0.08,w:2.1,h:0.28,fontSize:10,bold:true,color:e.color});
    tt(s,e.body,{x:x+0.98,y:y+0.38,w:8.4,h:0.46,fontSize:8.5,color:C.darkgray,valign:"top"});
  });

  footer(s,"各種報道・ジェトロ・MOFCOM公表資料（2017〜2026）");
}

// ============================================================
// Slide 4: 中国の対外直接投資規模
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"中国の対外直接投資規模","2024年は2年連続増加、前年比+8.4%。世界トップ3の投資大国に");

  const data=[
    {yr:"2020",v:153},{yr:"2021",v:179},{yr:"2022",v:163},{yr:"2023",v:174},{yr:"2024",v:188},
  ];
  const maxV=200, chartB=4.7, chartH=3.0;
  const barW=0.72, gap=0.56, startX=0.9;

  // Y-axis gridlines
  [0,50,100,150,200].forEach(v=>{
    const yy=chartB-v/maxV*chartH;
    box(s,startX,yy-0.003,6.2,0.006,"D1D5DB");
    tt(s,"$"+v+"B",{x:0.05,y:yy-0.14,w:0.82,h:0.28,fontSize:8,color:C.gray,align:"right"});
  });

  data.forEach((d,i)=>{
    const bh = d.v/maxV*chartH;
    const bx = startX+i*(barW+gap);
    const by = chartB-bh;
    const col = i===4?C.green:C.blue;
    box(s,bx,by,barW,bh,col);
    tt(s,"$"+d.v+"B",{x:bx,y:by-0.3,w:barW,h:0.28,fontSize:9,bold:true,color:col,align:"center"});
    tt(s,d.yr,{x:bx,y:chartB+0.06,w:barW,h:0.24,fontSize:9,color:C.gray,align:"center"});
  });

  // Right side key stats
  const stats=[
    {v:"世界3位",l:"対外投資規模（2024）"},
    {v:"+8.4%",l:"2024年 前年比増加"},
    {v:"$1,760B",l:"累計ODI残高（2023末）"},
    {v:"190+",l:"投資対象国・地域数"},
  ];
  stats.forEach((st,i)=>{
    const y=1.08+i*0.9;
    box(s,7.4,y,2.3,0.8,i%2===0?C.ltblue:C.ltgreen,i%2===0?C.blue:C.green,0.75);
    tt(s,st.v,{x:7.45,y:y+0.04,w:2.2,h:0.38,fontSize:18,bold:true,color:i%2===0?C.blue:C.green,align:"center"});
    tt(s,st.l,{x:7.45,y:y+0.46,w:2.2,h:0.28,fontSize:8,color:C.darkgray,align:"center"});
  });

  footer(s,"MOFCOM 2025年統計公報 / UNCTAD World Investment Report 2025 / ジェトロ世界貿易投資報告2025");
}

// ============================================================
// Slide 5: なぜ今この法律が必要か（3つの背景）
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"なぜ今この法律が必要か","3つの構造的背景が重なり、「部門規定」では限界に達した");

  const reasons=[
    {
      n:"①",title:"既存規制の「空白」と乱立",color:C.blue,bg:C.ltblue,
      pts:[
        "対外投資は発改委（大規模）・商務部（一般）・外為局（外貨）が別々に管轄",
        "部門規定（規章）は法的拘束力が弱く、企業が違反しても刑事罰が科しにくい",
        "個人による対外投資が「グレーゾーン」のまま拡大",
        "監督当局が「現在の枠組みはもはや現状に合わない」と明言（Q&A文書）",
      ]
    },
    {
      n:"②",title:"地政学リスクの高まりと自国企業保護",color:C.amber,bg:C.ltamber,
      pts:[
        "米国が中国向け投資制限（EO 14105・CHIPS Act）を強化 → 中国も対等規制が必要",
        "BYD・CATL等の中国企業が海外で制裁・関税のリスクに直面",
        "対外投資のリスク情報提供・紛争解決サポートを政府が担う必要性",
        "一帯一路（BRI）推進を「法的根拠」で裏付けたいという政策ニーズ",
      ]
    },
    {
      n:"③",title:"技術・データ安全保障の法制化",color:C.green,bg:C.ltgreen,
      pts:[
        "AI・量子・半導体技術の国外流出が国家安全に直結するリスク認識の高まり",
        "技術者の国境越え赴任・研修が実質的な「技術移転」になるケースが多発",
        "データ（コアデータ・個人情報）の海外流出を既存の「データ安全法」だけで管理するのは困難",
        "「輸出管理法」との連動で、対外投資規制に安全保障の視点を組み込む必要",
      ]
    },
  ];

  reasons.forEach((r,i)=>{
    const x=0.28+i*3.22, y=0.95, w=3.1, h=4.4;
    box(s,x,y,w,h,r.bg,r.color);
    box(s,x,y,w,0.48,r.color);
    tt(s,r.n,{x:x+0.1,y:y+0.06,w:0.36,h:0.36,fontSize:18,bold:true,color:C.white});
    tt(s,r.title,{x:x+0.46,y:y+0.1,w:w-0.56,h:0.36,fontSize:10.5,bold:true,color:C.white});
    r.pts.forEach((p,j)=>{
      oval(s,x+0.2,y+0.72+j*0.84,0.05,r.color);
      tt(s,p,{x:x+0.32,y:y+0.6+j*0.84,w:w-0.42,h:0.75,fontSize:9,color:C.darkgray,valign:"top"});
    });
  });

  footer(s,"国務院Q&A文書「三部门负责人就《规定》答记者问」（2026年6月）");
}

// ============================================================
// Slide 6: 法律の全体構造（二面性）
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"法律の全体構造","「促進・支援」と「安全・規制」が並立する二面構造");

  // Center divider (thin separator)
  box(s,4.78,0.92,0.09,4.6,C.navy);
  // Center label badge
  box(s,4.45,1.12,0.75,0.52,C.navy);
  tt(s,"国務院令\n第837号",{x:4.47,y:1.12,w:0.71,h:0.52,fontSize:8,bold:true,color:C.white,align:"center",valign:"middle"});

  // Left: 促進 (green)
  box(s,0.3,0.92,4.44,4.6,C.ltgreen,C.green,1.5);
  box(s,0.3,0.92,4.44,0.44,C.green);
  tt(s,"促進・支援（第1〜12条）",{x:0.4,y:0.95,w:4.24,h:0.36,fontSize:13,bold:true,color:C.white});
  const lpnts=[
    {k:"投資自主権の保護",v:"投資者は法に基づき自主決定・自己リスク負担・自己採算"},
    {k:"政府支援体制",v:"海外リスク情報提供・保険・融資・紛争解決の総合サービス"},
    {k:"BRI推進",v:"一帯一路に沿った産業・インフラ投資を国が積極支持"},
    {k:"個人投資家の明示化",v:"初めて個人が「投資者」として法的に定義・権利が保護される"},
  ];
  lpnts.forEach((p,i)=>{
    box(s,0.45,1.44+i*0.8,4.12,0.72,C.white,C.green,0.5);
    tt(s,p.k,{x:0.55,y:1.48+i*0.8,w:3.92,h:0.22,fontSize:10,bold:true,color:C.green});
    tt(s,p.v,{x:0.55,y:1.7+i*0.8,w:3.92,h:0.4,fontSize:8.5,color:C.darkgray,valign:"top"});
  });

  // Right: 規制 (amber/red)
  box(s,4.92,0.92,4.73,4.6,C.ltamber,C.amber,1.5);
  box(s,4.92,0.92,4.73,0.44,C.amber);
  tt(s,"規制・安全保障（第13〜38条）",{x:5.02,y:0.95,w:4.53,h:0.36,fontSize:13,bold:true,color:C.white});
  const rpnts=[
    {k:"第13条：技術輸出禁止",v:"規制品の無断使用禁止、技術者越境派遣・研修の組織も対象"},
    {k:"第14条：データ越境制限",v:"コアデータ・重要データ・個人情報の国外移転に事前審査"},
    {k:"第15条：安全審査",v:"国家安全に関わる投資は発改委・商務部が合同審査"},
    {k:"第33〜38条：罰則",v:"投資額の0.5〜10‰の罰金、強制売却、1〜3年の投資禁止"},
  ];
  rpnts.forEach((p,i)=>{
    box(s,5.06,1.44+i*0.8,4.44,0.72,C.white,C.amber,0.5);
    tt(s,p.k,{x:5.16,y:1.48+i*0.8,w:4.24,h:0.22,fontSize:10,bold:true,color:C.amber});
    tt(s,p.v,{x:5.16,y:1.7+i*0.8,w:4.24,h:0.4,fontSize:8.5,color:C.darkgray,valign:"top"});
  });
}

// ============================================================
// Slide 7: 促進・支援の側面
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"促進・支援の側面（第1〜12条）","今回初めて法的根拠が与えられた「投資の権利と支援」");

  const supports=[
    {
      title:"投資自主権の法的保護",icon:"⚖",color:C.blue,
      desc:"投資者は市場化原則に基づく自主決定・自己リスク負担を有する（第3条）。法定外の規制を排除し、行政による過度な介入を禁止。中国企業が海外でより果敢に投資できる法的根拠。",
    },
    {
      title:"個人投資家を初めて明示（歴史的転換）",icon:"👤",color:C.purple,
      desc:"従来は「法人・企業」が主体で個人はグレーゾーン。今回の第2条で個人も投資者として明示。富裕層・起業家・技術者の対外投資が初めて正式に法制化され、コンプライアンスの対象に。",
    },
    {
      title:"政府による総合支援体制",icon:"🏛",color:C.teal,
      desc:"海外リスク情報の定期提供（発改委）、政策性保険・融資（商務部・政策銀行）、在外公館を通じた権益保護、国際仲裁支援（第4〜11条）。投資前・中・後の一貫したサポートが義務化。",
    },
    {
      title:"BRI推進・国際競争参加の法的裏付け",icon:"🌐",color:C.green,
      desc:"一帯一路（BRI）協力の高品質化と産業・供給チェーンの国際協力推進を明示（第1条）。ASEAN・中東・アフリカへの製造業投資・インフラ投資が、今後さらに加速する可能性。",
    },
  ];

  supports.forEach((s2,i)=>{
    const col=i%2, row=Math.floor(i/2);
    const x=0.32+col*4.82, y=1.0+row*2.12, w=4.6, h=1.98;
    box(s,x,y,w,h,C.white,s2.color,1);
    box(s,x,y,w,0.36,s2.color);
    box(s,x,y,0.36,h,s2.color);
    tt(s,s2.title,{x:x+0.46,y:y+0.07,w:w-0.56,h:0.24,fontSize:11,bold:true,color:C.white});
    tt(s,s2.desc,{x:x+0.44,y:y+0.44,w:w-0.56,h:1.45,fontSize:9,color:C.darkgray,valign:"top"});
  });
}

// ============================================================
// Slide 8: 規制・安全保障の側面
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"規制・安全保障の側面（第13〜38条）","機微技術・データ・安全審査の3層規制が新設された");

  const layers=[
    {
      art:"第13条", title:"技術輸出・越境移転の禁止",color:C.red,
      items:[
        "輸出が禁止・制限されている財・技術・サービス・データを対外投資で無断使用することを禁止",
        "技術者を越境派遣して技術指導を行う行為、国外研修を組織する行為も「輸出」に相当",
        "→ 日本企業との技術合弁・ライセンス契約が中国側規制の対象になり得る",
      ]
    },
    {
      art:"第14条", title:"越境データ・個人情報の管理",color:C.amber,
      items:[
        "コアデータ・重要データ・個人情報を対外投資の相手先に提供する前に安全評価等が必要",
        "対象データの判定は「データ安全法」「個人情報保護法」との連動で決まる",
        "→ データを活用したM&A・JVで中国側パートナーがデータを持ち出せない場合が生じる",
      ]
    },
    {
      art:"第15条", title:"国家安全審査制度",color:C.purple,
      items:[
        "国家安全に影響する（可能性のある）投資は発改委・商務部が他機関と合同審査",
        "投資の実行後に生じた資産売却・株式移転も審査対象（事後も管理）",
        "→ 日本企業を買収したり日本企業に出資したりする中国企業が審査を受ける可能性",
      ]
    },
    {
      art:"第33〜38条", title:"罰則・強制措置",color:C.darkgray,
      items:[
        "違反投資：投資額の0.5〜10‰の罰金＋違法収益没収",
        "重大違反：中国国内での事業活動制限、1〜3年の対外投資禁止、担当者への個人罰則",
        "→ 中国パートナーが予告なく投資撤退・資産売却を命じられるリスクに注意",
      ]
    },
  ];

  layers.forEach((l,i)=>{
    const y=0.9+i*1.05, h=0.97;
    box(s,0.35,y,0.78,h,l.color);
    tt(s,l.art,{x:0.37,y:y+0.09,w:0.74,h:0.28,fontSize:10,bold:true,color:C.white,align:"center"});
    tt(s,l.title,{x:1.22,y:y+0.04,w:8.2,h:0.26,fontSize:11.5,bold:true,color:l.color});
    l.items.forEach((it,j)=>{
      oval(s,1.3,y+0.38+j*0.19,0.04,l.color);
      tt(s,it,{x:1.44,y:y+0.28+j*0.19,w:8.08,h:0.22,fontSize:8.5,color:C.darkgray});
    });
  });

  footer(s,"国務院令第837号 各条文 / JunHe Legal Updates（2026.06）/ Mayer Brown（2026.06）");
}

// ============================================================
// Slide 9: 安全審査制度の詳細と罰則
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"安全審査（第15条）の詳細","審査の対象・プロセス・不服申立てのポイント");

  // Trigger categories
  tt(s,"▌ 審査が必要になる3類型",{x:0.4,y:0.9,w:6,h:0.28,fontSize:11,bold:true,color:C.navy});
  const triggers=[
    {t:"機微技術分野への投資",d:"AI・量子・半導体・バイオ・宇宙・先進製造の海外企業へのM&A・出資",c:C.red},
    {t:"重要資源の取得",d:"レアアース・エネルギー・食料・鉱物等の海外での権益取得・設備投資",c:C.amber},
    {t:"データプラットフォームの取得",d:"大量の個人データ・産業データを保有する海外企業への投資・支配権取得",c:C.purple},
  ];
  triggers.forEach((t,i)=>{
    box(s,0.4,1.24+i*0.74,5.8,0.66,C.white,t.c,0.75);
    box(s,0.4,1.24+i*0.74,0.06,0.66,t.c);
    tt(s,t.t,{x:0.56,y:1.28+i*0.74,w:5.18,h:0.24,fontSize:10,bold:true,color:t.c});
    tt(s,t.d,{x:0.56,y:1.52+i*0.74,w:5.18,h:0.3,fontSize:8.5,color:C.darkgray});
  });

  // Process flow
  tt(s,"▌ 審査プロセス（実施細則は整備中）",{x:6.6,y:0.9,w:3.1,h:0.28,fontSize:10,bold:true,color:C.navy});
  const steps=[
    {t:"事前申告",c:C.blue},
    {t:"安全審査開始",c:C.teal},
    {t:"条件付き承認\nまたは禁止",c:C.amber},
    {t:"実行後の\n継続監視",c:C.green},
  ];
  steps.forEach((st,i)=>{
    box(s,6.65,1.24+i*0.78,2.95,0.62,st.c);
    tt(s,st.t,{x:6.7,y:1.28+i*0.78,w:2.85,h:0.54,fontSize:10,bold:true,color:C.white,align:"center",valign:"middle"});
    if(i<3) tt(s,"▼",{x:7.65,y:1.86+i*0.78,w:1.0,h:0.2,fontSize:11,color:"94A3B8",align:"center"});
  });

  // Warning box — positioned below all 4 steps (step4 ends at 1.24+3*0.78+0.62=4.20)
  box(s,0.35,4.32,9.25,0.92,"FFF7ED",C.amber,1.5);
  box(s,0.35,4.32,0.05,0.92,C.amber);
  tt(s,"⚠ 重要：実施細則はまだ未整備",{x:0.5,y:4.37,w:9.0,h:0.26,fontSize:11,bold:true,color:C.amber});
  tt(s,"審査の具体的な基準・期間・手続きは今後公表される実施細則に委ねられており、今の時点では不確実性が高い。中国側パートナーとの新規投資・M&A・技術提携を検討する際は、審査の対象となる可能性を想定した契約条項（解除条件・待機条項）の設定が不可欠。",
    {x:0.5,y:4.64,w:9.0,h:0.54,fontSize:9,color:C.darkgray,valign:"top"});
  footer(s,"国務院令第837号第15条 / Pillsbury Law（2026.06）/ Morgan Lewis（2026.06）");
}

// ============================================================
// Slide 10: 中国企業への影響①（チャンスとなる領域）
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"中国企業への影響①　加速が見込まれる対外投資","規制の明確化により「踏み切れなかった投資」が進みやすくなる");

  const accel=[
    {
      sector:"製造業・インフラ（BRI国中心）",color:C.green,icon:"🏭",
      why:"規制対象外の一般製造業・インフラ投資は法的根拠が強化され、政府支援も充実。ASEAN・中東・アフリカでの工場建設・物流拠点が加速。",
      eg:"例：BYD（タイ）、CATL（インドネシア）、Haier（インド・中東）",
      risk:"日本への影響：競合製品が現地で生産・供給され、日系メーカーのシェアが圧迫される"
    },
    {
      sector:"希少資源・エネルギー確保",color:C.amber,icon:"⚡",
      why:"レアアース・リチウム・銅等の資源権益取得が戦略的に推進。重要資源は第15条の審査対象となるが、国策として「通過」させる可能性が高い。",
      eg:"例：アフリカのリチウム・コバルト鉱山、中南米の銅山への投資強化",
      risk:"日本への影響：日本がアクセスしようとする鉱山権益が中国資本に先押さえされるリスク"
    },
    {
      sector:"個人投資家・スタートアップ支援",color:C.purple,icon:"💼",
      why:"初めて個人投資家が法的に認定。中国の富裕層・テック起業家が海外スタートアップへVCスタイルで投資するパスが整備される。",
      eg:"例：シリコンバレー・東京・テルアビブのスタートアップへの中国個人マネーの流入",
      risk:"日本への影響：日本のAI・医療・ロボットスタートアップへの中国個人マネー参入増加"
    },
  ];

  accel.forEach((a,i)=>{
    const y=1.02+i*1.46, h=1.36;
    box(s,0.35,y,9.25,h,C.white,a.color,1);
    box(s,0.35,y,0.06,h,a.color);
    badge(s,a.sector,0.48,y+0.08,3.8,a.color);
    tt(s,a.why,{x:0.5,y:y+0.36,w:5.5,h:0.54,fontSize:9,color:C.darkgray,valign:"top"});
    tt(s,a.eg,{x:0.5,y:y+0.9,w:5.5,h:0.36,fontSize:8.5,color:a.color,bold:true});
    box(s,6.12,y+0.08,3.4,1.18,"FFF7ED",C.amber,0.5);
    tt(s,a.risk,{x:6.2,y:y+0.1,w:3.22,h:1.14,fontSize:8.5,color:C.darkgray,valign:"top"});
  });

  footer(s,"Brownstein BHFS（2026.06）/ CMS Law（2026.06）/ Charltons Law（2026.06）");
}

// ============================================================
// Slide 11: 中国企業への影響②（制約が強まる領域）
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"中国企業への影響②　制約が強まる対外投資","機微技術・データ・既存海外資産の3分野で規制が実質的に強化");

  const constrs=[
    {
      title:"AI・半導体・先端技術分野の海外M&A",color:C.red,
      before:"従来：部門規定ベースで抜け道が多く、規制があいまいだった",
      after:"今後：第13条（技術移転禁止）+ 第15条（安全審査）の二重規制が適用",
      impact:"日本への影響：日本の半導体設計・精密部品・材料企業への中国資本によるM&Aが停滞または複雑化。両国当局審査が重なる「二重ゲート」状態に。",
      severity:"高"
    },
    {
      title:"技術者の越境派遣・研修（第13条の実務影響）",color:C.amber,
      before:"従来：技術者の海外赴任・研修は「投資管理」の対象外だった",
      after:"今後：制限品目の技術を持つ人材の国外派遣が実質的に輸出規制の対象に",
      impact:"日本への影響：中国人エンジニアが日本でのJVや技術研究に参加する際、中国側のコンプライアンス審査が必要になる可能性。プロジェクトの遅延リスク。",
      severity:"中"
    },
    {
      title:"既存の海外資産・株式の「売却・移転」も対象",color:C.purple,
      before:"従来：海外に持つ資産の管理は対外投資規制の対象外だった",
      after:"今後：既存の海外子会社・資産の売却・株式移転も第15条の審査対象",
      impact:"日本への影響：日本企業の中国資本持分を第三者に売る際、中国側の審査が必要になる可能性。EXIT（事業売却）のプロセスが予想外に長期化する恐れ。",
      severity:"中〜高"
    },
  ];

  constrs.forEach((c,i)=>{
    const y=0.92+i*1.49, h=1.4;
    box(s,0.35,y,9.25,h,C.white,c.color,1);
    box(s,0.35,y,0.05,h,c.color);
    badge(s,"リスク："+c.severity,7.9,y+0.08,1.62,c.color);
    tt(s,c.title,{x:0.5,y:y+0.08,w:7.3,h:0.24,fontSize:11,bold:true,color:c.color});
    box(s,0.5,y+0.38,2.45,0.24,"E2E8F0");
    tt(s,"【従来】"+c.before,{x:0.56,y:y+0.38,w:2.35,h:0.24,fontSize:8,color:C.gray,valign:"middle"});
    box(s,3.0,y+0.38,2.45,0.24,c.color);
    tt(s,"【今後】"+c.after,{x:3.06,y:y+0.38,w:2.35,h:0.24,fontSize:8,bold:true,color:C.white,valign:"middle"});
    tt(s,c.impact,{x:0.5,y:y+0.7,w:9.0,h:0.6,fontSize:9,color:C.darkgray,valign:"top"});
  });

  footer(s,"Morgan Lewis（2026.06）/ Pillsbury Law（2026.06）/ CMS Law「China Issues New Outbound Investment Regulation」");
}

// ============================================================
// Slide 12: 中国資本が日本に増加するとき何が起きるか
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"中国資本が日本に増加するとき何が起きるか","837号は中国企業の「一般投資」を加速させつつ、日本の制度との摩擦を生む");

  // Three scenarios
  const scenarios=[
    {
      n:"シナリオA",
      title:"一般製造業・消費財（規制少→加速）",
      color:C.green,bg:C.ltgreen,
      body:"中国投資家による日本の食品・流通・不動産・中小製造業への投資は規制対象外。個人投資家の正式化で、富裕層・起業家マネーが日本の中堅企業M&Aに流入するケースが増加見込み。",
      alert:"→ 日本企業：資本受け入れ先の国籍審査・持分比率管理が必要",
    },
    {
      n:"シナリオB",
      title:"先端製造・EV・素材（双方規制で複雑化）",
      color:C.amber,bg:C.ltamber,
      body:"EV電池・素材・精密機械等は中国側も日本側（外為法）も審査対象になるグレーゾーン。中国企業にとっては「第15条審査」、日本企業にとっては「外為法事前届出」の二重ゲートが発生。",
      alert:"→ 日本企業：デューデリジェンスに中国側規制リスクを織り込む",
    },
    {
      n:"シナリオC",
      title:"AI・半導体・量子（双方が強く制限）",
      color:C.red,bg:C.ltred,
      body:"中国が機密とみなす技術への対外投資は第13条・15条で制限、日本は外為法・経済安全保障推進法で規制。表向きは「商業提携」「研究協力」に見せながら実態を変える事例に注意が必要。",
      alert:"→ 日本企業：契約書・技術共有の範囲・経営支配権条項の詳細確認を",
    },
  ];

  scenarios.forEach((sc,i)=>{
    const x=0.28+i*3.22, y=0.95, w=3.1, h=4.38;
    box(s,x,y,w,h,sc.bg,sc.color,1.5);
    box(s,x,y,w,0.64,sc.color);
    badge(s,sc.n,x+0.1,y+0.1,1.1,C.darkgray);
    tt(s,sc.title,{x:x+0.08,y:y+0.38,w:w-0.16,h:0.24,fontSize:9.5,bold:true,color:C.white});
    tt(s,sc.body,{x:x+0.1,y:y+0.7,w:w-0.2,h:2.1,fontSize:9,color:C.darkgray,valign:"top"});
    box(s,x+0.1,y+2.88,w-0.2,1.38,sc.color);
    tt(s,sc.alert,{x:x+0.18,y:y+2.92,w:w-0.36,h:1.28,fontSize:9,bold:true,color:C.white,valign:"top"});
  });

  footer(s,"外為法（FEFTA）・経済安全保障推進法（日本）/ 国務院令第837号（中国）/ ジェトロ対日投資データ");
}

// ============================================================
// Slide 13: セクター別リスクマップ
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"日本企業　セクター別リスクマップ","中国資本の受け入れに関するリスク水準を業種別に整理");

  // Table
  const cols=["業種・分野","中国の投資意欲","中国側規制\n（837号）","日本側規制\n（外為法等）","総合リスク","注目ポイント"];
  const colW=[2.0,1.05,1.05,1.05,0.85,3.55];
  const rows=[
    {cells:["半導体・AI・量子","★★★","高（第13/15条）","高（安保審査）","最高","技術流出が最大懸念。商業提携に偽装した技術収奪に注意"], risk:"最高"},
    {cells:["EV電池・素材・材料","★★★","中（資源条項）","中（外為法）","高","CATL・BYDが日本材料メーカーへの出資を模索"], risk:"高"},
    {cells:["精密機械・ロボット","★★★","中（技術条項）","中（安保）","高","JV・ライセンス経由の技術移転が抜け穴になるリスク"], risk:"高"},
    {cells:["医療・バイオ・創薬","★★","中（データ条項）","中（外為法）","中〜高","患者データ・ゲノムデータの取り扱いに注意"], risk:"中〜高"},
    {cells:["食品・農業・農地","★","低","中（重要土地法）","中","農地・食料資産への中国資本参入は日本国内法で別途規制"], risk:"中"},
    {cells:["消費財・流通・EC","★★","低","低","低","規制上のリスクは小さいが、ブランド管理・品質管理に注意"], risk:"低"},
    {cells:["不動産（一般）","★★","低","低（一部中）","低〜中","重要施設周辺の土地取得は「重要土地等調査法」が適用"], risk:"低〜中"},
  ];
  const riskColor={"最高":C.red,"高":"DC6803","中〜高":C.amber,"中":"D97706","低〜中":C.teal,"低":C.green};
  const headerY=0.95, rowH=0.54;

  // Header
  let hx=0.35;
  colW.forEach((w,i)=>{
    box(s,hx,headerY,w,0.36,C.navy);
    tt(s,cols[i],{x:hx+0.04,y:headerY,w:w-0.08,h:0.36,fontSize:8,bold:true,color:C.white,align:"center",valign:"middle"});
    hx+=w;
  });

  // Data rows
  rows.forEach((r,ri)=>{
    let rx=0.35;
    const ry=headerY+0.36+ri*rowH;
    const bg=ri%2===0?C.offwhite:C.white;
    colW.forEach((w,ci)=>{
      box(s,rx,ry,w,rowH,ci===4?riskColor[r.risk]||C.gray:bg,C.lightgray,0.3);
      const fc=ci===4?C.white:(ci===0?C.darkgray:C.gray);
      tt(s,r.cells[ci],{x:rx+0.04,y:ry,w:w-0.08,h:rowH,fontSize:ci===5?7.5:8.5,
        color:fc,align:ci===0||ci===5?"left":"center",valign:"middle",bold:ci===0});
      rx+=w;
    });
  });

  footer(s,"外為法・経済安全保障推進法・重要土地等調査法（日本）/ 国務院令第837号（中国）/ 各種弁護士事務所レポート（2026年6月）");
}

// ============================================================
// Slide 14: 日本企業の実務対応
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.offwhite};
  titleBlock(s,"日本企業が今すべき実務対応","4つのアクションで「二重規制リスク」を事前に管理する");

  const actions=[
    {
      n:"Action 1", phase:"即時（1〜3ヶ月）",
      title:"中国資本受け入れ基準の明文化",
      color:C.red,
      items:[
        "中国資本（法人・個人）からの出資・M&Aオファーを受けた場合の社内意思決定基準を策定",
        "外為法に基づく「事前届出が必要な業種・持分比率」の一覧を法務部門で整備",
        "取締役会・経営会議レベルでの承認ルートを明確化（担当部署に任せきりにしない）",
      ]
    },
    {
      n:"Action 2", phase:"即時〜短期（3〜6ヶ月）",
      title:"保有技術・データの安全保障上のランク付け",
      color:C.amber,
      items:[
        "自社が保有する技術・ノウハウ・データを「機微度」でランク分け（高・中・低）",
        "中国の第13条・14条が禁じる「輸出制限品目」との重複確認を外部専門家と実施",
        "既存の中国パートナーとのライセンス契約・技術共有協定の範囲を再点検",
      ]
    },
    {
      n:"Action 3", phase:"短期（3〜9ヶ月）",
      title:"契約条項の見直し（知財・データ・解除条件）",
      color:C.blue,
      items:[
        "JV契約・資本提携契約に「中国政府の審査命令による強制売却が発生した場合の解除条件」を追加",
        "データ共有の範囲を具体的に定義し、特定データ類型を「共有対象外」として明示",
        "新規契約では「技術・特許の帰属」と「退出時の取り扱い」を詳細に規定",
      ]
    },
    {
      n:"Action 4", phase:"継続（随時）",
      title:"837号実施細則の動向モニタリング",
      color:C.green,
      items:[
        "第15条（安全審査）の実施細則はまだ未公表 — 公表後に即時影響評価が必要",
        "発改委・商務部の実際の審査運用事例を専門機関（ジェトロ・弁護士事務所）通じて収集",
        "半年ごとにセクター別リスクマップを更新し、取引・投資判断に反映",
      ]
    },
  ];

  actions.forEach((a,i)=>{
    const col=i%2, row=Math.floor(i/2);
    const x=0.28+col*4.82, y=0.92+row*2.2, w=4.65, h=2.1;
    box(s,x,y,w,h,C.white,a.color,1.5,);
    box(s,x,y,w,0.46,a.color);
    tt(s,a.n,{x:x+0.1,y:y+0.08,w:0.9,h:0.3,fontSize:9,bold:true,color:C.white});
    badge(s,a.phase,x+1.02,y+0.12,3.55,"334155");
    tt(s,a.title,{x:x+0.1,y:y+0.52,w:w-0.2,h:0.26,fontSize:11,bold:true,color:a.color});
    a.items.forEach((it,j)=>{
      oval(s,x+0.18,y+0.9+j*0.42,0.05,a.color);
      tt(s,it,{x:x+0.3,y:y+0.8+j*0.42,w:w-0.4,h:0.38,fontSize:8.5,color:C.darkgray,valign:"top"});
    });
  });
}

// ============================================================
// Slide 15: 結論・アクションアイテム
// ============================================================
{
  const s = pres.addSlide();
  s.background = {color:C.navy};
  box(s,0,0,0.22,5.625,C.amber);
  box(s,0.22,0,9.78,0.06,C.iceblue);

  tt(s,"結論とアクションアイテム",{x:0.5,y:0.2,w:9.0,h:0.48,fontSize:26,bold:true,color:C.white});
  box(s,0.5,0.72,4.5,0.03,C.amber);

  const concls=[
    {
      n:"1",
      title:"837号は「開放と管理の強化」を同時に実現する設計",
      body:"促進・支援面では対外投資の法的根拠が強化され、BRI国・一般産業への中国資本流出が加速。一方、機微技術・データ・安全審査の側面では従来比で規制が格段に強まる。「緩和か強化か」という二者択一ではなく、対象分野によって全く異なる影響が生じる。",
      color:C.iceblue
    },
    {
      n:"2",
      title:"中国資本の日本流入は増加、ただし「二重ゲート」が出現",
      body:"837号で制度的後押しを受けた中国企業が日本への投資を増やす一方、先端技術・データ分野では中国側（第15条審査）と日本側（外為法・経安法）の双方審査が必要になる。投資案件の審査負荷と不確実性が増大する。",
      color:C.iceblue
    },
    {
      n:"3",
      title:"今すぐ動く：実施細則の整備前が対応の好機",
      body:"第15条の実施細則はまだ未公表。「基準が明確でない今のうち」に社内基準・契約条項・技術棚卸しを整備することで、細則公表後の対応スピードが格段に上がる。実施細則が出てから動くのでは遅い。",
      color:C.iceblue
    },
  ];

  concls.forEach((c,i)=>{
    const y=1.0+i*1.42;
    box(s,0.5,y,0.38,0.38,C.amber);
    tt(s,c.n,{x:0.5,y:y+0.02,w:0.38,h:0.36,fontSize:18,bold:true,color:C.navy,align:"center"});
    tt(s,c.title,{x:0.98,y:y+0.02,w:8.3,h:0.3,fontSize:12,bold:true,color:C.amber});
    tt(s,c.body,{x:0.98,y:y+0.38,w:8.3,h:0.9,fontSize:9.5,color:C.white,valign:"top"});
  });

  tt(s,"2026年7月　経営企画部　｜　出所：国務院令第837号・JunHe・Morgan Lewis・Mayer Brown・Pillsbury（各2026.06）/ ジェトロ",
    {x:0.5,y:5.3,w:9.0,h:0.22,fontSize:7.5,color:C.gray});
}

// ============================================================
// 出力
// ============================================================
pres.writeFile({fileName:"中国対外投資規制837号分析.pptx"}).then(()=>{
  console.log("✅ 作成完了: 中国対外投資規制837号分析.pptx");
}).catch(err=>{
  console.error("❌ エラー:", err);
});
