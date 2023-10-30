from web import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fuzzywuzzy import fuzz

if __name__ == "__main__":
    df = pd.read_excel('xxx.xlsx')
    result_df = df[['WEB']].copy()
    print(result_df)
    # cmd: > chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\selenium_chrome"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='D:\downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe',
                              chrome_options=chrome_options)

    process_titles(9000, 9025, result_df, driver)

    df['TITLE'] = result_df['TITLE']
    df['ARTICLE_TEXT'] = df['ARTICLE_TEXT'].astype(str)
    df['TITLE'] = df['TITLE'].astype(str)
    df['similarity'] = df.apply(lambda row: fuzz.ratio(row['TITLE'], row['ARTICLE_TEXT']),
                                axis=1)
    df.to_excel(f'result{9000}.xlsx')

    # options = Options()
    # num = str(float(random.randint(500, 600)))
    # options.add_argument("--headless")  # run Chrome in headless mode
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 {}".format(
    #     num)
    # options.add_argument(f"user-agent={user_agent}")

    # disable loading images and css
    # prefs = {
    #     "profile.managed_default_content_settings.images": 2,
    #     "profile.managed_default_content_settings.stylesheet": 2
    # }
    # options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(executable_path='D:\downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe', options=options)
