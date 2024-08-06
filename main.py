import os
import requests
from flask import Flask, render_template, request, jsonify
from combineImages import create_images
from generateSlideshow import buildSlideshow
from recap import butidRecap
from datetime import datetime

app = Flask(__name__, template_folder="templates")


# Acquire Phone Number from User
def send_code(phone):
    print("> Entered phone number is ", phone)
    # First Post to send out OTP session and code
    url_send_code = "https://berealapi.fly.dev/login/send-code"

    # IMPORTANT: Format must be +##########
    payload = {"phone": phone}

    print("-- Sending OTP Session Request --")
    response = requests.post(url_send_code, json=payload)
    otp_session = "n/a"

    if response.status_code == 201:
        print("> Request successful!")
        print("Response:", response.json())
        response_json = response.json()
        if "data" in response_json and "otpSession" in response_json["data"]:
            otp_session = response_json["data"]["otpSession"]["sessionInfo"]
            print("OTP Session:", otp_session)
        else:
            print("No 'otpSession' found in the response.")
    else:
        print("Request failed with status code:", response.status_code)
        print(response.json())

    return otp_session


# Verify Session using otp_session code and user entered otp_code recieved from phone notification
def verify(otp_session, otp_code):
    # print("please enter OTP code")
    # otp_code = input()
    print("> OTP: ", otp_code)

    # Second POST request to verify base don user input
    url_verify = "https://berealapi.fly.dev/login/verify"

    payload_verify = {"code": otp_code, "otpSession": otp_session}

    print("-- Sending Verify Request --")
    print(payload_verify)
    response_verify = requests.post(url_verify, json=payload_verify)
    tokenObj = "n/a"

    if response_verify.status_code == 201:
        print("> Verification request successful!")
        print("Response:", response_verify.json())
        # Process the verification response if needed
        response_json = response_verify.json()
        if "data" in response_json and "token" in response_json["data"]:
            tokenObj = response_json["data"]["token"]
            print("tokenObj:", tokenObj)
        else:
            print("No 'tokenObj' found in the response.")
            exit()
    else:
        print(
            "> Verification request failed with status code:",
            response_verify.status_code,
        )
        print(response_verify.json())
        exit()

    return tokenObj


# Fetch user memories. Skip to this stage if we already acquired reusable token
def get_memories(tokenObj, start_date_range, end_date_range):
    url_mem_feed = "https://berealapi.fly.dev/friends/mem-feed"
    headers = {"token": tokenObj}

    # Create a folder named 'primary' if it doesn't exist
    folder_name = "primary"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create a folder named 'secondary' if it doesn't exist
    secondary_folder_name = "secondary"
    if not os.path.exists(secondary_folder_name):
        os.makedirs(secondary_folder_name)

    print("-- Sending Get Memories Request --")
    response_mem_feed = requests.get(url_mem_feed, headers=headers)
    data_array = []

    if response_mem_feed.status_code == 200:
        print("> GET request successful!")
        # Process the response from mem-feed endpoint
        print("Response:", response_mem_feed.json())
        print("we did it yay")
        response_data = response_mem_feed.json().get("data", {})
        data_array = response_data.get("data", [])

    else:
        print("GET request failed with status code:", response_mem_feed.status_code)

    start_date_str = str(start_date_range)
    end_date_str = str(end_date_range)
    # Convert the input strings to datetime objects
    start_date_object = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date_object = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Iterate through the 'data' array and download images
    for item in data_array:
        image_url = item["mainPostPrimaryMedia"].get("url", "")
        secondary_image_url = item["mainPostSecondaryMedia"].get("url", "")
        date = item["memoryDay"]
        date_object = datetime.strptime(date, "%Y-%m-%d")

        if image_url and start_date_object <= date_object <= end_date_object:
            # Extracting the image name from the URL
            image_name = date + "_" + image_url.split("/")[-1]
            # Downloading the image
            image_path = os.path.join(folder_name, image_name)
            with open(image_path, "wb") as img_file:
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    img_file.write(img_response.content)
                    print(f"Downloaded {image_name} to {folder_name}")
                else:
                    print(f"Failed to download {image_name}")
        if secondary_image_url and start_date_object <= date_object <= end_date_object:
            # Extracting the image name from the URL
            image_name = date + "_" + secondary_image_url.split("/")[-1]
            # Downloading the image
            image_path = os.path.join(secondary_folder_name, image_name)
            with open(image_path, "wb") as img_file:
                img_response = requests.get(secondary_image_url)
                if img_response.status_code == 200:
                    img_file.write(img_response.content)
                    print(f"Downloaded {image_name} to {secondary_folder_name}")
                else:
                    print(f"Failed to download {image_name}")

    return "complete"


