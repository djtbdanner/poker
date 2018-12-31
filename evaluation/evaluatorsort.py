import evaluation.evaluator

def quickSort(alist):
    quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
    if first<last:

        splitpoint = partition(alist,first,last)

        quickSortHelper(alist,first,splitpoint-1)
        quickSortHelper(alist,splitpoint+1,last)


def partition(alist,first,last):
    
    pivotvalue = alist[first]

    leftmark = first+1
    rightmark = last

    done = False
    while not done:
        while leftmark <= rightmark and evaluation.evaluator.leftIsLessThanOrEqual(alist[leftmark], pivotvalue):
            leftmark = leftmark + 1
        
        while evaluation.evaluator.leftIsGreaterOrEqual(alist[rightmark], pivotvalue) and rightmark >= leftmark:
            rightmark = rightmark -1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp


    return rightmark

# alist = [['AS','QH','2D','3D','4D'],['10S','QH','2D','3D','4D'],['AS','KH','QD','3D','4D'],['5D','8S','2D','3D','4D'],]
# print(alist)
# quickSort(alist)
# print(alist)
