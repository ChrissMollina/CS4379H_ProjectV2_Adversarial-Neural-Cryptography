"""
Quick test script to load earth.jpg from Desktop and sign/verify it.
"""

import numpy as np
from PIL import Image
import os
from neural_image_auth.inference import NeuralImageAuthenticator
from neural_image_auth.models.alice import create_alice_network
from neural_image_auth.models.bob import create_bob_network

# Path to your image
image_path = os.path.expanduser("~/Desktop/earth.jpg")

# Check if image exists
if not os.path.exists(image_path):
    print(f"❌ Error: Image not found at {image_path}")
    exit(1)

print(f"✓ Loading image from: {image_path}")

# Load the image
image = Image.open(image_path)
print(f"✓ Image shape (before resize): {image.size}")

# Convert to numpy array
image_array = np.array(image)
print(f"✓ Image array shape: {image_array.shape}")
print(f"✓ Image value range: [{image_array.min()}, {image_array.max()}]")

# Create the authenticator
print("\n✓ Creating neural networks...")
alice = create_alice_network()
bob = create_bob_network()

# Set up AES key
aes_key = b'sixteen_byte_key'  # 16 bytes for AES-128

print("✓ Initializing authenticator...")
auth = NeuralImageAuthenticator(alice, bob, aes_key)

# Sign your image
print("\n✓ Signing image with message 'EARTH_AUTHENTIC'...")
signed_image = auth.sign_image(image_array, message="EARTH_AUTHENTIC")
print(f"✓ Signed image shape: {signed_image.shape}")

# Verify the image
print("\n✓ Verifying image...")
result = auth.verify_image(signed_image)

print("\n" + "="*50)
print("VERIFICATION RESULTS")
print("="*50)
print(f"Authentic: {result['is_authentic']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Extracted Message: {result['extracted_message']}")
print(f"Bit Error Rate: {result['bit_error_rate']:.2%}")
print("="*50)

# Optionally save the signed image
output_path = os.path.expanduser("~/Desktop/earth_signed.jpg")
signed_image_pil = Image.fromarray(signed_image.astype(np.uint8))
signed_image_pil.save(output_path)
print(f"\n✓ Signed image saved to: {output_path}")
