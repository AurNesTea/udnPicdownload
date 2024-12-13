import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm

# 設置支持中文的字體
plt.rcParams['font.sans-serif'] = ['STHeiti']  # Mac 系統的字體
plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號顯示問題

# 創建繪圖空間和子圖
fig, ax = plt.subplots(figsize = (6, 6))

# 繪製軸線
ax.axvline(x=0, color='black', linewidth=0.5)
ax.axhline(y=0, color='black', linewidth=0.5)

# 4個象限區塊
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


# 載入資料
file_path = '/Users/kevintsai/Library/CloudStorage/OneDrive-個人/Kevin/UDN/Podcast/程式碼/soundon/datas/analytics-episode-list-下載數.csv'
data = pd.read_csv(file_path, encoding='utf-8')
x = data['發佈30天']
y = data['總下載']

# 計算 x 和 y 的平均值
x_mean = x.mean()
y_mean = y.mean()

# 繪製散佈圖
ax.scatter(x, y, s=20, color='blue')

# 繪製 x 和 y 的平均線
ax.axvline(x=x_mean, color='orange', linestyle='--', linewidth=1, label=f'平均 發佈7天: {x_mean:.2f}')
ax.axhline(y=y_mean, color='green', linestyle='--', linewidth=1, label=f'平均 總下載: {y_mean:.2f}')

# 添加每個點的標籤

for i, title in enumerate(data['標題']):
    title = title.split('.')[0]
    ax.text(x[i], y[i], title, ha='right', fontsize=8)  # 標籤位置微調

# 設置座標軸範圍
ax.set_xlim(0, max(x) + 500)
ax.set_ylim(0, max(y) + 500)

# 添加標題和標籤
ax.set_title('Podcast Downloads by Episode')
ax.set_xlabel('發佈30天')
ax.set_ylabel('總下載')

plt.show()