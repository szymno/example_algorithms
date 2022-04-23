import math


class PriorityQueue:
    def __init__(self, array=None, max_size=100):
        if array is None:
            self.heap_size = 0
            self.heap_array = [None for _ in range(max_size)]
        else:
            self.heap_array = array
            self.heap_size = len(array)
            self.build_heap()

    def insert(self, item):
        node_index = self.heap_size
        self.heap_size += 1

        while node_index > 0 and self.heap_array[self.parent(node_index)][1] > item[1]:
            self.heap_array[node_index] = self.heap_array[self.parent(node_index)]
            node_index = self.parent(node_index)
        self.heap_array[node_index] = item

    def build_heap(self):
        for index in range(self.heap_size // 2 - 1, -1, -1):
            self.heapify(index)

    def heapify(self, node_index):
        left_child_index = self.left_child(node_index)
        right_child_index = self.right_child(node_index)
        if left_child_index < self.heap_size and self.heap_array[left_child_index][1] < self.heap_array[node_index][1]:
            smallest_index = left_child_index
        else:
            smallest_index = node_index

        if (right_child_index < self.heap_size
                and self.heap_array[right_child_index][1] < self.heap_array[smallest_index][1]):
            smallest_index = right_child_index

        if smallest_index != node_index:
            self.heap_array[node_index], self.heap_array[smallest_index] = (self.heap_array[smallest_index],
                                                                            self.heap_array[node_index])
            self.heapify(smallest_index)

    def extract_min(self):
        if not self.heap_size:
            return None
        minimum = self.heap_array[0]
        self.heap_size -= 1
        self.heap_array[0], self.heap_array[self.heap_size] = self.heap_array[self.heap_size], self.heap_array[0]
        self.heapify(0)
        self.heap_array[self.heap_size] = None
        return minimum

    @staticmethod
    def parent(node_index):
        return math.ceil((node_index - 1) / 2)

    @staticmethod
    def left_child(node_index):
        return 2 * node_index + 1

    @staticmethod
    def right_child(node_index):
        return 2 * (node_index + 1)


class HuffmanCode:
    def __init__(self):
        self.character_frequency = dict()
        self.code_dictionary = dict()

    def _get_heap_path(self):
        huffman_heap = PriorityQueue(list(self.character_frequency.items()))
        while huffman_heap.heap_size != 1:
            node_1 = huffman_heap.extract_min()
            node_2 = huffman_heap.extract_min()
            node_x = ((node_1, node_2), node_2[1] + node_1[1])
            huffman_heap.insert(node_x)
        return huffman_heap.extract_min()

    def _read_character_frequency(self, text):
        for character in text:
            if character not in self.character_frequency.keys():
                self.character_frequency[character] = 1
            else:
                self.character_frequency[character] += 1

    def _get_code(self, level, current_code=""):
        if not isinstance(level[0], tuple):
            self.code_dictionary[level[0]] = current_code
        else:
            self._get_code(level[0][0], current_code + "0")
            self._get_code(level[0][1], current_code + "1")

    def _create(self, text):
        self._read_character_frequency(text)
        self._get_code(self._get_heap_path())

    def encode_text(self, text):
        self._create(text)
        encoded_text = ""
        for character in text:
            encoded_text += self.code_dictionary[character]
        return encoded_text


huffman = HuffmanCode()
input_text = input("Input text to encode: ")

encoded = huffman.encode_text(input_text)
print("encoded text: ", encoded)
print("compression ratio: ", len(input_text) * 8 / len(encoded))
print("codes for symbols:")
for symbol, code in huffman.code_dictionary.items():
    print(f"\t\t'{symbol}':\t{code}")



