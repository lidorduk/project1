import os
import cv2
import pytesseract
import socket
import serial
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
path_of_car = '5.jpg'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_license_plate = "4762911"
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

def Detect_car():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    f.close()

    img = cv2.imread(path_of_car)
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 2:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                return True
    return False
    """
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 2)
    cv2.imshow("Image", img)
    """

def license_plate_recognition():
    foreign_car_license_plate = ""
    # Load the image
    img = cv2.imread(path_of_car)

    # Convert the image to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Apply bilateral filter to remove noise
    blur = cv2.bilateralFilter(gray, 11, 17, 17)

    # Detect edges using Canny edge detection
    edged = cv2.Canny(blur, 30, 200)

    # Find contours in the image
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    # Initialize the license plate contour
    license_plate = None

    # Loop over the contours
    for contour in contours:
        # Approximate the contour to a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # If the polygon has four vertices, then it could be a license plate
        if len(approx) == 4:
            # Calculate the bounding box of the polygon
            x, y, w, h = cv2.boundingRect(approx)

            # Check if the bounding box has the aspect ratio of a license plate
            aspect_ratio = w / float(h)
            if aspect_ratio >= 2.5 and aspect_ratio <= 5.0:
                license_plate = gray[y:y + h, x:x + w]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                image_rgb = cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB)
                cv2.imshow("License Plate", image_rgb)
                custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --user-words israeli_number_plate_words.txt'
                text = pytesseract.image_to_string(license_plate, config=custom_config)
                text = text[:len(text) - 1]
                cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
                cv2.imshow("License Plate Detection", img)
                print("License Plate :", text)
                if text == my_license_plate:
                    return (True , None , None)
                else:
                    foreign_car_license_plate = text
                    cv2.imwrite("license_plate.jpg", image_rgb)
                break
    if os.path.exists("license_plate.jpg"):
        return (False , foreign_car_license_plate , "license_plate.jpg")

    # Show the detected license plate
    """
    image_rgb = cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB)
    cv2.imshow("License Plate", image_rgb)
    cv2.imshow("License Plate Detection", img)
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --user-words israeli_number_plate_words.txt'
    text = pytesseract.image_to_string(license_plate , config= custom_config)
    print("License Plate :", text)
    """

def start_session_with_server(message_to_server , path_of_msg):
    flag = False
    client.connect(('localhost', 12345))
    client.send(message_to_server.encode())
    file = open(path_of_msg , 'rb')
    image_data = file.read(2048)
    while image_data:
        client.send(image_data)
        image_data = file.read(2048)
    file.close()
    data = client.recv(2048).decode()
    if not data:
        # if data is not received break
        print("The information is lost")
    str_data = str(data)
    if str_data == "yes":
        flag = True
    client.close()
    print("client end session")
    os.remove("license_plate.jpg")
    return flag

def Get_distance():
    ser1 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)#esp32
    ser1.reset_input_buffer()
    while True:
        if ser1.in_waiting > 0:
            line1 = ser1.readline().decode('utf-8').rstrip()
            converted_num = int(line1)
            print(converted_num)
            if converted_num > 240:
                print("Ok")
            elif converted_num < 100:
                flag_detect_car = Detect_car()
                if flag_detect_car:
                    (flag_license_plate_reg , foreign_car_license_plate , path_of_license) = license_plate_recognition()
                    if flag_license_plate_reg == False:
                        message_to_server = "A foreign car with the number " + foreign_car_license_plate + \
                                            " is parked in your private parking lot. Do you approve triggering an alarm?"
                        flag_from_server = start_session_with_server(message_to_server, path_of_license)
                        ser2 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)#arduino nano alarm
                        ser2.reset_input_buffer()
                        if flag_from_server:
                            mode = b"active\n"
                            alarm_control(ser1, ser2, mode)
                        else:
                            mode = b"no active\n"
                            alarm_control(ser1, ser2, mode)

def alarm_control(ser1 , ser2 , mode):
    ser1.reset_input_buffer()
    if ser1.in_waiting > 0:
        line1 = ser1.readline().decode('utf-8').rstrip()
        converted_num = int(line1)
        while converted_num < 100:
            ser2.write(mode)
            if ser1.in_waiting > 0:
                line1 = ser1.readline().decode('utf-8').rstrip()
                converted_num = int(line1)
    if mode == b"active\n":
        ser2.write(b"no active\n")
    ser2.close()


if __name__ == '__main__':
    Get_distance()
    cv2.waitKey(0)