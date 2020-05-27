import os, logging, yaml, datetime, cv2
from resizeimage import resizeimage
import numpy as np
from PIL import Image, ExifTags
from matplotlib import pyplot as plot
from skimage import io

log = logging.getLogger('pixelogger.photos')
log.propagate = True

YAML_DATA_FILES_PATH = "./_data/photography"

PHOTO_SIZES = {
        "sm": { "width": "300", "height": "900" },
        "md": { "width": "900", "height": "600" },
        "lg": { "width": "1800", "height": "1200" }
        }

def clean_resized_folders(folder):
    try:
        os.system('find {} -name "sm" -type d -exec rm -r "\{\}" \;'.format(folder))
        os.system('find {} -name "md" -type d -exec rm -r "\{\}" \;'.format(folder))
        os.system('find {} -name "lg" -type d -exec rm -r "\{\}" \;'.format(folder))
        return f"Successfully removed all resized photos folders"
    except Exception as e:
        return f"Error cleaning resized photos folders {e}"

def resize_image(root, full_path, alignment, overwrite=False):
        
    filename = os.path.basename(full_path)
    with open(full_path, 'r+b') as f:
        with Image.open(f) as image:
            # run on all sizes
            for size in PHOTO_SIZES:
                resized_photo_path = os.path.join(root, size, filename)
                # Check if resized photo already 
                if overwrite:
                    resize_to_size(alignment, image, resized_photo_path, size)
                elif not overwrite:
                    if not os.path.isfile(resized_photo_path):
                        resize_to_size(alignment, image, resized_photo_path, size)
                        log.debug(f"Resized {resized_photo_path} successfully")
                    else:
                        log.info(f"{size} size exists for photo {filename} and overwrite set to {overwrite}")

def resize_to_size(alignment, image, resized_photo_path, size):
    try:
        # Check photo alignment, change resizing resolution based on it
        if alignment == "wide" or alignment == "square":
            final_photo_size = [int(PHOTO_SIZES[size]['width']), int(PHOTO_SIZES[size]['height'])]
            basewidth = int(PHOTO_SIZES[size]['width'])
        elif alignment == "tall":
            basewidth = int(PHOTO_SIZES[size]['height'])
            final_photo_size = [int(PHOTO_SIZES[size]['height']), int(PHOTO_SIZES[size]['width'])]
        
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    except Exception as e:
        log.warning(f"Output format could not be determined {alignment} photo {image.name}.\r\nError: {e}")

    try:
        image.save(resized_photo_path, image.format, quality=95) 
    except KeyError as e:
        log.warning(f"Output format could not be determined {resized_photo_path}, format: {image.format}.\r\nError: {e}")
    except IOError as e:
        log.warning(f"Error writing file {resized_photo_path.name}.\r\nError: {e}")


def filter_unwanted_images(filename):
    # Get specific extensions only
    extensions=['.jpg', '.jpeg', '.gif', '.png']

    # Do not check images in folders of already resized images
    image_filtered = filename.endswith(tuple(extensions))
    
    return image_filtered

