import urllib.request
import urllib.error
from time import strftime as st
from PythonAdv.ClassWork.Lesson05.class_tasks.D01 import decorator


url_list = ['https://i.imgur.com/VVJfdPs.jpg', 'https://i.imgur.com/0E2nnym.png',
            'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1024px-Python-logo-notext.svg.png',
            'https://www.sketchappsources.com/resources/source-image/python-logo.png',
            'https://desano.ru/uploads/catalog/1480/NS-10490-1.jpg', 'https://djangostars.com/blog/uploads/2019/03/cover-13.png'
            'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/1024px-Python.svg.png',
            'https://images-na.ssl-images-amazon.com/images/I/51IabRNacHL._SX425_.jpg',
            'https://cdn.imgbin.com/0/9/3/imgbin-web-development-python-software-developer-web-developer-software-development-python-logo-ffmsaJXYTNUWHQAUam4PMCA60.jpg',]


@decorator(False)
def multi_thread_download(url):
    path = url.split('/')[-1]

    try:

        s_t = (int(st('%H')), int(st('%M')), int(st('%S')))
        print(f'Downloading {path} start at {s_t[0]}.{s_t[1]}.{s_t[2]}')
        urllib.request.urlretrieve(url, f'./{path}')
        f_t = (int(st('%H')), int(st('%M')), int(st('%S')))
        print(f'Downloading {path} finish at {f_t[0]}.{f_t[1]}.{f_t[2]}')

        print(f'Time that takes to download: {f_t[0] - s_t[0]}.{f_t[1] - s_t[1]}.{f_t[2] - s_t[2]}')

    except Exception:
        print(f'Downloading file {path} failed')

for i in url_list:
    multi_thread_download(i)
