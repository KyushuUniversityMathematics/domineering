from keras.models import Sequential, Model
from keras.layers import (Dense, Dropout, Flatten,
                Conv2D, MaxPooling2D, InputLayer, Reshape,
                        merge, Input, Concatenate)
from keras.layers.pooling import AveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.optimizers import Adam

def create_td_model(n, learning_rate=1e-4):
    board_input = Input(shape=[n, n])
    N = n**2 * 2

    x = InputLayer([n, n])(board_input)
    x = Flatten()(x)
    x = Dense(N)(x)
    x = ELU()(x)
    x = Dense(N)(x)
    x = ELU()(x)
    x = Dense(N)(x)
    x = ELU()(x)

    y = InputLayer([n, n])(board_input)
    y = Reshape([n, n, 1])(y)
    y = Conv2D(64, (n, 1))(y)
    y = ELU()(y)
    y = Conv2D(64, (1, 1))(y)
    y = ELU()(y)
    y = Flatten()(y)

    z = InputLayer([n, n])(board_input)
    z = Reshape([n, n, 1])(z)
    z = Conv2D(64, (1, n))(z)
    z = ELU()(z)
    z = Conv2D(64, (1, 1))(z)
    z = ELU()(z)
    z = Flatten()(z)

    w = InputLayer([n, n])(board_input)
    w = Reshape([n, n, 1])(w)
    w = Conv2D(64, (2, 2))(w)
    w = ELU()(w)
    w = Conv2D(64, (2, 2))(w)
    w = ELU()(w)
    w = Flatten()(w)

    merged = Concatenate()([x, y, z])
    merged = Dense(4*N)(merged)
    merged = ELU()(merged)
    merged = Dense(2*N)(merged)
    merged = ELU()(merged)
    merged = Dense(N)(merged)
    merged = ELU()(merged)
    merged = Dense(N)(merged)
    merged = ELU()(merged)

    output = Dense(1, activation='tanh')(merged)

    model = Model(input=[board_input], output=[output])

    model.compile(optimizer=Adam(lr=learning_rate), loss='mse')

    # visualise the model
    #model.summary()
    from keras.utils.vis_utils import plot_model
    graph = plot_model(model, to_file = 'td_model_8x8.png', show_shapes=True)

    return model
