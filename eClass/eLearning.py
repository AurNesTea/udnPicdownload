import pandas as pd

# 讀取資料
df = pd.read_csv('/Users/kevintsai/Library/CloudStorage/OneDrive-個人/Kevin/UDN/udnPro/小工具/udn_courses - 線上課程.csv')

# 定義新網址前綴
nDomain = 'http://learning.udn.com/health/courses/'

# 檢查欄位是否存在
if '課程連結' in df.columns:
    # 轉換連結
    nLink = []
    for link in df['課程連結']:
        try:
            temp_link = nDomain + link.split('course/')[1]
        except IndexError:
            temp_link = ''  # 若格式錯誤，填空
        nLink.append(temp_link)

    # 加入新欄位
    df['未來要請it轉址課程頁'] = nLink

    # 儲存新 CSV
    df.to_csv('new_udn_course.csv', index=False, encoding='utf-8-sig')
    print("已成功儲存為 new_udn_course.csv")

else:
    print("找不到「課程連結」欄位，請確認欄位名稱是否正確。")
