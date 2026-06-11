import csv
import json
from sklearn.metrics import mean_absolute_error, r2_score
from application.metrics.functional.ICF import ICF
from application.metrics.functional.mismatch import Mismatch
from application.metrics.sequential.ICS import ICS
from application.metrics.formal.CPT import CPT
from application.metrics.formal.CAF import CAF
def main(): 
    def to_float(valor):
        return float(valor.replace(",", "."))

    ruta_entradaICF = "application/DataevaluacionMetricas/ICF/dataICF.csv"
    ruta_salidaICF = "application/DataevaluacionMetricas/ICF/dataResultadosICF.csv"

    resultadosICF = []
    calculadosICF = []
    

    with open(ruta_entradaICF, newline='', encoding='utf-8') as archivo_in, \
         open(ruta_salidaICF, mode='w', newline='', encoding='utf-8') as archivo_out:

        lector = csv.DictReader(archivo_in, delimiter=';')

        # nuevas columnas data 
    
        fieldnames = lector.fieldnames + ['resultadoCalculado']
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
            

            
            resultadosICF.append(real)
            calculadosICF.append(calculado)

            # Data salida 
            fila['resultadoCalculado'] = f"{calculado:.6f}"

            escritor.writerow(fila)

    # Resultado metricas MAE y R2
    print("MAE ICF:", mean_absolute_error(resultadosICF, calculadosICF))
    print("R2 ICF: ", r2_score(resultadosICF, calculadosICF))


    #Evaluación mismatch
    
    ruta_entradaMismatch = "application/DataevaluacionMetricas/mismatch/dataMismatch.csv"
    ruta_salidaMismatch = "application/DataevaluacionMetricas/mismatch/dataResultadosMismatch.csv"

    resultados_realesMismatch = []
    resultados_calculadosMismatch = []

    with open(ruta_entradaMismatch, newline='', encoding='utf-8') as archivo_in, \
         open(ruta_salidaMismatch, mode='w', newline='', encoding='utf-8') as archivo_out:

        lector = csv.DictReader(archivo_in, delimiter=';')

        fieldnames = lector.fieldnames + [
            "MismatchAgilCalculado",
            "MismatchTradicionalCalculado",
            "MismatchHibridoCalculado",
            "MismatchTotalCalculado"
        ]

        escritor = csv.DictWriter(
            archivo_out,
            fieldnames=fieldnames,
            delimiter=';'
        )

        escritor.writeheader()

        for fila in lector:
    
            characteristics = []

            for i in range(1, 7):

                characteristics.append({
                    "projectValue": to_float(
                        fila[f"Caracteristica{i}"]
                    ),
                    "weight": to_float(
                        fila[f"Peso{i}"]
                    ),
                    "methodologies": {
                        "agil": to_float(
                            fila[f"Agil{i}"]
                        ),
                        "tradicional": to_float(
                            fila[f"Tradicional{i}"]
                        ),
                        "hibrido": to_float(
                            fila[f"Hibrido{i}"]
                        )
                    }
                })

            mismatch_data = {
                "characteristics": characteristics
            }

            mismatch_agil = Mismatch(
                mismatch_data,
                "agil"
            ).calculate()

            mismatch_tradicional = Mismatch(
                mismatch_data,
                "tradicional"
            ).calculate()

            mismatch_hibrido = Mismatch(
                mismatch_data,
                "hibrido"
            ).calculate()

            mismatch_total = (
                mismatch_agil
                + mismatch_tradicional
                + mismatch_hibrido
            )

            resultado_real = to_float(
                fila["MismatchScore"]
            )
            
            resultados_realesMismatch.append(resultado_real)
            resultados_calculadosMismatch.append(mismatch_total)

            fila["MismatchAgilCalculado"] = f"{mismatch_agil:.4f}"
            fila["MismatchTradicionalCalculado"] = f"{mismatch_tradicional:.4f}"
            fila["MismatchHibridoCalculado"] = f"{mismatch_hibrido:.4f}"
            fila["MismatchTotalCalculado"] = f"{mismatch_total:.4f}"

            escritor.writerow(fila)
         
        print(
            "MAE Mismatch:",
            mean_absolute_error(
                resultados_realesMismatch,
                resultados_calculadosMismatch
            )
        )

        print(
            "R2 Mismatch:",
            r2_score(
                resultados_realesMismatch,
                resultados_calculadosMismatch
            )
        )


    ruta_entradaICS = "application/DataevaluacionMetricas/ICS/dataICS.csv"
    ruta_salidaICS = "application/DataevaluacionMetricas/ICS/dataResultadosICS.csv"

    resultados_realesICS = []
    resultados_calculadosICS = []

    with open(ruta_entradaICS, newline='', encoding='utf-8') as archivo_in, \
         open(ruta_salidaICS, mode='w', newline='', encoding='utf-8') as archivo_out:

        lector = csv.DictReader(archivo_in, delimiter=';')

        fieldnames = lector.fieldnames + ["ICSCalculado"]

        escritor = csv.DictWriter(
            archivo_out,
            fieldnames=fieldnames,
            delimiter=';'
        )

        escritor.writeheader()

        for fila in lector:

            violaciones = int(fila["Violaciones"])
            transiciones = int(fila["transiciones"])

            resultado_real = to_float(fila["ICS"])

            # Cálculo de la métrica
            if transiciones == 0:
                calculado = 1.0
            else:
                calculado = 1 - (violaciones / transiciones)

            calculado = max(0.0, min(1.0, calculado))

            resultados_realesICS.append(resultado_real)
            resultados_calculadosICS.append(calculado)

            fila["ICSCalculado"] = f"{calculado:.9f}"

            escritor.writerow(fila)

    print(
        "MAE ICS:",
        mean_absolute_error(
            resultados_realesICS,
            resultados_calculadosICS
        )
    )

    print(
        "R2 ICS:",
        r2_score(
            resultados_realesICS,
            resultados_calculadosICS
        )
    )
    ruta_entradaNSR = "application/DataevaluacionMetricas/NSR/dataNSR.csv"
    ruta_salidaNSR = "application/DataevaluacionMetricas/NSR/dataResultadosNSR.csv"

    resultados_realesNSR = []
    resultados_calculadosNSR = []

    with open(ruta_entradaNSR, newline='', encoding='utf-8') as archivo_in, \
        open(ruta_salidaNSR, mode='w', newline='', encoding='utf-8') as archivo_out:

        lector = csv.DictReader(archivo_in, delimiter=';')

        fieldnames = lector.fieldnames + ["NSRCalculado"]

        escritor = csv.DictWriter(
            archivo_out,
            fieldnames=fieldnames,
            delimiter=';'
        )

        escritor.writeheader()

        for fila in lector:

            violaciones = int(fila["Violaciones"])
            responsabilidades = int(fila["Roles"])

            resultado_real = to_float(fila["NSR"])

            if responsabilidades == 0:
                calculado = 1.0
            else:
                calculado = (
                    1
                    - (violaciones / responsabilidades)
                )

            calculado = max(0.0, min(1.0, calculado))

            resultados_realesNSR.append(resultado_real)
            resultados_calculadosNSR.append(calculado)

            fila["NSRCalculado"] = f"{calculado:.9f}"

            escritor.writerow(fila)

    print(
        "MAE NSR:",
        mean_absolute_error(
            resultados_realesNSR,
            resultados_calculadosNSR
        )
    )

    print(
        "R2 NSR:",
        r2_score(
            resultados_realesNSR,
            resultados_calculadosNSR
        )
    )

    ruta_entrada = "application/DataevaluacionMetricas/CPT/dataCPT.json"
    ruta_salida = "application/DataevaluacionMetricas/CPT/dataResultadosCPT.csv"

    resultados_realesCPT = []
    resultados_calculadosCPT = []


    with open(ruta_entrada, encoding="utf-8") as archivo:
        casos = json.load(archivo)


    with open(ruta_salida, mode="w", newline="", encoding="utf-8") as archivo_out:

        fieldnames = [
            "id",
            "intersectionEsperada",
            "intersectionCalculada",
            "unionEsperada",
            "unionCalculada",
            "cptEsperado",
            "cptCalculado"
        ]

        escritor = csv.DictWriter(
            archivo_out,
            fieldnames=fieldnames,
            delimiter=";"
        )

        escritor.writeheader()

        for caso in casos:

            data = {
                "agileWorkProducts":
                    caso["agileWorkProducts"],
                "planDrivenWorkProducts":
                    caso["planDrivenWorkProducts"]
            }

            cpt = CPT(data)

            calculado = cpt.calculate()

            agile_set = set(
                caso["agileWorkProducts"]
            )

            plan_set = set(
                caso["planDrivenWorkProducts"]
            )

            intersection_calculada = len(
                agile_set.intersection(plan_set)
            )

            union_calculada = len(
                agile_set.union(plan_set)
            )

            esperado = caso["expectedCPT"]

            resultados_realesCPT.append(
                esperado
            )

            resultados_calculadosCPT.append(
                calculado
            )

            escritor.writerow({
                "id": caso["id"],
                "intersectionEsperada":
                    caso["expectedIntersection"],
                "intersectionCalculada":
                    intersection_calculada,
                "unionEsperada":
                    caso["expectedUnion"],
                "unionCalculada":
                    union_calculada,
                "cptEsperado":
                    f"{esperado:.9f}",
                "cptCalculado":
                    f"{calculado:.9f}"
            })


    print(
        "MAE CPT:",
        mean_absolute_error(
            resultados_realesCPT,
            resultados_calculadosCPT
        )
    )

    print(
        "R2 CPT:",
        r2_score(
            resultados_realesCPT,
            resultados_calculadosCPT
        )
    )
    
    
    # Evaluación CAF

    ruta_entradaCAF = (
        "application/DataevaluacionMetricas/CAF/dataCAF.json"
    )

    ruta_salidaCAF = (
        "application/DataevaluacionMetricas/CAF/dataResultadosCAF.csv"
    )
    resultados_realesCAF = []
    resultados_calculadosCAF = []

    with open(
        ruta_entradaCAF,
        encoding="utf-8"
    ) as archivo:

        casos = json.load(archivo)

    with open(
        ruta_salidaCAF,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as archivo_out:

        fieldnames = [
            "id",
            "CAFEsperado",
            "CAFCalculado",
            "ErrorAbsoluto"
        ]

        escritor = csv.DictWriter(
            archivo_out,
            fieldnames=fieldnames,
            delimiter=";"
        )

        escritor.writeheader()

        for caso in casos:

            caf = CAF(
                documentation_data=caso
            )

            calculado = caf.calculate()

            esperado = caso["expectedCAF"]

            resultados_realesCAF.append(
                esperado
            )

            resultados_calculadosCAF.append(
                calculado
            )

            escritor.writerow({
                "id":
                    caso["id"],
                "CAFEsperado":
                    f"{esperado:.6f}",
                "CAFCalculado":
                    f"{calculado:.6f}",
                "ErrorAbsoluto":
                    f"{abs(esperado-calculado):.6f}"
            })

    print(
        "MAE CAF:",
        mean_absolute_error(
            resultados_realesCAF,
            resultados_calculadosCAF
        )
    )

    print(
        "R2 CAF:",
        r2_score(
            resultados_realesCAF,
            resultados_calculadosCAF
        )
    )
    
   
if __name__ == "__main__":
    main()