def export_photo_exif_data(img, full_path, overwrite=True):
    filename = os.path.splitext(os.path.basename(full_path))[0]
    file_path = os.path.dirname(full_path)
    file_dir_name = os.path.basename(file_path)
    # todo: create yaml path if it doesnt exist yet
    yaml_root_path = f"{YAML_DATA_FILES_PATH}/{file_dir_name}"
    yaml_file_path = f"{yaml_root_path}/{filename}.yml"

    # Check if yaml path exists
    # todo: take out of function to check if 
    #       yaml path exists only on the first file in directory
    if not os.path.isdir(yaml_root_path):
        try:
            os.makedirs(yaml_root_path)
            log.info(f"Created yaml path: {yaml_root_path}")
        except Exception as e:
            log.warning(f"Error creating yaml path: {yaml_root_path}")
    else:
        log.debug(f"Yaml path exists: {yaml_root_path}")

    try:
        exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
                }   
        
        data_dump = {}
        # todo: shift left test whether need to recreate file before getting exifdata
        # Strip photo creation time to get year only
        photo_time = datetime.datetime.strptime(exif["DateTimeOriginal"], '%Y:%m:%d  %H:%M:%S')
        try:
            data_dump["Shutter Speed"] = exif["ShutterSpeedValue"]
        except KeyError:
            pass
        try:
            data_dump["Year"] = photo_time.year
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Aperture"] = exif["ApertureValue"]
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Brightness"] = exif["BrightnessValue"]
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Camera"] = exif["Make"]
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Model"] = exif["Model"]
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Focal Length"] = exif["FocalLength"]
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Metering Mode"] = exif["MeteringMode"]
        except KeyError as e:
            log.debug(f"No exif key {e}")
        try:
            data_dump["Lens Specification"] = exif["LensSpecification"]
        except KeyError as e:
            log.debug(f"No exif key {e}")

        if overwrite:
            with open(yaml_file_path, 'w') as yml_file:
                try:
                    data = yaml.dump(data_dump, yml_file, default_flow_style=False)
                    log.debug(f"Dumping yaml for {yaml_file_path}")
                except yaml.YAMLError as e:
                    log.warning(f"Error dumping yaml for {yaml_file_path}")
                    
        elif not overwrite:
            if not os.path.isfile(yaml_file_path):
                with open(yaml_file_path, 'w') as yml_file:
                    try:
                        data = yaml.dump(data_dump, yml_file, default_flow_style=False)
                        log.debug(f"Dumping yaml for {yaml_file_path}")
                    except yaml.YAMLError as e:
                        log.warning(f"Error dumping yaml for {yaml_file_path}")
            else:
                log.debug(f"Yaml file exists and overwrite is set to false")
    except AttributeError as e:
        log.debug(f"Error getting exif data {e}")        

def export_photo_histogram(full_path, overwrite=False):
    filename = os.path.splitext(os.path.basename(full_path))[0]
    file_path = os.path.dirname(full_path)
    photo_histogram_file = f"{file_path}/histogram/{filename}.png"
    if overwrite:
        if 'histogram' not in filename:
            export_nice_histogram(full_path, photo_histogram_file)
            log.info(f"Outputing Histogram: {filename}")
    elif not overwrite:
        if not os.path.isfile(photo_histogram_file):
            export_nice_histogram(full_path, photo_histogram_file)
            log.info(f"Outputted Histogram: {filename}")
        else:
            log.debug(f"Histogram file exists and overwrite is set to false")
    
def export_nice_histogram(full_path, photo_histogram_file):
    image = io.imread(full_path)

    histo = plot.hist(image.ravel(), bins = 256, color = 'orange', )
    histo = plot.hist(image[:, :, 0].ravel(), bins = 256, color = 'red', alpha = 0.5)
    histo = plot.hist(image[:, :, 1].ravel(), bins = 256, color = 'green', alpha = 0.5)
    histo = plot.hist(image[:, :, 2].ravel(), bins = 256, color = 'blue', alpha = 0.5)
    histo = plot.xlabel('Intensity')
    histo = plot.ylabel('Pixels #')
    histo = plot.legend(['Total', 'Red Channel', 'Green Channel', 'Blue Channel'])
    plot.savefig(photo_histogram_file, bbox_inches='tight', dpi=75, transparent=True)



def export_photo_histogram_simple(full_path):
    filename = os.path.splitext(os.path.basename(full_path))[0]
    if 'histogram' not in filename:
        file_path = os.path.dirname(full_path)
        photo_histogram_file = f"{file_path}/{filename}_histogram.png"
        
        img = cv2.imread(full_path)
        color = ('b','g','r')
        plot.figure()

        for i,col in enumerate(color):
            histr = cv2.calcHist([img],[i],None,[256],[0,256])
            plot.plot(histr,color = col)
            plot.fill_between(histr, facecolor=col)
            plot.xlim([0,256])
        
        plot.savefig(photo_histogram_file, bbox_inches='tight', dpi=75, transparent=True)
        plot.close(photo_histogram_file)
