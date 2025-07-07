#Main purpose of this file is to orgnise the flux surfaces from flux_surfaces.py into a whole PlasmaState object ready for time evolution.
#We are essentially forming the system to evolve over time.

#1.Within the TokaMak, the magnetic field lines wind around the plasma.
#2.These magnetic field lines which are winding = magnetic flux surfaces.
#3.Surface is defined by a minor radius + safety factor (q)

#1.Any small perturbation like a change in current, tear these surfaces (NTM) and stay trapped
#2.Instead of closed magnetic loops we get magnetic islands which disrupt confinement

from plasma.flux_surface import FluxSurface


#Plasma state is just a bunch of flux_surfaces
class PlasmaState:
    def __init__(self, flux_surfaces):
        self.flux_surfaces = flux_surfaces

    
    #evolves all magnetic islands across the surfaces using th eprocided mre_solver and timestep dt
    def evolve_islands(self, dt, mre_solver):
        for fs in self.flux_surfaces:
            if fs.has_island():
                fs.magnetic_island.evolve(dt, fs, mre_solver)
    
    #Returns a list of  radius and island_width tuples for all surfaces that have a magnetic island
    def get_island_data(self):
        return [(fs.radius, fs.magnetic_island.w) for fs in self.flux_surfaces if fs.has_island()]


    def __repr__(self):
        return f"PlasmaState with {len(self.flux_surfaces)} surfaces"