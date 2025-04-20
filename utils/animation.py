import imageio
import matplotlib.pyplot as plt
from glob import glob

def create_gif(output_path="animated.gif", source="runs/detect/predict/*.jpg", duration=1):
    imgs = [plt.imread(p) for p in sorted(glob(source))]
    imageio.mimsave(output_path, imgs, duration=duration)
