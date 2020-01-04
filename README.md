# PyCaptcha
Image and Audio captcha generation using python

## ImgCaptcha
Initialisation with captcha customisation arguments
```
    image = ImgCaptcha()
```
![Captcha Image Sample](Images/Captcha.png)

### Captcha Height and Width
    c_height=200, c_width=600, red=None,

#### Captcha Colors(default random colors)  
select color values from 0 to 255
     
    red
    green
    blue

#### Captcha Font Type(Picks a random Font by default)
provide a font path
    
    font_type
    
#### Font Color(default "WHITE")
    font_color

#### Font Size(default 50)
    font_size

### Save Captcha Image
    image.save(filename, file_format)

### Show Captcha 
To see the Captcha Image

    image.show_image()

## Audio Captcha Under Development
-------------------
