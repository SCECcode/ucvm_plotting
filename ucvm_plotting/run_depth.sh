echo "==== test plot_depth_profile -H ==="
plot_depth_profile.py -H

echo "==== test plot_depth_profile -s -b -e -d -v -c -o ==="
plot_depth_profile.py -s 34,-118 -b 0 -e 50000 -d vs,vp,density -v 500 -c cvmh -o depth.png 

echo "==== view_png -f ==="
view_png.py -f depth.png

echo "=== cleanup ==="
rm depth.png depth_matprops.json depth_meta.json
