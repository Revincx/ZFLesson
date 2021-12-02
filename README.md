## 正方教务系统抢课

**本程序仅供开发测试，不保证可用性，也不保证一定能抢到课！**

项目代码由 [lessons-robber](https://github.com/EddieIvan01/lessons-robber) 修改而成，部分代码版权归原作者  [EddieIvan01](https://github.com/EddieIvan01) 所有，如有侵权请联系我删除。

### 功能特性

* 多站点多线程抢课
* 一次可以抢多门课程
* 如果没到抢课时间可以循环等待重试
* 课程已满时挂机捡漏

### 食用指南

在使用本代码之前请确保自己知道怎么运行Python代码并且了解yaml的基本格式。

1. 安装依赖，在命令行中执行：

   ```bash
   pip3 install -r requirements.txt
   ```

2. 将项目目录下的 `config.example.yml` 重命名为 `config.yml` 

3. 编辑 `config.yml` ，填写相应的字段。

4. 运行 `app.py`

   ```bash
   python3 app.py
   ```

### 声明

本项目源码仅供测试，请勿用于盈利等其他用途。

不提供可直接运行的二进制文件，请谨慎使用他人提供的不明程序，以免个人信息泄漏。
