// search-all.js
(function () {
    // 確保 DOM 載入完成後再初始化
    function initSearchAll() {
        const input = document.getElementById("searchInput");
        const searchBtn = document.getElementById("searchBtn");
        const clearBtn = document.getElementById("clearSearchBtn");
        // const searchAllContainer = document.getElementById("searchAll");
        const searchAllGrid = document.getElementById("searchAllGrid");
        const searchAllEmpty = document.getElementById("searchAllEmpty");
        const searchAllCount = document.getElementById("searchAllCount");

        if (!input || !searchBtn || !searchAllGrid) {
            console.warn("[search-all.js] 缺少必要元素，請確認 index.html 是否已正確插入 #searchAll、#searchInput");
            return;
        }

        // 進入與離開搜尋模式（加入防呆）
        function enterSearchMode() {
            document.body.classList.add("search-mode");
            if (clearBtn) clearBtn.style.display = "inline-block";
        }

        function exitSearchMode() {
            document.body.classList.remove("search-mode");
            if (clearBtn) clearBtn.style.display = "none";
            if (input) input.value = "";
            if (searchAllGrid) searchAllGrid.innerHTML = "";
            if (searchAllCount) searchAllCount.textContent = "";
            if (searchAllEmpty) searchAllEmpty.style.display = "none";

            // ✅ 回復分頁內容（依你的 app.js 提供的函式）
            if (typeof window.resetAllTabs === "function") {
                window.resetAllTabs();
            }
        }

        // 搜尋主程式（關鍵：有關鍵字時先切換到搜尋模式）
        function runSearch() {
            const keyword = (input?.value || "").trim().toLowerCase();

            if (!keyword) {
                exitSearchMode();
                return;
            }

            // ✅ 先切換 UI 到搜尋模式，避免渲染完成但畫面仍停在分頁視圖
            enterSearchMode();

            // 檢查 imageData 是否存在
            // 優先使用 window.imageData（由 data.js 設定），如果不存在則嘗試全域 imageData
            const imageDataToUse = window.imageData || (typeof imageData !== "undefined" ? imageData : null);
            
            if (!imageDataToUse || typeof imageDataToUse !== "object" || Array.isArray(imageDataToUse)) {
                console.error("[search-all.js] 找不到全域 imageData，請確認 data.js 是否先載入。");
                if (searchAllEmpty) {
                    searchAllEmpty.style.display = "block";
                    searchAllEmpty.textContent = "搜尋結果有誤，請聯繫管理員";
                }
                if (searchAllCount) searchAllCount.textContent = "";
                return;
            }

            // 彙整所有圖片
            const allImages = [];
            for (let i = 1; i <= 5; i++) {
                const list = imageDataToUse[i] || [];
                for (const item of list) allImages.push(item);
            }

            // 過濾
            const results = allImages.filter((item) => {
                const text = `${item.title || ""} ${item.subtitle || ""} ${item.keywords || ""}`.toLowerCase();
                return text.includes(keyword);
            });

            // 渲染
            if (searchAllGrid) searchAllGrid.innerHTML = "";
            if (!results.length) {
                if (searchAllEmpty) searchAllEmpty.style.display = "block";
                if (searchAllCount) searchAllCount.textContent = "0 張";
                return;
            }

            if (searchAllEmpty) searchAllEmpty.style.display = "none";
            if (searchAllCount) searchAllCount.textContent = `${results.length} 張`;

            const frag = document.createDocumentFragment();
            for (const item of results) {
                const card = document.createElement("div");
                card.className = "image-card";
                card.innerHTML = `
      <img src="${item.url}" alt="${item.title || ""}" loading="lazy" decoding="async">
      <div class="image-card-body">
        <div class="image-card-title">${item.title || ""}</div>
        <div class="image-card-text">${item.subtitle || ""}</div>
        <div class="image-tags">
          ${(item.keywords || "")
                        .split("、").map(t => t.trim()).filter(Boolean)
                        .map(t => `<span class="tag">${t}</span>`).join("")}
        </div>
      </div>`;
                card.addEventListener("click", () => {
                    if (typeof window.openImageModal === "function") {
                        window.openImageModal(item);
                    }
                });
                frag.appendChild(card);
            }
            searchAllGrid.appendChild(frag);
        }

        // 綁定事件（加防呆，避免元素缺失時報錯）
        if (searchBtn) {
            searchBtn.addEventListener("click", (e) => { e.preventDefault(); runSearch(); });
        }
        if (input) {
            input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); runSearch(); } });
            input.addEventListener("input", () => { if (!input.value.trim()) exitSearchMode(); });
        }
        if (clearBtn) {
            clearBtn.addEventListener("click", () => exitSearchMode());
        }
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSearchAll);
    } 
    else {
        initSearchAll();
    }
})();
