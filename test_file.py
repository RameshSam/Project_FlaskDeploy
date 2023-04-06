import cv2 , face_recognition , numpy as np , pyodbc , sqlite3
from models import database , Person_Details , Session

# mydb = sqlite3.connect("test_mydb.db")
# cursor = mydb.cursor()
s = Session()


video_capture = cv2.VideoCapture(0)

cv2.namedWindow("Camera Feed")

reg = 3211
name = "Sam"
email = "Josarun1601@gmail.com"
password = 2121

p = Person_Details(reg , name , email ,password )
s.add(p)
s.commit()

while True:
    # Capture a frame from the video feed
    ret, frame = video_capture.read()

    # Resize the frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Display the frame in the window
    cv2.imshow(' Interface ', small_frame)

    # Check if the user has clicked on the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        # User has clicked on the window, so capture the current frame
        rgb_small_frame = small_frame[:, :, ::-1]  # Convert from BGR to RGB

        # Encode the image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', rgb_small_frame)

        # Detect faces in the image
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Insert the image data, filename, and ID into the database
        Image_data = pyodbc.Binary(img_encoded)
        # img_filename = input("Enter the name for the image file: ")

        if len(face_encodings) > 0:

            encode_data  =  face_encodings[0].tobytes()
            database(p , name ,Image_data ,encode_data )

            # sql  = "INSERT INTO images (name, encoding, image) VALUES (?, ?, ?)"
            # val  =  ( img_filename , face_encodings[0].tobytes() , img_data )
            # cursor.execute(sql , val)
            # mydb.commit()
        else:
            print("No face detected in the image.")

        break

# Release the camera and database connection
video_capture.release()
# cursor.close()
# mydb.close()
cv2.destroyAllWindows()
