import pandas as pd
import glob

data_path = glob.glob('./data_1/*')

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    # nan 값 제거
    df_temp.dropna(inplace=True)
    # 중복 제거
    df_temp.drop_duplicates(subset=['landmark'], keep='first', inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)

# 중복 제거
df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./crawling_data/reviews_tour_1.csv', index=False)