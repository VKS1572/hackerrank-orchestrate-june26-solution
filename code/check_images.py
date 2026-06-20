import os

count = 0

for root, dirs, files in os.walk("dataset/images"):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            count += 1

print("Total Images:", count)