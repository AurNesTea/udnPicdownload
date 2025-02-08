import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繁體中文字體（請確認你已安裝 Noto Sans TC）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
# plt.rcParams['font.sans-serif'] = ['Noto Sans TC']
plt.rcParams['axes.unicode_minus'] = False

# 讀取 CSV
df_prevalence = pd.read_csv("dementia_data.csv")
df_severity = pd.read_csv("dementia_severity.csv")
df_bspd = pd.read_csv("dementia_bspd.csv")
df_future = pd.read_csv("dementia_future.csv")


# 設定繪圖風格
sns.set_style("whitegrid")

# 1️.失智症盛行率 - 折線圖
plt.figure(figsize=(8, 5))
sns.lineplot(x=df_prevalence["年齡區間"], y=df_prevalence["失智症盛行率(%)"], marker="o", color="b")
plt.title("不同年齡層的失智症盛行率")
plt.xlabel("年齡區間")
plt.ylabel("盛行率 (%)")
plt.show()

# 2️.失智症嚴重程度 - 圓餅圖
plt.figure(figsize=(6, 6))
plt.pie(df_severity["占比(%)"], labels=df_severity["失智程度"], autopct='%1.1f%%', colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
plt.title("失智症嚴重程度分佈")
plt.show()

# 3️.BPSD 主要症狀 - 長條圖
plt.figure(figsize=(8, 5))
sns.barplot(y=df_bspd["BPSD 症狀"], x=df_bspd["發生率(%)"], palette="coolwarm")
plt.title("失智症常見行為與情緒症狀（BPSD）")
plt.xlabel("發生率 (%)")
plt.ylabel("症狀類別")
plt.show()

# 4️.未來失智人口趨勢 - 折線圖
plt.figure(figsize=(8, 5))
sns.lineplot(x=df_future["年度"], y=df_future["65歲以上失智人口(萬)"], marker="o", label="65歲以上失智人口")
sns.lineplot(x=df_future["年度"], y=df_future["總失智人口(萬)"], marker="s", label="總失智人口")
plt.title("未來失智人口推估 (2024-2041)")
plt.xlabel("年度")
plt.ylabel("人口數 (萬)")
plt.legend()
plt.show()
