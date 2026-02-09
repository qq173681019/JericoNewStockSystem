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

// ===== Configuration Constants =====
const MAX_PREDICTION_HISTORY = 100; // Maximum number of prediction entries to keep in localStorage

// Backup/Import messages
const IMPORT_MODE_MESSAGE = '选择导入模式：\n\n点击"确定"= 合并模式（保留现有数据，更新重复项）\n点击"取消"= 替换模式（清空现有数据）\n\n建议选择"确定"进行合并';

// Helper function for consistent timestamp format
function formatTimestamp() {
    return new Date().toISOString().replace(/[-:]/g, '').replace('T', '_').split('.')[0];
}

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
    
    // Update technical indicators
    document.getElementById('rsi').textContent = data.technicalIndicators.rsi;
    document.getElementById('macd').textContent = data.technicalIndicators.macd;
    document.getElementById('kdj').textContent = data.technicalIndicators.kdj;
    document.getElementById('ma5').textContent = data.technicalIndicators.ma5;
    document.getElementById('ma20').textContent = data.technicalIndicators.ma20;
    document.getElementById('boll').textContent = data.technicalIndicators.boll;
    
    // Apply color classes based on prediction
    // Note: Following Chinese stock market convention where red=up/rise, green=down/fall
    // CSS variables: --success-color (red #ef4444), --danger-color (green #10b981)
    const shortTermElement = document.getElementById('shortTermPrediction');
    const mediumTermElement = document.getElementById('mediumTermPrediction');
    const adviceElement = document.getElementById('tradingAdvice');
    
    if (data.shortTermPrediction.startsWith('+')) {
        shortTermElement.style.color = 'var(--success-color)';
    } else {
        shortTermElement.style.color = 'var(--danger-color)';
    }
    
    // Apply color to medium-term prediction based on comparison with current price
    // Note: Following Chinese stock market convention (red=up, green=down)
    // --success-color is red (#ef4444) and --danger-color is green (#10b981)
    if (data.mediumTermPrediction && data.currentPrice) {
        // Extract price from format "¥XX.XX"
        const mediumPriceMatch = data.mediumTermPrediction.match(/[\d.]+/);
        if (mediumPriceMatch) {
            const mediumPrice = parseFloat(mediumPriceMatch[0]);
            const currentPrice = parseFloat(data.currentPrice);
            if (mediumPrice > currentPrice) {
                mediumTermElement.style.color = 'var(--success-color)'; // Red for higher price (upward)
            } else if (mediumPrice < currentPrice) {
                mediumTermElement.style.color = 'var(--danger-color)'; // Green for lower price (downward)
            } else {
                mediumTermElement.style.color = 'var(--text-primary)'; // Default for equal
            }
        }
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

function displayErrorMessage(message, errorType) {
    // Hide the prediction results section
    predictionResults.style.display = 'none';
    
    // Create or update error message display
    let errorDiv = document.getElementById('predictionError');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'predictionError';
        errorDiv.className = 'error-message-container';
        
        // Insert after the prediction form
        const form = document.querySelector('.prediction-form');
        if (form && form.parentNode) {
            form.parentNode.insertBefore(errorDiv, form.nextSibling);
        }
    }
    
    // Set error message content with icon and styling
    let errorIcon = '⚠️';
    let errorTitle = '无法获取数据';
    
    if (errorType === 'no_real_data' || errorType === 'no_historical_data') {
        errorIcon = '📊';
        errorTitle = '无法获取真实数据';
    } else if (errorType === 'network_error') {
        errorIcon = '🌐';
        errorTitle = '网络错误';
    } else if (errorType === 'prediction_failed') {
        errorIcon = '⚠️';
        errorTitle = '预测失败';
    }
    
    errorDiv.innerHTML = `
        <div class="error-card">
            <div class="error-icon">${errorIcon}</div>
            <h3 class="error-title">${errorTitle}</h3>
            <p class="error-message">${message}</p>
            <div class="error-suggestions">
                <p><strong>建议：</strong></p>
                <ul>
                    <li>检查股票代码是否正确（如：000001、600036）</li>
                    <li>确认股票是否在交易时间内</li>
                    <li>稍后再试</li>
                </ul>
            </div>
        </div>
    `;
    
    errorDiv.style.display = 'block';
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
            tradingAdvice: data.tradingAdvice
        };
        
        // Add to beginning of array (most recent first)
        history.unshift(entry);
        
        // Keep only last MAX_PREDICTION_HISTORY predictions to avoid excessive storage
        if (history.length > MAX_PREDICTION_HISTORY) {
            history = history.slice(0, MAX_PREDICTION_HISTORY);
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
            
            // Also load multi-timeframe predictions
            loadMultiTimeframePredictions(stockCode);
        } else {
            // Show error message instead of displaying predictions
            hideLoading();
            displayErrorMessage(result.message || '预测失败，请稍后重试', result.error);
        }
    } catch (error) {
        console.error('Prediction error:', error);
        hideLoading();
        displayErrorMessage('网络错误，无法连接到服务器', 'network_error');
    }
}

