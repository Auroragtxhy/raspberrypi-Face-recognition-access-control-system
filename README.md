# raspberrypi-Face-recognition-access-control-system（基于树莓派的人脸识别门禁系统）
----------------------------------
updata：2023年11月1日21:23:47
author：GT
* 这是目前最新的版本
* 相较于旧版增加了api_to_service.py文件，该文件用于在人脸识别后向服务器上传识别信息和所拍取的照片，不过服务器暂时只运行在本地，所以文件中定义的IP地址是127.0.0.1，目前该仓库中还没有包含服务器的项目代码
* 同时修改了主函数widget_main.py，在该文件中使用了上述增加的api_to_service.py文件所提供的API函数，完善了整个人脸识别的流程。
* 若是想要运行旧版的代码，只需将old_version文件夹下的widget_main.py替换上级目录中的widget_main.py即可，api_to_service.py则不用关心
* 这里不过多对项目进行介绍，若是想了解真个项目，请参看我的B站视频
* 【基于树莓派的人脸识别门禁系统—系统设计（代码讲解）】 https://www.bilibili.com/video/BV18K411U7LV/?share_source=copy_web&vd_source=b8ea6e0063d01669b2ad7d304dd1d386
* 【基于树莓派的人脸识别门禁系统—环境搭建】 https://www.bilibili.com/video/BV1Re4y117Nv/?share_source=copy_web&vd_source=b8ea6e0063d01669b2ad7d304dd1d386
* 【基于树莓派的人脸识别门禁系统——项目移植与实机演示】 https://www.bilibili.com/video/BV1nM411R7Jn/?share_source=copy_web&vd_source=b8ea6e0063d01669b2ad7d304dd1d386
* 还会有关于这个项目的最后一期视频
