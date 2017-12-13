

def sort(source):
    if len(source) == 1:
        return source
    left = sort(source[:len(source)//2])
    right = sort(source[len(source)//2:])
    return merge(left,right)

def merge(left, right):
    l, r, result = 0, 0, []
    for times in range(len(left)+len(right)):
        if l != len(left) and r != len(right):
            if len(left[l][2]) > len(right[r][2]):
                result.append(right[r])
                r += 1
            else:
                result.append(left[l])
                l += 1
        elif l == len(left):
            result.append(right[r])
            r += 1
        elif r == len(right):
            result.append(left[l])
            l += 1
    return result

print(sort([[1,2,[9,8,8,7,6,5,4,3,5,4,2,1,0]],[2,3,[1,2,3]],[3,4,[1,2]],[4,5,[1,2,3,4,5]]]))
