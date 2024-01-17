import pandas as pd
import matplotlib.pyplot as plt


def brand_analysis(df):
    # model percentage
    # by region and brand
    grouped1 = df.groupby(["REGION2", "BRAND"])["COPIES"].value_counts().unstack(fill_value=0)
    grouped1["MODELED_percentage"] = grouped1["MODELED"] / grouped1.sum(axis=1)
    # high_modeled_percentage_brands = grouped1[grouped1["MODELED_percentage"] > grouped1["MODELED_percentage"].mean()]

    grouped2 = df.groupby(["REGION2"])["COPIES"].value_counts().unstack(fill_value=0)
    grouped2["MODELED_percentage"] = grouped2["MODELED"] / grouped2.sum(axis=1)
    high_modeled_percentage_regions = grouped2[grouped2["MODELED_percentage"] > grouped2["MODELED_percentage"].mean()]

    # 获取grouped1和high_modeled_percentage_regions的第一层索引
    grouped1_first_level_index = grouped1.index.get_level_values(0)
    high_modeled_percentage_regions_first_level_index = high_modeled_percentage_regions.index
    # 使用isin()方法检查哪些索引在high_modeled_percentage_regions中出现
    indices_to_keep = grouped1_first_level_index.isin(high_modeled_percentage_regions_first_level_index)
    # 筛选出在high_modeled_percentage_regions中出现的索引
    grouped1_filtered = grouped1[indices_to_keep]
    # 再按照brand找出model占比较大的
    grouped1_filtered["MODELED_percentage"] = grouped1_filtered["MODELED"] / grouped1_filtered.sum(axis=1)
    high_modeled_percentage_brands2 = grouped1_filtered[
        grouped1_filtered["MODELED_percentage"] > grouped1_filtered["MODELED_percentage"].mean()]
    high_modeled_percentage_brands2.to_excel("MODELED percentage by region & brand.xlsx")

    # by country channel
    grouped3 = df.groupby(["CountryChannel", "BRAND"])["COPIES"].value_counts().unstack(fill_value=0)
    grouped3["MODELED_percentage"] = grouped3["MODELED"] / grouped3.sum(axis=1)
    high_modeled_percentage_brands_bychannel = grouped3[
        grouped3["MODELED_percentage"] >= 0.5]  # mean ~= 0.25, median = 0, 样本极不平衡
    high_modeled_percentage_brands_bychannel.to_excel("MODELED percentage by channel & brand.xlsx")

    # difference (by region and brand)
    df1 = df[["REGION2", "BRAND", "CountryChannel", "COPIES", "Sales Units E,NC", "Sales Units"]]
    df1 = df1.set_index(["REGION2", "BRAND"])
    df1["difference"] = abs(df1["Sales Units E,NC"] - df1["Sales Units"])
    df2 = df1[["Sales Units E,NC", "Sales Units", "difference"]]
    df2 = df2.fillna(0)  # fill nan as 0
    grouped4 = df2.groupby("REGION2")["difference"].sum().reset_index()
    grouped4 = grouped4.set_index("REGION2")
    grouped5 = df2.groupby(["REGION2", "BRAND"])["difference"].sum().reset_index()
    grouped5 = grouped5.set_index(["REGION2", "BRAND"])
    high_difference_regions = grouped4[grouped4["difference"] > grouped4["difference"].mean()]

    # 获取grouped5和high_difference_regions的第一层索引
    grouped5_first_level_index = grouped5.index.get_level_values(0)
    high_difference_regions_first_level_index = high_difference_regions.index
    # 使用isin()方法检查哪些索引在high_modeled_percentage_regions中出现
    indices_to_keep = grouped5_first_level_index.isin(high_difference_regions_first_level_index)
    # 筛选出在high_modeled_percentage_regions中出现的索引
    grouped5_filtered = grouped5[indices_to_keep]
    # 再按照city找出difference较大的
    high_difference_brands2 = grouped5_filtered[
        grouped5_filtered["difference"] > grouped5_filtered["difference"].mean()]
    high_difference_brands2.to_excel("High difference by region & brand (Aug.).xlsx")

    # difference (by channel and brand)
    df1 = df[["REGION2", "BRAND", "CountryChannel", "COPIES", "Sales Units E,NC", "Sales Units"]]
    df1 = df1.set_index(["CountryChannel", "BRAND"])
    df1["difference"] = abs(df1["Sales Units E,NC"] - df1["Sales Units"])
    df2 = df1[["Sales Units E,NC", "Sales Units", "difference"]]
    df2 = df2.fillna(0)  # fill nan as 0
    grouped6 = df2.groupby(["CountryChannel", "BRAND"])["difference"].sum().reset_index()
    grouped6 = grouped6.set_index(["CountryChannel", "BRAND"])
    high_difference_channels = grouped6[grouped6["difference"] > grouped6["difference"].mean()]
    high_difference_channels.to_excel("High difference by channel & brand (Aug.).xlsx")

    """
    9 月差距
        # difference (by region and brand)
        df1 = df[["REGION2", "BRAND", "CountryChannel", "COPIES", "Sales Units E,NC.1", "Sales Units.1"]]
        df1 = df1.set_index(["REGION2", "BRAND"])
        df1["difference"] = abs(df1["Sales Units E,NC.1"] - df1["Sales Units.1"])
        df2 = df1[["Sales Units E,NC.1", "Sales Units.1", "difference"]]
        df2 = df2.fillna(0)  # fill nan as 0
        grouped4 = df2.groupby("REGION2")["difference"].sum().reset_index()
        grouped4 = grouped4.set_index("REGION2")
        grouped5 = df2.groupby(["REGION2", "BRAND"])["difference"].sum().reset_index()
        grouped5 = grouped5.set_index(["REGION2", "BRAND"])
        high_difference_regions = grouped4[grouped4["difference"] > grouped4["difference"].mean()]
    
        # 获取grouped5和high_difference_regions的第一层索引
        grouped5_first_level_index = grouped5.index.get_level_values(0)
        high_difference_regions_first_level_index = high_difference_regions.index
        # 使用isin()方法检查哪些索引在high_modeled_percentage_regions中出现
        indices_to_keep = grouped5_first_level_index.isin(high_difference_regions_first_level_index)
        # 筛选出在high_modeled_percentage_regions中出现的索引
        grouped5_filtered = grouped5[indices_to_keep]
        # 再按照city找出difference较大的
        high_difference_brands2 = grouped5_filtered[
            grouped5_filtered["difference"] > grouped5_filtered["difference"].mean()]
        high_difference_brands2.to_excel("High difference by region & brand (Sep.).xlsx")
    
        # difference (by channel and brand)
        df1 = df[["REGION2", "BRAND", "CountryChannel", "COPIES", "Sales Units E,NC.1", "Sales Units.1"]]
        df1 = df1.set_index(["CountryChannel", "BRAND"])
        df1["difference"] = abs(df1["Sales Units E,NC.1"] - df1["Sales Units.1"])
        df2 = df1[["Sales Units E,NC.1", "Sales Units.1", "difference"]]
        df2 = df2.fillna(0)  # fill nan as 0
        grouped6 = df2.groupby(["CountryChannel", "BRAND"])["difference"].sum().reset_index()
        grouped6 = grouped6.set_index(["CountryChannel", "BRAND"])
        high_difference_channels = grouped6[grouped6["difference"] > grouped6["difference"].mean()]
        high_difference_channels.to_excel("High difference by channel & brand (Sep.).xlsx")
    
    """


if __name__ == "__main__":
    df = pd.read_excel("WEB data analysis-revised.xlsx")
    brand_analysis(df)
