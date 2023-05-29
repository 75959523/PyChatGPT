import urllib.request
import ssl


def execute(image_url, image_name):
    local_image_path = "/Users/haoyunlong/Desktop/{}.jpg".format(image_name)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(image_url, context=ctx) as response, open(local_image_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except Exception as e:
        print(e)
