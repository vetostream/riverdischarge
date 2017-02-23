#######################################
#Module:    River Discharge AI        #
#Author:    Genesis Dwight Bentulan   #
#Date:      January 27, 2017          #
#######################################

from rdmsystem.powerregression import PowerRegression

class RiverDischargeAI:

    def __init__(self, data_set=[], new_data=[]):
        print "River Discharge AI Initiated."
        print "Data set: {0}".format(data_set)
        self.data_set = data_set
        self.new_data = new_data
        
        if not self.data_set:
            try:
                raise ValueError
            except ValueError:
                print "data_set should not be empty"                

    def get_predicted_value_discharge(self):
        # Q = ax^b

        #Get constants
        self.pr = PowerRegression(self.data_set[0],self.data_set[1])
        self.a = self.pr.cons_asubzero_final
        self.b = self.pr.cons_asubone_final
        self.corrcoe = self.pr.r

        return [round(self.a*(x**self.b),2) for x in self.new_data]