from collections import Counter
from decimal import Decimal, getcontext

# Set high precision for longer strings
getcontext().prec = 50


def get_probability_ranges(text):
    total = Decimal(len(text))
    freq = Counter(text)
    ranges = {}
    low = Decimal(0)

    for char, count in sorted(freq.items()):
        prob = Decimal(count) / total
        ranges[char] = (low, low + prob)
        low += prob
    return ranges


def arithmetic_encode(text):
    if not text:
        return Decimal(0), {}, 0
    ranges = get_probability_ranges(text)
    low = Decimal(0)
    high = Decimal(1)

    for char in text:
        range_width = high - low
        char_low, char_high = ranges[char]
        high = low + range_width * char_high
        low = low + range_width * char_low

    # Any number in [low, high) represents the message; midpoint is standard
    encoded_value = (low + high) / Decimal(2)
    return encoded_value, ranges, len(text)


def arithmetic_decode(encoded_value, ranges, length):
    decoded = []
    value = encoded_value

    for _ in range(length):
        for char, (char_low, char_high) in ranges.items():
            if char_low <= value < char_high:
                decoded.append(char)
                value = (value - char_low) / (char_high - char_low)
                break

    return "".join(decoded)


if __name__ == "__main__":
    data = "ARITHMETIC"
    encoded_val, ranges, length = arithmetic_encode(data)
    decoded_str = arithmetic_decode(encoded_val, ranges, length)

    print("Original:     ", data)
    print("Encoded Value:", encoded_val)
    print("Decoded:      ", decoded_str)
