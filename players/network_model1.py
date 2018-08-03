from keras.models import Sequential, Model
from keras.layers import (Dense, Dropout, Flatten,
                Conv2D, MaxPooling2D, InputLayer, Reshape,
                        merge, Input, Concatenate)
from keras.layers.pooling import AveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.optimizers import Adam

def create_model(n, learning_rate=1e-4):
    board_input = Input(shape=[n, n])
    action_input = Input(shape=[n, n])

    #aaaaa
    m1 = Sequential([
        InputLayer([n,n]),
        Flatten()])
    merge_layer = Concatenate()([
        m1(board_input),
        m1(action_input)
    ])

    # x = Dense(16)(merge_layer)
    # x = ELU()(x)
    # x = Dense(16)(merge_layer)
    # x = ELU()(x)
    # output = Dense(1, activation='tanh')(x)

    y = InputLayer([n, n])(merge_layer)
    y = Reshape([n, n, 1])(y)
    y = Conv2D(64, (n, 1))(y)
    y = ELU()(y)
    y = Conv2D(64, (1, 1))(y)
    y = ELU()(y)
    y = Flatten()(y)

    output = Dense(1, activation='tanh')(y)

    model = Model(input=[board_input, action_input], output=[output])

    adam = Adam(lr=learning_rate)
    model.compile(optimizer=adam(lr=learning_rate), loss='mse')

    #from keras.utils.vis_utils import plot_model
    #graph = plot_model(model, to_file='dqn_model_8x8.png', show_shapes=True)

    return model