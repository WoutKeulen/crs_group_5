# crs_group_5
# INPUT PARAMETERS

# Patient type 1
lambda_t1 = 0.5075
mu_t1 = 0.4328
sigma_t1 = np.sqrt(0.00955)
-> lambda_t1: parameter for exponential distribution, for inter-calling times simulation
-> mu_t1: mean parameter for normal distribution, for scan duration simulation
-> sigma_t1: standard deviation parameter for normal distribution, for scan duration simulation

# Patient type 2
k_t2 = 12.587
theta_t2 = 0.05319
shape_t2 = 3
scale_t2 = 0.966
-> k_t2: shape parameter for gamma distribution, for inter-calling times simulation
-> theta_t2: scale parameter for gamma distribution, for inter-calling times simulation
-> shape_t2: shape parameter for weibull distribution, for scan duration simulation
-> scale_t2: scale parameter for weibull distribution, for scan duration simulation

# Scheduled appointment durations
appointment_duration_t1 = 0.4
appointment_duration_t2 = 0.8
-> appointment_duration_t1: length of scheduled appointment for type 1 patient
-> appointment_duration_t2: length of scheduled appointment for type 2 patient

# Thresholds for performance measures 
threshold_1 = 0.05  # corresponds to a waiting time of 3 minutes
threshold_2 = 0.1   # corresponds to a waiting time of 6 minutes
-> threshold_1, threshold_2: thresholds for waiting times in hours

# Number of days for one simulation
number_of_days = 100
-> number_of_days: number of days in one simulation

# Number of simulations
number_simulations = 1
-> number_simulations: number of total simulations, each spanning a number of days equal to number_of_days

