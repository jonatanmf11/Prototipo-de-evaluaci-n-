import numpy as np
import json
from sklearn import svm
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime
from application.metrics.functional.ICF import ICF

def evaluate_icf_model_traceable(
    n_samples=100,
    n_features=3,
    noise=0.05,
    save_path="application/dataevaluacion/experimentoICF.json",
    random_state=None,
    verbose=True
):
    if random_state is not None:
        np.random.seed(random_state)

    # =========================
    # 1. Dataset
    # =========================
    X = np.random.rand(n_samples, n_features)
    weights = np.random.rand(n_features)

    y_true = X @ weights
    y_true = y_true / y_true.max()

    noise_vector = np.random.normal(0, noise, size=n_samples)
    y_true_noisy = np.clip(y_true + noise_vector, 0, 1)

    # =========================
    # 2. Modelo
    # =========================
    model = svm.SVR()
    model.fit(X, y_true_noisy)

    # =========================
    # 3. Predicción
    # =========================
    y_pred = model.predict(X)

    # =========================
    # 4. Métricas
    # =========================
    mae = mean_absolute_error(y_true_noisy, y_pred)
    r2 = r2_score(y_true_noisy, y_pred)

    # =========================
    # 5. Artifact pairs
    # =========================
    artifact_pairs_true = [{"equivalence": float(v)} for v in y_true_noisy]
    artifact_pairs_pred = [{"equivalence": float(v)} for v in y_pred]

    # =========================
    # 6. Reporte
    # =========================
    experiment_report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "random_state": random_state
        },
        "configuration": {
            "n_samples": n_samples,
            "n_features": n_features,
            "noise": noise
        },
        "dataset": {
            "X": X.tolist(),
            "weights_used": weights.tolist(),
            "y_true_clean": y_true.tolist(),
            "noise_vector": noise_vector.tolist(),
            "y_true_final": y_true_noisy.tolist()
        },
        "model": {
            "type": "SVR",
            "parameters": model.get_params()
        },
        "predictions": {
            "y_pred": y_pred.tolist()
        },
        "metrics": {
            "MAE": float(mae),
            "R2": float(r2)
        }
    }

    with open(save_path, "w") as f:
        json.dump(experiment_report, f, indent=4)

    # =========================
    # 7. Impresión de resultados
    # =========================
    if verbose:
        print("\n===== RESULTADOS DEL EXPERIMENTO ICF =====")
        print(f"Muestras: {n_samples}")
        print(f"Características: {n_features}")
        print(f"Ruido: {noise}")
        print("----------------------------------------")
        print(f"MAE: {mae:.6f}")
        print(f"R²:  {r2:.6f}")
        print("----------------------------------------")

        # Estadísticas adicionales útiles para tesis
        print("Estadísticas adicionales:")
        print(f"Media y_true: {np.mean(y_true_noisy):.4f}")
        print(f"Media y_pred: {np.mean(y_pred):.4f}")
        print(f"Desv y_true:  {np.std(y_true_noisy):.4f}")
        print(f"Desv y_pred:  {np.std(y_pred):.4f}")

        print("----------------------------------------")
        print(f"Archivo guardado en: {save_path}")
        print("========================================\n")

    # =========================
    # 8. Retorno
    # =========================
    return {
        "model": model,
        "X": X,
        "y_true": y_true_noisy,
        "y_pred": y_pred,
        "weights": weights,
        "noise_vector": noise_vector,
        "MAE": mae,
        "R2": r2,
        "artifact_pairs_true": artifact_pairs_true,
        "artifact_pairs_pred": artifact_pairs_pred,
        "report": experiment_report,
        "file": save_path
    }
    
if __name__ == "__main__":
    result = evaluate_icf_model_traceable(
        n_samples=200,
        random_state=42,
        save_path="application/dataevaluacion/experimentoICF.json"
    )

    print("ICF cálculo manual:")

    icf = ICF(artifact_pairs=result["artifact_pairs_pred"])
    print("ICF:", icf.calculate(None))