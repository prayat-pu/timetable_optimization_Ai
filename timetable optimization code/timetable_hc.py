import seaborn as sns
from  hill_climbling import *
import matplotlib.pyplot as plt

timetable = {'monday':[(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0)],
             'tuesday':[(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0)],
             'wednesday':[(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0)],
             'thursday':[(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0)],
             'friday':[(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0),(-1,'',0)]}

# define contants
time_dict = {0:("08.00-09.00",5),
            1:("09.00-10.00",4),
            2:("10.00-11.00",3),
            3:("11.00-12.00",2),
            4:("13.00-14.00",3),
            5:("14.00-15.00",2),
            6:("15.00-16.00",1),
            7:("16.00-17.00",1)}

task_id_dict = {0:('clean room',1,1),
          1:('do homework',2,2),
          2:('write blog',3,3),
          3:('edit video and put on youtube',3,3),
          4:('play game',1,2),
          5:('read a book',1,1),
          6:('english practice',1,1),
          7:('watch movie',1,3),
          8:('exercise',1,1),
          9:('study AI',3,3),
          10:('guitar practice',1,1),
          11:('do research',3,3),
          12:('study Agile',3,3)}

currentSolution, currentEnergy,energy_hist = hillClimbing(timetable,task_id_dict,time_dict)
print(energy_hist)
print('final solution: ',currentSolution)
ax = sns.barplot(x=list(range(len(energy_hist))),y=energy_hist,alpha=0.5)
ax.set(xlabel='order of current energy',ylabel='max remain energy per week',title='Energy History',ylim=[max(energy_hist)-20,max(energy_hist)])
plt.show()
