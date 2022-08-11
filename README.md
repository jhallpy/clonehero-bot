# Clone Hero Bot
This is an idea I had after becoming more interested in Python. It is not intended to be used in a multiplayer scenario ever. 

## Simple Explanation
This program currently runs only on 1920x1080 monitors in fullscreen at 60fps. It **should** work with any background or highway added by users. 
Originally I used purely background subtraction with good results. Multiple problems arose that made it easier to convert the images to HSV and create a mask.
After creating a mask I retain the background subtraction for quick processing of ROI's that I then turn into input on the kyeboard with pynput. 

I have not tested it at faster speeds than the default speed. It should theoretically work if you have a high enough refresh. It would be purely limited by DXcam's speed however.


## Future Plans
I would like to make this work on any resolution without user input necessary. I will look more into this once it actually works on the current configuration I am using. I would also like to add a GUI to start and stop the program instead of requiring keyboard inputs. 

Again, this is purely for fun and not intended to be used for online gameplay. I wanted a fun way to learn more about openCV for Python and chose this as a fun test bed.