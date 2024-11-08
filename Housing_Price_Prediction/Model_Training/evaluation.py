import numpy as np
import mlflow
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import json
from datetime import datetime
import os

def evaluate_model(model, config, X_test, y_test):
    """
    Evaluates the model on the test data and logs metrics to MLflow.
    Args:
        model: The trained model to evaluate.
        config (dict): The configuration dictionary containing settings for evaluation.
        X_test: The features of the test dataset.
        y_test: The true labels of the test dataset.
    Returns:
        tuple: Predictions from the model and a dictionary of evaluation metrics.
    """
    print("Generating predictions...")
    predictions = model.predict(X_test)

    evaluation_metrics = {
        'mean_squared_error': mean_squared_error(y_test, predictions),
        'root_mean_squared_error': np.sqrt(mean_squared_error(y_test, predictions)),
        'mean_absolute_error': mean_absolute_error(y_test, predictions),
        'r2_score': r2_score(y_test, predictions)
    }

    with mlflow.start_run(nested=True):                    # Start an MLflow run for logging
        mlflow.log_metrics(evaluation_metrics)
        print("Evaluation metrics logged to MLflow.")
    
    if config.get('save_predictive_evaluations', False):
        eval_dir = "cvResults_bestModels"                  # Directory to save evaluation metrics
        os.makedirs(eval_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        eval_filename = f"predictive_evaluations_{model.__class__.__name__}_{timestamp}.json"
        eval_filepath = os.path.join(eval_dir, eval_filename)

        with open(eval_filepath, 'w') as f:
            json.dump(evaluation_metrics, f)
        print(f"Evaluation metrics saved at {eval_filepath}")
    
    return predictions, evaluation_metrics
