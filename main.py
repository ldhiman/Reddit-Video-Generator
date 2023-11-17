from moviepy.editor import *
import reddit, screenshot, time, subprocess, random, configparser, sys, math
from os import listdir
import youtube_upload
from os.path import isfile, join


def createVideo():
    config = configparser.ConfigParser()
    config.read("config.ini")
    outputDir = r"D:\Python\RedditVideoGenerator\OutputVideos"

    startTime = time.time()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if len(sys.argv) == 2:
        id, script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = 10
        id, script = reddit.getContent(outputDir, postOptionCount)
    fileName = script.getFileName()

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script, id)

    # Setup background clip
    bgDir = r"D:\Python\RedditVideoGenerator\BackgroundVideos"
    bgPrefix = "ShortTemplate_"
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
    bgCount = len(bgFiles)
    bgIndex = random.randint(1, bgCount)
    backgroundVideo = VideoFileClip(
        filename=rf"{bgDir}\{bgPrefix}{bgIndex}.mp4", audio=False
    ).subclip(0, script.getDuration())
    w, h = backgroundVideo.size

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(screenShotFile, duration=audioClip.duration).set_position(
            ("center", "center")
        )
        imageClip = imageClip.resize(width=(w - marginSize))
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = 64
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(
            __createClip(comment.screenShotFile, comment.audioClip, marginSize)
        )

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], size=backgroundVideo.size
    ).set_audio(contentOverlay.audio)
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate = "8000k"
    threads = "12"
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, codec="mpeg4", threads=threads, bitrate=bitrate, fps=24
    )
    print(f"Video completed in {time.time() - startTime}")

    # Preview in VLC for approval before uploading
    if False:
        vlcPath = "C:/Program Files/VideoLAN/VLC/vlc.exe"
        p = subprocess.Popen([vlcPath, outputFile])
        print("Waiting for video review. Type anything to continue")
        wait = input()

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")
    return script.title, outputFile
    # youtube_upload.upload_video(script.title, outputFile)


if __name__ == "__main__":
    createVideo()
