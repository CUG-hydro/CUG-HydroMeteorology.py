from PyPDF2 import PdfFileMerger
import os
from PIL import Image
# import glob
# import re


def merge_pdf(files, fout, delete=True):
  merger = PdfFileMerger()
  for f in files:
      merger.append(f)
  merger.write(fout)
  merger.close()
  if delete:
    [os.remove(f) for f in files]


def images2pdf(files, outfile="Plot.pdf"):
    img, *imgs = [Image.open(f) for f in sorted(files)]
    img.save(fp=outfile, format='PDF', append_images=imgs,
             save_all=True)


def images2gif(files, outfile="Plot.gif", duration=250):
    img, *imgs = [Image.open(f) for f in sorted(files)]
    img.save(fp=outfile, format='GIF', append_images=imgs,
             save_all=True, duration=duration, loop=0)
