// ===== DOM Elements =====
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const themeToggle = document.getElementById('themeToggle');
const navItems = document.querySelectorAll('.nav-item');
const views = document.querySelectorAll('.view');
const pageTitle = document.getElementById('pageTitle');
const viewContainer = document.getElementById('viewContainer');
const loadingOverlay = document.getElementById('loadingOverlay');

// Prediction elements
const stockCodeInput = document.getElementById('stockCode');
const predictBtn = document.getElementById('predictBtn');
const predictionResults = document.getElementById('predictionResults');
const quickSearch = document.getElementById('quickSearch');

// ===== Theme Management =====
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeToggle.checked = savedTheme === 'dark';
}

themeToggle.addEventListener('change', () => {
    const theme = themeToggle.checked ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
});

// ===== Navigation =====
const viewTitles = {
    prediction: '股票预测',
    watchlist: '观测池管理',
    history: '预测历史记录',
    analytics: '数据分析',
    settings: '系统设置'
};

function switchView(viewName) {
    // Update nav items
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.dataset.view === viewName) {
            item.classList.add('active');
        }
    });
    
    // Update views
    views.forEach(view => {
        view.classList.remove('active');
    });
    
    const targetView = document.getElementById(`${viewName}View`);
    if (targetView) {
        targetView.classList.add('active');
        pageTitle.textContent = viewTitles[viewName] || viewName;
    }
    
    // Close mobile sidebar
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }
}

navItems.forEach(item => {
    item.addEventListener('click', () => {
        const viewName = item.dataset.view;
        switchView(viewName);
    });
});

// ===== Mobile Menu Toggle =====
mobileMenuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

// ===== Stock Prediction =====
let priceChart = null;

function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}

function generateMockPredictionData(stockCode) {
    // Generate realistic mock data for demonstration
    const currentPrice = 10 + Math.random() * 50;
    const shortTermChange = (Math.random() - 0.5) * 6;
    const mediumTermPrice = currentPrice * (1 + (Math.random() - 0.3) * 0.2);
    
    return {
        stockCode: stockCode,
        currentPrice: currentPrice.toFixed(2),
        shortTermPrediction: shortTermChange > 0 ? `+${shortTermChange.toFixed(2)}%` : `${shortTermChange.toFixed(2)}%`,
        mediumTermPrediction: `¥${mediumTermPrice.toFixed(2)}`,
        tradingAdvice: shortTermChange > 2 ? '买入' : shortTermChange < -2 ? '卖出' : '持有',
        accuracy: `${(75 + Math.random() * 15).toFixed(1)}%`,
        technicalIndicators: {
            rsi: (30 + Math.random() * 40).toFixed(1),
            macd: (Math.random() - 0.5).toFixed(3),
            kdj: (40 + Math.random() * 40).toFixed(1),
            ma5: (currentPrice * (1 + (Math.random() - 0.5) * 0.05)).toFixed(2),
            ma20: (currentPrice * (1 + (Math.random() - 0.5) * 0.1)).toFixed(2),
            boll: `${(currentPrice * 0.95).toFixed(2)}-${(currentPrice * 1.05).toFixed(2)}`
        },
        priceHistory: generatePriceHistory(currentPrice)
    };
}

function generatePriceHistory(basePrice) {
    const history = [];
    const labels = [];
    let price = basePrice * 0.9;
    
    for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }));
        
        price = price * (1 + (Math.random() - 0.5) * 0.03);
        history.push(price.toFixed(2));
    }
    
    return { labels, data: history };
}

function displayPredictionResults(data) {
    // Update result cards
    document.getElementById('shortTermPrediction').textContent = data.shortTermPrediction;
    document.getElementById('mediumTermPrediction').textContent = data.mediumTermPrediction;
    document.getElementById('tradingAdvice').textContent = data.tradingAdvice;
    document.getElementById('accuracy').textContent = data.accuracy;
    
    // Update technical indicators
    document.getElementById('rsi').textContent = data.technicalIndicators.rsi;
    document.getElementById('macd').textContent = data.technicalIndicators.macd;
    document.getElementById('kdj').textContent = data.technicalIndicators.kdj;
    document.getElementById('ma5').textContent = data.technicalIndicators.ma5;
    document.getElementById('ma20').textContent = data.technicalIndicators.ma20;
    document.getElementById('boll').textContent = data.technicalIndicators.boll;
    
    // Apply color classes based on prediction
    const shortTermElement = document.getElementById('shortTermPrediction');
    const adviceElement = document.getElementById('tradingAdvice');
    
    if (data.shortTermPrediction.startsWith('+')) {
        shortTermElement.style.color = 'var(--success-color)';
    } else {
        shortTermElement.style.color = 'var(--danger-color)';
    }
    
    if (data.tradingAdvice === '买入') {
        adviceElement.style.color = 'var(--success-color)';
    } else if (data.tradingAdvice === '卖出') {
        adviceElement.style.color = 'var(--danger-color)';
    } else {
        adviceElement.style.color = 'var(--warning-color)';
    }
    
    // Update chart
    updatePriceChart(data.priceHistory);
    
    // Show results
    predictionResults.style.display = 'block';
}

