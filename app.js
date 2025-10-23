// 當前顯示的圖片數量
const currentDisplayCount = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
const itemsPerLoad = 20;

// 初始化頁面
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
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
    
    card.innerHTML = `
        <img src="${image.url}" alt="${image.title}" loading="lazy">
    `;
    
    card.addEventListener('click', () => openImageModal(image));
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
    const tags = image.keywords.split('、').map(tag => tag.trim());
    tagsContainer.innerHTML = tags.map(tag => `<span class="tag">#${tag}</span>`).join('');
    
    const applicationForm = document.getElementById('applicationForm');
    const downloadForm = document.getElementById('downloadForm');
    
    if (image.restriction === '需要申請' || image.restriction === '須申請使用') {
        // 檢查是否已經申請過
        const hasApplied = checkApplicationStatus(image.id);
        
        if (hasApplied) {
            // 已申請，顯示下載按鈕
            applicationForm.style.display = 'none';
            downloadForm.style.display = 'block';
            document.getElementById('downloadBtn').innerHTML = '<i class="bi bi-download me-2"></i>下載圖片';
        } else {
            // 未申請，顯示申請按鈕
            applicationForm.style.display = 'block';
            document.getElementById('applyBtn').setAttribute('data-image-id', image.id);
            downloadForm.style.display = 'none';
        }
    } else {
        applicationForm.style.display = 'none';
        downloadForm.style.display = 'block';
        document.getElementById('downloadBtn').innerHTML = '<i class="bi bi-download me-2"></i>下載圖片';
    }
    
    document.getElementById('downloadBtn').setAttribute('data-image-id', image.id);
    
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    modal.show();
}

// 監聽圖片 Modal 關閉事件
document.getElementById('imageModal').addEventListener('hidden.bs.modal', function() {
    // 確保移除所有 modal-backdrop
    removeAllModalBackdrops();
});

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
        const searchText = `${image.title} ${image.subtitle} ${image.keywords}`.toLowerCase();
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
        document.getElementById(`loadMore${tabNumber}`).style.display = 'block';
    }
    
    const activeTab = document.querySelector('.nav-link.active');
    const activeTabNumber = activeTab.getAttribute('data-bs-target').replace('#tab', '');
    loadImagesForTab(activeTabNumber);
}

