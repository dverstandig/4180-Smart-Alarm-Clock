## Welcome to GitHub Pages

TEST121212

## Authors

Dylan Verstandig\
Jacob Lattie\
Peter Nguyen

## Project Overview

The Smart Alarm Clock is a responsive graphical user interface for quickly recieving information about your day. Powered by a Raspberry Pi 3 and developed with Alexa Voice Services, the Smart Alarm Clock will keep you prepared.

## Gallery

Insert Images. NEED TO GET THEM OFF OF RPI 

## Hardware and Software

### Hardware

```
Raspberry Pi 3
Adafruit 7" 800x480 HDMI Backpack
USB Microphone
Auxiliary Speaker
```

### Software

```
Alexa Voice Services (AVS)
Qt Creator
PyQt5
```

## Alexa Environment

For Dylan <3

## GUI Environment

Our group used [PyQt](https://wiki.python.org/moin/PyQt) and Qt Creator to produce the Graphical User Interface for our alarm clock. By using QtCreator to set the intitial UI design of the application, we were able to quickly initialize any widgets needed. We chose PyQt over Qt5.12(C++) due to the ease of use when delpoying Python3 based code on the Raspberry Pi. In doing so, we avoided any cross compling errors when working between OSX and Raspian Jessie OS. 

Below are the packages and dependencies needed to get your own Smart Alarm up and running.

First, if on OSX, use [homebrew](https://brew.sh/) to install required packages:
```
brew install python3
brew install qt5
brew install pyqt5
```
Now, on the machine you are developing on, download [QTCreator](https://www.qt.io/download) to begin creating the UI of the Smart Alarm Clock:
```
Qt Creator Example
```
After editing the .ui file, simply run the following command to convert the .ui file into a python class that initializes the MainWindow object of your GUI as well as any widgets declared from Qt Creator:
```
pyuic5 mainwindow.ui > mainwindow_auto.py
```
As a debug step, I often ran the GUI code on my personal machine to preview any functionalities I implemented. To do so, create a main.py file to run the PyQt application
```
Create main.py. SHOW SIMPLE CODE FOR THIS
```
Let's recap. Your project folder should contain the following files (we can ignore the .cpp and .h extensions). Transport the following files from your development machine to the Raspberry Pi:
```
|__Project_Directory
   |__main.py
   |__mainwindow.ui
   |__mainwindow_auto.py
```
Finally, on your Raspberry Pi, use the apt-get command to download the packages needed to display your new GUI:
```
sudo apt-get install python3
sudo apt-get install python3-pyqt5
```








## Original README 

You can use the [editor on GitHub](https://github.com/Dverstandig/4180-Smart-Alarm-Clock/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/Dverstandig/4180-Smart-Alarm-Clock/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
