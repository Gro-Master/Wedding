import cv2
import requests
import numpy as np
from PIL import Image, ImageOps
from io import BytesIO

# Ваш API-ключ remove.bg
API_KEY = "YOUR_REMOVE_BG_API_KEY"

def remove_background(image_path):
    """Удаляет фон с изображения через API remove.bg"""
    with open(image_path, 'rb') as file:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': file},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY}
        )
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print("Ошибка удаления фона:", response.text)
        return None

def resize_proportional(image, target_size=(1500, 1000)):
    """Изменяет размер изображения пропорционально и вписывает в рамки."""
    # Исходные размеры
    w, h = image.size
    target_w, target_h = target_size

    # Вычисляем новый размер, сохраняя пропорции
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)

    # Масштабируем изображение
    image_resized = image.resize((new_w, new_h), Image.LANCZOS)

    # Создаем новое изображение с нужным размером и вставляем в центр
    new_image = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 0))  # Прозрачный фон
    new_image.paste(image_resized, ((target_w - new_w) // 2, (target_h - new_h) // 2))

    return new_image

def process_image(image_path, output_path):
    """Удаляет фон, изменяет размер пропорционально и сохраняет"""
    img_no_bg = remove_background(image_path)
    if img_no_bg:
        img_resized = resize_proportional(img_no_bg, (1500, 1000))
        img_resized.save(output_path, format="PNG")
        print(f"Обработанное изображение сохранено как {output_path}")
    else:
        print("Не удалось обработать изображение.")

# Использование
process_image("IMG_9226.jpg", "output.png")
