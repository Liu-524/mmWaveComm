import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square, find_peaks
def get_sinc_response(data, freq,size=50):
    
    x = np.arange(0, size, 1)
    y = np.sinc(x).reshape((size, 1))
    res = np.dot(data, y).sum(axis=-1) / freq
    return res

def get_box_response(data, period):
    size = data.shape[-1]
    x = np.arange(0, size, 1)
    y = square(2 * np.pi * (1/period) * x).reshape((size,1))
    # plt.plot(x,y)
    # plt.show()
    res = np.dot(data, y).sum(axis=-1)
    return res



exp_time = "0one"

raw = np.load(f'data_{exp_time}.npy')
raw_adc = np.zeros((raw.shape[0], 3, 256))
for i, data in enumerate(raw):
    raw_adc[i] = data[3][:,:256]
## chirps/frames, antenna, samples

data = np.array([frame["adcSamples"][:, :256] for frame in raw])
res = np.fft.fft(data, axis=2) / 256
plt.xlabel('range bin')
plt.ylabel('time/frame')
plt.imshow(np.absolute(res[:,0,28:128]), cmap='jet')
plt.show()


amp = np.absolute(res[:,0,28:128])
phase = np.angle(res[:,0,28:128])


send_period = 4.8
frame_dur = 0.05 # sec
window_size = int(send_period / frame_dur)
stride = window_size // 2
signal_periods = [0.7, 1.2]
signal_periods = [x * 2 * (1//frame_dur) for x in signal_periods]
stride_offsets = 3

windows = np.lib.stride_tricks.sliding_window_view(amp, window_size, axis=0)


windows = windows - windows.mean(axis=2, keepdims=True)
# windows = windows / windows.std(axis=2, keepdims=True)
# axis => window#, range(freq), time.
check = 53



inspect_window = 165

# plt.plot(windows[5, check])
# plt.imshow(get_box_response(windows, 40))
# plt.show()

# channel proposing threshold (unit in response to ideal wave) 
# 6m -> 15
# 4m -> 100
# 2m -> 1000
threshold = 100
proposed_channels = set()
wl2res = {}
for i, wl in enumerate(signal_periods):
    # plt.plot(windows[2, check])
    digi_res = get_box_response(windows[::stride], wl)
    for k in range(1, stride_offsets):
        windows_2 = windows[stride * k // stride_offsets  :: stride]
        try:
            digi_res = np.maximum(digi_res, get_box_response(windows_2, wl))
        except:
            digi_res = np.maximum(digi_res[:-1], get_box_response(windows_2, wl))

    plt.imshow(np.maximum(digi_res, digi_res))
    plt.show()
    max_res = digi_res.max(axis=0)

    proposed_channels = proposed_channels.union(set(np.arange(0,digi_res.shape[1], 1) [max_res>threshold]))
    
    wl2res[wl] = digi_res

proposed_channels = sorted(proposed_channels)
print(proposed_channels)
peaks = []
for wl in wl2res:
    zo = signal_periods.index(wl)
    res = wl2res[wl]
    plt.plot(res[:, proposed_channels[len(proposed_channels) // 2]])
    signal = res[:, proposed_channels[len(proposed_channels) // 2]]

    #height is adjustable from high to low when no enough bits are detected
    # 2m height-> 500 prom -> 10
    # 6m height -> 10 prom -> 5
    
    peak_idx, info = find_peaks(signal, distance=3, prominence=5, height=10)
    if (len(peak_idx) != 0):
        peak_hi = max(info['peak_heights'])
        for i, p in enumerate(peak_idx):
            peaks.append((p, info['peak_heights'][i] / peak_hi, zo))
    plt.show()

def process_peaks(data):
    data.sort(key=lambda x: x[1], reverse=True)
    print(data)
    data = data[:4]
    data.sort(key=lambda x: x[0])
    message = np.array([zo for _,_,zo in data])
    print(message)
    if (len(message) != 4):
        print("error: not enough bits detected")
        exit()
    message = np.array([8,4,2,1]) @ message
    return message

print(process_peaks(peaks))


    
