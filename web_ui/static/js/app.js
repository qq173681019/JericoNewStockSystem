// ===== Global Variables =====
let priceChart = null;
let indicatorChart = null;

// ===== DOM Elements =====
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menu-toggle');
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const themeToggle = document.getElementById('theme-toggle');
const loadingOverlay = document.getElementById('loading-overlay');
const toastContainer = document.getElementById('toast-container');

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initializeNavigation();
    initializePredictionPage();
    initializeWatchlistPage();
    initializeHistoryPage();
    initializeAnalysisPage();
    initializeSettingsPage();
});

// ===== Theme Management =====
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeToggle.checked = savedTheme === 'dark';
    
    themeToggle.addEventListener('change', () => {
        const newTheme = themeToggle.checked ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        showToast('主题已切换', 'info');
    });
}

// ===== Navigation =====
function initializeNavigation() {
    // Menu toggle for mobile
    menuToggle?.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
    
    // Page navigation
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = item.getAttribute('data-page');
            navigateToPage(pageName);
        });
    });
}

function navigateToPage(pageName) {
    // Update active nav item
    navItems.forEach(item => {
        if (item.getAttribute('data-page') === pageName) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Update active page
    pages.forEach(page => {
        if (page.id === `${pageName}-page`) {
            page.classList.add('active');
        } else {
            page.classList.remove('active');
        }
    });
    
    // Close sidebar on mobile
    if (window.innerWidth <= 1024) {
        sidebar.classList.remove('active');
    }
}

// ===== Prediction Page =====
function initializePredictionPage() {
    const predictBtn = document.getElementById('predict-btn');
    const stockCodeInput = document.getElementById('stock-code');
    const predictionResults = document.getElementById('prediction-results');
    
    predictBtn.addEventListener('click', async () => {
        const stockCode = stockCodeInput.value.trim();
        const predictionType = document.getElementById('prediction-type').value;
        
        if (!stockCode) {
            showToast('请输入股票代码', 'error');
            return;
        }
        
        // Validate stock code format
        if (!/^\d{6}$/.test(stockCode)) {
            showToast('股票代码格式不正确，应为6位数字', 'error');
            return;
        }
        
        await runPrediction(stockCode, predictionType);
    });
    
    // Allow Enter key to trigger prediction
    stockCodeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            predictBtn.click();
        }
    });
}

async function runPrediction(stockCode, predictionType) {
    showLoading(true);
    
    try {
        // Simulate API call - replace with actual API endpoint
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Mock prediction data
        const predictionData = generateMockPrediction(stockCode, predictionType);
        
        displayPredictionResults(predictionData);
        showToast('预测完成', 'success');
    } catch (error) {
        console.error('Prediction error:', error);
        showToast('预测失败，请重试', 'error');
    } finally {
        showLoading(false);
    }
}

function generateMockPrediction(stockCode, predictionType) {
    const currentPrice = 15.50 + Math.random() * 5;
    const priceChange = (Math.random() - 0.5) * 2;
    const targetPrice = currentPrice + priceChange;
    
    return {
        stockCode: stockCode,
        currentPrice: currentPrice.toFixed(2),
        targetPrice: targetPrice.toFixed(2),
        trend: priceChange > 0 ? '上涨' : '下跌',
        trendPercent: ((priceChange / currentPrice) * 100).toFixed(2),
        confidence: (85 + Math.random() * 10).toFixed(1),
        riskLevel: priceChange > 1 ? '高' : priceChange > 0 ? '中' : '低',
        position: priceChange > 0 ? '70%' : '30%',
        advice: priceChange > 0 ? '建议买入' : '建议观望',
        updateTime: new Date().toLocaleString('zh-CN'),
        historicalData: generateHistoricalData(),
        indicators: generateIndicators()
    };
}

function generateHistoricalData() {
    const data = [];
    const basePrice = 15;
    for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        data.push({
            date: date.toISOString().split('T')[0],
            price: basePrice + Math.random() * 5 - 2.5
        });
    }
    return data;
}

function generateIndicators() {
    return {
        macd: (Math.random() - 0.5).toFixed(3),
        rsi: (30 + Math.random() * 40).toFixed(1),
        kdj: (40 + Math.random() * 30).toFixed(1),
        volume: (Math.random() * 1000000).toFixed(0)
    };
}

function displayPredictionResults(data) {
    // Show results section
    const resultsSection = document.getElementById('prediction-results');
    resultsSection.style.display = 'block';
    
    // Update result cards
    document.getElementById('trend-result').textContent = 
        `${data.trend} ${data.trendPercent}%`;
    document.getElementById('confidence').textContent = `${data.confidence}%`;
    
    document.getElementById('target-price').textContent = `¥${data.targetPrice}`;
    document.getElementById('current-price').textContent = `¥${data.currentPrice}`;
    
    document.getElementById('risk-level').textContent = data.riskLevel;
    document.getElementById('position').textContent = data.position;
    
    document.getElementById('advice').textContent = data.advice;
    document.getElementById('update-time').textContent = data.updateTime;
    
    // Update trend card color
    const trendCard = document.querySelector('.card-icon.trend-up');
    if (data.trend === '下跌') {
        trendCard.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
    } else {
        trendCard.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    }
    
    // Update analysis content
    const analysisContent = document.getElementById('analysis-content');
    analysisContent.innerHTML = `
        <p><strong>股票代码：</strong>${data.stockCode}</p>
        <p><strong>当前价格：</strong>¥${data.currentPrice}</p>
        <p><strong>预测价格：</strong>¥${data.targetPrice}</p>
        <p><strong>预测趋势：</strong>${data.trend}，涨跌幅约 ${data.trendPercent}%</p>
        <p><strong>置信度：</strong>${data.confidence}%</p>
        <p><strong>技术指标：</strong></p>
        <ul style="margin-left: 20px; margin-top: 10px;">
            <li>MACD: ${data.indicators.macd}</li>
            <li>RSI: ${data.indicators.rsi}</li>
            <li>KDJ: ${data.indicators.kdj}</li>
            <li>成交量: ${formatNumber(data.indicators.volume)}</li>
        </ul>
        <p style="margin-top: 15px;"><strong>交易建议：</strong>${data.advice}，建议仓位 ${data.position}</p>
        <p><strong>风险提示：</strong>股市有风险，投资需谨慎。本预测仅供参考，不构成投资建议。</p>
    `;
    
    // Draw charts
    drawPriceChart(data.historicalData);
    drawIndicatorChart(data.indicators);
}

