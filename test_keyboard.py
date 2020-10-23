import sys

sys.stdout.write('根据两点坐标计算直线斜率k，截距b：\n')
for line in sys.stdin:
    if line == '\n': break
    
    x1, y1, x2, y2 = (float(x) for x in line.split())
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    sys.stdout.write('斜率:{}，截距:{}\n'.format(k, b))