import glob, sys, os, cv2, datetime, math
from wand.image import Image 
from wand.display import display
from wand.color import Color
from wand.font import Font
from wand.drawing import Drawing

cap = cv2.VideoCapture(sys.argv[1])
currentframe = cv2.cv.CV_CAP_PROP_POS_FRAMES
fps = cv2.cv.CV_CAP_PROP_FPS
frames = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
images = []
timestamps = []

print "Getting frames."
for x in range(1,10):

    cap.set(currentframe, (frames/10)*x)

    ret, frame = cap.read()
    
    images.append("temp/" + str(cap.get(currentframe)) + ".png")
    cv2.imwrite("temp/" + str(cap.get(currentframe)) + ".png", frame)
    timestamps.append(datetime.timedelta(seconds=cap.get(currentframe) / cap.get(fps)))

cap.release()

print "Creating background image."
with Image(filename=images[0]) as b:
    with Color('white') as bgc:
        with Image(width=b.width*2, height=b.height*2, background=bgc) as bg: 
            bg.save(filename="temp/background.png")

print "Creating montage.."
with Image(filename="temp/background.png") as bg:
    offset_x = 0
    offset_y = 0
    row_size = 3
    i = 1
    font = Font(path="Alfphabet-IV.ttf", size=48)

    for image in images:    
        with Image(filename=image) as picture:      
            picture.resize(int(bg.width / 3), int(bg.height / 3))
            timestamp_text = str(timestamps[images.index(image)])
            milliseconds = timestamp_text.index('.')
            picture.caption(timestamp_text[:milliseconds], left=5, top=5, font=font)
            bg.composite(picture, left=offset_x, top=offset_y)

            if i == 3:
                offset_y += picture.height + 10
                offset_x = 0
                i = 0
            else:
                offset_x += picture.width + 10

            i += 1
        bg.save(filename="Output (" + sys.argv[1] + ").png")
    
print "Cleaning up!"

for image in images:
    os.remove(image)
os.remove("temp/background.png")