// Load multi-timeframe predictions
async function loadMultiTimeframePredictions(stockCode) {
    const timeframes = ['30min', '1day'];
    
    for (const timeframe of timeframes) {
        // Set loading state
        setTimeframeLoading(timeframe, true);
        
        try {
            const response = await fetch(`/api/predict/multi/${stockCode}?timeframe=${timeframe}`);
            const result = await response.json();
            
            if (result.success) {
                updateTimeframeCard(timeframe, result);
            } else {
                setTimeframeError(timeframe, result.message || '预测失败');
            }
        } catch (error) {
            console.error(`Error loading ${timeframe} prediction:`, error);
            setTimeframeError(timeframe, '网络错误');
        } finally {
            setTimeframeLoading(timeframe, false);
        }
    }
}

// Set timeframe card loading state
function setTimeframeLoading(timeframe, isLoading) {
    const statusElement = document.getElementById(`status${timeframe}`);
    if (statusElement) {
        if (isLoading) {
            statusElement.textContent = '加载中...';
            statusElement.className = 'timeframe-status loading';
        } else {
            statusElement.className = 'timeframe-status';
        }
    }
}

// Set timeframe card error state
function setTimeframeError(timeframe, message) {
    const statusElement = document.getElementById(`status${timeframe}`);
    if (statusElement) {
        statusElement.textContent = '❌';
        statusElement.className = 'timeframe-status error';
        statusElement.title = message || '无法获取数据';
    }
    
    // Set error message instead of placeholder values
    const priceElement = document.getElementById(`price${timeframe}`);
    const changeElement = document.getElementById(`change${timeframe}`);
    const confidenceElement = document.getElementById(`confidence${timeframe}`);
    
    if (priceElement) {
        priceElement.textContent = '数据不可用';
        priceElement.style.fontSize = '14px';
        priceElement.style.color = 'var(--text-secondary)';
    }
    if (changeElement) {
        changeElement.textContent = '--';
        changeElement.style.color = 'var(--text-secondary)';
    }
    if (confidenceElement) {
        confidenceElement.textContent = '--';
        confidenceElement.style.color = 'var(--text-secondary)';
    }
}

// Update timeframe card with prediction data
function updateTimeframeCard(timeframe, data) {
    // Update status (no more fallback, only success)
    const statusElement = document.getElementById(`status${timeframe}`);
    if (statusElement) {
        statusElement.textContent = '✓';
        statusElement.className = 'timeframe-status success';
        statusElement.title = '';
    }
    
    // Update price
    const priceElement = document.getElementById(`price${timeframe}`);
    if (priceElement && data.prediction && data.prediction.targetPrice) {
        priceElement.textContent = `¥${data.prediction.targetPrice}`;
        priceElement.style.fontSize = '';  // Reset to default
        
        // Apply color based on expected change direction
        if (data.prediction.expectedChange !== undefined) {
            const change = data.prediction.expectedChange;
            if (change > 0) {
                priceElement.className = 'value-number positive';
            } else if (change < 0) {
                priceElement.className = 'value-number negative';
            } else {
                priceElement.className = 'value-number neutral';
            }
            priceElement.style.opacity = '1';
        }
    }
    
    // Update change
    const changeElement = document.getElementById(`change${timeframe}`);
    if (changeElement && data.prediction && data.prediction.expectedChange !== undefined) {
        const change = data.prediction.expectedChange;
        const changeText = change >= 0 ? `+${change.toFixed(2)}%` : `${change.toFixed(2)}%`;
        changeElement.textContent = changeText;
        
        // Apply color based on direction
        if (change > 0) {
            changeElement.className = 'change-number positive';
        } else if (change < 0) {
            changeElement.className = 'change-number negative';
        } else {
            changeElement.className = 'change-number neutral';
        }
        changeElement.style.opacity = '1';
    }
    
    // Update confidence
    const confidenceElement = document.getElementById(`confidence${timeframe}`);
    if (confidenceElement && data.prediction && data.prediction.confidence !== undefined) {
        const confidence = (data.prediction.confidence * 100).toFixed(0);
        confidenceElement.textContent = `${confidence}%`;
        
        // Style based on confidence level
        if (isFallback || data.prediction.confidence < 0.4) {
            confidenceElement.style.color = '#ff6b6b';
        } else if (data.prediction.confidence < 0.7) {
            confidenceElement.style.color = '#ffa500';
        } else {
            confidenceElement.style.color = '#51cf66';
        }
    }
}

