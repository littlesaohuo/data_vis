import numpy as np
import pcl
import pcl.pcl_visualization
# lidar_path 指定一个kitti 数据的点云bin文件就行了
lidar_path = "/home/zx/data/huawei+sample/non-structure-new/000003.bin"
pointcloud = np.fromfile(str(lidar_path),dtype=np.float32).reshape([-1, 6])

# 这里第四列代表颜色值,根据自己需要进行赋值
pointcloud[:, 3] = 3329330

# # PointCloud_PointXYZRGB 需要点云数据是N*4，分别表示x,y,z,RGB ,其中RGB 用一个整数表示颜色；
color_cloud = pcl.PointCloud(pointcloud[:,:3])
visual = pcl.pcl_visualization.CloudViewing()
visual.ShowMonochromeCloud(color_cloud)
flag = True
while flag:
    flag != visual.WasStopped()