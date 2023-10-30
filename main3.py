import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

# main3 for taobao and t-mall

if __name__ == "__main__":
    df = pd.read_excel('xxx.xlsx')
    # df['MARK'] = 0

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

                # need to sign in
                if current_url.startswith('https://login.taobao.com/'):
                    print("请登陆后按Enter键继续")
                    input()
                if pd.isna(link):
                    continue
                if link.startswith('https://detail.tmall.com/') or link.startswith('https://item.taobao.com/'):
                    driver.get(link)
                    driver.implicitly_wait(5)
                    if '您查看的页面找不到了' in driver.title:
                        df.at[index, 'MARK'] = 1
                    if "很抱歉，您查看的宝贝不存在，可能已下架或者被转移。" in driver.page_source or "此宝贝已下架" in driver.page_source or "很抱歉，您查看的商品找不到了" in driver.page_source:
                        df.at[index, 'MARK'] = 1

                    if driver.title == '验证码拦截' or driver.title == '商品详情':
                        print("请手动判断后按Enter键继续（失效1，未失效0）")
                        df.at[index, 'MARK'] = input()
                    elif driver.title == '访问被拒绝':
                        print("寄！")  # just for fun:)
                        input()

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
