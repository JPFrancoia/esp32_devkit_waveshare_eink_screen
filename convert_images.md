## GIMP: convert image to 1 bit image

Source: https://graphicdesign.stackexchange.com/questions/103717/how-do-i-create-true-two-color-images-in-gimp

In GIMP click Image > Mode > Indexed
Select the option which says "Use Black and White (1 bit) palette"
Click File > Export As

Give your file a new new name, and end with the file extension .BMP and
hit Export - if a warning comes up about transparency not being supported
in bitmap, ignore it, and hit OK.


## Convert a BMP image to a Python framebuffer

Source: https://forum.micropython.org/viewtopic.php?t=4806&start=20

See previous section on how to get a BMP image.

Now I convert that into a very old bitmap format (binary PBM file format
'P4' by Jef Poskanzer). That stuff dates back to the 1980's, but the fun
here is that the data of that bitmap is arranged EXACTLY as it is in a
MONO_HLSB type MicroPython FrameBuffer.

```
convert smile1.bmp smile1.pbm
```

Use the convert command from ImageMagick.

The smile1.pbm file will contain two '\n' terminated lines. The first one
identifying the file format 'P4' (monochrome bitmap binary) and the second
'<width> <height>' in decimal, space separated. The remaining bytes in that
file are the binary bitmap data.V

```
$ head -2 smile1.pbm
```

Then use the following python snippet:

```python
import sys
import os

def main():
    if len(sys.argv) != 2:
        usage()
        return 2

    with open(sys.argv[1], 'rb') as fd:
        pbm_format = fd.readline().strip()
        if pbm_format != b'P4':
            print("ERROR: input file must be binary PBM (type P4)",
                  file = sys.stderr)
            return 1
        pbm_dims = [int(d) for d in fd.readline().strip().split()]
        pbm_data = fd.read()

    fbbase = "fb_{0}".format(os.path.basename(sys.argv[1]))
    fbname = os.path.splitext(fbbase)[0]
    with sys.stdout as fd:
        f = "{0} = framebuf.FrameBuffer(bytearray({1}), {2}, {3}, framebuf.MONO_HLSB)\n"
        fd.write(f.format(fbname, str(pbm_data), pbm_dims[0], pbm_dims[1]))


def usage():
    print("""usage: {0} PBM_FILE""".format(os.path.basename(sys.argv[0])),
          file = sys.stderr)

if __name__ == '__main__':
    main()
```

Output:

```python
fb_smile1 = framebuf.FrameBuffer(bytearray(b'\x00~\x00\x03\xff\xc0\x07\x81\xe0\x1e\x00x8\x00\x1c0\x00\x0c`\x00\x0ea\xc3\x86\xe0\x00\x07\xc0\x00\x03\xc0\x00\x03\xc0\x00\x02\xc0\x00\x03\xc0\x00\x03\xe0B\x07`<\x06`\x00\x060\x00\x0c8\x00\x1c\x1e\x00x\x07\x81\xe0\x03\xff\xc0\x00\xff\x00'), 24, 23, framebuf.MONO_HLSB)
```

This can be used directly in MicroPython scripts that use framebuffers.
