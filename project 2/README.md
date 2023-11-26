# bookstore II
## 功能

实现一个提供网上购书功能的网站后端。<br>
网站支持书商在上面开商店，购买者可以通过网站购买。<br>
买家和卖家都可以注册自己的账号。<br>
一个卖家可以开一个或多个网上商店，
买家可以为自已的账户充值，在任意商店购买图书。<br>
支持 下单->付款->发货->收货 流程。<br>

1.实现对应接口的功能，见项目的doc文件夹下面的.md文件描述 （60%）<br>

其中包括：

1)用户权限接口，如注册、登录、登出、注销<br>

2)买家用户接口，如充值、下单、付款<br>

3)卖家用户接口，如创建店铺、填加书籍信息及描述、增加库存<br>

通过对应的功能测试，所有test case都pass <br>


2.为项目添加其它功能 ：（40%）<br>

1)实现后续的流程 <br>
发货 -> 收货

2)搜索图书 <br>
用户可以通过关键字搜索，参数化的搜索方式；
如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。
如果显示结果较大，需要分页
(使用全文索引优化查找)

3)订单状态，订单查询和取消定单<br>
用户可以查自已的历史订单，用户也可以取消订单。<br>
取消定单可由买家主动地取消定单，或者买家下单后，经过一段时间超时仍未付款，定单也会自动取消。 <br>


## bookstore目录结构
```
bookstore
  |-- be                            后端
        |-- model                     后端逻辑代码
        |-- view                      访问后端接口
        |-- ....
  |-- doc                           JSON API规范说明
  |-- fe                            前端访问与测试代码
        |-- access
        |-- bench                     效率测试
        |-- data                    
            |-- book.db                 sqlite 数据库(book.db，较少量的测试数据)
            |-- book_lx.db              sqlite 数据库(book_lx.db， 较大量的测试数据，要从网盘下载)
            |-- scraper.py              从豆瓣爬取的图书信息数据的代码
        |-- test                      功能性测试（包含对前60%功能的测试，不要修改已有的文件，可以提pull request或bug）
        |-- conf.py                   测试参数，修改这个文件以适应自己的需要
        |-- conftest.py               pytest初始化配置，修改这个文件以适应自己的需要
        |-- ....
  |-- ....
```


## 安装配置
从 https://gitea.shuishan.net.cn/CDMS.Zhouxuan.2023Fall.DASE/Project_2 获取代码，并以 bookstore 文件夹为根目录打开

强调一下，尽量新建干净的环境并且使用3.6或者3.7的 Python！

安装 Python (需要 Python3.6 以上)

进入 bookstore 文件夹下：

安装依赖

    pip install -r requirements.txt

Linux 和 MacOS 执行测试
    
    bash script/test.sh

Windows 执行测试参考视频：https://www.bilibili.com/video/BV1Lu4y1h7Pn/
（注意：如果提示`"RuntimeError: Not running with the Werkzeug Server"`，请输入下述命令，将 flask 和 Werkzeug 的版本均降低为2.0.0。）
 
    pip install flask==2.0.0  
    pip install Werkzeug==2.0.0

bookstore/fe/data/book.db中包含测试的数据，从豆瓣网抓取的图书信息，
其DDL为：
```python
create table book
(
    id TEXT primary key,
    title TEXT,
    author TEXT,
    publisher TEXT,
    original_title TEXT,
    translator TEXT,
    pub_year TEXT,
    pages INTEGER,
    price INTEGER,
    currency_unit TEXT,
    binding TEXT,
    isbn TEXT,
    author_intro TEXT,
    book_intro text,
    content TEXT,
    tags TEXT,
    picture BLOB
);
```
更多的数据可以从网盘下载，下载地址为，链接：

	https://pan.baidu.com/s/1bjCOW8Z5N_ClcqU54Pdt8g
提取码：

	hj6q

这份数据同bookstore/fe/data/book.db的schema相同，但是有更多的数据(约3.5GB, 40000+行)
## 要求

**1人**完成下述内容：

1.允许向接口中增加或修改参数，允许修改 HTTP 方法，允许增加新的测试接口，请尽量不要修改现有接口的 url 或删除现有接口，请根据设计合理的拓展接口（加分项+2～5分）。
测试程序如果有问题可以提bug （加分项，每提1个 bug +2, 提1个 pull request +5）。

2.核心数据使用关系型数据库（PostgreSQL 或 MySQL 数据库）。
blob 数据（如图片和大段的文字描述）可以分离出来存其它 NoSQL 数据库或文件系统。

3.对所有的接口都要写 test case，通过测试并计算代码覆盖率（有较高的覆盖率是加分项 +2~5）。

4.尽量使用正确的软件工程方法及工具，如，版本控制，测试驱动开发 （利用版本控制是加分项 +2~5）

5.后端使用技术，实现语言不限；不要复制这个项目上的后端代码（不是正确的实践， 减分项 -2~5）

6.不需要实现页面

7.最后评估分数时考虑以下要素：

1）实现完整度，全部测试通过，效率合理

2）正确地使用数据库和设计分析工具，ER图，从ER图导出关系模式，规范化，事务处理，索引等

3）其它...


## 报告内容

1.简述从文档型数据库到关系型数据库的改动，以及改动的理由（如提高访问速度，便于编写业务逻辑代码等）

2.要求中提到的点，可以适当在报告中展示

3.关系数据库设计：关系型 schema

4.对60%基础功能和40%附加功能的接口、后端逻辑、数据库操作、测试用例进行介绍，展示测试结果与测试覆盖率。

5.如果完成，可以展示本次大作业的亮点，比如要求中的“3 4”两点。

注：验收依据为报告，本次大作业所作的工作要完整展示在报告中。


## 验收与考核准测

- 提交**代码+报告**压缩包到**作业提交入口**
- 命名规则：2023_ECNU_PJ2_学号_姓名(.zip)
- 提交截止日期：**2023.12.23 23:59**

考核标准：

1.没有提交或没有实质的工作，得D
2.完成"要求"中的第1点，可得C
3.完成前3点，通过全部测试用例且有较高的测试覆盖率，可得B
4.完成前2点的基础上，体现出第3 4点，可得A
5.以上均为参考，最后等级会根据最终的工作质量有所调整