function updatePriceChart(historyData) {
    // Simple chart implementation without Chart.js dependency
    const canvas = document.getElementById('priceChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = 300;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Get data points
    const data = historyData.data.map(v => parseFloat(v));
    const labels = historyData.labels;
    const maxValue = Math.max(...data);
    const minValue = Math.min(...data);
    const range = maxValue - minValue || 1;
    const padding = 40;
    
    // Draw grid
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i < 5; i++) {
        const y = padding + (height - padding * 2) * (i / 4);
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }
    
    // Draw line
    ctx.strokeStyle = 'rgb(59, 130, 246)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    data.forEach((value, index) => {
        const x = padding + (width - padding * 2) * (index / (data.length - 1));
        const y = height - padding - ((value - minValue) / range) * (height - padding * 2);
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    // Draw points
    ctx.fillStyle = 'rgb(59, 130, 246)';
    data.forEach((value, index) => {
        const x = padding + (width - padding * 2) * (index / (data.length - 1));
        const y = height - padding - ((value - minValue) / range) * (height - padding * 2);
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
    });
    
    // Draw labels
    ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
    ctx.font = '12px Inter, sans-serif';
    ctx.textAlign = 'center';
    
    // Show min and max values
    ctx.textAlign = 'right';
    ctx.fillText(maxValue.toFixed(2), padding - 5, padding + 5);
    ctx.fillText(minValue.toFixed(2), padding - 5, height - padding + 5);
    
    // Show date labels (first, middle, last)
    ctx.textAlign = 'center';
    if (labels.length > 0) {
        ctx.fillText(labels[0], padding, height - 10);
        ctx.fillText(labels[Math.floor(labels.length / 2)], width / 2, height - 10);
        ctx.fillText(labels[labels.length - 1], width - padding, height - 10);
    }
}

async function runPrediction() {
    const stockCode = stockCodeInput.value.trim();
    
    if (!stockCode) {
        alert('请输入股票代码');
        return;
    }
    
    showLoading();
    
    try {
        // Simulate API call with timeout
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // In a real application, you would call your backend API here:
        // const response = await fetch(`/api/predict/${stockCode}`);
        // const data = await response.json();
        
        // For now, use mock data
        const data = generateMockPredictionData(stockCode);
        displayPredictionResults(data);
    } catch (error) {
        console.error('Prediction error:', error);
        alert('预测过程中出现错误，请稍后重试');
    } finally {
        hideLoading();
    }
}

predictBtn.addEventListener('click', runPrediction);

stockCodeInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        runPrediction();
    }
});

// ===== Quick Search =====
quickSearch.addEventListener('input', (e) => {
    const searchTerm = e.target.value.trim();
    if (searchTerm.length >= 6) {
        // Auto-fill stock code input if on prediction view
        stockCodeInput.value = searchTerm;
    }
});

// ===== Watchlist Management =====
const addStockBtn = document.getElementById('addStockBtn');

addStockBtn.addEventListener('click', () => {
    const stockCode = prompt('请输入要添加的股票代码:');
    if (stockCode) {
        addToWatchlist(stockCode);
    }
});

function addToWatchlist(stockCode) {
    // In a real application, this would call an API
    const tbody = document.getElementById('watchlistBody');
    const mockData = generateMockWatchlistItem(stockCode);
    
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${mockData.code}</td>
        <td>${mockData.name}</td>
        <td>¥${mockData.price}</td>
        <td class="${mockData.change >= 0 ? 'positive' : 'negative'}">${mockData.change >= 0 ? '+' : ''}${mockData.change}%</td>
        <td>¥${mockData.targetPrice}</td>
        <td><span class="badge badge-success">正常</span></td>
        <td>
            <button class="btn-icon" title="详情"><span>ℹ️</span></button>
            <button class="btn-icon" title="删除" onclick="this.closest('tr').remove()"><span>🗑️</span></button>
        </td>
    `;
    
    tbody.appendChild(row);
}

function generateMockWatchlistItem(stockCode) {
    const price = 10 + Math.random() * 50;
    return {
        code: stockCode,
        name: '示例股票',
        price: price.toFixed(2),
        change: ((Math.random() - 0.5) * 5).toFixed(2),
        targetPrice: (price * 1.1).toFixed(2)
    };
}

// ===== Initialize Charts for Analytics View =====
function initAnalyticsCharts() {
    // Simple implementation without Chart.js
    // In production, these would be replaced with actual chart library or server-side rendering
    console.log('Analytics view loaded - charts would be rendered here');
}

// Initialize charts when analytics view is opened
navItems.forEach(item => {
    if (item.dataset.view === 'analytics') {
        item.addEventListener('click', () => {
            setTimeout(initAnalyticsCharts, 300);
        });
    }
});

// ===== Initialize Application =====
function init() {
    initTheme();
    
    // Set default view
    switchView('prediction');
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    console.log('SIAPS Web UI initialized');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ===== Utility Functions =====
function formatCurrency(value) {
    return `¥${parseFloat(value).toFixed(2)}`;
}

function formatPercentage(value) {
    const num = parseFloat(value);
    return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`;
}

// Export for potential use in other modules
window.SIAPS = {
    switchView,
    runPrediction,
    addToWatchlist,
    formatCurrency,
    formatPercentage
};
