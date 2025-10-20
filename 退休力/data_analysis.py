#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
退休力資料分析程式
分析 retire_2025_processed.csv 資料並生成分析報告

功能：
1. 讀取處理後的退休力資料
2. 進行多維度資料分析
3. 生成統計報告
4. 輸出 Excel 格式的分析結果
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """
    載入資料
    """
    print("載入資料...")
    
    # 讀取處理後的資料
    data_file = "data/retire_2025_processed.csv"
    try:
        df = pd.read_csv(data_file, encoding='utf-8')
        print(f"成功載入資料: {len(df)} 筆記錄, {len(df.columns)} 個欄位")
        return df
    except Exception as e:
        print(f"載入資料時發生錯誤: {e}")
        return None

def basic_statistics(df):
    """
    基本統計分析
    """
    print("\n=== 基本統計分析 ===")
    
    # 基本資訊
    # 年齡欄位是編碼過的，需要轉換為實際年齡組
    age_mapping = {1: '20-29歲', 2: '30-39歲', 3: '40-49歲', 4: '50-59歲', 
                   5: '60-69歲', 6: '70-79歲', 7: '80-89歲', 8: '90歲以上'}
    
    basic_info = {
        '總樣本數': len(df),
        '男性': len(df[df['sex'] == 1]),
        '女性': len(df[df['sex'] == 2]),
        '平均年齡組': df['age'].mean(),
        '年齡組標準差': df['age'].std(),
        '最小年齡組': df['age'].min(),
        '最大年齡組': df['age'].max(),
        '主要年齡組': age_mapping.get(df['age'].mode().iloc[0], '未知')
    }
    
    # 分數統計
    score_columns = ['總分', '財務分數', '健康分數', '社交分數', '心靈分數', '獨立分數']
    score_stats = df[score_columns].describe()
    
    # 等級分布
    grade_dist = df['grade'].value_counts().sort_index()
    
    # 城市分布
    city_dist = df['city'].value_counts().head(10)
    
    # 群組分布
    cluster_dist = df['cluster'].value_counts().sort_index()
    
    return {
        'basic_info': basic_info,
        'score_stats': score_stats,
        'grade_dist': grade_dist,
        'city_dist': city_dist,
        'cluster_dist': cluster_dist
    }

def demographic_analysis(df):
    """
    人口統計分析
    """
    print("\n=== 人口統計分析 ===")
    
    # 性別分布
    gender_analysis = df.groupby('sex').agg({
        'age': ['count', 'mean', 'std'],
        '總分': ['mean', 'std'],
        '財務分數': 'mean',
        '健康分數': 'mean',
        '社交分數': 'mean',
        '心靈分數': 'mean',
        '獨立分數': 'mean'
    }).round(2)
    
    # 年齡組分析 (使用編碼後的年齡組)
    age_mapping = {1: '20-29歲', 2: '30-39歲', 3: '40-49歲', 4: '50-59歲', 
                   5: '60-69歲', 6: '70-79歲', 7: '80-89歲', 8: '90歲以上'}
    df['age_group'] = df['age'].map(age_mapping)
    
    age_analysis = df.groupby('age_group').agg({
        '總分': ['count', 'mean', 'std'],
        '財務分數': 'mean',
        '健康分數': 'mean',
        '社交分數': 'mean',
        '心靈分數': 'mean',
        '獨立分數': 'mean'
    }).round(2)
    
    # 等級分析
    grade_analysis = df.groupby('grade').agg({
        '總分': ['count', 'mean', 'std'],
        '財務分數': 'mean',
        '健康分數': 'mean',
        '社交分數': 'mean',
        '心靈分數': 'mean',
        '獨立分數': 'mean'
    }).round(2)
    
    return {
        'gender_analysis': gender_analysis,
        'age_analysis': age_analysis,
        'grade_analysis': grade_analysis
    }

