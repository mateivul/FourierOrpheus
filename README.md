# FourierOrpheus

This is a animation I made in python with the Manim library. It draws the **h** from the Hack Club logo with different number of rotating circles and at the end shows the Orpheus flag.

## Development journey / how it works

First I downloaded the svg and png logos form the HackClub branding page. Then made a script to extract dots alsong the h's outline form the svg path data. Then I inserted the dots into a Fourier transform which gives back the size, speed, and starting agnle of each cirlce. Then using Manim I animated the circles starting with 5 and reaching 80, with a special animation for the last phase and Orpheus showing up.

### if you want to run locally:

**on mac**:

```
brew install ffmpeg cario pango pkg-config
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cd src && manim -pqh main.py FourierOrpheus
```

**on windows**:

```
winget install Gyan.FFmpeg
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
manim -pqh main.py FourierOrpheus
```

Output animation will be in `src/media/videos/main/1080p60`
