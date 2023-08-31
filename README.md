# News-text-classifier
## 1 目录
├─chart  
│  ├─procedure chart：设计流图  
│  └─screenshot：运行截图  
├─code  
│  ├─databases  
│  ├─input：训练数据和预测数据  
│  ├─model_and_dict：模型和词典  
│  ├─output：textCNN的输出  
│  └─temp_and_file：软件运行时所需的文件以及输出文件  
├─document：设计文档  
└─references  
## 2 算法介绍
<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/textCNN%E7%BB%93%E6%9E%84.png" alt="替代文本" width="700px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/procedure%20chart/textCNN.png" alt="替代文本" width="500px">  
将数据进行预处理（分词，去停用词，去非中文）后，使用预训练的词典，将单词矩阵（一行是一个句子）转换成单词索引矩阵，训练数据一共180000条，将所有文本长度补齐至12个单词长度。按照batch_size = 64划分批次，通过embeding层将每一个单词映射成64维向量，使用unsqueeze函数添加一个维度以进行卷积操作。分别使用H = 3, 4, 5三种尺寸的卷积核进行卷积操作（卷积核宽度等于词向量的维度），并通过relu函数激活，然后最大池化降维。最后通过全连接层和softmax层映射到10个class。
以下是卷积层输出的维度计算。

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/%E5%8D%B7%E7%A7%AF%E5%B1%82%E8%BE%93%E5%87%BA.png" alt="替代文本" width="700px">

## 3 系统使用说明
本系统使用python语言开发，使用pyqt5程序包设计系统界面，利用MySQLWorkbench连接数据库。
### 3.1 系统运行环境和配置
| 项目 | 详情 |
| -------- | :-------: |
| 开发硬件环境	| AMD Ryzen 5 3500U 2.10GHz 16.0GB内存 |
| 操作系统	| Windows11家庭中文版 |
| 开发环境与工具	| PyCharm Community Edition 2022.1.3;pyQt5 |
| 编程语言	| python 3.11 |
| 模型 | textCNN |

### 3.2 系统操作说明
#### 3.2.1 登录模块说明
以下是登录注册模块截图，用户账号由8位数字组成，密码长度在8-16位字符，登录界面和账号注册界面右下角都有勾选框，用户可选择注册为普通用户或管理员，并且登录对应账号。

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E7%99%BB%E9%99%86.png" alt="替代文本" width="400px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E6%B3%A8%E5%86%8C.png" alt="替代文本" width="400px">

### 3.2.2 新闻爬取模块说明
新闻爬取模块大致分为两块，新闻的预爬取和正式爬取，用户（管理员）可选择爬取新闻的类别和爬取数量（最大默认为80条），点击“预爬取”按钮，程序开始获取新闻标题和各条新闻的url，接着点击“爬取”按钮，程序开始逐条爬取新闻，并计数爬取失败的条数，最后点击“保存到数据库”，若数据库已经保存了某条新闻，则相同的新闻不会二次入库，并提示保存失败条数。

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E6%96%B0%E9%97%BB%E7%88%AC%E5%8F%961.png" alt="替代文本" width="700px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E6%96%B0%E9%97%BB%E7%88%AC%E5%8F%962.png" alt="替代文本" width="700px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E6%96%B0%E9%97%BB%E7%88%AC%E5%8F%963.png" alt="替代文本" width="700px">

### 3.2.3 数据预处理模块说明
数据预处理主要用于处理乱码数据和内容缺失数据，进入“数据预处理”界面，用户点击“刷新”按钮获取最新数据，用户可查看到各新闻标题以及新闻链接，选中列表中的新闻，点击“查看内容”按钮，可在左下角文本显示框中查看新闻内容，点击“词云”按钮，可对新闻文本生成词云，对于缺失数据，用户可在选中后点击“删除记录”按钮删除对应数据。

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E6%95%B0%E6%8D%AE%E9%A2%84%E8%A7%88.png" alt="替代文本" width="700px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E5%88%A0%E9%99%A4.png" alt="替代文本" width="700px">

### 3.2.4 新闻分类模块说明
进入“文本分类”模块，用户点击“刷新”按钮，获取最新数据，点击“执行分类”按钮即可对新闻进行分类（程序已保存训练好的模型），点击“重置”按钮会将当前管理员管理的所有新闻分类信息重置，最后，若对分类有异议，可自行更改。

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E9%87%8D%E7%BD%AE.png" alt="替代文本" width="700px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E5%88%86%E7%B1%BB.png" alt="替代文本" width="700px">

<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E4%BF%AE%E6%94%B9%E5%88%86%E7%B1%BB.png" alt="替代文本" width="700px">

### 3.2.5 管理员个人中心模块说明
管理员个人中心界面所显示的“贡献值”是管理员所管理的所有新闻的计数，左下的表格是对应类别的计数。点击“编辑个人信息”按钮即可跳转信息编辑界面，提供修改昵称和个人简介以及密码修改服务。点击“登出账号”将退出当前账号，跳转至登录界面。
<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E4%B8%AA%E4%BA%BA%E6%8E%8C%E5%BF%83.png" alt="替代文本" width="700px">
 
<img src="https://github.com/tomatoyou/News-text-classifier/blob/main/chart/screenshot/%E4%BF%AE%E6%94%B9%E5%AF%86%E7%A0%81.png" alt="替代文本" width="700px">

