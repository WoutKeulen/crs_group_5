# skills code OR-part
import numpy as np

# INPUT PARAMETERS #############################################################################
# Patient type 1
# input for lambda, l_t1, is per day, therefore uses working hours
l_t1 = 17
working_hours = 9
mu_t1 = 0.4
sigma_t1 = 0.1
# Patient type 2
k_t2 = 14
theta_t2 = 0.048
mu_t2 = 0
sigma_t2 = 0.25

# Scheduled appointment time for each patient type
appointment_duration_t1 = 0.4
appointment_duration_t2 = 0.8

# Thresholds for performance measures (performance measures 6.1 & 6.2)
threshold_1 = 0.01
threshold_2 = 0.1

# Number of days for one simulation
number_of_days = 23
# Number of simulations
number_simulations = 10
#################################################################################################

# CODE START ####################################################################################
# function that returns 7 list of lists in the following order:
# 1) list containing lists of simulated call times for type 1 patients for a given number of days
# 2) list containing lists of simulated scan times for type 1 patients for a given number of days
# 3) list containing lists of simulated call times for type 2 patients for a given number of days
# 4) list containing lists of simulated scan times for type 2 patients for a given number of days
# 5) list containing sorted lists of simulated call times for patients of type 1 and 2 combined
# 6) list containing list of simulated scan durations for patients of type 1 and type 2 combined
# 7) list containing lists which keep track of patient type for each day
def patient_simulation(number_of_days):
    # add list here where you keep track of non-combined and append them
    master_call_type1 = []
    master_scan_type1 = []
    master_call_type2 = []
    master_scan_type2 = []
    master_call_combined = []
    master_scan_combined = []
    master_index_combined = []
    for i in range(number_of_days):
        call_t1 = arrival_simulation_t1(l_t1, working_hours)
        call_t2 = arrival_simulation_t2(mu_t2, sigma_t2)
        scan_t1 = scan_times_type1(call_t1, mu_t1, sigma_t1)
        scan_t2 = scan_times_type2(call_t2, k_t2, theta_t2)
        # add these to the global lists where types are seperated:
        master_call_type1.append(call_t1)
        master_call_type2.append(call_t2)
        master_scan_type1.append(scan_t1)
        master_scan_type2.append(scan_t2)
        # Construct lists for the case of patients not seperated on type
        call_today, scan_today, index_today = comb_sim_cal(call_t1, call_t2, scan_t1, scan_t2)
        master_call_combined.append(call_today)
        master_scan_combined.append(scan_today)
        master_index_combined.append(index_today)
    return (master_call_type1, master_scan_type1, master_call_type2, master_scan_type2, master_call_combined,
            master_scan_combined, master_index_combined)

#######################
# simulation functions#
#######################
# function that returns simulated calling times for 1 day for type 1 patients
def arrival_simulation_t1(l, working_hours):
    l_hour = l / working_hours
    l_hour_inverse = 1.0 / l_hour
    arrival_time = [8.00]
    counter = 1
    while arrival_time[-1] <= 17.00:
        arrival_time.append(arrival_time[counter - 1] + np.random.exponential(l_hour_inverse))
        counter += 1
    arrival_time.remove(arrival_time[0])
    arrival_time.remove(arrival_time[-1])
    return arrival_time
# function that returns simulated calling times for 1 day for type 2 patients
def arrival_simulation_t2(mu_t2, sigma_t2):
    arrival_time = [8.00]
    counter = 1
    while arrival_time[-1] <= 17.00:
        # standard normal here?
        arrival_time.append(arrival_time[counter - 1] + np.random.lognormal(mu_t2, sigma_t2))
        counter += 1
    arrival_time.remove(arrival_time[0])
    arrival_time.remove(arrival_time[-1])
    return arrival_time
# function that returns simulated scan durations for type 1 patients
def scan_times_type1(day, mu1, sigma1):
    scan_time_list_prime = []
    for x in range(len(day)):
        scan_time_list_prime.append(np.random.normal(mu1, sigma1))
    return scan_time_list_prime
# function that returns simulated scan durations for type 2 patients
def scan_times_type2(day, shape_k, scale_theta):
    scan_time_list_prime = []
    for x in range(len(day)):
        scan_time_list_prime.append(np.random.gamma(shape_k, scale_theta))
    return scan_time_list_prime
