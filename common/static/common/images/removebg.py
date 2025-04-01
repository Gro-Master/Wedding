import requests
from PIL import Image
# from rembg import remove

def resize_and_pad_left(input_image_path, sample_image_path, output_image_path):
    # Открываем образец и входное изображение
    sample_image = Image.open(sample_image_path)
    input_image = Image.open(input_image_path).convert("RGBA")  # Открываем с поддержкой прозрачности

    # Получаем размеры образца
    sample_width, sample_height = sample_image.size

    # Масштабируем входное изображение по высоте образца (с сохранением пропорций)
    aspect_ratio = input_image.width / input_image.height
    new_height = sample_height
    new_width = int(new_height * aspect_ratio)
    input_image = input_image.resize((new_width, new_height), Image.LANCZOS)

    # Создаем новое изображение с прозрачным фоном
    new_image = Image.new("RGBA", (sample_width, sample_height), (0, 0, 0, 0))  # Прозрачный фон

    # Вычисляем сдвиг (новое изображение должно быть справа, а слева — прозрачный фон)
    x_offset = sample_width - new_width  # Смещение по X (заполняем только слева)

    # Вставляем изображение справа
    new_image.paste(input_image, (x_offset, 0))

    # Сохраняем результат в PNG
    new_image.save(output_image_path, format="PNG")
    print(f"Изображение приведено к формату образца и сохранено как {output_image_path}")

def remove_background(input_image_path, output_image_path, api_key):
    # Открытие изображения
    with open(input_image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Отправка изображения на сервер Remove.bg для удаления фона
    url = 'https://api.remove.bg/v1.0/removebg'
    response = requests.post(
        url,
        files={'image_file': image_data},
        headers={'X-Api-Key': api_key},
        stream=True
    )

    # Проверка ответа от сервера
    if response.status_code == 200:
        # Сохранение изображения без фона
        with open(output_image_path, 'wb') as output_file:
            output_file.write(response.content)
        print(f"Фон успешно удален и сохранен в {output_image_path}")
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")

def remove_bg_local(input_image_path, output_image_path):
    image = Image.open(input_image_path)
    output = remove(image)  # Удаляем фон без потери качества
    output.save(output_image_path, format="PNG")
    print(f"Фон удален и сохранен в {output_image_path}")

def resize_with_padding(input_image_path, output_image_path, target_width, target_height, background_color=(0, 0, 0, 0)):
    """
    Масштабирует изображение до заданного размера (target_width x target_height), сохраняя пропорции.
    Добавляет фон, если изображение не совпадает по соотношению сторон.

    :param input_image_path: Путь к исходному изображению
    :param output_image_path: Путь для сохранения результата
    :param target_width: Желаемая ширина
    :param target_height: Желаемая высота
    :param background_color: Цвет фона (по умолчанию прозрачный)
    """
    # Открываем изображение
    image = Image.open(input_image_path).convert("RGBA")

    # Исходные размеры
    original_width, original_height = image.size

    # Вычисляем коэффициент масштабирования (чтобы картинка полностью вписывалась)
    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Масштабируем изображение
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Создаем новый холст с заданными размерами
    new_image = Image.new("RGBA", (target_width, target_height), background_color)

    # Вычисляем координаты для центрирования
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    # Вставляем масштабированное изображение по центру
    new_image.paste(resized_image, (x_offset, y_offset), resized_image)

    # Сохраняем результат в PNG (чтобы сохранить прозрачность)
    new_image.save(output_image_path, format="PNG")
    print(f"Изображение сохранено в {output_image_path}")


# Пример использования
input_image_path = 'IMG_9226.png'  # Путь к исходному изображению
output_image_path = 'output_image.png'  # Путь для сохранения результата
sample_image_path = 'sample.png' 
api_key = 'oErv1nSdrzKr9cyazUnU6kx1'  # Ваш API-ключ от remove.bg

# remove_background(input_image_path, output_image_path, api_key)

# resize_and_pad_left(input_image_path, sample_image_path, output_image_path)

# Пример использования
# remove_bg_local(input_image_path, output_image_path)

resize_with_padding("footer.jpg", "footer_res.jpg", 1000, 400)