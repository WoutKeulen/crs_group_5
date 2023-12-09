# crs_group_5
input parameters overview

l_t1: lambda for poisson arrivals per day of type 1 patiënt
working_hours: is used for calculating arrival times with lambda for the time interval 8:00-17:00

mu_t1: mean duration of normally distributed scanning time for type 1 patient
sigma_t1: standard deviation of normally distributed scanning time for type 1 patient


k_t2: parameter for gamma distributed scan duration for patient of type 2
theta_t2: parameter for gamma distributed scan duration for patient of type 2

mu_t2: mean of lognormal arrival time for  patient of type 2
sigma_t2: standard deviation of lognormal arrival time for patient of type 2

appointment_duration_t1: time reserved for appointment of patient of type 1
appointment_duration_t2: time reserved for appointment of patient of type 2


threshold_1, threshold_2: thresholds for waiting times, performance measure functions check how many patients are above the threshold


number_of_days: number of days included in one simulation
number_simulations: number of simulations 
