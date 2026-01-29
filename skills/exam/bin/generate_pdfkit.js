const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

// ============ 配置区域 ============
const config = {
  title: '数学练习卷 - 3 年级下册',
  date: '2026-01-30',
  theme: '海底小纵队',
  outputFileName: '海底小纵队-2026-01-30.pdf',

  // 分数配置
  scores: {
    oral: 2,      // 口算题每题分数
    calc: 4,      // 计算题每题分数
    word: 10      // 应用题每题分数
  }
};

// 试卷数据 - 可动态调整数量
const oralProblems = [
  { q: '137 + 45', a: '182' }, { q: '258 + 67', a: '325' }, { q: '376 + 58', a: '434' }, { q: '152 - 37', a: '115' },
  { q: '264 - 58', a: '206' }, { q: '473 - 69', a: '404' }, { q: '125 + 87', a: '212' }, { q: '346 - 79', a: '267' },
  { q: '218 + 94', a: '312' }, { q: '527 - 68', a: '459' }, { q: '215 × 4', a: '860' }, { q: '168 × 5', a: '840' },
  { q: '472 × 3', a: '1416' }, { q: '384 × 6', a: '2304' }, { q: '864 ÷ 4', a: '216' }, { q: '936 ÷ 6', a: '156' },
  { q: '872 ÷ 8', a: '109' }, { q: '954 ÷ 9', a: '106' }, { q: '648 ÷ 4', a: '162' }, { q: '756 ÷ 7', a: '108' }
];

const calcProblems = [
  { q: '25 × 4 + 130', a: '230' },
  { q: '360 ÷ 6 - 25', a: '35' },
  { q: '145 + 265 - 180', a: '230' },
  { q: '156 × 3 - 278', a: '190' },
  { q: '540 ÷ 9 + 175', a: '235' }
];

const wordProblems = [
  {
    q: '海底小纵队的呱唧收集了 8 箱宝藏，每箱有 125 枚金币。分给了巴克队长 375 枚金币，呱唧还剩下多少枚金币？',
    a: '125 × 8 - 375 = 625 枚'
  },
  {
    q: '皮医生诊所里有 5 瓶药水，每瓶装有 180 毫升。给病人用了 420 毫升，还剩下多少毫升药水？',
    a: '180 × 5 - 420 = 480 毫升'
  }
];

// ============ 辅助函数 ============

// 居中绘制标题
function drawCenteredTitle(doc, text, y, fontSize = 14, isBold = true) {
  doc.font(isBold ? 'Chinese-Bold' : 'Chinese')
     .fontSize(fontSize)
     .text(text, 50, y, { width: 495, align: 'center' });
  return doc.y;
}

// 绘制分隔线
function drawLine(doc, y) {
  doc.moveTo(50, y)
     .lineTo(545, y)
     .strokeColor('#000')
     .lineWidth(1)
     .stroke();
}

// 计算总分
function calcTotalScore() {
  return oralProblems.length * config.scores.oral +
         calcProblems.length * config.scores.calc +
         wordProblems.length * config.scores.word;
}

// ============ 创建 PDF ============
const doc = new PDFDocument({
  size: 'A4',
  margins: { top: 60, bottom: 50, left: 50, right: 50 },
  bufferPages: true
});

// 字体路径
const fontPath = path.join(__dirname, 'fonts', 'SourceHanSansCN-Normal.ttf');

// 注册中文字体
doc.registerFont('Chinese', fontPath);
doc.registerFont('Chinese-Bold', fontPath);

// 输出流
const stream = fs.createWriteStream(config.outputFileName);
doc.pipe(stream);

// ============ 页眉 ============
const headerTopY = 40;
const headerTitleY = 52;
const headerSubY = 75;
const headerBottomY = 92;

drawLine(doc, headerTopY);

drawCenteredTitle(doc, config.title, headerTitleY, 18, true);
drawCenteredTitle(doc, `日期：${config.date}    主题：${config.theme}`, headerSubY, 11, false);

drawLine(doc, headerBottomY);

doc.y = headerBottomY + 13;

// ============ 一、口算题 ============
const oralScore = oralProblems.length * config.scores.oral;
doc.y = drawCenteredTitle(doc, `一、口算题（每题 ${config.scores.oral} 分，共 ${oralScore} 分）`, doc.y, 14, true) + 8;

doc.font('Chinese').fontSize(12);

