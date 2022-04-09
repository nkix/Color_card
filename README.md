# Color_card

## Content
* [Install](#install)
* [Usage](#usage)

 <hr>

## Install
Download and unzip the file to your local directory
Numpy and OpenCV need to be installed before running these scripts

 <hr>

## Usage
### Windows
1. With cmd, enter the directory of these scripts
   ```sh
   cd ..\Color_classification
   ```
2. The usage of scipt can be checked with running
   ```sh
   python color_app.py -h
   ```
#### For single image
This command can be used to process single image input
```sh
python color_app.py -f <image directory> -k <k value> -m <max number of colors in card> -s -o
```
-f : required, the directory of image input  
-k : required, the k value applied to KMeans, will also decide the number of colors output  
-m ：the max number of color shown in color card applied if k is larger than m, default would be 15  
-s : use this to show specific RGB value of colors in the color card  
-o : call a image segmentation function before color analysis  
with -o choosen, user will be required to draw the range of object interested. Use need to press Enter to confirm the selection, and then press 0 to confirm the segmentation  

example:
```sh
python color_app.py -f images/banana.jpg -k 10 -o
```  

#### For package of images
This command can be used to process single image input
```sh
python color_app.py -p <package directory> -k <k value> -m <max number of colors in card> -s
```
This command will automatically process all images within this directory, analysis and classify them

example:
```sh
python color_app.py -p images -k 15
```


 
