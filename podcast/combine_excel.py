import pandas as pd
import glob
from functools import reduce

files = glob.glob("datas/Ep*.csv")
print(len(files))

# 提取 Ep 集數作為後綴
dfs_with_suffixes = []
for f in files:
    ep_num = f.split('/')[-1].split('.')[0]  # 提取文件名中的 Ep 集數
    temp_df = pd.read_csv(f)
    # 重命名欄位，為每個集數加上後綴
    temp_df = temp_df.rename(columns={'下載數': f'下載數_{ep_num}', '不重複下載數': f'不重複下載數_{ep_num}'})
    dfs_with_suffixes.append(temp_df)

# 使用 reduce 逐步合併 DataFrame
result = reduce(
    lambda left, right: pd.merge(left, right, on='date', how='outer'),
    dfs_with_suffixes)

# 查看合併後的結果
print(result)
file_name = 'soundon_Data'
result.to_csv(f'{file_name}.csv', index=False)


print("合併完成，結果已保存為 f'{file_name}.csv'")