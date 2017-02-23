#######################################
#Module:    Power Regression Model    #
#Author:    Genesis Dwight Bentulan   #
#Date:      January 18, 2017          #
#######################################


#y = ax^b; where a and b are constants
#ln y = ln a + b ln x
#Z = ln y, Azero = ln a, b = Aone, W = ln x
#Z = Azero + Aone * W
#n = number of data samples

from math import pow, log, e, sqrt

class PowerRegression:
    def __init__(self, variable_one, variable_two):
        self.variable_one = variable_one #data-list one; y;
        self.variable_two = variable_two #data-list two; x;
        self.Aone = "Not calculated!"
        self.Azero = "Not calculated!"
        
        #calculate number n
        self.n = len(self.variable_one)

        #perform op
        self.calc_asubone()
        self.calc_asubzero()

        self.cons_asubone_final = self.Aone             #b constant
        self.cons_asubzero_final = pow(e, self.Azero)   #a constant
        self.calc_correlation_val()

        self.try_y(20)

        print "Created a Power Regression Model given; y = ax^b where \n a = {0} \n b = {1} \n r = {2} \n r^2 = {3}".format(self.cons_asubzero_final,self.cons_asubone_final,self.r,pow(self.r,2))

    def calc_alpha(self):
        # let alpha = n * summation of (WiZi) - summation of Wi * summation of Zi
        # x = n * summation of (WiZi)
        # y = summation of Wi * summation of Zi

        #solve for x

        first_set = self.variable_one
        second_set = self.variable_two
        
        wi_set = [log(x) for x in second_set]
        zi_set = [log(y) for y in first_set]

        self.summation_wi = sum(wi_set)
        self.summation_zi = sum(zi_set)
        
        wi_zi = [x*y for x,y in zip(zi_set,wi_set)]
        summation_wi_zi = sum(wi_zi)


        x = self.n * summation_wi_zi
        y = self.summation_wi * self.summation_zi

        alpha = x - y

        return alpha

    def calc_beta(self):
        # let beta  = n * summation of (Wi)^2 - (summation of Wi)^2
        # x = n * summation of (Wi)^2
        # y = (summation of Wi)^2

        second_set = self.variable_two
        wi_set = [log(x) for x in second_set]

        y = pow(sum(wi_set), 2)
        x = self.n * sum([x**2 for x in wi_set])

        beta = x - y

        return beta

    def calc_asubone(self):
        # Aone = alpha/beta
        self.alpha = self.calc_alpha()
        self.beta = self.calc_beta()

        self.Aone = self.alpha/self.beta

    def calc_asubzero(self):
        # Azero = summation of z - Aone * summation of w
        self.Azero = (self.summation_zi)/self.n - self.Aone * (self.summation_wi)/self.n

    def calc_correlation_val(self):
        # Calculate Sy and Sx;
        Sy = self.calc_standard_deviation(self.variable_one, self.summation_zi)
        Sx = self.calc_standard_deviation(self.variable_two, self.summation_wi)

        #calculate Zy and Zx;
        Zy = self.calc_standardized_value(Sy, self.summation_zi, self.variable_one)
        Zx = self.calc_standardized_value(Sx, self.summation_wi, self.variable_two)

        #calculate corcoef
        self.r = sum([x*y for x,y in zip(Zy,Zx)])/(self.n-1)
        
        
    def calc_standard_deviation(self, data_points, summation_v):
        #calculate standard deviation for Sx; data_sets = Xi-X_MEAN
        v_mean = summation_v/self.n
        set_copy = data_points

        dfrn = [v-v_mean for v in set_copy]
        Sv = sqrt(sum([v**2 for v in dfrn])/(self.n-1))

        return Sv

    def calc_standardized_value(self, Sv, summation_v, data_points):
        v_mean = summation_v/self.n
        set_copy = data_points

        dfrn = [v-v_mean for v in set_copy]
        Zv = [x/Sv for x in dfrn]

        return Zv

    def try_y(self, in_val):
        y = self.cons_asubzero_final * pow(in_val,self.cons_asubone_final)
        print y