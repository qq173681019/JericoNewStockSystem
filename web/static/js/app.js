// App State Management
const appState = {
    currentView: 'home',
    watchlist: [],
    predictionHistory: [],
    isDarkTheme: true
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadInitialData();
    updateTime();
    setInterval(updateTime, 1000);
});

// Initialize Application
function initializeApp() {
    // Set initial theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    appState.isDarkTheme = savedTheme === 'dark';
    document.body.classList.toggle('dark-theme', appState.isDarkTheme);
    document.getElementById('theme-switch').checked = appState.isDarkTheme;
    
    // Load saved data from localStorage
    loadFromLocalStorage();
}

// Setup Event Listeners
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const view = e.currentTarget.getAttribute('data-view');
            navigateToView(view);
        });
    });
    
    // Theme toggle
    document.getElementById('theme-switch').addEventListener('change', toggleTheme);
    
    // Global search
    document.getElementById('global-search').addEventListener('input', handleGlobalSearch);
    
    // Stock code input - enter key
    const stockCodeInput = document.getElementById('stock-code');
    if (stockCodeInput) {
        stockCodeInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                runPrediction();
            }
        });
    }
}

// Navigation
function navigateToView(viewName) {
    // Update navigation active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-view') === viewName) {
            item.classList.add('active');
        }
    });
    
    // Update view display
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`${viewName}-view`).classList.add('active');
    
    appState.currentView = viewName;
    
    // Load view-specific data
    if (viewName === 'watchlist') {
        renderWatchlist();
    } else if (viewName === 'history') {
        renderHistory();
    }
}

// Theme Toggle
function toggleTheme() {
    appState.isDarkTheme = !appState.isDarkTheme;
    document.body.classList.toggle('dark-theme', appState.isDarkTheme);
    localStorage.setItem('theme', appState.isDarkTheme ? 'dark' : 'light');
}

// Update Current Time
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
    document.getElementById('current-time').textContent = timeString;
}

// Global Search
function handleGlobalSearch(e) {
    const query = e.target.value.toLowerCase();
    // Implement search logic here
    console.log('Searching for:', query);
}

// Stock Prediction
async function runPrediction() {
    const stockCode = document.getElementById('stock-code').value.trim();
    const predictionType = document.getElementById('prediction-type').value;
    
    if (!stockCode) {
        showNotification('请输入股票代码', 'warning');
        return;
    }
    
    // Validate stock code format (6 digits)
    if (!/^\d{6}$/.test(stockCode)) {
        showNotification('股票代码格式不正确，请输入6位数字', 'error');
        return;
    }
    
    const resultsSection = document.getElementById('prediction-results');
    resultsSection.innerHTML = '<div class="placeholder"><i class="fas fa-spinner fa-spin placeholder-icon"></i><p>正在分析中...</p></div>';
    
    // Simulate API call
    setTimeout(() => {
        const result = generateMockPrediction(stockCode, predictionType);
        displayPredictionResult(result);
        savePredictionToHistory(result);
    }, 1500);
}

// Generate Mock Prediction Data
function generateMockPrediction(stockCode, predictionType) {
    const directions = ['up', 'down', 'neutral'];
    const direction = directions[Math.floor(Math.random() * directions.length)];
    const confidence = (Math.random() * 0.3 + 0.65).toFixed(2); // 0.65-0.95
    const currentPrice = (Math.random() * 50 + 10).toFixed(2);
    const predictedPrice = direction === 'up' 
        ? (parseFloat(currentPrice) * (1 + Math.random() * 0.1)).toFixed(2)
        : direction === 'down'
        ? (parseFloat(currentPrice) * (1 - Math.random() * 0.1)).toFixed(2)
        : currentPrice;
    
    const stockNames = {
        '000001': '平安银行',
        '600000': '浦发银行',
        '000002': '万科A',
        '600036': '招商银行'
    };
    
    return {
        stockCode,
        stockName: stockNames[stockCode] || `股票${stockCode}`,
        predictionType: predictionType === 'short' ? '短期预测' : predictionType === 'medium' ? '中期预测' : '长期预测',
        direction,
        confidence: parseFloat(confidence),
        currentPrice: parseFloat(currentPrice),
        predictedPrice: parseFloat(predictedPrice),
        changePercent: ((predictedPrice - currentPrice) / currentPrice * 100).toFixed(2),
        timestamp: new Date().toISOString(),
        recommendation: direction === 'up' ? '建议买入' : direction === 'down' ? '建议卖出' : '建议持有'
    };
}

