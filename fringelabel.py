import numpy as np
from skimage import measure, morphology
from PIL import Image
import pandas as pd
from console_progressbar import ProgressBar


class FringeAnalysis:
    def __init__(self):
        self.name_image = ""
        self.image = []
        self.image_bw = []
        self.cte = 0
        self.image_v = []
        self.image_h = []
        self.original = []

    def load_image(self, name):
        # Loading image into class structure
        print("Loading {}...".format(name))
        self.name_image = name
        # Image should be read as a grayscale matrix
        aux = np.asarray(Image.open(self.name_image).convert('L'), dtype=np.uint16)
        self.image = aux.copy()
        del aux
        # binary image over threshold
        if self.image is not None:
            self.image_bw = self.bin_array(self.image)
            self.original = self.image_bw.copy()
        else:
            print("Not a valid image")

    @staticmethod
    def bin_array(numpy_array, threshold=128, background=0):
        """
        "binarize" a numpy array

        background = 0 : change background to Black "white background images"
        background = 1 : keep black background "black background images"

        else just convert over the threshold
        """
        numpy_array = np.where(numpy_array >= threshold, 255 * background, 255 * (1 - background))
        return numpy_array

    @staticmethod
    def find_size(image, start):
        dis = 0
        x = start[0]
        y = start[1]
        end = 1
        while end != 0:
            up = True if image[y - 1][x] != 0 else False
            up_right = True if image[y - 1][x + 1] != 0 else False
            right = True if image[y][x + 1] != 0 else False
            down_right = True if image[y + 1][x + 1] != 0 else False
            down = True if image[y + 1][x] != 0 else False
            down_left = True if image[y + 1][x - 1] != 0 else False
            left = True if image[y][x - 1] != 0 else False
            up_left = True if image[y - 1][x - 1] != 0 else False

            end = up + up_right + right + down_right + down + down_left + left + up_left
            if end == 0:
                return dis
            else:
                if up:
                    dis = dis + 1
                    image[y][x] = 0
                    y = y - 1

                if down:
                    dis = dis + 1
                    image[y][x] = 0
                    y = y + 1

                if left:
                    dis = dis + 1
                    image[y][x] = 0
                    x = x - 1

                if right:
                    dis = dis + 1
                    image[y][x] = 0
                    x = x + 1

                if up_left:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x - 1
                    y = y - 1

                if up_right:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x + 1
                    y = y - 1

                if down_left:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x - 1
                    y = y + 1

                if down_right:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x + 1
                    y = y + 1

    def filter_sizes(self):
        """
        Each resolution in images can help me to make a little filter over te images.
        450 kx for example need minimum 22 pixels to be considered a correct fringe
        adjust those values to the necessities.

        if you wanna see the changes between those 2 images, before and after filter
        aux = np.uint8(np.where(self.image_bw > 0, 255, 0))
        Image.fromarray(aux).save("pos.tif")
        put those lines before and after morphology instruction


        :return: None, OverWrite the image_wb attribute
        """

        m450kx = "450kx" in self.name_image
        m590kx = "590kx" in self.name_image
        m690kx = "690kx" in self.name_image
        print("cleaning noisy elements from image...")
        self.image_bw = measure.label(self.image_bw)
        if m450kx:
            # diag 21.41
            min_size = 22
            morphology.remove_small_objects(self.image_bw, connectivity=2, min_size=min_size, in_place=True)
            self.cte = 40.8
            print("Resolution: M450kx")
        if m590kx:
            # diag 18.31
            min_size = 19
            morphology.remove_small_objects(self.image_bw, connectivity=2, min_size=min_size, in_place=True)
            self.cte = 53.6
            print("Resolution: M590kx")
        if m690kx:
            # diag 13.93
            min_size = 14
            morphology.remove_small_objects(self.image_bw, connectivity=2, min_size=min_size, in_place=True)
            self.cte = 62.7
            print("Resolution: M690kx")

    def process_lc(self):
        if self.image is not None:
            self.filter_sizes()
            labels = self.image_bw
            final_label = np.zeros((len(labels), len(labels[0])))
            final_label_h = np.zeros((len(labels), len(labels[0])))
            final_label_v = np.zeros((len(labels), len(labels[0])))
            df = pd.DataFrame(columns=['image', 'coord_start', 'coord_end', 'c', 'l', 'c/l'])
            # df_rejected = pd.DataFrame(columns=['image', 'coord_start', 'coord_end', 'c', 'l'])
            index = 0
            a = measure.regionprops(labels, coordinates='xy')
            bar = len(a) - 1
            print("\nisolating and measuring fringes:")
            pb = ProgressBar(total=bar, prefix='processed fringes', suffix='Done', decimals=3, length=50, fill='X',
                             zfill='-')

            for region in a:
                pb.print_progress_bar(index)
                img_aux = region.image
                base = np.zeros([len(img_aux) + 2, len(img_aux[0]) + 2])
                x = 0
                for row in img_aux:
                    y = 0
                    for element in row:
                        base[x + 1][y + 1] = 1 if element else 0
                        y += 1
                    x += 1
                aux = base.copy()
                for x in range(len(base)):
                    for y in range(len(base[0])):
                        if base[x][y] == 1:
                            aux[x][y] = base[x - 1][y - 1] + \
                                        base[x - 1][y] + \
                                        base[x - 1][y + 1] + \
                                        base[x][y - 1] + \
                                        base[x + 1][y - 1] + \
                                        base[x + 1][y] + \
                                        base[x + 1][y + 1] + \
                                        base[x][y + 1]
                        else:
                            pass
                u = 0
                k = 0
                alpha = []
                omega = []
                for row in aux:
                    coords = [i for (i, val) in enumerate(row) if val == 1]
                    if len(coords) != 0:
                        k += 1
                        if len(coords) == 2:
                            alpha = [coords[0], u]
                            omega = [coords[1], u]
                            k += 1
                        if len(coords) == 1:
                            if k == 1:
                                alpha = [coords[0], u]
                            if k == 2:
                                omega = [coords[0], u]
                    triple = [i for (i, val) in enumerate(row) if val == 3]
                    if len(triple) != 0:
                        k = 3
                    u += 1
                if k != 2:
                    alpha = []
                    omega = []
                if (k == 2) & (len(alpha) != 0) & (len(omega) != 0):
                    long = np.sqrt(np.power((alpha[0] - omega[0]), 2) + np.power((alpha[1] - omega[1]), 2))
                    curvature = self.find_size(aux, alpha)
                    ori = np.rad2deg(region.orientation)
                    df = df.append(
                        {'image': index, 'coord_start': alpha, 'coord_end': omega, 'c': curvature, 'l': long,
                         'c/l': curvature / long, 'orientation': ori}, ignore_index=True)

                    x1 = region.bbox[0]
                    x2 = region.bbox[2]
                    y1 = region.bbox[1]
                    y2 = region.bbox[3]
                    final_label[x1:x2, y1:y2] = final_label[x1:x2, y1:y2] + region.image

                    if (-45 < ori) & (ori < 45):
                        final_label_h[x1:x2, y1:y2] = final_label_h[x1:x2, y1:y2] + region.image
                    else:
                        final_label_v[x1:x2, y1:y2] = final_label_h[x1:x2, y1:y2] + region.image

                    final_label[x1:x2, y1:y2] = region.image
                    pass
                index += 1
                pass
            name_aux = self.name_image.split('.')
            df.to_excel(name_aux[0] + "_fringes.xlsx", index=False)

            definitive = final_label * 255

            im = Image.fromarray(final_label_v * 255)
            im.save(name_aux[0] + "_v." + name_aux[1])
            im = Image.fromarray(final_label_h * 255)
            im.save(name_aux[0] + "_h." + name_aux[1])
            im = Image.fromarray(definitive)
            im.save(name_aux[0] + "_final." + name_aux[1])

            bad_f = self.original - final_label_h * 255 - final_label_v * 255
            im = Image.fromarray(bad_f)
            im.save(name_aux[0] + "_bad_fringes." + name_aux[1])

        else:
            print("First load any valid image")

    def process_inter_distance(self, dir_image):
        name_aux = dir_image.split('.')
        print("Loading {} vertical and horizontal...".format(dir_image[0]))
        self.image_v = Image.open(name_aux[0] + "_v." + name_aux[1])
        self.image_h = Image.open(name_aux[0] + "_h." + name_aux[1])
