# Face-Recognition-Attendance
Attendance tracking app that will recognize when a registered student has entered frame. This project can be used in schools, universities, the corporate world, and many other applications to ensure participants are showing up for school or work.

Uses OpenCV, FaceRecognition, and MongoDB to store user's face as well as time registered. Then checks user photo to see if a similar photo is registered in database. If it is not, then the script will prompt the user to enter a username which will be used as the student's ID. If it is registered, then the user will be notified that the student is already registered.

## Usage:
- Check attendance:
    Will run `face_match.py` to verify the students that show up to class and are registered within the database
- Add faces:
    Will run `add_faces.py` to allow users to get registered within the database

## Installing DLib on Windows Machines (Python 3.7-3.10)
DLib is a machine learning module that is required for Face Recognition to work. It can be downloaded from the following [link](https://github.com/Cool-PY/Python-Dlib-Repository/blob/main/dlib-19.22.99-cp310-cp310-win_amd64.whl).
After the file has been downloaded, go to the command prompt and enter the following command: `cd DIRECTORY_OF_DOWNLOADED_DLIB`. Once that has been completed, enter the command: `pip uninstall dlib`
Finally, enter: `pip install dlib-19.22.99-cp310-cp310-win_amd64.whl`

## Installing Necessary Packages:
- OpenCV (CV2) - Image processing library used to take user's picture and monitor users entering room: `pip install opencv-python`
- Face Recognition - Facial recognition library used to determine if a user matches with database: `pip install face-recognition`
- Numpy - Matrix processing library needed to find images as matrix values: `pip install numpy`