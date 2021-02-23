import os
import numpy as np
from PIL import Image 




def generate_checkerboard(img_width, img_height, grid_size):
    ck = np.kron([[255, 0] * int(grid_size/2), [0, 255] * int(grid_size/2)]*int(grid_size/ 2) , np.ones((int(img_height / grid_size), int(img_width/ grid_size))))
    
    #ck = np.expand_dims(ck, axis=2)

    ck = ck.astype(np.uint8) # this is needed ot use ToTensor() transformaion in pytorch

    return ck


def get_tiled_ground_truth(mask, grid_size):
    height = mask.shape[0]
    width = mask.shape[1]
    tile_height = height / grid_size
    tile_width = width / grid_size

    if len(mask.shape) ==3:
        mask = mask[:, : , 0] # get only 0th channel

    else:
        mask = mask
    
    tile_mask = np.zeros_like(mask, dtype=np.uint8)

   # if grid_size == mask.shape[0]:
    #    return mask
    
    for c in range(grid_size):
        
        for r in range(grid_size):
        
            #mask = (mask > 128) # convert mask to binary
            #print(mask)

            row_start = int(r*tile_height)
            row_end = int(r*tile_height + tile_height)
            column_start =  int(c * tile_width) 
            column_end = int(c * tile_width + tile_width)
            
            #print("row start=", row_start)
            #print("row end=", row_end)
            #print("column start=", column_start)
            #print("colum end=", column_end)

            tile_sum = np.sum(mask[row_start:row_end, column_start:column_end])

            #print(tile_sum)  
            
            if tile_sum > 0:
                tile_mask[row_start:row_end, column_start:column_end] = 255
            
        #tile = 
    tile_mask = tile_mask.astype(np.uint8)

    # tile_mask = np.stack((tile_mask,)*3, axis=-1)
    #plt.imshow(tile_mask)
    return tile_mask


def one_hot_encode(label, label_values):
    """
    Convert a mask into  one-hot format
    by replacing each pixel value with a vector of length num_classes
    
    Parameters
    ----------
    label: array 
        The 2D array segmentation image label

    label_values: [r, g, b] array for each class
        
    # Returns
        A 2D array with the same width and hieght as the input, but
        with a depth size of num_classes
    """
    semantic_map = []
    for colour in label_values:
        equality = np.equal(label, colour)
        class_map = np.all(equality, axis = -1)
        semantic_map.append(class_map)
    semantic_map = np.stack(semantic_map, axis=-1)

    return semantic_map.astype('float')


class DatasetWithGridEncoding(object):
    """
    A class of Dataset whch is supported for Pytorch.

    ...

    Attributes
    ----------
    imgs_root: str
        A root directory contains image files

    masks_root: str
        A root directory contains mask files. Please use the image names as prefix for mask's names to find correct mask for correct image.

    img_size: int
        A size of image. Image width and height are resized into this given size.

    grid_sizes: int array
        A array of int sizes which is used as grid sizes (default is  [2,4,8,16,32,64,128,256])

    transforms: Pytorch transforms
        Other type of transforms which come with Pytorch library. 
    
    label_values: [r,g,b] value array for segmentation classes

    Methods
    -------
    __getitem__(idx):
        Get an single data item from the dataset with image, gird_encoding image and correspondig mask.
    """

    def __init__(self, imgs_root, masks_root, img_size = 256, grid_sizes=[2,4,8,16,32,64,128,256] , transforms = None, label_values=None):
        """
        Parameters
        ----------
        imgs_root: str
            A root directory contains image files

        masks_root: str
            A root directory contains mask files. Please use the image names as prefix for mask's names to find correct mask for correct image.

        img_size: int
            A size of image. Image width and height are resized into this given size.

        grid_sizes: int array
            A array of int sizes which is used as grid sizes (default is  [2,4,8,16,32,64,128,256])

        transforms: Pytorch transforms
            Other type of transforms which come with Pytorch library.

        label_values: [r,g,b] value array for segmentation classes
        """

        self.imgs_root = imgs_root
        self.masks_root = masks_root

        self.img_size = img_size

        self.transforms = transforms
        self.label_values = label_values

        self.length_of_grid_sizes = len(grid_sizes)

        self.imgs = list(sorted(os.listdir(self.imgs_root)))
        self.masks = list(sorted(os.listdir(self.masks_root)))

        self.num_imgs = len(self.imgs)

        self.imgs = self.imgs * self.length_of_grid_sizes
        self.masks = self.masks * self.length_of_grid_sizes

        self.grid_sizes_repeated = np.repeat(grid_sizes, self.num_imgs)

        self.all_in_one = list(zip(self.imgs, self.masks, self.grid_sizes_repeated)) #(img, mask, grid_size)

       # self.imgs_repeated
        #self.masks_repea

    def __len__(self):
        return len(self.all_in_one)


    def __getitem__(self, idx):
        """ Get an single data item from the dataset with image, gird_encoding image and correspondig mask. 
        
        Main function which return data for Pytorch dataloader.

        Parameters
        ---------
        idx: index of the datarecord to be returned. 

        Returns
        -------
        dictionary
            A dictionary with three keys and corresponding values, {"img":img, "grid_encode": grid_encode, "mask":mask}
        """

        img_path = os.path.join(self.imgs_root, self.all_in_one[idx][0]) # 0th one= image
        mask_path = os.path.join(self.masks_root, self.all_in_one[idx][1]) # 1st one = mask
        grid_size = self.all_in_one[idx][2] # 2nd one = grid size

        img_size = self.img_size

        img = Image.open(img_path)
        mask = Image.open(mask_path)

        grid_encode = generate_checkerboard(img_size, img_size, grid_size)#[:, :, 0]
    

        # resizing
        img = img.resize((img_size, img_size), Image.NEAREST)
        mask = mask.resize((img_size, img_size), Image.NEAREST)

        # covert to numpy

        img = np.array(img)
        mask = np.array(mask) #



        # clean mask values (this is done to remove small values in mask images)
        mask = (mask > 128) * 255 # if mask value > 128, set it to 255 (this will remove 254, 253 values and 1,2 etc)
         
        mask = get_tiled_ground_truth(mask, grid_size)
        #mask = mask[:, :, 0]

        #one hot encoding
        if self.label_values is not None:
            mask = one_hot_encode(mask, self.label_values)

       

        if self.transforms is not None:
            # img, target= self.transforms(img, target)

            img = self.transforms(img)
            mask = self.transforms(mask)
            grid_encode = self.transforms(grid_encode)

      

          
        return {"img":img, "grid_encode": grid_encode, "mask":mask}



