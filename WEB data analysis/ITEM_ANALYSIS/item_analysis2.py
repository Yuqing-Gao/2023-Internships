import pandas as pd


def item_analysis2(df):
    aug_channel = pd.read_excel("High difference by channel & brand & item (Aug.).xlsx")
    sep_channel = pd.read_excel("High difference by channel & brand & item (Sep.).xlsx")
    aug_region = pd.read_excel("High difference by region & brand & item (Aug.).xlsx")
    sep_channel = pd.read_excel("High difference by region & brand & item (Sep.).xlsx")


if __name__ == "__main__":
    df = pd.read_excel("WEB data analysis-revised.xlsx")
