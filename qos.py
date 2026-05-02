import qiskit
import numpy as np
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from run_cal_fidelity import *
from concurrent.futures import ProcessPoolExecutor


def _calculate_partition_makespan_worker(args):
    # This worker function is executed in parallel.
    # Its purpose is to rapidly estimate the execution cost (e.g., heuristic makespan)
    # for a single partition of quantum circuits assigned to a QPU,
    # based on a defined cost model (e.g., total depth).
    pass

def get_two_qubit_gate_list(input_qasm_path):
    qc = qiskit.QuantumCircuit.from_qasm_file(input_qasm_path)
    two_qubit_pairs = []
    for instr in qc.data:
        op = instr.operation
        qubits = instr.qubits
        if len(qubits) == 2:
            q0 = qc.qubits.index(qubits[0])
            q1 = qc.qubits.index(qubits[1])
            two_qubit_pairs.append((q0, q1))
    return two_qubit_pairs

def get_gate_counts_per_layer(dag):
    layer_gate_counts = []
    for layer in dag.layers():
        subdag = layer['graph']
        gate_count = sum(1 for node in subdag.op_nodes())
        layer_gate_counts.append(gate_count)
    return layer_gate_counts

def gates_list_to_QC(gate_list):  # default all 2-q gates circuit
    Lqubit = max(max(gate) for gate in gate_list) + 1

    circ = QuantumCircuit(Lqubit)
    for two_qubit_gate in gate_list:
        circ.cz(two_qubit_gate[0], two_qubit_gate[1])

    dag = circuit_to_dag(circ)
    return circ, dag

def print_dag_layers(dag):
    for i, layer in enumerate(dag.layers()):
        subdag = layer['graph']
        gates = []
        for node in subdag.op_nodes():
            name = node.name
            qargs = [qubit._index for qubit in node.qargs]
            gates.append(qargs)

class quanta_circ():
    def __init__(self):
        self.name = ''
        self.abspath = ''
        self.qc_qiskit = None
        self.dag_width_list = []
        self.twoqu_gate_list = []
        self.allocated = False

class quputer():
    def __init__(self, max_width):
        self.time_width = []
        self.max_width = max_width

    def add_task(self, start_time, width_profile):
        if not width_profile: return
        end_time = start_time + len(width_profile)
        if end_time > len(self.time_width):
            self.time_width.extend([0] * (end_time - len(self.time_width)))

        for t in range(len(width_profile)):
            self.time_width[start_time + t] += width_profile[t]

    def find_earliest_fit(self, width_profile):
        # This method implements the core scheduling logic.
        # It searches the QPU's resource timeline (time_width) to find
        # the earliest start time at which the given `width_profile` can
        # be accommodated without exceeding the QPU's maximum width capacity.
        pass


