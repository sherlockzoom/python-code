

```python
import pandas as pd
```

# 1. 用户的基本属性`user_info.txt`。共6个字段，其中字段性别为0表示性别未知。

> 用户id,性别,职业,教育程度,婚姻状态,户口类型


```python
train_user_info = pd.read_csv("train/user_info_train.txt", header=None)
train_user_info.columns = [u'用户id',u'性别',
                           u'职业',u'教育程度',
                           u'婚姻状态',u'户口类型']
train_user_info.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>用户id</th>
      <th>性别</th>
      <th>职业</th>
      <th>教育程度</th>
      <th>婚姻状态</th>
      <th>户口类型</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3150</td>
      <td>1</td>
      <td>2</td>
      <td>4</td>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6965</td>
      <td>1</td>
      <td>2</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1265</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6360</td>
      <td>1</td>
      <td>2</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2583</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
train_user_info.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 55596 entries, 0 to 55595
    Data columns (total 6 columns):
    用户id    55596 non-null int64
    性别      55596 non-null int64
    职业      55596 non-null int64
    教育程度    55596 non-null int64
    婚姻状态    55596 non-null int64
    户口类型    55596 non-null int64
    dtypes: int64(6)
    memory usage: 2.5 MB


# 2. 银行流水记录bank_detail.txt。共5个字段，其中，第2个字段，时间戳为0表示时间未知；第3个字段，交易类型有两个值，1表示支出、0表示收入；第5个字段，工资收入标记为1时，表示工资收入。

> 用户id,时间戳,交易类型,交易金额,工资收入标记


```python
train_bank_detail = pd.read_csv("train/bank_detail_train.txt", header=None)
train_bank_detail.columns = [u'用户id',u'时间戳',
                             u'交易类型',u'交易金额',
                             u'工资收入标记']
train_bank_detail.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>用户id</th>
      <th>时间戳</th>
      <th>交易类型</th>
      <th>交易金额</th>
      <th>工资收入标记</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6965</td>
      <td>5894316387</td>
      <td>0</td>
      <td>13.756664</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6965</td>
      <td>5894321388</td>
      <td>1</td>
      <td>13.756664</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6965</td>
      <td>5897553564</td>
      <td>0</td>
      <td>14.449810</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6965</td>
      <td>5897563463</td>
      <td>1</td>
      <td>10.527763</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6965</td>
      <td>5897564598</td>
      <td>1</td>
      <td>13.651303</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
train_bank_detail.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 6070197 entries, 0 to 6070196
    Data columns (total 5 columns):
    用户id      int64
    时间戳       int64
    交易类型      int64
    交易金额      float64
    工资收入标记    int64
    dtypes: float64(1), int64(4)
    memory usage: 231.6 MB


# 3. 用户浏览行为browse_history.txt。共4个字段。其中，第2个字段，时间戳为0表示时间未知。

> 用户id,时间戳,浏览行为数据,浏览子行为编号


```python
train_browse_history = pd.read_csv("train/browse_history_train.txt", header=None)
train_browse_history.columns = [u'用户id',u'时间戳',
                                u'浏览行为数据',u'浏览子行为编号']
train_browse_history.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>用户id</th>
      <th>时间戳</th>
      <th>浏览行为数据</th>
      <th>浏览子行为编号</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>34801</td>
      <td>5926003545</td>
      <td>173</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>34801</td>
      <td>5926003545</td>
      <td>164</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>34801</td>
      <td>5926003545</td>
      <td>38</td>
      <td>7</td>
    </tr>
    <tr>
      <th>3</th>
      <td>34801</td>
      <td>5926003545</td>
      <td>45</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>34801</td>
      <td>5926003545</td>
      <td>110</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>




```python
train_browse_history.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 22919547 entries, 0 to 22919546
    Data columns (total 4 columns):
    用户id       int64
    时间戳        int64
    浏览行为数据     int64
    浏览子行为编号    int64
    dtypes: int64(4)
    memory usage: 699.4 MB


# 4. 信用卡账单记录bill_detail.txt。共15个字段，其中，第2个字段，时间戳为0表示时间未知。为方便浏览，字段以表格的形式给出。

>   用户id,账单时间戳,银行id,上期账单金额,上期还款金额,信用卡额度,本期账单余额,本期账单最低还款额,消费笔数,本期账单金额,调整金额,循环利息,可用金额,预借现金额度,还款状态


