import json
import os.path
import subprocess
import sys
import tempfile

from pyte import Screen, Stream
from PIL import Image, ImageDraw, ImageFont


def main(path):
    font = ImageFont.truetype("SourceCodePro-Regular.otf", size=16)
    with tempfile.TemporaryDirectory() as dirname, open(path, 'r') as f:
        meta = json.loads(f.readline())
        screen = Screen(meta['width'], meta['height'])
        stream = Stream()
        stream.attach(screen)
        i = 0
        for line in f:
            delay, opt, text = json.loads(line)
            img = Image.new("RGBA", (1280, 960))
            draw = ImageDraw.Draw(img)
            stream.feed(text)
            draw.multiline_text((0, 0), "\n".join(screen.display), font=font)
            img.save(os.path.join(dirname, '%04d.gif' % i))
            i = i + 1
        subprocess.run('gifsicle -d 10 --loopcount -O2 --output %s.gif %s/*.gif' % (path, dirname),
                       shell=True, check=True)

if __name__ == "__main__":
    main(sys.argv[1])
