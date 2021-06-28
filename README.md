# Start teaching you to train your own classification model from the production of CIFAR dataset
> Catalogue
>* Make your own dataset with reference to CIFAR format
>* Use your own dataset to train the model
## Reference CIFAR format to create their own datasets
###### Detailed tutorial code has been disclosed in my Github, Here is the code used
* First of all the pictures on the files by category folder, the folder name is the category name. For example: if there are 20 categories, there are 20 folders
* Extract the path of all pictures into a file, each line in the file contains the path of the picture and the index of the category to which the picture belongs (the corresponding relationship between the picture category and the index will be generated at the same time)
    * Run get_filename.py file, generating the image path + category index (data / cow_jpg.lst) and the category index correspondence table (data / object_list.txt)
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
    * The category index correspondence table corresponds to the category represented by the file name and the index, because the string cannot be used as the category name when training the model. For example: dog 0, cat 1, chicken 3...
* Split the training set and the test set (here I will shuffle all the data first, take a part as the training set, and the rest as the test set)
    * Open make_test_batch.py 
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
    * Fill in the image path + category index (data/cow_jpg.lst) file generated in the previous step to line 3
    * Set the split threshold, I set 0.2 as the split threshold, which means that the first 20% is the test set, and the rest is the training set
    * Run!
    * Generate <kbd>test_batch</kbd> (file name: data/cow_jpg_test.lst)
    And <kbd>train_batch</kbd> (file name: data/cow_jpg_train.lst)
* Make CIFAR batch
    * Run the demo.py file, fill in the file_list parameter in the image path file generated in the previous step (data/cow_jpg_train.lst)
    * Fill in the split tran file (cow_jpg_train.lst), set bin_num to 4, four batch_train files will be generated
    * Fill in the split tran file (cow_jpg_test.lst), set bin_num to 1, and a batch_test file will be generated
    * A total of five files are generated, which are the same as the CIFAR compressed package provided by the management
* Make CIFAR .mate file
    * Create a batches.meta file in the batch folder
    * Open the edit_mate.py file
    * Fill in the number of samples contained in each batch (num_cases_per_batch), here I set 2500 because I have a total of 10,000 samples, divided into four batches
    * Replace the category name (the file name is not an index) in the category index table file (object_list.txt) to the tenth line in order, which should be the category name, which is the file name, for example: cat, dog, chicken, here it is Numeric string
    * Run!
    * Generate batches.meta file
#### This way you will get: data_batch_0,...,test_batch, batches.meta and other three types of files, which are exactly the same as the official CIFAR dataset. Below we take any model that uses the CIFAR dataset as an example. test
## Training the model with the dataset made by yourself
* Open data_utils.py, find the following piece of code, set the download to No (download=False), even if you can’t find it, skip this step
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
* Run the model train.py and report an error
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
    * The reason is that the model does not find the CIFAR file, because the CIFAR function comes with integrity verification (check_integrity), just close it.
* Turn off file integrity verification in CIFAR source code
    * Find the location of the CIFAR source code according to the error message
    * I am ```/opt/conda/envs/ViT/lib/python3.6/site-packages/torchvision/datasets/cifar.py```
    * Open the source code and comment out the following lines
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
    * Find num_classes = 10 in the code, modify 10 to the number of your categories
    * In pycharm, crtl + shift + F can be searched for num_classes
    * Successfully run!
    
    #cifar10Dataset-master This is my blog address https://blog.csdn.net/p609354432/article/details/118312563
