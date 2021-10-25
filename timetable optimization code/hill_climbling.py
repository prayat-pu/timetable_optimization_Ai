import random
import collections

def check_remain_hours(day_data):
    workload_perday = 8
    total_hours = 0
    for item_data in day_data:
        hour = item_data[2]
        total_hours += hour
    return workload_perday - total_hours

def check_free_time_of_day(day_data):
    for i,item_data in enumerate(day_data):
        if item_data[0] == -1:
            return i
    return 0

def put_task_in_timetable(task_id,task_data,time_index,day_data):
    task_name = task_data[0]
    task_piority = task_data[1]
    total_hours = task_data[2]
    task_turple = (task_id,task_name,1)
    rest_turple = (13,'rest',1)
    work_continous = 0
    for i in range(total_hours):
        if work_continous == 2 and task_piority != 2 and time_index+i+1 < len(day_data) and task_piority!=1:
            day_data[time_index+i] = rest_turple
            day_data[time_index+i+1] = task_turple
        else:
            day_data[time_index+i] = task_turple
        work_continous +=1
    return day_data

def randomSolution(timetable,task_id_dict,time_dict):
    new_timetable = {}
    num_tasks = len(task_id_dict)
    num_days =5
    round_ = 0
    for task_id, task_data in task_id_dict.items():
            task_hour = task_data[2]
            days_list = ['monday','tuesday','wednesday','thursday','friday']
            for i in range(num_days):
                # random day 
                random_day_index = random.randint(0,len(days_list)-1)

                random_day = days_list[random_day_index]

                days_list.pop(random_day_index)
                day_data = timetable[random_day]

                # check remain hours for work.
                remain_hours = check_remain_hours(day_data)

                if remain_hours != 0 and remain_hours >= task_hour :
                    #check freetime 
                    freetime_index = check_free_time_of_day(day_data)
                    #random time
                    
                    day_data = put_task_in_timetable(task_id,task_data,freetime_index,day_data)
                    new_timetable[random_day] = day_data
                    break

    return new_timetable

def calculate_energy(solution_timetable,task_id_dict,time_dict):
    #cost function -> 
    total_remain_energy_per_week = 0
    for day,day_data in solution_timetable.items():
        i = 0 
        remain_energy_per_day = 100
        while(i<len(day_data)):
            
            task_id = day_data[i][0]
            if task_id != -1 and task_id != 13:
                task_piority = task_id_dict[task_id][1]
                task_hour = task_id_dict[task_id][2]
                time_weight = time_dict[i][1]
                i+=task_hour
            else:
                task_piority = 0
                task_hour = 0
                time_weight = time_dict[i][1]
                i+=1

            use_energy_per_task =   (task_piority*task_hour)/time_weight
            remain_energy_per_day -= use_energy_per_task 

        total_remain_energy_per_week += remain_energy_per_day

    return total_remain_energy_per_week

def find_tasks_in_day(day_data):
    task_in_day = []
    task_old  = set()
    for i,item in enumerate(day_data):
        task_id = item[0]
        if i == 0:
            task_in_day.append(task_id)
        else:
            if  task_id not in task_old:
                task_in_day.append(task_id)
        task_old.add(task_id)
        task_in_day = [x  for x in task_in_day if x != -1 and x != 13] # filter -1 out of list
    return task_in_day # task in day that have old position

def data_new_day_timetable():
    return [(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0)]

def getNeighbours(solution_timetable,task_id_dict):
    neighbours = []
    
    all_change_timetable = solution_timetable.copy()
    count = 0
    
    for day,day_data in solution_timetable.items():
        task_in_day = find_tasks_in_day(day_data)
        task_in_day  = collections.deque(task_in_day)
        for i in range(1,len(task_in_day)+1):
            initial_solution_timetable = solution_timetable.copy()
            task_in_day.rotate(1)
            new_day_data = data_new_day_timetable()

            for task_id in task_in_day:
                freetime_index = check_free_time_of_day(new_day_data)
                task_data = task_id_dict[task_id]
                new_day_data = put_task_in_timetable(task_id,task_data,freetime_index,new_day_data)
            initial_solution_timetable[day] = new_day_data
            all_change_timetable[day] = new_day_data
            neighbours.append(initial_solution_timetable)
            if count >= 1:
                neighbours.append(all_change_timetable)
        count += 1

    return neighbours


def getBestNeighbour(time_dict,task_id_dict, neighbours):
    bestEnergy = calculate_energy(neighbours[0],task_id_dict,time_dict)
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentEnergy = calculate_energy(neighbour,task_id_dict,time_dict)
        if currentEnergy > bestEnergy:
            bestEnergy = currentEnergy
            bestNeighbour = neighbour
    return bestNeighbour, bestEnergy



def hillClimbing(timetable,task_id_dict,time_dict):
    currentSolution = randomSolution(timetable,task_id_dict,time_dict)
    print('initial solution: ',currentSolution)
    currentEnergy = calculate_energy(currentSolution,task_id_dict,time_dict)
    neighbours = getNeighbours(currentSolution,task_id_dict)
    print('lengh of neighbors: ',len(neighbours))
    bestNeighbour, bestEnergy = getBestNeighbour(time_dict,task_id_dict,neighbours)
    print(f'current currentEnergy: {currentEnergy}')
    # print(f'1 best Energy: {bestEnergy}')
    energy_hist = []
    energy_hist.append(currentEnergy)
    energy_hist.append(bestEnergy)
    while bestEnergy > currentEnergy:
        currentSolution = bestNeighbour
        currentEnergy = bestEnergy
        energy_hist.append(currentEnergy)
        neighbours = getNeighbours(currentSolution,task_id_dict)
        bestNeighbour, bestEnergy = getBestNeighbour(time_dict,task_id_dict,neighbours)
    # energy_hist.pop(-1)
    return currentSolution, currentEnergy,energy_hist