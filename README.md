## mmWaveComm
### Final Project for CS437 EKS Fall 2023

#### Additional Infrastructure:
 * You must construct a retroreflector and blocking device, using a motor that can run on Raspberry Pi and some sort of matalic "blocker" to be actuated in front of the retroreflector.
 * The motor should be properly attached to the Raspberry Pi's GPIO, live and ground pins.
 * * Our specific setup used a small, square peice of cardboard plated with aluminum tape as the metalic blocker, a "Tiny Pro 9g Micro Servo" as the motor, a small cardboard box a bit taller than the cardboard blocker as a stand, and a provided 3-d printed, copper plated retroreflector.
 * * The motor was taped to the flat end of the square blocker, then taped the flat-side of the motor down to the box such that the blocker is jutting off completly from the box and can rotate away from it.
 * * Then, we put the retroreflector behind the the area blocked by the blocker, standing it up with some object so that the reflective parts points towards the blocker. We also angled the blocker about 45 degrees by rotating the box such that the blocker was still in front of the reflector.
 * * Lastly, this settup should face the radar. 

#### How to run:
* parse_bin_data.py: After obtaining your radar capture with Industrial_Visualizer (not included). Set the path in parse_bin_data.py to the corresponding directory and run.
* RadioComMotor.py: Download this file Raspberry Pi. After properly attaching the blocking device to the Raspberry Pi, set variable `char_to_send` to the desired 4 bit number and run. If desired, you can moddify `modtime` to change the frequencies that correspond with the binary bits, but this is not recommended. 
* decoder.py: After you've parsed the binaries. Set `exp_time` to the bin file capture name (by default it is the capture time, we renamed some for documentation). Then run.   
Errors: decoder can fail when no range is proposed or no enough bits are detected. When it happens, refer to the inline comments for parameter `threshold` and call to the function `find_peaks`. They should be adjusted for ideal output. These parameters generally correspond to a range of distances and chirp slops, so they does not hurt the robustness of the system. 


#### Data
The data are named in `0_?{number}_{distance}?_(noise)?` format. Number tells what number is being send. Distance is the distance between the sender and receiver. Noise tells if we add noise to the environment with additional moving corner reflector. If no distance is present, the distance is 2 meters.
