import cv2
import numpy as np
from skimage import measure
from PIL import Image
import pandas as pd
from console_progressbar import ProgressBar


class FringeAnalysis:
    def __init__(self):
        self.name_image = ""
        self.image = []
        self.image_bw = []
        self.cte = 0

    def load_image(self, name):
        # Loading image into class structure
        print("Loading {}...".format(name))
        self.name_image = name
        # Image should be read as a grayscale matrix
        self.image = cv2.imread(self.name_image, 0)
        # binary image over threshold
        self.image_bw = self.bin_array(np.array(self.image))

    @staticmethod
    def bin_array(numpy_array, threshold=128, background=0):
        """
		"binarize" a numpy array

		background = 0 : change background to Black "white background images"
		background = 1 : keep black background "black background images"

		else just convert over the threshold
		"""
        for i in range(len(numpy_array)):
            for j in range(len(numpy_array[0])):
                if background == 0:
                    numpy_array[i][j] = 0 if numpy_array[i][j] > threshold else 255
                else:
                    numpy_array[i][j] = 255 if numpy_array[i][j] > threshold else 0
        return numpy_array

    @staticmethod
    def clean_image(image, min_size):
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
        sizes = stats[1:, -1]
        nb_components = nb_components - 1
        pb = ProgressBar(
            total=nb_components - 1, prefix='cleaning little fringes:',
            suffix='Done', decimals=3, length=50, fill='X', zfill='-')
        img2 = output.copy()
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] < min_size:
                img2[output == i + 1] = 0
            pb.print_progress_bar(i)
        return img2

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
        m450kx = "450kx" in self.name_image
        m590kx = "590kx" in self.name_image
        m690kx = "690kx" in self.name_image
        print("cleaning noisy elements from image...")
        if m450kx:
            # diagonal perfecta 21.41
            min_size = 22
            self.image_bw = self.clean_image(self.image_bw, min_size)
            self.cte = 40.8
            print("\nResolution: M450kx")
        if m590kx:
            # diagonal perfecta 18.31
            min_size = 19
            self.image_bw = self.clean_image(self.image_bw, min_size)
            self.cte = 53.6
            print("\nResolution: M590kx")
        if m690kx:
            # perfecta 13.93
            min_size = 14
            self.image_bw = self.clean_image(self.image_bw, min_size)
            self.cte = 62.7
            print("\nResolution: M690kx")

    def process_lc(self):
        self.filter_sizes()
        labels = self.image_bw
        final_label = np.zeros((len(labels), len(labels[0])))
        print(len(final_label), len(final_label[0]))
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
                final_label[x1:x2, y1:y2] = region.image
                pass
            index += 1
            pass
        name_aux = self.name_image.split('.')
        df.to_excel(name_aux[0] + "_fringes.xlsx", index=False)

        definitive = final_label * 255
        complementary = np.subtract(self.image_bw, definitive)

        im = Image.fromarray(definitive)
        im.save(name_aux[0] + "_final." + name_aux[1])

        im = Image.fromarray(complementary)
        im.save(name_aux[0] + "_del." + name_aux[1])