```python
train_bill_detail = pd.read_csv("train/bill_detail_train.txt", header=None)
train_bill_detail.columns = [ u'用户id',u'账单时间戳',u'银行id',u'上期账单金额',
                             u'上期还款金额',u'信用卡额度',u'本期账单余额',
                             u'本期账单最低还款额',u'消费笔数',u'本期账单金额',
                             u'调整金额',u'循环利息',u'可用金额',
                             u'预借现金额度',u'还款状态']
train_bill_detail.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>用户id</th>
      <th>账单时间戳</th>
      <th>银行id</th>
      <th>上期账单金额</th>
      <th>上期还款金额</th>
      <th>信用卡额度</th>
      <th>本期账单余额</th>
      <th>本期账单最低还款额</th>
      <th>消费笔数</th>
      <th>本期账单金额</th>
      <th>调整金额</th>
      <th>循环利息</th>
      <th>可用金额</th>
      <th>预借现金额度</th>
      <th>还款状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3150</td>
      <td>5906744363</td>
      <td>6</td>
      <td>18.626118</td>
      <td>18.661937</td>
      <td>20.664418</td>
      <td>18.905766</td>
      <td>17.847133</td>
      <td>1</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>19.971271</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3150</td>
      <td>5906744401</td>
      <td>6</td>
      <td>18.905766</td>
      <td>18.909954</td>
      <td>20.664418</td>
      <td>19.113305</td>
      <td>17.911506</td>
      <td>1</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>19.971271</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3150</td>
      <td>5906744427</td>
      <td>6</td>
      <td>19.113305</td>
      <td>19.150290</td>
      <td>20.664418</td>
      <td>19.300194</td>
      <td>17.977610</td>
      <td>1</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>19.971271</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3150</td>
      <td>5906744515</td>
      <td>6</td>
      <td>19.300194</td>
      <td>19.300280</td>
      <td>21.000890</td>
      <td>20.303240</td>
      <td>18.477177</td>
      <td>1</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>20.307743</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3150</td>
      <td>5906744562</td>
      <td>6</td>
      <td>20.303240</td>
      <td>20.307744</td>
      <td>21.000890</td>
      <td>20.357134</td>
      <td>18.510985</td>
      <td>1</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>20.307743</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
train_bill_detail.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2338118 entries, 0 to 2338117
    Data columns (total 15 columns):
    用户id         int64
    账单时间戳        int64
    银行id         int64
    上期账单金额       float64
    上期还款金额       float64
    信用卡额度        float64
    本期账单余额       float64
    本期账单最低还款额    float64
    消费笔数         int64
    本期账单金额       float64
    调整金额         float64
    循环利息         float64
    可用金额         float64
    预借现金额度       float64
    还款状态         int64
    dtypes: float64(10), int64(5)
    memory usage: 267.6 MB


# 5放款时间信息loan_time.txt。共2个字段，用户id和放款时间。 

> 用户id,放款时间


```python
train_loan_time = pd.read_csv("train/loan_time_train.txt", header=None)
train_loan_time.columns = [u'用户id',u'放款时间']
train_loan_time.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>用户id</th>
      <th>放款时间</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>5914855887</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>5914855887</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>5914855887</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>5914855887</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>5914855887</td>
    </tr>
  </tbody>
</table>
</div>




```python
train_loan_time.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 55596 entries, 0 to 55595
    Data columns (total 2 columns):
    用户id    55596 non-null int64
    放款时间    55596 non-null int64
    dtypes: int64(2)
    memory usage: 868.8 KB


# 6.顾客是否发生逾期行为的记录overdue.txt。共2个字段。样本标签为1，表示逾期30天以上；样本标签为0，表示逾期10天以内。

> 注意：逾期10天~30天之内的用户，并不在此问题考虑的范围内。用于测试的用户，只提供id列表，文件名为testUsers.csv

> 用户id,样本标签


```python
train_overdue = pd.read_csv('train/overdue_train.txt', header=None)
train_overdue.columns = [u'用户id',u'样本标签']
train_overdue.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>用户id</th>
      <th>样本标签</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
train_overdue.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 55596 entries, 0 to 55595
    Data columns (total 2 columns):
    用户id    55596 non-null int64
    样本标签    55596 non-null int64
    dtypes: int64(2)
    memory usage: 868.8 KB



