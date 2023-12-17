from gpiozero import Servo
from time import sleep

# Number to send. Our setup currently only sends 4 bit numbers (0-15). CAN MODDIFY
char_to_send = 10


# Variables controlling the frequency of the bits
#Aproximate time for one bit to be sent (seconds)
runtime = 4.8
#1/2 of the period for 0 and 1, with the timmed matched to the bit by index (seconds)
# this controlls what frequencies each bit is represented by. 
modtime = [.7, 1.2]


# convert the bit into a 4 bit binary list
msg_bits = [int(x) for x in "{0:b}".format(char_to_send)]
pads = 4 - len(msg_bits)
msg_bits = [0] * pads + msg_bits
print(msg_bits)


# Delay to re-orient motor.
servo=Servo(2)
sleep(3)

try:
    #For each bit, modulate at the indexed frequency for a set amount of time
    for b in msg_bits:
        cur_timer = modtime[b]
        runiter = int(runtime/cur_timer)
        print(runiter)
        
        #Each "blocked" and "unblocked" will persist for a <modtime> ammount of time,
        # and it will modulate like this for about <runtime> time
        for i in range(0, runiter):
            print("Bit:", b, "   Iteration:", i)
            servo.min()
            sleep(cur_timer)
            servo.max()
            sleep(cur_timer)
            
        #Separate each transmission with a delay to easier programming. 
        sleep(runtime/2)


except KeyboardInterrupt:
    print("stop")




