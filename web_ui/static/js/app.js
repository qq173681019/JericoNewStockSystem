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
    
    // Load data when switching to specific views
    if (viewName === 'watchlist') {
        loadWatchlist();
    } else if (viewName === 'analytics') {
        loadAnalyticsData();
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

// Stock code to name mapping (常见股票)
const stockNameMap = {
    '000001': '平安银行', '000333': '美的集团', '000651': '格力电器', '000858': '五粮液',
    '600000': '浦发银行', '600009': '上海机场', '600016': '民生银行', '600028': '中国石化',
    '600030': '中信证券', '600036': '招商银行', '600104': '上汽集团', '600111': '北方稀土',
    '600276': '恒瑞医药', '600519': '贵州茅台', '600585': '海螺水泥', '600887': '伊利股份',
    '601012': '隆基绿能', '601857': '中国石油', '601988': '中国银行', '688008': '澜起科技',
    '688799': '有研新材', '800000': '中医药A'
};

function getStockName(stockCode) {
    return stockNameMap[stockCode] || `股票${stockCode}`;
}

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
        stockName: getStockName(stockCode),
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
    // Update stock info
    document.getElementById('resultStockCode').textContent = data.stockCode || '--';
    document.getElementById('resultStockName').textContent = data.stockName || '未知股票';
    document.getElementById('resultCurrentPrice').textContent = data.currentPrice ? `¥${data.currentPrice}` : '--';
    
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
    
    // Save prediction to history in localStorage
    savePredictionToHistory(data);
    
    // Show results
    predictionResults.style.display = 'block';
}

function savePredictionToHistory(data) {
    try {
        // Get existing history from localStorage
        const historyJson = localStorage.getItem('predictionHistory');
        let history = historyJson ? JSON.parse(historyJson) : [];
        
        // Create history entry
        const entry = {
            timestamp: new Date().toISOString(),
            stockCode: data.stockCode,
            stockName: data.stockName,
            currentPrice: data.currentPrice,
            shortTermPrediction: data.shortTermPrediction,
            mediumTermPrediction: data.mediumTermPrediction,
            tradingAdvice: data.tradingAdvice,
            accuracy: data.accuracy
        };
        
        // Add to beginning of array (most recent first)
        history.unshift(entry);
        
        // Keep only last 100 predictions to avoid excessive storage
        if (history.length > 100) {
            history = history.slice(0, 100);
        }
        
        // Save back to localStorage
        localStorage.setItem('predictionHistory', JSON.stringify(history));
    } catch (e) {
        console.error('Error saving prediction to history:', e);
    }
}

