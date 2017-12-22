# LectureHelper

Description:
-----------

This program is designed to help Coursera students to see video lectures in text format. It
combines 1-minute screenshots of lecture videos with subtitles file to produce textual
representation of the lecture.

Installation:
------------

This program is written using Python 2.7
In order to run this program, 2 additional products are required.
1) A program implementing TextEdit algorithm:
https://github.com/davidadamojr/TextRank
Just follow the instructions, and it will guide to install all its dependencies.
2) A program for processing video file and converting it to 1-minute slides:
https://ffmpeg.org/

Preparation:
-----------

Before you start this program you need to download Coursera material. You can download
lectures from Coursera by hand or using other tools. When you are downloading please
maintain the following structure:

CourseraRootDirectory
          |________Lecture1.1
                     |_______index.mp4
                     |_______subtitle.txt
                     |_______subtitles.vtt
          |________Lecture1.1
                     |_______index.mp4
                     |_______subtitle.txt
                     |_______subtitles.vtt
          .
          .
          .
          |________Lecture12.1
                     |_______index.mp4
                     |_______subtitle.txt
                     |_______subtitles.vtt
          |________Lecture12.2
                     |_______index.mp4
                     |_______subtitle.txt
                     |_______subtitles.vtt
You can download one or more or all lectures.

Configuration:
--------------

This program needs to be configured by adding proper fields to config.py file.
courseradir: enter absolute path to CourseraRootDirectory from above.
lecturedir: enter absolute path to output directory.
ffmpegdir:directory where ffmpeg executable is located


What happens inside the program:
-------------------------------

For each lesson, the program uses TextRank program with subtitle.txt
input to create file’s summary and a list of keywords.
After this ffmpeg program is called on each lecture’s .mp4 file to
produce video images (slides) at 1-minute intervals.
Later subtitles.vtt file is combine with slides for this lesson to
produce and integrated file.

Output:
-------

The output index file is located at the following place:

OutputDirectory
        |__________images
        |__________lectures
                        |______Lectures.html
                        |______Lecture1.1
                        |______Lecture1.2
                        .
                        .
                        .

To execute:
----------

python lecture.py
