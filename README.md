# goss
Github Object Storage System 使用 Github 构建类似 oss 的对象储存工具，本工具可以很方便的管理 github 数据，可以很方便的搭建图床

***暂不支持 windows 系统***

**创建仓库**

![goss1](https://raw.githubusercontent.com/wxnacy/image/master/blog/goss1.gif)

**上传本地图片**

![goss2](https://raw.githubusercontent.com/wxnacy/image/master/blog/goss3.gif)

## 安装

使用 pip 安装非常方便

```bash
$ pip install goss
```

**更新**

```bash
$ pip install --upgrade goss
```

## 快速开始

goss 的命令格式基本遵守了 RESTful 风格

### 仓库

```bash
$ goss-cli repo                                 # 查看仓库列表
$ goss-cli repo <repository-name>               # 查看指定仓库
$ goss-cli repo <repository-name> -m post       # 创建仓库
$ goss-cli repo <repository-name> -m delete     # 删除仓库
```

**上传文件**

```bash
$ goss <filepath> -r <repository-name>
```

**查看仓库文件列表**

```bash
$ goss-cli file -r <repository-name>
```

**查看文件详情**

```bash
$ goss-cli file <path> -r <repository-name>
```

**下载文件**

```bash
$ goss-cli file <path> -r <repository-name> -D
```

**删除文件**

```bash
$ goss-cli file <path> -r <repository-name> -m delete
```

更多使用请使用帮助命令 `goss-cli --help` 或者 `goss-cli repo --help`
