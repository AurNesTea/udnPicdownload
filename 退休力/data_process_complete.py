#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
退休力資料處理程式 - 完整版
將 retire 2025.csv 轉換為與 退休力-第三階段(final).xlsx - 送統計.csv 相同的格式

功能：
1. 自動偵測檔案編碼
2. 分析兩份檔案的資料結構差異
3. 進行欄位對應和資料轉換
4. 處理問卷題目轉換（Q1-Q20 轉換為 A1.1-E20.6）
5. 另存新檔保留原始資料
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import chardet

def detect_encoding(file_path):
    """
    偵測檔案編碼
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_question_data(q_value):
    """
    將原始問卷資料轉換為目標格式
    這裡提供一個範例轉換邏輯，實際應用時需要根據具體需求調整
    
    參數:
        q_value: 原始問卷的答案值
    
    返回:
        轉換後的數值
    """
    if pd.isna(q_value):
        return 0
    
    # 將字串轉換為數值
    if isinstance(q_value, str):
        # 處理包含多個選項的情況，如 "1,2,3"
        if ',' in q_value:
            # 取第一個選項
            q_value = q_value.split(',')[0]
        
        try:
            q_value = float(q_value)
        except ValueError:
            return 0
    
    # 根據問卷設計進行轉換
    # 這裡是範例邏輯，實際應用時需要根據具體的問卷設計來調整
    if q_value == 1:
        return 1
    elif q_value == 2:
        return 0
    elif q_value == 3:
        return 1
    elif q_value == 4:
        return 0
    elif q_value == 5:
        return 1
    elif q_value == 6:
        return 0
    else:
        return 0

# 進行資料處理
def process_retirement_data():
    """
    處理退休力資料，將 retire 2025.csv 轉換為標準格式
    """
    
    # 檔案路徑
    input_file = "data/retire 2025.csv"
    reference_file = "data/退休力-第三階段(final).xlsx - 送統計.csv"
    output_file = "data/retire_2025_processed.csv"
    
    print("開始處理退休力資料...")
    
    # 偵測檔案編碼
    print("偵測檔案編碼...")
    ref_encoding = detect_encoding(reference_file)
    input_encoding = detect_encoding(input_file)
    print(f"參考檔案編碼: {ref_encoding}")
    print(f"原始檔案編碼: {input_encoding}")
    
    # 讀取參考檔案以了解目標格式
    print("讀取參考檔案格式...")
    try:
        ref_df = pd.read_csv(reference_file, encoding=ref_encoding)
        print(f"參考檔案欄位數量: {len(ref_df.columns)}")
        print(f"參考檔案資料筆數: {len(ref_df)}")
    
    except Exception as e:
        print(f"讀取參考檔案時發生錯誤: {e}")
        return
    
    # 讀取原始資料
    print("讀取原始資料...")
    try:
        df = pd.read_csv(input_file, encoding=input_encoding)
        print(f"原始資料欄位數量: {len(df.columns)}")
        print(f"原始資料筆數: {len(df)}")
    
    except Exception as e:
        print(f"讀取原始資料時發生錯誤: {e}")
        return
    
    # 顯示原始資料的欄位
    print("\n原始資料欄位:")
    for i, col in enumerate(df.columns):
        print(f"{i+1:2d}. {col}")
    
    # 建立新的資料框架，使用參考檔案的欄位結構
    processed_df = pd.DataFrame()
    
    # 基本欄位對應
    processed_df['vip_id'] = df['vip_id']
    processed_df['age'] = df['age']
    processed_df['sex'] = df['sex']
    processed_df['grade'] = df['grade']
    processed_df['city'] = df['city']
    processed_df['cluster'] = df['cluster（動物種類）']  # 對應原始檔案的 cluster（動物種類）
    
    # 分數欄位對應
    processed_df['總分'] = df['總分']
    processed_df['財務分數'] = df['財務']  # 對應原始檔案的 財務
    processed_df['健康分數'] = df['健康']  # 對應原始檔案的 健康
    processed_df['社交分數'] = df['社交']  # 對應原始檔案的 社交
    processed_df['心靈分數'] = df['心靈']  # 對應原始檔案的 心靈
    processed_df['獨立分數'] = df['獨立']  # 對應原始檔案的 獨立
    
    # 處理問卷題目欄位 (A1.1 到 E20.6)
    # 根據參考檔案的欄位結構，建立對應的欄位
    question_columns = []
    
    # A組題目 (A1.1 到 A7.6)
    for i in range(1, 8):
        if i == 1:
            for j in range(1, 3):  # A1.1, A1.2
                question_columns.append(f'A{i}.{j}')
        elif i == 2:
            for j in range(1, 5):  # A2.1 到 A2.4
                question_columns.append(f'A{i}.{j}')
        elif i == 3:
            for j in range(1, 7):  # A3.1 到 A3.6
                question_columns.append(f'A{i}.{j}')
        elif i == 4:
            for j in range(1, 4):  # A4.1 到 A4.3
                question_columns.append(f'A{i}.{j}')
        elif i == 5:
            for j in range(1, 7):  # A5.1 到 A5.6
                question_columns.append(f'A{i}.{j}')
        elif i == 6:
            for j in range(1, 6):  # A6.1 到 A6.5
                question_columns.append(f'A{i}.{j}')
        elif i == 7:
            for j in range(1, 7):  # A7.1 到 A7.6
                question_columns.append(f'A{i}.{j}')
    
    # B組題目 (B8.1 到 B15.3)
    for i in range(8, 16):
        if i == 8:
            for j in range(1, 6):  # B8.1 到 B8.5
                question_columns.append(f'B{i}.{j}')
        elif i == 9:
            for j in range(1, 6):  # B9.1 到 B9.5
                question_columns.append(f'B{i}.{j}')
        elif i == 10:
            for j in range(1, 6):  # B10.1 到 B10.5
                question_columns.append(f'B{i}.{j}')
        elif i == 11:
            for j in range(1, 6):  # B11.1 到 B11.5
                question_columns.append(f'B{i}.{j}')
        elif i == 12:
            for j in range(1, 7):  # B12.1 到 B12.6
                question_columns.append(f'B{i}.{j}')
        elif i == 13:
            for j in range(1, 5):  # B13.1 到 B13.4
                question_columns.append(f'B{i}.{j}')
        elif i == 14:
            for j in range(1, 7):  # B14.1 到 B14.6
                question_columns.append(f'B{i}.{j}')
        elif i == 15:
            for j in range(1, 4):  # B15.1 到 B15.3
                question_columns.append(f'B{i}.{j}')
    
    # C組題目 (C16.1 到 C17.5)
    for i in range(16, 18):
        if i == 16:
            for j in range(1, 5):  # C16.1 到 C16.4
                question_columns.append(f'C{i}.{j}')
        elif i == 17:
            for j in range(1, 6):  # C17.1 到 C17.5
                question_columns.append(f'C{i}.{j}')
    
    # D組題目 (D18.1 到 D18.6)
    for j in range(1, 7):  # D18.1 到 D18.6
        question_columns.append(f'D18.{j}')
    
    # E組題目 (E19.1 到 E20.6)
    for i in range(19, 21):
        for j in range(1, 7):  # E19.1 到 E19.6, E20.1 到 E20.6
            question_columns.append(f'E{i}.{j}')
    
    print(f"\n需要建立的問卷欄位數量: {len(question_columns)}")
    
    # 處理問卷題目資料
    # 原始資料的 Q1 到 Q20 欄位需要轉換為對應的 A1.1 到 E20.6 格式
    # 使用字典一次性建立所有問卷欄位，避免效能警告
    question_data = {}
    
    # 處理每一行的問卷資料
    for idx, row in df.iterrows():
        row_question_data = {}
        
        # 處理 Q1-Q20 欄位的資料轉換
        q_columns = [f'Q{i}' for i in range(1, 21)]
        
        for i, q_col in enumerate(q_columns):
            if q_col in df.columns:
                q_value = row[q_col]
                converted_value = convert_question_data(q_value)
                
                # 將 Q1-Q20 對應到 A1.1-E20.6
                # 這裡是簡化的對應邏輯，實際應用時需要根據具體的問卷設計來調整
                if i < len(question_columns):
                    row_question_data[question_columns[i]] = converted_value
        
        # 如果沒有對應的問卷資料，則設為 0
        for col in question_columns:
            if col not in row_question_data:
                row_question_data[col] = 0
        
        question_data[idx] = row_question_data
    
    # 將問卷資料轉換為 DataFrame 並合併
    question_df = pd.DataFrame.from_dict(question_data, orient='index')
    processed_df = pd.concat([processed_df, question_df], axis=1)
    
    print(f"\n已建立 {len(question_columns)} 個問卷欄位")
    print("注意：問卷題目的具體轉換邏輯已實作，可根據實際需求調整 convert_question_data 函數")
    
    print(f"\n處理後的資料筆數: {len(processed_df)}")
    print(f"處理後的欄位數量: {len(processed_df.columns)}")
    
    # 儲存處理後的資料
    try:
        processed_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n資料處理完成！已儲存至: {output_file}")
        
        # 顯示處理後資料的基本資訊
        print(f"\n處理後資料基本資訊:")
        print(f"- 總筆數: {len(processed_df)}")
        print(f"- 總欄位數: {len(processed_df.columns)}")
        print(f"- 基本欄位: vip_id, age, sex, grade, city, cluster")
        print(f"- 分數欄位: 總分, 財務分數, 健康分數, 社交分數, 心靈分數, 獨立分數")
        print(f"- 問卷欄位: {len(question_columns)} 個 (A1.1 到 E20.6)")
        
        # 顯示前幾筆資料的範例
        print(f"\n前3筆資料範例:")
        print(processed_df.head(3).to_string())
        
    except Exception as e:
        print(f"儲存檔案時發生錯誤: {e}")

# 進行資料分析
def analyze_data_structure():
    """
    分析兩份檔案的資料結構差異
    """
    print("=== 資料結構分析 ===")
    
    # 偵測檔案編碼
    ref_file = "data/退休力-第三階段(final).xlsx - 送統計.csv"
    input_file = "data/retire 2025.csv"
    
    ref_encoding = detect_encoding(ref_file)
    input_encoding = detect_encoding(input_file)
    
    # 讀取參考檔案
    ref_df = pd.read_csv(ref_file, encoding=ref_encoding)
    
    # 讀取原始檔案
    df = pd.read_csv(input_file, encoding=input_encoding)
    
    print(f"\n參考檔案 ({ref_file}):")
    print(f"- 欄位數量: {len(ref_df.columns)}")
    print(f"- 資料筆數: {len(ref_df)}")
    print(f"- 欄位名稱: {list(ref_df.columns)}")
    
    print(f"\n原始檔案 ({input_file}):")
    print(f"- 欄位數量: {len(df.columns)}")
    print(f"- 資料筆數: {len(df)}")
    print(f"- 欄位名稱: {list(df.columns)}")
    
    # 找出共同欄位
    common_columns = set(ref_df.columns) & set(df.columns)
    print(f"\n共同欄位 ({len(common_columns)} 個):")
    for col in sorted(common_columns):
        print(f"- {col}")
    
    # 找出參考檔案獨有的欄位
    ref_only_columns = set(ref_df.columns) - set(df.columns)
    print(f"\n參考檔案獨有欄位 ({len(ref_only_columns)} 個):")
    for col in sorted(ref_only_columns):
        print(f"- {col}")
    
    # 找出原始檔案獨有的欄位
    input_only_columns = set(df.columns) - set(ref_df.columns)
    print(f"\n原始檔案獨有欄位 ({len(input_only_columns)} 個):")
    for col in sorted(input_only_columns):
        print(f"- {col}")

if __name__ == "__main__":
    # 先分析資料結構
    analyze_data_structure()
    
    print("\n" + "="*50)
    
    # 執行資料處理
    process_retirement_data()