def score_analysis(df):
    """
    分數分析
    """
    print("\n=== 分數分析 ===")
    
    score_columns = ['總分', '財務分數', '健康分數', '社交分數', '心靈分數', '獨立分數']
    
    # 分數相關性分析
    correlation_matrix = df[score_columns].corr()
    
    # 分數分布分析
    score_distribution = {}
    for col in score_columns:
        score_distribution[col] = {
            'mean': df[col].mean(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'median': df[col].median(),
            'q25': df[col].quantile(0.25),
            'q75': df[col].quantile(0.75)
        }
    
    # 高分群組分析 (總分前20%)
    high_score_threshold = df['總分'].quantile(0.8)
    high_score_group = df[df['總分'] >= high_score_threshold]
    
    # 低分群組分析 (總分後20%)
    low_score_threshold = df['總分'].quantile(0.2)
    low_score_group = df[df['總分'] <= low_score_threshold]
    
    return {
        'correlation_matrix': correlation_matrix,
        'score_distribution': score_distribution,
        'high_score_group': high_score_group,
        'low_score_group': low_score_group,
        'high_score_threshold': high_score_threshold,
        'low_score_threshold': low_score_threshold
    }

def questionnaire_analysis(df):
    """
    問卷分析
    """
    print("\n=== 問卷分析 ===")
    
    # 取得所有問卷欄位
    question_columns = [col for col in df.columns if col.startswith(('A', 'B', 'C', 'D', 'E'))]
    
    # 各組問卷統計
    group_stats = {}
    for group in ['A', 'B', 'C', 'D', 'E']:
        group_cols = [col for col in question_columns if col.startswith(group)]
        if group_cols:
            group_stats[f'{group}組'] = {
                '題數': len(group_cols),
                '平均得分': df[group_cols].mean(axis=1).mean(),
                '標準差': df[group_cols].mean(axis=1).std(),
                '最高得分': df[group_cols].mean(axis=1).max(),
                '最低得分': df[group_cols].mean(axis=1).min()
            }
    
    # 問卷項目分析
    question_analysis = {}
    for col in question_columns:
        question_analysis[col] = {
            '平均分': df[col].mean(),
            '標準差': df[col].std(),
            '回答1的比例': (df[col] == 1).mean(),
            '回答0的比例': (df[col] == 0).mean()
        }
    
    return {
        'group_stats': group_stats,
        'question_analysis': question_analysis
    }

def generate_insights(df, basic_stats, demo_stats, score_stats, quest_stats):
    """
    生成洞察分析
    """
    print("\n=== 洞察分析 ===")
    
    insights = []
    
    # 基本洞察
    insights.append("📊 基本統計洞察:")
    insights.append(f"- 總樣本數: {basic_stats['basic_info']['總樣本數']} 人")
    insights.append(f"- 主要年齡組: {basic_stats['basic_info']['主要年齡組']}")
    insights.append(f"- 性別比例: 男性 {basic_stats['basic_info']['男性']} 人, 女性 {basic_stats['basic_info']['女性']} 人")
    
    # 分數洞察
    insights.append("\n📈 分數洞察:")
    total_score_mean = basic_stats['score_stats'].loc['mean', '總分']
    insights.append(f"- 平均總分: {total_score_mean:.1f} 分")
    
    # 找出最高和最低的分數維度
    score_means = basic_stats['score_stats'].loc['mean', ['財務分數', '健康分數', '社交分數', '心靈分數', '獨立分數']]
    highest_dimension = score_means.idxmax()
    lowest_dimension = score_means.idxmin()
    insights.append(f"- 最高分維度: {highest_dimension} ({score_means[highest_dimension]:.1f} 分)")
    insights.append(f"- 最低分維度: {lowest_dimension} ({score_means[lowest_dimension]:.1f} 分)")
    
    # 人口統計洞察
    insights.append("\n👥 人口統計洞察:")
    gender_analysis = demo_stats['gender_analysis']
    if len(gender_analysis) > 1:
        male_avg = gender_analysis.loc[1, ('總分', 'mean')]
        female_avg = gender_analysis.loc[2, ('總分', 'mean')]
        insights.append(f"- 男性平均總分: {male_avg:.1f} 分")
        insights.append(f"- 女性平均總分: {female_avg:.1f} 分")
    
    # 問卷洞察
    insights.append("\n📝 問卷洞察:")
    for group, stats in quest_stats['group_stats'].items():
        insights.append(f"- {group}: 平均得分 {stats['平均得分']:.2f} 分 (共 {stats['題數']} 題)")
    
    return insights

def save_to_excel(df, basic_stats, demo_stats, score_stats, quest_stats, insights, output_file):
    """
    將分析結果儲存到 Excel 檔案
    """
    print(f"\n儲存分析結果到: {output_file}")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 原始資料
        df.to_excel(writer, sheet_name='原始資料', index=False)
        
        # 基本統計
        basic_info_df = pd.DataFrame([basic_stats['basic_info']])
        basic_info_df.to_excel(writer, sheet_name='基本統計', index=False)
        
        basic_stats['score_stats'].to_excel(writer, sheet_name='分數統計')
        basic_stats['grade_dist'].to_excel(writer, sheet_name='等級分布')
        basic_stats['city_dist'].to_excel(writer, sheet_name='城市分布')
        basic_stats['cluster_dist'].to_excel(writer, sheet_name='群組分布')
        
        # 人口統計分析
        demo_stats['gender_analysis'].to_excel(writer, sheet_name='性別分析')
        demo_stats['age_analysis'].to_excel(writer, sheet_name='年齡組分析')
        demo_stats['grade_analysis'].to_excel(writer, sheet_name='等級分析')
        
        # 分數分析
        score_stats['correlation_matrix'].to_excel(writer, sheet_name='分數相關性')
        
        # 分數分布
        score_dist_df = pd.DataFrame(score_stats['score_distribution']).T
        score_dist_df.to_excel(writer, sheet_name='分數分布')
        
        # 高分群組
        score_stats['high_score_group'].to_excel(writer, sheet_name='高分群組', index=False)
        score_stats['low_score_group'].to_excel(writer, sheet_name='低分群組', index=False)
        
        # 問卷分析
        group_stats_df = pd.DataFrame(quest_stats['group_stats']).T
        group_stats_df.to_excel(writer, sheet_name='問卷組別統計')
        
        # 問卷項目分析 (前50個項目)
        question_analysis_df = pd.DataFrame(quest_stats['question_analysis']).T.head(50)
        question_analysis_df.to_excel(writer, sheet_name='問卷項目分析')
        
        # 洞察分析
        insights_df = pd.DataFrame({'洞察分析': insights})
        insights_df.to_excel(writer, sheet_name='洞察分析', index=False)
    
    print("✅ 分析結果已成功儲存到 Excel 檔案")

def main():
    """
    主程式
    """
    print("退休力資料分析程式")
    print("=" * 50)
    
    # 載入資料
    df = load_data()
    if df is None:
        return
    
    # 進行各項分析
    basic_stats = basic_statistics(df)
    demo_stats = demographic_analysis(df)
    score_stats = score_analysis(df)
    quest_stats = questionnaire_analysis(df)
    
    # 生成洞察
    insights = generate_insights(df, basic_stats, demo_stats, score_stats, quest_stats)
    
    # 輸出洞察到控制台
    for insight in insights:
        print(insight)
    
    # 儲存到 Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/退休力分析報告_{timestamp}.xlsx"
    save_to_excel(df, basic_stats, demo_stats, score_stats, quest_stats, insights, output_file)
    
    print(f"\n🎉 分析完成！結果已儲存至: {output_file}")

if __name__ == "__main__":
    main()
