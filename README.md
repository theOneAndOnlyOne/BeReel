<a name="readme-top"></a>

![Welcome Screen](https://github.com/theOneAndOnlyOne/BeReel/blob/main/static/images/BeReal_Header.png)

# BeReel:

Miss the Timelapse Recap feature from ReReal? Introducing BeReel. A Flask-based webtool that gives you a customized timelapse of your favourite BeReal memories. 

![Video Settings](https://github.com/theOneAndOnlyOne/BeReel/blob/main/static/images/BeReel_Video_Settings.png)


* Implements a BeReal API to fetch user memories in a usable format
* Fetch Memories at a specified date range
* Renders using many open source libraries and fully customizable (with many features to come
* Create a timelapsed that syncs with the .WAV audio

## Getting Started

Follow these instructions to get your project up and running.

### Prerequisites

Make sure you have the following installed on your machine:

- [Python](https://www.python.org/downloads/) (<b>Only compatible with version 3.11</b>)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [ffmpeg](https://ffmpeg.org/download.html)

### Installing Dependencies

Run all required libraries and run the app:
```bash
pip install -r requirements.txt --user
python main.py
```
The Flask app will be available on [http://localhost:5000/](http://localhost:5000/). Multiple folders will be created to pull all image data from your memories

### Project Structure

- main.py: Main flask app and drives webpage and API requests
- combineImages.py: processes photos to be used for the slideshow
- generateSlideshow.py: rendering timelapse video and audio

### Current Developments

- [ ] Add 'no sound' option
- [ ] Display RealMoji
- [ ] Toggle Date Label setting
- [ ] Show render progress from terminal->webpage

## Remarks

This project wouldn't be here without the amazing work by [chemokita13](https://github.com/chemokita13/beReal-api). Please give him a star.

This app is to be run <b>locally</b> as to comply with user security laws and privacy. Under no cases does this app store metadata elsewhere.
The app utilizes this third-party API which may not be following terms set by BeReal, all videos and images produced from this app is to be considered personal use and should only use accounts owned by the user: 
If the company has particular issues, please submit a request via links in my profile.

## Privacy Policy

BeReel was developed as an open-source app and gathers information from an unofficial BeReal API from chemokita13. BeReel has no association and responsibility with the API's development and how it accesses user information. See this [link](https://github.com/chemokita13/beReal-api) for more information about this API Project. This app is to be run <b>locally</b> as to comply with user security laws and privacy. Under no cases does this app store metadata elsewhere and all related images to develop the timelapse can be found in local folders labelled /primary /secondary /combined /static. All videos and images produced from this app is to be considered personal use and should only use accounts owned by the user.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Buy Me A Coffee!

You like the work here? Feel free to buy me a coffee by following this [link](https://www.buymeacoffee.com/theoneandonlyone)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
