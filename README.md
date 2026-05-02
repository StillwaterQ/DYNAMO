# DYNAMO: Dynamic Neutral Atom Multi-programming Optimizer Towards Quantum Operating Systems

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

## Overview

DYNAMO (Dynamic Neutral Atom Multi-programming Optimizer) is the first framework engineered to realize comprehensive multi-programming capabilities on dynamically field-programmable neutral atom quantum architectures, addressing a critical gap in quantum operating system (QOS) development.

By facilitating the concurrent execution of multiple quantum programs, DYNAMO achieves significant performance improvements, including compilation speedups up to 352.42x and superior estimated circuit fidelity compared to state-of-the-art single-circuit optimizers. It also demonstrates robust, balanced workload distribution across multi-QPU systems.

This repository contains the implementation of DYNAMO, including its two-level optimization strategy, spatial deformation modeling, and constraint-based SMT scheduling techniques.

For more details, refer to the paper:

**DYNAMO: Dynamic Neutral Atom Multi-programming Optimizer Towards Quantum Operating Systems**

## Features

* **Multi-programming Support**: The first framework to enable concurrent execution of multiple quantum circuits on neutral atom QPUs.

* **Two-Level Optimization Strategy**:

  * **Inter-QPU Scheduler**: A pre-compilation framework using hybrid optimization (SA+B&B/LPT) for global load balancing across multiple QPUs.

  * **Intra-QPU Compiler**: A core compiler enabling parallel execution *within* a single QPU.

* **Spatial Deformation Modeling**: Manages complex AOD (acousto-optic deflector) movement constraints through dynamic partitioning into Order-Preserving Zones (OPZ) and Order-Free Zones (OFZ).

* **Constraint-Based SMT Scheduling**: Utilizes SMT (Satisfiability Modulo Theories) to manage resource contention and ensure conflict-free, correct compilation of concurrent circuits.

* **Scalability**: Evaluated on circuits with depths ranging from 12 to 3847, demonstrating robust performance across diverse workloads.

## Installation

### Prerequisites

* **Python**: Version 3.9 or higher

* **Operating System**: Linux (Ubuntu)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/DYNAMO.git
   cd DYNAMO
