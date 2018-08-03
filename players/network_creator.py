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

    x = Dense(16)(merge_layer)
    x = ELU()(x)
    x = Dense(16)(merge_layer)
    x = ELU()(x)
    output = Dense(1, activation='tanh')(x)

    model = Model(input=[board_input, action_input], output=[output])

    adam = Adam(lr=learning_rate)
    model.compile(optimizer=Adam(lr=learning_rate), loss='mse')

    #from keras.utils.vis_utils import plot_model
    #graph = plot_model(model, to_file='dqn_model_8x8.png', show_shapes=True)

    return model


    '''prev'''
    model_v = Sequential([
        InputLayer([n, n]),
        Reshape([n, n, 1]),
        Conv2D(64, (n, 1)),
        ELU(),
        Conv2D(64, (1, 1)),
        ELU(),
        Flatten()
    ])

    model_h = Sequential([
        InputLayer([n, n]),
        Reshape([n, n, 1]),
        Conv2D(64, (1, n)),
        ELU(),
        Conv2D(64, (1, 1)),
        ELU(),
        Flatten()
    ])

    model_2x2 = Sequential([
        InputLayer([n, n]),
        Reshape([n, n, 1]),
        Conv2D(64, (2, 2)),
        ELU(),
        Conv2D(64, (1, 1)),
        ELU(),
        Flatten()
    ])

    merge_layer = Concatenate()([
        model_v(board_input),
        model_h(board_input),
        model_2x2(board_input),
        model_v(action_input),
        model_h(action_input),
        model_2x2(action_input)
    ])
    '''

    merge_layer = merge([
        model_v(board_input),
        model_h(board_input),
        model_2x2(board_input),
        model_v(action_input),
        model_h(action_input),
        model_2x2(action_input)
    ], mode='concat', concat_axis=-1)
    '''

    x = Dense(1024)(merge_layer)
    x = BatchNormalization()(x)
    x = ELU()(x)
    x = Dense(512)(x)
    x = BatchNormalization()(x)
    x = ELU()(x)
    x = Dense(256)(x)
    x = BatchNormalization()(x)
    x = ELU()(x)
    x = Dense(128)(x)
    x = BatchNormalization()(x)
    x = ELU()(x)
    output = Dense(1, activation='tanh')(x)

    model = Model(input=[board_input, action_input], output=[output])

    adam = Adam(lr=learning_rate)
    model.compile(optimizer=Adam(lr=learning_rate), loss='mse')

    return model

if __name__ == '__main__':
    create_model(4).summary()
