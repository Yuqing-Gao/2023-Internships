import pandas as pd


def new_analysis(df):
    df1 = df[["COMPANY", "Price CNY NE,NC", "Price CNY", "Price CNY NE,NC.1", "Price CNY.1"]].fillna(0)
    df1["difference"] = abs(df1["Price CNY NE,NC"]-df1["Price CNY"])
    df1["difference.1"] = abs(df1["Price CNY NE,NC.1"] - df1["Price CNY.1"])

    # 计算 "difference" 和 "difference.1" 列的均值和标准差
    mean_difference = df1["difference"].mean()
    std_difference = df1["difference"].std()

    mean_difference_1 = df1["difference.1"].mean()
    std_difference_1 = df1["difference.1"].std()

    # 使用均值和标准差来确定阈值，例如可以选择 2 倍标准差作为阈值
    threshold = 2 * std_difference
    threshold_1 = 2 * std_difference_1

    # 筛选出 "difference" 列大于阈值的行
    large_difference_rows = df1[df1["difference"] > threshold]

    # 筛选出 "difference.1" 列大于阈值的行
    large_difference_rows_1 = df1[df1["difference.1"] > threshold_1]

    # 创建新的DataFrame存储筛选结果
    df_large_difference = large_difference_rows.copy().set_index("COMPANY")
    df_large_difference_1 = large_difference_rows_1.copy().set_index("COMPANY")

    df_large_difference.to_excel("large gap companies in detail (Aug.).xlsx")
    df_large_difference_1.to_excel("large gap companies in detail (Sep.).xlsx")

    df_large_difference_grouped = df_large_difference.groupby("COMPANY")["difference"].sum()
    df_large_difference_1_grouped = df_large_difference_1.groupby("COMPANY")["difference.1"].sum()

    df_large_difference_grouped.to_excel("large gap companies (Aug.).xlsx")
    df_large_difference_1_grouped.to_excel("large gap companies (Sep.).xlsx")


if __name__ == "__main__":
    df = pd.read_excel("WEB data analysis-revised.xlsx")
    new_analysis(df)