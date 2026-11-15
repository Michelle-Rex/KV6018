import container_instances as prob

#sort cylinders by size
def size_sort(instance: prob.Instance):
    #sort cylinders largest to smallest
    new_order = sorted(instance.cylinders, key = lambda x: x.diameter, reverse = True) 