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

        if (typeof window.data !== "object") {
            alert("找不到全域變數 data，請確認 data.js 是否已正確載入。");
            return;
        }

        let allImages = [];
        Object.keys(window.data).forEach((tab) => {
            const list = window.data[tab] || [];
            list.forEach((item) => allImages.push(item));
        });

        // 過濾符合關鍵字的項目
        const results = allImages.filter((item) => {
            const text = `
        ${item.title || ""}
        ${item.description || ""}
        ${(item.tags || []).join(" ")}
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
          <img src="${item.image}" alt="${item.title || ""}" loading="lazy" decoding="async">
          <div class="image-card-body">
            <div class="image-card-title">${item.title || ""}</div>
            <div class="image-card-text">${item.description || ""}</div>
            <div class="image-tags">
              ${(item.tags || [])
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
