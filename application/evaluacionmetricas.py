import csv
from sklearn.metrics import mean_absolute_error, r2_score
from application.metrics.functional.ICF import ICF
import random


def main(): 
    
    ruta_entrada = "application/DataevaluacionMetricas/ICF/dataICF.csv"
    ruta_salida = "application/DataevaluacionMetricas/ICF/dataResultadosICF.csv"

    resultados = []
    calculados = []
    calculados_ruido = []

    with open(ruta_entrada, newline='', encoding='utf-8') as archivo_in, \
         open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_out:

        lector = csv.DictReader(archivo_in, delimiter=';')

        # nuevas columnas data 
        columnas_ruido = [f'Equivalencia{i}_ruido' for i in range(1, 21)]
        fieldnames = lector.fieldnames + columnas_ruido + ['resultadoCalculado', 'resultadoRuido']
        escritor = csv.DictWriter(archivo_out, fieldnames=fieldnames, delimiter=';')

        escritor.writeheader()

        for fila in lector:
            # crear lista de equivalencias
            equivalencias = [
                float(fila[f'Equivalencia{i}'].replace(',', '.'))
                for i in range(1, 21)
            ]

            # 🔹 Resultado real
            real = float(fila['Resultado ICF'].replace(',', '.'))

            # 🔹 Calculo normal
            artifact_pairs = [{"equivalence": valor} for valor in equivalencias]
            icf = ICF(artifact_pairs=artifact_pairs)
            calculado = icf.calculate(model=None)
            
                
            #Calculo con ruido
            eq_ruido = [
                max(0.0, min(1.0, v + random.uniform(-0.05, 0.05)))
                for v in equivalencias
            ]
            
            for i in range(20):
                fila[f'Equivalencia{i+1}_ruido'] = f"{eq_ruido[i]:.6f}"

            artifact_pairs_ruido = [{"equivalence": valor} for valor in eq_ruido]
            icf_ruido = ICF(artifact_pairs=artifact_pairs_ruido)
            calculado_ruido = icf_ruido.calculate(model=None)

            
            resultados.append(real)
            calculados.append(calculado)
            calculados_ruido.append(calculado_ruido)

            # Data salida 
            fila['resultadoCalculado'] = f"{calculado:.6f}"
            fila['resultadoRuido'] = f"{calculado_ruido:.6f}"

            escritor.writerow(fila)

    # Resultado metricas MAE y R2
    print("MAE:", mean_absolute_error(resultados, calculados))
    print("R2:", r2_score(resultados, calculados))

    print("MAE con ruido:", mean_absolute_error(resultados, calculados_ruido))
    print("R2 con ruido:", r2_score(resultados, calculados_ruido))


if __name__ == "__main__":
    main()