import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))



import requests
import json
import time

URL = 'https://yesno.wtf/api'

GIF_FOLDER = os.path.join(HERE_PATH, 'gifs')


if __name__ == '__main__':

    n_iteration = 0
    while True:
        time.sleep(5)
        n_iteration += 1
        print('{}'.format(n_iteration))

        response = requests.get(URL)
        if response.ok:
            answer = json.loads(response.content)

            gif_url = answer['image']
            path, filename = os.path.split(gif_url)
            _, foldername = os.path.split(path)

            r = requests.get(gif_url)
            if r.ok:
                gif_savefilename = os.path.join(GIF_FOLDER, foldername, filename)
                if os.path.exists(gif_savefilename):
                    print('{} already exists'.format(gif_savefilename))
                with open(gif_savefilename, 'wb') as f:
                    f.write(r.content)
