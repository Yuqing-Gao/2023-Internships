"""
一个df，有“REGION2”“CITY2”“CountryChannel”“COPIES”“BRAND”“Item”“Sales Units NE,NC”“Sales Units E,NC”“Sales Units”列。

1． Vol分析：by region，Total + by Country Channel的 COPIES占比，标注Model占比过大的，另外也标注一下EC跟ENC变动过大的部分；
1. group by “REGION2”和 “CountryChannel”（其中REGION2以“CITY2”分层），分析“COPIES”列。其中“COPIES列只有三类数据：“MODELED”
"REGULAR" "COPY".找出MODELED占比过大的，再找出“Sales Units E,NC”“Sales Units”两列差距过大的。
2． Brand分析：by region，by Country Channel，各brand的COPIES占比，标注Model占比过大的，另外也标注一下EC跟ENC变动过大的部分；
3． Item分析：by region，by Country Channel，各brand中的型号COPIES占比，标注Model占比过大的，另外请标注regular enc占比与EC占比差距过大的（也就是真数推总后改动过大的部分）
4． 新型号样本情况分析：观察 NENC=0，EC有数的部分，缺失新型号的region和品牌请标注出来；
5． 老旧型号分析：帮忙标注 NENC有数，EC等于零的部分，老旧型号的TT需要清理一波；
6． Price CNY和Price CNY NE,NC之间的gap过大的，看是否集中在几家company里；
"""
import pandas as pd
import matplotlib.pyplot as plt


def pre_process():
    df = pd.read_excel("WEB data analysis-raw.xlsx", header=1)
    print(df)

    # group by

    # Merge city columns
    # 将"CITY2"列中值为"OTHERS"的行替换为对应的"CITY"和"CITY ID"的值
    mask = df['CITY2'] == 'OTHERS'
    df.loc[mask, 'CITY2'] = df['CITY']
    df.loc[mask, 'CITY2 ID'] = df['CITY ID']

    # 删除"CITY"列和"CITY ID"列
    df.drop(['CITY', 'CITY ID'], axis=1, inplace=True)
    print(df)


