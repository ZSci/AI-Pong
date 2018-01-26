import pickle
import random

with open('./io_data.p', 'rb') as file:
	data = []
	try:
		while True:
			data.extend(pickle.load(file))
	except EOFError:
		pass

dir_map = {'up': [1, 0, 0], 'dn': [0, 1, 0], 'nl' : [0, 0, 1]}

upd_data = [j for i in data[10:] for j in i]
upd_data = [data_sample.split(',') for data_sample in upd_data]

random.shuffle(upd_data)

counters = {'up':0, 'dn':0, 'nl':0}

for data_sample in upd_data:
	counters[data_sample[1]] += 1

min_count = counters[min(counters, key=counters.get)]

counters = {'up':0, 'dn':0, 'nl':0}
del_idx = 0

for i in range(len(upd_data)):
	counters[upd_data[i-del_idx][1]] += 1
	if counters[upd_data[i-del_idx][1]] <= min_count:
		pass
	else:
		del upd_data[i-del_idx]
		del_idx+=1

counters = {'up':0, 'dn':0, 'nl':0}

# del_idx = 0
# for i in range(len(upd_data)):
# 	if 'nl' in upd_data[i-del_idx]:
# 		del upd_data[i-del_idx]
# 		del_idx += 1 

inp_data = [[round(float(dat), 4) for dat in data_sample[2:]] for data_sample in upd_data]
out_data = [dir_map[data_sample[1]] for data_sample in upd_data]