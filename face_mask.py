
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

specs_ori = cv2.imread('glass.png', -1)
cigar_ori = cv2.imread('cigar.png', -1)
mus_ori = cv2.imread('mustache.png', -1)


def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return 




def create_mask(url_file):

    cap = cv2.VideoCapture(url_file)


    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(f'final_{url_file}', fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(3)), int(cap.get(4))))


    try:
        while cap.isOpened():
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(img, 1.2, 5, 0, (120, 120), (350, 350))
            
            for (x, y, w, h) in faces:
                if h > 0 and w > 0:
                    glass_symin = int(y + 1.5 * h / 5)
                    glass_symax = int(y + 2.5 * h / 5)
                    sh_glass = glass_symax - glass_symin

                    cigar_symin = int(y + 4 * h / 6)
                    cigar_symax = int(y + 5.5 * h / 6)
                    sh_cigar = cigar_symax - cigar_symin

                    mus_symin = int(y + 3.5 * h / 6)
                    mus_symax = int(y + 5 * h / 6)
                    sh_mus = mus_symax - mus_symin

                    face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]
                    face_cigar_roi_color = img[cigar_symin:cigar_symax, x:x + w]
                    face_mus_roi_color = img[mus_symin:mus_symax, x:x + w]

                    specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
                    # cigar = cv2.resize(cigar_ori, (w, sh_cigar), interpolation=cv2.INTER_CUBIC)
                    mustache = cv2.resize(mus_ori, (w, sh_mus), interpolation=cv2.INTER_CUBIC)

                    transparentOverlay(face_glass_roi_color, specs)
                    # transparentOverlay(face_cigar_roi_color, cigar, (int(w / 2), int(sh_cigar / 2)))
                    # transparentOverlay(face_mus_roi_color, mustache)

            out.write(img)
            # cv2.imshow('Video', img)

            if cv2.waitKey(delay=1) == 27:
                break
            
    except Exception as e: print(e)

    print('finished processing')

    cap.release()
    out.release()

