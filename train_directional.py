import keras

from models import future_direction_conv
import numpy as np

from settings import *


def make_labels(x, y):
    price_diff = y[:, -1, 0] - x[:, -1, 0]
    return price_diff > 0


class SaveModel(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        acc = int(logs['val_acc'] * 100)
        if acc > 60 or (self.accepted_acc is not None and acc - self.accepted_acc >= 1):
            self.model.save('assets/directional_{}.h5'.format(acc))
            self.accepted_acc = acc


if __name__ == '__main__':
    x_train = np.load('cache/x_train.npy')
    y_raw = np.load('cache/y_train.npy')
    y_train = make_labels(x_train, y_raw)

    x_valid = np.load('cache/x_test.npy')
    y_valid = np.load('cache/y_test.npy')
    y_valid = make_labels(x_valid, y_valid)

    ensure_dir_exists(os.path.join(ROOT_DIR, 'assets'))

    model = future_direction_conv(x_train.shape)

    cb_save = SaveModel()

    train_history = model.fit(
        x_train, y_train, epochs=50, batch_size=128, shuffle=True,
        validation_data=(x_valid, y_valid),
        callbacks=[cb_save]
    )
    print("\nTraining complete!\n")
