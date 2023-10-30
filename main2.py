import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

# main2 for jingdong

if __name__ == "__main__":
    df = pd.read_excel('xxx.xlsx')
    df['MARK'] = 0

    # cmd: > chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\selenium_chrome"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='D:\downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe',
                              chrome_options=chrome_options)

    try:
        start_index = 0
        batch_size = 200  # number of rows everytime
        end_index = start_index + batch_size

        while end_index < len(df):
            end_index = min(start_index + batch_size, len(df))
            batch_df = df.iloc[start_index:end_index]
            current_url = driver.current_url

            for index, row in batch_df.iterrows():
                link = row['WEB']

                # Verification code
                if current_url.startswith('https://cfe.m.jd.com/'):
                    print("请手动处理验证码并按Enter键继续")
                    input()  # wait for input
                    continue

                if pd.isna(link):
                    continue
                elif link.startswith('https://item.jd.com'):
                    driver.get(link)
                    driver.implicitly_wait(5)

                    # if jump to https://www.jd.com/?d
                    if current_url == 'https://www.jd.com/?d':
                        df.at[index, 'MARK'] = 1

                    # if the product is removed
                    elif "该商品已下柜，欢迎挑选其他商品！" in driver.page_source:
                        df.at[index, 'MARK'] = 1

                print(index, start_index, df.loc[index, 'MARK'])

            # save the result
            df.to_excel('ONLINETT-WEB-2309.xlsx', index=False)
            # update the index
            start_index += batch_size

    except TimeoutException as e:
        print(f"Timed out: {e}")
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.close()  # close the window
