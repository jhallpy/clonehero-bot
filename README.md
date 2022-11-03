# Clone Hero Bot
This is an idea I had after becoming more interested in Python. 
I was very interested in image processing and decided to use openCV to create a bot that would automatically play Clone Hero. 

## Simple Explanation
This program currently runs only on 1920x1080 monitors in fullscreen at 60fps. It **should** work with any background added by users. Any highway that doesn't have the note colors near the end of the highway will also work. 

Originally I used purely background subtraction with good results. Multiple problems arose that made it easier to convert the images to HSV and create a mask.
After creating a mask I retain the background subtraction for quick processing of ROI's that I then turn into input on the kyeboard with pynput. 

I have not tested it at faster note speeds than the default speed. It should theoretically work at higher note speeds if you have a high enough refresh rate. Currently the entire loop runs in 1-3 milliseconds. DXcam states that it will capture frames up to 240fps but, I currently have no way to test if this is correct or how it would affect the programs speed. Though based off the math of 3 milliseconds per frame processed the math comes out to 300fps which is faster than the stated cap of DXcam. 

## Installation and Use
Currently this is a command line program. Download the repo, install all of the dependencies from the requirements.txt file, then run the app.py file as you would on your operating system. The program starts/pauses with the letter 'T'. To exit the program press the letter 'Y". 

I have plans in the future to potentially create a GUI for this program but that will be after I have worked out most of the major bugs.

## Future Plans
I would like to make this work on any resolution without user input necessary. I will look more into this once it actually works on the current configuration I am using. I would also like to add a GUI to start and stop the program instead of requiring keyboard inputs. 

I plan to add images that I have saved of different steps and edge cases I have solved during the creation of this program.

This is purely for fun and not intended to be used for online gameplay. I wanted a fun way to learn more about openCV for Python and chose this as a fun test bed.