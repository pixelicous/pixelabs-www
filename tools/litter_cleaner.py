# Gallery Cat
# A script by Pixel to get photo data and resize images for pixelabs website

import os, logging

# Logger
LOG_LEVEL = os.environ.get("GALLERY_RUNNER_LOG_LEVEL", default="INFO").upper()
LOG_NUM_LEVEL = getattr(logging, LOG_LEVEL, None)

PHOTO_SIZES = {
        "thumb": { "width": "300", "height": "200" },
        "sm": { "width": "450", "height": "300" },
        "md": { "width": "900", "height": "600" },
        "lg": { "width": "1800", "height": "1200" }
        }

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

# Root location to run
GALLERY_ROOT_PATH = "./assets/portfolio"

SIZES_STRING_LIST = ', '.join([size for size in PHOTO_SIZES])
EXTRA_FOLDERS = ['histogram']

# Find all main portfolio paths under assets
portfolio_paths = [f.path for f in os.scandir(GALLERY_ROOT_PATH) if f.is_dir()]
         
log.info(f"## CLEAN UP INITIATED")
# Resize images into relevant size folders
for root, dirs, files in os.walk(GALLERY_ROOT_PATH):
    for filename in filter(filter_unwanted_images, files):
        full_path = os.path.join(root, filename)
        directory_name = os.path.basename(os.path.dirname(full_path))
        directory_path = os.path.dirname(full_path)

        # Don't resize the resized photos
        if directory_name not in PHOTO_SIZES:
            if ('histogram' not in filename or 'header' not in filename ) and 'histogram' not in full_path: 
                try:
                    log.info(f"Cleaning up originals: {full_path}")
                    os.remove(full_path)
                    if not os.path.isfile(full_path):
                        log.debug(f"Cleaned {full_path} successfully")
                except OSError as e: # name the Exception `e`
                    log.debug(f"Clean error: {e.strerror}")
                    log.debug(f"Error code: {e.code }")
            else:
                log.debug(f"Ignoring: {full_path}")