# function that takes simulated values for 1 day for calling times and scan durations for patient types 1 & 2
# and returns a sorted list of calling times, scan durations and a list of type-indexes of the combined lists
def comb_sim_cal(sim_call_t1, sim_call_t2, sim_app_t1, sim_app_t2):
    # list typecast added for now, probably not needed
    call_times1 = list(np.copy(sim_call_t1))
    call_times2 = list(np.copy(sim_call_t2))
    app_duration1 = list(np.copy(sim_app_t1))
    app_duration2 = list(np.copy(sim_app_t2))
    comb_call_time = []
    comb_call_index = []
    comb_app_dur = []
    while len(call_times1) > 0 and len(call_times2) > 0:
        if call_times1[0] < call_times2[0]:
            comb_call_time.append(call_times1[0])
            comb_call_index.append(1)
            comb_app_dur.append(app_duration1[0])
            del call_times1[0]
            del app_duration1[0]
        elif call_times1[0] > call_times2[0]:
            comb_call_time.append(call_times2[0])
            comb_call_index.append(2)
            comb_app_dur.append(app_duration2[0])
            del call_times2[0]
            del app_duration2[0]
    # after this while statement, either type 1 or type 2 is empty
    # so to complete add remainder of nonempty list to combined list
    if len(call_times1) > 0:
        for x in range(len(call_times1)):
            comb_call_time.append(call_times1[x])
            comb_call_index.append(1)
            comb_app_dur.append(app_duration1[x])
    elif len(call_times2) > 0:
        for y in range(len(call_times2)):
            comb_call_time.append(call_times2[y])
            comb_call_index.append(2)
            comb_app_dur.append(app_duration2[y])
    return comb_call_time, comb_app_dur, comb_call_index
# function that returns (theoretical) schedule under the old system for one day
def app_schedule(patient_scan_times, app_res_time):
    app_schedule = [8.0]
    for y in range(1, len(patient_scan_times)):
        app_schedule.append(round(app_schedule[y - 1] + app_res_time, 2))
    return app_schedule
# function that returns (theoretical) schedule under the old system for multiple days
def app_schedule_global(global_scan_typex, number_of_days, app_res_time):
    global_schedule = []
    for x in range(number_of_days):
        one_day_schedule = app_schedule(global_scan_typex[x], app_res_time)
        global_schedule.append(one_day_schedule)
    return global_schedule
# function that returns realized schedule for 1 day, works for both old and new system
def app_schedule_real(app_schedule, patient_scan_times):
    actual_start_time = [8.0]
    for i in range(0, len(app_schedule) - 1):
        if actual_start_time[i] + patient_scan_times[i] <= app_schedule[i + 1]:
            actual_start_time.append(app_schedule[i + 1])
        elif actual_start_time[i] + patient_scan_times[i] > app_schedule[i + 1]:
            actual_start_time.append(actual_start_time[i] + patient_scan_times[i])
    return actual_start_time
# function that returns realized schedule for multiple days, works for both old and new system
def app_schedule_real_global(old_system_typex, global_scan_typex, number_of_days):
    global_schedule_real = []
    for x in range(number_of_days):
        one_day_real = app_schedule_real(old_system_typex[x], global_scan_typex[x])
        global_schedule_real.append(one_day_real)
    return global_schedule_real
