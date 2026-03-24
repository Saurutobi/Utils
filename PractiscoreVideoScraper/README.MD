# Selenium scraper to get match data

requires >= python 3.10 

1. Install requirements with <code>pip3 install -r requirements.txt</code>
2. Download the match data and put in localfile
3. Run with <code>python PractiscoreVideoScraper_localfile.py [firstName] [lastName] [marcelprint=true, donprint=false]</code>

# HowTo
open up the match, inspect, first file at around 1500-1800 lines of code is the json blob for all 3 files. grab that separate it put it in the files then run the above

# using psScraper_web.py,
1. Run with <code>python psScraper_web.py [results url]</code>