// Timeframe button click handlers
document.addEventListener('DOMContentLoaded', () => {
    const timeframeButtons = document.querySelectorAll('.btn-timeframe');
    
    timeframeButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            timeframeButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Optionally highlight the corresponding card
            const timeframe = button.dataset.timeframe;
            highlightTimeframeCard(timeframe);
        });
    });
});

// Highlight selected timeframe card
function highlightTimeframeCard(timeframe) {
    const cards = document.querySelectorAll('.timeframe-card');
    cards.forEach(card => {
        if (card.dataset.timeframe === timeframe) {
            card.style.borderColor = 'var(--primary-color)';
            card.style.transform = 'scale(1.02)';
            card.style.backgroundColor = 'var(--bg-secondary)';
            card.setAttribute('aria-selected', 'true');
        } else {
            card.style.borderColor = 'var(--border-color)';
            card.style.transform = 'scale(1)';
            card.style.backgroundColor = 'var(--bg-primary)';
            card.setAttribute('aria-selected', 'false');
        }
    });
    
    // Scroll to card if needed
    const selectedCard = document.querySelector(`.timeframe-card[data-timeframe="${timeframe}"]`);
    if (selectedCard) {
        selectedCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
        const stockCodeInput = document.getElementById('modalStockCode');
        if (stockCodeInput) {
            stockCodeInput.value = '';
        }
        // Clear optional fields if they exist
        const targetPriceInput = document.getElementById('modalTargetPrice');
        if (targetPriceInput) {
            targetPriceInput.value = '';
        }
        const targetDaysInput = document.getElementById('modalTargetDays');
        if (targetDaysInput) {
            targetDaysInput.value = '';
        }
        // Focus on stock code input
        setTimeout(() => {
            if (stockCodeInput) {
                stockCodeInput.focus();
            }
        }, 100);
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

// Export watchlist button
const exportWatchlistBtn = document.getElementById('exportWatchlistBtn');
if (exportWatchlistBtn) {
    exportWatchlistBtn.addEventListener('click', async () => {
        try {
            exportWatchlistBtn.disabled = true;
            exportWatchlistBtn.innerHTML = '<span>⏳</span> 导出中...';
            
            const response = await fetch('/api/watchlist/export');
            const result = await response.json();
            
            if (result.success) {
                // Create a download link
                const dataStr = JSON.stringify(result.data, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                // Use consistent timestamp format with backend
                link.download = `watchlist_backup_${formatTimestamp()}.json`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                exportWatchlistBtn.innerHTML = '<span>✅</span> 已导出';
                setTimeout(() => {
                    exportWatchlistBtn.innerHTML = '<span>📥</span> 导出';
                    exportWatchlistBtn.disabled = false;
                }, 1500);
            } else {
                throw new Error(result.error || '导出失败');
            }
        } catch (error) {
            console.error('Export error:', error);
            alert('导出失败: ' + error.message);
            exportWatchlistBtn.innerHTML = '<span>❌</span> 导出失败';
            setTimeout(() => {
                exportWatchlistBtn.innerHTML = '<span>📥</span> 导出';
                exportWatchlistBtn.disabled = false;
            }, 1500);
        }
    });
}

// Import watchlist button
const importWatchlistBtn = document.getElementById('importWatchlistBtn');
const importFileInput = document.getElementById('importFileInput');

if (importWatchlistBtn && importFileInput) {
    importWatchlistBtn.addEventListener('click', () => {
        importFileInput.click();
    });
    
    importFileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        
        try {
            importWatchlistBtn.disabled = true;
            importWatchlistBtn.innerHTML = '<span>⏳</span> 导入中...';
            
            const reader = new FileReader();
            reader.onload = async (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    // Ask user if they want to merge or replace with clearer message
                    const merge = confirm(IMPORT_MODE_MESSAGE);
                    
                    const response = await fetch('/api/watchlist/import', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({data, merge})
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        alert(result.message);
                        await loadWatchlist();
                        importWatchlistBtn.innerHTML = '<span>✅</span> 已导入';
                    } else {
                        throw new Error(result.error || '导入失败');
                    }
                } catch (error) {
                    console.error('Import error:', error);
                    alert('导入失败: ' + error.message);
                    importWatchlistBtn.innerHTML = '<span>❌</span> 导入失败';
                } finally {
                    setTimeout(() => {
                        importWatchlistBtn.innerHTML = '<span>📤</span> 导入';
                        importWatchlistBtn.disabled = false;
                    }, 1500);
                }
            };
            
            reader.readAsText(file);
            // Reset file input
            importFileInput.value = '';
        } catch (error) {
            console.error('File read error:', error);
            alert('读取文件失败: ' + error.message);
            importWatchlistBtn.innerHTML = '<span>❌</span> 导入失败';
            setTimeout(() => {
                importWatchlistBtn.innerHTML = '<span>📤</span> 导入';
                importWatchlistBtn.disabled = false;
            }, 1500);
        }
    });
}

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
    
    // Use clientWidth for more accurate width (excludes scrollbar and padding)
    // Subtract a small buffer to prevent horizontal overflow
    const rawWidth = container.clientWidth || container.offsetWidth || 800;
    const width = rawWidth - 2; // Subtract 2px to account for potential borders
    // Determine if mobile based on viewport width, not just container width
    const isMobile = window.innerWidth < 768;
    
    // Calculate dynamic height based on number of sectors and available area
    // More sectors = need more height, especially on mobile
    const sectorsCount = sectors.length;
    let height;
    if (isMobile) {
        // Mobile: calculate based on sectors count with minimum height per sector
        // Allocate 70px per sector on average, with min/max bounds
        height = Math.max(
            TREEMAP_CONFIG.MIN_MOBILE_HEIGHT, 
            Math.min(TREEMAP_CONFIG.MAX_MOBILE_HEIGHT, sectorsCount * TREEMAP_CONFIG.MOBILE_HEIGHT_PER_SECTOR)
        );
    } else {
        // Desktop: also scale with sector count but less aggressively (30px per sector)
        height = Math.max(
            TREEMAP_CONFIG.MIN_DESKTOP_HEIGHT, 
            Math.min(TREEMAP_CONFIG.MAX_DESKTOP_HEIGHT, sectorsCount * TREEMAP_CONFIG.DESKTOP_HEIGHT_PER_SECTOR)
        );
    }
    
    // Sort by sector weight (market size) for better treemap layout
    // This ensures larger sectors get more space, not just volatile ones
    const sortedSectors = [...sectors].sort((a, b) => {
        const aWeight = calculateSectorWeight(a);
        const bWeight = calculateSectorWeight(b);
        return bWeight - aWeight;
    });
    
    // Simple treemap layout algorithm (squarified-like)
    const cells = calculateTreemapLayout(sortedSectors, width, height);
    
    // Set container height to accommodate all cells
    container.style.height = height + 'px';
    
    // Generate treemap cells
    let html = '';
    cells.forEach((cell, index) => {
        const change = cell.change || 0;
        const color = getTreemapColor(change);
        const changeSign = change > 0 ? '+' : '';
        
        // Determine size class for text visibility (mobile-responsive)
        const area = cell.w * cell.h;
        let sizeClass = '';
        if (area < 400) sizeClass = 'micro';       // Below ~20x20 - ultra small cells
        else if (area < 600) sizeClass = 'mini';   // Below ~25x25 - extra small cells
        else if (area < 2500) sizeClass = 'tiny';  // Below 50x50
        else if (area < 5000) sizeClass = 'small'; // Below ~70x70
        
        html += `
            <div class="treemap-cell ${sizeClass}" 
                 data-cell-index="${index}"
                 style="left: ${cell.x}px; top: ${cell.y}px; width: ${cell.w}px; height: ${cell.h}px; background: ${color};"
                 title="${cell.name}: ${changeSign}${change}%\n热度: ${cell.heat}\n个股数: ${cell.stocks}">
                <span class="cell-name">${cell.name}</span>
                <span class="cell-change">${changeSign}${change}%</span>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Store cells data on container for event delegation
    container._cellsData = cells;
}

// Handle click on treemap cell to enlarge if it's small
let enlargedCell = null;

/**
 * Initialize treemap event handlers using event delegation for better performance.
 * Should be called on DOMContentLoaded to set up click handlers for cell enlargement.
 * Uses event delegation to handle all cell clicks with a single listener on the container.
 */
function initTreemapEventHandlers() {
    const treemapContainer = document.getElementById('sectorTreemap');
    if (!treemapContainer) return;
    
    // Use event delegation for better performance
    treemapContainer.addEventListener('click', function(e) {
        // If clicking on a cell, handle enlarge/un-enlarge
        const cellElement = e.target.closest('.treemap-cell');
        if (cellElement) {
            const cellIndex = parseInt(cellElement.getAttribute('data-cell-index'));
            if (!isNaN(cellIndex) && treemapContainer._cellsData) {
                const cellData = treemapContainer._cellsData[cellIndex];
                if (cellData) {
                    handleTreemapCellClick(cellElement, cellData, e);
                }
            }
        } else if (e.target === treemapContainer && enlargedCell) {
            // If clicking on the container background, close any enlarged cell
            const prevData = enlargedCell.data;
            enlargedCell.element.classList.remove('enlarged');
            enlargedCell.element.style.position = 'absolute';
            enlargedCell.element.style.transform = '';
            enlargedCell.element.style.zIndex = '';
            enlargedCell.element.style.left = prevData.x + 'px';
            enlargedCell.element.style.top = prevData.y + 'px';
            enlargedCell = null;
        }
    });
}

/**
 * Handle click on treemap cell to enlarge or un-enlarge it.
 * Small cells (area < ENLARGE_THRESHOLD_AREA) can be enlarged for better text visibility.
 * 
 * @param {HTMLElement} cellElement - The DOM element of the clicked cell
 * @param {Object} cellData - The cell's data including position (x, y) and size (w, h)
 * @param {Event} event - The click event object
 */
function handleTreemapCellClick(cellElement, cellData, event) {
    const area = cellData.w * cellData.h;
    
    // Determine threshold based on mobile or desktop
    const isMobile = window.innerWidth < TREEMAP_CONFIG.MOBILE_WIDTH_THRESHOLD;
    const threshold = isMobile ? TREEMAP_CONFIG.ENLARGE_THRESHOLD_AREA_MOBILE : TREEMAP_CONFIG.ENLARGE_THRESHOLD_AREA;
    
    // Only enlarge small cells using configured threshold
    // Small cells have area LESS THAN threshold - fixed logic
    if (area >= threshold && !cellElement.classList.contains('enlarged')) {
        return; // Don't enlarge large cells - they're already readable
    }
    
    // If this cell is already enlarged, un-enlarge it
    if (cellElement.classList.contains('enlarged')) {
        cellElement.classList.remove('enlarged');
        cellElement.style.position = 'absolute';
        cellElement.style.transform = '';
        cellElement.style.zIndex = '';
        cellElement.style.left = cellData.x + 'px';
        cellElement.style.top = cellData.y + 'px';
        enlargedCell = null;
        return;
    }
    
    // Un-enlarge any previously enlarged cell
    if (enlargedCell) {
        const prevData = enlargedCell.data;
        enlargedCell.element.classList.remove('enlarged');
        enlargedCell.element.style.position = 'absolute';
        enlargedCell.element.style.transform = '';
        enlargedCell.element.style.zIndex = '';
        enlargedCell.element.style.left = prevData.x + 'px';
        enlargedCell.element.style.top = prevData.y + 'px';
    }
    
    // Enlarge this cell
    cellElement.classList.add('enlarged');
    
    // Calculate positioning: center the enlarged cell in the visible viewport
    // Get the center of the visible viewport area
    const viewportCenterX = window.innerWidth / 2;
    const viewportCenterY = window.innerHeight / 2;
    
    // Position using fixed positioning to break out of scroll context
    // The cell becomes fixed, so we use viewport coordinates directly
    cellElement.style.position = 'fixed';
    cellElement.style.left = viewportCenterX + 'px';
    cellElement.style.top = viewportCenterY + 'px';
    cellElement.style.transform = `translate(-50%, -50%) scale(${TREEMAP_CONFIG.ENLARGE_SCALE_FACTOR})`;
    cellElement.style.zIndex = '1000';
    
    enlargedCell = { element: cellElement, data: cellData };
    
    event.stopPropagation();
}

// Constants for treemap layout calculation
const TREEMAP_CONFIG = {
    DEFAULT_STOCKS_VALUE: 50,      // Default stocks count when not available
    DEFAULT_HEAT_VALUE: 50,        // Default heat value when not available
    NORMALIZATION_FACTOR: 10,      // Divider for stocks/heat normalization
    MIN_SECTOR_WEIGHT: 3,          // Minimum weight per sector (reduced to allow smaller cells)
    MIN_CELL_AREA_DESKTOP: 2500,   // Minimum cell area in px² for desktop (50x50px)
    MIN_CELL_AREA_MOBILE: 200,     // Minimum cell area in px² for mobile (reduced from 300 to ~14x14px)
    MIN_CELL_WIDTH_DESKTOP: 50,    // Minimum cell width in pixels for desktop
    MIN_CELL_WIDTH_MOBILE: 14,     // Minimum cell width in pixels for mobile (reduced from 17px)
    MIN_CELL_HEIGHT_DESKTOP: 40,   // Minimum cell height in pixels for desktop
    MIN_CELL_HEIGHT_MOBILE: 14,    // Minimum cell height in pixels for mobile (reduced from 17px)
    MOBILE_WIDTH_THRESHOLD: 768,   // Screen width threshold for mobile
    ENLARGE_THRESHOLD_AREA: 5000,  // Cell area threshold for enlarge feature (px²) - desktop
    ENLARGE_THRESHOLD_AREA_MOBILE: 3000, // Cell area threshold for enlarge on mobile (increased from 2000 so more cells are enlargeable)
    ENLARGE_SCALE_FACTOR: 2.5,     // Scale factor when enlarging small cells
    // Dynamic height calculation constants
    MIN_MOBILE_HEIGHT: 1200,       // Minimum treemap height on mobile (px)
    MAX_MOBILE_HEIGHT: 2400,       // Maximum treemap height on mobile (px)
    MOBILE_HEIGHT_PER_SECTOR: 70,  // Height allocation per sector on mobile (px)
    MIN_DESKTOP_HEIGHT: 500,       // Minimum treemap height on desktop (px)
    MAX_DESKTOP_HEIGHT: 800,       // Maximum treemap height on desktop (px)
    DESKTOP_HEIGHT_PER_SECTOR: 30  // Height allocation per sector on desktop (px)
};

// Helper function to calculate sector weight based on market metrics
function calculateSectorWeight(sector) {
    // Weight = normalized stocks count + normalized heat value
    // This matches real stock market behavior where area represents market importance
    const stockWeight = (sector.stocks || TREEMAP_CONFIG.DEFAULT_STOCKS_VALUE) / TREEMAP_CONFIG.NORMALIZATION_FACTOR;
    const heatWeight = (sector.heat || TREEMAP_CONFIG.DEFAULT_HEAT_VALUE) / TREEMAP_CONFIG.NORMALIZATION_FACTOR;
    const baseWeight = stockWeight + heatWeight;
    
    // Enforce minimum weight to ensure all sectors have reasonable display size
    return Math.max(baseWeight, TREEMAP_CONFIG.MIN_SECTOR_WEIGHT);
}

// Calculate treemap layout using squarified algorithm
function calculateTreemapLayout(sectors, width, height) {
    if (!sectors || sectors.length === 0) return [];
    
    // Determine if we're on mobile based on container width
    const isMobile = width < TREEMAP_CONFIG.MOBILE_WIDTH_THRESHOLD;
    const minCellArea = isMobile ? TREEMAP_CONFIG.MIN_CELL_AREA_MOBILE : TREEMAP_CONFIG.MIN_CELL_AREA_DESKTOP;
    const minCellWidth = isMobile ? TREEMAP_CONFIG.MIN_CELL_WIDTH_MOBILE : TREEMAP_CONFIG.MIN_CELL_WIDTH_DESKTOP;
    const minCellHeight = isMobile ? TREEMAP_CONFIG.MIN_CELL_HEIGHT_MOBILE : TREEMAP_CONFIG.MIN_CELL_HEIGHT_DESKTOP;
    
    // Calculate total weight across all sectors
    const totalWeight = sectors.reduce((sum, s) => sum + calculateSectorWeight(s), 0);
    
    // Normalize weights to total area with minimum size enforcement
    const totalArea = width * height;
    
    const sectorsWithArea = sectors.map(s => {
        const weight = calculateSectorWeight(s);
        const idealArea = (weight / totalWeight) * totalArea;
        
        return {
            ...s,
            weight: weight,
            // Enforce minimum area for readability (responsive based on device)
            area: Math.max(idealArea, minCellArea)
        };
    });
    
    // Calculate actual total area after enforcing minimums
    const actualTotalArea = sectorsWithArea.reduce((sum, s) => sum + s.area, 0);
    
    // If total area exceeds container, scale down areas proportionally while respecting minimums
    if (actualTotalArea > totalArea) {
        const scale = totalArea / actualTotalArea;
        sectorsWithArea.forEach(s => {
            // Scale down but don't go below minimum
            s.area = Math.max(s.area * scale, minCellArea * 0.8); // Allow 20% below minimum if necessary
        });
    }
    
    // Squarify layout with responsive minimum cell dimensions
    const cells = squarify(sectorsWithArea, 0, 0, width, height, minCellWidth, minCellHeight);
    
    // Ensure no cells extend beyond container bounds
    cells.forEach(cell => {
        if (cell.x + cell.w > width) {
            cell.w = Math.max(width - cell.x, minCellWidth);
        }
        if (cell.y + cell.h > height) {
            cell.h = Math.max(height - cell.y, minCellHeight);
        }
    });
    
    return cells;
}

// Squarified treemap algorithm for better aspect ratios
function squarify(items, x, y, width, height, minCellWidth, minCellHeight) {
    if (items.length === 0) return [];
    
    // Use provided parameters for responsive layout
    // Fallback to desktop defaults for backward compatibility (should not normally happen)
    const effectiveMinWidth = minCellWidth || TREEMAP_CONFIG.MIN_CELL_WIDTH_DESKTOP;
    const effectiveMinHeight = minCellHeight || TREEMAP_CONFIG.MIN_CELL_HEIGHT_DESKTOP;
    
    const cells = [];
    let remaining = [...items];
    let currentX = x;
    let currentY = y;
    let remainingWidth = width;
    let remainingHeight = height;
    
    while (remaining.length > 0) {
        // Determine layout direction
        const isHorizontal = remainingWidth >= remainingHeight;
        
        // Calculate how many items to put in the next row
        const totalRemainingArea = remaining.reduce((sum, item) => sum + item.area, 0);
        let row = [];
        let rowArea = 0;
        
        // Greedily add items to row while improving aspect ratio
        let previousAspectRatio = Infinity;
        for (let i = 0; i < remaining.length; i++) {
            const item = remaining[i];
            const testRowArea = rowArea + item.area;
            const testRow = [...row, item];
            
            // Calculate aspect ratio for this row
            const aspectRatio = calculateRowAspectRatio(
                testRow, 
                testRowArea, 
                isHorizontal ? remainingWidth : remainingHeight
            );
            
            // Add item only if it improves aspect ratio
            // Stop when aspect ratio starts getting worse
            if (row.length === 0) {
                // Always add first item
                row.push(item);
                rowArea = testRowArea;
                previousAspectRatio = aspectRatio;
            } else if (remaining.length === 1) {
                // Add last item to avoid orphan
                row.push(item);
                rowArea = testRowArea;
            } else if (aspectRatio <= previousAspectRatio) {
                // Add if aspect ratio improves or stays same
                row.push(item);
                rowArea = testRowArea;
                previousAspectRatio = aspectRatio;
            } else {
                // Aspect ratio got worse, stop adding to this row
                break;
            }
        }
        
        // If we couldn't add anything, force add at least one
        if (row.length === 0 && remaining.length > 0) {
            row = [remaining[0]];
            rowArea = remaining[0].area;
        }
        
        // Layout the row
        if (isHorizontal) {
            // Horizontal layout (row spans width, divided vertically)
            const rowHeight = rowArea / remainingWidth;
            let cellX = currentX;
            
            row.forEach(item => {
                const cellWidth = item.area / rowHeight;
                cells.push({
                    ...item,
                    x: Math.round(cellX),
                    y: Math.round(currentY),
                    w: Math.max(Math.round(cellWidth) - 2, effectiveMinWidth),
                    h: Math.max(Math.round(rowHeight) - 2, effectiveMinHeight)
                });
                cellX += cellWidth;
            });
            
            currentY += rowHeight;
            remainingHeight -= rowHeight;
        } else {
            // Vertical layout (row spans height, divided horizontally)
            const rowWidth = rowArea / remainingHeight;
            let cellY = currentY;
            
            row.forEach(item => {
                const cellHeight = item.area / rowWidth;
                cells.push({
                    ...item,
                    x: Math.round(currentX),
                    y: Math.round(cellY),
                    w: Math.max(Math.round(rowWidth) - 2, effectiveMinWidth),
                    h: Math.max(Math.round(cellHeight) - 2, effectiveMinHeight)
                });
                cellY += cellHeight;
            });
            
            currentX += rowWidth;
            remainingWidth -= rowWidth;
        }
        
        // Remove processed items
        remaining = remaining.slice(row.length);
    }
    
    return cells;
}

// Calculate aspect ratio for a row of items
function calculateRowAspectRatio(row, rowArea, rowLength) {
    if (row.length === 0 || rowArea === 0 || rowLength === 0) return Infinity;
    
    // Row perpendicular dimension (width for vertical rows, height for horizontal)
    const rowPerpendicularDim = rowArea / rowLength;
    
    // Calculate worst aspect ratio of cells in the row
    let worstRatio = 0;
    row.forEach(item => {
        // Cell dimension along the row direction
        const cellLength = item.area / rowPerpendicularDim;
        // Aspect ratio is max(width/height, height/width) to always be >= 1
        const ratio = Math.max(cellLength / rowPerpendicularDim, rowPerpendicularDim / cellLength);
        worstRatio = Math.max(worstRatio, ratio);
    });
    
    return worstRatio;
}

// Get color for treemap (red for up, green for down - Chinese stock market convention)
// Updated color scheme with 10 distinct levels for better mobile visibility
function getTreemapColor(change) {
    // Red = up (rise), Green = down (fall) - Chinese stock market convention
    // 10 distinct color levels corresponding to the requested ranges
    if (change >= 10) return '#8B0000';        // 黑红色 (Black-red) - >=10%
    if (change >= 8) return '#B22222';         // 深红色 (Dark red) - 8-10%
    if (change >= 5) return '#DC143C';         // 大红色 (Bright red) - 5-8%
    if (change >= 2) return '#FF6B6B';         // 浅红色 (Light red) - 2-5%
    if (change >= 1) return '#FFB3B3';         // 浅黄色调红 (Light yellowish red) - 1-2%
    if (change > -1) return '#FFFFCC';         // 浅黄色/白色 (Light yellow/white) - -1% to 1%
    if (change > -3) return '#C8E6C9';         // 浅绿色 (Light green) - -3% to -1%
    if (change > -5) return '#81C784';         // 绿色 (Green) - -5% to -3%
    if (change > -8) return '#43A047';         // 深绿色 (Dark green) - -8% to -5%
    return '#1B5E20';                           // 黑绿色 (Black-green) - <=-8%
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
    
    // Update stat cards (only 2 cards now: total predictions and accurate predictions)
    const statCards = statsContainer.querySelectorAll('.stat-card h3');
    if (statCards.length >= 2) {
        statCards[0].textContent = statistics.total || 0;
        statCards[1].textContent = statistics.accurate || 0;
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
    
    // Initialize treemap event handlers
    initTreemapEventHandlers();
    
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
