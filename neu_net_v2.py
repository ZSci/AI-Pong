import tflearn as tfl

from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

from data_preprocess import inp_data, out_data

network = input_data(shape=[None, 5], name='input')

network = fully_connected(network, 128, activation='relu')
network = dropout(network, 0.8)

network = fully_connected(network, 256, activation='relu')
network = dropout(network, 0.8)

network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.8)

network = fully_connected(network, 256, activation='relu')
network = dropout(network, 0.8)

network = fully_connected(network, 128, activation='relu')
network = dropout(network, 0.8)

network = fully_connected(network, 3, activation='softmax')
network = regression(network, optimizer='adam', learning_rate=1e-3, loss='categorical_crossentropy', name='targets')

model = tfl.DNN(network)

if __name__ == '__main__':
	model.fit(inp_data, out_data, n_epoch = 1000, batch_size = 16, show_metric = True)
	model.save('model_v4.tfl')