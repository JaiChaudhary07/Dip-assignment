import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def rgb_to_hsi(rgb):
    """Convert an RGB uint8 image to HSI (H in [0, 2*pi], S and I in [0, 1])."""
    rgb = rgb.astype(np.float32) / 255.0
    R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    I = (R + G + B) / 3.0
    min_rgb = np.minimum(np.minimum(R, G), B)
    S = 1.0 - (3.0 / (R + G + B + 1e-6)) * min_rgb

    num = 0.5 * ((R - G) + (R - B))
    den = np.sqrt((R - G) ** 2 + (R - B) * (G - B)) + 1e-6
    theta = np.arccos(np.clip(num / den, -1.0, 1.0))
    H = np.where(B <= G, theta, 2 * np.pi - theta)

    return H, S, I


def hsi_to_rgb(H, S, I):
    """Convert HSI channels back to an RGB uint8 image."""
    R, G, B = np.zeros_like(H), np.zeros_like(H), np.zeros_like(H)

    # RG Sector (0 <= H < 2*pi/3)
    m1 = (H >= 0) & (H < 2 * np.pi / 3)
    B[m1] = I[m1] * (1 - S[m1])
    R[m1] = I[m1] * (1 + (S[m1] * np.cos(H[m1])) / (np.cos(np.pi / 3 - H[m1]) + 1e-6))
    G[m1] = 3 * I[m1] - (R[m1] + B[m1])

    # GB Sector (2*pi/3 <= H < 4*pi/3)
    m2 = (H >= 2 * np.pi / 3) & (H < 4 * np.pi / 3)
    H2 = H[m2] - 2 * np.pi / 3
    R[m2] = I[m2] * (1 - S[m2])
    G[m2] = I[m2] * (1 + (S[m2] * np.cos(H2)) / (np.cos(np.pi / 3 - H2) + 1e-6))
    B[m2] = 3 * I[m2] - (R[m2] + G[m2])

    # BR Sector (4*pi/3 <= H <= 2*pi)
    m3 = (H >= 4 * np.pi / 3) & (H <= 2 * np.pi)
    H3 = H[m3] - 4 * np.pi / 3
    G[m3] = I[m3] * (1 - S[m3])
    B[m3] = I[m3] * (1 + (S[m3] * np.cos(H3)) / (np.cos(np.pi / 3 - H3) + 1e-6))
    R[m3] = 3 * I[m3] - (G[m3] + B[m3])

    rgb = np.stack([R, G, B], axis=-1)
    return np.clip(rgb * 255.0, 0, 255).astype(np.uint8)


def load_input_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "input.jpg")
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Could not load image at {img_path}")
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    img_rgb = load_input_image()

    # Convert to HSI and apply Mean (Averaging) Filter on Intensity channel
    H, S, I = rgb_to_hsi(img_rgb)
    I_filtered = cv2.blur(I, (5, 5))

    # Convert back to RGB
    output_rgb = hsi_to_rgb(H, S, I_filtered)

    # Save output image
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_mean_hsi.jpg")
    cv2.imwrite(out_path, cv2.cvtColor(output_rgb, cv2.COLOR_RGB2BGR))

    # Display Input and Output
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title("Input Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(output_rgb)
    plt.title("Mean Filtered (HSI)")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
