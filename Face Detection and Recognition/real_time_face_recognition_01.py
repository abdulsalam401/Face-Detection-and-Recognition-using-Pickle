# import cv2
# import face_recognition  
# import os

# # Load known face(s)
# known_face_encodings = []
# known_face_names = []

# # Folder containing known faces (e.g., "known_faces/abdul salam.jpg")
# known_faces_dir = 'known_faces'

# for filename in os.listdir(known_faces_dir):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         path = os.path.join(known_faces_dir, filename)
#         image = face_recognition.load_image_file(path)
#         encodings = face_recognition.face_encodings(image)

#         if len(encodings) > 0:
#             known_face_encodings.append(encodings[0])
#             name = os.path.splitext(filename)[0]
#             known_face_names.append(name)
#         else:
#             print(f"No face found in {filename}")

# # Start webcam
# video_capture = cv2.VideoCapture(0)

# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         break

#     # Resize frame for faster processing
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#     # Detect face locations
#     face_locations = face_recognition.face_locations(rgb_small_frame)

#     # Skip frame if no face
#     if len(face_locations) == 0:
#         cv2.imshow('Video', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         continue

#     # Get face encodings
#     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#     face_names = []

#     for face_encoding in face_encodings:
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         name = "Unknown"

#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#         if len(face_distances) > 0:
#             best_match_index = face_distances.argmin()
#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]

#         face_names.append(name)

#     # Draw results on original frame
#     for (top, right, bottom, left), name in zip(face_locations, face_names):
#         # Scale back up face locations
#         top *= 4
#         right *= 4
#         bottom *= 4
#         left *= 4

#         # Draw rectangle and name
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#         cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
#         cv2.putText(frame, f"This is {name}", (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

#     # Display the result
#     cv2.imshow('Video', frame)

#     # Exit on 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Cleanup
# video_capture.release()
# cv2.destroyAllWindows()


"""Second try """

import cv2
import face_recognition
import os

# Load known faces ONCE (outside the loop)
known_face_encodings = []
known_face_names = []

known_faces_dir = 'known_faces'
for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        
        if encodings:  # If at least one face is found
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Process only every 2nd frame (speeds up processing)
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Downscale frame for faster processing (1/4th size)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Only process every other frame
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                best_match_index = matches.index(True)
                name = known_face_names[best_match_index]
            face_names.append(name)

    process_this_frame = not process_this_frame  # Toggle frame processing

    # Display results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up to original size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


"""third try"""

# import cv2
# import face_recognition
# import os
# import threading

# # Load known faces in the background (to avoid startup delay)
# def load_known_faces():
#     global known_face_encodings, known_face_names
#     known_face_encodings = []
#     known_face_names = []
    
#     known_faces_dir = 'known_faces'
#     for filename in os.listdir(known_faces_dir):
#         if filename.lower().endswith((".jpg", ".png")):
#             path = os.path.join(known_faces_dir, filename)
#             image = face_recognition.load_image_file(path)
#             encodings = face_recognition.face_encodings(image)
#             if encodings:
#                 known_face_encodings.append(encodings[0])
#                 known_face_names.append(os.path.splitext(filename)[0])

# # Start loading known faces in a separate thread
# thread = threading.Thread(target=load_known_faces)
# thread.daemon = True  # Allows the thread to exit when the main program exits
# thread.start()

# # Initialize webcam (show feed immediately)
# video_capture = cv2.VideoCapture(0)

# # Main loop
# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         break

#     # Display raw webcam feed instantly
#     cv2.imshow('Video', frame)

#     # Check if known faces are loaded
#     if 'known_face_encodings' in globals():
#         # Process faces (same as before, but now it runs after the webcam starts)
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#         rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             name = "Unknown"
            
#             if True in matches:
#                 name = known_face_names[matches.index(True)]
            
#             # Scale back up and draw
#             top *= 4; right *= 4; bottom *= 4; left *= 4
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#             cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
#         # Update the displayed frame with face detection
#         cv2.imshow('Video', frame)

#     # Exit on 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video_capture.release()
# cv2.destroyAllWindows()