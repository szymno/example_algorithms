from PIL import Image, ImageOps


class ImageProcessing:
    def __init__(self, image):
        self.image = Image.open(image)

    #  Histogram equalization

    def histogram_equalization(self):
        counter = {x: 0 for x in range(256)}

        for x in range(self.image.width):
            for y in range(self.image.height):
                counter[round(sum(self.image.getpixel((x, y))) / 3)] += 1

        for i in range(1, 256):
            counter[i] += counter[i - 1]

        minimum = min(counter.values(), key=lambda c: (not c, c))
        multiply_constant = 255 / (self.image.width * self.image.height - minimum)

        normalized = {i: round(multiply_constant * (counter[i] - minimum)) for i in range(256)}

        for x in range(self.image.width):
            for y in range(self.image.height):
                self.image.putpixel((x, y), tuple(normalized[round(sum(self.image.getpixel((x, y))) / 3)]
                                                  for _ in range(3)))

    # thresholding

    def calculate_threshold(self):
        for x in range(self.image.width):
            for y in range(self.image.height):
                pixel = self.image.getpixel((x, y))
                self.image.putpixel((x, y), self._pixel_single_threshold(pixel))

    @staticmethod
    def _pixel_single_threshold(rgb_values, threshold=120):
        if sum(rgb_values) / 3 < threshold:
            return 0, 0, 0
        return 255, 255, 255

    #  mean filtering

    def _summed_area_pixels(self):
        summed_table = [[255 for _ in range(self.image.height)]
                        for _ in range(self.image.width)]

        for x in range(1, self.image.width):
            for y in range(1, self.image.height):
                summed_table[x][y] = (sum(self.image.getpixel((x, y))) // 3
                                      + summed_table[x - 1][y]
                                      + summed_table[x][y - 1]
                                      - summed_table[x - 1][y - 1])

        return summed_table

    def mean_filter(self, mask):
        division_part = 1 / pow(mask, 2)

        mask = mask - 1
        self.image = ImageOps.expand(self.image, mask, (127, 127, 127))

        summed_table = self._summed_area_pixels()

        mask = mask // 2
        for x in range(mask, self.image.width - mask):
            for y in range(mask, self.image.height - mask):
                self.image.putpixel((x, y),
                                    tuple([int((summed_table[x + mask][y + mask]
                                                - summed_table[x - 1][y + mask]
                                                - summed_table[x + mask][y - 1]
                                                + summed_table[x - 1][y - 1]) * division_part) for _ in range(3)]))


if __name__ == "__main__":
    black_and_white = ImageProcessing("yoda.jpeg")
    black_and_white.calculate_threshold()
    black_and_white.image.show()

    histogram = ImageProcessing("yoda.jpeg")
    histogram.histogram_equalization()
    histogram.image.show()

    mean_filter = ImageProcessing("road.jpg")
    mean_filter.mean_filter(71)
    mean_filter.image.show()