// Display Prediction Result
function displayPredictionResult(result) {
    const directionText = {
        'up': '上涨',
        'down': '下跌',
        'neutral': '震荡'
    };
    
    const directionIcon = {
        'up': 'fa-arrow-trend-up',
        'down': 'fa-arrow-trend-down',
        'neutral': 'fa-minus'
    };
    
    const html = `
        <div class="prediction-result">
            <div class="stock-info">
                <div class="stock-header">
                    <div>
                        <div class="stock-code">${result.stockCode}</div>
                        <div style="color: var(--text-secondary); margin-top: 0.25rem;">${result.stockName}</div>
                    </div>
                    <div class="prediction-badge ${result.direction}">
                        <i class="fas ${directionIcon[result.direction]}"></i>
                        ${directionText[result.direction]}
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-label">当前价格</div>
                        <div class="metric-value">¥${result.currentPrice}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">预测价格</div>
                        <div class="metric-value">¥${result.predictedPrice}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">预测涨跌</div>
                        <div class="metric-value" style="color: ${result.direction === 'up' ? 'var(--success-color)' : result.direction === 'down' ? 'var(--danger-color)' : 'var(--warning-color)'}">
                            ${result.changePercent > 0 ? '+' : ''}${result.changePercent}%
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="background-color: var(--bg-secondary); padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 1rem;">
                <h3 style="margin-bottom: 1rem; color: var(--text-primary);">预测详情</h3>
                <div style="display: grid; gap: 1rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: var(--text-secondary);">预测类型</span>
                        <span style="font-weight: 600; color: var(--text-primary);">${result.predictionType}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: var(--text-secondary);">置信度</span>
                        <span style="font-weight: 600; color: var(--text-primary);">${(result.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: var(--text-secondary);">建议操作</span>
                        <span style="font-weight: 600; color: var(--primary-color);">${result.recommendation}</span>
                    </div>
                </div>
            </div>
            
            <div style="background-color: var(--bg-secondary); padding: 1.5rem; border-radius: 0.75rem;">
                <h3 style="margin-bottom: 1rem; color: var(--text-primary);">技术分析</h3>
                <p style="color: var(--text-secondary); line-height: 1.8;">
                    基于历史数据和机器学习模型分析，该股票在${result.predictionType}内预计${directionText[result.direction]}。
                    当前技术指标显示${result.direction === 'up' ? '多头趋势' : result.direction === 'down' ? '空头趋势' : '震荡走势'}，
                    成交量${result.direction === 'up' ? '放大' : '正常'}，建议${result.recommendation.replace('建议', '')}。
                </p>
            </div>
        </div>
    `;
    
    document.getElementById('prediction-results').innerHTML = html;
    showNotification('预测完成', 'success');
}

// Save Prediction to History
function savePredictionToHistory(result) {
    appState.predictionHistory.unshift({
        ...result,
        id: Date.now(),
        timestamp: new Date().toISOString()
    });
    
    // Keep only last 100 predictions
    if (appState.predictionHistory.length > 100) {
        appState.predictionHistory = appState.predictionHistory.slice(0, 100);
    }
    
    saveToLocalStorage();
}

