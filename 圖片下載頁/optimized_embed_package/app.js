// 當前顯示的圖片數量
const currentDisplayCount = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
const itemsPerLoad = 20;


// 搜尋與查找索引
const imageById = {};
function buildSearchIndex() {
    for (let t = 1; t <= 5; t++) {
        const arr = imageData[t] || [];
        for (const img of arr) {
            // 建立查找索引
            if (img && img.id) imageById[img.id] = img;
            // 預先組合搜尋字串
            const title = (img.title || "");
            const sub = (img.subtitle || "");
            const kw = (img.keywords || "");
            img._search = `${title} ${sub} ${kw}`.toLowerCase();
        }

// 建立單次事件委派（每個 grid 綁一次）
const _delegatedGrids = new Set();
function setupGridDelegation(tabNumber){
    const grid = document.getElementById(`grid${tabNumber}`);
    if (!grid || _delegatedGrids.has(grid)) return;
    grid.addEventListener('click', (e)=>{
        const card = e.target.closest('.image-card');
        if (!card) return;
        const id = card.getAttribute('data-image-id');
        const img = imageById[id];
        if (img) openImageModal(img);
    });
    _delegatedGrids.add(grid);
}
    }
}
// 初始化頁面
document.addEventListener('DOMContentLoaded', function() {
    buildSearchIndex();
    initializeTabs();
    for (let t=1;t<=5;t++){ setupGridDelegation(t);}
    setupSearch();
    setupLoadMoreButtons();
    loadInitialImages();
});

// 初始化頁籤
function initializeTabs() {
    const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', function(event) {
            const targetTab = event.target.getAttribute('data-bs-target').replace('#', '');
            const tabNumber = targetTab.replace('tab', '');
            
            if (currentDisplayCount[tabNumber] === 0) {
                loadImagesForTab(tabNumber);
            }
        });
    });
}

// 載入初始圖片
function loadInitialImages() {
    loadImagesForTab(1);
}

// 為指定頁籤載入圖片
function loadImagesForTab(tabNumber) {
    const grid = document.getElementById(`grid${tabNumber}`);
    const images = imageData[tabNumber] || [];
    const startIndex = currentDisplayCount[tabNumber];
    const endIndex = Math.min(startIndex + itemsPerLoad, images.length);
    
    showLoading(tabNumber);
    
    setTimeout(() => {
        for (let i = startIndex; i < endIndex; i++) {
            const image = images[i];
            const imageCard = createImageCard(image);
            grid.appendChild(imageCard);
        }
        
        currentDisplayCount[tabNumber] = endIndex;
        hideLoading(tabNumber);
        updateLoadMoreButton(tabNumber);
    }, 500);
}

// 創建圖片卡片
function createImageCard(image) {
    const card = document.createElement('div');
    card.className = 'image-card';
    card.setAttribute('data-image-id', image.id);
    
    const rawKw = (image.keywords || "");
    const tags = rawKw.split('、').map(tag => tag.trim()).filter(Boolean);
    
    card.innerHTML = `
        <img src="${image.url}" alt="${image.title}" loading="lazy" onerror="this.onerror=null;this.src='data:image/gif;base64,R0lGODlhAQABAAAAACw=';">
        <div class="image-card-body">
            <h6 class="image-card-title">${image.title}</h6>
            <p class="image-card-text">${image.subtitle}</p>
            <div class="image-tags">
                ${tags.map(tag => `<span class="tag">#${tag}</span>`).join('')}
            </div>
        </div>
    `;
    
    return card;
}

// 開啟圖片Modal
function openImageModal(image) {
    document.getElementById('modalImage').src = image.url;
    document.getElementById('modalImage').alt = image.title;
    document.getElementById('imageModalLabel').textContent = image.title;
    document.getElementById('modalTitle').textContent = image.title;
    document.getElementById('modalDescription').textContent = image.subtitle;
    
    const tagsContainer = document.getElementById('modalTags');
    const rawKw = (image.keywords || "");
    const tags = rawKw.split('、').map(tag => tag.trim()).filter(Boolean);
    tagsContainer.innerHTML = tags.map(tag => `<span class="tag">#${tag}</span>`).join('');
    
    const applicationForm = document.getElementById('applicationForm');
    if (image.restriction === '需要申請') {
        applicationForm.style.display = 'block';
        document.getElementById('applyBtn').setAttribute('data-image-id', image.id);
    } else {
        applicationForm.style.display = 'none';
    }
    
    document.getElementById('downloadBtn').setAttribute('data-image-id', image.id);
    
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    modal.show();
}

