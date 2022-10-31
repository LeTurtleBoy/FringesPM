import numpy as np
from skimage import measure, morphology
from PIL import Image
import pandas as pd
import os.path


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
        aux = np.asarray(Image.open(self.name_image).convert("L"), dtype=np.uint16)
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
    def bin_array_2(numpy_array):
        """
        "binarize" a numpy array

        background = 0 : change background to Black "white background images"
        background = 1 : keep black background "black background images"

        else just convert over the threshold
        """
        numpy_array = np.where(numpy_array == True, 255, 0)
        return numpy_array

    @staticmethod
    def find_size(image, start):
        dis = 0
        y = start[0]
        x = start[1]
        end = 1
        while end != 0:
            new_down = True if image[y - 1][x] != 0 else False
            new_down_right = True if image[y - 1][x + 1] != 0 else False
            right = True if image[y][x + 1] != 0 else False
            new_up_right = True if image[y + 1][x + 1] != 0 else False
            new_up = True if image[y + 1][x] != 0 else False
            new_up_left = True if image[y + 1][x - 1] != 0 else False
            left = True if image[y][x - 1] != 0 else False
            new_down_left = True if image[y - 1][x - 1] != 0 else False

            end = (
                new_down + new_down_right + right + new_up_right + new_up + new_up_left + left + new_down_left
            )
            if end == 0:
                return dis
            else:
                if new_down:
                    dis = dis + 1
                    image[y][x] = 0
                    y = y - 1

                if new_up:
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

                if new_down_left:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x - 1
                    y = y - 1

                if new_down_right:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x + 1
                    y = y - 1

                if new_up_left:
                    dis = dis + np.sqrt(2)
                    image[y][x] = 0
                    x = x - 1
                    y = y + 1

                if new_up_right:
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
            df = pd.DataFrame(
                columns=[
                    "image",
                    "coord_start_x",
                    "coord_start_y",
                    "coord_end_x",
                    "coord_end_y" "c",
                    "l",
                    "c/l",
                ]
            )
            # df_rejected = pd.DataFrame(columns=['image', 'coord_start', 'coord_end', 'c', 'l'])
            index = 0
            a = measure.regionprops(labels)
            bar = len(a) - 1
            print("isolating and measuring fringes!")
            counter = -1
            for region in a:
                counter += 1
                img_aux = region.image

                """
                Logica para generar una region para el fringe ( Box que lo envuelve )
                0 0 0 0 0 0 0 0
                0 1 0 0 0 0 0 0
                0 0 1 0 0 0 0 0
                0 0 0 1 0 0 0 0 
                0 0 0 0 1 1 0 0
                0 0 0 0 0 0 1 0
                0 0 0 0 0 0 0 0
                """

                base = np.zeros([len(img_aux) + 2, len(img_aux[0]) + 2])
                x = 0
                for pixinfo in img_aux:
                    y = 0
                    for element in pixinfo:
                        base[x + 1][y + 1] = 1 if element else 0
                        y += 1
                    x += 1
                aux = base.copy()

                """
                logica para generar vector de vecinos
                0 0 0 0 0 0 0 0
                0 1 0 0 0 0 0 0
                0 0 2 0 0 0 0 0
                0 0 0 2 0 0 0 0 
                0 0 0 0 2 2 0 0
                0 0 0 0 0 0 1 0
                0 0 0 0 0 0 0 0
                """
                for x in range(len(base)):
                    for y in range(len(base[0])):
                        if base[x][y] == 1:
                            aux[x][y] = (
                                base[x - 1][y - 1]
                                + base[x - 1][y]
                                + base[x - 1][y + 1]
                                + base[x][y - 1]
                                + base[x + 1][y - 1]
                                + base[x + 1][y]
                                + base[x + 1][y + 1]
                                + base[x][y + 1]
                            )
                        else:
                            pass

                u = 0
                k = 0
                alpha = []
                omega = []
                # buscar mas de 2 vecinos
                # max([max(i) for i in aux])

                # buscar mas de 2 inicios
                # sum([list(i).count(1) for i in aux])

                # Buscar las coordenadas de inicio y de final
                # eliminando aquellos elementos con mas de un inicio o mas de un final

                heads = sum([list(i).count(1) for i in aux])
                max_neigh = max([max(i) for i in aux])

                if heads != 2 or max_neigh != 2:
                    continue

                else:
                    row = 0
                    alpha = []
                    omega = []
                    for data_row in aux:
                        if 1 in data_row:
                            if len(alpha) == 0:
                                alpha = [row, list(data_row).index(1)]
                                try:
                                    omega = [row, list(data_row).index(1, alpha[1] + 1)]
                                    break
                                except ValueError:
                                    pass
                            else:
                                omega = [row, list(data_row).index(1)]
                        row += 1
                longitude = np.sqrt(np.power((alpha[0] - omega[0]), 2) + np.power((alpha[1] - omega[1]), 2))
                curvature = self.find_size(aux, alpha)
                ori = np.rad2deg(region.orientation)
                df = df.append(
                    {
                        "image": index,
                        "coord_start_x": alpha[0],
                        "coord_start_y": alpha[1],
                        "coord_end_x": omega[0],
                        "coord_end_y": omega[1],
                        "c": curvature,
                        "l": longitude,
                        "c/l": curvature / longitude,
                        "orientation": ori,
                    },
                    ignore_index=True,
                )

                x1 = region.bbox[0]
                x2 = region.bbox[2]
                y1 = region.bbox[1]
                y2 = region.bbox[3]
                final_label[x1:x2, y1:y2] = final_label[x1:x2, y1:y2] + region.image

                if (-45 < ori) & (ori < 45):
                    final_label_v[x1:x2, y1:y2] = final_label_v[x1:x2, y1:y2] + region.image
                else:
                    final_label_h[x1:x2, y1:y2] = final_label_h[x1:x2, y1:y2] + region.image

                final_label[x1:x2, y1:y2] = region.image
                index += 1

            name_aux = self.name_image.split(".")
            df.to_csv(name_aux[0] + "_fringes.csv", index=False)

            definitive = final_label * 255

            Image.fromarray(final_label_v * 255).convert("1").save(name_aux[0] + "_v.png")
            Image.fromarray(final_label_h * 255).convert("1").save(name_aux[0] + "_h.png")
            Image.fromarray(definitive).convert("1").save(name_aux[0] + "_final.png")

            bad_f = self.original - final_label_h * 255 - final_label_v * 255
            Image.fromarray(bad_f).convert("1").save(name_aux[0] + "_bad.png")

        else:
            print("First load any valid image")
        print("Done!")

    def load_inter_distance(self, dir_image):
        name_aux = dir_image.split(".")
        print("Loading {} vertical and horizontal...".format(name_aux[0]))
        if os.path.isfile(name_aux[0] + "_h.png"):
            self.image_h = self.bin_array_2(np.array(Image.open(name_aux[0] + "_h.png")), background=1)
            self.process_id("Horizontal", measure.label(self.image_h))
        if os.path.isfile(name_aux[0] + "_v.png"):
            self.image_v = self.bin_array_2(np.array(Image.open(name_aux[0] + "_v.png")), background=1)
            self.process_id("Vertical", measure.label(self.image_v))
        if self.image_v == []:
            print("no hay imagenes verticales")
        if self.image_h == []:
            print("no hay imagenes horizontales")
        if (self.image_v == []) & (self.image_h == []):
            print("No hay imagenes procesadas Horizontales o Verticales")
            return 0

    def process_id_old(self, mode):
        if mode == "Horizontal":
            info_image_struct = measure.regionprops(self.image_h)
            for region in info_image_struct:
                image_masked = self.image_h.copy()
                aux = np.zeros((len(image_masked), len(image_masked[0])))
                n = 100
                aux[
                    (region.bbox[0] - n) : (region.bbox[2] + n), (region.bbox[1] - n) : (region.bbox[3] + n)
                ] = 1
                image_masked[aux == 0] = 0
                I, J = np.nonzero(image_masked)
                F = [[0, 0, 0]] * len(I)
                for x in range(len(I)):
                    F[x] = [image_masked[I[x]][J[x]], I[x], J[x]]
                df = pd.DataFrame(F, columns=["Fringe_label", "x", "y"])
                groups = df.groupby("Fringe_label")
                data_size = len(groups.groups)
                Vector = [0] * data_size
                u = 0
                for ref, df in groups:
                    Vector[u] = df.values
                    u += 1
                pure_data = []
                n = 0
                for i in range(1):
                    name = (
                        "process fringe "
                        + str(region.label)
                        + " with "
                        + str(len(Vector) - 1)
                        + " possible couples"
                    )
                    total_it = len(Vector) - i
                    for j in range(i + 1, len(Vector)):
                        l = 0
                        base = Vector[i]
                        aux = Vector[j]
                        for pixinfo in base:
                            aux_data = []
                            old_distance = 0
                            for pixinfo_ in aux:
                                a = pixinfo_[1] - pixinfo[1]
                                b = pixinfo_[2] - pixinfo[2]
                                if a == 0:
                                    angle = np.pi / 2 * np.sign(b)
                                elif b == 0:
                                    angle = np.pi * int(x < 0)
                                else:
                                    angle = np.arctan(b / a)
                                # Necessary rotation to reference in traditional coords(x,y)
                                angle = angle - (np.pi / 2)
                                angle = angle * (180.0 / np.pi)
                                distance = np.sqrt((a) ** 2 + (b) ** 2)
                                if (
                                    (distance > 60)
                                    | (angle > 135)
                                    | (angle < -135)
                                    | ((angle < 45) & (angle > -45))
                                ):
                                    break
                                else:
                                    if aux_data == []:
                                        aux_data = [
                                            pixinfo[0],
                                            pixinfo[1],
                                            pixinfo[2],
                                            pixinfo_[0],
                                            pixinfo_[1],
                                            pixinfo_[2],
                                            distance,
                                            angle,
                                        ]
                                        old_distance = distance
                                    else:
                                        if distance < old_distance:
                                            aux_data = [
                                                pixinfo[0],
                                                pixinfo[1],
                                                pixinfo[2],
                                                pixinfo_[0],
                                                pixinfo_[1],
                                                pixinfo_[2],
                                                distance,
                                                angle,
                                            ]
                                            old_distance = distance
                                    l -= -1
                            if aux_data != []:
                                if pure_data != []:
                                    pure_data.append(aux_data)
                                else:
                                    pure_data = [aux_data]
                                n -= -1
                if pure_data != []:
                    a = pd.DataFrame(pure_data)
                    a.to_csv("indis_fringe" + str(region.label) + ".csv", index=False)
                else:
                    print("not fringe in range for interplanar distance")
                self.image_h = np.where(self.image_h == region.label, 0, self.image_h)

    def process_id(self, path):
        pass
