import os
def getFlist(path):
    root_dirs = []

    for root, dirs, files in os.walk(path):
        print('root_dir:', root)
        print('sub_dirs:', dirs)
        print('files:', files)
        root_dirs.append(root)
        print('root_dirs:', root_dirs[1:])
        # for i in range(dirs):
        #     child_path = 'data/%s/'%dirs[i]
        #     for root, dirs, files in os.walk(child_path):
        #         print('child_root_dir:', root)
        #         print('child_sub_dirs:', dirs)
        #         print('child_files:', files)
    root_dirs = root_dirs[1:]
    return root_dirs

def getChildList(root_dirs):
    j = 0
    f = open('data/cow_jpg.lst', 'w')#生成文件路径和类别索引

    for path in root_dirs:
        for root, dirs, files in os.walk(path):
            print('child_root_dir:', root)
            print('child_sub_dirs:', dirs)
            print('child_files:', files)
            for file in files:
                f.write('%s/%s %i\n'%(root,file,j))

        j = j+1
    f.close()

if __name__ == '__main__':
    resDir = 'data'
    f2 = open('data/object_list.txt', 'w')#生成类别和索引的对应表
    root_dirs = getFlist(resDir)
    k = 0
    for root_dir in root_dirs:
        f2.write('%s %s\n'%(root_dir,k))
        k = k+1
    f2.close()
    getChildList(root_dirs)
    print(root_dirs)