# function that returns schedule for 1 day, for both machines, under the new system
# also returns additional lists needed for performance measures
def schedule_new(combined_scan_times, combined_index, app_res_type1, app_res_type2):
    # machine 1 and 2:
    app_schedule_m1 = [8.0]
    app_schedule_m2 = [8.0]
    # lists to keep track of scan types on each machine:
    scan_time_m1 = []
    scan_time_m2 = []
    # lists to keep track of patient types on each machine
    type_index_m1 = []
    type_index_m2 = []
    # first patient to machine 1
    if combined_index[0] == 1:
        app_schedule_m1.append(round(app_schedule_m1[0] + app_res_type1, 2))
        scan_time_m1.append(combined_scan_times[0])
        type_index_m1.append(1)
    elif combined_index[0] == 2:
        app_schedule_m1.append(round(app_schedule_m1[0] + app_res_type2, 2))
        scan_time_m1.append(combined_scan_times[0])
        type_index_m1.append(2)
    # first patient to machine 2
    if combined_index[1] == 1:
        app_schedule_m2.append(round(app_schedule_m2[0] + app_res_type1, 2))
        scan_time_m2.append(combined_scan_times[1])
        type_index_m2.append(1)
    elif combined_index[1] == 2:
        app_schedule_m2.append(round(app_schedule_m2[0] + app_res_type2, 2))
        scan_time_m2.append(combined_scan_times[1])
        type_index_m2.append(2)

    # maybe change around if statements here
    # now assigning rest of patients
    for x in range(2, len(combined_scan_times)):
        if app_schedule_m1[-1] <= app_schedule_m2[-1]:
            if combined_index[x] == 1:
                app_schedule_m1.append(round(app_schedule_m1[-1] + app_res_type1, 2))
                scan_time_m1.append(combined_scan_times[x])
                type_index_m1.append(1)
            elif combined_index[x] == 2:
                app_schedule_m1.append(round(app_schedule_m1[-1] + app_res_type2, 2))
                scan_time_m1.append(combined_scan_times[x])
                type_index_m1.append(2)
        elif app_schedule_m1[-1] > app_schedule_m2[-1]:
            if combined_index[x] == 1:
                app_schedule_m2.append(round(app_schedule_m2[-1] + app_res_type1, 2))
                scan_time_m2.append(combined_scan_times[x])
                type_index_m2.append(1)
            elif combined_index[x] == 2:
                app_schedule_m2.append(round(app_schedule_m2[-1] + app_res_type2, 2))
                scan_time_m2.append(combined_scan_times[x])
                type_index_m2.append(2)
    # check if last patient is schedules now?
    # probably not, add extra code for this, for now solved by keeping track of indexes etc.
    # here, indexes are one removed, one machine is equal length, other one shorter
    last_caller_type = combined_index[-1]
    last_caller_length = combined_scan_times[-1]
    if app_schedule_m1[-1] <= app_schedule_m2[-1]:
        scan_time_m1.append(last_caller_length)
        type_index_m1.append(last_caller_type)
    elif app_schedule_m1[-1] > app_schedule_m2[-1]:
        scan_time_m2.append(last_caller_length)
        type_index_m2.append(last_caller_type)

    return app_schedule_m1, scan_time_m1, type_index_m1, app_schedule_m2, scan_time_m2, type_index_m2
# function that returns schedule for multiple days, for both machines, under the new system
# also returns additional lists needed for performance measures
def new_schedule_global(combined_scan_times, combined_index, app_res_type1, app_res_type2, number_of_days):
    glob_sched_m1 = []
    glob_scan_m1 = []
    glob_index_m1 = []
    glob_sched_m2 = []
    glob_scan_m2 = []
    glob_index_m2 = []
    for x in range(number_of_days):
        (day_sched_m1, day_scan_m1, day_index_m1,
         day_sched_m2, day_scan_m2, day_index_m2)\
            = schedule_new(combined_scan_times[x], combined_index[x], app_res_type1, app_res_type2)
        glob_sched_m1.append(day_sched_m1)
        glob_scan_m1.append(day_scan_m1)
        glob_index_m1.append(day_index_m1)
        glob_sched_m2.append(day_sched_m2)
        glob_scan_m2.append(day_scan_m2)
        glob_index_m2.append(day_index_m2)
    return glob_sched_m1, glob_scan_m1, glob_index_m1, glob_sched_m2, glob_scan_m2, glob_index_m2

########################
# PERFORMANCE MEASURES #
########################
# 1) total waiting time
def total_wait_time_global(schedules_m1, real_schedules_m1, schedules_m2, real_schedules_m2):
    global_wait_time = 0.0
    # for machine 1
    for x in range(0, len(schedules_m1)):
        for y in range(0, len(schedules_m1[x])):
            if real_schedules_m1[x][y] - schedules_m1[x][y] > 0:
                global_wait_time += real_schedules_m1[x][y] - schedules_m1[x][y]
    # for machine 2
    for x in range(0, len(schedules_m2)):
        for y in range(0, len(schedules_m2[x])):
            if real_schedules_m2[x][y] - schedules_m2[x][y] > 0:
                global_wait_time += real_schedules_m2[x][y] - schedules_m2[x][y]

    return global_wait_time
# 2) maximum waiting time per machine, works both under old & new system #
def max_wait_time_global(schedules_m1, real_schedules_m1, schedules_m2, real_schedules_m2):
    max_wait_global = 0.0
    for x in range(len(schedules_m1)):
        for y in range(len(schedules_m1[x])):
            temp_wait_time = real_schedules_m1[x][y] - schedules_m1[x][y]
            if temp_wait_time >= max_wait_global:
                max_wait_global = temp_wait_time
    for x in range(len(schedules_m2)):
        for y in range(len(schedules_m2[x])):
            temp_wait_time = real_schedules_m2[x][y] - schedules_m2[x][y]
            if temp_wait_time >= max_wait_global:
                max_wait_global = temp_wait_time
    return max_wait_global
