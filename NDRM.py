import os
import subprocess
from multiprocessing import Pool

def resize_video(input_path, output_path, size):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={size[0]}:{size[1]}',
        '-c:v', 'mpeg4',  # Замените 'h264_nvenc' на 'mpeg4' для совместимости с AVI
        '-qscale:v', '3',  # Качество для кодека MPEG4
        output_path
    ]
    subprocess.run(command)

def change_speed(input_path, output_path, speed):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-filter:v', f'setpts={1/speed}*PTS',  # Изменение скорости
        '-c:v', 'mpeg4',  # Кодек MPEG4 для AVI
        '-b:v', '5000k',  # Установка битрейта видео
        output_path
    ]
    subprocess.run(command)



def process_file(args):
    task, file, size_choice, speed_choice, sizes, speeds = args

    if task == "1":
        input_path = os.path.join('input', file)
        output_path = os.path.join('output', f"resized_{file}")
        resize_video(input_path, output_path, sizes[size_choice])
    elif task == "2":
        input_path = os.path.join('input', file)
        output_path = os.path.join('output', f"speed_{file}")
        change_speed(input_path, output_path, float(speeds[speed_choice]))

def main():
    # Создание папок
    if not os.path.exists('input'):
        os.makedirs('input')
    if not os.path.exists('output'):
        os.makedirs('output')

    while not os.listdir('input'):
        input("Внесите видеозаписи и нажмите Enter...")

    while True:
        files = os.listdir('input')
        for index, file in enumerate(files, 1):
            print(f"{index}. {file}")
        choice = input("Выберите файл или файлы для обработки (разделите пробелами для множественного выбора): ")
        chosen_files = [files[int(i) - 1] for i in choice.split() if i.isdigit() and 1 <= int(i) <= len(files)]

        print("1. Изменить размер видео")
        print("2. Ускорить/замедлить видео")
        task = input("Выберите задачу: ")

        if task == "1":
            sizes = {
                "1": (3840, 2160),
                "2": (1920, 1080),
                "3": (1280, 720),
                "4": (960, 540),
                "5": (640, 480),
                "6": (426, 240)
            }
            for key, value in sizes.items():
                print(f"{key}. {value[0]}x{value[1]}")
            size_choice = input("Выберите размер: ")
            speeds = None
            speed_choice = None
        elif task == "2":
            sizes = None
            size_choice = None
            speeds = {
                "1": 10, "2": 5, "3": 3, "4": 2, "5": 1.5,
                "-1": 0.1, "-2": 0.2, "-3": 0.33, "-4": 0.5, "-5": 0.67
            }
            print("Ускорение:")
            for key, value in speeds.items():
                if float(key) > 0:
                    print(f"{key}. {value}x")
            print("Замедление:")
            for key, value in speeds.items():
                if float(key) < 0:
                    print(f"{key}. {value}x")
            speed_choice = input("Выберите коэффициент ускорения/замедления: ")
        else:
            print("Неверный выбор.")
            continue

        with Pool(4) as p:
            p.map(process_file, [(task, file, size_choice, speed_choice, sizes, speeds) for file in chosen_files])

if __name__ == "__main__":
    main()
