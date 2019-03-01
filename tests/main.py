def test_segments(segments, height, affiche=False):
    result = np.zeros((height, height))
    for segment in segments:
        for point in segment:
            result[point[0], point[1]] +=1
    if affiche :
        print(result)
    return np.array_equal(np.ones((height, height)), result)


def test_all_segments(height):
    max_lenght = height-1
    total = 0
    fails = 0
    passed_all = True
    not_working = []
    for x in range(height):
        total+=2
        #from (0, 0)
        seg_tmp = get_segment(0, 0, x, max_lenght, height)
        if len(seg_tmp) > 1 :
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
        else :
            not_working.append([0, 0, x, max_lenght])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp

        seg_tmp = get_segment(0, 0, max_lenght, x, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
        else :
            not_working.append([0, 0, max_lenght, x, height])
            print("pas de segment pour", not_working[-1])
            print(seg_temp)
            fails+=1
            tmp = False
        passed_all = passed_all and tmp
    for x in range(height):
        total+=2
        #from (max, 0)
        seg_tmp = get_segment(max_lenght, 0, 0, x, height)
        if len(seg_tmp) >= 1 :
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
        else :
            not_working.append([max_lenght, 0, 0, x])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp

        seg_tmp = get_segment(max_lenght, 0, x, 0, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                fails+=1
        else :
            not_working.append([max_lenght, 0, x, 0])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp

    for x in range(height):
        total+=2
        #from (max, max)
        seg_tmp = get_segment(max_lenght, max_lenght, x, 0, height)
        if len(seg_tmp) >= height-1 :
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                fails+=1
        else :
            not_working.append([max_lenght, max_lenght, x, 0])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp


        seg_tmp = get_segment(max_lenght, max_lenght, 0, x, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                fails+=1
        else :
            not_working.append([max_lenght, max_lenght, 0, x])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp


    for x in range(height):
        total+=2
        #from (0, max)
        seg_tmp = get_segment(0, max_lenght, x, 0, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                not_working.append([0, max_lenght, x, 0])
                print("erreur avec le segment",not_working[-1])
                fails+=1
        else :
            not_working.append([0, max_lenght, x, 0])
            fails+=1
            print("pas de segment pour", not_working[-1])
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp


        seg_tmp = get_segment(0, max_lenght, max_lenght, x, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                not_working.append([0, max_lenght, max_lenght, x])
                print("erreur avec le segment",not_working[-1])
                fails+=1
        else :
            not_working.append([0, max_lenght, 0, x])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp
    print("nombre total : ", total, ", nombre raté :", fails)
    return passed_all
