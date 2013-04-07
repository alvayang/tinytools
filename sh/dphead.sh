xrandr --output DP1 --right-of LVDS1 --auto
if [ $1 ]
then
xrandr --output DP1 --off
fi
