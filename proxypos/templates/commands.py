import os
import sys
import subprocess

def convert(width,img,output):
    temporal_path = os.path.dirname(img)
    cmd = "convert -crop %sx255 %s %s"%(width,img,output)
    s = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE)

    s1,s2 = s.communicate()
    
    try:
        return [f for f in os.listdir(temporal_path)
               if f.startswith("pticket") and f.endswith(".png")]
    except OSError:
        return []

def wkhtmltoimage(html,css,width):
    temporal_path = os.path.dirname(html)
    img = os.path.join(temporal_path,"ticket.png")
    output = os.path.join(temporal_path,"pticket.png")
    cmd = "wkhtmltoimage --user-style-sheet %s --crop-w %s %s %s"%(css,width,html,img)
    s = subprocess.Popen(cmd,shell=True, stderr=subprocess.PIPE)
    s1,s2 = s.communicate()
    
    return convert(width,img,output)
