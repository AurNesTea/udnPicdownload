import pandas as pd

def remove_duplicate_links(file_path, output_path):
    # 讀取 CSV 檔案
    df = pd.read_csv(file_path)
    
    # 確保欄位名稱正確
    required_columns = {'tags', 'Title', '內文', '來源', '作者', 'Link'}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV 文件缺少必要的欄位")
    
    # 根據 Link 欄位去重複，只保留第一筆出現的數據
    df_cleaned = df.drop_duplicates(subset=['Link'], keep='first')
    
    # 將處理後的數據保存為新的 CSV 檔案
    df_cleaned.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"已成功去除重複的 Link，結果已保存至 {output_path}")

# 使用範例
input_file = "/Users/kevintsai/Library/CloudStorage/OneDrive-個人/Kevin/UDN/udnPro/dataClean/articles_with_tags.csv"  # 替換為實際的 CSV 路徑
output_file = "/Users/kevintsai/Library/CloudStorage/OneDrive-個人/Kevin/UDN/udnPro/dataClean/articles_cleaned.csv"   # 替換為實際的儲存路徑
remove_duplicate_links(input_file, output_file)
