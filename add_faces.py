# Check if face already exists in DIR
# If it doesn't, then add face to DIR
# If it does, ignore and move on to next face in img

import cv2
import numpy as np
import os
import shutil
import face_recognition

DIR = 'C:\\Users\\tocar\\Documents\\Code\\AttendanceSystem\\Face-Recognition-Attendance\\data'
CURRENT_DIR = 'C:\\Users\\tocar\\Documents\\Code\\AttendanceSystem\\Face-Recognition-Attendance\\'
dir_size = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print(os.listdir(DIR))

cam = cv2.VideoCapture(0)

known_face_encodings = []

# Loads all pictures from DIR
for image in os.listdir(DIR):
    img = face_recognition.load_image_file('data\\' + image)
    known_face_encodings.append(face_recognition.face_encodings(img)[0])

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
            if dir_size != 0:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                # Checks to see if face exists in DIR
                if matches[best_match_index]:
                    print('User already added to database. Try again with a different user')
                else:
                    username = input('Enter username: ')
                    cv2.imwrite(username + '.jpg', small_frame)
                    # Moves img into data directory
                    shutil.move(CURRENT_DIR + username + '.jpg', DIR + '\\' + username + '.jpg')
                    img = face_recognition.load_image_file('data\\'+ username + '.jpg')
                    face_encodings.append(face_recognition.face_encodings(img[0]))
                    print('Image: ' + username + '.jpg has been added to ' + DIR)
                    dir_size += 1
                    
            else:
                username = input('Enter username: ')
                cv2.imwrite(username + '.jpg', small_frame)
                # Moves img into data directory
                shutil.move(CURRENT_DIR + username + '.jpg', DIR + '\\' + username + '.jpg')
                img = face_recognition.load_image_file('data\\'+ username + '.jpg')
                face_encodings.append(face_recognition.face_encodings(img[0]))
                print('Image: ' + username + '.jpg has been added to ' + DIR)
                dir_size += 1            
                    

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cam.release()
cv2.destroyAllWindows()