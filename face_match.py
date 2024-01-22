import face_recognition
import cv2
import os
import numpy as np
import mysql.connector
from datetime import date, datetime

# Directory as to where user photos are currently stored
DIR = 'C:\\Users\\tocar\\Documents\\Code\\AttendanceSystem\\Face-Recognition-Attendance\\data'
tdy = date.today().strftime('%m_%d_%Y')
tme = str(datetime.now().strftime("%H:%M:%S"))

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="known_faces",
    auth_plugin='mysql_native_password'
    )

my_cursor = db.cursor()
my_cursor.execute('Show TABLES LIKE %s', (tdy,))
result = my_cursor.fetchone()

if result is None:
    my_cursor.execute(f'CREATE TABLE {tdy} (name VARCHAR(20), time VARCHAR(15))')
    db.commit()

my_cursor.close()
cam = cv2.VideoCapture(0)

known_face_encodings = []
known_names = [] # array of all user names

# Loads all pictures from DIR
for image in os.listdir(DIR):
    img = face_recognition.load_image_file('data\\' + image)
    known_face_encodings.append(face_recognition.face_encodings(img)[0])
    known_names.append(image[:-4:])

face_locations = []
face_encodings = [] # Encodings of all the new faces, will be used to match with known_face_encodings
names = []
process_frame = True

while True:
    ret, frame = cam.read()

    if process_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

            names.append(name)

            if len(names) > 0:
                my_cursor = db.cursor()

                for name in names:
                    my_cursor.execute(f'SELECT * FROM {tdy} WHERE name = %s', (name,))
                    result = my_cursor.fetchone()

                    if result is None:
                        sql = f"INSERT INTO {tdy} (name, time) VALUES (%s, %s)"
                        val = (name, tme)
                        my_cursor.execute(sql, val)
                        db.commit()

    process_frame = not process_frame
    for (top, right, bottom, left), name in zip(face_locations, names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cam.release()
cv2.destroyAllWindows()