class DatasetWithGridEncodingFromFilePaths(object):
    """
    A class of Dataset whch is supported for Pytorch.

    ...

    Attributes
    ----------
    img_paths_file: str
        A file with all paths of images. File should have one path (absolute path) per line. 

    mask_paths_file: str
        A file with all paths of masks. File should have one path (absolute path) per line. Please use the image names as prefix for mask's names to find correct mask for correct image.

    img_size: int
        A size of image. Image width and height are resized into this given size.

    grid_sizes: int array
        A array of int sizes which is used as grid sizes (default is  [2,4,8,16,32,64,128,256])

    transforms: Pytorch transforms
        Other type of transforms which come with Pytorch library. 

    label_values: [r,g,b] value array for segmentation classes

    Methods
    -------
    __getitem__(idx):
        Get an single data item from the dataset with image, gird_encoding image and correspondig mask.
    """

    def __init__(self, img_paths_file, mask_paths_file, img_size = 256, grid_sizes=[2,4,8,16,32,64,128,256] , transforms = None, label_values=None):
        """
        Parameters
        ----------
        img_paths_file: str
        A file with all paths of images. File should have one path (absolute path) per line. 

        mask_paths_file: str
        A file with all paths of masks. File should have one path (absolute path) per line. Please use the image names as prefix for mask's names to find correct mask for correct image.

        img_size: int
            A size of image. Image width and height are resized into this given size.

        grid_sizes: int array
            A array of int sizes which is used as grid sizes (default is  [2,4,8,16,32,64,128,256])

        transforms: Pytorch transforms
            Other type of transforms which come with Pytorch library.

        label_values: [r,g,b] value array for segmentation classes
        """

        self.img_paths_file = img_paths_file
        self.mask_paths_file = mask_paths_file

        self.img_size = img_size

        self.transforms = transforms
        self.label_values = label_values

        self.length_of_grid_sizes = len(grid_sizes)


        # Reading files lines to lists
        with open(self.img_paths_file) as f:
            self.img_paths = f.readlines()

        self.img_paths = [x.strip() for x in self.img_paths] # remove /n line chatacter 

        with open(self.mask_paths_file) as f:
            self.mask_paths = f.readlines()

        self.mask_paths = [x.strip() for x in self.mask_paths] # remove /n line chatacter 

        self.imgs = list(sorted(self.img_paths))
        self.masks = list(sorted(self.mask_paths))

        self.num_imgs = len(self.imgs)

        self.imgs = self.imgs * self.length_of_grid_sizes
        self.masks = self.masks * self.length_of_grid_sizes

        self.grid_sizes_repeated = np.repeat(grid_sizes, self.num_imgs)

        self.all_in_one = list(zip(self.imgs, self.masks, self.grid_sizes_repeated)) #(img, mask, grid_size)

       # self.imgs_repeated
        #self.masks_repea

    def __len__(self):
        return len(self.all_in_one)


    def __getitem__(self, idx):
        """ Get an single data item from the dataset with image, gird_encoding image and correspondig mask. 
        
        Main function which return data for Pytorch dataloader.

        Parameters
        ---------
        idx: index of the datarecord to be returned. 

        Returns
        -------
        dictionary
            A dictionary with three keys and corresponding values, {"img":img, "grid_encode": grid_encode, "mask":mask}
        """

        img_path = self.all_in_one[idx][0] # 0th one= image
        mask_path = self.all_in_one[idx][1] # 1st one = mask
        grid_size = self.all_in_one[idx][2] # 2nd one = grid size

        img_size = self.img_size

        img = Image.open(img_path)
        mask = Image.open(mask_path)

        grid_encode = generate_checkerboard(img_size, img_size, grid_size)#[:, :, 0]
    

        # resizing
        img = img.resize((img_size, img_size), Image.NEAREST)
        mask = mask.resize((img_size, img_size), Image.NEAREST)

        # covert to numpy

        img = np.array(img)
        mask = np.array(mask) #



        # clean mask values (this is done to remove small values in mask images)
        mask = (mask > 128) * 255 # if mask value > 128, set it to 255 (this will remove 254, 253 values and 1,2 etc)
         
        mask = get_tiled_ground_truth(mask, grid_size)
        #mask = mask[:, :, 0]

        #one hot encoding
        if self.label_values is not None:
            mask = one_hot_encode(mask, self.label_values)

       

        if self.transforms is not None:
            # img, target= self.transforms(img, target)

            img = self.transforms(img)
            mask = self.transforms(mask)
            grid_encode = self.transforms(grid_encode)

          
        return {"img":img, "grid_encode": grid_encode, "mask":mask}




