import cv2

# Путь к исходному изображению
input_path = 'about.png'       # можно использовать .png, .jpeg и т.п.
output_path = 'about_bw.png'

# Загружаем изображение
image = cv2.imread(input_path)

# Преобразуем в градации серого
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Сохраняем результат
cv2.imwrite(output_path, gray_image)

print(f"Готово! Сохранено как {output_path}")