function drawPriceChart(historicalData) {
    const ctx = document.getElementById('price-chart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (priceChart) {
        priceChart.destroy();
    }
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalData.map(d => d.date),
            datasets: [{
                label: '股价走势',
                data: historicalData.map(d => d.price),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function drawIndicatorChart(indicators) {
    const ctx = document.getElementById('indicator-chart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (indicatorChart) {
        indicatorChart.destroy();
    }
    
    indicatorChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['MACD', 'RSI', 'KDJ'],
            datasets: [{
                label: '技术指标值',
                data: [
                    parseFloat(indicators.macd) * 100,
                    parseFloat(indicators.rsi),
                    parseFloat(indicators.kdj)
                ],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderColor: [
                    '#3b82f6',
                    '#8b5cf6',
                    '#10b981'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// ===== Watchlist Page =====
function initializeWatchlistPage() {
    const addToWatchlistBtn = document.getElementById('add-to-watchlist-btn');
    
    addToWatchlistBtn?.addEventListener('click', () => {
        const stockCode = prompt('请输入要添加的股票代码：');
        if (stockCode && /^\d{6}$/.test(stockCode)) {
            addToWatchlist(stockCode);
        } else if (stockCode) {
            showToast('股票代码格式不正确', 'error');
        }
    });
}

function addToWatchlist(stockCode) {
    showToast(`已添加股票 ${stockCode} 到观测池`, 'success');
    // Implement actual watchlist addition logic
}

// ===== History Page =====
function initializeHistoryPage() {
    const exportHistoryBtn = document.getElementById('export-history-btn');
    const historyFilter = document.getElementById('history-filter');
    
    exportHistoryBtn?.addEventListener('click', () => {
        exportHistory();
    });
    
    historyFilter?.addEventListener('change', (e) => {
        filterHistory(e.target.value);
    });
}

function exportHistory() {
    showToast('历史记录导出功能开发中...', 'info');
    // Implement export logic
}

function filterHistory(filterType) {
    showToast(`筛选类型: ${filterType}`, 'info');
    // Implement filtering logic
}

// ===== Analysis Page =====
function initializeAnalysisPage() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const analysisStockCode = document.getElementById('analysis-stock-code');
    
    analyzeBtn?.addEventListener('click', () => {
        const stockCode = analysisStockCode.value.trim();
        if (!stockCode) {
            showToast('请输入股票代码', 'error');
            return;
        }
        if (!/^\d{6}$/.test(stockCode)) {
            showToast('股票代码格式不正确', 'error');
            return;
        }
        runTechnicalAnalysis(stockCode);
    });
}

async function runTechnicalAnalysis(stockCode) {
    showLoading(true);
    
    try {
        await new Promise(resolve => setTimeout(resolve, 1500));
        showToast(`股票 ${stockCode} 技术分析完成`, 'success');
        // Update indicator cards with real data
    } catch (error) {
        showToast('技术分析失败', 'error');
    } finally {
        showLoading(false);
    }
}

// ===== Settings Page =====
function initializeSettingsPage() {
    const themeSelect = document.getElementById('theme-select');
    
    themeSelect?.addEventListener('change', (e) => {
        const theme = e.target.value;
        if (theme === 'auto') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        } else {
            document.documentElement.setAttribute('data-theme', theme);
        }
        localStorage.setItem('theme', theme);
        showToast('设置已保存', 'success');
    });
}

// ===== Utility Functions =====
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('active');
    } else {
        loadingOverlay.classList.remove('active');
    }
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'error' ? 'exclamation-circle' : 
                 'info-circle';
    
    toast.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

function formatNumber(num) {
    return parseInt(num).toLocaleString('zh-CN');
}

// ===== Quick Search =====
const quickSearch = document.getElementById('quick-search');
quickSearch?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const searchTerm = quickSearch.value.trim();
        if (searchTerm) {
            // Navigate to prediction page and populate the search
            navigateToPage('prediction');
            document.getElementById('stock-code').value = searchTerm;
            showToast(`搜索: ${searchTerm}`, 'info');
        }
    }
});

// ===== Responsive Sidebar =====
window.addEventListener('resize', () => {
    if (window.innerWidth > 1024) {
        sidebar.classList.remove('active');
    }
});

// ===== Click outside sidebar to close on mobile =====
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 1024) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});