def Vol_analysis(df):
    df1 = df[["REGION2", "CITY2", "CountryChannel", "COPIES", "Sales Units E,NC", "Sales Units"]]
    df1 = df1.set_index(["REGION2", "CITY2"])

    # by region and city
    grouped1 = df.groupby(["REGION2", "CITY2"])["COPIES"].value_counts().unstack(fill_value=0)
    grouped1["MODELED_percentage"] = grouped1["MODELED"] / grouped1.sum(axis=1)
    # high_modeled_percentage_citys = grouped1[grouped1["MODELED_percentage"] > grouped1["MODELED_percentage"].mean()]

    # by region
    grouped2 = df.groupby(["REGION2"])["COPIES"].value_counts().unstack(fill_value=0)
    grouped2["MODELED_percentage"] = grouped2["MODELED"] / grouped2.sum(axis=1)
    high_modeled_percentage_regions = grouped2[grouped2["MODELED_percentage"] > grouped2["MODELED_percentage"].mean()]

    # by country channel
    # grouped3 = df.groupby(["CountryChannel"])["COPIES"].value_counts().unstack(fill_value=0)
    # grouped3["MODELED_percentage"] = grouped3["MODELED"] / grouped3.sum(axis=1)

    # grouped.hist(grid=0, column='MODELED_percentage')
    # plt.title('Modeled Percentage by xxx')
    # plt.savefig('Modeled Percentage by xxx.png', dpi=300)

    # 获取grouped1和high_modeled_percentage_regions的第一层索引
    grouped1_first_level_index = grouped1.index.get_level_values(0)
    high_modeled_percentage_regions_first_level_index = high_modeled_percentage_regions.index
    # 使用isin()方法检查哪些索引在high_modeled_percentage_regions中出现
    indices_to_keep = grouped1_first_level_index.isin(high_modeled_percentage_regions_first_level_index)
    # 筛选出在high_modeled_percentage_regions中出现的索引
    grouped1_filtered = grouped1[indices_to_keep]
    # 再按照city找出model占比较大的
    grouped1_filtered["MODELED_percentage"] = grouped1_filtered["MODELED"] / grouped1_filtered.sum(axis=1)
    high_modeled_percentage_citys2 = grouped1_filtered[grouped1_filtered["MODELED_percentage"] > grouped1_filtered["MODELED_percentage"].mean()]
    # high_modeled_percentage_citys2.to_excel("MODELED percentage by region & city.xlsx")

    # EC 和 ENC 差值 (by region & city)
    df1["difference"] = abs(df1["Sales Units E,NC"]-df1["Sales Units"])
    df2 = df1[["Sales Units E,NC", "Sales Units", "difference"]]
    df2 = df2.fillna(0)  # fill nan as 0
    grouped4 = df2.groupby("REGION2")["difference"].sum().reset_index()
    grouped4 = grouped4.set_index("REGION2")
    grouped5 = df2.groupby(["REGION2", "CITY2"])["difference"].sum().reset_index()
    grouped5 = grouped5.set_index(["REGION2", "CITY2"])
    high_difference_regions = grouped4[grouped4["difference"] > grouped4["difference"].mean()]

    # 获取grouped5和high_difference_regions的第一层索引
    grouped5_first_level_index = grouped5.index.get_level_values(0)
    high_difference_regions_first_level_index = high_difference_regions["REGION2"]
    # 使用isin()方法检查哪些索引在high_modeled_percentage_regions中出现
    indices_to_keep = grouped5_first_level_index.isin(high_difference_regions_first_level_index)
    # 筛选出在high_modeled_percentage_regions中出现的索引
    grouped5_filtered = grouped5[indices_to_keep]
    # 再按照city找出difference较大的
    high_difference_citys2 = grouped5_filtered[
        grouped5_filtered["difference"] > grouped5_filtered["difference"].mean()]
    # high_difference_citys2.to_excel("High difference by region & city (Aug.).xlsx")

    # EC 和 ENC 差值 (by channel)
    df3 = df1[["CountryChannel", "difference"]]
    df3 = df3.fillna(0)  # fill nan as 0
    grouped6 = df3.groupby("CountryChannel")["difference"].sum().reset_index()
    grouped6 = grouped6.set_index("CountryChannel")
    grouped6.to_excel("difference by channel (Aug.).xlsx")
    # high_difference_channels = grouped6[grouped6["difference"] > grouped6["difference"].mean()]  # 高于平均的就一个

    """
    9月的差值
    # EC 和 ENC 差值 (by region & city)
    df1 = df[["REGION2", "CITY2", "CountryChannel", "COPIES", "Sales Units E,NC.1", "Sales Units.1"]]
    df1 = df1.set_index(["REGION2", "CITY2"])
    df1["difference"] = abs(df1["Sales Units E,NC.1"]-df1["Sales Units.1"])
    df2 = df1[["Sales Units E,NC.1", "Sales Units.1", "difference"]]
    df2 = df2.fillna(0)  # fill nan as 0
    grouped4 = df2.groupby("REGION2")["difference"].sum().reset_index()
    grouped4 = grouped4.set_index("REGION2")
    grouped5 = df2.groupby(["REGION2", "CITY2"])["difference"].sum().reset_index()
    grouped5 = grouped5.set_index(["REGION2", "CITY2"])
    high_difference_regions = grouped4[grouped4["difference"] > grouped4["difference"].mean()]

    # 获取grouped5和high_difference_regions的第一层索引
    grouped5_first_level_index = grouped5.index.get_level_values(0)
    high_difference_regions = high_difference_regions.reset_index()
    high_difference_regions_first_level_index = high_difference_regions["REGION2"]
    # 使用isin()方法检查哪些索引在high_modeled_percentage_regions中出现
    indices_to_keep = grouped5_first_level_index.isin(high_difference_regions_first_level_index)
    # 筛选出在high_modeled_percentage_regions中出现的索引
    grouped5_filtered = grouped5[indices_to_keep]
    # 再按照city找出difference较大的
    high_difference_citys2 = grouped5_filtered[
        grouped5_filtered["difference"] > grouped5_filtered["difference"].mean()]
    # high_difference_citys2.to_excel("High difference by region & city (Sep.).xlsx")

    # EC 和 ENC 差值 (by channel)
    df3 = df1[["CountryChannel", "difference"]]
    df3 = df3.fillna(0)  # fill nan as 0
    grouped6 = df3.groupby("CountryChannel")["difference"].sum().reset_index()
    grouped6 = grouped6.set_index("CountryChannel")
    grouped6.to_excel("difference by channel (Sep.).xlsx")
    # high_difference_channels = grouped6[grouped6["difference"] > grouped6["difference"].mean()]  # 高于平均的就一个
    """


if __name__ == "__main__":
    df = pd.read_excel("WEB data analysis-revised.xlsx")
    Vol_analysis(df)
