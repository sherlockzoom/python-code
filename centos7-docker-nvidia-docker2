> `yum install --downloadonly --downloaddir=<your_dir> <package-name>`  下载安装包


## 1. nvidia dirvier 384.66

http://www.nvidia.com/download/driverResults.aspx/122821/en-us

+ `rpm -i nvidia-diag-driver-local-repo-rhel7-384.66-1.0-1.x86_64.rpm` 
+  `yum clean all`
+ `yum install cuda-drivers` 
+  `reboot`

##2. cuda8.0

https://developer.nvidia.com/cuda-80-ga2-download-archive

`sudo rpm -i cuda-repo-rhel7-8-0-local-ga2-8.0.61-1.x86_64.rpm`
`sudo yum clean all`
`sudo yum install cuda`

## 3. docker

https://docs.docker.com/install/linux/docker-ce/binaries/#install-static-binaries

tar xzvf /path/to/<FILE>.tar.gz
sudo cp docker/* /usr/bin/
sudo dockerd &


## 4. nvidia-docker2

https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0)

sudo yum install nvidia-docker2
sudo pkill -SIGHUP dockerd

## FQA
###  1. Docker 安装后出现：WARNING: bridge-nf-call-iptables is disabled 的解决办法
```
vim /etc/sysctl.conf
net.bridge.bridge-nf-call-ip6tables = 1 
net.bridge.bridge-nf-call-iptables = 1 net.bridge.bridge-nf-call-arptables = 1
```
