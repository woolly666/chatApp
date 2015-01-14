import subprocess
import tempfile
import os
       
(fd, filename) = tempfile.mkstemp()
tfile = os.fdopen(fd, "w")
tfile.write("Hello, world!\n")
tfile.close()
subprocess.Popen(["/bin/cat", filename]).wait()  
with open("hi" + "hello" + ".txt",'a') as log:
     with open(filename, "rb") as f:
        print(f.read(), file=log)
  

       

