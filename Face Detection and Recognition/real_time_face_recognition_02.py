import cv2
import face_recognition
import pickle
import os


DATA_FILE = "faces.pkl"


known_face_encodings = []
known_face_names = []

if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
    with open(DATA_FILE, "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)
    print(f"[INFO] Loaded {len(known_face_names)} known face(s).")
else:
    print("[INFO] No known faces found. Starting fresh...")


video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

       
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 1)

    
    cv2.imshow("Face Recognition", frame)

    # Press "s" to save a new face
    key = cv2.waitKey(1)
    if key == ord("s"):
        new_name = input("Enter name for this face: ").strip()
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(new_name)
            with open(DATA_FILE, "wb") as f:
                pickle.dump((known_face_encodings, known_face_names), f)
            print(f"[INFO] Saved new face: {new_name}")
        else:
            print("[WARNING] No face detected to save.")

    # Press "q" to quit
    elif key == ord("q"):
        break


video_capture.release()
cv2.destroyAllWindows()
