import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time import strftime

last_idle = 0
last_total = 0
utilization_data = []
load_data = []
time_data = []
max_points = 60 
tick_interval = 10


plt.figure(figsize=(10, 10))
plt.suptitle('Real Time System Monitoring')


ax1 = plt.subplot(2, 1, 1)
ax1.set_title('Real-Time CPU Utilization')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('CPU Utilization (%)')
line1, = ax1.plot([], [], lw=2)
ax1.set_xlim(0, 60)  
ax1.set_ylim(0, 100) 
ax1.grid()

ax2 = plt.subplot(2, 1, 2)
ax2.set_title('Real-Time Load')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Load Average')
line2, = ax2.plot([], [], lw=2)
ax2.set_xlim(0, 60)  
ax2.set_ylim(0, 12) 
ax2.grid()

def update(frame):
    global last_idle, last_total, time_counter
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle, total - last_total
        last_idle, last_total = idle, total
        
        utilization = 100.0 * (1.0 - idle_delta / total_delta)
        
        utilization_data.append(utilization)

        current_time = strftime('%H:%M:%S')
        time_data.append(current_time)

        if len(utilization_data) > max_points:
            utilization_data.pop(0)
            time_data.pop(0)

        line1.set_data(range(len(time_data)), utilization_data)
        ax1.set_xticks(range(len(time_data)), time_data, rotation=30, ha='right')

        if len(time_data) > 1:
            ax1.set_xticks(range(0, len(time_data), tick_interval), time_data[::tick_interval], rotation=30, ha='right')

    with open('/proc/loadavg', 'r') as f2:
        loadavg = f2.readline().strip().split()
    
        minute_average=float(loadavg[0])
        load_data.append(minute_average)
        if len(load_data) > max_points:
            load_data.pop(0)

        line2.set_data(range(len(time_data)), load_data)
        ax2.set_xticks(range(len(time_data)), time_data, rotation=30, ha='right')

        if len(time_data) > 1:
            ax2.set_xticks(range(0, len(time_data), tick_interval), time_data[::tick_interval], rotation=30, ha='right')
    return line1, line2

ani = FuncAnimation(plt.gcf(), update, interval=1000)  
plt.tight_layout(rect=[0, 0.1, 1, 0.98])  
plt.subplots_adjust(hspace=0.5) 
plt.show()
