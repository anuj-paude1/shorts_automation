



def get_link(key):
    from youtubesearchpython import VideosSearch
    videosSearch = VideosSearch(key, limit = 100)
    result=videosSearch.result()["result"]
    for _ in result:
        duration=_["duration"].split(":")
        duration=int(duration[0]+duration[1])
        if duration<120:
            return _["link"]
    

def get_video_yt(what=""):
    from pytube import Search,YouTube
    key=what+" stock footage no watermark high quality -how"
    print(key)
    link=get_link(key)
    print(link)
    yt=YouTube(link)
    video = yt.streams.get_highest_resolution()
    filename=f"{what}.mp4"
    video.download(output_path="../temp/videos",filename=filename)
    return filename

def get_video_pixabay(what=""):
    api_key="32736707-f15f01d5c8df3abc424b8dc95"
    import cloudscraper
    if what=="":
        return -1
    scraper = cloudscraper.create_scraper()
    response = scraper.get(f"https://pixabay.com/api/videos/?key={api_key}&q={what}").json()
    if(response["total"]==0):
        get_video_pixabay(' '.join(what.split()[:-1]))
    else:
        video_res=response["hits"][0]['videos']['large']['url']
        print(video_res)
        video=scraper.get(video_res)
        # Specify the path where you want to save the image
        vid_name=what[:10]
        vid_path = f'../temp/videos/{vid_name}.mp4'
        with open(vid_path, 'wb') as file:
            file.write(video.content)
        return f"{vid_name}.mp4"
    



def get_img(what):
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium import webdriver
    import cloudscraper
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)


    driver.get('https://www.google.com/imghp')
    prompt=what+" png transparent"
    # Find the search bar and input your query (e.g., "cat")
    search_box = driver.find_element(By.ID,"APjFqb")
    search_box.send_keys(prompt)
    search_box.submit()

    # Wait for the search results to load (you may need to adjust the sleep time)
    time.sleep(2)

    # Find the first image and click on it to view the larger version
    first = driver.find_element(By.XPATH,'//*[@data-ri="0"]')
    first.click()
    time.sleep(5)
    big_img=driver.find_element(By.XPATH,'//*[@jsname="kn3ccd"]')
    src=big_img.get_attribute("src")
    # Wait for the larger image to load (you may need to adjust the sleep time)
    time.sleep(2)

    scraper = cloudscraper.create_scraper()

    response = scraper.get(src)
    image_name=what[:10]
    # Specify the path where you want to save the image
    image_path = f'../temp/images/{image_name}.png'

    with open(image_path, 'wb') as file:
        file.write(response.content)
    # Close the browser
    driver.quit()
    return f"{image_name}.png"

def main():
    ...

if __name__=="__main__":
    main()