// 設定載入更多按鈕
function setupLoadMoreButtons() {
    for (let i = 1; i <= 5; i++) {
        const button = document.getElementById(`loadMore${i}`);
        button.addEventListener('click', () => {
            loadImagesForTab(i);
        });
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
document.getElementById('downloadBtn').addEventListener('click', async function() {
    const imageId = this.getAttribute('data-image-id');
    const imageUrl = document.getElementById('modalImage').src;
    
    console.log('開始下載圖片:', imageId, imageUrl);
    
    try {
        // 嘗試使用 fetch 下載
        const response = await fetch(imageUrl, { 
            mode: 'cors', 
            cache: 'no-cache',
            headers: {
                'Accept': 'image/*'
            }
        });
        
        console.log('Fetch 回應狀態:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const blob = await response.blob();
        console.log('Blob 大小:', blob.size, '類型:', blob.type);
        
        const objectUrl = URL.createObjectURL(blob);
        
        // 從 URL 或 Content-Type 判斷副檔名
        let extension = 'jpg';
        if (blob.type) {
            const mimeType = blob.type.split('/')[1];
            if (mimeType) extension = mimeType;
        } else {
            // 從 URL 判斷副檔名
            const urlExtension = imageUrl.split('.').pop().toLowerCase();
            if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(urlExtension)) {
                extension = urlExtension;
            }
        }
        
        console.log('使用副檔名:', extension);
        
        // 建立下載連結
        const link = document.createElement('a');
        link.href = objectUrl;
        link.download = `medical_image_${imageId}.${extension}`;
        link.style.display = 'none';
        
        // 觸發下載
        document.body.appendChild(link);
        link.click();
        
        // 清理
        setTimeout(() => {
            document.body.removeChild(link);
            URL.revokeObjectURL(objectUrl);
        }, 100);
        
        showToast('圖片下載成功！', 'success');
        
    } catch (error) {
        console.error('下載失敗:', error);
        
        // 後備方案：使用代理下載
        try {
            // 嘗試使用代理服務下載
            const proxyUrl = `https://cors-anywhere.herokuapp.com/${imageUrl}`;
            const response = await fetch(proxyUrl, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const objectUrl = URL.createObjectURL(blob);
                
                const link = document.createElement('a');
                link.href = objectUrl;
                link.download = `medical_image_${imageId}.jpg`;
                link.style.display = 'none';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(objectUrl);
                
                showToast('圖片下載成功！', 'success');
                return;
            }
        } catch (proxyError) {
            console.error('代理下載失敗:', proxyError);
        }
        
        // 最後的後備方案：在新分頁開啟
        window.open(imageUrl, '_blank');
        showToast('瀏覽器限制直接下載，已在新分頁開啟圖片。請右鍵另存新檔。', 'info');
    }
});

// 檢查申請狀態
function checkApplicationStatus(imageId) {
    const appliedImages = JSON.parse(localStorage.getItem('appliedImages') || '[]');
    return appliedImages.includes(imageId);
}

// 標記圖片為已申請
function markImageAsApplied(imageId) {
    const appliedImages = JSON.parse(localStorage.getItem('appliedImages') || '[]');
    if (!appliedImages.includes(imageId)) {
        appliedImages.push(imageId);
        localStorage.setItem('appliedImages', JSON.stringify(appliedImages));
    }
}

// 申請表單
document.getElementById('applyBtn').addEventListener('click', function() {
    const imageId = this.getAttribute('data-image-id');
    
    // 開啟 Google 問卷 Modal
    const formModal = new bootstrap.Modal(document.getElementById('formModal'));
    formModal.show();
    
    // 記錄申請的圖片 ID
    sessionStorage.setItem('pendingApplication', imageId);
    
    showToast(`已開啟申請表單，請填寫完整資訊`, 'info');
});

// 監聽表單 Modal 關閉事件
document.getElementById('formModal').addEventListener('hidden.bs.modal', function() {
    const pendingImageId = sessionStorage.getItem('pendingApplication');
    if (pendingImageId) {
        // 模擬表單填寫完成（實際應用中需要更複雜的驗證邏輯）
        markImageAsApplied(pendingImageId);
        sessionStorage.removeItem('pendingApplication');
        
        showToast('申請表單已提交，現在可以下載圖片了！', 'success');
        
        // 確保移除所有 modal-backdrop
        removeAllModalBackdrops();
        
        // 重新開啟圖片 Modal 以更新按鈕狀態
        setTimeout(() => {
            const currentImage = getCurrentImageById(pendingImageId);
            if (currentImage) {
                openImageModal(currentImage);
            }
        }, 1000);
    } else {
        // 即使沒有待處理的申請，也要確保移除背景層
        removeAllModalBackdrops();
    }
});

// 移除所有 Modal 背景層的函數
function removeAllModalBackdrops() {
    const backdrops = document.getElementsByClassName('modal-backdrop');
    while (backdrops.length > 0) {
        backdrops[0].parentNode.removeChild(backdrops[0]);
    }
    // 移除 body 上的 modal-open class
    document.body.classList.remove('modal-open');
    // 重置 body 的 overflow 樣式
    document.body.style.overflow = '';
}

// 根據 ID 取得圖片資料
function getCurrentImageById(imageId) {
    for (let tabNumber = 1; tabNumber <= 5; tabNumber++) {
        const images = imageData[tabNumber] || [];
        const image = images.find(img => img.id === imageId);
        if (image) return image;
    }
    return null;
}

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