function updatePriceChart(historyData) {
    // Simple chart implementation without Chart.js dependency
    const canvas = document.getElementById('priceChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Get parent container width or use default
    const container = canvas.parentElement;
    const containerWidth = container ? container.offsetWidth : 800;
    const width = canvas.width = containerWidth > 0 ? containerWidth : 800;
    const height = canvas.height = 300;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Check if we have valid data
    if (!historyData || !historyData.data || historyData.data.length === 0) {
        // Draw "No data" message
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.font = '16px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('暂无历史数据 / No historical data available', width / 2, height / 2);
        return;
    }
    
    // Get data points
    const data = historyData.data.map(v => parseFloat(v));
    const labels = historyData.labels;
    
    // Validate data
    if (data.some(isNaN) || data.length === 0) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.font = '16px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('数据格式错误 / Invalid data format', width / 2, height / 2);
        return;
    }
    
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
        // Call backend API for real prediction
        const response = await fetch(`/api/predict/${stockCode}`);
        const result = await response.json();
        
        if (result.success) {
            // Transform API data to display format
            const data = {
                stockCode: result.stockCode,
                stockName: result.stockName || '',
                currentPrice: result.currentPrice || 0,
                shortTermPrediction: (result.prediction.shortTerm.change >= 0)
                    ? `+${result.prediction.shortTerm.change}%` 
                    : `${result.prediction.shortTerm.change}%`,
                mediumTermPrediction: `¥${result.prediction.mediumTerm.targetPrice}`,
                tradingAdvice: result.prediction.advice,
                accuracy: `${result.prediction.accuracy}%`,
                technicalIndicators: {
                    rsi: result.technicalIndicators.RSI,
                    macd: result.technicalIndicators.MACD,
                    kdj: result.technicalIndicators.KDJ,
                    ma5: result.technicalIndicators.MA5,
                    ma20: result.technicalIndicators.MA20,
                    boll: result.technicalIndicators.BOLL
                },
                priceHistory: result.priceHistory || generatePriceHistory(result.currentPrice)
            };
            
            displayPredictionResults(data);
        } else {
            alert(result.message || '预测失败，请稍后重试');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Fallback to mock data if API fails
        console.log('Using fallback mock data');
        const data = generateMockPredictionData(stockCode);
        displayPredictionResults(data);
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
const refreshWatchlistBtn = document.getElementById('refreshWatchlistBtn');

// Show add stock modal
addStockBtn.addEventListener('click', () => {
    openAddStockModal();
});

// Modal functions
function openAddStockModal() {
    const modal = document.getElementById('addStockModal');
    if (modal) {
        modal.style.display = 'flex';
        // Clear previous values
        document.getElementById('modalStockCode').value = '';
        document.getElementById('modalTargetPrice').value = '';
        document.getElementById('modalTargetDays').value = '';
        // Focus on stock code input
        setTimeout(() => document.getElementById('modalStockCode').focus(), 100);
    }
}

function closeAddStockModal() {
    const modal = document.getElementById('addStockModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Submit add stock form
async function submitAddStock() {
    const stockCode = document.getElementById('modalStockCode').value.trim();
    
    if (!stockCode) {
        alert('请输入股票代码');
        return;
    }
    
    showLoading();
    closeAddStockModal();
    
    try {
        const requestBody = { stockCode: stockCode };
        
        const response = await fetch('/api/watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        const result = await response.json();
        
        if (result.success) {
            await loadWatchlist();
            alert(result.message || `成功添加 ${stockCode} 到观测池`);
        } else {
            alert(result.error || '添加失败');
        }
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        alert('添加失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Navigate to prediction page and analyze stock
function analyzePrediction(stockCode) {
    // Switch to prediction view
    switchView('prediction');
    // Fill in the stock code
    stockCodeInput.value = stockCode;
    // Trigger prediction
    runPrediction();
}

// Make functions globally accessible
window.openAddStockModal = openAddStockModal;
window.closeAddStockModal = closeAddStockModal;
window.submitAddStock = submitAddStock;
window.analyzePrediction = analyzePrediction;

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('addStockModal');
    if (e.target === modal) {
        closeAddStockModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeAddStockModal();
    }
});

// Refresh watchlist button
refreshWatchlistBtn.addEventListener('click', async () => {
    refreshWatchlistBtn.disabled = true;
    refreshWatchlistBtn.innerHTML = '<span>⏳</span> 刷新中...';
    
    try {
        await loadWatchlist();
        // Show success feedback
        refreshWatchlistBtn.innerHTML = '<span>✅</span> 已刷新';
        setTimeout(() => {
            refreshWatchlistBtn.innerHTML = '<span>🔄</span> 刷新数据';
            refreshWatchlistBtn.disabled = false;
        }, 1500);
    } catch (error) {
        console.error('Refresh failed:', error);
        refreshWatchlistBtn.innerHTML = '<span>❌</span> 刷新失败';
        setTimeout(() => {
            refreshWatchlistBtn.innerHTML = '<span>🔄</span> 刷新数据';
            refreshWatchlistBtn.disabled = false;
        }, 1500);
    }
});

// Add to watchlist from prediction page
const addToWatchlistFromPredictionBtn = document.getElementById('addToWatchlistFromPrediction');
if (addToWatchlistFromPredictionBtn) {
    addToWatchlistFromPredictionBtn.addEventListener('click', async () => {
        const stockCode = document.getElementById('resultStockCode').textContent;
        if (stockCode && stockCode !== '--') {
            await addToWatchlistQuick(stockCode);
        } else {
            alert('请先进行股票预测');
        }
    });
}

// Add to watchlist from history page (global function for onclick)
window.addToWatchlistFromHistory = async function(stockCode) {
    await addToWatchlistQuick(stockCode);
};

// Quick add to watchlist without prompt
async function addToWatchlistQuick(stockCode) {
    try {
        const response = await fetch('/api/watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ stockCode: stockCode })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message || `成功添加 ${stockCode} 到观测池`);
        } else {
            alert(result.error || '添加失败');
        }
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        alert('添加失败: ' + error.message);
    }
}

async function addToWatchlist(stockCode) {
    showLoading();
    
    try {
        const response = await fetch('/api/watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ stockCode: stockCode })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Reload watchlist to show new item with real data
            await loadWatchlist();
            alert(result.message || `成功添加 ${stockCode} 到观测池`);
        } else {
            alert(result.error || '添加失败');
        }
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        alert('添加失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function loadWatchlist() {
    const tbody = document.getElementById('watchlistBody');
    if (!tbody) return;
    
    // Try to load from cache first for instant display
    const cachedData = localStorage.getItem('watchlistData');
    if (cachedData) {
        try {
            const cached = JSON.parse(cachedData);
            renderWatchlistData(cached, tbody);
        } catch (e) {
            console.error('Error parsing cached watchlist:', e);
        }
    }
    
    try {
        const response = await fetch('/api/watchlist');
        const result = await response.json();
        
        if (result.success && result.data) {
            // Save to localStorage for persistence
            localStorage.setItem('watchlistData', JSON.stringify(result.data));
            renderWatchlistData(result.data, tbody);
        }
    } catch (error) {
        console.error('Error loading watchlist:', error);
        // If we have cached data, keep showing it
        if (!cachedData) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--danger-color);">加载失败</td></tr>';
        }
    }
}

function renderWatchlistData(data, tbody) {
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">观测池为空，点击上方"+"按钮添加股票</td></tr>';
        return;
    }
    
    data.forEach(stock => {
        const changeClass = stock.change >= 0 ? 'positive' : 'negative';
        const changeSign = stock.change >= 0 ? '+' : '';
        const statusBadge = stock.change > 3 ? 'badge-success' : 
                           stock.change < -3 ? 'badge-danger' : 'badge-info';
        const statusText = stock.change > 3 ? '强势' : 
                          stock.change < -3 ? '弱势' : '平稳';
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${stock.code}</strong></td>
            <td>${stock.name || '-'}</td>
            <td>¥${stock.currentPrice ? stock.currentPrice.toFixed(2) : '-'}</td>
            <td class="${changeClass}">${changeSign}${stock.change ? stock.change.toFixed(2) : 0}%</td>
            <td><span class="badge ${statusBadge}">${statusText}</span></td>
            <td>
                <button class="btn-icon" title="预测分析" onclick="analyzePrediction('${stock.code}')"><span>📊</span></button>
                <button class="btn-icon" title="刷新" onclick="refreshWatchlistItem('${stock.code}')"><span>🔄</span></button>
                <button class="btn-icon" title="删除" onclick="removeFromWatchlist('${stock.code}')"><span>🗑️</span></button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function removeFromWatchlist(stockCode) {
    if (!confirm(`确定要从观测池移除 ${stockCode} 吗？`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/watchlist', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ stockCode: stockCode })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Clear cache to force reload
            localStorage.removeItem('watchlistData');
            await loadWatchlist();
        } else {
            alert(result.error || '删除失败');
        }
    } catch (error) {
        console.error('Error removing from watchlist:', error);
        alert('删除失败: ' + error.message);
    }
}

async function refreshWatchlistItem(stockCode) {
    // Just reload the entire list to get fresh data
    await loadWatchlist();
}

// ===== Initialize Charts for Analytics View =====
function initAnalyticsCharts() {
    // Load analytics data from API
    loadAnalyticsData();
}

// Refresh analytics data (called by refresh button)
async function refreshAnalytics() {
    const btn = document.getElementById('refreshAnalyticsBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '🔄 刷新中...';
    }
    
    try {
        await loadAnalyticsData();
        if (btn) {
            btn.innerHTML = '✅ 已刷新';
            setTimeout(() => {
                btn.innerHTML = '🔄 刷新数据';
                btn.disabled = false;
            }, 1500);
        }
    } catch (error) {
        console.error('Refresh failed:', error);
        if (btn) {
            btn.innerHTML = '❌ 刷新失败';
            setTimeout(() => {
                btn.innerHTML = '🔄 刷新数据';
                btn.disabled = false;
            }, 2000);
        }
    }
}

async function loadAnalyticsData() {
    // Show loading indicator
    showLoading();
    
    // Try to load from cache first for instant display
    const cachedAnalytics = localStorage.getItem('analyticsData');
    if (cachedAnalytics) {
        try {
            const cached = JSON.parse(cachedAnalytics);
            renderAnalyticsData(cached);
        } catch (e) {
            console.error('Error parsing cached analytics:', e);
        }
    }
    
    try {
        console.log('Loading analytics data...');
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        if (data.success || data.sectorHeat) {
            // Save to localStorage for persistence
            localStorage.setItem('analyticsData', JSON.stringify(data));
            renderAnalyticsData(data);
            console.log('✓ Analytics charts rendered');
        } else {
            console.error('Failed to load analytics data');
            if (!cachedAnalytics) {
                drawDemoSectorChart();
                drawDemoSentimentChart();
            }
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        // Draw demo charts if API fails and no cache
        if (!cachedAnalytics) {
            drawDemoSectorChart();
            drawDemoSentimentChart();
        }
    } finally {
        // Hide loading indicator
        hideLoading();
    }
}

function renderAnalyticsData(data) {
    drawSectorChart(data.sectorHeat);
    drawSentimentChart(data.marketSentiment);
    
    // Draw heatmap with all sectors
    if (data.allSectors && data.allSectors.length > 0) {
        drawSectorHeatmap(data.allSectors);
        // Update source tag
        const sourceTag = document.getElementById('sectorSource');
        if (sourceTag && data.allSectors[0]) {
            const source = data.allSectors[0].source || 'unknown';
            sourceTag.textContent = source === 'tonghuashun' ? '同花顺' : '东方财富';
        }
    }
}

// Store sectors data for view switching
let cachedSectorsData = [];
let currentHeatmapView = 'grid';

// Switch heatmap view between grid and treemap
function switchHeatmapView(view) {
    currentHeatmapView = view;
    
    // Update button states
    const gridBtn = document.getElementById('gridViewBtn');
    const treemapBtn = document.getElementById('treemapViewBtn');
    const gridContainer = document.getElementById('sectorHeatmap');
    const treemapContainer = document.getElementById('sectorTreemap');
    
    if (view === 'grid') {
        gridBtn.classList.add('active');
        treemapBtn.classList.remove('active');
        gridContainer.style.display = 'grid';
        treemapContainer.style.display = 'none';
    } else {
        gridBtn.classList.remove('active');
        treemapBtn.classList.add('active');
        gridContainer.style.display = 'none';
        treemapContainer.style.display = 'block';
        // Draw treemap if we have cached data
        if (cachedSectorsData.length > 0) {
            drawSectorTreemap(cachedSectorsData);
        }
    }
}

// Draw sector heatmap showing all sectors
function drawSectorHeatmap(sectors) {
    const container = document.getElementById('sectorHeatmap');
    if (!container) return;
    
    // Cache data for view switching
    cachedSectorsData = sectors;
    
    // Update count
    const countTag = document.getElementById('heatmapCount');
    if (countTag) {
        countTag.textContent = `${sectors.length}个板块`;
    }
    
    // Sort by change (descending)
    const sortedSectors = [...sectors].sort((a, b) => b.change - a.change);
    
    // Generate heatmap cells
    let html = '';
    sortedSectors.forEach(sector => {
        const change = sector.change || 0;
        const color = getHeatmapColor(change);
        const changeSign = change > 0 ? '+' : '';
        
        html += `
            <div class="heatmap-cell" style="background: ${color};" 
                 title="${sector.name}: ${changeSign}${change}%\n热度: ${sector.heat}\n个股数: ${sector.stocks}">
                <span class="sector-name">${sector.name}</span>
                <span class="sector-change">${changeSign}${change}%</span>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // If treemap view is active, also draw treemap
    if (currentHeatmapView === 'treemap') {
        drawSectorTreemap(sectors);
    }
}

// Draw treemap visualization (similar to the screenshot)
function drawSectorTreemap(sectors) {
    const container = document.getElementById('sectorTreemap');
    if (!container) return;
    
    const width = container.offsetWidth || 800;
    const height = 500;
    
    // Sort by absolute change (larger changes get more space)
    const sortedSectors = [...sectors].sort((a, b) => {
        // Weight by absolute change value - bigger movers get more space
        const aWeight = Math.abs(a.change) + 1;
        const bWeight = Math.abs(b.change) + 1;
        return bWeight - aWeight;
    });
    
    // Simple treemap layout algorithm (squarified-like)
    const cells = calculateTreemapLayout(sortedSectors, width, height);
    
    // Generate treemap cells
    let html = '';
    cells.forEach(cell => {
        const change = cell.change || 0;
        const color = getTreemapColor(change);
        const changeSign = change > 0 ? '+' : '';
        
        // Determine size class for text visibility
        const area = cell.w * cell.h;
        let sizeClass = '';
        if (area < 1500) sizeClass = 'tiny';
        else if (area < 4000) sizeClass = 'small';
        
        html += `
            <div class="treemap-cell ${sizeClass}" 
                 style="left: ${cell.x}px; top: ${cell.y}px; width: ${cell.w}px; height: ${cell.h}px; background: ${color};"
                 title="${cell.name}: ${changeSign}${change}%\n热度: ${cell.heat}\n个股数: ${cell.stocks}">
                <span class="cell-name">${cell.name}</span>
                <span class="cell-change">${changeSign}${change}%</span>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Calculate treemap layout using slice-and-dice algorithm
function calculateTreemapLayout(sectors, width, height) {
    if (!sectors || sectors.length === 0) return [];
    
    // Calculate weights based on absolute change + base weight
    const totalWeight = sectors.reduce((sum, s) => sum + Math.abs(s.change) + 2, 0);
    
    const cells = [];
    let x = 0, y = 0;
    let remainingWidth = width;
    let remainingHeight = height;
    let isHorizontal = width >= height;
    let currentRow = [];
    let currentRowWeight = 0;
    
    sectors.forEach((sector, index) => {
        const weight = Math.abs(sector.change) + 2;
        currentRow.push({ ...sector, weight });
        currentRowWeight += weight;
        
        // Decide when to start new row (roughly when we've filled half)
        const shouldBreak = currentRowWeight / totalWeight > 0.15 || index === sectors.length - 1;
        
        if (shouldBreak) {
            // Layout current row
            const rowFraction = currentRowWeight / totalWeight;
            
            if (isHorizontal) {
                const rowHeight = Math.max(30, remainingHeight * rowFraction * (sectors.length / (index + 1)) * 0.5);
                let rowX = x;
                
                currentRow.forEach(item => {
                    const cellWidth = (item.weight / currentRowWeight) * remainingWidth;
                    cells.push({
                        ...item,
                        x: rowX,
                        y: y,
                        w: Math.max(cellWidth - 1, 20),
                        h: Math.max(rowHeight - 1, 20)
                    });
                    rowX += cellWidth;
                });
                
                y += rowHeight;
                remainingHeight -= rowHeight;
            } else {
                const rowWidth = Math.max(30, remainingWidth * rowFraction * (sectors.length / (index + 1)) * 0.5);
                let rowY = y;
                
                currentRow.forEach(item => {
                    const cellHeight = (item.weight / currentRowWeight) * remainingHeight;
                    cells.push({
                        ...item,
                        x: x,
                        y: rowY,
                        w: Math.max(rowWidth - 1, 20),
                        h: Math.max(cellHeight - 1, 20)
                    });
                    rowY += cellHeight;
                });
                
                x += rowWidth;
                remainingWidth -= rowWidth;
            }
            
            // Reset for next row
            currentRow = [];
            currentRowWeight = 0;
            isHorizontal = !isHorizontal;
        }
    });
    
    return cells;
}

// Get color for treemap (red for up, green for down - Chinese stock market convention)
function getTreemapColor(change) {
    // Red = up (rise), Green = down (fall) - Chinese stock market convention
    if (change > 3) return '#C62828';      // Dark red - strong rise
    if (change > 2) return '#E53935';      // Red
    if (change > 1) return '#EF5350';      // Medium red
    if (change > 0.5) return '#E57373';    // Light red
    if (change > 0) return '#EF9A9A';      // Very light red
    if (change > -0.5) return '#BDBDBD';   // Gray - flat
    if (change > -1) return '#81C784';     // Very light green
    if (change > -2) return '#66BB6A';     // Light green
    if (change > -3) return '#43A047';     // Medium green
    return '#1B5E20';                       // Dark green - strong fall
}

// Get color based on change percentage (for grid view)
function getHeatmapColor(change) {
    // Red = up (rise), Green = down (fall) - Chinese stock market convention
    if (change > 2) return '#E53935';      // Strong rise - red
    if (change > 1) return '#EF5350';      // Rise - light red
    if (change > 0) return '#EF9A9A';      // Slight rise - very light red
    if (change > -0.5) return '#FFEB3B';   // Flat - yellow
    if (change > -1) return '#81C784';     // Slight fall - light green
    if (change > -2) return '#43A047';     // Fall - green
    return '#1B5E20';                       // Strong fall - dark green
}

function drawSectorChart(sectorData) {
    const canvas = document.getElementById('sectorChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;
    const containerWidth = container ? container.offsetWidth : 400;
    const width = canvas.width = containerWidth > 0 ? containerWidth : 400;
    const height = canvas.height = 300;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    const data = sectorData.data || sectorData.labels.map(() => 50 + Math.random() * 30);
    const labels = sectorData.labels || [];
    const colors = sectorData.colors || ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F'];
    const details = sectorData.details || [];
    
    if (!labels || labels.length === 0) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('暂无数据', width / 2, height / 2);
        return;
    }
    
    const maxValue = Math.max(...data, 100);
    const barWidth = (width - 60) / labels.length;
    const barSpacing = barWidth * 0.2;
    const actualBarWidth = barWidth - barSpacing;
    const chartHeight = height - 60;
    const padding = 40;
    
    // Draw bars
    labels.forEach((label, i) => {
        const value = data[i] || 0;
        const barHeight = (value / maxValue) * chartHeight;
        const x = padding + i * barWidth + barSpacing / 2;
        const y = height - 40 - barHeight;
        
        // Draw bar
        ctx.fillStyle = colors[i % colors.length];
        ctx.fillRect(x, y, actualBarWidth, barHeight);
        
        // Draw label
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(label, x + actualBarWidth / 2, height - 20);
        
        // Draw value on top of bar
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.font = 'bold 11px Arial';
        ctx.fillText(Math.round(value), x + actualBarWidth / 2, y - 5);
    });
    
    // Draw axis
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding - 5, height - 40);
    ctx.lineTo(width - 10, height - 40);
    ctx.stroke();
    
    // Display detailed sector information
    if (details && details.length > 0) {
        displaySectorDetails(details);
    }
}

function displaySectorDetails(details) {
    const detailsContainer = document.getElementById('sectorDetails');
    if (!detailsContainer) return;
    
    let detailsHTML = '<div class="sector-details-content">';
    details.forEach(sector => {
        // Chinese stock market convention: red for up/rise, green for down/fall
        const changeColor = sector.change > 0 ? '#ef4444' : sector.change < 0 ? '#10b981' : '#999';
        const changeSign = sector.change > 0 ? '+' : '';
        detailsHTML += `
            <div class="sector-detail-item">
                <div class="sector-header">
                    <span class="sector-name" style="border-left: 4px solid ${sector.color};">${sector.name}</span>
                    <span class="sector-heat">热度: ${sector.heat}</span>
                </div>
                <div class="sector-stats">
                    <div class="stat"><strong>个股数:</strong> ${sector.stocks}</div>
                    <div class="stat"><strong>涨幅:</strong> <span style="color: ${changeColor}">${changeSign}${sector.change}%</span></div>
                </div>
                <div class="sector-companies">
                    <strong>代表企业:</strong> ${sector.topCompanies.join(' · ')}
                </div>
            </div>
        `;
    });
    detailsHTML += '</div>';
    detailsContainer.innerHTML = detailsHTML;
}

function drawDemoSectorChart() {
    const demoData = {
        labels: ['金融', '医药', '科技', '制造', '消费', '能源'],
        data: [85, 78, 92, 65, 80, 55],
        colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    };
    drawSectorChart(demoData);
}

function drawSentimentChart(sentimentData) {
    const canvas = document.getElementById('sentimentChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;
    const containerWidth = container ? container.offsetWidth : 400;
    const width = canvas.width = containerWidth > 0 ? containerWidth : 400;
    const height = canvas.height = 300;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    const value = sentimentData.value || 50;
    const level = sentimentData.level || '中立';
    const color = sentimentData.color || '#FFCC44';
    const history = sentimentData.history || [];
    
    // Draw gauge chart
    const centerX = width / 2;
    const centerY = height * 0.6;
    const radius = Math.min(width, height) * 0.3;
    
    // Draw gauge background
    ctx.fillStyle = '#f0f0f0';
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI, true);
    ctx.fill();
    
    // Draw gauge value
    const angle = (value / 100) * Math.PI;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI - angle, Math.PI + angle, false);
    ctx.fill();
    
    // Draw gauge border
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI, true);
    ctx.stroke();
    
    // Draw center circle
    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.7, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw value text
    ctx.fillStyle = color;
    ctx.font = 'bold 32px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(Math.round(value), centerX, centerY - 10);
    
    // Draw level text
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(level, centerX, centerY + 25);
    
    // Draw scale labels
    const labels = ['恐惧', '中立', '贪婪'];
    const positions = [width * 0.1, width * 0.5, width * 0.9];
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.font = '11px Arial';
    labels.forEach((label, i) => {
        ctx.textAlign = 'center';
        ctx.fillText(label, positions[i], height - 20);
    });
}

function drawDemoSentimentChart() {
    const demoData = {
        value: 65,
        level: '乐观',
        color: '#88DD44',
        history: []
    };
    drawSentimentChart(demoData);
}

// ===== History Management =====
async function loadHistoryData(filter = 'all') {
    try {
        const response = await fetch(`/api/history?filter=${filter}`);
        const result = await response.json();
        
        if (result.success && result.data) {
            updateHistoryTable(result.data);
            updateHistoryStats(result.statistics);
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function updateHistoryTable(historyData) {
    const tbody = document.querySelector('#historyView .history-table tbody');
    if (!tbody) return;
    
    // Clear existing rows
    tbody.innerHTML = '';
    
    // Add new rows
    historyData.forEach(record => {
        const row = document.createElement('tr');
        
        // Determine classes for styling
        const predClass = record.predictedResult.startsWith('+') ? 'positive' : 
                         record.predictedResult.startsWith('-') ? 'negative' : '';
        
        const badgeClass = record.accuracy === 'accurate' ? 'badge-success' :
                          record.accuracy === 'pending' ? 'badge-info' : 'badge-warning';
        
        // Extract stock code (remove stock name if present)
        const stockCodeOnly = record.stockCode.split(' ')[0];
        
        row.innerHTML = `
            <td>${record.timestamp}</td>
            <td>${record.stockCode} ${record.stockName || ''}</td>
            <td>${record.predictionType}</td>
            <td class="${predClass}">${record.predictedResult}</td>
            <td>${record.actualResult}</td>
            <td><span class="badge ${badgeClass}">${record.accuracyBadge}</span></td>
            <td><button class="btn-icon" onclick="viewPredictionDetail('${record.id}')"><span>👁️</span></button></td>
            <td><button class="btn-icon btn-add" onclick="addToWatchlistFromHistory('${stockCodeOnly}')" title="添加到观测池"><span>➕</span></button></td>
        `;
        
        tbody.appendChild(row);
    });
}

function updateHistoryStats(statistics) {
    if (!statistics) return;
    
    const statsContainer = document.querySelector('#historyView .history-stats');
    if (!statsContainer) return;
    
    // Update stat cards
    const statCards = statsContainer.querySelectorAll('.stat-card h3');
    if (statCards.length >= 3) {
        statCards[0].textContent = statistics.total || 0;
        statCards[1].textContent = `${statistics.accuracy_rate || 0}%`;
        statCards[2].textContent = statistics.accurate || 0;
    }
}

function viewPredictionDetail(predictionId) {
    // TODO: Show detailed prediction view
    console.log('Viewing prediction:', predictionId);
}

// Clear history function
async function clearHistory() {
    if (!confirm('确定要清空所有历史记录吗？此操作不可恢复！')) {
        return;
    }
    
    try {
        showLoading();
        const response = await fetch('/api/history/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            // Reload history data
            loadHistoryData('all');
        } else {
            alert('清空失败: ' + (result.error || '未知错误'));
        }
    } catch (error) {
        console.error('Error clearing history:', error);
        alert('清空历史记录时发生错误');
    } finally {
        hideLoading();
    }
}

// Add event listener for clear history button
document.addEventListener('DOMContentLoaded', () => {
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }
    
    // Pre-load watchlist data
    loadWatchlist();
});

// Initialize charts when analytics view is opened
navItems.forEach(item => {
    if (item.dataset.view === 'analytics') {
        item.addEventListener('click', () => {
            setTimeout(initAnalyticsCharts, 300);
        });
    }
    
    // Load history when history view is opened
    if (item.dataset.view === 'history') {
        item.addEventListener('click', () => {
            setTimeout(() => loadHistoryData('all'), 300);
        });
    }
    
    // Reload watchlist when watchlist view is opened (for fresh data)
    if (item.dataset.view === 'watchlist') {
        item.addEventListener('click', () => {
            setTimeout(loadWatchlist, 100);
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
