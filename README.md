## mmWaveComm
### Final Project for CS437 EKS Fall 2023

#### How to run:
* parse_bin_data.py: After obtaining your radar capture with Industrial_Visualizer (not included). Set the path in parse_bin_data.py to the corresponding directory and run.
* decoder.py: After you've parsed the binaries. Set `exp_time` to the bin file capture name (by default it is the capture time, we renamed some for documentation). Then run.   
Errors: decoder can fail when no range is proposed or no enough bits are detected. When it happens, refer to the inline comments for parameter `threshold` and call to the function `find_peaks`. They should be adjusted for ideal output. These parameters generally correspond to a range of distances and chirp slops, so they does not hurt the robustness of the system. 


#### Data
The data are named in `0_?{number}_{distance}?_(noise)?` format. Number tells what number is being send. Distance is the distance between the sender and receiver. Noise tells if we add noise to the environment with additional moving corner reflector.