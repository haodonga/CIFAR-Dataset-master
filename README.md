#从CIFAR数据集制作开始教你训练自己的分类模型
> 目录
>* 参考CIFAR的格式制作自己的数据集
>* 使用自己制作的数据集训练模型
##参考CIFAR的格式制作自己的数据集
###### 代码已经公开在本人的Github，下面是代码使用的详细教程，本代码使用python2.x编写，不会python2.x没关系（不涉及python2.x的编写），装一个就行。
* 首先将所有图片按类别放在文件夹中，文件夹名为类别名。例如：存在20个类就分20个文件夹
* 将所有图片的路径提取到一个文件中，文件中每行包含图片路径和图片所属类别的索引（同时会生成图片类别和索引的对应关系）
    * 运行 get_filename.py 文件，生成图片路径+类别索引（data/cow_jpg.lst）和类别索引对应表（data/object_list.txt）
        ```python
        import os
        def getFlist(path):
            root_dirs = []
            for root, dirs, files in os.walk(path):
                print('root_dir:', root)
                print('sub_dirs:', dirs)
                print('files:', files)
                root_dirs.append(root)
                print('root_dirs:', root_dirs[1:])
            root_dirs = root_dirs[1:]
            return root_dirs
        def getChildList(root_dirs):
            j = 0
            f = open('data/cow_jpg.lst', 'w')#生成文件路径和类别索引
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
         ```
    * 类别索引对应表就是将文件名所表示的类别与索引相对应，因为训练模型时不能以字符串作为类别名。例如：狗 0，猫 1，鸡 3……
* 拆分训练集与测试集（这里我先将所有数据打乱，取一部分作为训练集，剩下的则作为测试集）
    * 打开 make_test_batch.py 文件
        ```python
        import os
        import random
        f = open('data/cow_jpg.lst')#上一步生成的图片路径文件
        list = f.readlines()
        print(len(list))
        random.shuffle(list)
        print(list)
        set_num = int(float(len(list))*0.2)
        #0.2为拆分阈值，0.2则是前20%为测试集，剩下的是训练集
        test_list = list[:set_num]
        train_list = list[set_num:]
        print('================')
        print(len(test_list))
        print(len(train_list))
        print(test_list and train_list)
        
        f2 = open('data/cow_jpg_train.lst','w')
        for i in train_list:
            f2.write(i)
        f3 = open('data/cow_jpg_test.lst','w')
        for i in test_list:
            f3.write(i)
        f.close()
        f2.close()
        f3.close()
        ```
    * 将上一步生成的图片路径+类别索引（data/cow_jpg.lst）文件填到第3行
    * 设置拆分阈值，我设定了0.2为拆分阈值，其含义为前20%为测试集，剩下的是训练集
    * 运行！
    * 生成 <kbd>test_batch</kbd> (文件名：data/cow_jpg_test.lst)
    和 <kbd>train_batch</kbd> (文件名：data/cow_jpg_train.lst)
* 制作CIFAR的batch
    * 运行 demo.py 文件，其中将file_list参数填写上一步生成的图片路径文件（data/cow_jpg_train.lst）
    * 填写拆分出的tran文件（cow_jpg_train.lst），bin_num 设置为4，就会生成四个batch_train文件
    * 填写拆分出的tran文件（cow_jpg_test.lst），bin_num 设置为1，就会生成一个batch_test文件
    * 共生成五个文件，与管方提供的CIFAR压缩包相同
* 制作CIFAR的.mate文件
    * 在batch文件夹中新建一个batches.meta文件
    * 打开 edit_mate.py 文件
    * 填写每个batch包含的样本数量(num_cases_per_batch) ，这里我设置了2500因为我一共有10000个样本，分了四个batch
    * 将类别索引表文件（object_list.txt）中的类别名（文件名不是索引）按顺序替换到第十行，应该是类别名，也就是文件名，例如：猫，狗，鸡，我这里是数字字符串
    * 运行！
    * 生成 batches.meta 文件
####这样你就会得到：data_batch_0,...,test_batch,batches.meta等三类文件，与官方的CIFAR数据集完全一致，下面我们以任何一个使用CIFAR数据集的模型为例，进行测试
##使用自己制作的数据集训练模型
* 打开data_utils.py,找到下面这段代码，将下载设置为否（download=False），找不到就算了，跳过这步
   ```python
  if args.dataset == "cifar10":
        trainset = datasets.CIFAR10(root="./data",
                                    train=True,
                                    download=False,
                                    transform=transform_train)
     
        testset = datasets.CIFAR10(root="./data",
                                   train=False,
                                   download=False,
                                   transform=transform_test) if args.local_rank in [-1, 0] else None
    ```
* 跑一下模型 train.py ,报错 
    * ```
      Traceback (most recent call last):
          File "/workspace/ViT-pytorch-main/train.py", line 347, in <module>
            main()
          File "/workspace/ViT-pytorch-main/train.py", line 342, in main
            train(args, model)
          File "/workspace/ViT-pytorch-main/train.py", line 158, in train
            train_loader, test_loader = get_loader(args)
          File "/workspace/ViT-pytorch-main/utils/data_utils.py", line 31, in get_loader
            transform=transform_train)
          File "/opt/conda/envs/ViT/lib/python3.6/site-packages/torchvision/datasets/cifar.py", line 93, in __init__
            self._load_meta()
          File "/opt/conda/envs/ViT/lib/python3.6/site-packages/torchvision/datasets/cifar.py", line 99, in _load_meta
            ' You can use download=True to download it'
            RuntimeError: Dataset metadata file not found or corrupted. You can use download=True to download it
        ``` 
    * 原因是模型没有找到CIFAR文件，因为CIFAR函数中自带完整性验证(check_integrity)，关闭即可。
* 关闭CIFAR源码中的文件完整性验证
    * 根据报错信息找到CIFAR源码的位置
    * 我这里是```/opt/conda/envs/ViT/lib/python3.6/site-packages/torchvision/datasets/cifar.py```
    * 打开源码，注释掉如下几行
      ```
        if not check_integrity(path, self.meta['md5']):
            raise RuntimeError('Dataset metadata file not found or corrupted.' +
                           ' You can use download=True to download it')
      ```
      ```
        if not self._check_integrity():
             raise RuntimeError('Dataset not found or corrupted.' +
                                ' You can use download=True to download it')
        ```
      ```
        if not check_integrity(fpath, md5):
           return False
        ```
    * 找到代码中的num_classes = 10，将10修改为你的类别数量  
    * pycharm中可以 crtl + shift + F 搜索 num_classes
    * 运行成功！
    
    