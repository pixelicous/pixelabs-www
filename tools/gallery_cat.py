# Gallery Cat
# A script by Pixel to get photo data and resize images for pixelabs website

import os, logging
from photo_functions import *
from PIL import Image

# Logger
LOG_LEVEL = os.environ.get("GALLERY_RUNNER_LOG_LEVEL", default="INFO").upper()
LOG_NUM_LEVEL = getattr(logging, LOG_LEVEL, None)

if not isinstance(LOG_NUM_LEVEL, int):
    raise ValueError('Invalid log level: %s' % LOG_LEVEL)

logging.basicConfig(level=LOG_NUM_LEVEL)

log = logging.getLogger('pixelogger')

# Logger handler setup
if (log.hasHandlers()):
    logging.getLogger().handlers.clear()

log.setLevel(getattr(logging, LOG_LEVEL))
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(formatter)
log.addHandler(console)

# Overwrite variables
ENABLE_PHOTO_RESIZE = bool(os.environ.get(f"GALLERY_RUNNER_PHOTO_RESIZE", default=True))
ENABLE_PHOTO_HISTOGRAM_CREATE = bool(os.environ.get(f"GALLERY_RUNNER_PHOTO_HISTORGRAM", default=True))
YAML_OVERWRITE = bool(os.environ.get(f"GALLERY_RUNNER_OVERWRITE_YAML", default=False))
RESIZE_OVERWRITE = bool(os.environ.get(f"GALLERY_RUNNER_OVERWRITE_RESIZE", default=False))
HISTOGRAM_OVERWRITE = bool(os.environ.get(f"GALLERY_RUNNER_OVERWRITE_HISTOGRAM", default=False))
ENABLE_PHOTO_ORIGINALS_CLEANUP = bool(os.environ.get(f"GALLERY_RUNNER_CLEAN_ORIGINALS", default=False))
# Root location to run
GALLERY_ROOT_PATH = "./assets/portfolio"
SIZES_STRING_LIST = ', '.join([size for size in PHOTO_SIZES])
EXTRA_FOLDERS = ['histogram']

# Clean resized photos at beginning
#os.chdir(root_path)
#print(clean_resized_folders(GALLERY_ROOT_PATH))
#os.chdir(root_path)
log.debug(f"Histogram enabled: {ENABLE_PHOTO_HISTOGRAM_CREATE}")
log.debug(f"resize enabled: {ENABLE_PHOTO_RESIZE}")
log.debug(f"Histogram overwrite yaml: {YAML_OVERWRITE}")
log.debug(f"Histogram overwrite resize: {RESIZE_OVERWRITE}")
# Find all main portfolio paths under assets
portfolio_paths = [f.path for f in os.scandir(GALLERY_ROOT_PATH) if f.is_dir()]

# Create relevant size directories per folder
log.info(f"#1 Creating {SIZES_STRING_LIST} directories for portfolio directories")
for portfolio_root in portfolio_paths:
    for portfolio_dirname in os.scandir(portfolio_root):
        # Ignoring local OSX paths if any
        if portfolio_dirname.name.lower() != '.ds_store':
            new_paths_created = [] # Variable to print out which directories where need to be created
            # Check if various sizes directories exist
            portfolio_dir_root_path = os.path.basename(os.path.dirname(portfolio_dirname))
            gallery_path = os.path.join(portfolio_dirname)      
            for photo_size in PHOTO_SIZES:
                photo_size_path = os.path.join(portfolio_dirname, photo_size)      
                if not os.path.isdir(photo_size_path):
                    try:
                        log.debug(f"Creating: {photo_size_path}")
                        os.makedirs(photo_size_path)
                        new_paths_created.append(photo_size)
                    except OSError as e:
                        log.warning(f"Error raised while creating {photo_size_path} : {e}")
                else:
                    log.debug(f"Folder {photo_size} already created, skipping")
                    sync_removed_photos(photo_size_path, gallery_path)
                    
            new_paths_created = ", ".join(new_paths_created)
            if len(new_paths_created) != 0:
                log.info(f"Created {new_paths_created} directories for {portfolio_dir_root_path}/{os.path.basename(portfolio_dirname)}")
        else:
            log.debug(f"Ignoring: {portfolio_dirname}")
         
log.info(f"#2 Resizing images and saving in {SIZES_STRING_LIST} directories")
# Resize images into relevant size folders
for root, dirs, files in os.walk(GALLERY_ROOT_PATH):
    for filename in filter(filter_unwanted_images, files):
        full_path = os.path.join(root, filename)
        directory_name = os.path.basename(os.path.dirname(full_path))
        directory_path = os.path.dirname(full_path)

        # Don't resize the resized photos
        if directory_name not in PHOTO_SIZES:
            try:
                img = Image.open(full_path)
            except IOError as e:
                log.error(f"Error opening {full_path}")
            
            # Get photo alignment for resize function later
            if img.size[0] > img.size[1]:
                image_alignment = "wide"
            elif img.size[0] < img.size[1]:
                image_alignment = "tall"
            elif img.size[0] == img.size[1]:
                image_alignment = "square"
            else:
                log.warning(f"Error getting image size of {full_path}")
            
            # Don't get information for an histogram photo
            if 'histogram' not in filename and 'histogram' not in full_path: 
                # Only generate information for photographs
                if ENABLE_PHOTO_RESIZE:
                    log.info(f"Legitimate for resizing: {full_path}")
                    log.debug(f"Original size {img.size}")
                    resize_image(root, full_path, image_alignment, RESIZE_OVERWRITE)
                if "photography" in full_path:
                    # Generate other folders not related to sizes (not to mix up lists)
                    for extra_folder in EXTRA_FOLDERS:
                        extra_folder_path = os.path.join(directory_path, extra_folder)
                        if not os.path.isdir(extra_folder_path):
                            try:
                                log.debug(f"Creating: {extra_folder_path}")
                                os.makedirs(extra_folder_path)
                            except OSError as e:
                                log.critical(f"Error raised while creating {extra_folder_path} : {e}")
                        else:
                            pass     
                    if ENABLE_PHOTO_HISTOGRAM_CREATE:
                        log.info(f"Photography file: {full_path} - Exporting image data and histogram")
                        export_photo_exif_data(img, full_path, YAML_OVERWRITE)
                        histo_path = os.path.join(directory_path, 'thumb', filename)
                        export_photo_histogram(full_path, histo_path, HISTOGRAM_OVERWRITE)
                        
                if ENABLE_PHOTO_ORIGINALS_CLEANUP:
                    try:
                        log.info(f"Cleaning up originals before caching: {full_path}")
                        os.remove(full_path)
                        if not os.path.isfile(full_path):
                            log.debug(f"Cleaned {full_path} successfully")
                    except:
                        log.debug(f"Clean error: {full_path}")
            else:
                log.debug(f"Ignoring: {full_path}")