// Watchlist Management
function showAddStockModal() {
    document.getElementById('add-stock-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('add-stock-modal').classList.remove('active');
    // Clear form
    document.getElementById('modal-stock-code').value = '';
    document.getElementById('modal-stock-name').value = '';
    document.getElementById('modal-target-price').value = '';
    document.getElementById('modal-stop-loss').value = '';
}

function addToWatchlist() {
    const code = document.getElementById('modal-stock-code').value.trim();
    const name = document.getElementById('modal-stock-name').value.trim();
    const targetPrice = parseFloat(document.getElementById('modal-target-price').value);
    const stopLoss = parseFloat(document.getElementById('modal-stop-loss').value);
    
    if (!code || !name) {
        showNotification('请填写股票代码和名称', 'warning');
        return;
    }
    
    // Check if already exists
    if (appState.watchlist.some(item => item.code === code)) {
        showNotification('该股票已在观测池中', 'warning');
        return;
    }
    
    appState.watchlist.push({
        id: Date.now(),
        code,
        name,
        targetPrice: targetPrice || null,
        stopLoss: stopLoss || null,
        currentPrice: (Math.random() * 50 + 10).toFixed(2),
        addedAt: new Date().toISOString()
    });
    
    saveToLocalStorage();
    renderWatchlist();
    closeModal();
    showNotification('添加成功', 'success');
}

function removeFromWatchlist(id) {
    if (confirm('确定要从观测池中移除这只股票吗？')) {
        appState.watchlist = appState.watchlist.filter(item => item.id !== id);
        saveToLocalStorage();
        renderWatchlist();
        showNotification('已移除', 'success');
    }
}

function renderWatchlist() {
    const container = document.getElementById('watchlist-grid');
    
    if (appState.watchlist.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                <p>观测池为空，点击右上角按钮添加股票</p>
            </div>
        `;
        return;
    }
    
    const html = appState.watchlist.map(item => `
        <div class="watchlist-card">
            <div class="watchlist-header">
                <div class="stock-details">
                    <h3>${item.code}</h3>
                    <p>${item.name}</p>
                </div>
                <div class="watchlist-actions">
                    <button class="icon-button" onclick="removeFromWatchlist(${item.id})" title="移除">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            
            <div style="margin: 1rem 0;">
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">
                    ¥${item.currentPrice}
                </div>
            </div>
            
            ${item.targetPrice ? `
                <div class="price-info" style="margin-bottom: 0.5rem;">
                    <span class="price-label">目标价格</span>
                    <span class="price-value">¥${item.targetPrice}</span>
                </div>
            ` : ''}
            
            ${item.stopLoss ? `
                <div class="price-info">
                    <span class="price-label">止损价格</span>
                    <span class="price-value">¥${item.stopLoss}</span>
                </div>
            ` : ''}
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// History Management
function renderHistory() {
    const tbody = document.querySelector('#history-table tbody');
    
    if (appState.predictionHistory.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <i class="fas fa-inbox" style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.3; display: block;"></i>
                    暂无历史记录
                </td>
            </tr>
        `;
        return;
    }
    
    const directionText = {
        'up': '上涨',
        'down': '下跌',
        'neutral': '震荡'
    };
    
    const html = appState.predictionHistory.map(item => `
        <tr>
            <td>${new Date(item.timestamp).toLocaleString('zh-CN')}</td>
            <td><strong>${item.stockCode}</strong></td>
            <td>${item.stockName}</td>
            <td>${item.predictionType}</td>
            <td>
                <span class="status-badge ${item.direction === 'up' ? 'success' : item.direction === 'down' ? 'error' : 'warning'}">
                    ${directionText[item.direction]}
                </span>
            </td>
            <td>${(item.confidence * 100).toFixed(0)}%</td>
            <td>
                <button class="action-button btn-view" onclick="viewPredictionDetail(${item.id})">
                    查看
                </button>
            </td>
        </tr>
    `).join('');
    
    tbody.innerHTML = html;
}

function viewPredictionDetail(id) {
    const prediction = appState.predictionHistory.find(p => p.id === id);
    if (prediction) {
        // Navigate to prediction view and display the result
        navigateToView('prediction');
        document.getElementById('stock-code').value = prediction.stockCode;
        document.getElementById('prediction-type').value = 
            prediction.predictionType.includes('短期') ? 'short' : 
            prediction.predictionType.includes('中期') ? 'medium' : 'long';
        displayPredictionResult(prediction);
    }
}

// Local Storage
function saveToLocalStorage() {
    localStorage.setItem('appState', JSON.stringify({
        watchlist: appState.watchlist,
        predictionHistory: appState.predictionHistory
    }));
}

function loadFromLocalStorage() {
    try {
        const saved = localStorage.getItem('appState');
        if (saved) {
            const data = JSON.parse(saved);
            appState.watchlist = data.watchlist || [];
            appState.predictionHistory = data.predictionHistory || [];
        }
    } catch (e) {
        console.error('Failed to load from localStorage:', e);
    }
}

function loadInitialData() {
    // Load sample data if empty
    if (appState.watchlist.length === 0) {
        // Add some sample stocks for demo
        appState.watchlist = [
            {
                id: 1,
                code: '000001',
                name: '平安银行',
                targetPrice: 15.0,
                stopLoss: 12.0,
                currentPrice: '13.45',
                addedAt: new Date().toISOString()
            },
            {
                id: 2,
                code: '600000',
                name: '浦发银行',
                targetPrice: 10.0,
                stopLoss: 8.0,
                currentPrice: '9.23',
                addedAt: new Date().toISOString()
            }
        ];
        saveToLocalStorage();
    }
}

// Notification System
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: var(--bg-primary);
        color: var(--text-primary);
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        border-left: 4px solid ${
            type === 'success' ? 'var(--success-color)' : 
            type === 'warning' ? 'var(--warning-color)' : 
            type === 'error' ? 'var(--danger-color)' : 
            'var(--primary-color)'
        };
    `;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'warning' ? 'exclamation-triangle' : 
                 type === 'error' ? 'times-circle' : 
                 'info-circle';
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="fas fa-${icon}" style="color: ${
                type === 'success' ? 'var(--success-color)' : 
                type === 'warning' ? 'var(--warning-color)' : 
                type === 'error' ? 'var(--danger-color)' : 
                'var(--primary-color)'
            };"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add slide in/out animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Make functions globally accessible
window.navigateToView = navigateToView;
window.runPrediction = runPrediction;
window.showAddStockModal = showAddStockModal;
window.closeModal = closeModal;
window.addToWatchlist = addToWatchlist;
window.removeFromWatchlist = removeFromWatchlist;
window.viewPredictionDetail = viewPredictionDetail;
