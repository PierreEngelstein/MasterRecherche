pkg load image
i = imread('holmes_nb.bmp');
imshow(i);

J = imnoise(i, 'salt & pepper', 0.5);
imshow(i);