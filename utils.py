import glob
import numpy as np
import cv2
import glob
import moviepy.editor as mp
import moviepy
import ffmpeg
import os
import subprocess
print("moviepy version",moviepy.__version__)
import requests
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession



def resize_img(image,Resize=(1080,1920)):
    imgshp=image.shape
    h,w=imgshp[:2]
    #print(h,w)
    hw=h//w
    rhw=Resize[0]/Resize[1]
    
    img_r=cv2.resize(image,Resize,interpolation=cv2.INTER_AREA)

    return img_r


def ImageAudio(image,Audio,outname,outshape=[1080,1920]):
    mpAudio=mp.AudioFileClip(Audio)
    dur=mpAudio.duration
    ic = mp.ImageClip(image).set_duration(dur)
    ic.audio = mpAudio
    ic.write_videofile(f"{outname}.mp4", fps=10,audio=True)
    AddAudio(f"{outname}.mp4",Audio,f"{outname}_ffmpg.mp4")

    #cmd=f"ffmpeg -i {Audio} -i {image} -acodec copy -r 1 -shortest -vf scale=1280:720 {outname}.mp4"
   # subprocess.run(cmd)





def AddAudio(audioless_file,Audio_file,outname):
 
    file=audioless_file
    video_info=ffmpeg.probe(file)
    #video_info
    input_video =ffmpeg.input(file)
    input_audio =ffmpeg.input(Audio_file).audio
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{outname}.mp4').run(overwrite_output=True)
    return f"{outname} Created"

##########################################################
def get_source(url):

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)
def get_feed_to_df(url):
    response = get_source(url)
    
    df = pd.DataFrame(columns = ['title', 'pubDate', 'guid', 'description',"audio","image"])

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        
          
            title = item.find('title', first=True).text
            pubDate = item.find('pubDate', first=True).text
            guid = item.find('guid', first=True).text
            description = item.find('description', first=True).text
            audio=item.find("enclosure")[0].attrs["url"]
            pic=item.find("image")[0].attrs["href"]
            row = {'title': title, 'pubDate': pubDate, 'guid': guid, 'description': description,"audio":audio,"image":pic}
            df = df.append(row, ignore_index=True)
    df.pubDate=pd.to_datetime(df.pubDate)
    return df

def download_req(url,savename):
    response = requests.get(url)
    with open(savename, 'wb') as saveFile:
            saveFile.write(response.content)

def download_anchor(latest=0,url="https://anchor.fm/s/561f4400/podcast/rss",download_path="./danchor_downloads/"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    df=get_feed_to_df(url)
   # if latest.type==
    row=df.iloc[latest]
    
    date=str(row.pubDate.date())+"_"+str(row.pubDate.time()).replace(":","")
    saveFilePathAudio=os.path.join(os.getcwd(),f"{download_path}Anchor_download_{date}.mp3")
    download_req(row.audio,saveFilePathAudio)
    saveFilePathImage=saveFilePathAudio.replace(".mp3",".jpg")
    download_req(row.image,saveFilePathImage)
  #  response = requests.get(row.audio)
  #  with open(saveFilePath, 'wb') as saveFile:
   #         saveFile.write(response.content)
    return saveFilePathAudio,saveFilePathImage
    
    


##########################################################

def main():
    #image="Podcast_Tools/Podcast_video/test_material/image_1.jpg"
    url1="https://anchor.fm/s/561f4400/podcast/rss"
    url2="https://anchor.fm/s/55642738/podcast/rss"
    audio,image=download_anchor(url=url1)
    image=r"D:\JJJapan\Podcast\20210105\JinJapan_thumbnail.png"
    ImageAudio(image,audio,"Podcast_Tools/Podcast_video/test_material/test_out")


if __name__=="__main__":
    main()

