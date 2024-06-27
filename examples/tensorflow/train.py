import keras
import mlflow
import numpy as np
from mlflow.models import ModelSignature
from mlflow.types import Schema, TensorSpec

# Set the tracking server URI for logging
mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# Set/create a new MLflow experiment
mlflow.set_experiment("TensorFlow Example")

# Enable autologging
mlflow.tensorflow.autolog(log_models=False, checkpoint=False)

# Prepare data for a 2-class classification
X_train = np.random.uniform(size=[1000, 28, 28, 3])
y_train = np.random.randint(2, size=1000)

# Create a model
model = keras.Sequential(
    [
        keras.Input([28, 28, 3]),
        keras.layers.Conv2D(8, 2),
        keras.layers.MaxPool2D(2),
        keras.layers.Flatten(),
        keras.layers.Dense(2),
        keras.layers.Softmax(),
    ]
)
model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(),
    optimizer="Adam",
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

# Specify the model's signature and provide an input example from the training data
input_schema = Schema(
    [
        TensorSpec(np.dtype(np.float64), (-1, 28, 28, 3), "input"),
    ]
)
output_schema = Schema([TensorSpec(np.dtype(np.float32), (-1, 2), "output")])
signature = ModelSignature(inputs=input_schema, outputs=output_schema)
input_example = X_train[:3, :]

# Start tracking the training process
with mlflow.start_run() as train:
    model.fit(
        X_train,
        y_train,
        batch_size=32,
        epochs=10,
        validation_split=0.1,
        callbacks=[
            keras.callbacks.ModelCheckpoint(
                filepath="checkpoints/tensorflow-example.keras",
                monitor="val_loss",
                mode="min",
                save_best_only=True,
            )
        ],
    )
    mlflow.tensorflow.log_model(
        model,
        "tensorflow-example",
        input_example=input_example,
        signature=signature,
        pip_requirements=["-r requirements.txt"],
    )
