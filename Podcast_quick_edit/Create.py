import os , sys, stat
import glob
import subprocess
import shutil
from PIL import Image
import moviepy.editor as mp
import moviepy
import ffmpeg

#Files

print(__file__)
BASEDIR= os.path.realpath(__file__).replace("Create.py","")
#base files names
Phase=["phase1.m4a","phase2.m4a"]



def AddAudio(audioless_file,Audio_file,outname):
    file=audioless_file
    video_info=ffmpeg.probe(file)
    #video_info
    input_video =ffmpeg.input(file)
    input_audio =ffmpeg.input(Audio_file).audio
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{outname}.mp4').run(overwrite_output=True)
    return f"{outname} Created"


def CreateAudio_files(location,Phase=Phase):
    new_file=os.path.join(location,'mylist.txt')
    out_file=os.path.join(location,'output.mp4')
    with open(f"{new_file}","w+") as f:
        #Intro
        intro_f=[file for file in os.listdir(location) if "intro" in file.lower()][0]
        print( f"file '{os.path.join(location,intro_f)}'", file=f)
        print( f"file '{os.path.join(BASEDIR,'mics',Phase[0])}'", file=f)
        print( f"file '{os.path.join(BASEDIR,'mics',Phase[1])}'", file=f)
        #for Pfile in Phase1:
            #print(f"file '{os.path.join(BASEDIR,Pfile)}'", file=f)
           
        Part_files=[file for file in os.listdir(location) if "p" in file.lower()]
        for file in Part_files:
             print( f"file '{os.path.join(location,file)}'", file=f)
             print( f"file '{os.path.join(BASEDIR,'mics',Phase[1])}'", file=f)
    f.close()
    subprocess.run(f"ffmpeg -f concat -safe 0 -i {new_file} -acodec copy {out_file}", shell=True, check=True)
    return out_file

def main():
    location=os.path.join(BASEDIR,"Test" )
    out_file=CreateAudio_files(location)

    t=mp.AudioFileClip(out_file).duration
    ic = mp.ImageClip(os.path.join(location,"2.png")).set_duration(t)
   
    video = mp.concatenate([ic], method="compose")
    #video.audio = Audio
    video.write_videofile('audioless.mp4', fps=20)
    AddAudio('audioless.mp4',out_file,os.path.join(BASEDIR,"final.mp4"))
    os.remove("audioless.mp4")
if __name__ =="__main__":
    main()