# 3) average waiting time per machine, all days, works both under old & new system #
def avg_wait_time_global(schedules_m1, real_schedules_m1, schedules_m2, real_schedules_m2):
    time_waited = 0.0
    num_patients = 0.0
    for x in range(len(schedules_m1)):
        num_patients += len(schedules_m1[x])
    for x in range(len(schedules_m2)):
        num_patients += len(schedules_m2[x])
    for y in range(len(schedules_m1)):
        for z in range(len(schedules_m1[y])):
            if real_schedules_m1[y][z] - schedules_m1[y][z] > 0:
                time_waited += real_schedules_m1[y][z] - schedules_m1[y][z]
    for y in range(len(schedules_m2)):
        for z in range(len(schedules_m2[y])):
            if real_schedules_m2[y][z] - schedules_m2[y][z] > 0:
                time_waited += real_schedules_m2[y][z] - schedules_m2[y][z]
    return time_waited / num_patients
# 4) total idle time
# think about if finished before 1700 counts as idle time? Currently not implemented
def total_idle_time(schedules_m1, real_schedules_m1, schedules_m2, real_schedules_m2, scan_m1, scan_m2):
    idle_time_global = 0.0
    for x in range(0, len(schedules_m1)):
        for y in range(1, len(schedules_m1[x])):
            if schedules_m1[x][y] >= real_schedules_m1[x][y - 1]:
                idle_time_global += schedules_m1[x][y] - real_schedules_m1[x][y - 1]
        # check if machine 1 is idle after last appointment, i.e. between end last appointment and 17:00
        if real_schedules_m1[x][-1] + scan_m1[x][-1] < 17.0:
            idle_time_global += 17.0 - real_schedules_m1[x][-1] + scan_m1[x][-1]
    for x in range(0, len(schedules_m2)):
        for y in range(1, len(schedules_m2[x])):
            if schedules_m2[x][y] >= real_schedules_m2[x][y - 1]:
                idle_time_global += schedules_m2[x][y] - real_schedules_m2[x][y - 1]
        # check if machine 2 is idle after last appointment, i.e. between end last appointment and 17:00
        if real_schedules_m2[x][-1] + scan_m2[x][-1] < 17.0:
            idle_time_global += 17.0 - real_schedules_m2[x][-1] + scan_m2[x][-1]
    return idle_time_global
# 5) total over time
# comment
def total_overtime(schedules_m1, real_schedules_m1, schedules_m2, real_schedules_m2, scan_m1, scan_m2):
    overtime_global = 0.0
    # for machine 1
    for x in range(0, len(schedules_m1)):
        if real_schedules_m1[x][-1] + scan_m1[x][-1] > 17.0:
            overtime_global += real_schedules_m1[x][-1] + scan_m1[x][-1] - 17.0
    # for machine 2
    for x in range(0, len(schedules_m2)):
        if real_schedules_m2[x][-1] + scan_m2[x][-1] > 17.0:
            overtime_global += real_schedules_m2[x][-1] + scan_m2[x][-1] - 17.0
    return overtime_global
# 6) thresholds
def wait_threshold(schedules_m1, real_schedules_m1, schedules_m2, real_schedules_m2, threshold):
    global_threshold = 0
    num_patients = 0
    # machine 1
    for x in range(0, len(schedules_m1)):
        for y in range(0, len(schedules_m1[x])):
            num_patients += len(schedules_m1[x])
            if real_schedules_m1[x][y] - schedules_m1[x][y] > threshold:
                global_threshold += 1
    # machine 2
    for x in range(0, len(schedules_m2)):
        for y in range(0, len(schedules_m2[x])):
            num_patients += len(schedules_m2[x])
            if real_schedules_m2[x][y] - schedules_m2[x][y] > threshold:
                global_threshold += 1
    return (global_threshold / num_patients) * 100

##############################################################################
# DRIVER CODE FOR number_simulations SIMULATIONS, EACH OF SIZE number_of_days#
##############################################################################
total_waiting_old_glob = [] # 1
total_waiting_new_glob = [] # 1
max_waiting_old_glob = []   # 2
max_waiting_new_glob = []   # 2
avg_waiting_old_glob = []   # 3
avg_waiting_new_glob = []   # 3
idle_time_old_glob = []     # 4
idle_time_new_glob = []     # 4
overtime_old = []           # 5
overtime_new = []           # 5
threshold_old_1_glob = []   # 6.1
threshold_new_1_glob = []   # 6.1
threshold_old_2_glob = []   # 6.2
threshold_new_2_glob = []   # 6.2

