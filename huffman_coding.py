import heapq
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix or "0"
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map


def huffman_encode(text):
    if not text:
        return "", {}, None
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    encoded_text = "".join(codes[ch] for ch in text)
    return encoded_text, codes, root


def huffman_decode(encoded_text, root):
    if not encoded_text or root is None:
        return ""
    decoded = []
    curr = root
    for bit in encoded_text:
        curr = curr.left if bit == "0" else curr.right
        if curr.char is not None:
            decoded.append(curr.char)
            curr = root
    return "".join(decoded)


if __name__ == "__main__":
    data = "HUFFMAN CODING"
    encoded, codes, tree = huffman_encode(data)
    decoded = huffman_decode(encoded, tree)

    print("Original:", data)
    print("Codes:   ", codes)
    print("Encoded: ", encoded)
    print("Decoded: ", decoded)
