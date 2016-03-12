Title: Как поменять разрешение в консоле Linux (ubuntu 14.10)
Date: 2015-01-31 16:54
Tags: ubuntu
Category: IT
Author: Swasher


В файле `/etc/default/grub` пишем:

    ::console
    GRUB_GFXMODE=1600x1200 #для 27"
    GRUB_GFXMODE=1280x768 #для 24"
    GRUB_GFXPAYLOAD_LINUX=keep

Обновляем 

    ::console   
    $ sudo update-grub2
    $ sudo reboot

Ссылки:

- [gfxmode][]
- [gfxpayload][]


  [gfxmode]: https://www.gnu.org/software/grub/manual/html_node/gfxmode.html
  [gfxpayload]: https://www.gnu.org/software/grub/manual/html_node/gfxpayload.html