// 設定搜尋功能
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    
    function performSearch() {
        const query = searchInput.value.trim().toLowerCase();
        if (query === '') {
            resetAllTabs();
            return;
        }
        
        for (let tabNumber = 1; tabNumber <= 5; tabNumber++) {
            searchInTab(tabNumber, query);
        }
    }
    
    searchBtn.addEventListener('click', performSearch);
    let _timer; 
    searchInput.addEventListener('input', function(){
        clearTimeout(_timer);
        _timer = setTimeout(performSearch, 300);
    });
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

// 在指定頁籤中搜尋
function searchInTab(tabNumber, query) {
    const grid = document.getElementById(`grid${tabNumber}`);
    const images = imageData[tabNumber] || [];
    
    grid.innerHTML = '';
    
    const filteredImages = images.filter(image => {
        const searchText = image._search || `${(image.title||"")} ${(image.subtitle||"")} ${(image.keywords||"")}`.toLowerCase();
        return searchText.includes(query);
    });
    
    filteredImages.forEach(image => {
        const imageCard = createImageCard(image);
        grid.appendChild(imageCard);
    });
    
    document.getElementById(`loadMore${tabNumber}`).style.display = 'none';
}

// 重置所有頁籤
function resetAllTabs() {
    for (let tabNumber = 1; tabNumber <= 5; tabNumber++) {
        const grid = document.getElementById(`grid${tabNumber}`);
        grid.innerHTML = '';
        currentDisplayCount[tabNumber] = 0;
        const btn = document.getElementById(`loadMore${tabNumber}`);
        if (btn) btn.style.display = 'block';
    }
    
    const activeTab = document.querySelector('.nav-link.active');
    const activeTabNumber = activeTab ? activeTab.getAttribute('data-bs-target').replace('#tab', '') : '1';
    loadImagesForTab(activeTabNumber);
}

// 設定載入更多按鈕
function setupLoadMoreButtons() {
    for (let i = 1; i <= 5; i++) {
        const button = document.getElementById(`loadMore${i}`);
        if (!button) continue;
        button.addEventListener('click', () => { loadImagesForTab(i); });
    }
}

// 更新載入更多按鈕狀態
function updateLoadMoreButton(tabNumber) {
    const button = document.getElementById(`loadMore${tabNumber}`);
    const images = imageData[tabNumber] || [];
    
    if (currentDisplayCount[tabNumber] < images.length) {
        button.style.display = 'block';
        const remaining = images.length - currentDisplayCount[tabNumber];
        button.innerHTML = `<i class="bi bi-plus-circle me-2"></i>載入更多圖片 (還有 ${remaining} 張)`;
    } else {
        button.style.display = 'none';
    }
}

// 顯示載入動畫
function showLoading(tabNumber) {
    document.getElementById(`loading${tabNumber}`).style.display = 'block';
}

// 隱藏載入動畫
function hideLoading(tabNumber) {
    document.getElementById(`loading${tabNumber}`).style.display = 'none';
}

// 下載圖片
document.getElementById('downloadBtn').addEventListener('click', function() {
    const imageId = this.getAttribute('data-image-id');
    const imgEl = document.getElementById('modalImage');
    const href = imgEl.src;
    try {
        const a = document.createElement('a');
        a.href = href;
        a.download = `medical_image_${imageId}.jpg`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast('圖片下載成功！', 'success');
    } catch (e) {
        // 跨網域下載可能被瀏覽器阻擋：改為另開分頁，讓使用者另存
        window.open(href, '_blank');
        showToast('已開新分頁，請另存圖片。', 'info');
    }
});

// 申請表單
document.getElementById('applyBtn').addEventListener('click', function() {
    const imageId = this.getAttribute('data-image-id');
    showToast(`已記錄圖片編號 ${imageId}，請聯繫管理員填寫申請表單`, 'info');
});

// 顯示提示訊息
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'info'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
