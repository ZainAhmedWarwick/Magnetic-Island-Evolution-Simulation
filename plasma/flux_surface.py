#This file will define the fundamental geometry + instability info

#Function included within this class;

#1.FluxSurface: Represents a magnetic surface in the plasma

#2.Magnetic Island: represents a magnetic island (instability) living on the surface


class MagneticIsland: #Magnetic island class sole purpose is to define a magnetic island (1 use)

    #To define a  magneitc island you must intialise it with width, mode numbers and a bootstrap current. Additionally island can evolve with time using the MRE.

    def __init__(self, w0, m, n, bootstrap_drive):

        self.w = w0  #Represents starting island width
        self.m = m   #Mode numbers related to torodial and poloidal harmonics
        self.n = n
        self.bootstrap_drive = bootstrap_drive  #self generated current within the plasma due to pressure gradients

    def evolve(self, dt, flux_surface, mre_solver):
        dw_dt = mre_solver(self, flux_surface) #mre_solver esentially solves the MRE to solve for the change in width of island over time
        self.w += dw_dt * dt #Total width with all contributions added up 


#Components of a Flux surface made out of a radius, safety factor and a magnetic island

class FluxSurface: 
    #Just intialising a Flux surface, descrbing a magnetic flux surface
    def __init__(self, radius, q, magnetic_island=None):
        self.radius = radius
        self.q = q
        self.magnetic_island = magnetic_island

    #returns true if the flux surface contains an island disrupting confinement
    def has_island(self):
        return self.magnetic_island is not None

    #Returns a readable string is island is present
    def __repr__(self):
         return f"FluxSurface(r={self.radius}, q={self.q}, island={'yes' if self.magnetic_island else 'no'})"


       
                 




