import numpy as np
from keras.models import Sequential
from keras.layers import Dense



# Generate some random data for the model
x_data = np.random.rand(100, 2).astype(np.float32)
y_data = np.random.randint(0, 2, (100, 1)).astype(np.float32)

# Create a Sequential model
model = Sequential()

# Add a dense fully connected layer with 4 neurons and 2 input neurons
model.add(Dense(4, input_dim=2, activation='sigmoid'))

# Add a dense fully connected layer with 1 neuron as output
model.add(Dense(1, activation='sigmoid'))

# Compile the model with binary_crossentropy as loss function
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model on the data
model.fit(x_data, y_data, epochs=200000, batch_size=10)
