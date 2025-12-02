import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

def run_pipeline_test():
    print("1. Initializing STOL Pipeline")
    
    # Define the Airfoil (NACA 4412 is a classic high-lift STOL foil)
    # We use n_points_per_side=200 to ensure XFOIL has enough resolution
    airfoil = asb.Airfoil("naca4412").repanel(n_points_per_side=200)
    
    print("2. Sending Geometry to XFOIL")
    
    # This is the "Wrapper" part. 
    # We tell Python to start XFOIL, feed it the airfoil, and get the data.
    # Note: 'xfoil_command="xfoil"' assumes you added it to your PATH.
    try:
        xf_analysis = asb.XFoil(
            airfoil=airfoil,
            Re=1e6,              # Reynolds Number (Landing speed)
            mach=0.1,            # Low speed
            timeout=30           # Kill it if it hangs (common XFOIL issue)
        )
        
        # Run a sweep from -5 to 15 degrees
        print("Running Alpha Sweep (-5 to 15 deg)...")
        results = xf_analysis.alpha(np.linspace(-5, 15, 21))
        
        print("3. Success! Data Retrieved")
        print(f"    Max Lift (Cl_max): {np.max(results['CL']):.3f}")
        
        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(results["alpha"], results["CL"], "-o", color="blue")
        plt.title("NACA 4412 Lift Curve (Generated via Python Automation)")
        plt.xlabel("Angle of Attack (deg)")
        plt.ylabel("Lift Coefficient ($C_l$)")
        plt.grid(True)
        plt.show()
        
    except Exception as e:
        print("\n[ERROR] Python could not find XFOIL.")
        print("Did you add the XFOIL folder to your System PATH?")
        print(f"Error details: {e}")

if __name__ == "__main__":
    run_pipeline_test()