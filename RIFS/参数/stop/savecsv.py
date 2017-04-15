import csv

csvfile = file('0.4.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(["pStoppingDepth",1,2,3,4,5])
writer.writerow(["ALL",1,1,1,1,1])
writer.writerow(["ALL2",0.795,0.795,0.809,0.806,0.806])
writer.writerow(["ALL3",0.856,0.863,0.863,0.883,0.883])
writer.writerow(["ALL4",0.910,0.930,0.939,0.949,0.949])
