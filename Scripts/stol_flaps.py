import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

def rotate_airfoil(x, y, angle_deg, hinge_x=0.7):
    """
    Manually rotates the trailing edge of an airfoil to simulate a flap.
    hinge_x: The chord percentage where the flap starts (0.7 = 70% chord).
    """
    angle_rad = np.radians(angle_deg)
    
    # Identify points behind the hinge line
    is_flap = x >= hinge_x
    
    # Mathematical rotation matrix for the flap points
    # We rotate them downwards (positive angle = flap down)
    x_new = np.where(is_flap, 
                     hinge_x + (x - hinge_x) * np.cos(angle_rad) + y * np.sin(angle_rad), 
                     x)
    y_new = np.where(is_flap, 
                     - (x - hinge_x) * np.sin(angle_rad) + y * np.cos(angle_rad), 
                     y)
    
    return x_new, y_new

def run_flap_sweep():
    print("--- Starting High-Lift Flap Simulation ---")
    
    # 1. Setup
    base_airfoil = asb.Airfoil("naca4412")
    reynolds_number = 1e6
    flap_angles = [0, 10, 20, 30] # We will test these 4 settings
    colors = ['blue', 'green', 'orange', 'red']
    
    plt.figure(figsize=(12, 8))
    
    # 2. The Loop (Iterate through each flap setting)
    for i, angle in enumerate(flap_angles):
        print(f"--> Testing Flap Deflection: {angle} degrees...")
        
        # A. Create the Flapped Geometry
        # We get the coordinates, rotate the tail, and make a new Airfoil object
        x, y = base_airfoil.coordinates.T
        x_flap, y_flap = rotate_airfoil(x, y, angle_deg=angle, hinge_x=0.7)
        
        # Repanel is CRITICAL: It smooths out the sharp hinge corner so XFOIL doesn't crash
        flapped_airfoil = asb.Airfoil(
            name=f"NACA4412_Flap_{angle}",
            coordinates=np.column_stack((x_flap, y_flap))
        ).repanel(n_points_per_side=200)
        
        # B. Run XFOIL
        try:
            xf = asb.XFoil(
                airfoil=flapped_airfoil,
                Re=reynolds_number,
                timeout=60 # Give it more time for complex shapes
            )
            # We scan Alpha from -5 to 15 degrees
            result = xf.alpha(np.linspace(-5, 15, 21))
            
            # C. Plot the result immediately
            plt.plot(result["alpha"], result["CL"], 
                     "-o", color=colors[i], label=f'Flap {angle}°')
            
            # Print the max lift found for this setting
            max_lift = np.max(result["CL"])
            print(f"    Max Lift (CL_max): {max_lift:.2f}")
            
        except Exception as e:
            print(f"    [Warning] XFOIL struggled with {angle} deg flap. (This is normal for high angles)")

    # 3. Finalize Plot
    plt.title("STOL Performance: Lift Increase due to Flaps", fontsize=14)
    plt.xlabel("Angle of Attack (deg)", fontsize=12)
    plt.ylabel("Lift Coefficient ($C_L$)", fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=12)
    plt.axhline(y=2.0, color='k', linestyle='--', alpha=0.5, label='STOL Target (CL=2.0)')
    plt.show()

if __name__ == "__main__":
    run_flap_sweep()