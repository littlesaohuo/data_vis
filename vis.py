import numpy as np
import mayavi.mlab
import argparse

# parser = argparse.ArgumentParser(description="arg parser")
# parser.add_argument('--path', type=str, default='./', required=True)
# parser.add_argument("--sf", type=int, default=0,\
# required=True)

# args = parser.parse_args()
# lidar_path更换为自己的.bin文件路径
start_idx=0
file_name="/home/zx/data/huawei+sample/test/"
pointcloud = np.fromfile(\
str(file_name+"%06d.bin"%start_idx),\
dtype=np.float32).reshape([-1, 6])

fig = mayavi.mlab.figure(bgcolor=(0, 0, 0), engine=None, size=(640, 500))

def draw_grid(x1, y1, x2, y2, fig, tube_radius=None, color=(0.5, 0.5, 0.5)):
    mayavi.mlab.plot3d([x1, x1], [y1, y2], [0, 0], color=color, tube_radius=tube_radius, line_width=1, figure=fig)
    mayavi.mlab.plot3d([x2, x2], [y1, y2], [0, 0], color=color, tube_radius=tube_radius, line_width=1, figure=fig)
    mayavi.mlab.plot3d([x1, x2], [y1, y1], [0, 0], color=color, tube_radius=tube_radius, line_width=1, figure=fig)
    mayavi.mlab.plot3d([x1, x2], [y2, y2], [0, 0], color=color, tube_radius=tube_radius, line_width=1, figure=fig)
    return fig

def draw_multi_grid_range(fig, grid_size=20, bv_range=(-60, -60, 60, 60)):
    for x in range(bv_range[0], bv_range[2], grid_size):
        for y in range(bv_range[1], bv_range[3], grid_size):
            fig = draw_grid(x, y, x + grid_size, y + grid_size, fig)

    return fig

def show_frame_idx(current_idx):
    title_text = "frame_idx: %06d"%current_idx
    mayavi.mlab.title(title_text, size=0.2, height=0.1)

def update_point_3d(path_name, start_frame_idx):
    path_new=path_name+"%06d"%start_frame_idx+".bin"
    pointcloud = np.fromfile(str(path_new),dtype=np.float32).reshape([-1, 6])
    x = pointcloud[:, 0]  # x position of point
    y = pointcloud[:, 1]  # y position of point
    z = pointcloud[:, 2]  # z position of point
    current_camera = mayavi.mlab.view()
    mayavi.mlab.clf(fig)
    mayavi.mlab.points3d(x, y, z,
                     z,  # Values used for Color
                     mode="point",
                     colormap='spectral',  # 'bone', 'copper', 'gnuplot'
                     color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                     figure=fig,
                     )
    mayavi.mlab.view(        
            azimuth=current_camera[0],
            elevation=current_camera[1],
            focalpoint=current_camera[3],
            distance=current_camera[2],
            figure=fig,)
    mayavi.mlab.show()

def piker_callback_left(picker): #当鼠标点击会返回一个vtk picker对象，我们将对该对象进行处理判断
    global start_idx
    start_idx+=1
    update_point_3d(file_name, start_idx)
    show_frame_idx(start_idx)

def piker_callback_right(picker): #当鼠标点击会返回一个vtk picker对象，我们将对该对象进行处理判断
    global start_idx
    start_idx = start_idx-1 if start_idx >= 1 else 0 
    update_point_3d(file_name, start_idx)
    show_frame_idx(start_idx)




##################################################################################################
x = pointcloud[:, 0]  # x position of point
y = pointcloud[:, 1]  # y position of point
z = pointcloud[:, 2]  # z position of point
r = pointcloud[:, 3]  # reflectance value of point
d = np.sqrt(x ** 2 + y ** 2)  # Map Distance from sensor

degr = np.degrees(np.arctan(z / d))

vals = 'height'
if vals == "height":
    col = z
else:
    col = d

picker = fig.on_mouse_pick(piker_callback_left, button='Left')
picker = fig.on_mouse_pick(piker_callback_right, button='Right')

draw_multi_grid_range(fig, bv_range=(0, -40, 100, 40))
mayavi.mlab.points3d(x, y, z,
                     col,  # Values used for Color
                     mode="point",
                     colormap='spectral',  # 'bone', 'copper', 'gnuplot'
                     color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                     figure=fig,
                     )
mayavi.mlab.view(
        azimuth=180,
        elevation=70,
        focalpoint=[12.0909996, -1.04700089, -2.03249991],
        distance=62.0,
        figure=fig,
    )

show_frame_idx(start_idx)
mayavi.mlab.show()
