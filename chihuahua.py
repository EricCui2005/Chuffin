#@title Chihuahua Image Scraping

"""URL Scraping"""
API_KEY = 'AIzaSyAS-u_0MjNx8wfyydLcRB0VTdKXNZ0GgiU'
SEARCH_ENGINE_ID = 'b45c4833ea6a64914'
SEARCH_QUERY = 'chihuahua'  # or your search term

image_links = []

for i in range(0, 300, 10):  # Start parameter for pagination (0, 10, 20, ..., 190)
    url = f'https://www.googleapis.com/customsearch/v1?q={SEARCH_QUERY}&cx={SEARCH_ENGINE_ID}&key={API_KEY}&searchType=image&start={i+1}'

    response = requests.get(url)
    result = response.json()

    # Extracting image URLs and adding them to the list
    image_links.extend(item['link'] for item in result.get('items', []))

    # Check if less than 10 results were returned in the last request; if so, break out of the loop
    if len(result.get('items', [])) < 10:
        break
# Note: Ensure you have enough quota to make multiple requests


"""URL Cleaning"""


# Function to check if the URL strictly ends with .jpg, .jpeg, or .png
def strict_image_url_check(url):
    # Split the URL to remove query parameters and fragments
    base_url = url.split('?')[0].split('#')[0]
    return base_url.lower().endswith(('.jpg', '.jpeg', '.png'))

# Filter the list of URLs
strict_filtered_urls = [url for url in image_links if strict_image_url_check(url)]

# # Print or use the strictly filtered URLs
# for url in image_links:
#   print(url)

"""Clearing Colab Download Folder"""

# Specify the folder you want to clear
folder_path = '/content/Chihuahua'  # Change this to your folder path

# Check if the folder exists
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # List all files and directories in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # If it is a file, delete it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it is a directory, delete it and all its contents
            elif os.path.isdir(file_path):
                # For deleting directories and their contents, you can use shutil.rmtree
                import shutil
                shutil.rmtree(file_path)
            print(f"{file_path} is deleted.")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
else:
    print(f"The specified path does not exist: {folder_path}")

"""Downloading Images from URLs"""

# Folder where you want to save the images
save_folder = "/content/Chihuahua"

# Create the folder if it doesn't already exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Function to download an image from a URL
def download_image(image_url, save_folder, timeout=3):
    try:
        image_name = image_url.split("/")[-1]
        save_path = os.path.join(save_folder, image_name)
        
        # Add a timeout parameter to the request
        response = requests.get(image_url, timeout=timeout)
        
        response.raise_for_status()
        
        with open(save_path, 'wb') as image_file:
            image_file.write(response.content)
            
        print(f"Successfully downloaded {image_name}")
    except requests.exceptions.Timeout:
        print(f"Request timed out for {image_url}. Skipping...")
    except requests.exceptions.RequestException as e:
        # Catches other requests-related exceptions
        print(f"Error downloading {image_url}: {e}")


# Loop through the image URLs and download each image
for url in image_links:
    download_image(url, save_folder)