for i in range(0, number_simulations):
    # simulated calling times, scan durations, combined lists
    (global_call_type1, global_scan_type1,
     global_call_typ2, global_scan_type2,
     master_call_global, master_scan_global,
     master_index_global) = patient_simulation(number_of_days)
    # schedules and realized schedules under OLD SYSTEM:
    old_system_type1 = app_schedule_global(global_scan_type1, number_of_days, appointment_duration_t1)
    old_system_type2 = app_schedule_global(global_scan_type2, number_of_days, appointment_duration_t2)
    old_sys_real_type1 = app_schedule_real_global(old_system_type1, global_scan_type1, number_of_days)
    old_sys_real_type2 = app_schedule_real_global(old_system_type2, global_scan_type2, number_of_days)
    # schedules and realized schedules under NEW SYSTEM:
    # add additional comment here
    (new_system_m1, new_sys_scan_m1, new_sys_index_m1,
     new_system_m2, new_sys_scan_m2, new_sys_index_m2) \
        = new_schedule_global(master_scan_global, master_index_global, appointment_duration_t1, appointment_duration_t2,
                              number_of_days)
    new_system_real_m1 = app_schedule_real_global(new_system_m1, new_sys_scan_m1, number_of_days)
    new_system_real_m2 = app_schedule_real_global(new_system_m2, new_sys_scan_m2, number_of_days)
    # Performance measure driver code #
    # 1
    total_waiting_old_glob.append(total_wait_time_global(old_system_type1, old_sys_real_type1, old_system_type2,
                                               old_sys_real_type2))
    total_waiting_new_glob.append(total_wait_time_global(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2))
    # 2
    max_waiting_old_glob.append(max_wait_time_global(old_system_type1, old_sys_real_type1, old_system_type2, old_sys_real_type2))
    max_waiting_new_glob.append(max_wait_time_global(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2))
    # 3
    avg_waiting_old_glob.append(avg_wait_time_global(old_system_type1, old_sys_real_type1, old_system_type2, old_sys_real_type2))
    avg_waiting_new_glob.append(avg_wait_time_global(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2))
    # 4
    idle_time_old_glob.append(total_idle_time(old_system_type1, old_sys_real_type1, old_system_type2, old_sys_real_type2,
                                global_scan_type1, global_scan_type2))
    idle_time_new_glob.append(total_idle_time(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2,
                                new_sys_scan_m1, new_sys_scan_m2))
    # 5
    overtime_old.append(total_overtime(old_system_type1, old_sys_real_type1, old_system_type2, old_sys_real_type2,
                                global_scan_type1, global_scan_type2))
    overtime_new.append(total_overtime(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2,
                                new_sys_scan_m1, new_sys_scan_m2))
    # 6.1
    threshold_old_1_glob.append(wait_threshold(old_system_type1, old_sys_real_type1, old_system_type2, old_sys_real_type2, threshold_1))
    threshold_new_1_glob.append(wait_threshold(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2, threshold_1))
    # 6.2
    threshold_old_2_glob.append(wait_threshold(old_system_type1, old_sys_real_type1, old_system_type2, old_sys_real_type2, threshold_2))
    threshold_new_2_glob.append(wait_threshold(new_system_m1, new_system_real_m1, new_system_m2, new_system_real_m2, threshold_2))

# PRINTING RESULTS FOR SIMULATIONS IN LISTS #
# 1
print("total waiting old:", total_waiting_old_glob)
print("total waiting new:", total_waiting_new_glob)
# 2
print("max waiting old:", max_waiting_old_glob)
print("max waiting new:", max_waiting_new_glob)
# 3
print("average waiting old:", avg_waiting_old_glob)
print("average waiting new:", avg_waiting_new_glob)
# 4
print("idle time old:", idle_time_old_glob)
print("idle time new:", idle_time_new_glob)
# 5
print("overtime old:", overtime_old)
print("overtime new:", overtime_new)
# 6.1
print("threshold 1 old:", threshold_1, threshold_old_1_glob)
print("threshold 1 new:", threshold_1, threshold_new_1_glob)
# 6.2
print("threshold 2 old:", threshold_2, threshold_old_2_glob)
print("threshold 2 new:", threshold_2, threshold_new_2_glob)
