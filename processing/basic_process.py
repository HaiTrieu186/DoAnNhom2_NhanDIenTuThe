import numpy as np

def gamma_process(img, gamma):
    img_float=img/255
    gamma_corrected=np.power(img_float,gamma)
    gamma_corrected=np.uint8(gamma_corrected*255)
    return gamma_corrected

def log_process(img):
    img_float = img.astype(np.float32)
    c = 255 / np.log(1 + np.max(img_float))
    log_image = c * np.log(1 + img_float)
    log_image = np.uint8(log_image)
    return log_image

def linear_process(img):
    r_min, r_max = np.min(img), np.max(img)
    stretched = (img - r_min) * (255 / (r_max - r_min))
    stretched = np.uint8(stretched)
    return stretched