import requests


def save_image_from_url(image_url, image_name):
    local_image_path = f"/home/service/images/{image_name}.jpg"

    try:
        # 发送GET请求并获取图片内容
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # 使用二进制模式打开文件
        with open(local_image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    except Exception as e:
        print(e)
