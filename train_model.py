import numpy as np
import keras
from matplotlib import pyplot
import cv2
import os
from sklearn import metrics
from sklearn import svm as SVM


def plot_training(label_train: str, label_val: str, title: str, y_label: str, train_data: list, val_data: list,
                  epochs: range):
    pyplot.figure(label_train)
    pyplot.plot(epochs, train_data, "bo", label=label_train)
    pyplot.plot(epochs, val_data, "r", label=label_val)
    pyplot.title(title)
    pyplot.xlabel("Epochs")
    pyplot.ylabel(y_label)
    pyplot.legend()
    graph_path = "graficos"

    if not os.path.isdir(graph_path):
        os.mkdir(graph_path)

    pyplot.savefig(os.path.join(graph_path, title), format="svg")

    pyplot.show()


def load_dataset(file_name: str) -> (np.array, np.array, np.array, np.array):
    x_test, x_train, y_test, y_train = np.load(file_name).values()

    x = x_train.astype("float32") / 255
    x_val = x_test.astype("float32") / 255
    return x, x_val, y_train, y_test


def show_image(name_window: str, image: np.array):
    cv2.namedWindow(name_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_window, image)
    cv2.waitKey()


def reshape_to_plot(y_pred: np.array, y_true: np.array) -> (np.array, np.array):
    return y_pred.reshape((y_pred.shape[0], 200, 200)), y_true.reshape((y_true.shape[0], 200, 200))


def show_y_pred(y_pred: np.array, y_true: np.array):
    y_pred, y_true = reshape_to_plot(y_pred, y_true)
    for pred, true in zip(y_pred, y_true):
        show_image("True", true)
        show_image("Pred", pred)


def build_model(input_shape: tuple, output_size: int) -> keras.Sequential:
    model = keras.Sequential()
    model.add(keras.layers.Conv2D(64, kernel_size=3, activation="relu", input_shape=input_shape))
    model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.25))

    model.add(keras.layers.Conv2D(64, kernel_size=3, activation="relu"))
    model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.25))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation="relu"))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(output_size, activation=keras.activations.softmax))
    model.compile(optimizer=keras.optimizers.Adadelta(), loss=keras.losses.categorical_crossentropy,
                  metrics=["accuracy"])
    return model


def plot_history(history: dict, plot=False) -> None:
    val_loss = history["val_loss"]
    val_acc = history["val_accuracy"]
    loss = history["loss"]
    acc = history["accuracy"]
    epochs = range(1, len(acc) + 1)

    if plot:
        pyplot.ion()
    else:
        pyplot.ioff()

    plot_training("Training loss", "Validation loss", "Training and validation loss Pornography_Database", "Loss",
                  loss, val_loss, epochs)

    plot_training("Training acc", "Validation acc", "Training and validation accuracy Pornography_Database", "Accuracy",
                  acc, val_acc, epochs)


def train_deep_learning(x: np.array, x_test: np.array, y_train: np.array, y_test: np.array, epochs: int,
                        batch_size=None) -> keras.Model:
    y_train_categorical = keras.utils.to_categorical(y_train, 2)
    y_test_categorical = keras.utils.to_categorical(y_test, 2)

    model = build_model(x[0].shape, y_train_categorical[0].size)

    history = model.fit(x, y_train_categorical, batch_size=batch_size, epochs=epochs,
                        validation_data=(x_test, y_test_categorical)).history

    plot_history(history)

    model.save("teddy_model")

    return model


def train_svm(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray) -> (SVM.NuSVC, list):
    x: np.ndarray = x_train.reshape((x_train.shape[0], -1))

    x_val: np.ndarray = x_test.reshape((x_test.shape[0], -1))

    svm = SVM.NuSVC(gamma=5)
    svm.fit(x, y_train)
    y_pred = svm.predict(x_val)

    return svm, y_pred


def type_to_char(n: int) -> str:
    if n == 0:
        return "Non Porn"
    else:
        return "Porn"


def evaluate_classifier(y_pred: np.ndarray, y_true: np.ndarray):
    y_pred_char_array = [type_to_char(int(np.argmax(pred))) for pred in y_pred]

    y_true_char_array = [type_to_char(true) for true in y_true]

    matrix = metrics.confusion_matrix(y_true_char_array, y_pred_char_array, labels=["Porn", "Non Porn"])

    print(matrix)


def evaluate_deep_learning(saved_weights: str, x_test: np.ndarray, y_test: np.ndarray):
    model: keras.models.Model = keras.models.load_model(saved_weights)

    y_pred = model.predict(x_test, use_multiprocessing=True)

    evaluate_classifier(y_pred, y_test)


def main():
    x, x_val, y_train, y_test = load_dataset("dataset/Pornography_Database.npz")

    print("training Deep Learning")
    train_deep_learning(x, x_val, y_train, y_test, 20)

    print("Deep Leaning Results")
    evaluate_deep_learning("teddy_model", x_val, y_test)

    print("training SVM")
    svm, y_pred = train_svm(x, y_train, x_val, y_test)

    print("SVM results")
    evaluate_classifier(y_pred, y_test)



if __name__ == '__main__':
    main()
