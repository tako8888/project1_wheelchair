import os
import pandas as pd
import numpy as np

# 現在のディレクトリを基準にする
current_dir = os.getcwd()

# Column-Metadataを含むすべてのCSVファイルを読み込み、辞書を作成
metadata_dict = {}

for root, dirs, files in os.walk(current_dir):
    for file in files:
        if 'Column-Metadata' in file and file.endswith('.csv'):
            metadata_path = os.path.join(root, file)
            metadata_df = pd.read_csv(metadata_path)
            for _, row in metadata_df.iterrows():
                metadata_dict[row['Column Name']] = row['Label']

# census.csvを読み込み
census_file = os.path.join(current_dir, 'census.csv')
merged_df = pd.read_csv(census_file)

# 列名に対応するラベルを取得し、ラベルがない場合はNaNを設定
labels = [metadata_dict.get(col, np.nan) for col in merged_df.columns]

# ラベル行をデータフレームの最初の行に挿入
labels_df = pd.DataFrame([labels], columns=merged_df.columns)
merged_df_with_labels = pd.concat([labels_df, merged_df], ignore_index=True)

# 結果を確認
print(merged_df_with_labels.head())

# 必要なら新しいCSVとして保存
output_file = os.path.join(current_dir, 'census_with_labels.csv')
merged_df_with_labels.to_csv(output_file, index=False)
