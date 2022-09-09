from PIL import Image
import os


def cut_img_sheet(image_name="img.png", col=1, row=1, naming=None):
    """
    Cuts an image into smaller parts.\n
    Can use a 2D `naming` array to set the name of the images, sort some images into seperate folders or to not save some images.
    """
    # image.show()
    if naming == None or (len(naming) >= col and len(naming[0]) >= row):
        try:
            image = Image.open(image_name)
        except FileNotFoundError:
            print("Image not found!")
        else:
            # variables
            if naming == None:
                cur_num = 0
            image_ext = image_name.split(".")[-1]
            folder_name = image_name.removesuffix("." + image_ext)
            size = image.size
            x_size = size[0]/col
            y_size = size[1]/row
            # make folder
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            # split img
            # left, top, right, bottom
            for x in range(col):
                for y in range(row):
                    cropped = image.crop((x*x_size, y*y_size, (x+1)*x_size, (y+1)*y_size))
                    if naming == None:
                        crop_name = cur_num
                        cur_num += 1
                    else:
                        crop_name = str(naming[x][y])
                        if crop_name.find("*DELETE*") == -1:
                            if crop_name.find("/") != -1:
                                dir_for_name = str(crop_name + "||").removesuffix("/" + (crop_name + "||").split("/")[-1])
                                if not os.path.isdir(f"{folder_name}/{dir_for_name}"):
                                    os.mkdir(f"{folder_name}/{dir_for_name}")
                    if naming == None or crop_name.find("*DELETE*") == -1:
                        cropped.save(f"{folder_name}/{crop_name}.{image_ext}")
    else:
        print(f"Naming array is not big enough: [{len(naming)}, {len(naming[0])}] < [{col}, {row}]")

def make_naming_array(names_col:list, names_row:list, separator=""):
    """
    Combines 2 arrays into a 2D array for the `cut_img_sheet` function.\n
    If an image name has a "/" in it, it will be treated as a path, and will make a seprate folder for that image accordingly.\n
    If an image name would include "*DELETE*", then it won't be saved instead.
    """
    naming = []
    for name_c in names_col:
        naming_c = []
        for name_r in names_row:
            naming_c.append(f"{name_r}{separator}{name_c}")
        naming.append(naming_c)
    return naming


if __name__ == "__main__":
    image_name = "cards.png"
    grid_size = [13, 8]
    names_col = ["A", "N_2", "N_3", "N_4", "N_5", "N_6", "N_7", "N_8", "N_9", "N_10", "J", "Q", "K"]
    names_row = ["CLUB/", "*DELETE*", "SPADE/", "*DELETE*", "HEART/", "*DELETE*", "DIAMOND/", "*DELETE*"]
    # names_row = ["CLUB/", "_trash/C1_", "_trash/C2_", "SPADE/", "_trash/S1_", "_trash/S2_", "HEART/", "_trash/H1_", "_trash/H2_", "DIAMOND/", "_trash/D1_", "_trash/D2_"]
    cut_img_sheet(image_name, grid_size[0], grid_size[1], make_naming_array(names_col, names_row))
    # cut_img_sheet("n.png", 4, 4)