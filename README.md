# Digital Image Processing — Filters & Compression

## Folder Structure
- `filters/` 
  - `1_mean_filter_hsi.py`
  - `2_gaussian_filter_hsi.py`
  - `3_median_filter_hsi.py`
  - `4_laplacian_filter_hsi.py`
  - `5_sobel_filter_hsi.py`
  - `input.jpg` 
- `compression/`  
  - `huffman_coding.py`
  - `arithmetic_coding.py`

## Setup & Usage
1. Install dependencies (needed only for the image filter scripts):
   ```bash
   pip install -r requirements.txt
   ```
2. Run any filter script (each displays Input vs. Output and saves the filtered output image):
   ```bash
   python filters/1_mean_filter_hsi.py
   ```
3. Run either compression script:
   ```bash
   python compression/huffman_coding.py
   python compression/arithmetic_coding.py
   ```
