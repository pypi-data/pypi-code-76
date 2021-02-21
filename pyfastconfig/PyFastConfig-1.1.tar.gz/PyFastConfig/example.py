import PyFastConfig as fc

#Declare
min_t = 25
max_t = 35.5
arr = [45, 'hello', 81.5]
text = 'Simple Text'

#Save
array = [min_t, max_t, arr, text]
fc.save(array)

#Load
#import values (only if run_mode is not False)
#With copy namespace
exec(fc.load("config.txt"))


#Returns names
print(fc.load("config.txt", return_only_names=True))

#Returns values
print(fc.load("config.txt", return_only_values=True))

#Returns an array (use if you have disabled any of the following options: save_types or save_names)
print(fc.load("config.txt", run_mode=False))


#Result
print(min_t)
print(max_t)
print(min_t + max_t)
print(arr)
print(arr[0] + arr[2])
print(text)