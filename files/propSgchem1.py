import numpy as np
import arepy as apy
import h5py as hp

class propSgchem1:

    ###############################
    # Chemical abundances
    ###############################

    def prop_ChemicalAbundances(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids)
    def prop_x_H2(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids,0)
    def prop_x_HP(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids,1)
    def prop_x_DP(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids,2)
    def prop_x_HD(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids,3)
    def prop_x_HEP(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids,4)
    def prop_x_HEPP(self,prop,ids):
        return self.getDataset('ChemicalAbundances',prop['ptype'],ids,5)
    def prop_x_H(self,prop,ids):
        return self.chem['x0_H']  - 2*self.prop_x_H2(prop,ids) - self.prop_x_HP(prop,ids) - self.prop_x_HD(prop,ids)
    def prop_x_HE(self,prop,ids):
        return self.chem['x0_He'] - self.prop_x_HEP(prop,ids)  - self.prop_x_HEPP(prop,ids)
    def prop_x_D(self,prop,ids):
        return self.chem['x0_D']  - self.prop_x_DP(prop,ids)   - self.prop_x_HD(prop,ids)

    ###############################
    # Mass fractions of species in the cell
    ###############################

    def prop_X_H2(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_H2(prop,ids) * 2
    def prop_X_HP(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_HP(prop,ids) * 1
    def prop_X_DP(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_DP(prop,ids) * 2
    def prop_X_HD(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_HD(prop,ids) * 3
    def prop_X_HEP(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_HEP(prop,ids) * 4
    def prop_X_HEPP(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_HEPP(prop,ids) * 4
    def prop_X_H(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_H(prop,ids) * 1
    def prop_X_HE(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_HE(prop,ids) * 4
    def prop_X_D(self,prop,ids):
        return self.chem['X_H'] * self.prop_x_D(prop,ids) * 2

    ###############################
    # Total mass of species in the cell (code units)
    ###############################

    def prop_M_H2(self,prop,ids):
        return self.prop_X_H2(prop,ids) *   self.prop_Masses(prop,ids)
    def prop_M_HP(self,prop,ids):
        return self.prop_X_HP(prop,ids) *   self.prop_Masses(prop,ids)
    def prop_M_DP(self,prop,ids):
        return self.prop_X_DP(prop,ids) *   self.prop_Masses(prop,ids)
    def prop_M_HD(self,prop,ids):
        return self.prop_X_HD(prop,ids) *   self.prop_Masses(prop,ids)
    def prop_M_HEP(self,prop,ids):
        return self.prop_X_HEP(prop,ids) *  self.prop_Masses(prop,ids)
    def prop_M_HEPP(self,prop,ids):
        return self.prop_X_HEPP(prop,ids) * self.prop_Masses(prop,ids)
    def prop_M_H(self,prop,ids):
        return self.prop_X_H(prop,ids) *    self.prop_Masses(prop,ids)
    def prop_M_HE(self,prop,ids):
        return self.prop_X_HE(prop,ids) *   self.prop_Masses(prop,ids)
    def prop_M_D(self,prop,ids):
        return self.prop_X_D(prop,ids) *    self.prop_Masses(prop,ids)

    ###############################
    # Photon ionization/heating rates 
    ###############################
 
    def prop_PhotonRates(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids)
    def prop_RIH(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,0)
    def prop_HRIH(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,1)
    def prop_RIH2(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,2)
    def prop_HRIH2(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,3)
    def prop_RDH2(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,4)
    def prop_HRD(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,5)
    def prop_RIHE(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,6)
    def prop_HRIHE(self,prop,ids):         
        return self.getDataset('PhotonRates',prop['ptype'],ids,7)


    ###############################
    # Photon fluxes in the cell (photons per second)
    ###############################

    def prop_PhotonFlux(self,prop,ids):         
        return self.getDataset('PhotonFlux',prop['ptype'],ids) * self.units['flux']
    def prop_F056(self,prop,ids):
        return self.getDataset('PhotonFlux',prop['ptype'],ids,0) * self.units['flux']
    def prop_F112(self,prop,ids):
        return self.getDataset('PhotonFlux',prop['ptype'],ids,1) * self.units['flux']
    def prop_F136(self,prop,ids):
        return self.getDataset('PhotonFlux',prop['ptype'],ids,2) * self.units['flux']
    def prop_F152(self,prop,ids):
        return self.getDataset('PhotonFlux',prop['ptype'],ids,3) * self.units['flux']
    def prop_F246(self,prop,ids):
        return self.getDataset('PhotonFlux',prop['ptype'],ids,4) * self.units['flux']
    def prop_FTOT(self,prop,ids):
        return np.sum(self.prop_PhotonFlux(prop,ids),axis=1)


    ###############################
    # Derived properties
    ###############################

    # Polytropic index
    def prop_Gamma(self,prop,ids):
        if self.hasDataset('Gamma',prop['ptype']):
            return self.getDataset('Gamma',prop['ptype'],ids)
        else:
            return apy.const.gamma    
    
    # Temperature of the gas (K)
    def prop_Temperature(self,prop,ids):
        # The follwoing seems to be wrong
        #inten = self.sf[pt]['InternalEnergy'][:]
        #utherm = inten[ids] * self.sf['Header'].attrs['UnitVelocity_in_cm_per_s']**2
        #return ( calcGamma() - 1. ) * utherm * (calcMu() * apy.const.m_p) / apy.const.k_B
    
        # The following calculation was taken from voronoi_makeimage.c line 2240 
        # and gives the same temperatures as are shown on the Arepo images
        dens = self.prop_Density(prop,ids)
        yn = dens * self.units['density'] / ((1.0 + 4.0 * self.chem['x0_He']) * apy.const.m_p)
        en = self.prop_InternalEnergy(prop,ids) * dens * self.units['energy'] / self.units['volume']
        yntot = (1.0 + self.chem['x0_He'] - self.prop_x_H2(prop,ids) + self.prop_x_HP(prop,ids) + \
                 self.prop_x_HEP(prop,ids) + self.prop_x_HEPP(prop,ids) ) * yn
        return (self.prop_Gamma(prop,ids) - 1.0) * en / (yntot * apy.const.k_B) 

    # Mean molecular weight
    def prop_Mu(self,prop,ids):
        mu = ( self.chem['x0_H'] + 2.*self.chem['x0_D'] + 4.*self.chem['x0_He'] ) / \
            ( self.chem['x0_H'] + self.chem['x0_D'] + self.chem['x0_He'] + \
              self.prop_x_HP(prop,ids) + self.prop_x_DP(prop,ids) + \
              self.prop_x_HEP(prop,ids) + 2*self.prop_x_HEPP(prop,ids) )
        return mu
    
    # Number density of the gas (particles per cubic centimeter)
    def prop_NumberDensity(self,prop,ids):
        density = self.prop_Density(prop,ids) * self.units['density']  # density (g/cm^3)
        return density / ( apy.const.m_p * self.prop_Mu(prop,ids) )        

    # Recombination factor of Hydrogen type B from SGChem/coolinmo.F (rec*cm^3/s)
    def prop_AlphaB(self,prop,ids):
        tinv = 1.0 / self.prop_Temperature(prop,ids)
        return 2.753e-14 * (315614 * tinv)**1.5 / ( 1. + (115188 * tinv)**0.407 )**2.242

    # Pressure (code units)
    def prop_Pressure(self,prop,ids):
        return (self.prop_Gamma(prop,ids)-1.) * self.prop_Density(prop,ids) * self.prop_InternalEnergy(prop,ids)

    # Recombination rate (rec/s)
    def prop_RecombH(self,prop,ids): 
        density = self.prop_Density(prop,ids) * self.units['density']  # density (g/cm^3)
        numdens = density / ((1. + 4. * self.chem['x0_He']) * apy.const.m_p); # nucleon number density [1/cm^3]
        return self.prop_AlphaB(prop,ids) * numdens

    # Stromgren radius if a source is in the cell (physical code units)
    def prop_StromgrenRadius(self,prop,ids):
        flux = self.prop_PhotonFlux(prop,ids)
        test = apy.phys.IonizationFrontTest(
            a=self.prop_AlphaB(prop,ids), 
            n=self.prop_NumberDensity(prop,ids),
            Q=np.sum(flux[:,2:],axis=1),
            T_avg=self.prop_Temperature(prop,ids), 
            gamma=self.prop_Gamma(prop,ids), 
            mu=self.prop_Mu(prop,ids)
        )
        return test.r_st / self.units['length'] 