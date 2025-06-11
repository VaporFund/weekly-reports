const fs = require('fs-extra');
const path = require('path');
const csv = require('csv-parser');
const moment = require('moment');
const winston = require('winston');
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');
const { Chart, registerables } = require('chart.js');

// ลงทะเบียน Chart.js components
Chart.register(...registerables);

// ตั้งค่า logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.simple(),
  transports: [
    new winston.transports.Console()
  ]
});

// ตั้งค่าค่าคงที่
const FOLDER = 'chart_images';
const MARKDOWN_FOLDER = 'reports';
const GITHUB_REPO_URL = "https://raw.githubusercontent.com/VaporFund/weekly-reports/main";
const GITHUB_IMAGES_PATH = `${GITHUB_REPO_URL}/${FOLDER}`;

// สร้าง ChartJSNodeCanvas instance
const width = 1200;
const height = 800;
const chartCallback = (ChartJS) => {
  ChartJS.defaults.font.family = 'Arial';
  ChartJS.defaults.font.size = 14;
};
const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height, chartCallback });

// ฟังก์ชันสร้างโฟลเดอร์
async function ensureFoldersExist() {
  await fs.ensureDir(FOLDER);
  await fs.ensureDir(MARKDOWN_FOLDER);
}

// ฟังก์ชันสร้างกราฟพื้นฐาน
async function basicCharts(token, csvSource) {
  const results = [];
  await new Promise((resolve, reject) => {
    fs.createReadStream(csvSource)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', resolve)
      .on('error', reject);
  });

  const data = results.map(row => ({
    quoted_at: moment(row.quoted_at).toDate(),
    output_amount_readable: parseFloat(row.output_amount) / 1e18,
    output_amount_formatted: parseFloat(row.output_amount_formatted)
  }));

  // สร้างกราฟ Token Amount
  const tokenAmountConfig = {
    type: 'line',
    data: {
      labels: data.map(d => moment(d.quoted_at).format('HH:mm')),
      datasets: [{
        label: 'Token Amount',
        data: data.map(d => d.output_amount_readable),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `${token} Token Amount Over Time`
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };

  // สร้างกราฟ USDC Return
  const usdcReturnConfig = {
    type: 'line',
    data: {
      labels: data.map(d => moment(d.quoted_at).format('HH:mm')),
      datasets: [{
        label: 'USDC Return',
        data: data.map(d => d.output_amount_formatted),
        borderColor: 'rgb(153, 102, 255)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'USDC Return Value Over Time'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };

  // สร้างภาพกราฟ
  const tokenAmountImage = await chartJSNodeCanvas.renderToBuffer(tokenAmountConfig);
  const usdcReturnImage = await chartJSNodeCanvas.renderToBuffer(usdcReturnConfig);

  // บันทึกไฟล์
  const tokenAmountPath = path.join(FOLDER, `${token}_token_amount.png`);
  const usdcReturnPath = path.join(FOLDER, `${token}_usdc_return.png`);
  
  await fs.writeFile(tokenAmountPath, tokenAmountImage);
  await fs.writeFile(usdcReturnPath, usdcReturnImage);

  return { data, tokenAmountPath, usdcReturnPath };
}

// ฟังก์ชันสร้างกราฟแนวโน้ม
async function trendLines(token, data) {
  // คำนวณเส้นแนวโน้ม
  const xValues = data.map((_, i) => i);
  const yValues = data.map(d => d.output_amount_readable);
  
  const n = xValues.length;
  const sumX = xValues.reduce((a, b) => a + b, 0);
  const sumY = yValues.reduce((a, b) => a + b, 0);
  const sumXY = xValues.reduce((a, b, i) => a + b * yValues[i], 0);
  const sumXX = xValues.reduce((a, b) => a + b * b, 0);
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;
  
  const trendLine = xValues.map(x => slope * x + intercept);

  const config = {
    type: 'line',
    data: {
      labels: data.map(d => moment(d.quoted_at).format('HH:mm')),
      datasets: [
        {
          label: 'Token Amount',
          data: data.map(d => d.output_amount_readable),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        },
        {
          label: 'Trend Line',
          data: trendLine,
          borderColor: 'rgb(255, 99, 132)',
          borderDash: [5, 5],
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `${token} Token Amount with Trend Line`
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };

  const image = await chartJSNodeCanvas.renderToBuffer(config);
  const filePath = path.join(FOLDER, `${token}_trend_lines.png`);
  await fs.writeFile(filePath, image);
  
  return filePath;
}

// ฟังก์ชันวิเคราะห์ความสัมพันธ์
async function correlationAnalysis(token, data) {
  const xValues = data.map(d => d.output_amount_readable);
  const yValues = data.map(d => d.output_amount_formatted);
  
  const n = xValues.length;
  const sumX = xValues.reduce((a, b) => a + b, 0);
  const sumY = yValues.reduce((a, b) => a + b, 0);
  const sumXY = xValues.reduce((a, b, i) => a + b * yValues[i], 0);
  const sumXX = xValues.reduce((a, b) => a + b * b, 0);
  const sumYY = yValues.reduce((a, b) => a + b * b, 0);
  
  const correlation = (n * sumXY - sumX * sumY) / 
    Math.sqrt((n * sumXX - sumX * sumX) * (n * sumYY - sumY * sumY));

  const config = {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'Token Amount vs USDC Return',
        data: data.map(d => ({
          x: d.output_amount_readable,
          y: d.output_amount_formatted
        })),
        backgroundColor: 'rgba(75, 192, 192, 0.5)'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Relationship Between Token Amount and USDC Return'
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Token Amount'
          }
        },
        y: {
          title: {
            display: true,
            text: 'USDC Return'
          }
        }
      }
    }
  };

  const image = await chartJSNodeCanvas.renderToBuffer(config);
  const filePath = path.join(FOLDER, `${token}_correlation.png`);
  await fs.writeFile(filePath, image);
  
  return { correlation, filePath };
}

// ฟังก์ชันสร้างรายงาน Markdown
async function generateMarkdownReport(symbol, chartPaths, data, correlation) {
  const timestamp = moment().format('YYYY-MM-DD HH:mm:ss');
  
  const tokenStats = {
    count: data.length,
    mean: data.reduce((a, b) => a + b.output_amount_readable, 0) / data.length,
    min: Math.min(...data.map(d => d.output_amount_readable)),
    max: Math.max(...data.map(d => d.output_amount_readable))
  };
  
  const usdcStats = {
    count: data.length,
    mean: data.reduce((a, b) => a + b.output_amount_formatted, 0) / data.length,
    min: Math.min(...data.map(d => d.output_amount_formatted)),
    max: Math.max(...data.map(d => d.output_amount_formatted))
  };

  const markdownContent = `# ${symbol} Price Analysis Report

Generated on: ${timestamp}

## Overview

This report provides a comprehensive analysis of ${symbol} token price data including:
- Basic price trend visualization
- Enhanced trend analysis with annotations
- Correlation analysis between token amount and USDC return
- Statistical summary

## Key Metrics

| Metric | Value |
|--------|-------|
| **Data Points** | ${data.length} |
| **Correlation Coefficient** | ${correlation.toFixed(4)} |
| **Token Amount Range** | ${tokenStats.min.toFixed(2)} - ${tokenStats.max.toFixed(2)} |
| **USDC Return Range** | ${usdcStats.min.toFixed(2)} - ${usdcStats.max.toFixed(2)} |

## Basic Price Charts

The following charts show the basic price trends for ${symbol} token amount and USDC return over time.

![${symbol} Basic Price Charts](${GITHUB_IMAGES_PATH}/${path.basename(chartPaths.tokenAmountPath)})

## Enhanced Trend Analysis

These enhanced visualizations include trend lines and annotations highlighting minimum and maximum values.

![${symbol} Enhanced Trend Charts](${GITHUB_IMAGES_PATH}/${path.basename(chartPaths.trendLinesPath)})

## Correlation Analysis

The scatter plot below shows the relationship between token amount and USDC return, with a correlation coefficient of **${correlation.toFixed(4)}**.

![${symbol} Correlation Analysis](${GITHUB_IMAGES_PATH}/${path.basename(chartPaths.correlationPath)})

## Statistical Summary

### ${symbol} Token Amount Statistics
- **Count**: ${tokenStats.count}
- **Mean**: ${tokenStats.mean.toFixed(4)}
- **Minimum**: ${tokenStats.min.toFixed(4)}
- **Maximum**: ${tokenStats.max.toFixed(4)}

### USDC Return Statistics
- **Count**: ${usdcStats.count}
- **Mean**: ${usdcStats.mean.toFixed(4)}
- **Minimum**: ${usdcStats.min.toFixed(4)}
- **Maximum**: ${usdcStats.max.toFixed(4)}

## Interpretation

${Math.abs(correlation) > 0.7 ? '### Strong Correlation' : Math.abs(correlation) > 0.3 ? '### Moderate Correlation' : '### Weak Correlation'}

The correlation coefficient of ${correlation.toFixed(4)} indicates a ${Math.abs(correlation) > 0.7 ? 'strong' : Math.abs(correlation) > 0.3 ? 'moderate' : 'weak'} ${correlation > 0 ? 'positive' : 'negative'} relationship between token amount and USDC return.

---

*Report generated by VaporFund Analytics*
`;

  const markdownFilename = path.join(MARKDOWN_FOLDER, `${symbol}_analysis_report.md`);
  await fs.writeFile(markdownFilename, markdownContent);
  
  return markdownFilename;
}

// ฟังก์ชันหลัก
async function main() {
  try {
    await ensureFoldersExist();
    
    logger.info(`GitHub images will be referenced from: ${GITHUB_IMAGES_PATH}`);
    logger.info(`Make sure to push the '${FOLDER}' folder to your GitHub repository!`);
    
    // ตัวอย่างการใช้งาน (คุณจะต้องปรับปรุงส่วนนี้ตามความต้องการของคุณ)
    const tokenSymbol = 'uSOL';
    const csvSource = `quotes_${tokenSymbol}.csv`;
    
    const { data, tokenAmountPath, usdcReturnPath } = await basicCharts(tokenSymbol, csvSource);
    const trendLinesPath = await trendLines(tokenSymbol, data);
    const { correlation, filePath: correlationPath } = await correlationAnalysis(tokenSymbol, data);
    
    const chartPaths = {
      tokenAmountPath,
      usdcReturnPath,
      trendLinesPath,
      correlationPath
    };
    
    await generateMarkdownReport(tokenSymbol, chartPaths, data, correlation);
    
    logger.info('✅ Processing complete!');
    logger.info(`📊 Generated report for ${tokenSymbol}`);
    logger.info(`📁 Chart images saved in: ${FOLDER}/`);
    logger.info(`📄 Markdown report saved in: ${MARKDOWN_FOLDER}/`);
    
  } catch (error) {
    logger.error('Error in main process:', error);
  }
}

// เริ่มต้นโปรแกรม
main(); 