class DatasetWithGridEncodingFromDataFrame(object):
    """
    A class of Dataset whch is supported for Pytorch.

    ...

    Attributes
    ----------
    df : pd.DataFrame
        A dataframe with two colomns: image_path and mask_path. Each column has absolute path of image and maks.

    img_size: int
        A size of image. Image width and height are resized into this given size.

    grid_sizes: int array
        A array of int sizes which is used as grid sizes (default is  [2,4,8,16,32,64,128,256])

    transforms: Pytorch transforms
        Other type of transforms which come with Pytorch library. 

    label_values: [r,g,b] value array for segmentation classes

    Methods
    -------
    __getitem__(idx):
        Get an single data item from the dataset with image, gird_encoding image and correspondig mask.
    """

    def __init__(self, df, img_size = 256, grid_sizes=[2,4,8,16,32,64,128,256] , transforms = None, label_values=None):
        """
        Parameters
        ----------
        df : pd.DataFrame
            A dataframe with two colomns: image_path and mask_path. Each column has absolute path of image and maks.

        img_size: int
            A size of image. Image width and height are resized into this given size.

        grid_sizes: int array
            A array of int sizes which is used as grid sizes (default is  [2,4,8,16,32,64,128,256])

        transforms: Pytorch transforms
            Other type of transforms which come with Pytorch library.

        label_values: [r,g,b] value array for segmentation classes
        """

        self.df = df
        self.img_size = img_size

        self.transforms = transforms
        self.label_values = label_values

        self.length_of_grid_sizes = len(grid_sizes)

        self.imgs = list(self.df["image_path"])
        self.masks = list(self.df["mask_path"])

        self.num_imgs = len(self.df)


        self.imgs = self.imgs * self.length_of_grid_sizes
        self.masks = self.masks * self.length_of_grid_sizes

        self.grid_sizes_repeated = np.repeat(grid_sizes, self.num_imgs)

        self.all_in_one = list(zip(self.imgs, self.masks, self.grid_sizes_repeated)) #(img, mask, grid_size)

       # self.imgs_repeated
        #self.masks_repea

    def __len__(self):
        return len(self.all_in_one)


    def __getitem__(self, idx):
        """ Get an single data item from the dataset with image, gird_encoding image and correspondig mask. 
        
        Main function which return data for Pytorch dataloader.

        Parameters
        ---------
        idx: index of the datarecord to be returned. 

        Returns
        -------
        dictionary
            A dictionary with three keys and corresponding values, {"img":img, "grid_encode": grid_encode, "mask":mask}
        """

        img_path = self.all_in_one[idx][0] # 0th one= image
        mask_path = self.all_in_one[idx][1] # 1st one = mask
        grid_size = self.all_in_one[idx][2] # 2nd one = grid size

        img_size = self.img_size

        img = Image.open(img_path)
        mask = Image.open(mask_path)

        grid_encode = generate_checkerboard(img_size, img_size, grid_size)#[:, :, 0]
    

        # resizing
        img = img.resize((img_size, img_size), Image.NEAREST)
        mask = mask.resize((img_size, img_size), Image.NEAREST)

        # covert to numpy

        img = np.array(img)
        mask = np.array(mask) #



        # clean mask values (this is done to remove small values in mask images)
        mask = (mask > 128) * 255 # if mask value > 128, set it to 255 (this will remove 254, 253 values and 1,2 etc)
         
        mask = get_tiled_ground_truth(mask, grid_size)
        #mask = mask[:, :, 0]

        #one hot encoding
        if self.label_values is not None:
            mask = one_hot_encode(mask, self.label_values)

       

        if self.transforms is not None:
            # img, target= self.transforms(img, target)

            img = self.transforms(img)
            mask = self.transforms(mask)
            grid_encode = self.transforms(grid_encode)

          
        return {"img":img, "grid_encode": grid_encode, "mask":mask}