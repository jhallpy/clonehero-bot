# Clone Hero Bot
This is an idea I had after becoming more interested in Python. 
I was very interested in image processing and decided to use openCV to create a bot that would automatically play Clone Hero. 

## Simple Explanation
This program currently runs only on 1920x1080 monitors in fullscreen at 60fps. It **should** work with any background added by users. Any highway that doesn't have note colors near the end of the highway will also work. 

Originally I used purely background subtraction with good results. Multiple problems arose that made it easier to convert the images to HSV and create a mask.
After creating a mask I retain the background subtraction for quick processing of ROI's that I then turn into input on the kyeboard with pynput. 

I have not tested it at faster note speeds than the default speed. It should theoretically work at higher note speeds if you have a high enough refresh rate. Currently the entire loop runs in 1-3 milliseconds. DXcam states that it will capture frames up to 240fps but, I currently have no way to test if this is correct or how it would affect the programs speed. Though based off the math of 3 milliseconds per frame processed the math comes out to 300fps which is faster than the stated cap of DXcam. 

## Installation and Use
Currently this is a command line program. Download the repo, install all of the dependencies from the requirements.txt file, then run the app.py file as you would on your operating system. The program starts/pauses with the letter 'T'. To exit the program press the letter 'Y". 

## No Longer Developing
I've completed what I set out to do. This program is not for the masses to use to cheat. I simply wanted a fun way to learn OpenCV in Python. There are still bugs in this program that I don't plan to fix. As it stands it will FC most songs. It won't set any score records. I do not account for star power at all. I will not be developing this for any other game at all. 

I no longer plan to create a GUI for this program as it's not something that interests me. 

I will at a later date add documentation on the development process. 