import random
import pandas as pd
from selenium.common.exceptions import TimeoutException, WebDriverException


def process_titles(start_i, end_i, df, driver):

    try:
        for i in range(start_i, end_i):
            print(i)
            if pd.isna(df.loc[i, 'WEB']):
                df.loc[i, 'TITLE'] = 'NULL'
                continue
            try:
                driver.get(df.loc[i, 'WEB'])
                driver.implicitly_wait(5)
                title = driver.title
                df.loc[i, 'TITLE'] = title
            except TimeoutException as e:
                print(f"Timed out: {e}")
                df.loc[i, 'TITLE'] = 'WRONG'
                continue
            except WebDriverException as e:
                print(f"WebDriver error: {e}")
                df.loc[i, 'TITLE'] = 'WRONG'
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                df.loc[i, 'TITLE'] = 'WRONG'
                continue
    finally:
        driver.close()
