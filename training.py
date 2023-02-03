import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Dropout
#from tensorflow.python.keras.utils import to_categorical
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
from sklearn import metrics

df = pd.read_pickle(
    "wakeword implementation\\final_audio_data_csv/audio_data.csv")
x = df['feature'].values
x = np.concatenate(x, axis=0).reshape(len(x), 40)

y = np.array(df["class_label"].tolist())
y = to_categorical(y)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)

model = Sequential([
    Dense(256, input_shape=x_train[0].shape),
    Activation("relu"),
    Dropout(0.5),
    Dense(256),
    Activation("relu"),
    Dropout(0.5),
    Dense(2, activation="softmax"),
])

print(model.summary())
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print("Model Score: \n")
history = model.fit(x_train, y_train, epochs=1000)
model.save('wakeword implementation\\saved_model/WWD.h5')
score = model.evaluate(x_test, y_test)
print(score)


print("Model classification report: \n")
y_pred = np.argmax(model.predict(x_test), axis=1)
cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
print(classification_report(np.argmax(y_test, axis=1), y_pred))
# plot_confusion_matrix(
#    cm, classes=['Does not contain wake word', "has wake word"])


cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[
                                            'Does not contain wake word', "has wake word"])

cm_display.plot()
plt.show()
