# Returns a list of four lists of images, specifying the columns each image needs to go in to
def sorted_search(searches):
    curr_list = []
    for each in searches:
        curr_list.append((each['image_ratio'], each))
    curr_list.sort(reverse=True, key=lambda tup: tup[0])
    final_list = [[], [], [], []]
    sum_list = [0, 0, 0, 0]
    for each in curr_list:
        min_index = sum_list.index(min(sum_list))
        final_list[min_index].append(each[1])
        sum_list[min_index] += each[0]
    return final_list
