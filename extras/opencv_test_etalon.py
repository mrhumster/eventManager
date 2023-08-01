import cv2
import numpy as np
import face_recognition as fr
import uuid
import os
from os import path
from os import system
import numpy as np
from random import randrange
from threading import Thread, Lock

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

directory = '/home/omra/PycharmProjects/eventManager/faces'

known_face_encodings = []
known_face_names = []

hello_list = ['Приветствую!', 'Я вас категорически приветствую!', 'Доброго времени суток!', 'Моё почтение!',
              'Доброго дня!', 'Привет, мой свет!', 'Рада вас видеть!', 'Здравствуй', 'Доброго здоровья!',
              'Доброго времени бытия']

first_hello_list = []


def fc_enc(directory, known_face_encodings, known_face_names):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image = fr.load_image_file(f)
            known_face_encodings.append(fr.face_encodings(image)[0])
            index = path.basename(f).index('.')
            known_face_names.append(str(path.basename(f)[:index]))
    print('faces update')


##    return known_face_encodings, known_face_names


def FHL(hello_list, name):
    system(f"ale '{hello_list[randrange(len(hello_list))]} {name}!'")


def eta_cre(frame, directory):
    uid = uuid.uuid4()
    cv2.imwrite(f"{directory}/{uid}.jpg", frame)
    print('Photo save')


font = cv2.FONT_HERSHEY_COMPLEX

fc_enc(directory, known_face_encodings, known_face_names)

while True:
    # Получение кадра видеопотока
    ret, frame = cap.read()
    rgb_small_frame = np.ascontiguousarray(frame[:, :, ::-1])

    fc_locations = fr.face_locations(rgb_small_frame)
    fc_encodings = fr.face_encodings(rgb_small_frame, fc_locations)

    # Обработка каждого найденного лица
    for (top, right, bottom, left), face_encoding in zip(fc_locations, fc_encodings):

        matches = fr.compare_faces(known_face_encodings, face_encoding)

        name = "Неизвестный"

        fc_distances = fr.face_distance(known_face_encodings, face_encoding)

        match_index = np.argmin(fc_distances)

        if matches[match_index]:
            name = known_face_names[match_index]
            face_match_percentage = (1 - fc_distances) * 100
            cv2.putText(frame, str(face_match_percentage[match_index])[:4], (left - 35, bottom + 60), font, 1.0,
                        (255, 255, 255), 1)

        cv2.rectangle(frame, (left, top), (right, bottom + 25), (0, 0, 0), 2)
        cv2.rectangle(frame, (left, bottom), (right, bottom + 25), (0, 0, 0), cv2.FILLED)

        cv2.putText(frame, name, (left - 35, bottom + 30), font, 1.0, (255, 255, 255), 1)

        if name != "Неизвестный" and any(ch.isdigit() for ch in name) == False and name not in first_hello_list:
            first_hello_list.append(name)
            t1 = Thread(target=FHL, args=(hello_list, name))
            t1.start()

    # Вывод кадра на экран
    #cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        known_face_encodings = []
        known_face_names = []
        t3 = Thread(target=fc_enc, args=(directory, known_face_encodings, known_face_names))
        t3.start()
        t3.join()

    if cv2.waitKey(1) & 0xFF == ord('n') and name == "Неизвестный":
        t2 = Thread(target=eta_cre, args=(frame, directory))
        t2.start()

    if cv2.waitKey(1) & 0xFF == ord('c'):
        first_hello_list = []

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Остановка видеопотока и закрытие окон
cap.release()
cv2.destroyAllWindows()
