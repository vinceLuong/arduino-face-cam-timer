import cv2
import face_recognition
import numpy as np
import time

import serial


def stop_timer(ser: serial.Serial):
    ser.write(b'x')


def start_timer(ser: serial.Serial):
    ser.write(b'v')


def read_faces(frame):
    """
    Locate the faces of the frame(image) and identify who each person is.

    :param frame: np.ndarray, 2D array of RGB values of the frame/image
    :return: face_names (List), face_locations(List)
        Returns a list of the faces recognized and a list of the (x,y) co-ordinates of where in the image it is located
    """
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/x size for faster face recognition processing
    scaling_factor = 2
    small_frame = cv2.resize(frame, (0, 0), fx=1 / scaling_factor, fy=1 / scaling_factor)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # dont process all frame, only every frame_skip_count'th frame to save time
    if frame_count % frame_skip_count == 0:
        curr_time = time.time()
        if len(processing_times) > 0:
            print("Time since last face check: ", curr_time - processing_times[-1])
        processing_times.append(curr_time)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

            face_names.append(name)

    return face_names, face_locations


if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    vincent_image = face_recognition.load_image_file("images/vincent.jpg")
    vincent_encoding = face_recognition.face_encodings(vincent_image)[0]

    # Load a sample picture and learn how to recognize it.
    #vincent_image2 = face_recognition.load_image_file("images/vincent2.jpg")
    #vincent_encoding2 = face_recognition.face_encodings(vincent_image)[0]

    # Load a sample picture and learn how to recognize it.
    #vincent_image3 = face_recognition.load_image_file("images/vincent3.jpg")
    #vincent_encoding3 = face_recognition.face_encodings(vincent_image)[0]

    # Load a sample picture and learn how to recognize it.
    #raymond_image = face_recognition.load_image_file("images/raymond.png")
    #raymond_encoding = face_recognition.face_encodings(raymond_image)[0]

    #known_encodings = [vincent_encoding, vincent_encoding2, vincent_encoding3, raymond_encoding]
    #known_names = ["Vincent", "Vincent", "Vincent", "Raymond"]

    known_encodings = [vincent_encoding]
    known_names = ["Vincent"]

    last_results = [None] * 10

    frame_count = 0
    frame_skip_count = 4

    processing_times = []

    arduino_timer_ind = False
    reset_counter = 0
    no_vincent_counter = 0
    nothing_counter = 0
    not_vincent_counter = 0

    # TODO: Remove these debugging/testing variables
    scaling_factor = 2

    ser = serial.Serial('COM3', baudrate=9600, timeout=1)
    stop_timer(ser)
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        if frame_count % frame_skip_count == 0:
            face_names, face_locations = read_faces(frame)

            if "Vincent" in face_names:
                print("Vincent!")
            elif len(face_names) != 0:
                print("Raymond?!?")
                not_vincent_counter = not_vincent_counter + 1
            else:
                print("Nothing D:")
                nothing_counter = nothing_counter + 1

            # store the latest result in the last_results
            if "Vincent" in face_names:
                last_results[ int((frame_count / frame_skip_count) % len(last_results)) ] = "Vincent"
            else:
                last_results[ int((frame_count / frame_skip_count) % len(last_results)) ] = "Nope"
                no_vincent_counter = no_vincent_counter + 1

            # check if Vincent has been missing for a while (aka he left)
            if "Vincent" not in last_results:
                print("Vincent left!")
                reset_counter = reset_counter + 1

                if arduino_timer_ind is True:
                    stop_timer(ser)
                    arduino_timer_ind = False
            else:
                if arduino_timer_ind is False:
                    arduino_timer_ind = True
                    start_timer(ser)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= scaling_factor
                right *= scaling_factor
                bottom *= scaling_factor
                left *= scaling_factor

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        frame_count = frame_count + 1

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Frames: ", frame_count, frame_count / 4)
            print("Reset Counter: ", reset_counter)
            print("Not Vincents: ", not_vincent_counter)
            print("Nothings: ", nothing_counter)

            print("No Vincent Results in last_results: ", no_vincent_counter)
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