// 动态分栏 - 根据题目数量决定列数
const colsPerRow = 2;
const rowsPerCol = Math.ceil(oralProblems.length / colsPerRow);

for (let row = 0; row < rowsPerCol; row++) {
  const y = doc.y;
  for (let col = 0; col < colsPerRow; col++) {
    const idx = row + col * rowsPerCol;
    if (idx < oralProblems.length) {
      const x = 50 + col * 265;
      doc.text(`${idx + 1}. ${oralProblems[idx].q} = ______`, x, y, { width: 230 });
    }
  }
}

doc.y += 15;

// ============ 二、计算题 ============
const calcScore = calcProblems.length * config.scores.calc;
doc.y = drawCenteredTitle(doc, `二、计算题（每题 ${config.scores.calc} 分，共 ${calcScore} 分）`, doc.y + 8, 14, true) + 10;

doc.font('Chinese').fontSize(12);
calcProblems.forEach((p, i) => {
  doc.text(`${i + 1}. ${p.q} = ______`, 50, doc.y, { width: 500 });
  doc.y += 10;
});

// ============ 三、应用题 ============
const wordScore = wordProblems.length * config.scores.word;
doc.y = drawCenteredTitle(doc, `三、应用题 - ${config.theme}（每题 ${config.scores.word} 分，共 ${wordScore} 分）`, doc.y + 10, 14, true) + 10;

doc.font('Chinese').fontSize(12);
wordProblems.forEach((p, i) => {
  doc.text(`${i + 1}. ${p.q}`, 50, doc.y, { width: 495 });
  doc.y += 6;

  doc.text('（列式计算）', 50, doc.y, { width: 495 });
  doc.y += 6;

  // 答题空间
  const lineY = doc.y + 8;
  doc.moveTo(50, lineY)
     .lineTo(545, lineY)
     .strokeColor('#666')
     .lineWidth(0.5)
     .stroke();

  doc.text('答：', 50, doc.y, { width: 495 });
  doc.y = lineY + 18;
});

// ============ 参考答案页 ============
doc.addPage();

// 答案页眉 - 标题居中
const ansHeaderTopY = 45;
const ansTitleY = 52;
const ansHeaderBottomY = 70;

drawLine(doc, ansHeaderTopY);
drawCenteredTitle(doc, '参考答案', ansTitleY, 18, true);
drawLine(doc, ansHeaderBottomY);

doc.y = ansHeaderBottomY + 15;

// 口算题答案 - 标题和内容都居左
doc.font('Chinese-Bold').fontSize(13).text('口算题', 50, doc.y);
doc.y += 8;

doc.font('Chinese').fontSize(11);
const oralAnsCols = 2;
const oralAnsRows = Math.ceil(oralProblems.length / oralAnsCols);

for (let row = 0; row < oralAnsRows; row++) {
  const y = doc.y;
  for (let col = 0; col < oralAnsCols; col++) {
    const idx = row + col * oralAnsRows;
    if (idx < oralProblems.length) {
      const x = 50 + col * 265;
      doc.text(`${idx + 1}. ${oralProblems[idx].a}`, x, y, { width: 230 });
    }
  }
  doc.y += 10;
}

// 计算题答案 - 标题和内容都居左
doc.y += 5;
doc.font('Chinese-Bold').fontSize(13).text('计算题', 50, doc.y);
doc.y += 8;

doc.font('Chinese').fontSize(11);
calcProblems.forEach((p, i) => {
  doc.text(`${i + 1}. ${p.a}`, 50, doc.y, { width: 500 });
  doc.y += 8;
});

// 应用题答案 - 标题和内容都居左
doc.y += 5;
doc.font('Chinese-Bold').fontSize(13).text('应用题', 50, doc.y);
doc.y += 8;

doc.font('Chinese').fontSize(11);
wordProblems.forEach((p, i) => {
  doc.text(`${i + 1}. ${p.a}`, 50, doc.y, { width: 500 });
  doc.y += 8;
});

// ============ 结束 ============
doc.end();

stream.on('finish', () => {
  const totalScore = calcTotalScore();
  console.log(`✅ PDF 已生成: ${config.outputFileName}`);
  console.log(`📁 位置: ${process.cwd()}/${config.outputFileName}`);
  console.log(`📐 格式: A4 (210mm × 297mm)`);
  console.log(`📊 题目: 口算${oralProblems.length}题 + 计算${calcProblems.length}题 + 应用${wordProblems.length}题`);
  console.log(`💯 总分: ${totalScore}分`);
});
