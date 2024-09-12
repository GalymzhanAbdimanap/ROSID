import cv2
import os
import random

def apply_sliding_window_mask(mask_path, window_size, stride, output_folder):
    # Загружаем маску
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    height, width = mask.shape
    
    output_filename = os.path.basename(mask_path)[:-4]
    # Проходим по маске с помощью скользящего окна
    for y in range(0, height - int(window_size[1]/3), stride):
        for x in range(0, width - int(window_size[0]/3), stride):
            # Проверяем, не выходит ли окно за пределы маски
            if x + window_size[0] <= width and y + window_size[1] <= height:
                # Вырезаем кусок маски
                window_mask = mask[y:y+window_size[1], x:x+window_size[0]]
                crop_filename = f'{output_folder}/{output_filename}_{x}_{y}.png'
            else:
                if x + window_size[0] > width and y + window_size[1] > height:
                    window_mask = mask[height-window_size[1]:height, width-window_size[0]:width]
                    crop_filename =  f'{output_folder}/{output_filename}_{width-window_size[0]}_{height-window_size[1]}.png'
                elif x + window_size[0] > width:
                    window_mask = mask[y:y+window_size[1], width-window_size[0]:width]
                    crop_filename =  f'{output_folder}/{output_filename}_{width-window_size[0]}_{y}.png'
                else:
                    window_mask = mask[height-window_size[1]:height, x:x+window_size[0]]
                    crop_filename =  f'{output_folder}/{output_filename}_{x}_{height-window_size[1]}.png'
                
                                
            # Сохраняем обрезанную маску
            cv2.imwrite(crop_filename, window_mask)




def apply_sliding_window(image_path, window_size, stride, output_folder):
    # Загружаем изображение
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    output_filename = os.path.basename(image_path)[:-4]
    
    # Проходим по изображению с помощью скользящего окна
    for y in range(0, height - int(window_size[1]/3), stride):
        for x in range(0, width - int(window_size[0]/3), stride):
            # Проверяем, не выходит ли окно за пределы изображения
            if x + window_size[0] <= width and y + window_size[1] <= height:
                # Вырезаем кусок изображения
                window = img[y:y+window_size[1], x:x+window_size[0]]
                crop_filename = f'{output_folder}/{output_filename}_{x}_{y}.png'
            else:
                if x + window_size[0] > width and y + window_size[1] > height:
                    window = img[height-window_size[1]:height, width-window_size[0]:width]
                    crop_filename =  f'{output_folder}/{output_filename}_{width-window_size[0]}_{height-window_size[1]}.png'
                elif x + window_size[0] > width:
                    window = img[y:y+window_size[1], width-window_size[0]:width]
                    crop_filename =  f'{output_folder}/{output_filename}_{width-window_size[0]}_{y}.png'
                else:
                    window = img[height-window_size[1]:height, x:x+window_size[0]]
                    crop_filename =  f'{output_folder}/{output_filename}_{x}_{height-window_size[1]}.png'
                
            cv2.imwrite(crop_filename, window)


def split_dataset(input_folder, output_folder, train_ratio=0.9, val_ratio=0.1, test_ratio=0.0):
    # Проверяем, существует ли папка output_folder, если нет, создаем ее
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    # Получаем список файлов входной папки
    files = os.listdir(input_folder)
    num_files = len(files)

    # Перемешиваем список файлов
    random.shuffle(files)

    # Рассчитываем количество файлов для каждого набора данных
    num_train = int(num_files * train_ratio)
    num_val = int(num_files * val_ratio)
    num_test = num_files - num_train - num_val



    
    train_filenames = []
    val_filenames = []
    test_filenames = []
    # Копируем файлы в соответствующие папки
    for i, file in enumerate(files):
        if i < num_train:
            train_filenames.append(file[:-4])
        elif i < num_train + num_val:
            val_filenames.append(file[:-4])
        else:
            test_filenames.append(file[:-4])
        
        
    if train_filenames:
        with open(os.path.join(output_folder, 'splits', 'train.txt'), 'w') as f:
            f.writelines(line + '\n' for line in train_filenames)
    if val_filenames:
        with open(os.path.join(output_folder, 'splits', 'val.txt'), 'w') as f:
            f.writelines(line + '\n' for line in val_filenames)
    if test_filenames:
        with open(os.path.join(output_folder, 'splits', 'test.txt'), 'w') as f:       
            f.writelines(line + '\n' for line in test_filenames)


def main(input_dir, output_dir, window_size = (320, 320), stride = 106, train_per = 0.9, test_per = 0.1):

    # output_dir ='dataset_landsat_743_320_320'
    output_images = f'{output_dir}/images'
    output_labels = f'{output_dir}/labels_rgb'
    output_mask = f'{output_dir}/labels'
    output_images_test = f'{output_dir}/test/images'
    output_labels_test = f'{output_dir}/test/labels_rgb'
    output_mask_test = f'{output_dir}/test/labels'

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_images, exist_ok=True)
    os.makedirs(output_labels, exist_ok=True)
    os.makedirs(output_mask, exist_ok=True)

    os.makedirs(f'{output_dir}/test', exist_ok=True)
    os.makedirs(output_images_test, exist_ok=True)
    os.makedirs(output_labels_test, exist_ok=True)
    os.makedirs(output_mask_test, exist_ok=True)
    
    

    # Размер окна и шаг
    

    for root, dir, files in os.walk(input_dir):#'src_dataset_landsat_743/images'
        train_files = len(files) * train_per
        for i, file in enumerate(files):
            
            
            # if file != 'LC08_165030_20130502.png':
            #     continue
            image_path = f'{root}/{file}'
            label_path =  f'{root.split("/")[0]}/labels_rgb/{file}'
            mask_path = f'{root.split("/")[0]}/labels/{file}'

            if i+1 < train_files:
                # Применяем скользящее окно и сохраняем обрезанные изображения
                apply_sliding_window(image_path, window_size, stride, output_images)
                apply_sliding_window(label_path, window_size, stride, output_labels)
                apply_sliding_window_mask(mask_path, window_size, stride, output_mask)

            else:
                apply_sliding_window(image_path, window_size, stride, output_images_test)
                apply_sliding_window(label_path, window_size, stride, output_labels_test)
                apply_sliding_window_mask(mask_path, window_size, stride, output_mask_test)
        break

    #Split Train
    input_folder = output_images  # Папка с изображениями
    output_folder = output_dir  # Папка для сохранения разделенных наборов данных
    os.makedirs(os.path.join(output_folder, 'splits'), exist_ok=True)
    # Создаем разделенные наборы данных
    split_dataset(input_folder, output_folder, train_ratio=0.9, val_ratio=0.1, test_ratio=0.0)

    #Split Test
    input_folder = output_images_test  # Папка с изображениями
    output_folder = output_dir  # Папка для сохранения разделенных наборов данных
    # Создаем разделенные наборы данных
    split_dataset(input_folder, output_folder, train_ratio=0.0, val_ratio=0.0, test_ratio=1.0)

# Пример использования функции
if __name__ == "__main__":

    main('ROSID/images', 'ROSID_320_320', window_size = (320, 320), stride = 106, train_per = 0.9, test_per = 0.1)
    # apply_sliding_window('src_dataset_landsat_743/test/images/LT05_165030_20070923.png', window_size = (320, 320), stride = 106, output_folder='dataset_landsat_743_320_320/test/images')

    
    
    
    
    
    
    
