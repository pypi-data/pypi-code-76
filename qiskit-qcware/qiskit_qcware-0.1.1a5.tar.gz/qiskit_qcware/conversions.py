from qiskit.providers import Options
from qiskit.circuit import QuantumCircuit as QiskitCircuit
from qiskit.result.models import (ExperimentResult, ExperimentResultData)
from quasar import Circuit as QuasarCircuit
from quasar import Backend as QuasarBackend
from quasar import ProbabilityHistogram as QuasarProbabilityHistogram
from qcware_transpile.translations.qiskit.to_quasar import translate  # type: ignore
from typing import Dict


def quasar_circuit_from_qiskit(c: QiskitCircuit) -> QuasarCircuit:
    result = translate(c)
    return result


def qiskit_circuit_measurement_map(c: QiskitCircuit) -> Dict[int, int]:
    """Creates a map from qubit index to classical bit index,
    used to remap the quasar measurement histogram to a qiskit
    count result
    """
    measurements = [x for x in c.data if x[0].name == 'measure']
    return {
        c.qubits.index(x[1][0]): c.clbits.index(x[2][0])
        for x in measurements
    }


def remap_histogram_key(original_key: int, bit_map: Dict[int, int]) -> int:
    """Quasar histogram keys are a bitstring representing the state
    of the vector (0101 -> 5).  We have the problem where those
    bits are mapped into the classical bits via the measurement map
    (see qiskit_circuit_measurement_map).  This function does that remapping.
    (assuming LSB to the right at first)
    For example, if the key is 0101 (5), and we have mapped bit 0 to 0 and bit 2 to 1,
    the new key is 11 (3)
    """
    result = 0
    for k, v in bit_map.items():
        result = result | (((original_key >> k) & 1) << v)
    return result


def remap_probability_histogram(
        h: QuasarProbabilityHistogram,
        bit_map: Dict[int, int] = None) -> Dict[str, int]:
    count_histogram = h.to_count_histogram()
    if bit_map is None:
        result = {hex(k): v for k, v in count_histogram.items()}
    else:
        result = {}
        for k, v in count_histogram.items():
            new_k = hex(remap_histogram_key(k, bit_map))
            result[new_k] = result.get(new_k, 0) + v
    return result


def qiskit_experiment_result_from_quasar_probability_histogram(
        h: QuasarProbabilityHistogram, bit_map: Dict[int,
                                                     int]) -> ExperimentResult:
    # it's possible for a null bit map if there are no measurement gates, in which
    # case the aer simulator returns {} for counts since nothing is measured
    qiskit_counts = remap_probability_histogram(
        h, bit_map) if len(bit_map) > 0 else {}
    experiment_data = ExperimentResultData(counts=qiskit_counts)
    experiment_result = ExperimentResult(shots=h.nmeasurement,
                                         success=True,
                                         data=experiment_data)
    # meas_level = MeasLevel.CLASSIFIED, meas_return = MeasLevel.AVERAGE ?
    # TODO must set jobj_id and job_id
    return experiment_result


def measurement_result_from_qiskit_circuit(
    qiskit_circuit: QiskitCircuit,
    options: Options,
    backend: QuasarBackend,
) -> ExperimentResult:
    bit_map = qiskit_circuit_measurement_map(qiskit_circuit)
    quasar_circuit: QuasarCircuit = quasar_circuit_from_qiskit(qiskit_circuit)
    probability_histogram: QuasarProbabilityHistogram = backend.run_measurement(
        circuit=quasar_circuit, nmeasurement=options.shots)
    result: ExperimentResult = qiskit_experiment_result_from_quasar_probability_histogram(
        probability_histogram, bit_map)
    return result


def qiskit_experiment_result_from_statevector(sv) -> ExperimentResult:
    experiment_data = ExperimentResultData(statevector=sv)
    experiment_result = ExperimentResult(shots=1,
                                         success=True,
                                         data=experiment_data)
    return experiment_result


def statevector_result_from_qiskit_circuit(
        qiskit_circuit: QiskitCircuit, options: Options,
        backend: QuasarBackend) -> ExperimentResult:
    quasar_circuit: QuasarCircuit = quasar_circuit_from_qiskit(qiskit_circuit)
    sv = backend.run_statevector(circuit=quasar_circuit)
    result: ExperimentResult = qiskit_experiment_result_from_statevector(sv)
    return result
