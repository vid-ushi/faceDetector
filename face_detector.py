import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import dlib


class FaceDetector:
    def __init__(self, master):
        self.master = master
        master.title("Face Detector")
        master.configure(bg='#404252')

        self.detector = dlib.get_frontal_face_detector()

        self.frame = tk.Frame(master, bg='#404252')
        self.frame.pack(pady=20)

        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg='white', highlightthickness=0, bd=4,
                                relief='groove')
        self.canvas.pack(pady=10)

        style = ttk.Style()
        style.configure('Custom.TButton', padding=10, relief='flat', background='#c1c1c1', foreground='#404252',
                        font=('Segoe UI', 12))

        self.camera_button = ttk.Button(master, text="Video Camera", command=self.video_camera, style='Custom.TButton')
        self.camera_button.pack(pady=10)

        self.upload_button = ttk.Button(master, text="Upload Video", command=self.upload_video, style='Custom.TButton')
        self.upload_button.pack(pady=10)

        self.cap = None

        # Bind function to handle window close event
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Release video capture if active
        if self.cap is not None:
            self.cap.release()
        # Close the Tkinter application
        self.master.destroy()

    def video_camera(self):
        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(0)  # Video capture from default camera (change index if needed)
        self.detect_faces()

    def upload_video(self):
        if self.cap is not None:
            self.cap.release()

        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])  # Use filedialog directly
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.detect_faces_resized()

    def detect_faces(self):
        if self.cap is None or not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open video source!")
            return

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            # Horizontally flip the frame
            frame = cv2.flip(frame, 1)

            # Convert the frame to grayscale for dlib face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces using dlib
            faces = self.detector(gray)

            # Draw rectangles around detected faces
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Convert the frame back to RGB for display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame
            self.photo = self.convert_to_tkimage(frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.master.update()

        self.cap.release()

    def detect_faces_resized(self):
        if self.cap is None or not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open video source!")
            return

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            # Resize frame while maintaining aspect ratio to fit within 400x400
            h, w = frame.shape[:2]
            if h > w:
                new_h = 400
                new_w = int(w * (new_h / h))
            else:
                new_w = 400
                new_h = int(h * (new_w / w))
            frame_resized = cv2.resize(frame, (new_w, new_h))

            # Horizontally flip the frame
            frame_resized = cv2.flip(frame_resized, 1)

            # Convert the frame to grayscale for dlib face detection
            gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

            # Detect faces using dlib
            faces = self.detector(gray)

            # Draw rectangles around detected faces
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Convert the frame back to RGB for display
            frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Display the frame
            self.photo = self.convert_to_tkimage(frame_resized)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.master.update()

        self.cap.release()

    def convert_to_tkimage(self, frame):
        return PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))


root = tk.Tk()
app = FaceDetector(root)
root.geometry("500x600")
root.resizable(width=False, height=False)
root.mainloop()