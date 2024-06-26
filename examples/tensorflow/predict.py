import mlflow
import numpy as np

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# Prepare the data for predictions
X_test = np.random.uniform(size=[3, 28, 28, 3])

try:
    # Try to load the champion model
    champion_model = mlflow.pyfunc.load_model("models:/tensorflow-example@champion")
    predictions = champion_model.predict(X_test)
    print(predictions)
except mlflow.MlflowException:
    print("The model hasn't been registered or assigned an alias yet.")
