// search-all.js
(function () {
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

    // 進入與離開搜尋模式
    function enterSearchMode() {
        document.body.classList.add("search-mode");
        clearBtn.style.display = "inline-block";
    }
    function exitSearchMode() {
        document.body.classList.remove("search-mode");
        clearBtn.style.display = "none";
        input.value = "";
        searchAllGrid.innerHTML = "";
        searchAllCount.textContent = "";
        searchAllEmpty.style.display = "none";
    }

    // 搜尋主程式
    function runSearch() {
        const keyword = input.value.trim().toLowerCase();
        if (!keyword) {
            exitSearchMode();
            return;
        }

        if (typeof window.imageData !== "object") {
            // 改為非阻塞的錯誤處理：
            // 1) 記錄到 console
            // 2) 發送日誌到後端 API 寫入 logs/front_logs
            // 3) 在畫面顯示友善的錯誤訊息給使用者
            const friendlyMsg = "搜尋結果有誤，請聯繫管理員";
            console.error("[search-all.js] 找不到全域變數 imageData，請確認 data.js 是否已正確載入。");

            // 發送錯誤日誌到後端
            const logEntry = {
                ts: new Date().toISOString(),
                level: "error",
                file: "search-all.js",
                message: "找不到全域變數 imageData",
                userAgent: navigator.userAgent || "",
                url: window.location.href || ""
            };

            // 嘗試發送到後端 API 寫入 logs/front_logs（如果有的話）
            // 如果沒有後端，這個請求會失敗但不影響功能
            fetch("/api/log-front-error", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(logEntry),
            }).catch((err) => {
                // 靜默失敗，不影響使用者體驗
                // 這在純靜態網站（如 GitHub Pages）中是正常的
                console.warn("[search-all.js] 無法發送日誌到伺服器（正常，如果沒有後端 API）");
            });

            if (searchAllEmpty) {
                searchAllEmpty.style.display = "block";
                searchAllEmpty.textContent = friendlyMsg;
            }
            if (searchAllCount) searchAllCount.textContent = "";

            return;
        }

        let allImages = [];
        Object.keys(window.imageData).forEach((tab) => {
            const list = window.imageData[tab] || [];
            list.forEach((item) => allImages.push(item));
        });

        // 過濾符合關鍵字的項目
        const results = allImages.filter((item) => {
            const text = `
        ${item.title || ""}
        ${item.subtitle || ""}
        ${item.keywords || ""}
      `.toLowerCase();
            return text.includes(keyword);
        });

        // 更新畫面
        searchAllGrid.innerHTML = "";
        if (results.length === 0) {
            searchAllEmpty.style.display = "block";
            searchAllCount.textContent = "0 張";
        } else {
            searchAllEmpty.style.display = "none";
            searchAllCount.textContent = `${results.length} 張`;
            const frag = document.createDocumentFragment();

            results.forEach((item) => {
                const card = document.createElement("div");
                card.className = "image-card";
                card.innerHTML = `
          <img src="${item.url}" alt="${item.title || ""}" loading="lazy" decoding="async">
          <div class="image-card-body">
            <div class="image-card-title">${item.title || ""}</div>
            <div class="image-card-text">${item.subtitle || ""}</div>
            <div class="image-tags">
              ${(item.keywords || "")
                        .split("、")
                        .map((t) => t.trim())
                        .filter(Boolean)
                        .map((t) => `<span class="tag">${t}</span>`)
                        .join("")}
            </div>
          </div>
        `;

                // 點擊卡片 → 呼叫原本 app.js 的 Modal 顯示
                card.addEventListener("click", () => {
                    openImageModal(item);
                });

                frag.appendChild(card);
            });

            searchAllGrid.appendChild(frag);
        }

        enterSearchMode();
    }

    // 綁定事件
    searchBtn.addEventListener("click", runSearch);
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") runSearch();
    });
    clearBtn.addEventListener("click", exitSearchMode);
    input.addEventListener("input", () => {
        if (!input.value.trim()) exitSearchMode();
    });
})();