class naos():
    def __init__(self, quputer_num):
        self.quputer_num = quputer_num
        self.scheduler_max_width = None
        self.qtc_list = []
        self.partitions = []
        self.optimized_sequences = []

    def add_qc(self, name, abspath):
        qtc = quanta_circ()
        qtc.name = name
        qtc.abspath = abspath
        qc_qiskit = QuantumCircuit.from_qasm_file(abspath)
        qtc.gates = get_2q_gates_list(qc_qiskit)
        _, qtc.dag = gates_list_to_QC(qtc.gates)
        qtc.dag_width_list = get_gate_counts_per_layer(qtc.dag)
        qtc.max_width = max(qtc.dag_width_list) if qtc.dag_width_list else 0
        qtc.depth = qc_qiskit.depth()
        self.qtc_list.append(qtc)

    def allocate(self):
        self.scheduler_max_width = self._calculate_heuristic_max_width()

        best_state, best_heuristic_makespan = self.allocate_with_simulated_annealing()

        final_partitions = [[] for _ in range(self.quputer_num)]
        for circuit_idx, qpu_idx in enumerate(best_state):
            final_partitions[qpu_idx].append(circuit_idx)
        self.partitions = final_partitions

        self.optimize_sequences()
        final_makespans = [self._calculate_makespan(seq) for seq in self.optimized_sequences]
        final_max_makespan = max(final_makespans) if final_makespans else 0

    def _calculate_energy_heuristic(self, state: list[int], executor: ProcessPoolExecutor, depths: list[int]) -> int:
        pass

    def allocate_with_simulated_annealing(self):
        pass

    def optimize_sequences(self):
        self.optimized_sequences = []
        for i, partition in enumerate(self.partitions):
            if not partition:
                self.optimized_sequences.append([])
                continue
            optimal_sequence = self._find_optimal_sequence_iterative(partition)
            self.optimized_sequences.append(optimal_sequence)

    def _find_optimal_sequence_iterative(self, circuit_indices: list[int]) -> list[int]:
        pass

    def _calculate_makespan(self, sequence_of_indices: list[int]) -> int:
        pass

    def _calculate_heuristic_max_width(self) -> int:
        if not self.qtc_list: return 1
        peak_demand = max([qtc.max_width for qtc in self.qtc_list] or [0])
        total_avg_width = sum([(sum(qtc.dag_width_list) / qtc.depth) for qtc in self.qtc_list if qtc.depth > 0])
        avg_concurrent_load = total_avg_width / self.quputer_num
        heuristic_value = max(1, int(np.ceil(avg_concurrent_load)))
        final_width = max(peak_demand, heuristic_value)
        return final_width


def reinsert_single_qubit_gates(cir_abspath, last_json):
    pass

def get_2q_gates_list(circ):
    gate_2q_list = []
    instruction = circ.data
    for ins in instruction:
        if ins.operation.num_qubits == 2:
            gate_2q_list.append((ins.qubits[0]._index, ins.qubits[1]._index))
    return gate_2q_list

def find_best_position_in_single_quputer(qtc: quanta_circ, qpu: quputer, max_width, parallel_tasks_upbound):
    best_loss = float('inf')
    best_qpu = None
    for t in range(len(qpu.time_width) + 1):
        qpu_ = copy.deepcopy(qpu)
        qpu_.add_task(qtc.name, t, qtc.dag_width_list)
        if max(qpu_.time_width) > max_width or any([len(tasks)>parallel_tasks_upbound for tasks in qpu_.time_task]):
            continue
        else:
            curr_loss = len(qpu_.time_width)
        if curr_loss <= best_loss:
            best_loss = curr_loss
            best_qpu = copy.deepcopy(qpu_)
    return best_qpu, best_loss

def compilation_tasks(qasm_name_list, qasm_files_dir, qpu_name, qpu_num):
    name_combine = '__'.join([os.path.splitext(f)[0] for f in qasm_name_list])
    inter_dir = f'{os.path.basename(qasm_files_dir)}_qpunum{qpu_num}/{qpu_name}/{name_combine}'
    space_cirs = []
    
    for qasm_name in qasm_name_list:
        cir_abspath = settings.find_abspath(qasm_name, dirs=qasm_files_dir)
        cir_two_qubit_gate_list = get_two_qubit_gate_list(cir_abspath)
        
        input_info = settings.input_dict(gridx=settings.gridx_list[0],
                                         aodx_per_site=settings.aodx_per_site,
                                         input_cir_name=qasm_name.removesuffix(".qasm"),
                                         input_cir_edges=cir_two_qubit_gate_list,
                                         space_cirs=space_cirs,
                                         commutable=settings.commutable,
                                         subdir=inter_dir)

        os.makedirs(input_info.save_dir, exist_ok=True)
        run_function(input_info)
        
        last_qasm_name = copy.deepcopy(qasm_name)
        last_json = f'{input_info.save_dir}/{last_qasm_name.removesuffix(".qasm")}.json'
        if not os.path.exists(last_json):
            raise ValueError(f'{last_json} does not exist')
            

        reinsert_single_qubit_gates(cir_abspath, last_json) 
        
        space_cirs.append(last_json)
        
    cal_total_time_depth_fidelity(abs_path = inter_dir)
