# High-Lift STOL Aerodynamics Pipeline ✈️

![Python](https://img.shields.io/badge/Code-Python_3.11-blue?logo=python&logoColor=white)
![CFD](https://img.shields.io/badge/Validation-Ansys_Fluent-orange?logo=ansys&logoColor=white)
![CAD](https://img.shields.io/badge/Design-OpenVSP-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

## 📖 Project Overview
This project establishes a **multi-fidelity aerodynamic analysis pipeline** designed to optimize a high-lift wing for regional Short Take-Off and Landing (STOL) aircraft. 

Moving beyond manual iteration, this workflow integrates **Python-based automation** for rapid design space exploration with **Industrial CFD** for physics validation. The goal was to design a clean-sheet wing capable of high-efficiency cruise ($L/D > 15$) while maintaining the high $C_{L_{max}}$ required for short-field operations.

---

## 🛠️ The Engineering Pipeline
The project follows a "Crawl, Walk, Run" engineering methodology:

### Phase 1: Automated Low-Fidelity Design (Python & XFOIL)
* **Tools:** Python, `AeroSandbox`, `NeuralFoil`
* **Method:** Developed a script to perform parametric sweeps of flap deflection angles ($0^\circ$ to $30^\circ$) and Angles of Attack.
* **Outcome:** Automated 80+ simulations in under 10 seconds, selecting the **NACA 4412** airfoil for its superior camber characteristics and identifying a 65% increase in $C_{l_{max}}$ with flaps deployed.

### Phase 2: 3D Sizing & Induced Drag (OpenVSP)
* **Tools:** OpenVSP, VSPAERO (Vortex Lattice Method)
* **Method:** Extruded the optimized section into a finite wing ($b=12m$, $c=1.5m$) to model 3D effects.
* **Outcome:** Quantified **wingtip vortex generation** and induced drag penalties, optimizing the planform to a straight-wing configuration to ensure favorable root-to-tip stall progression.

### Phase 3: High-Fidelity Validation (Ansys Fluent)
* **Tools:** Ansys Workbench, DesignModeler, Fluent
* **Method:** RANS CFD simulation using the **SST $k-\omega$ turbulence model** with a hybrid mesh (inflation layers for boundary layer resolution).
* **Outcome:** Validated the final aerodynamic forces at cruise velocity (40 m/s), confirming no premature flow separation.

---

## 📊 Key Results

The multi-fidelity analysis successfully validated the wing's performance against regional transport targets.

| Performance Metric | Value | Unit | Condition |
| :--- | :--- | :--- | :--- |
| **Lift Force** | **4,027** | N | Cruise (0° AOA) |
| **Drag Force** | **218.5** | N | Total Viscous + Pressure |
| **Lift Coefficient ($C_L$)** | **0.228** | - | 3D Finite Wing |
| **L/D Efficiency** | **18.43** | - | **Highly Efficient** |

### Visual Validation

**1. RANS CFD Velocity Field**
*Visualization of flow acceleration over the suction surface and stagnation point at the leading edge.*
[Velocity Contour](<CFD Results/Velocity Contour.png>)

**2. RANS CFD Pressure Field**
*Visualization of pressure distribution over the suction surface and stagnation point at the leading edge.*
[Pressure Contour](<CFD Results/Pressure Distribution.png>)

**3. WingTip Vortex Visualisation**
*Visualization of vortex generated at the wingtip (distribution of particles) [*]
[WingTip Vortex](<CFD Results/Vortex Visualizer.png>)

**4.1. Automated Lift Curve Sweep**
![NACA 4412 Lift Curve](<CFD Results/NACA 4412 Lift Curve.png>)

**4.2. Automated Lift Curve Sweep with flaps**
[Lift Curve of Wing with Flaps / Elevators](<CFD Results/Lift with Flaps.png>)


---

## 📂 Repository Structure

```text
├── 📂 cad and cfd files 
│   ├── STOL_Wing.stp          # Final Clean-Sheet Wing Geometry (STEP)
│   └── STOL_Wing.vsp3         # OpenVSP parametric model
├── 📂 scripts
│   ├── stol_pipeline.py       # Main automation script (AeroSandbox)
│   └── lift_curve_gen.py      # Data visualization script
├── 📂 cfd_results
│   ├── Velocity_Contour.png   # High-Res CFD visualization
│   └── Lift_Drag_Report.txt   # Raw Fluent output data
└── README.md

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.