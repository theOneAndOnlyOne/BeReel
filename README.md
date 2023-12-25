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

- [Python](https://www.python.org/downloads/) (Only compatible with versions <3.12)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installing Dependencies

Run all required libraries and run the app:
```bash
pip install -r requirements.txt
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

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
