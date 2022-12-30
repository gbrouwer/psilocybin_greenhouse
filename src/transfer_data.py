import os
import sys

os.system('scp -r pi@greenhouse:/home/pi/Code/psilocybin_greenhouse/data/measurements ../data')
os.system('scp -r pi@greenhouse:/home/pi/Code/psilocybin_greenhouse/data/camera1 ../data')
os.system('scp -r pi@greenhouse:/home/pi/Code/psilocybin_greenhouse/data/camera2 ../data')
os.system('scp -r pi@greenhouse:/home/pi/Code/psilocybin_greenhouse/data/lux ../data')
