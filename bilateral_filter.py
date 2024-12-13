import time
import numpy as np
import random
import math
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def extract_and_flatten_channels(image_array):
    image_r = image_array[:, :, 0]
    image_g = image_array[:, :, 1]
    image_b = image_array[:, :, 2]

    image_r_colors = image_r.flatten().tolist()
    image_g_colors = image_g.flatten().tolist()
    image_b_colors = image_b.flatten().tolist()

    return (image_r, image_g, image_b), (image_r_colors, image_g_colors, image_b_colors)

def poisson_disk_sampling(image_colors, num_samples, radius):
    sampled_colors = []

    def is_valid_sample(new_color):
        for color in sampled_colors:
            if np.linalg.norm(np.array(color) - np.array(new_color)) < 2 * radius:
                return False
        return True

    while len(sampled_colors) < num_samples:
        candidate = random.choice(image_colors)
        if is_valid_sample(candidate):
            sampled_colors.append(candidate)
    return sampled_colors

def o1_gaussian_filter(image, sigma):
    return gaussian_filter(image, sigma)

def bilinear_interpolation(target_color, sampled_colors, filtered_components):
    distances = [np.linalg.norm(np.array(target_color) - np.array(color)) for color in sampled_colors]
    min_dist = min(distances) if distances else 1e-8
    weights = [np.exp(-d**2 / (2 * min_dist**2)) for d in distances]
    weighted_sum = sum(w * c for w, c in zip(weights, filtered_components))
    normalization_factor = sum(weights)
    return weighted_sum / normalization_factor if normalization_factor != 0 else 0

def process_image(image_array, num_samples, radius, sigma):
    start_time = time.perf_counter()

    (image_r, image_g, image_b), (image_r_colors, image_g_colors, image_b_colors) = extract_and_flatten_channels(image_array)

    t0 = time.perf_counter()
    sampled_r = poisson_disk_sampling(image_r_colors, num_samples, radius)
    sampled_g = poisson_disk_sampling(image_g_colors, num_samples, radius)
    sampled_b = poisson_disk_sampling(image_b_colors, num_samples, radius)
    t1 = time.perf_counter()
    print(f"Poisson disk sampling time: {t1 - t0:.4f} seconds")

    t0 = time.perf_counter()
    filtered_r = o1_gaussian_filter(image_r, sigma)
    filtered_g = o1_gaussian_filter(image_g, sigma)
    filtered_b = o1_gaussian_filter(image_b, sigma)
    t1 = time.perf_counter()
    print(f"Gaussian filtering time: {t1 - t0:.4f} seconds")

    target_r = random.choice(sampled_r)
    target_g = random.choice(sampled_g)
    target_b = random.choice(sampled_b)

    t0 = time.perf_counter()
    interpolated_r = bilinear_interpolation(target_r, sampled_r, filtered_r.flatten())
    interpolated_g = bilinear_interpolation(target_g, sampled_g, filtered_g.flatten())
    interpolated_b = bilinear_interpolation(target_b, sampled_b, filtered_b.flatten())
    t1 = time.perf_counter()
    print(f"Interpolation time: {t1 - t0:.4f} seconds")

    filtered_image = np.stack([filtered_r, filtered_g, filtered_b], axis=-1)

    end_time = time.perf_counter()
    print(f"Total processing time: {end_time - start_time:.4f} seconds")

    return filtered_image, (interpolated_r, interpolated_g, interpolated_b)

if __name__ == "__main__":
    image_path = 'shiba-1.jpg'
    image = Image.open(image_path)
    image_array = np.array(image)

    num_samples = 20
    radius = 4
    sigma = 0.9

    result_image, interpolated_values = process_image(image_array.astype(np.uint8), num_samples, radius, sigma)

    plt.imshow(image_array)
    plt.title("Original Image")
    plt.axis('off')
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.imshow(result_image.astype(np.uint8))
    plt.title("Filtered Color Image")
    plt.axis('off')
    plt.show()

    print("Interpolated values (R, G, B):", interpolated_values)
