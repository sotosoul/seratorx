# Seratorx

A collection of utilities for your Serato DJ library. Designed for professional DJs using Serato DJ Pro or Lite. Can be used on both Windows and macOS systems.

_Seratorx_ is a portmanteau of Serato and Torx, the hexagonal screwdriver type. In other words, Seratorx is a tool that can be used by DJs to manage their Serato DJ library.

I've been working as a professional DJ since circa 2003. Still a high-school student, I remember burning audio CDs, preparing labels, writing info like BPM and maybe some asterisks to indicate my favourites, and carrying them around in heavy CD carrying cases, typically produced by manufacturers like Case Logic. I started using Serato Scratch Live (SSL) back in 2012 in an attempt to move away from this hassle. I was impressed by the timecode technique. As time went by, I became a proficient user of SSL and, later, Serato DJ Pro. One thing that never impressed me, however, is the library management, as there were functionalities that I've always wanted but were missing.

## Setting up your Serato DJ library

I have read a lot and I have watched several YouTube videos about how to best organize my Serato library. I won't go into details, however, there's one cardinal rule no DJ should ever ignore if they're using Serato software: never organize your DJ music on the filesystem, i.e., using folders and subfolders. Instead, place all your audio files (mp3) into a folder, import them to Serato DJ, and organize your music from within Serato using crates, subcrates, and smart crates. _Maybe_ some exceptional cases can justify keeping your mp3s in multiple folders; even then, it's doubtful whether such a system can remain effective and efficient in the long run.

In short, **one directory** (such as `/Users/my_username/Music/Serato`) **containing all the audio files and no subfolders**.

## Get started

Have a look at the `start_here.py` file to get an idea of what you can do with Seratorx.

_Note: I'm using the decoding functions available on the repo of [sharst](https://github.com/sharst)._