# All images referenced in the 'primary' URLs should now be saved in the 'primary' folder
# 'secondary' URLS saved in 'secondary', etc.


# -------------------------------------------------------------------------------------------------------------------------
# Flask App Routing


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        otp_session = send_code(phone_number)

        if otp_session != "n/a":
            return render_template("verify.html", otp_session=otp_session)

        return render_template(
            "index.html",
            message="Invalid phone number. Check formatting and Please try again.",
        )

    return render_template("index.html")


@app.route("/verify", methods=["POST"])
def verify_code():
    if request.method == "POST":
        user_code = request.form["verification_code"]
        otp_session = request.form["otp_session"]
        print("> verify_code otp_session: ", otp_session)
        tokenObj = verify(otp_session, user_code)

        if tokenObj != "n/a":
            return render_template("process.html", tokenObj=tokenObj)

        else:
            return render_template("failure.html")
        # return render_template('verify.html', tokenObj='n/a', message='Invalid verification code. Please try again.')

    return render_template("verify.html")


@app.route("/process", methods=["POST"])
def process_data():
    if request.method == "POST":
        start_date_range = request.form["start_date_range"]
        end_date_range = request.form["end_date_range"]
        wav_file = request.files["wav_file"]
        tokenObj = request.form["tokenObj"]
        mode = request.form.get("mode")

        print("> HTML Form Elements: ")
        print("start_date_range ", str(start_date_range))
        print("end_date_range ", str(end_date_range))
        print("wav_file ", str(wav_file))
        print("mode", str(mode))
        # Call get_memories function

        print("> donwloading music file locally: ")
        try:
            # Save the uploaded WAV file locally
            upload_directory = os.getcwd()
            print("saving file to ", upload_directory)
            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            wav_file.save(os.path.join(upload_directory, "curr_song.wav"))

        except Exception as e:
            print(f"Error in processing data: {str(e)}")

        result = " "
        if not os.path.exists("primary") or not os.path.exists("secondary"):
            print("> downloading images locally")
            result = get_memories(tokenObj, start_date_range, end_date_range)

        if result != "n/a":
            # Execute the Python functions
            create_images()  # process images and apply effects
            # do something with current page here
            buildSlideshow(mode)  # assemble files and load audio
            # do something with current page here
            return render_template("preview.html")
        else:
            return render_template("failure.html")

    return render_template("process.html")


@app.route("/recap", methods=["POST"])
def recap():
    if request.method == "POST":
        start_date_range = "2023-01-01"
        end_date_range = "2023-12-31"
        tokenObj = request.form["tokenObj"]

        # check if a folder called 'primary' exists and 'secondary' exists

        result = " "
        if not os.path.exists("primary") or not os.path.exists("secondary"):
            print("> downloading images locally")
            result = get_memories(tokenObj, start_date_range, end_date_range)

        if result != "n/a":
            # Execute the Python functions
            create_images()  # process images and apply effects
            # do something with current page here
            butidRecap()  # assemble files and load audio
            # do something with current page here
            return render_template("preview.html")
        else:
            return render_template("failure.html")

    return render_template("process.html")


# @app.route('/run-python-functions', methods=['POST'])
# def run_python_functions():
#    try:
#        # Execute the Python functions
#        create_images() # process images and apply effects
#        buildSlideshow() # assemble files and load audio
#
#        return render_template('preview.html') # Success! redirect to preview page
#
#    except Exception as e:
#        # Return a JSON response indicating failure
#        return render_template('failure.html', message=str(e)) # Failure! redirect to failure page


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/preview")
def preview():
    return render_template("preview.html")


@app.route("/failure")
def failure():
    return render_template("failure.html")


if __name__ == "__main__":
    app.run(debug=True)

# otp_session = send_code()
# tokenObj = verify(otp_session)
# get_memories(tokenObj)
# create_images()
# buildSlideshow()
