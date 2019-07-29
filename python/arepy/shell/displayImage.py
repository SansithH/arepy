# Display an image using the 'display'
import subprocess

def displayImage( fileName='figOverview_*.png' ):    
    from sys import platform
    if platform == "linux" or platform == "linux2":
        subprocess.call(["display", fileName ])
    elif platform == "darwin":
        print(fileName)
        subprocess.call(["open", fileName ])
    elif platform == "win32":
        subprocess.call(["display", fileName ])
    