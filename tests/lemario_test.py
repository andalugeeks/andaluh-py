# - Ksar Feui <a.moreno.losana@gmail.com>
# - J. Félix Ontañón <felixonta@gmail.com>
# - Sergio Soto <scots4ever@gmail.com>

import csv
import pprint
from pathlib import Path

import andaluh


# Función legacy para compatibilidad (opcional)
def lemario():
    """Test legacy que muestra estadísticas generales"""
    file = Path(__file__).parent / "lemario_cas_and.csv"
    
    transcription_errors = []
    stats = {"total": 0, "ok": 0, "fail": 0}

    with open(file) as fh:
        rd = csv.DictReader(fh, delimiter=',')

        for row in rd:
            caste = row['cas']
            andal = row['and']
            trans = andaluh.epa(row['cas'])

            if andal != trans:
                transcription_errors.append((caste, andal, trans))
                stats["fail"] += 1
            else:
                stats["ok"] += 1

            stats["total"] += 1
    
    # Solo mostrar errores si los hay
    if transcription_errors:
        print("\nErrores de transcripción encontrados:")
        for error in transcription_errors[:10]:  # Limitar a 10 primeros errores
            print(f"{error[0]} => Esperado: {error[1]}, Obtenido: {error[2]}")
        if len(transcription_errors) > 10:
            print(f"... y {len(transcription_errors) - 10} errores más")

    print(f"\nEstadísticas del lemario:")
    pprint.pprint(stats)
    
    # El test pasa si hay al menos un 95% de aciertos
    success_rate = stats["ok"] / stats["total"] if stats["total"] > 0 else 0
    assert success_rate >= 0.95, f"Tasa de éxito muy baja: {success_rate:.2%}"

if __name__ == "__main__":
    lemario()