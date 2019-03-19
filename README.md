**Components**
* [Raspberry PI 3B+](https://www.amazon.com/gp/product/B07BC7BMHY/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) 
* [Seedstudio-GrovePi](https://www.amazon.com/gp/product/B01BRCEWV2/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1) 
* [32GB Memory Card](https://www.amazon.com/gp/product/B06XWN9Q99/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) 
* [3.5'' Screen](https://www.amazon.com/gp/product/B01IGBDT02/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1) (Optional) 

**Installation**
* [Install GrovePi](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/)  
```
sudo curl -kL dexterindustries.com/update_grovepi | bash
sudo reboot 
``` 
* Check i2c & [Update Firmware](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/updating-firmware/)
```
# Check if i2c is accessible / seen 
sudo i2cdetect -y 1

# If not update firmware 
sudo git clone https://github.com/DexterInd/GrovePi
cd GrovePi/Firmware 
sudo chmod +x firmware_update.sh
sudo ./firmware_update.sh
```
* [Install 3.5'' Monitor](https://github.com/goodtft/LCD-show) 
```
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show
```
