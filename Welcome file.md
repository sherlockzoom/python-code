---


---

<p><strong>Chapter 2 – End-to-end Machine Learning project</strong></p>
<p><em>Welcome to Machine Learning Housing Corp.! Your task is to predict median house values in Californian districts, given a number of features from these districts.</em></p>
<p><em>This notebook contains all the sample code and solutions to the exercices in chapter 2.</em></p>
<p><strong>Note</strong>: You may find little differences between the code outputs in the book and in these Jupyter notebooks: these slight differences are mostly due to the random nature of many training algorithms: although I have tried to make these notebooks’ outputs as constant as possible, it is impossible to guarantee that they will produce the exact same output on every platform. Also, some data structures (such as dictionaries) do not preserve the item order. Finally, I fixed a few minor bugs (I added notes next to the concerned cells) which lead to slightly different results, without changing the ideas presented in the book.</p>
<h1 id="setup">Setup</h1>
<p>First, let’s make sure this notebook works well in both python 2 and 3, import a few common modules, ensure MatplotLib plots figures inline and prepare a function to save the figures:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># To support both python 2 and python 3</span>
<span class="token keyword">from</span> __future__ <span class="token keyword">import</span> division<span class="token punctuation">,</span> print_function<span class="token punctuation">,</span> unicode_literals

<span class="token comment"># Common imports</span>
<span class="token keyword">import</span> numpy <span class="token keyword">as</span> np
<span class="token keyword">import</span> os
<span class="token keyword">import</span> sys

<span class="token comment"># to make this notebook's output stable across runs</span>
np<span class="token punctuation">.</span>random<span class="token punctuation">.</span>seed<span class="token punctuation">(</span><span class="token number">42</span><span class="token punctuation">)</span>

<span class="token comment"># To plot pretty figures</span>
<span class="token operator">%</span>matplotlib inline
<span class="token keyword">import</span> matplotlib
<span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>pyplot <span class="token keyword">as</span> plt
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'axes.labelsize'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">14</span>
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'xtick.labelsize'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">12</span>
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'ytick.labelsize'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">12</span>

<span class="token comment"># Where to save the figures</span>
PROJECT_ROOT_DIR <span class="token operator">=</span> <span class="token string">"."</span>
CHAPTER_ID <span class="token operator">=</span> <span class="token string">"end_to_end_project"</span>
IMAGES_PATH <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>PROJECT_ROOT_DIR<span class="token punctuation">,</span> <span class="token string">"images"</span><span class="token punctuation">,</span> CHAPTER_ID<span class="token punctuation">)</span>
<span class="token keyword">if</span> <span class="token operator">not</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>exists<span class="token punctuation">(</span>IMAGES_PATH<span class="token punctuation">)</span><span class="token punctuation">:</span>
    os<span class="token punctuation">.</span>makedirs<span class="token punctuation">(</span>IMAGES_PATH<span class="token punctuation">)</span>

<span class="token keyword">def</span> <span class="token function">save_fig</span><span class="token punctuation">(</span>fig_id<span class="token punctuation">,</span> tight_layout<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> fig_extension<span class="token operator">=</span><span class="token string">"png"</span><span class="token punctuation">,</span> resolution<span class="token operator">=</span><span class="token number">300</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    path <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>IMAGES_PATH<span class="token punctuation">,</span> fig_id <span class="token operator">+</span> <span class="token string">"."</span> <span class="token operator">+</span> fig_extension<span class="token punctuation">)</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Saving figure"</span><span class="token punctuation">,</span> fig_id<span class="token punctuation">)</span>
    <span class="token keyword">if</span> tight_layout<span class="token punctuation">:</span>
        plt<span class="token punctuation">.</span>tight_layout<span class="token punctuation">(</span><span class="token punctuation">)</span>
    plt<span class="token punctuation">.</span>savefig<span class="token punctuation">(</span>path<span class="token punctuation">,</span> <span class="token builtin">format</span><span class="token operator">=</span>fig_extension<span class="token punctuation">,</span> dpi<span class="token operator">=</span>resolution<span class="token punctuation">)</span>

<span class="token comment"># Ignore useless warnings (see SciPy issue #5998)</span>
<span class="token keyword">import</span> warnings
warnings<span class="token punctuation">.</span>filterwarnings<span class="token punctuation">(</span>action<span class="token operator">=</span><span class="token string">"ignore"</span><span class="token punctuation">,</span> module<span class="token operator">=</span><span class="token string">"scipy"</span><span class="token punctuation">,</span> message<span class="token operator">=</span><span class="token string">"^internal gelsd"</span><span class="token punctuation">)</span>
</code></pre>
<h1 id="get-the-data">Get the data</h1>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> os
<span class="token keyword">import</span> tarfile
<span class="token keyword">from</span> six<span class="token punctuation">.</span>moves <span class="token keyword">import</span> urllib

DOWNLOAD_ROOT <span class="token operator">=</span> <span class="token string">"https://raw.githubusercontent.com/ageron/handson-ml/master/"</span>
HOUSING_PATH <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span><span class="token string">"datasets"</span><span class="token punctuation">,</span> <span class="token string">"housing"</span><span class="token punctuation">)</span>
HOUSING_URL <span class="token operator">=</span> DOWNLOAD_ROOT <span class="token operator">+</span> <span class="token string">"datasets/housing/housing.tgz"</span>

<span class="token keyword">def</span> <span class="token function">fetch_housing_data</span><span class="token punctuation">(</span>housing_url<span class="token operator">=</span>HOUSING_URL<span class="token punctuation">,</span> housing_path<span class="token operator">=</span>HOUSING_PATH<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">if</span> <span class="token operator">not</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>isdir<span class="token punctuation">(</span>housing_path<span class="token punctuation">)</span><span class="token punctuation">:</span>
        os<span class="token punctuation">.</span>makedirs<span class="token punctuation">(</span>housing_path<span class="token punctuation">)</span>
    tgz_path <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>housing_path<span class="token punctuation">,</span> <span class="token string">"housing.tgz"</span><span class="token punctuation">)</span>
    urllib<span class="token punctuation">.</span>request<span class="token punctuation">.</span>urlretrieve<span class="token punctuation">(</span>housing_url<span class="token punctuation">,</span> tgz_path<span class="token punctuation">)</span>
    housing_tgz <span class="token operator">=</span> tarfile<span class="token punctuation">.</span><span class="token builtin">open</span><span class="token punctuation">(</span>tgz_path<span class="token punctuation">)</span>
    housing_tgz<span class="token punctuation">.</span>extractall<span class="token punctuation">(</span>path<span class="token operator">=</span>housing_path<span class="token punctuation">)</span>
    housing_tgz<span class="token punctuation">.</span>close<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">fetch_housing_data<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> pandas <span class="token keyword">as</span> pd

<span class="token keyword">def</span> <span class="token function">load_housing_data</span><span class="token punctuation">(</span>housing_path<span class="token operator">=</span>HOUSING_PATH<span class="token punctuation">)</span><span class="token punctuation">:</span>
    csv_path <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>housing_path<span class="token punctuation">,</span> <span class="token string">"housing.csv"</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> pd<span class="token punctuation">.</span>read_csv<span class="token punctuation">(</span>csv_path<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing <span class="token operator">=</span> load_housing_data<span class="token punctuation">(</span><span class="token punctuation">)</span>
housing<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-122.23</td>
      <td>37.88</td>
      <td>41.0</td>
      <td>880.0</td>
      <td>129.0</td>
      <td>322.0</td>
      <td>126.0</td>
      <td>8.3252</td>
      <td>452600.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-122.22</td>
      <td>37.86</td>
      <td>21.0</td>
      <td>7099.0</td>
      <td>1106.0</td>
      <td>2401.0</td>
      <td>1138.0</td>
      <td>8.3014</td>
      <td>358500.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-122.24</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>1467.0</td>
      <td>190.0</td>
      <td>496.0</td>
      <td>177.0</td>
      <td>7.2574</td>
      <td>352100.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-122.25</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>1274.0</td>
      <td>235.0</td>
      <td>558.0</td>
      <td>219.0</td>
      <td>5.6431</td>
      <td>341300.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-122.25</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>1627.0</td>
      <td>280.0</td>
      <td>565.0</td>
      <td>259.0</td>
      <td>3.8462</td>
      <td>342200.0</td>
      <td>NEAR BAY</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;class 'pandas.core.frame.DataFrame'&gt;
RangeIndex: 20640 entries, 0 to 20639
Data columns (total 10 columns):
longitude             20640 non-null float64
latitude              20640 non-null float64
housing_median_age    20640 non-null float64
total_rooms           20640 non-null float64
total_bedrooms        20433 non-null float64
population            20640 non-null float64
households            20640 non-null float64
median_income         20640 non-null float64
median_house_value    20640 non-null float64
ocean_proximity       20640 non-null object
dtypes: float64(9), object(1)
memory usage: 1.6+ MB
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"ocean_proximity"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;1H OCEAN     9136
INLAND        6551
NEAR OCEAN    2658
NEAR BAY      2290
ISLAND           5
Name: ocean_proximity, dtype: int64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>describe<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20433.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-119.569704</td>
      <td>35.631861</td>
      <td>28.639486</td>
      <td>2635.763081</td>
      <td>537.870553</td>
      <td>1425.476744</td>
      <td>499.539680</td>
      <td>3.870671</td>
      <td>206855.816909</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.003532</td>
      <td>2.135952</td>
      <td>12.585558</td>
      <td>2181.615252</td>
      <td>421.385070</td>
      <td>1132.462122</td>
      <td>382.329753</td>
      <td>1.899822</td>
      <td>115395.615874</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-124.350000</td>
      <td>32.540000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>1.000000</td>
      <td>0.499900</td>
      <td>14999.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>-121.800000</td>
      <td>33.930000</td>
      <td>18.000000</td>
      <td>1447.750000</td>
      <td>296.000000</td>
      <td>787.000000</td>
      <td>280.000000</td>
      <td>2.563400</td>
      <td>119600.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>-118.490000</td>
      <td>34.260000</td>
      <td>29.000000</td>
      <td>2127.000000</td>
      <td>435.000000</td>
      <td>1166.000000</td>
      <td>409.000000</td>
      <td>3.534800</td>
      <td>179700.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>-118.010000</td>
      <td>37.710000</td>
      <td>37.000000</td>
      <td>3148.000000</td>
      <td>647.000000</td>
      <td>1725.000000</td>
      <td>605.000000</td>
      <td>4.743250</td>
      <td>264725.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>-114.310000</td>
      <td>41.950000</td>
      <td>52.000000</td>
      <td>39320.000000</td>
      <td>6445.000000</td>
      <td>35682.000000</td>
      <td>6082.000000</td>
      <td>15.000100</td>
      <td>500001.000000</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token operator">%</span>matplotlib inline
<span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>pyplot <span class="token keyword">as</span> plt

housing<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">,</span><span class="token number">15</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"attribute_histogram_plots"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure attribute_histogram_plots
</code></pre>
<p><img src="output_13_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># to make this notebook's output identical at every run</span>
np<span class="token punctuation">.</span>random<span class="token punctuation">.</span>seed<span class="token punctuation">(</span><span class="token number">42</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> numpy <span class="token keyword">as</span> np

<span class="token comment"># For illustration only. Sklearn has train_test_split()</span>
<span class="token keyword">def</span> <span class="token function">split_train_test</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> test_ratio<span class="token punctuation">)</span><span class="token punctuation">:</span>
    shuffled_indices <span class="token operator">=</span> np<span class="token punctuation">.</span>random<span class="token punctuation">.</span>permutation<span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">)</span>
    test_set_size <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span> <span class="token operator">*</span> test_ratio<span class="token punctuation">)</span>
    test_indices <span class="token operator">=</span> shuffled_indices<span class="token punctuation">[</span><span class="token punctuation">:</span>test_set_size<span class="token punctuation">]</span>
    train_indices <span class="token operator">=</span> shuffled_indices<span class="token punctuation">[</span>test_set_size<span class="token punctuation">:</span><span class="token punctuation">]</span>
    <span class="token keyword">return</span> data<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span>train_indices<span class="token punctuation">]</span><span class="token punctuation">,</span> data<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span>test_indices<span class="token punctuation">]</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> split_train_test<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> <span class="token number">0.2</span><span class="token punctuation">)</span>
<span class="token keyword">print</span><span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>train_set<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token string">"train +"</span><span class="token punctuation">,</span> <span class="token builtin">len</span><span class="token punctuation">(</span>test_set<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token string">"test"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>16512 train + 4128 test
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> zlib <span class="token keyword">import</span> crc32

<span class="token keyword">def</span> <span class="token function">test_set_check</span><span class="token punctuation">(</span>identifier<span class="token punctuation">,</span> test_ratio<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> crc32<span class="token punctuation">(</span>np<span class="token punctuation">.</span>int64<span class="token punctuation">(</span>identifier<span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token operator">&amp;</span> <span class="token number">0xffffffff</span> <span class="token operator">&lt;</span> test_ratio <span class="token operator">*</span> <span class="token number">2</span><span class="token operator">**</span><span class="token number">32</span>

<span class="token keyword">def</span> <span class="token function">split_train_test_by_id</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> test_ratio<span class="token punctuation">,</span> id_column<span class="token punctuation">)</span><span class="token punctuation">:</span>
    ids <span class="token operator">=</span> data<span class="token punctuation">[</span>id_column<span class="token punctuation">]</span>
    in_test_set <span class="token operator">=</span> ids<span class="token punctuation">.</span><span class="token builtin">apply</span><span class="token punctuation">(</span><span class="token keyword">lambda</span> id_<span class="token punctuation">:</span> test_set_check<span class="token punctuation">(</span>id_<span class="token punctuation">,</span> test_ratio<span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> data<span class="token punctuation">.</span>loc<span class="token punctuation">[</span><span class="token operator">~</span>in_test_set<span class="token punctuation">]</span><span class="token punctuation">,</span> data<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>in_test_set<span class="token punctuation">]</span>
</code></pre>
<p>The implementation of <code>test_set_check()</code> above works fine in both Python 2 and Python 3. In earlier releases, the following implementation was proposed, which supported any hash function, but was much slower and did not support Python 2:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> hashlib

<span class="token keyword">def</span> <span class="token function">test_set_check</span><span class="token punctuation">(</span>identifier<span class="token punctuation">,</span> test_ratio<span class="token punctuation">,</span> <span class="token builtin">hash</span><span class="token operator">=</span>hashlib<span class="token punctuation">.</span>md5<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> <span class="token builtin">hash</span><span class="token punctuation">(</span>np<span class="token punctuation">.</span>int64<span class="token punctuation">(</span>identifier<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>digest<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">&lt;</span> <span class="token number">256</span> <span class="token operator">*</span> test_ratio
</code></pre>
<p>If you want an implementation that supports any hash function and is compatible with both Python 2 and Python 3, here is one:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">test_set_check</span><span class="token punctuation">(</span>identifier<span class="token punctuation">,</span> test_ratio<span class="token punctuation">,</span> <span class="token builtin">hash</span><span class="token operator">=</span>hashlib<span class="token punctuation">.</span>md5<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> <span class="token builtin">bytearray</span><span class="token punctuation">(</span><span class="token builtin">hash</span><span class="token punctuation">(</span>np<span class="token punctuation">.</span>int64<span class="token punctuation">(</span>identifier<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>digest<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">&lt;</span> <span class="token number">256</span> <span class="token operator">*</span> test_ratio
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_with_id <span class="token operator">=</span> housing<span class="token punctuation">.</span>reset_index<span class="token punctuation">(</span><span class="token punctuation">)</span>   <span class="token comment"># adds an `index` column</span>
train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> split_train_test_by_id<span class="token punctuation">(</span>housing_with_id<span class="token punctuation">,</span> <span class="token number">0.2</span><span class="token punctuation">,</span> <span class="token string">"index"</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_with_id<span class="token punctuation">[</span><span class="token string">"id"</span><span class="token punctuation">]</span> <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"longitude"</span><span class="token punctuation">]</span> <span class="token operator">*</span> <span class="token number">1000</span> <span class="token operator">+</span> housing<span class="token punctuation">[</span><span class="token string">"latitude"</span><span class="token punctuation">]</span>
train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> split_train_test_by_id<span class="token punctuation">(</span>housing_with_id<span class="token punctuation">,</span> <span class="token number">0.2</span><span class="token punctuation">,</span> <span class="token string">"id"</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">test_set<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>index</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>ocean_proximity</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>-122.26</td>
      <td>37.84</td>
      <td>42.0</td>
      <td>2555.0</td>
      <td>665.0</td>
      <td>1206.0</td>
      <td>595.0</td>
      <td>2.0804</td>
      <td>226700.0</td>
      <td>NEAR BAY</td>
      <td>-122222.16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>-122.26</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>2202.0</td>
      <td>434.0</td>
      <td>910.0</td>
      <td>402.0</td>
      <td>3.2031</td>
      <td>281500.0</td>
      <td>NEAR BAY</td>
      <td>-122222.15</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>-122.26</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>3503.0</td>
      <td>752.0</td>
      <td>1504.0</td>
      <td>734.0</td>
      <td>3.2705</td>
      <td>241800.0</td>
      <td>NEAR BAY</td>
      <td>-122222.15</td>
    </tr>
    <tr>
      <th>12</th>
      <td>12</td>
      <td>-122.26</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>2491.0</td>
      <td>474.0</td>
      <td>1098.0</td>
      <td>468.0</td>
      <td>3.0750</td>
      <td>213500.0</td>
      <td>NEAR BAY</td>
      <td>-122222.15</td>
    </tr>
    <tr>
      <th>13</th>
      <td>13</td>
      <td>-122.26</td>
      <td>37.84</td>
      <td>52.0</td>
      <td>696.0</td>
      <td>191.0</td>
      <td>345.0</td>
      <td>174.0</td>
      <td>2.6736</td>
      <td>191300.0</td>
      <td>NEAR BAY</td>
      <td>-122222.16</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> train_test_split

train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> train_test_split<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> test_size<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">test_set<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20046</th>
      <td>-119.01</td>
      <td>36.06</td>
      <td>25.0</td>
      <td>1505.0</td>
      <td>NaN</td>
      <td>1392.0</td>
      <td>359.0</td>
      <td>1.6812</td>
      <td>47700.0</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>3024</th>
      <td>-119.46</td>
      <td>35.14</td>
      <td>30.0</td>
      <td>2943.0</td>
      <td>NaN</td>
      <td>1565.0</td>
      <td>584.0</td>
      <td>2.5313</td>
      <td>45800.0</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>15663</th>
      <td>-122.44</td>
      <td>37.80</td>
      <td>52.0</td>
      <td>3830.0</td>
      <td>NaN</td>
      <td>1310.0</td>
      <td>963.0</td>
      <td>3.4801</td>
      <td>500001.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>20484</th>
      <td>-118.72</td>
      <td>34.28</td>
      <td>17.0</td>
      <td>3051.0</td>
      <td>NaN</td>
      <td>1705.0</td>
      <td>495.0</td>
      <td>5.7376</td>
      <td>218600.0</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>9814</th>
      <td>-121.93</td>
      <td>36.62</td>
      <td>34.0</td>
      <td>2351.0</td>
      <td>NaN</td>
      <td>1063.0</td>
      <td>428.0</td>
      <td>3.7250</td>
      <td>278000.0</td>
      <td>NEAR OCEAN</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"median_income"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>hist<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;matplotlib.axes._subplots.AxesSubplot at 0x7f6db0132fd0&gt;
</code></pre>
<p><img src="output_27_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># Divide by 1.5 to limit the number of income categories</span>
housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span> <span class="token operator">=</span> np<span class="token punctuation">.</span>ceil<span class="token punctuation">(</span>housing<span class="token punctuation">[</span><span class="token string">"median_income"</span><span class="token punctuation">]</span> <span class="token operator">/</span> <span class="token number">1.5</span><span class="token punctuation">)</span>
<span class="token comment"># Label those above 5 as 5</span>
housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>where<span class="token punctuation">(</span>housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span> <span class="token operator">&lt;</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">5.0</span><span class="token punctuation">,</span> inplace<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>3.0    7236
2.0    6581
4.0    3639
5.0    2362
1.0     822
Name: income_cat, dtype: int64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>hist<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;matplotlib.axes._subplots.AxesSubplot at 0x7f6db00c60d0&gt;
</code></pre>
<p><img src="output_30_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> StratifiedShuffleSplit

split <span class="token operator">=</span> StratifiedShuffleSplit<span class="token punctuation">(</span>n_splits<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">,</span> test_size<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
<span class="token keyword">for</span> train_index<span class="token punctuation">,</span> test_index <span class="token keyword">in</span> split<span class="token punctuation">.</span>split<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    strat_train_set <span class="token operator">=</span> housing<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>train_index<span class="token punctuation">]</span>
    strat_test_set <span class="token operator">=</span> housing<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>test_index<span class="token punctuation">]</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">strat_test_set<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>strat_test_set<span class="token punctuation">)</span>
</code></pre>
<pre><code>3.0    0.350533
2.0    0.318798
4.0    0.176357
5.0    0.114583
1.0    0.039729
Name: income_cat, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>housing<span class="token punctuation">)</span>
</code></pre>
<pre><code>3.0    0.350581
2.0    0.318847
4.0    0.176308
5.0    0.114438
1.0    0.039826
Name: income_cat, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">income_cat_proportions</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> data<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span>

train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> train_test_split<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> test_size<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>

compare_props <span class="token operator">=</span> pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token string">"Overall"</span><span class="token punctuation">:</span> income_cat_proportions<span class="token punctuation">(</span>housing<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token string">"Stratified"</span><span class="token punctuation">:</span> income_cat_proportions<span class="token punctuation">(</span>strat_test_set<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token string">"Random"</span><span class="token punctuation">:</span> income_cat_proportions<span class="token punctuation">(</span>test_set<span class="token punctuation">)</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span>sort_index<span class="token punctuation">(</span><span class="token punctuation">)</span>
compare_props<span class="token punctuation">[</span><span class="token string">"Rand. %error"</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">100</span> <span class="token operator">*</span> compare_props<span class="token punctuation">[</span><span class="token string">"Random"</span><span class="token punctuation">]</span> <span class="token operator">/</span> compare_props<span class="token punctuation">[</span><span class="token string">"Overall"</span><span class="token punctuation">]</span> <span class="token operator">-</span> <span class="token number">100</span>
compare_props<span class="token punctuation">[</span><span class="token string">"Strat. %error"</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">100</span> <span class="token operator">*</span> compare_props<span class="token punctuation">[</span><span class="token string">"Stratified"</span><span class="token punctuation">]</span> <span class="token operator">/</span> compare_props<span class="token punctuation">[</span><span class="token string">"Overall"</span><span class="token punctuation">]</span> <span class="token operator">-</span> <span class="token number">100</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">compare_props
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>Overall</th>
      <th>Random</th>
      <th>Stratified</th>
      <th>Rand. %error</th>
      <th>Strat. %error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1.0</th>
      <td>0.039826</td>
      <td>0.040213</td>
      <td>0.039729</td>
      <td>0.973236</td>
      <td>-0.243309</td>
    </tr>
    <tr>
      <th>2.0</th>
      <td>0.318847</td>
      <td>0.324370</td>
      <td>0.318798</td>
      <td>1.732260</td>
      <td>-0.015195</td>
    </tr>
    <tr>
      <th>3.0</th>
      <td>0.350581</td>
      <td>0.358527</td>
      <td>0.350533</td>
      <td>2.266446</td>
      <td>-0.013820</td>
    </tr>
    <tr>
      <th>4.0</th>
      <td>0.176308</td>
      <td>0.167393</td>
      <td>0.176357</td>
      <td>-5.056334</td>
      <td>0.027480</td>
    </tr>
    <tr>
      <th>5.0</th>
      <td>0.114438</td>
      <td>0.109496</td>
      <td>0.114583</td>
      <td>-4.318374</td>
      <td>0.127011</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">for</span> set_ <span class="token keyword">in</span> <span class="token punctuation">(</span>strat_train_set<span class="token punctuation">,</span> strat_test_set<span class="token punctuation">)</span><span class="token punctuation">:</span>
    set_<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"income_cat"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">,</span> inplace<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
</code></pre>
<h1 id="discover-and-visualize-the-data-to-gain-insights">Discover and visualize the data to gain insights</h1>
<pre class=" language-python"><code class="prism  language-python">housing <span class="token operator">=</span> strat_train_set<span class="token punctuation">.</span>copy<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"bad_visualization_plot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure bad_visualization_plot
</code></pre>
<p><img src="output_39_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.1</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"better_visualization_plot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure better_visualization_plot
</code></pre>
<p><img src="output_40_1.png" alt="png"></p>
<p>The argument <code>sharex=False</code> fixes a display bug (the x-axis values and legend were not displayed). This is a temporary fix (see: <a href="https://github.com/pandas-dev/pandas/issues/10611">https://github.com/pandas-dev/pandas/issues/10611</a>). Thanks to Wilmer Arellano for pointing it out.</p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.4</span><span class="token punctuation">,</span>
    s<span class="token operator">=</span>housing<span class="token punctuation">[</span><span class="token string">"population"</span><span class="token punctuation">]</span><span class="token operator">/</span><span class="token number">100</span><span class="token punctuation">,</span> label<span class="token operator">=</span><span class="token string">"population"</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span><span class="token number">7</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    c<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> cmap<span class="token operator">=</span>plt<span class="token punctuation">.</span>get_cmap<span class="token punctuation">(</span><span class="token string">"jet"</span><span class="token punctuation">)</span><span class="token punctuation">,</span> colorbar<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span>
    sharex<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>legend<span class="token punctuation">(</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"housing_prices_scatterplot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure housing_prices_scatterplot
</code></pre>
<p><img src="output_42_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>image <span class="token keyword">as</span> mpimg
california_img<span class="token operator">=</span>mpimg<span class="token punctuation">.</span>imread<span class="token punctuation">(</span>PROJECT_ROOT_DIR <span class="token operator">+</span> <span class="token string">'/images/end_to_end_project/california.png'</span><span class="token punctuation">)</span>
ax <span class="token operator">=</span> housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span><span class="token number">7</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                       s<span class="token operator">=</span>housing<span class="token punctuation">[</span><span class="token string">'population'</span><span class="token punctuation">]</span><span class="token operator">/</span><span class="token number">100</span><span class="token punctuation">,</span> label<span class="token operator">=</span><span class="token string">"Population"</span><span class="token punctuation">,</span>
                       c<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> cmap<span class="token operator">=</span>plt<span class="token punctuation">.</span>get_cmap<span class="token punctuation">(</span><span class="token string">"jet"</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                       colorbar<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.4</span><span class="token punctuation">,</span>
                      <span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>imshow<span class="token punctuation">(</span>california_img<span class="token punctuation">,</span> extent<span class="token operator">=</span><span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">124.55</span><span class="token punctuation">,</span> <span class="token operator">-</span><span class="token number">113.80</span><span class="token punctuation">,</span> <span class="token number">32.45</span><span class="token punctuation">,</span> <span class="token number">42.05</span><span class="token punctuation">]</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.5</span><span class="token punctuation">,</span>
           cmap<span class="token operator">=</span>plt<span class="token punctuation">.</span>get_cmap<span class="token punctuation">(</span><span class="token string">"jet"</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>ylabel<span class="token punctuation">(</span><span class="token string">"Latitude"</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>xlabel<span class="token punctuation">(</span><span class="token string">"Longitude"</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>

prices <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span>
tick_values <span class="token operator">=</span> np<span class="token punctuation">.</span>linspace<span class="token punctuation">(</span>prices<span class="token punctuation">.</span><span class="token builtin">min</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> prices<span class="token punctuation">.</span><span class="token builtin">max</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token number">11</span><span class="token punctuation">)</span>
cbar <span class="token operator">=</span> plt<span class="token punctuation">.</span>colorbar<span class="token punctuation">(</span><span class="token punctuation">)</span>
cbar<span class="token punctuation">.</span>ax<span class="token punctuation">.</span>set_yticklabels<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token string">"$%dk"</span><span class="token operator">%</span><span class="token punctuation">(</span><span class="token builtin">round</span><span class="token punctuation">(</span>v<span class="token operator">/</span><span class="token number">1000</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token keyword">for</span> v <span class="token keyword">in</span> tick_values<span class="token punctuation">]</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>
cbar<span class="token punctuation">.</span>set_label<span class="token punctuation">(</span><span class="token string">'Median House Value'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">)</span>

plt<span class="token punctuation">.</span>legend<span class="token punctuation">(</span>fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"california_housing_prices_plot"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure california_housing_prices_plot
</code></pre>
<p><img src="output_43_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">corr_matrix <span class="token operator">=</span> housing<span class="token punctuation">.</span>corr<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">corr_matrix<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>sort_values<span class="token punctuation">(</span>ascending<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>median_house_value    1.000000
median_income         0.687160
total_rooms           0.135097
housing_median_age    0.114110
households            0.064506
total_bedrooms        0.047689
population           -0.026920
longitude            -0.047432
latitude             -0.142724
Name: median_house_value, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># from pandas.tools.plotting import scatter_matrix # For older versions of Pandas</span>
<span class="token keyword">from</span> pandas<span class="token punctuation">.</span>plotting <span class="token keyword">import</span> scatter_matrix

attributes <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> <span class="token string">"median_income"</span><span class="token punctuation">,</span> <span class="token string">"total_rooms"</span><span class="token punctuation">,</span>
              <span class="token string">"housing_median_age"</span><span class="token punctuation">]</span>
scatter_matrix<span class="token punctuation">(</span>housing<span class="token punctuation">[</span>attributes<span class="token punctuation">]</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">12</span><span class="token punctuation">,</span> <span class="token number">8</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"scatter_matrix_plot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure scatter_matrix_plot
</code></pre>
<p><img src="output_46_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"median_income"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span>
             alpha<span class="token operator">=</span><span class="token number">0.1</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>axis<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">16</span><span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">550000</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"income_vs_house_value_scatterplot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure income_vs_house_value_scatterplot
</code></pre>
<p><img src="output_47_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"rooms_per_household"</span><span class="token punctuation">]</span> <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"total_rooms"</span><span class="token punctuation">]</span><span class="token operator">/</span>housing<span class="token punctuation">[</span><span class="token string">"households"</span><span class="token punctuation">]</span>
housing<span class="token punctuation">[</span><span class="token string">"bedrooms_per_room"</span><span class="token punctuation">]</span> <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">]</span><span class="token operator">/</span>housing<span class="token punctuation">[</span><span class="token string">"total_rooms"</span><span class="token punctuation">]</span>
housing<span class="token punctuation">[</span><span class="token string">"population_per_household"</span><span class="token punctuation">]</span><span class="token operator">=</span>housing<span class="token punctuation">[</span><span class="token string">"population"</span><span class="token punctuation">]</span><span class="token operator">/</span>housing<span class="token punctuation">[</span><span class="token string">"households"</span><span class="token punctuation">]</span>
</code></pre>
<p>Note: there was a bug in the previous cell, in the definition of the <code>rooms_per_household</code> attribute. This explains why the correlation value below differs slightly from the value in the book (unless you are reading the latest version).</p>
<pre class=" language-python"><code class="prism  language-python">corr_matrix <span class="token operator">=</span> housing<span class="token punctuation">.</span>corr<span class="token punctuation">(</span><span class="token punctuation">)</span>
corr_matrix<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>sort_values<span class="token punctuation">(</span>ascending<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>median_house_value          1.000000
median_income               0.687160
rooms_per_household         0.146285
total_rooms                 0.135097
housing_median_age          0.114110
households                  0.064506
total_bedrooms              0.047689
population_per_household   -0.021985
population                 -0.026920
longitude                  -0.047432
latitude                   -0.142724
bedrooms_per_room          -0.259984
Name: median_house_value, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"rooms_per_household"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span>
             alpha<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>axis<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">520000</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<p><img src="output_51_0.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>describe<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>rooms_per_household</th>
      <th>bedrooms_per_room</th>
      <th>population_per_household</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16354.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16354.000000</td>
      <td>16512.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-119.575834</td>
      <td>35.639577</td>
      <td>28.653101</td>
      <td>2622.728319</td>
      <td>534.973890</td>
      <td>1419.790819</td>
      <td>497.060380</td>
      <td>3.875589</td>
      <td>206990.920724</td>
      <td>5.440341</td>
      <td>0.212878</td>
      <td>3.096437</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.001860</td>
      <td>2.138058</td>
      <td>12.574726</td>
      <td>2138.458419</td>
      <td>412.699041</td>
      <td>1115.686241</td>
      <td>375.720845</td>
      <td>1.904950</td>
      <td>115703.014830</td>
      <td>2.611712</td>
      <td>0.057379</td>
      <td>11.584826</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-124.350000</td>
      <td>32.540000</td>
      <td>1.000000</td>
      <td>6.000000</td>
      <td>2.000000</td>
      <td>3.000000</td>
      <td>2.000000</td>
      <td>0.499900</td>
      <td>14999.000000</td>
      <td>1.130435</td>
      <td>0.100000</td>
      <td>0.692308</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>-121.800000</td>
      <td>33.940000</td>
      <td>18.000000</td>
      <td>1443.000000</td>
      <td>295.000000</td>
      <td>784.000000</td>
      <td>279.000000</td>
      <td>2.566775</td>
      <td>119800.000000</td>
      <td>4.442040</td>
      <td>0.175304</td>
      <td>2.431287</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>-118.510000</td>
      <td>34.260000</td>
      <td>29.000000</td>
      <td>2119.500000</td>
      <td>433.000000</td>
      <td>1164.000000</td>
      <td>408.000000</td>
      <td>3.540900</td>
      <td>179500.000000</td>
      <td>5.232284</td>
      <td>0.203031</td>
      <td>2.817653</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>-118.010000</td>
      <td>37.720000</td>
      <td>37.000000</td>
      <td>3141.000000</td>
      <td>644.000000</td>
      <td>1719.250000</td>
      <td>602.000000</td>
      <td>4.744475</td>
      <td>263900.000000</td>
      <td>6.056361</td>
      <td>0.239831</td>
      <td>3.281420</td>
    </tr>
    <tr>
      <th>max</th>
      <td>-114.310000</td>
      <td>41.950000</td>
      <td>52.000000</td>
      <td>39320.000000</td>
      <td>6210.000000</td>
      <td>35682.000000</td>
      <td>5358.000000</td>
      <td>15.000100</td>
      <td>500001.000000</td>
      <td>141.909091</td>
      <td>1.000000</td>
      <td>1243.333333</td>
    </tr>
  </tbody>
</table>

<h1 id="prepare-the-data-for-machine-learning-algorithms">Prepare the data for Machine Learning algorithms</h1>
<pre class=" language-python"><code class="prism  language-python">housing <span class="token operator">=</span> strat_train_set<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span> <span class="token comment"># drop labels for training set</span>
housing_labels <span class="token operator">=</span> strat_train_set<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>copy<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">sample_incomplete_rows <span class="token operator">=</span> housing<span class="token punctuation">[</span>housing<span class="token punctuation">.</span>isnull<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token builtin">any</span><span class="token punctuation">(</span>axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">]</span><span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
sample_incomplete_rows
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4629</th>
      <td>-118.30</td>
      <td>34.07</td>
      <td>18.0</td>
      <td>3759.0</td>
      <td>NaN</td>
      <td>3296.0</td>
      <td>1462.0</td>
      <td>2.2708</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>6068</th>
      <td>-117.86</td>
      <td>34.01</td>
      <td>16.0</td>
      <td>4632.0</td>
      <td>NaN</td>
      <td>3038.0</td>
      <td>727.0</td>
      <td>5.1762</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>17923</th>
      <td>-121.97</td>
      <td>37.35</td>
      <td>30.0</td>
      <td>1955.0</td>
      <td>NaN</td>
      <td>999.0</td>
      <td>386.0</td>
      <td>4.6328</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>13656</th>
      <td>-117.30</td>
      <td>34.05</td>
      <td>6.0</td>
      <td>2155.0</td>
      <td>NaN</td>
      <td>1039.0</td>
      <td>391.0</td>
      <td>1.6675</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>19252</th>
      <td>-122.79</td>
      <td>38.48</td>
      <td>7.0</td>
      <td>6837.0</td>
      <td>NaN</td>
      <td>3468.0</td>
      <td>1405.0</td>
      <td>3.1662</td>
      <td>&lt;1H OCEAN</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">sample_incomplete_rows<span class="token punctuation">.</span>dropna<span class="token punctuation">(</span>subset<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">]</span><span class="token punctuation">)</span>    <span class="token comment"># option 1</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">sample_incomplete_rows<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span>       <span class="token comment"># option 2</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4629</th>
      <td>-118.30</td>
      <td>34.07</td>
      <td>18.0</td>
      <td>3759.0</td>
      <td>3296.0</td>
      <td>1462.0</td>
      <td>2.2708</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>6068</th>
      <td>-117.86</td>
      <td>34.01</td>
      <td>16.0</td>
      <td>4632.0</td>
      <td>3038.0</td>
      <td>727.0</td>
      <td>5.1762</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>17923</th>
      <td>-121.97</td>
      <td>37.35</td>
      <td>30.0</td>
      <td>1955.0</td>
      <td>999.0</td>
      <td>386.0</td>
      <td>4.6328</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>13656</th>
      <td>-117.30</td>
      <td>34.05</td>
      <td>6.0</td>
      <td>2155.0</td>
      <td>1039.0</td>
      <td>391.0</td>
      <td>1.6675</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>19252</th>
      <td>-122.79</td>
      <td>38.48</td>
      <td>7.0</td>
      <td>6837.0</td>
      <td>3468.0</td>
      <td>1405.0</td>
      <td>3.1662</td>
      <td>&lt;1H OCEAN</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">median <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>median<span class="token punctuation">(</span><span class="token punctuation">)</span>
sample_incomplete_rows<span class="token punctuation">[</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fillna<span class="token punctuation">(</span>median<span class="token punctuation">,</span> inplace<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span> <span class="token comment"># option 3</span>
sample_incomplete_rows
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4629</th>
      <td>-118.30</td>
      <td>34.07</td>
      <td>18.0</td>
      <td>3759.0</td>
      <td>433.0</td>
      <td>3296.0</td>
      <td>1462.0</td>
      <td>2.2708</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>6068</th>
      <td>-117.86</td>
      <td>34.01</td>
      <td>16.0</td>
      <td>4632.0</td>
      <td>433.0</td>
      <td>3038.0</td>
      <td>727.0</td>
      <td>5.1762</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>17923</th>
      <td>-121.97</td>
      <td>37.35</td>
      <td>30.0</td>
      <td>1955.0</td>
      <td>433.0</td>
      <td>999.0</td>
      <td>386.0</td>
      <td>4.6328</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>13656</th>
      <td>-117.30</td>
      <td>34.05</td>
      <td>6.0</td>
      <td>2155.0</td>
      <td>433.0</td>
      <td>1039.0</td>
      <td>391.0</td>
      <td>1.6675</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>19252</th>
      <td>-122.79</td>
      <td>38.48</td>
      <td>7.0</td>
      <td>6837.0</td>
      <td>433.0</td>
      <td>3468.0</td>
      <td>1405.0</td>
      <td>3.1662</td>
      <td>&lt;1H OCEAN</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>preprocessing <span class="token keyword">import</span> Imputer

imputer <span class="token operator">=</span> Imputer<span class="token punctuation">(</span>strategy<span class="token operator">=</span><span class="token string">"median"</span><span class="token punctuation">)</span>
</code></pre>
<p>Remove the text attribute because median can only be calculated on numerical attributes:</p>
<pre class=" language-python"><code class="prism  language-python">housing_num <span class="token operator">=</span> housing<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">'ocean_proximity'</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span>
<span class="token comment"># alternatively: housing_num = housing.select_dtypes(include=[np.number])</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">imputer<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_num<span class="token punctuation">)</span>
</code></pre>
<pre><code>Imputer(axis=0, copy=True, missing_values='NaN', strategy=u'median',
    verbose=0)
</code></pre>
<pre class=" language-python"><code class="prism  language-python">imputer<span class="token punctuation">.</span>statistics_
</code></pre>
<pre><code>array([ -118.51  ,    34.26  ,    29.    ,  2119.5   ,   433.    ,
        1164.    ,   408.    ,     3.5409])
</code></pre>
<p>Check that this is the same as manually computing the median of each attribute:</p>
<pre class=" language-python"><code class="prism  language-python">housing_num<span class="token punctuation">.</span>median<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>values
</code></pre>
<pre><code>array([ -118.51  ,    34.26  ,    29.    ,  2119.5   ,   433.    ,
        1164.    ,   408.    ,     3.5409])
</code></pre>
<p>Transform the training set:</p>
<pre class=" language-python"><code class="prism  language-python">X <span class="token operator">=</span> imputer<span class="token punctuation">.</span>transform<span class="token punctuation">(</span>housing_num<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_tr <span class="token operator">=</span> pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">(</span>X<span class="token punctuation">,</span> columns<span class="token operator">=</span>housing_num<span class="token punctuation">.</span>columns<span class="token punctuation">,</span>
                          index <span class="token operator">=</span> <span class="token builtin">list</span><span class="token punctuation">(</span>housing<span class="token punctuation">.</span>index<span class="token punctuation">.</span>values<span class="token punctuation">)</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_tr<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>sample_incomplete_rows<span class="token punctuation">.</span>index<span class="token punctuation">.</span>values<span class="token punctuation">]</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4629</th>
      <td>-118.30</td>
      <td>34.07</td>
      <td>18.0</td>
      <td>3759.0</td>
      <td>433.0</td>
      <td>3296.0</td>
      <td>1462.0</td>
      <td>2.2708</td>
    </tr>
    <tr>
      <th>6068</th>
      <td>-117.86</td>
      <td>34.01</td>
      <td>16.0</td>
      <td>4632.0</td>
      <td>433.0</td>
      <td>3038.0</td>
      <td>727.0</td>
      <td>5.1762</td>
    </tr>
    <tr>
      <th>17923</th>
      <td>-121.97</td>
      <td>37.35</td>
      <td>30.0</td>
      <td>1955.0</td>
      <td>433.0</td>
      <td>999.0</td>
      <td>386.0</td>
      <td>4.6328</td>
    </tr>
    <tr>
      <th>13656</th>
      <td>-117.30</td>
      <td>34.05</td>
      <td>6.0</td>
      <td>2155.0</td>
      <td>433.0</td>
      <td>1039.0</td>
      <td>391.0</td>
      <td>1.6675</td>
    </tr>
    <tr>
      <th>19252</th>
      <td>-122.79</td>
      <td>38.48</td>
      <td>7.0</td>
      <td>6837.0</td>
      <td>433.0</td>
      <td>3468.0</td>
      <td>1405.0</td>
      <td>3.1662</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">imputer<span class="token punctuation">.</span>strategy
</code></pre>
<pre><code>u'median'
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_tr <span class="token operator">=</span> pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">(</span>X<span class="token punctuation">,</span> columns<span class="token operator">=</span>housing_num<span class="token punctuation">.</span>columns<span class="token punctuation">)</span>
housing_tr<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-121.89</td>
      <td>37.29</td>
      <td>38.0</td>
      <td>1568.0</td>
      <td>351.0</td>
      <td>710.0</td>
      <td>339.0</td>
      <td>2.7042</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-121.93</td>
      <td>37.05</td>
      <td>14.0</td>
      <td>679.0</td>
      <td>108.0</td>
      <td>306.0</td>
      <td>113.0</td>
      <td>6.4214</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-117.20</td>
      <td>32.77</td>
      <td>31.0</td>
      <td>1952.0</td>
      <td>471.0</td>
      <td>936.0</td>
      <td>462.0</td>
      <td>2.8621</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-119.61</td>
      <td>36.31</td>
      <td>25.0</td>
      <td>1847.0</td>
      <td>371.0</td>
      <td>1460.0</td>
      <td>353.0</td>
      <td>1.8839</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-118.59</td>
      <td>34.23</td>
      <td>17.0</td>
      <td>6592.0</td>
      <td>1525.0</td>
      <td>4459.0</td>
      <td>1463.0</td>
      <td>3.0347</td>
    </tr>
  </tbody>
</table>

<p>Now let’s preprocess the categorical input feature, <code>ocean_proximity</code>:</p>
<pre class=" language-python"><code class="prism  language-python">housing_cat <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">'ocean_proximity'</span><span class="token punctuation">]</span>
housing_cat<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>17606     &lt;1H OCEAN
18632     &lt;1H OCEAN
14650    NEAR OCEAN
3230         INLAND
3555      &lt;1H OCEAN
19480        INLAND
8879      &lt;1H OCEAN
13685        INLAND
4937      &lt;1H OCEAN
4861      &lt;1H OCEAN
Name: ocean_proximity, dtype: object
</code></pre>
<p>We can use Pandas’ <code>factorize()</code> method to convert this string categorical feature to an integer categorical feature, which will be easier for Machine Learning algorithms to handle:</p>
<pre class=" language-python"><code class="prism  language-python">housing_cat_encoded<span class="token punctuation">,</span> housing_categories <span class="token operator">=</span> housing_cat<span class="token punctuation">.</span>factorize<span class="token punctuation">(</span><span class="token punctuation">)</span>
housing_cat_encoded<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token number">10</span><span class="token punctuation">]</span>
</code></pre>
<pre><code>array([0, 0, 1, 2, 0, 2, 0, 2, 0, 0])
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_categories
</code></pre>
<pre><code>Index([u'&lt;1H OCEAN', u'NEAR OCEAN', u'INLAND', u'NEAR BAY', u'ISLAND'], dtype='object')
</code></pre>
<p><strong>Warning</strong>: earlier versions of the book used the <code>LabelEncoder</code> class instead of Pandas’ <code>factorize()</code> method. This was incorrect: indeed, as its name suggests, the <code>LabelEncoder</code> class was designed for labels, not for input features. The code worked because we were handling a single categorical input feature, but it would break if you passed multiple categorical input features.</p>
<p>We can convert each categorical value to a one-hot vector using a <code>OneHotEncoder</code>:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>preprocessing <span class="token keyword">import</span> OneHotEncoder

encoder <span class="token operator">=</span> OneHotEncoder<span class="token punctuation">(</span><span class="token punctuation">)</span>
housing_cat_1hot <span class="token operator">=</span> encoder<span class="token punctuation">.</span>fit_transform<span class="token punctuation">(</span>housing_cat_encoded<span class="token punctuation">.</span>reshape<span class="token punctuation">(</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">,</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
housing_cat_1hot
</code></pre>
<pre><code>&lt;16512x5 sparse matrix of type '&lt;type 'numpy.float64'&gt;'
	with 16512 stored elements in Compressed Sparse Row format&gt;
</code></pre>
<p>The <code>OneHotEncoder</code> returns a sparse array by default, but we can convert it to a dense array if needed:</p>
<pre class=" language-python"><code class="prism  language-python">housing_cat_1hot<span class="token punctuation">.</span>toarray<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>array([[ 1.,  0.,  0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  0.,  0.,  0.],
       ..., 
       [ 0.,  0.,  1.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.]])
</code></pre>
<p><strong>Warning</strong>: earlier versions of the book used the <code>LabelBinarizer</code> class at this point. Again, this was incorrect: just like the <code>LabelEncoder</code> class, the <code>LabelBinarizer</code> class was designed to preprocess labels, not input features. A better solution is to use Scikit-Learn’s upcoming <code>CategoricalEncoder</code> class: it will soon be added to Scikit-Learn, and in the meantime you can use the code below (copied from <a href="https://github.com/scikit-learn/scikit-learn/pull/9151">Pull Request #9151</a>).</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># Definition of the CategoricalEncoder class, copied from PR #9151.</span>
<span class="token comment"># Just run this cell, or copy it to your code, do not try to understand it (yet).</span>

<span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>base <span class="token keyword">import</span> BaseEstimator<span class="token punctuation">,</span> TransformerMixin
<span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>utils <span class="token keyword">import</span> check_array
<span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>preprocessing <span class="token keyword">import</span> LabelEncoder
<span class="token keyword">from</span> scipy <span class="token keyword">import</span> sparse

<span class="token keyword">class</span> <span class="token class-name">CategoricalEncoder</span><span class="token punctuation">(</span>BaseEstimator<span class="token punctuation">,</span> TransformerMixin<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">"""Encode categorical features as a numeric array.
    The input to this transformer should be a matrix of integers or strings,
    denoting the values taken on by categorical (discrete) features.
    The features can be encoded using a one-hot aka one-of-K scheme
    (``encoding='onehot'``, the default) or converted to ordinal integers
    (``encoding='ordinal'``).
    This encoding is needed for feeding categorical data to many scikit-learn
    estimators, notably linear models and SVMs with the standard kernels.
    Read more in the :ref:`User Guide &lt;preprocessing_categorical_features&gt;`.
    Parameters
    ----------
    encoding : str, 'onehot', 'onehot-dense' or 'ordinal'
        The type of encoding to use (default is 'onehot'):
        - 'onehot': encode the features using a one-hot aka one-of-K scheme
          (or also called 'dummy' encoding). This creates a binary column for
          each category and returns a sparse matrix.
        - 'onehot-dense': the same as 'onehot' but returns a dense array
          instead of a sparse matrix.
        - 'ordinal': encode the features as ordinal integers. This results in
          a single column of integers (0 to n_categories - 1) per feature.
    categories : 'auto' or a list of lists/arrays of values.
        Categories (unique values) per feature:
        - 'auto' : Determine categories automatically from the training data.
        - list : ``categories[i]`` holds the categories expected in the ith
          column. The passed categories are sorted before encoding the data
          (used categories can be found in the ``categories_`` attribute).
    dtype : number type, default np.float64
        Desired dtype of output.
    handle_unknown : 'error' (default) or 'ignore'
        Whether to raise an error or ignore if a unknown categorical feature is
        present during transform (default is to raise). When this is parameter
        is set to 'ignore' and an unknown category is encountered during
        transform, the resulting one-hot encoded columns for this feature
        will be all zeros.
        Ignoring unknown categories is not supported for
        ``encoding='ordinal'``.
    Attributes
    ----------
    categories_ : list of arrays
        The categories of each feature determined during fitting. When
        categories were specified manually, this holds the sorted categories
        (in order corresponding with output of `transform`).
    Examples
    --------
    Given a dataset with three features and two samples, we let the encoder
    find the maximum value per feature and transform the data to a binary
    one-hot encoding.
    &gt;&gt;&gt; from sklearn.preprocessing import CategoricalEncoder
    &gt;&gt;&gt; enc = CategoricalEncoder(handle_unknown='ignore')
    &gt;&gt;&gt; enc.fit([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]])
    ... # doctest: +ELLIPSIS
    CategoricalEncoder(categories='auto', dtype=&lt;... 'numpy.float64'&gt;,
              encoding='onehot', handle_unknown='ignore')
    &gt;&gt;&gt; enc.transform([[0, 1, 1], [1, 0, 4]]).toarray()
    array([[ 1.,  0.,  0.,  1.,  0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.]])
    See also
    --------
    sklearn.preprocessing.OneHotEncoder : performs a one-hot encoding of
      integer ordinal features. The ``OneHotEncoder assumes`` that input
      features take on values in the range ``[0, max(feature)]`` instead of
      using the unique values.
    sklearn.feature_extraction.DictVectorizer : performs a one-hot encoding of
      dictionary items (also handles string-valued features).
    sklearn.feature_extraction.FeatureHasher : performs an approximate one-hot
      encoding of dictionary items or strings.
    """</span>

    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> encoding<span class="token operator">=</span><span class="token string">'onehot'</span><span class="token punctuation">,</span> categories<span class="token operator">=</span><span class="token string">'auto'</span><span class="token punctuation">,</span> dtype<span class="token operator">=</span>np<span class="token punctuation">.</span>float64<span class="token punctuation">,</span>
                 handle_unknown<span class="token operator">=</span><span class="token string">'error'</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        self<span class="token punctuation">.</span>encoding <span class="token operator">=</span> encoding
        self<span class="token punctuation">.</span>categories <span class="token operator">=</span> categories
        self<span class="token punctuation">.</span>dtype <span class="token operator">=</span> dtype
        self<span class="token punctuation">.</span>handle_unknown <span class="token operator">=</span> handle_unknown

    <span class="token keyword">def</span> <span class="token function">fit</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""Fit the CategoricalEncoder to X.
        Parameters
        ----------
        X : array-like, shape [n_samples, n_feature]
            The data to determine the categories of each feature.
        Returns
        -------
        self
        """</span>

        <span class="token keyword">if</span> self<span class="token punctuation">.</span>encoding <span class="token operator">not</span> <span class="token keyword">in</span> <span class="token punctuation">[</span><span class="token string">'onehot'</span><span class="token punctuation">,</span> <span class="token string">'onehot-dense'</span><span class="token punctuation">,</span> <span class="token string">'ordinal'</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
            template <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"encoding should be either 'onehot', 'onehot-dense' "</span>
                        <span class="token string">"or 'ordinal', got %s"</span><span class="token punctuation">)</span>
            <span class="token keyword">raise</span> ValueError<span class="token punctuation">(</span>template <span class="token operator">%</span> self<span class="token punctuation">.</span>handle_unknown<span class="token punctuation">)</span>

        <span class="token keyword">if</span> self<span class="token punctuation">.</span>handle_unknown <span class="token operator">not</span> <span class="token keyword">in</span> <span class="token punctuation">[</span><span class="token string">'error'</span><span class="token punctuation">,</span> <span class="token string">'ignore'</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
            template <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"handle_unknown should be either 'error' or "</span>
                        <span class="token string">"'ignore', got %s"</span><span class="token punctuation">)</span>
            <span class="token keyword">raise</span> ValueError<span class="token punctuation">(</span>template <span class="token operator">%</span> self<span class="token punctuation">.</span>handle_unknown<span class="token punctuation">)</span>

        <span class="token keyword">if</span> self<span class="token punctuation">.</span>encoding <span class="token operator">==</span> <span class="token string">'ordinal'</span> <span class="token operator">and</span> self<span class="token punctuation">.</span>handle_unknown <span class="token operator">==</span> <span class="token string">'ignore'</span><span class="token punctuation">:</span>
            <span class="token keyword">raise</span> ValueError<span class="token punctuation">(</span><span class="token string">"handle_unknown='ignore' is not supported for"</span>
                             <span class="token string">" encoding='ordinal'"</span><span class="token punctuation">)</span>

        X <span class="token operator">=</span> check_array<span class="token punctuation">(</span>X<span class="token punctuation">,</span> dtype<span class="token operator">=</span>np<span class="token punctuation">.</span><span class="token builtin">object</span><span class="token punctuation">,</span> accept_sparse<span class="token operator">=</span><span class="token string">'csc'</span><span class="token punctuation">,</span> copy<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
        n_samples<span class="token punctuation">,</span> n_features <span class="token operator">=</span> X<span class="token punctuation">.</span>shape

        self<span class="token punctuation">.</span>_label_encoders_ <span class="token operator">=</span> <span class="token punctuation">[</span>LabelEncoder<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token keyword">for</span> _ <span class="token keyword">in</span> <span class="token builtin">range</span><span class="token punctuation">(</span>n_features<span class="token punctuation">)</span><span class="token punctuation">]</span>

        <span class="token keyword">for</span> i <span class="token keyword">in</span> <span class="token builtin">range</span><span class="token punctuation">(</span>n_features<span class="token punctuation">)</span><span class="token punctuation">:</span>
            le <span class="token operator">=</span> self<span class="token punctuation">.</span>_label_encoders_<span class="token punctuation">[</span>i<span class="token punctuation">]</span>
            Xi <span class="token operator">=</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> i<span class="token punctuation">]</span>
            <span class="token keyword">if</span> self<span class="token punctuation">.</span>categories <span class="token operator">==</span> <span class="token string">'auto'</span><span class="token punctuation">:</span>
                le<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>Xi<span class="token punctuation">)</span>
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                valid_mask <span class="token operator">=</span> np<span class="token punctuation">.</span>in1d<span class="token punctuation">(</span>Xi<span class="token punctuation">,</span> self<span class="token punctuation">.</span>categories<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">)</span>
                <span class="token keyword">if</span> <span class="token operator">not</span> np<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span>valid_mask<span class="token punctuation">)</span><span class="token punctuation">:</span>
                    <span class="token keyword">if</span> self<span class="token punctuation">.</span>handle_unknown <span class="token operator">==</span> <span class="token string">'error'</span><span class="token punctuation">:</span>
                        diff <span class="token operator">=</span> np<span class="token punctuation">.</span>unique<span class="token punctuation">(</span>Xi<span class="token punctuation">[</span><span class="token operator">~</span>valid_mask<span class="token punctuation">]</span><span class="token punctuation">)</span>
                        msg <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"Found unknown categories {0} in column {1}"</span>
                               <span class="token string">" during fit"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>diff<span class="token punctuation">,</span> i<span class="token punctuation">)</span><span class="token punctuation">)</span>
                        <span class="token keyword">raise</span> ValueError<span class="token punctuation">(</span>msg<span class="token punctuation">)</span>
                le<span class="token punctuation">.</span>classes_ <span class="token operator">=</span> np<span class="token punctuation">.</span>array<span class="token punctuation">(</span>np<span class="token punctuation">.</span>sort<span class="token punctuation">(</span>self<span class="token punctuation">.</span>categories<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">)</span>

        self<span class="token punctuation">.</span>categories_ <span class="token operator">=</span> <span class="token punctuation">[</span>le<span class="token punctuation">.</span>classes_ <span class="token keyword">for</span> le <span class="token keyword">in</span> self<span class="token punctuation">.</span>_label_encoders_<span class="token punctuation">]</span>

        <span class="token keyword">return</span> self

    <span class="token keyword">def</span> <span class="token function">transform</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""Transform X using one-hot encoding.
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to encode.
        Returns
        -------
        X_out : sparse matrix or a 2-d array
            Transformed input.
        """</span>
        X <span class="token operator">=</span> check_array<span class="token punctuation">(</span>X<span class="token punctuation">,</span> accept_sparse<span class="token operator">=</span><span class="token string">'csc'</span><span class="token punctuation">,</span> dtype<span class="token operator">=</span>np<span class="token punctuation">.</span><span class="token builtin">object</span><span class="token punctuation">,</span> copy<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
        n_samples<span class="token punctuation">,</span> n_features <span class="token operator">=</span> X<span class="token punctuation">.</span>shape
        X_int <span class="token operator">=</span> np<span class="token punctuation">.</span>zeros_like<span class="token punctuation">(</span>X<span class="token punctuation">,</span> dtype<span class="token operator">=</span>np<span class="token punctuation">.</span><span class="token builtin">int</span><span class="token punctuation">)</span>
        X_mask <span class="token operator">=</span> np<span class="token punctuation">.</span>ones_like<span class="token punctuation">(</span>X<span class="token punctuation">,</span> dtype<span class="token operator">=</span>np<span class="token punctuation">.</span><span class="token builtin">bool</span><span class="token punctuation">)</span>

        <span class="token keyword">for</span> i <span class="token keyword">in</span> <span class="token builtin">range</span><span class="token punctuation">(</span>n_features<span class="token punctuation">)</span><span class="token punctuation">:</span>
            valid_mask <span class="token operator">=</span> np<span class="token punctuation">.</span>in1d<span class="token punctuation">(</span>X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> i<span class="token punctuation">]</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span>categories_<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">)</span>

            <span class="token keyword">if</span> <span class="token operator">not</span> np<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span>valid_mask<span class="token punctuation">)</span><span class="token punctuation">:</span>
                <span class="token keyword">if</span> self<span class="token punctuation">.</span>handle_unknown <span class="token operator">==</span> <span class="token string">'error'</span><span class="token punctuation">:</span>
                    diff <span class="token operator">=</span> np<span class="token punctuation">.</span>unique<span class="token punctuation">(</span>X<span class="token punctuation">[</span><span class="token operator">~</span>valid_mask<span class="token punctuation">,</span> i<span class="token punctuation">]</span><span class="token punctuation">)</span>
                    msg <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"Found unknown categories {0} in column {1}"</span>
                           <span class="token string">" during transform"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>diff<span class="token punctuation">,</span> i<span class="token punctuation">)</span><span class="token punctuation">)</span>
                    <span class="token keyword">raise</span> ValueError<span class="token punctuation">(</span>msg<span class="token punctuation">)</span>
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    <span class="token comment"># Set the problematic rows to an acceptable value and</span>
                    <span class="token comment"># continue `The rows are marked `X_mask` and will be</span>
                    <span class="token comment"># removed later.</span>
                    X_mask<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> i<span class="token punctuation">]</span> <span class="token operator">=</span> valid_mask
                    X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> i<span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token operator">~</span>valid_mask<span class="token punctuation">]</span> <span class="token operator">=</span> self<span class="token punctuation">.</span>categories_<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
            X_int<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> i<span class="token punctuation">]</span> <span class="token operator">=</span> self<span class="token punctuation">.</span>_label_encoders_<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">.</span>transform<span class="token punctuation">(</span>X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> i<span class="token punctuation">]</span><span class="token punctuation">)</span>

        <span class="token keyword">if</span> self<span class="token punctuation">.</span>encoding <span class="token operator">==</span> <span class="token string">'ordinal'</span><span class="token punctuation">:</span>
            <span class="token keyword">return</span> X_int<span class="token punctuation">.</span>astype<span class="token punctuation">(</span>self<span class="token punctuation">.</span>dtype<span class="token punctuation">,</span> copy<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>

        mask <span class="token operator">=</span> X_mask<span class="token punctuation">.</span>ravel<span class="token punctuation">(</span><span class="token punctuation">)</span>
        n_values <span class="token operator">=</span> <span class="token punctuation">[</span>cats<span class="token punctuation">.</span>shape<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token keyword">for</span> cats <span class="token keyword">in</span> self<span class="token punctuation">.</span>categories_<span class="token punctuation">]</span>
        n_values <span class="token operator">=</span> np<span class="token punctuation">.</span>array<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token operator">+</span> n_values<span class="token punctuation">)</span>
        indices <span class="token operator">=</span> np<span class="token punctuation">.</span>cumsum<span class="token punctuation">(</span>n_values<span class="token punctuation">)</span>

        column_indices <span class="token operator">=</span> <span class="token punctuation">(</span>X_int <span class="token operator">+</span> indices<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">.</span>ravel<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">[</span>mask<span class="token punctuation">]</span>
        row_indices <span class="token operator">=</span> np<span class="token punctuation">.</span>repeat<span class="token punctuation">(</span>np<span class="token punctuation">.</span>arange<span class="token punctuation">(</span>n_samples<span class="token punctuation">,</span> dtype<span class="token operator">=</span>np<span class="token punctuation">.</span>int32<span class="token punctuation">)</span><span class="token punctuation">,</span>
                                n_features<span class="token punctuation">)</span><span class="token punctuation">[</span>mask<span class="token punctuation">]</span>
        data <span class="token operator">=</span> np<span class="token punctuation">.</span>ones<span class="token punctuation">(</span>n_samples <span class="token operator">*</span> n_features<span class="token punctuation">)</span><span class="token punctuation">[</span>mask<span class="token punctuation">]</span>

        out <span class="token operator">=</span> sparse<span class="token punctuation">.</span>csc_matrix<span class="token punctuation">(</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> <span class="token punctuation">(</span>row_indices<span class="token punctuation">,</span> column_indices<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                                shape<span class="token operator">=</span><span class="token punctuation">(</span>n_samples<span class="token punctuation">,</span> indices<span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                                dtype<span class="token operator">=</span>self<span class="token punctuation">.</span>dtype<span class="token punctuation">)</span><span class="token punctuation">.</span>tocsr<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> self<span class="token punctuation">.</span>encoding <span class="token operator">==</span> <span class="token string">'onehot-dense'</span><span class="token punctuation">:</span>
            <span class="token keyword">return</span> out<span class="token punctuation">.</span>toarray<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            <span class="token keyword">return</span> out
</code></pre>
<p>The <code>CategoricalEncoder</code> expects a 2D array containing one or more categorical input features. We need to reshape <code>housing_cat</code> to a 2D array:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment">#from sklearn.preprocessing import CategoricalEncoder # in future versions of Scikit-Learn</span>

cat_encoder <span class="token operator">=</span> CategoricalEncoder<span class="token punctuation">(</span><span class="token punctuation">)</span>
housing_cat_reshaped <span class="token operator">=</span> housing_cat<span class="token punctuation">.</span>values<span class="token punctuation">.</span>reshape<span class="token punctuation">(</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">)</span>
housing_cat_1hot <span class="token operator">=</span> cat_encoder<span class="token punctuation">.</span>fit_transform<span class="token punctuation">(</span>housing_cat_reshaped<span class="token punctuation">)</span>
housing_cat_1hot
</code></pre>
<pre><code>&lt;16512x5 sparse matrix of type '&lt;type 'numpy.float64'&gt;'
	with 16512 stored elements in Compressed Sparse Row format&gt;
</code></pre>
<p>The default encoding is one-hot, and it returns a sparse array. You can use <code>toarray()</code> to get a dense array:</p>
<pre class=" language-python"><code class="prism  language-python">housing_cat_1hot<span class="token punctuation">.</span>toarray<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>array([[ 1.,  0.,  0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  1.],
       ..., 
       [ 0.,  1.,  0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.]])
</code></pre>
<p>Alternatively, you can specify the encoding to be <code>"onehot-dense"</code> to get a dense matrix rather than a sparse matrix:</p>
<pre class=" language-python"><code class="prism  language-python">cat_encoder <span class="token operator">=</span> CategoricalEncoder<span class="token punctuation">(</span>encoding<span class="token operator">=</span><span class="token string">"onehot-dense"</span><span class="token punctuation">)</span>
housing_cat_1hot <span class="token operator">=</span> cat_encoder<span class="token punctuation">.</span>fit_transform<span class="token punctuation">(</span>housing_cat_reshaped<span class="token punctuation">)</span>
housing_cat_1hot
</code></pre>
<pre><code>array([[ 1.,  0.,  0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  1.],
       ..., 
       [ 0.,  1.,  0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.]])
</code></pre>
<pre class=" language-python"><code class="prism  language-python">cat_encoder<span class="token punctuation">.</span>categories_
</code></pre>
<pre><code>[array(['&lt;1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'], dtype=object)]
</code></pre>
<p>Let’s create a custom transformer to add extra attributes:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>base <span class="token keyword">import</span> BaseEstimator<span class="token punctuation">,</span> TransformerMixin

<span class="token comment"># column index</span>
rooms_ix<span class="token punctuation">,</span> bedrooms_ix<span class="token punctuation">,</span> population_ix<span class="token punctuation">,</span> household_ix <span class="token operator">=</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">,</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">6</span>

<span class="token keyword">class</span> <span class="token class-name">CombinedAttributesAdder</span><span class="token punctuation">(</span>BaseEstimator<span class="token punctuation">,</span> TransformerMixin<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> add_bedrooms_per_room <span class="token operator">=</span> <span class="token boolean">True</span><span class="token punctuation">)</span><span class="token punctuation">:</span> <span class="token comment"># no *args or **kargs</span>
        self<span class="token punctuation">.</span>add_bedrooms_per_room <span class="token operator">=</span> add_bedrooms_per_room
    <span class="token keyword">def</span> <span class="token function">fit</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> self  <span class="token comment"># nothing else to do</span>
    <span class="token keyword">def</span> <span class="token function">transform</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        rooms_per_household <span class="token operator">=</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> rooms_ix<span class="token punctuation">]</span> <span class="token operator">/</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> household_ix<span class="token punctuation">]</span>
        population_per_household <span class="token operator">=</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> population_ix<span class="token punctuation">]</span> <span class="token operator">/</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> household_ix<span class="token punctuation">]</span>
        <span class="token keyword">if</span> self<span class="token punctuation">.</span>add_bedrooms_per_room<span class="token punctuation">:</span>
            bedrooms_per_room <span class="token operator">=</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> bedrooms_ix<span class="token punctuation">]</span> <span class="token operator">/</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> rooms_ix<span class="token punctuation">]</span>
            <span class="token keyword">return</span> np<span class="token punctuation">.</span>c_<span class="token punctuation">[</span>X<span class="token punctuation">,</span> rooms_per_household<span class="token punctuation">,</span> population_per_household<span class="token punctuation">,</span>
                         bedrooms_per_room<span class="token punctuation">]</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            <span class="token keyword">return</span> np<span class="token punctuation">.</span>c_<span class="token punctuation">[</span>X<span class="token punctuation">,</span> rooms_per_household<span class="token punctuation">,</span> population_per_household<span class="token punctuation">]</span>

attr_adder <span class="token operator">=</span> CombinedAttributesAdder<span class="token punctuation">(</span>add_bedrooms_per_room<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
housing_extra_attribs <span class="token operator">=</span> attr_adder<span class="token punctuation">.</span>transform<span class="token punctuation">(</span>housing<span class="token punctuation">.</span>values<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_extra_attribs <span class="token operator">=</span> pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">(</span>housing_extra_attribs<span class="token punctuation">,</span> columns<span class="token operator">=</span><span class="token builtin">list</span><span class="token punctuation">(</span>housing<span class="token punctuation">.</span>columns<span class="token punctuation">)</span><span class="token operator">+</span><span class="token punctuation">[</span><span class="token string">"rooms_per_household"</span><span class="token punctuation">,</span> <span class="token string">"population_per_household"</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
housing_extra_attribs<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
      <th>rooms_per_household</th>
      <th>population_per_household</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-121.89</td>
      <td>37.29</td>
      <td>38</td>
      <td>1568</td>
      <td>351</td>
      <td>710</td>
      <td>339</td>
      <td>2.7042</td>
      <td>&lt;1H OCEAN</td>
      <td>4.62537</td>
      <td>2.0944</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-121.93</td>
      <td>37.05</td>
      <td>14</td>
      <td>679</td>
      <td>108</td>
      <td>306</td>
      <td>113</td>
      <td>6.4214</td>
      <td>&lt;1H OCEAN</td>
      <td>6.00885</td>
      <td>2.70796</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-117.2</td>
      <td>32.77</td>
      <td>31</td>
      <td>1952</td>
      <td>471</td>
      <td>936</td>
      <td>462</td>
      <td>2.8621</td>
      <td>NEAR OCEAN</td>
      <td>4.22511</td>
      <td>2.02597</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-119.61</td>
      <td>36.31</td>
      <td>25</td>
      <td>1847</td>
      <td>371</td>
      <td>1460</td>
      <td>353</td>
      <td>1.8839</td>
      <td>INLAND</td>
      <td>5.23229</td>
      <td>4.13598</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-118.59</td>
      <td>34.23</td>
      <td>17</td>
      <td>6592</td>
      <td>1525</td>
      <td>4459</td>
      <td>1463</td>
      <td>3.0347</td>
      <td>&lt;1H OCEAN</td>
      <td>4.50581</td>
      <td>3.04785</td>
    </tr>
  </tbody>
</table>

<p>Now let’s build a pipeline for preprocessing the numerical attributes:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>pipeline <span class="token keyword">import</span> Pipeline
<span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>preprocessing <span class="token keyword">import</span> StandardScaler

num_pipeline <span class="token operator">=</span> Pipeline<span class="token punctuation">(</span><span class="token punctuation">[</span>
        <span class="token punctuation">(</span><span class="token string">'imputer'</span><span class="token punctuation">,</span> Imputer<span class="token punctuation">(</span>strategy<span class="token operator">=</span><span class="token string">"median"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">'attribs_adder'</span><span class="token punctuation">,</span> CombinedAttributesAdder<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">'std_scaler'</span><span class="token punctuation">,</span> StandardScaler<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">)</span>

housing_num_tr <span class="token operator">=</span> num_pipeline<span class="token punctuation">.</span>fit_transform<span class="token punctuation">(</span>housing_num<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_num_tr
</code></pre>
<pre><code>array([[-1.15604281,  0.77194962,  0.74333089, ..., -0.31205452,
        -0.08649871,  0.15531753],
       [-1.17602483,  0.6596948 , -1.1653172 , ...,  0.21768338,
        -0.03353391, -0.83628902],
       [ 1.18684903, -1.34218285,  0.18664186, ..., -0.46531516,
        -0.09240499,  0.4222004 ],
       ..., 
       [ 1.58648943, -0.72478134, -1.56295222, ...,  0.3469342 ,
        -0.03055414, -0.52177644],
       [ 0.78221312, -0.85106801,  0.18664186, ...,  0.02499488,
         0.06150916, -0.30340741],
       [-1.43579109,  0.99645926,  1.85670895, ..., -0.22852947,
        -0.09586294,  0.10180567]])
</code></pre>
<p>And a transformer to just select a subset of the Pandas DataFrame columns:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>base <span class="token keyword">import</span> BaseEstimator<span class="token punctuation">,</span> TransformerMixin

<span class="token comment"># Create a class to select numerical or categorical columns </span>
<span class="token comment"># since Scikit-Learn doesn't handle DataFrames yet</span>
<span class="token keyword">class</span> <span class="token class-name">DataFrameSelector</span><span class="token punctuation">(</span>BaseEstimator<span class="token punctuation">,</span> TransformerMixin<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> attribute_names<span class="token punctuation">)</span><span class="token punctuation">:</span>
        self<span class="token punctuation">.</span>attribute_names <span class="token operator">=</span> attribute_names
    <span class="token keyword">def</span> <span class="token function">fit</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> self
    <span class="token keyword">def</span> <span class="token function">transform</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> X<span class="token punctuation">[</span>self<span class="token punctuation">.</span>attribute_names<span class="token punctuation">]</span><span class="token punctuation">.</span>values
</code></pre>
<p>Now let’s join all these components into a big pipeline that will preprocess both the numerical and the categorical features:</p>
<pre class=" language-python"><code class="prism  language-python">num_attribs <span class="token operator">=</span> <span class="token builtin">list</span><span class="token punctuation">(</span>housing_num<span class="token punctuation">)</span>
cat_attribs <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">"ocean_proximity"</span><span class="token punctuation">]</span>

num_pipeline <span class="token operator">=</span> Pipeline<span class="token punctuation">(</span><span class="token punctuation">[</span>
        <span class="token punctuation">(</span><span class="token string">'selector'</span><span class="token punctuation">,</span> DataFrameSelector<span class="token punctuation">(</span>num_attribs<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">'imputer'</span><span class="token punctuation">,</span> Imputer<span class="token punctuation">(</span>strategy<span class="token operator">=</span><span class="token string">"median"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">'attribs_adder'</span><span class="token punctuation">,</span> CombinedAttributesAdder<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">'std_scaler'</span><span class="token punctuation">,</span> StandardScaler<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">)</span>

cat_pipeline <span class="token operator">=</span> Pipeline<span class="token punctuation">(</span><span class="token punctuation">[</span>
        <span class="token punctuation">(</span><span class="token string">'selector'</span><span class="token punctuation">,</span> DataFrameSelector<span class="token punctuation">(</span>cat_attribs<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">'cat_encoder'</span><span class="token punctuation">,</span> CategoricalEncoder<span class="token punctuation">(</span>encoding<span class="token operator">=</span><span class="token string">"onehot-dense"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>pipeline <span class="token keyword">import</span> FeatureUnion

full_pipeline <span class="token operator">=</span> FeatureUnion<span class="token punctuation">(</span>transformer_list<span class="token operator">=</span><span class="token punctuation">[</span>
        <span class="token punctuation">(</span><span class="token string">"num_pipeline"</span><span class="token punctuation">,</span> num_pipeline<span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">"cat_pipeline"</span><span class="token punctuation">,</span> cat_pipeline<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_prepared <span class="token operator">=</span> full_pipeline<span class="token punctuation">.</span>fit_transform<span class="token punctuation">(</span>housing<span class="token punctuation">)</span>
housing_prepared
</code></pre>
<pre><code>array([[-1.15604281,  0.77194962,  0.74333089, ...,  0.        ,
         0.        ,  0.        ],
       [-1.17602483,  0.6596948 , -1.1653172 , ...,  0.        ,
         0.        ,  0.        ],
       [ 1.18684903, -1.34218285,  0.18664186, ...,  0.        ,
         0.        ,  1.        ],
       ..., 
       [ 1.58648943, -0.72478134, -1.56295222, ...,  0.        ,
         0.        ,  0.        ],
       [ 0.78221312, -0.85106801,  0.18664186, ...,  0.        ,
         0.        ,  0.        ],
       [-1.43579109,  0.99645926,  1.85670895, ...,  0.        ,
         1.        ,  0.        ]])
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_prepared<span class="token punctuation">.</span>shape
</code></pre>
<pre><code>(16512, 16)
</code></pre>
<h1 id="select-and-train-a-model">Select and train a model</h1>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>linear_model <span class="token keyword">import</span> LinearRegression

lin_reg <span class="token operator">=</span> LinearRegression<span class="token punctuation">(</span><span class="token punctuation">)</span>
lin_reg<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># let's try the full pipeline on a few training instances</span>
some_data <span class="token operator">=</span> housing<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token number">5</span><span class="token punctuation">]</span>
some_labels <span class="token operator">=</span> housing_labels<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token number">5</span><span class="token punctuation">]</span>
some_data_prepared <span class="token operator">=</span> full_pipeline<span class="token punctuation">.</span>transform<span class="token punctuation">(</span>some_data<span class="token punctuation">)</span>

<span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Predictions:"</span><span class="token punctuation">,</span> lin_reg<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>some_data_prepared<span class="token punctuation">)</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Predictions: [ 210644.60459286  317768.80697211  210956.43331178   59218.98886849
  189747.55849879]
</code></pre>
<p>Compare against the actual values:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Labels:"</span><span class="token punctuation">,</span> <span class="token builtin">list</span><span class="token punctuation">(</span>some_labels<span class="token punctuation">)</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Labels: [286600.0, 340600.0, 196900.0, 46300.0, 254500.0]
</code></pre>
<pre class=" language-python"><code class="prism  language-python">some_data_prepared
</code></pre>
<pre><code>array([[-1.15604281,  0.77194962,  0.74333089, -0.49323393, -0.44543821,
        -0.63621141, -0.42069842, -0.61493744, -0.31205452, -0.08649871,
         0.15531753,  1.        ,  0.        ,  0.        ,  0.        ,
         0.        ],
       [-1.17602483,  0.6596948 , -1.1653172 , -0.90896655, -1.0369278 ,
        -0.99833135, -1.02222705,  1.33645936,  0.21768338, -0.03353391,
        -0.83628902,  1.        ,  0.        ,  0.        ,  0.        ,
         0.        ],
       [ 1.18684903, -1.34218285,  0.18664186, -0.31365989, -0.15334458,
        -0.43363936, -0.0933178 , -0.5320456 , -0.46531516, -0.09240499,
         0.4222004 ,  0.        ,  0.        ,  0.        ,  0.        ,
         1.        ],
       [-0.01706767,  0.31357576, -0.29052016, -0.36276217, -0.39675594,
         0.03604096, -0.38343559, -1.04556555, -0.07966124,  0.08973561,
        -0.19645314,  0.        ,  1.        ,  0.        ,  0.        ,
         0.        ],
       [ 0.49247384, -0.65929936, -0.92673619,  1.85619316,  2.41221109,
         2.72415407,  2.57097492, -0.44143679, -0.35783383, -0.00419445,
         0.2699277 ,  1.        ,  0.        ,  0.        ,  0.        ,
         0.        ]])
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>metrics <span class="token keyword">import</span> mean_squared_error

housing_predictions <span class="token operator">=</span> lin_reg<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">)</span>
lin_mse <span class="token operator">=</span> mean_squared_error<span class="token punctuation">(</span>housing_labels<span class="token punctuation">,</span> housing_predictions<span class="token punctuation">)</span>
lin_rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span>lin_mse<span class="token punctuation">)</span>
lin_rmse
</code></pre>
<pre><code>68628.198198489219
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>metrics <span class="token keyword">import</span> mean_absolute_error

lin_mae <span class="token operator">=</span> mean_absolute_error<span class="token punctuation">(</span>housing_labels<span class="token punctuation">,</span> housing_predictions<span class="token punctuation">)</span>
lin_mae
</code></pre>
<pre><code>49439.895990018973
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>tree <span class="token keyword">import</span> DecisionTreeRegressor

tree_reg <span class="token operator">=</span> DecisionTreeRegressor<span class="token punctuation">(</span>random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
tree_reg<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>DecisionTreeRegressor(criterion='mse', max_depth=None, max_features=None,
           max_leaf_nodes=None, min_impurity_decrease=0.0,
           min_impurity_split=None, min_samples_leaf=1,
           min_samples_split=2, min_weight_fraction_leaf=0.0,
           presort=False, random_state=42, splitter='best')
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_predictions <span class="token operator">=</span> tree_reg<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">)</span>
tree_mse <span class="token operator">=</span> mean_squared_error<span class="token punctuation">(</span>housing_labels<span class="token punctuation">,</span> housing_predictions<span class="token punctuation">)</span>
tree_rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span>tree_mse<span class="token punctuation">)</span>
tree_rmse
</code></pre>
<pre><code>0.0
</code></pre>
<h1 id="fine-tune-your-model">Fine-tune your model</h1>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> cross_val_score

scores <span class="token operator">=</span> cross_val_score<span class="token punctuation">(</span>tree_reg<span class="token punctuation">,</span> housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">,</span>
                         scoring<span class="token operator">=</span><span class="token string">"neg_mean_squared_error"</span><span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">)</span>
tree_rmse_scores <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>scores<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">display_scores</span><span class="token punctuation">(</span>scores<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Scores:"</span><span class="token punctuation">,</span> scores<span class="token punctuation">)</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Mean:"</span><span class="token punctuation">,</span> scores<span class="token punctuation">.</span>mean<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Standard deviation:"</span><span class="token punctuation">,</span> scores<span class="token punctuation">.</span>std<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>

display_scores<span class="token punctuation">(</span>tree_rmse_scores<span class="token punctuation">)</span>
</code></pre>
<pre><code>Scores: [ 70232.0136482   66828.46839892  72444.08721003  70761.50186201
  71125.52697653  75581.29319857  70169.59286164  70055.37863456
  75370.49116773  71222.39081244]
Mean: 71379.0744771
Standard deviation: 2458.31882043
</code></pre>
<pre class=" language-python"><code class="prism  language-python">lin_scores <span class="token operator">=</span> cross_val_score<span class="token punctuation">(</span>lin_reg<span class="token punctuation">,</span> housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">,</span>
                             scoring<span class="token operator">=</span><span class="token string">"neg_mean_squared_error"</span><span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">)</span>
lin_rmse_scores <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>lin_scores<span class="token punctuation">)</span>
display_scores<span class="token punctuation">(</span>lin_rmse_scores<span class="token punctuation">)</span>
</code></pre>
<pre><code>Scores: [ 66782.73843989  66960.118071    70347.95244419  74739.57052552
  68031.13388938  71193.84183426  64969.63056405  68281.61137997
  71552.91566558  67665.10082067]
Mean: 69052.4613635
Standard deviation: 2731.6740018
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>ensemble <span class="token keyword">import</span> RandomForestRegressor

forest_reg <span class="token operator">=</span> RandomForestRegressor<span class="token punctuation">(</span>random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
forest_reg<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
           oob_score=False, random_state=42, verbose=0, warm_start=False)
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_predictions <span class="token operator">=</span> forest_reg<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">)</span>
forest_mse <span class="token operator">=</span> mean_squared_error<span class="token punctuation">(</span>housing_labels<span class="token punctuation">,</span> housing_predictions<span class="token punctuation">)</span>
forest_rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span>forest_mse<span class="token punctuation">)</span>
forest_rmse
</code></pre>
<pre><code>21941.911027380233
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> cross_val_score

forest_scores <span class="token operator">=</span> cross_val_score<span class="token punctuation">(</span>forest_reg<span class="token punctuation">,</span> housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">,</span>
                                scoring<span class="token operator">=</span><span class="token string">"neg_mean_squared_error"</span><span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">)</span>
forest_rmse_scores <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>forest_scores<span class="token punctuation">)</span>
display_scores<span class="token punctuation">(</span>forest_rmse_scores<span class="token punctuation">)</span>
</code></pre>
<pre><code>Scores: [ 51650.94405471  48920.80645498  52979.16096752  54412.74042021
  50861.29381163  56488.55699727  51866.90120786  49752.24599537
  55399.50713191  53309.74548294]
Mean: 52564.1902524
Standard deviation: 2301.87380392
</code></pre>
<pre class=" language-python"><code class="prism  language-python">scores <span class="token operator">=</span> cross_val_score<span class="token punctuation">(</span>lin_reg<span class="token punctuation">,</span> housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">,</span> scoring<span class="token operator">=</span><span class="token string">"neg_mean_squared_error"</span><span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">)</span>
pd<span class="token punctuation">.</span>Series<span class="token punctuation">(</span>np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>scores<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>describe<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>count       10.000000
mean     69052.461363
std       2879.437224
min      64969.630564
25%      67136.363758
50%      68156.372635
75%      70982.369487
max      74739.570526
dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>svm <span class="token keyword">import</span> SVR

svm_reg <span class="token operator">=</span> SVR<span class="token punctuation">(</span>kernel<span class="token operator">=</span><span class="token string">"linear"</span><span class="token punctuation">)</span>
svm_reg<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
housing_predictions <span class="token operator">=</span> svm_reg<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">)</span>
svm_mse <span class="token operator">=</span> mean_squared_error<span class="token punctuation">(</span>housing_labels<span class="token punctuation">,</span> housing_predictions<span class="token punctuation">)</span>
svm_rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span>svm_mse<span class="token punctuation">)</span>
svm_rmse
</code></pre>
<pre><code>111094.6308539982
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> GridSearchCV

param_grid <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token comment"># try 12 (3×4) combinations of hyperparameters</span>
    <span class="token punctuation">{</span><span class="token string">'n_estimators'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">30</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">'max_features'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">,</span> <span class="token number">6</span><span class="token punctuation">,</span> <span class="token number">8</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token comment"># then try 6 (2×3) combinations with bootstrap set as False</span>
    <span class="token punctuation">{</span><span class="token string">'bootstrap'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token boolean">False</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">'n_estimators'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">10</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">'max_features'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span>

forest_reg <span class="token operator">=</span> RandomForestRegressor<span class="token punctuation">(</span>random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
<span class="token comment"># train across 5 folds, that's a total of (12+6)*5=90 rounds of training </span>
grid_search <span class="token operator">=</span> GridSearchCV<span class="token punctuation">(</span>forest_reg<span class="token punctuation">,</span> param_grid<span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">5</span><span class="token punctuation">,</span>
                           scoring<span class="token operator">=</span><span class="token string">'neg_mean_squared_error'</span><span class="token punctuation">,</span> return_train_score<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
grid_search<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>GridSearchCV(cv=5, error_score='raise',
       estimator=RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
           oob_score=False, random_state=42, verbose=0, warm_start=False),
       fit_params=None, iid=True, n_jobs=1,
       param_grid=[{u'n_estimators': [3, 10, 30], u'max_features': [2, 4, 6, 8]}, {u'n_estimators': [3, 10], u'max_features': [2, 3, 4], u'bootstrap': [False]}],
       pre_dispatch='2*n_jobs', refit=True, return_train_score=True,
       scoring=u'neg_mean_squared_error', verbose=0)
</code></pre>
<p>The best hyperparameter combination found:</p>
<pre class=" language-python"><code class="prism  language-python">grid_search<span class="token punctuation">.</span>best_params_
</code></pre>
<pre><code>{u'max_features': 8, u'n_estimators': 30}
</code></pre>
<pre class=" language-python"><code class="prism  language-python">grid_search<span class="token punctuation">.</span>best_estimator_
</code></pre>
<pre><code>RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features=8, max_leaf_nodes=None, min_impurity_decrease=0.0,
           min_impurity_split=None, min_samples_leaf=1,
           min_samples_split=2, min_weight_fraction_leaf=0.0,
           n_estimators=30, n_jobs=1, oob_score=False, random_state=42,
           verbose=0, warm_start=False)
</code></pre>
<p>Let’s look at the score of each hyperparameter combination tested during the grid search:</p>
<pre class=" language-python"><code class="prism  language-python">cvres <span class="token operator">=</span> grid_search<span class="token punctuation">.</span>cv_results_
<span class="token keyword">for</span> mean_score<span class="token punctuation">,</span> params <span class="token keyword">in</span> <span class="token builtin">zip</span><span class="token punctuation">(</span>cvres<span class="token punctuation">[</span><span class="token string">"mean_test_score"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> cvres<span class="token punctuation">[</span><span class="token string">"params"</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span>np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>mean_score<span class="token punctuation">)</span><span class="token punctuation">,</span> params<span class="token punctuation">)</span>
</code></pre>
<pre><code>63647.854446 {u'max_features': 2, u'n_estimators': 3}
55611.5015988 {u'max_features': 2, u'n_estimators': 10}
53370.0640736 {u'max_features': 2, u'n_estimators': 30}
60959.1388585 {u'max_features': 4, u'n_estimators': 3}
52740.5841667 {u'max_features': 4, u'n_estimators': 10}
50374.1421461 {u'max_features': 4, u'n_estimators': 30}
58661.2866462 {u'max_features': 6, u'n_estimators': 3}
52009.9739798 {u'max_features': 6, u'n_estimators': 10}
50154.1177737 {u'max_features': 6, u'n_estimators': 30}
57865.3616801 {u'max_features': 8, u'n_estimators': 3}
51730.0755087 {u'max_features': 8, u'n_estimators': 10}
49694.8514333 {u'max_features': 8, u'n_estimators': 30}
62874.4073931 {u'max_features': 2, u'n_estimators': 3, u'bootstrap': False}
54643.4998083 {u'max_features': 2, u'n_estimators': 10, u'bootstrap': False}
59437.8922859 {u'max_features': 3, u'n_estimators': 3, u'bootstrap': False}
52735.3582936 {u'max_features': 3, u'n_estimators': 10, u'bootstrap': False}
57490.0168279 {u'max_features': 4, u'n_estimators': 3, u'bootstrap': False}
51008.2615672 {u'max_features': 4, u'n_estimators': 10, u'bootstrap': False}
</code></pre>
<pre class=" language-python"><code class="prism  language-python">pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">(</span>grid_search<span class="token punctuation">.</span>cv_results_<span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>mean_fit_time</th>
      <th>mean_score_time</th>
      <th>mean_test_score</th>
      <th>mean_train_score</th>
      <th>param_bootstrap</th>
      <th>param_max_features</th>
      <th>param_n_estimators</th>
      <th>params</th>
      <th>rank_test_score</th>
      <th>split0_test_score</th>
      <th>...</th>
      <th>split2_test_score</th>
      <th>split2_train_score</th>
      <th>split3_test_score</th>
      <th>split3_train_score</th>
      <th>split4_test_score</th>
      <th>split4_train_score</th>
      <th>std_fit_time</th>
      <th>std_score_time</th>
      <th>std_test_score</th>
      <th>std_train_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.047588</td>
      <td>0.002515</td>
      <td>-4.051049e+09</td>
      <td>-1.106013e+09</td>
      <td>NaN</td>
      <td>2</td>
      <td>3</td>
      <td>{u'max_features': 2, u'n_estimators': 3}</td>
      <td>18</td>
      <td>-3.850668e+09</td>
      <td>...</td>
      <td>-4.194135e+09</td>
      <td>-1.116843e+09</td>
      <td>-3.906732e+09</td>
      <td>-1.112813e+09</td>
      <td>-4.169669e+09</td>
      <td>-1.129842e+09</td>
      <td>0.002064</td>
      <td>0.000087</td>
      <td>1.431223e+08</td>
      <td>2.173798e+07</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.153054</td>
      <td>0.007240</td>
      <td>-3.092639e+09</td>
      <td>-5.819353e+08</td>
      <td>NaN</td>
      <td>2</td>
      <td>10</td>
      <td>{u'max_features': 2, u'n_estimators': 10}</td>
      <td>11</td>
      <td>-3.052380e+09</td>
      <td>...</td>
      <td>-3.124982e+09</td>
      <td>-5.780873e+08</td>
      <td>-2.865117e+09</td>
      <td>-5.713421e+08</td>
      <td>-3.169914e+09</td>
      <td>-5.797944e+08</td>
      <td>0.000650</td>
      <td>0.000178</td>
      <td>1.306954e+08</td>
      <td>7.584886e+06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.462324</td>
      <td>0.021171</td>
      <td>-2.848364e+09</td>
      <td>-4.396234e+08</td>
      <td>NaN</td>
      <td>2</td>
      <td>30</td>
      <td>{u'max_features': 2, u'n_estimators': 30}</td>
      <td>9</td>
      <td>-2.692176e+09</td>
      <td>...</td>
      <td>-2.943808e+09</td>
      <td>-4.374429e+08</td>
      <td>-2.619893e+09</td>
      <td>-4.374715e+08</td>
      <td>-2.968460e+09</td>
      <td>-4.451903e+08</td>
      <td>0.006894</td>
      <td>0.000629</td>
      <td>1.604534e+08</td>
      <td>2.883885e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.077386</td>
      <td>0.002587</td>
      <td>-3.716017e+09</td>
      <td>-9.850011e+08</td>
      <td>NaN</td>
      <td>4</td>
      <td>3</td>
      <td>{u'max_features': 4, u'n_estimators': 3}</td>
      <td>16</td>
      <td>-3.729600e+09</td>
      <td>...</td>
      <td>-3.736527e+09</td>
      <td>-9.172986e+08</td>
      <td>-3.404974e+09</td>
      <td>-1.035901e+09</td>
      <td>-3.914186e+09</td>
      <td>-9.711998e+08</td>
      <td>0.000700</td>
      <td>0.000162</td>
      <td>1.690029e+08</td>
      <td>4.047487e+07</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.253690</td>
      <td>0.007875</td>
      <td>-2.781569e+09</td>
      <td>-5.160154e+08</td>
      <td>NaN</td>
      <td>4</td>
      <td>10</td>
      <td>{u'max_features': 4, u'n_estimators': 10}</td>
      <td>8</td>
      <td>-2.667093e+09</td>
      <td>...</td>
      <td>-2.891599e+09</td>
      <td>-4.960301e+08</td>
      <td>-2.613393e+09</td>
      <td>-5.422542e+08</td>
      <td>-2.949550e+09</td>
      <td>-5.158794e+08</td>
      <td>0.004021</td>
      <td>0.000395</td>
      <td>1.278498e+08</td>
      <td>1.498960e+07</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.757576</td>
      <td>0.021818</td>
      <td>-2.537554e+09</td>
      <td>-3.878685e+08</td>
      <td>NaN</td>
      <td>4</td>
      <td>30</td>
      <td>{u'max_features': 4, u'n_estimators': 30}</td>
      <td>3</td>
      <td>-2.387199e+09</td>
      <td>...</td>
      <td>-2.663178e+09</td>
      <td>-3.789712e+08</td>
      <td>-2.397951e+09</td>
      <td>-4.036920e+08</td>
      <td>-2.649850e+09</td>
      <td>-3.846171e+08</td>
      <td>0.003527</td>
      <td>0.000696</td>
      <td>1.209935e+08</td>
      <td>8.424973e+06</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.102198</td>
      <td>0.002501</td>
      <td>-3.441147e+09</td>
      <td>-9.030212e+08</td>
      <td>NaN</td>
      <td>6</td>
      <td>3</td>
      <td>{u'max_features': 6, u'n_estimators': 3}</td>
      <td>14</td>
      <td>-3.119576e+09</td>
      <td>...</td>
      <td>-3.587747e+09</td>
      <td>-9.360639e+08</td>
      <td>-3.331544e+09</td>
      <td>-9.025026e+08</td>
      <td>-3.577062e+09</td>
      <td>-8.612945e+08</td>
      <td>0.002566</td>
      <td>0.000088</td>
      <td>1.884229e+08</td>
      <td>2.639683e+07</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.340551</td>
      <td>0.007072</td>
      <td>-2.705037e+09</td>
      <td>-5.014210e+08</td>
      <td>NaN</td>
      <td>6</td>
      <td>10</td>
      <td>{u'max_features': 6, u'n_estimators': 10}</td>
      <td>6</td>
      <td>-2.553481e+09</td>
      <td>...</td>
      <td>-2.762945e+09</td>
      <td>-4.996537e+08</td>
      <td>-2.519522e+09</td>
      <td>-4.989516e+08</td>
      <td>-2.906270e+09</td>
      <td>-5.063617e+08</td>
      <td>0.003600</td>
      <td>0.000199</td>
      <td>1.464963e+08</td>
      <td>3.357661e+06</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1.036997</td>
      <td>0.020305</td>
      <td>-2.515436e+09</td>
      <td>-3.840197e+08</td>
      <td>NaN</td>
      <td>6</td>
      <td>30</td>
      <td>{u'max_features': 6, u'n_estimators': 30}</td>
      <td>2</td>
      <td>-2.371924e+09</td>
      <td>...</td>
      <td>-2.607962e+09</td>
      <td>-3.805596e+08</td>
      <td>-2.351220e+09</td>
      <td>-3.856159e+08</td>
      <td>-2.662399e+09</td>
      <td>-3.904866e+08</td>
      <td>0.003193</td>
      <td>0.000148</td>
      <td>1.283580e+08</td>
      <td>3.796810e+06</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.132511</td>
      <td>0.002587</td>
      <td>-3.348400e+09</td>
      <td>-8.884890e+08</td>
      <td>NaN</td>
      <td>8</td>
      <td>3</td>
      <td>{u'max_features': 8, u'n_estimators': 3}</td>
      <td>13</td>
      <td>-3.351347e+09</td>
      <td>...</td>
      <td>-3.396841e+09</td>
      <td>-8.596460e+08</td>
      <td>-3.131753e+09</td>
      <td>-8.893698e+08</td>
      <td>-3.509451e+09</td>
      <td>-9.146734e+08</td>
      <td>0.000737</td>
      <td>0.000206</td>
      <td>1.226683e+08</td>
      <td>2.730057e+07</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.444634</td>
      <td>0.007224</td>
      <td>-2.676001e+09</td>
      <td>-4.923247e+08</td>
      <td>NaN</td>
      <td>8</td>
      <td>10</td>
      <td>{u'max_features': 8, u'n_estimators': 10}</td>
      <td>5</td>
      <td>-2.572358e+09</td>
      <td>...</td>
      <td>-2.844608e+09</td>
      <td>-4.730979e+08</td>
      <td>-2.462797e+09</td>
      <td>-5.154156e+08</td>
      <td>-2.777049e+09</td>
      <td>-4.979127e+08</td>
      <td>0.003798</td>
      <td>0.000270</td>
      <td>1.393253e+08</td>
      <td>1.446900e+07</td>
    </tr>
    <tr>
      <th>11</th>
      <td>1.347425</td>
      <td>0.021286</td>
      <td>-2.469578e+09</td>
      <td>-3.809175e+08</td>
      <td>NaN</td>
      <td>8</td>
      <td>30</td>
      <td>{u'max_features': 8, u'n_estimators': 30}</td>
      <td>1</td>
      <td>-2.358884e+09</td>
      <td>...</td>
      <td>-2.591134e+09</td>
      <td>-3.772512e+08</td>
      <td>-2.319816e+09</td>
      <td>-3.881153e+08</td>
      <td>-2.528200e+09</td>
      <td>-3.807496e+08</td>
      <td>0.008091</td>
      <td>0.000833</td>
      <td>1.089395e+08</td>
      <td>4.853344e+06</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0.071177</td>
      <td>0.002865</td>
      <td>-3.953191e+09</td>
      <td>0.000000e+00</td>
      <td>False</td>
      <td>2</td>
      <td>3</td>
      <td>{u'max_features': 2, u'n_estimators': 3, u'boo...</td>
      <td>17</td>
      <td>-3.792367e+09</td>
      <td>...</td>
      <td>-4.050371e+09</td>
      <td>-0.000000e+00</td>
      <td>-3.668520e+09</td>
      <td>-0.000000e+00</td>
      <td>-4.087237e+09</td>
      <td>-0.000000e+00</td>
      <td>0.001398</td>
      <td>0.000022</td>
      <td>1.898516e+08</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>13</th>
      <td>0.236335</td>
      <td>0.008313</td>
      <td>-2.985912e+09</td>
      <td>-6.056027e-01</td>
      <td>False</td>
      <td>2</td>
      <td>10</td>
      <td>{u'max_features': 2, u'n_estimators': 10, u'bo...</td>
      <td>10</td>
      <td>-2.808029e+09</td>
      <td>...</td>
      <td>-3.125519e+09</td>
      <td>-0.000000e+00</td>
      <td>-2.788623e+09</td>
      <td>-0.000000e+00</td>
      <td>-3.100391e+09</td>
      <td>-2.967449e+00</td>
      <td>0.002125</td>
      <td>0.000137</td>
      <td>1.535103e+08</td>
      <td>1.181156e+00</td>
    </tr>
    <tr>
      <th>14</th>
      <td>0.094911</td>
      <td>0.002869</td>
      <td>-3.532863e+09</td>
      <td>-1.214568e+01</td>
      <td>False</td>
      <td>3</td>
      <td>3</td>
      <td>{u'max_features': 3, u'n_estimators': 3, u'boo...</td>
      <td>15</td>
      <td>-3.604830e+09</td>
      <td>...</td>
      <td>-3.552984e+09</td>
      <td>-0.000000e+00</td>
      <td>-3.610963e+09</td>
      <td>-0.000000e+00</td>
      <td>-3.455760e+09</td>
      <td>-6.072840e+01</td>
      <td>0.001890</td>
      <td>0.000067</td>
      <td>7.251650e+07</td>
      <td>2.429136e+01</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0.313297</td>
      <td>0.008246</td>
      <td>-2.781018e+09</td>
      <td>-5.272080e+00</td>
      <td>False</td>
      <td>3</td>
      <td>10</td>
      <td>{u'max_features': 3, u'n_estimators': 10, u'bo...</td>
      <td>7</td>
      <td>-2.756941e+09</td>
      <td>...</td>
      <td>-2.831963e+09</td>
      <td>-0.000000e+00</td>
      <td>-2.672258e+09</td>
      <td>-0.000000e+00</td>
      <td>-2.793018e+09</td>
      <td>-5.465556e+00</td>
      <td>0.003446</td>
      <td>0.000170</td>
      <td>6.329307e+07</td>
      <td>8.093117e+00</td>
    </tr>
    <tr>
      <th>16</th>
      <td>0.120070</td>
      <td>0.002876</td>
      <td>-3.305102e+09</td>
      <td>0.000000e+00</td>
      <td>False</td>
      <td>4</td>
      <td>3</td>
      <td>{u'max_features': 4, u'n_estimators': 3, u'boo...</td>
      <td>12</td>
      <td>-3.143457e+09</td>
      <td>...</td>
      <td>-3.440323e+09</td>
      <td>-0.000000e+00</td>
      <td>-3.047980e+09</td>
      <td>-0.000000e+00</td>
      <td>-3.337950e+09</td>
      <td>-0.000000e+00</td>
      <td>0.002027</td>
      <td>0.000076</td>
      <td>1.867866e+08</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>17</th>
      <td>0.401096</td>
      <td>0.008489</td>
      <td>-2.601843e+09</td>
      <td>-3.028238e-03</td>
      <td>False</td>
      <td>4</td>
      <td>10</td>
      <td>{u'max_features': 4, u'n_estimators': 10, u'bo...</td>
      <td>4</td>
      <td>-2.531436e+09</td>
      <td>...</td>
      <td>-2.606596e+09</td>
      <td>-0.000000e+00</td>
      <td>-2.437626e+09</td>
      <td>-0.000000e+00</td>
      <td>-2.726341e+09</td>
      <td>-0.000000e+00</td>
      <td>0.005403</td>
      <td>0.000062</td>
      <td>1.082086e+08</td>
      <td>6.056477e-03</td>
    </tr>
  </tbody>
</table>
<p>18 rows × 23 columns</p>

<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> RandomizedSearchCV
<span class="token keyword">from</span> scipy<span class="token punctuation">.</span>stats <span class="token keyword">import</span> randint

param_distribs <span class="token operator">=</span> <span class="token punctuation">{</span>
        <span class="token string">'n_estimators'</span><span class="token punctuation">:</span> randint<span class="token punctuation">(</span>low<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">,</span> high<span class="token operator">=</span><span class="token number">200</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string">'max_features'</span><span class="token punctuation">:</span> randint<span class="token punctuation">(</span>low<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">,</span> high<span class="token operator">=</span><span class="token number">8</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>

forest_reg <span class="token operator">=</span> RandomForestRegressor<span class="token punctuation">(</span>random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
rnd_search <span class="token operator">=</span> RandomizedSearchCV<span class="token punctuation">(</span>forest_reg<span class="token punctuation">,</span> param_distributions<span class="token operator">=</span>param_distribs<span class="token punctuation">,</span>
                                n_iter<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">5</span><span class="token punctuation">,</span> scoring<span class="token operator">=</span><span class="token string">'neg_mean_squared_error'</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
rnd_search<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>RandomizedSearchCV(cv=5, error_score='raise',
          estimator=RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
           oob_score=False, random_state=42, verbose=0, warm_start=False),
          fit_params=None, iid=True, n_iter=10, n_jobs=1,
          param_distributions={u'n_estimators': &lt;scipy.stats._distn_infrastructure.rv_frozen object at 0x7f6dc02e0d90&gt;, u'max_features': &lt;scipy.stats._distn_infrastructure.rv_frozen object at 0x7f6dc07960d0&gt;},
          pre_dispatch='2*n_jobs', random_state=42, refit=True,
          return_train_score='warn', scoring=u'neg_mean_squared_error',
          verbose=0)
</code></pre>
<pre class=" language-python"><code class="prism  language-python">cvres <span class="token operator">=</span> rnd_search<span class="token punctuation">.</span>cv_results_
<span class="token keyword">for</span> mean_score<span class="token punctuation">,</span> params <span class="token keyword">in</span> <span class="token builtin">zip</span><span class="token punctuation">(</span>cvres<span class="token punctuation">[</span><span class="token string">"mean_test_score"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> cvres<span class="token punctuation">[</span><span class="token string">"params"</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span>np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>mean_score<span class="token punctuation">)</span><span class="token punctuation">,</span> params<span class="token punctuation">)</span>
</code></pre>
<pre><code>49147.1524172 {u'max_features': 7, u'n_estimators': 180}
51396.8768969 {u'max_features': 5, u'n_estimators': 15}
50797.0573732 {u'max_features': 3, u'n_estimators': 72}
50840.744514 {u'max_features': 5, u'n_estimators': 21}
49276.1753033 {u'max_features': 7, u'n_estimators': 122}
50775.4633168 {u'max_features': 3, u'n_estimators': 75}
50681.383925 {u'max_features': 3, u'n_estimators': 88}
49612.1525305 {u'max_features': 5, u'n_estimators': 100}
50473.0175142 {u'max_features': 3, u'n_estimators': 150}
64458.2538503 {u'max_features': 5, u'n_estimators': 2}
</code></pre>
<pre class=" language-python"><code class="prism  language-python">feature_importances <span class="token operator">=</span> grid_search<span class="token punctuation">.</span>best_estimator_<span class="token punctuation">.</span>feature_importances_
feature_importances
</code></pre>
<pre><code>array([  7.33442355e-02,   6.29090705e-02,   4.11437985e-02,
         1.46726854e-02,   1.41064835e-02,   1.48742809e-02,
         1.42575993e-02,   3.66158981e-01,   5.64191792e-02,
         1.08792957e-01,   5.33510773e-02,   1.03114883e-02,
         1.64780994e-01,   6.02803867e-05,   1.96041560e-03,
         2.85647464e-03])
</code></pre>
<pre class=" language-python"><code class="prism  language-python">extra_attribs <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">"rooms_per_hhold"</span><span class="token punctuation">,</span> <span class="token string">"pop_per_hhold"</span><span class="token punctuation">,</span> <span class="token string">"bedrooms_per_room"</span><span class="token punctuation">]</span>
cat_encoder <span class="token operator">=</span> cat_pipeline<span class="token punctuation">.</span>named_steps<span class="token punctuation">[</span><span class="token string">"cat_encoder"</span><span class="token punctuation">]</span>
cat_one_hot_attribs <span class="token operator">=</span> <span class="token builtin">list</span><span class="token punctuation">(</span>cat_encoder<span class="token punctuation">.</span>categories_<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
attributes <span class="token operator">=</span> num_attribs <span class="token operator">+</span> extra_attribs <span class="token operator">+</span> cat_one_hot_attribs
<span class="token builtin">sorted</span><span class="token punctuation">(</span><span class="token builtin">zip</span><span class="token punctuation">(</span>feature_importances<span class="token punctuation">,</span> attributes<span class="token punctuation">)</span><span class="token punctuation">,</span> reverse<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>[(0.36615898061813418, 'median_income'),
 (0.16478099356159051, 'INLAND'),
 (0.10879295677551573, u'pop_per_hhold'),
 (0.073344235516012421, 'longitude'),
 (0.062909070482620302, 'latitude'),
 (0.056419179181954007, u'rooms_per_hhold'),
 (0.053351077347675809, u'bedrooms_per_room'),
 (0.041143798478729635, 'housing_median_age'),
 (0.014874280890402767, 'population'),
 (0.014672685420543237, 'total_rooms'),
 (0.014257599323407807, 'households'),
 (0.014106483453584102, 'total_bedrooms'),
 (0.010311488326303787, '&lt;1H OCEAN'),
 (0.0028564746373201579, 'NEAR OCEAN'),
 (0.0019604155994780701, 'NEAR BAY'),
 (6.0280386727365991e-05, 'ISLAND')]
</code></pre>
<pre class=" language-python"><code class="prism  language-python">final_model <span class="token operator">=</span> grid_search<span class="token punctuation">.</span>best_estimator_

X_test <span class="token operator">=</span> strat_test_set<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span>
y_test <span class="token operator">=</span> strat_test_set<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>copy<span class="token punctuation">(</span><span class="token punctuation">)</span>

X_test_prepared <span class="token operator">=</span> full_pipeline<span class="token punctuation">.</span>transform<span class="token punctuation">(</span>X_test<span class="token punctuation">)</span>
final_predictions <span class="token operator">=</span> final_model<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>X_test_prepared<span class="token punctuation">)</span>

final_mse <span class="token operator">=</span> mean_squared_error<span class="token punctuation">(</span>y_test<span class="token punctuation">,</span> final_predictions<span class="token punctuation">)</span>
final_rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span>final_mse<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">final_rmse
</code></pre>
<pre><code>47766.003966433083
</code></pre>
<h1 id="extra-material">Extra material</h1>
<h2 id="a-full-pipeline-with-both-preparation-and-prediction">A full pipeline with both preparation and prediction</h2>
<pre class=" language-python"><code class="prism  language-python">full_pipeline_with_predictor <span class="token operator">=</span> Pipeline<span class="token punctuation">(</span><span class="token punctuation">[</span>
        <span class="token punctuation">(</span><span class="token string">"preparation"</span><span class="token punctuation">,</span> full_pipeline<span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">(</span><span class="token string">"linear"</span><span class="token punctuation">,</span> LinearRegression<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">]</span><span class="token punctuation">)</span>

full_pipeline_with_predictor<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
full_pipeline_with_predictor<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>some_data<span class="token punctuation">)</span>
</code></pre>
<pre><code>array([ 210644.60459286,  317768.80697211,  210956.43331178,
         59218.98886849,  189747.55849879])
</code></pre>
<h2 id="model-persistence-using-joblib">Model persistence using joblib</h2>
<pre class=" language-python"><code class="prism  language-python">my_model <span class="token operator">=</span> full_pipeline_with_predictor
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>externals <span class="token keyword">import</span> joblib
joblib<span class="token punctuation">.</span>dump<span class="token punctuation">(</span>my_model<span class="token punctuation">,</span> <span class="token string">"my_model.pkl"</span><span class="token punctuation">)</span> <span class="token comment"># DIFF</span>
<span class="token comment">#...</span>
my_model_loaded <span class="token operator">=</span> joblib<span class="token punctuation">.</span>load<span class="token punctuation">(</span><span class="token string">"my_model.pkl"</span><span class="token punctuation">)</span> <span class="token comment"># DIFF</span>
</code></pre>
<h2 id="example-scipy-distributions-for-randomizedsearchcv">Example SciPy distributions for <code>RandomizedSearchCV</code></h2>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> scipy<span class="token punctuation">.</span>stats <span class="token keyword">import</span> geom<span class="token punctuation">,</span> expon
geom_distrib<span class="token operator">=</span>geom<span class="token punctuation">(</span><span class="token number">0.5</span><span class="token punctuation">)</span><span class="token punctuation">.</span>rvs<span class="token punctuation">(</span><span class="token number">10000</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
expon_distrib<span class="token operator">=</span>expon<span class="token punctuation">(</span>scale<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">.</span>rvs<span class="token punctuation">(</span><span class="token number">10000</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>geom_distrib<span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>expon_distrib<span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<p><img src="output_143_0.png" alt="png"></p>
<p><img src="output_143_1.png" alt="png"></p>
<h1 id="exercise-solutions">Exercise solutions</h1>
<h2 id="section">1.</h2>
<p>Question: Try a Support Vector Machine regressor (<code>sklearn.svm.SVR</code>), with various hyperparameters such as <code>kernel="linear"</code> (with various values for the <code>C</code> hyperparameter) or <code>kernel="rbf"</code> (with various values for the <code>C</code> and <code>gamma</code> hyperparameters). Don’t worry about what these hyperparameters mean for now. How does the best <code>SVR</code> predictor perform?</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> GridSearchCV

param_grid <span class="token operator">=</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span><span class="token string">'kernel'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">'linear'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">'C'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">10</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">30</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">100</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">300</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">1000</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">3000</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">10000</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">30000.0</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span><span class="token string">'kernel'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">'rbf'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">'C'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">1.0</span><span class="token punctuation">,</span> <span class="token number">3.0</span><span class="token punctuation">,</span> <span class="token number">10</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">30</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">100</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">300</span><span class="token punctuation">.</span><span class="token punctuation">,</span> <span class="token number">1000.0</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
         <span class="token string">'gamma'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token number">0.01</span><span class="token punctuation">,</span> <span class="token number">0.03</span><span class="token punctuation">,</span> <span class="token number">0.1</span><span class="token punctuation">,</span> <span class="token number">0.3</span><span class="token punctuation">,</span> <span class="token number">1.0</span><span class="token punctuation">,</span> <span class="token number">3.0</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span>

svm_reg <span class="token operator">=</span> SVR<span class="token punctuation">(</span><span class="token punctuation">)</span>
grid_search <span class="token operator">=</span> GridSearchCV<span class="token punctuation">(</span>svm_reg<span class="token punctuation">,</span> param_grid<span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">5</span><span class="token punctuation">,</span> scoring<span class="token operator">=</span><span class="token string">'neg_mean_squared_error'</span><span class="token punctuation">,</span> verbose<span class="token operator">=</span><span class="token number">2</span><span class="token punctuation">,</span> n_jobs<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">)</span>
grid_search<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>Fitting 5 folds for each of 50 candidates, totalling 250 fits
[CV] kernel=linear, C=10.0 ...........................................
[CV] kernel=linear, C=10.0 ...........................................
[CV] kernel=linear, C=10.0 ...........................................
[CV] kernel=linear, C=10.0 ...........................................
[CV] ............................ kernel=linear, C=10.0, total=   8.3s
[CV] kernel=linear, C=10.0 ...........................................
[CV] ............................ kernel=linear, C=10.0, total=   8.3s
[CV] kernel=linear, C=30.0 ...........................................
[CV] ............................ kernel=linear, C=10.0, total=   8.4s
[CV] kernel=linear, C=30.0 ...........................................
[CV] ............................ kernel=linear, C=10.0, total=   8.4s
[CV] kernel=linear, C=30.0 ...........................................
[CV] ............................ kernel=linear, C=30.0, total=   8.1s
[CV] kernel=linear, C=30.0 ...........................................
[CV] ............................ kernel=linear, C=10.0, total=   8.3s
[CV] kernel=linear, C=30.0 ...........................................
[CV] ............................ kernel=linear, C=30.0, total=   8.1s
[CV] kernel=linear, C=100.0 ..........................................
[CV] ............................ kernel=linear, C=30.0, total=   8.4s
[CV] kernel=linear, C=100.0 ..........................................
[CV] ............................ kernel=linear, C=30.0, total=   8.0s
[CV] kernel=linear, C=100.0 ..........................................
[CV] ........................... kernel=linear, C=100.0, total=   8.0s
[CV] kernel=linear, C=100.0 ..........................................
[CV] ............................ kernel=linear, C=30.0, total=   8.2s
[CV] kernel=linear, C=100.0 ..........................................
[CV] ........................... kernel=linear, C=100.0, total=   8.0s
[CV] kernel=linear, C=300.0 ..........................................
[CV] ........................... kernel=linear, C=100.0, total=   7.8s
[CV] kernel=linear, C=300.0 ..........................................
[CV] ........................... kernel=linear, C=100.0, total=   7.9s
[CV] kernel=linear, C=300.0 ..........................................
[CV] ........................... kernel=linear, C=100.0, total=   8.3s
[CV] kernel=linear, C=300.0 ..........................................
[CV] ........................... kernel=linear, C=300.0, total=   8.0s
[CV] kernel=linear, C=300.0 ..........................................
[CV] ........................... kernel=linear, C=300.0, total=   8.1s
[CV] kernel=linear, C=1000.0 .........................................
[CV] ........................... kernel=linear, C=300.0, total=   8.3s
[CV] kernel=linear, C=1000.0 .........................................
[CV] ........................... kernel=linear, C=300.0, total=   8.1s
[CV] kernel=linear, C=1000.0 .........................................
[CV] ........................... kernel=linear, C=300.0, total=   8.2s
[CV] kernel=linear, C=1000.0 .........................................
[CV] .......................... kernel=linear, C=1000.0, total=   8.7s
[CV] kernel=linear, C=1000.0 .........................................
[CV] .......................... kernel=linear, C=1000.0, total=   8.6s
[CV] kernel=linear, C=3000.0 .........................................
[CV] .......................... kernel=linear, C=1000.0, total=   8.6s
[CV] kernel=linear, C=3000.0 .........................................
[CV] .......................... kernel=linear, C=1000.0, total=   8.8s
[CV] kernel=linear, C=3000.0 .........................................
[CV] .......................... kernel=linear, C=1000.0, total=   8.8s
[CV] kernel=linear, C=3000.0 .........................................
[CV] .......................... kernel=linear, C=3000.0, total=   9.3s
[CV] kernel=linear, C=3000.0 .........................................
[CV] .......................... kernel=linear, C=3000.0, total=   9.4s
[CV] kernel=linear, C=10000.0 ........................................
[CV] .......................... kernel=linear, C=3000.0, total=   9.5s
[CV] kernel=linear, C=10000.0 ........................................
[CV] .......................... kernel=linear, C=3000.0, total=   9.3s
[CV] kernel=linear, C=10000.0 ........................................
[CV] .......................... kernel=linear, C=3000.0, total=   8.9s
[CV] kernel=linear, C=10000.0 ........................................
[CV] ......................... kernel=linear, C=10000.0, total=  11.9s
[CV] kernel=linear, C=10000.0 ........................................
[CV] ......................... kernel=linear, C=10000.0, total=  12.2s
[CV] kernel=linear, C=30000.0 ........................................
[CV] ......................... kernel=linear, C=10000.0, total=  11.4s
[CV] kernel=linear, C=30000.0 ........................................
[CV] ......................... kernel=linear, C=10000.0, total=  12.3s
[CV] kernel=linear, C=30000.0 ........................................


[Parallel(n_jobs=4)]: Done  33 tasks      | elapsed:  1.7min


[CV] ......................... kernel=linear, C=10000.0, total=  11.1s
[CV] kernel=linear, C=30000.0 ........................................
[CV] ......................... kernel=linear, C=30000.0, total=  19.6s
[CV] kernel=linear, C=30000.0 ........................................
[CV] ......................... kernel=linear, C=30000.0, total=  20.0s
[CV] kernel=rbf, C=1.0, gamma=0.01 ...................................
[CV] ......................... kernel=linear, C=30000.0, total=  20.8s
[CV] kernel=rbf, C=1.0, gamma=0.01 ...................................
[CV] ......................... kernel=linear, C=30000.0, total=  19.9s
[CV] kernel=rbf, C=1.0, gamma=0.01 ...................................
[CV] ......................... kernel=linear, C=30000.0, total=  17.6s
[CV] kernel=rbf, C=1.0, gamma=0.01 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.01, total=  25.1s
[CV] kernel=rbf, C=1.0, gamma=0.01 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.01, total=  25.3s
[CV] kernel=rbf, C=1.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.01, total=  25.0s
[CV] kernel=rbf, C=1.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.01, total=  25.2s
[CV] kernel=rbf, C=1.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.01, total=  14.6s
[CV] kernel=rbf, C=1.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.03, total=  14.3s
[CV] kernel=rbf, C=1.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.03, total=  14.7s
[CV] kernel=rbf, C=1.0, gamma=0.1 ....................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.03, total=  14.8s
[CV] kernel=rbf, C=1.0, gamma=0.1 ....................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.03, total=  14.5s
[CV] kernel=rbf, C=1.0, gamma=0.1 ....................................
[CV] .................... kernel=rbf, C=1.0, gamma=0.03, total=  14.3s
[CV] kernel=rbf, C=1.0, gamma=0.1 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.1, total=  14.2s
[CV] kernel=rbf, C=1.0, gamma=0.1 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.1, total=  13.8s
[CV] kernel=rbf, C=1.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.1, total=  13.8s
[CV] kernel=rbf, C=1.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.1, total=  13.8s
[CV] kernel=rbf, C=1.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.1, total=  13.8s
[CV] kernel=rbf, C=1.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.3, total=  13.3s
[CV] kernel=rbf, C=1.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=1.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=1.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.3, total=  13.5s
[CV] kernel=rbf, C=1.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=1.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=1.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=1.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=1.0, total=  13.0s
[CV] kernel=rbf, C=1.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=1.0, total=  13.1s
[CV] kernel=rbf, C=1.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=1.0, total=  13.0s
[CV] kernel=rbf, C=1.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=3.0, total=  14.5s
[CV] kernel=rbf, C=1.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=1.0, gamma=3.0, total=  14.4s
[CV] kernel=rbf, C=3.0, gamma=0.01 ...................................
[CV] ..................... kernel=rbf, C=1.0, gamma=3.0, total=  14.6s
[CV] kernel=rbf, C=3.0, gamma=0.01 ...................................
[CV] ..................... kernel=rbf, C=1.0, gamma=3.0, total=  14.1s
[CV] kernel=rbf, C=3.0, gamma=0.01 ...................................
[CV] ..................... kernel=rbf, C=1.0, gamma=3.0, total=  14.2s
[CV] kernel=rbf, C=3.0, gamma=0.01 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.01, total=  13.9s
[CV] kernel=rbf, C=3.0, gamma=0.01 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.01, total=  13.9s
[CV] kernel=rbf, C=3.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.01, total=  13.9s
[CV] kernel=rbf, C=3.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.01, total=  14.1s
[CV] kernel=rbf, C=3.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.01, total=  14.0s
[CV] kernel=rbf, C=3.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.03, total=  14.0s
[CV] kernel=rbf, C=3.0, gamma=0.03 ...................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.03, total=  13.9s
[CV] kernel=rbf, C=3.0, gamma=0.1 ....................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.03, total=  14.1s
[CV] kernel=rbf, C=3.0, gamma=0.1 ....................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.03, total=  13.6s
[CV] kernel=rbf, C=3.0, gamma=0.1 ....................................
[CV] .................... kernel=rbf, C=3.0, gamma=0.03, total=  13.8s
[CV] kernel=rbf, C=3.0, gamma=0.1 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.1, total=  13.7s
[CV] kernel=rbf, C=3.0, gamma=0.1 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.1, total=  13.5s
[CV] kernel=rbf, C=3.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.1, total=  13.4s
[CV] kernel=rbf, C=3.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.1, total=  13.4s
[CV] kernel=rbf, C=3.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.1, total=  13.7s
[CV] kernel=rbf, C=3.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=3.0, gamma=0.3 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.3, total=  13.6s
[CV] kernel=rbf, C=3.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.3, total=  13.7s
[CV] kernel=rbf, C=3.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.3, total=  13.2s
[CV] kernel=rbf, C=3.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=0.3, total=  13.2s
[CV] kernel=rbf, C=3.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=3.0, gamma=1.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=1.0, total=  13.0s
[CV] kernel=rbf, C=3.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=3.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=3.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=1.0, total=  12.7s
[CV] kernel=rbf, C=3.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=3.0, total=  14.1s
[CV] kernel=rbf, C=3.0, gamma=3.0 ....................................
[CV] ..................... kernel=rbf, C=3.0, gamma=3.0, total=  13.9s
[CV] kernel=rbf, C=10.0, gamma=0.01 ..................................
[CV] ..................... kernel=rbf, C=3.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=10.0, gamma=0.01 ..................................
[CV] ..................... kernel=rbf, C=3.0, gamma=3.0, total=  13.9s
[CV] kernel=rbf, C=10.0, gamma=0.01 ..................................
[CV] ..................... kernel=rbf, C=3.0, gamma=3.0, total=  14.3s
[CV] kernel=rbf, C=10.0, gamma=0.01 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.01, total=  14.4s
[CV] kernel=rbf, C=10.0, gamma=0.01 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.01, total=  14.2s
[CV] kernel=rbf, C=10.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.01, total=  14.0s
[CV] kernel=rbf, C=10.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.01, total=  14.2s
[CV] kernel=rbf, C=10.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.01, total=  14.2s
[CV] kernel=rbf, C=10.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.03, total=  14.0s
[CV] kernel=rbf, C=10.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.03, total=  14.2s
[CV] kernel=rbf, C=10.0, gamma=0.1 ...................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.03, total=  14.1s
[CV] kernel=rbf, C=10.0, gamma=0.1 ...................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.03, total=  14.3s
[CV] kernel=rbf, C=10.0, gamma=0.1 ...................................
[CV] ................... kernel=rbf, C=10.0, gamma=0.03, total=  14.3s
[CV] kernel=rbf, C=10.0, gamma=0.1 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.1, total=  14.0s
[CV] kernel=rbf, C=10.0, gamma=0.1 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.1, total=  14.0s
[CV] kernel=rbf, C=10.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.1, total=  13.6s
[CV] kernel=rbf, C=10.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.1, total=  13.6s
[CV] kernel=rbf, C=10.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.1, total=  13.8s
[CV] kernel=rbf, C=10.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.3, total=  13.2s
[CV] kernel=rbf, C=10.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=10.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=10.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.3, total=  13.5s
[CV] kernel=rbf, C=10.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=0.3, total=  13.3s
[CV] kernel=rbf, C=10.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=10.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=10.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=10.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=10.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=1.0, total=  13.2s
[CV] kernel=rbf, C=10.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=10.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=10.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=30.0, gamma=0.01 ..................................
[CV] .................... kernel=rbf, C=10.0, gamma=3.0, total=  14.1s
[CV] kernel=rbf, C=30.0, gamma=0.01 ..................................
[CV] .................... kernel=rbf, C=10.0, gamma=3.0, total=  14.1s
[CV] kernel=rbf, C=30.0, gamma=0.01 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.01, total=  13.8s
[CV] kernel=rbf, C=30.0, gamma=0.01 ..................................
[CV] .................... kernel=rbf, C=10.0, gamma=3.0, total=  14.5s
[CV] kernel=rbf, C=30.0, gamma=0.01 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.01, total=  13.8s
[CV] kernel=rbf, C=30.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.01, total=  13.9s
[CV] kernel=rbf, C=30.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.01, total=  14.0s
[CV] kernel=rbf, C=30.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.01, total=  14.1s
[CV] kernel=rbf, C=30.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.03, total=  14.1s
[CV] kernel=rbf, C=30.0, gamma=0.03 ..................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.03, total=  14.2s
[CV] kernel=rbf, C=30.0, gamma=0.1 ...................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.03, total=  13.9s
[CV] kernel=rbf, C=30.0, gamma=0.1 ...................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.03, total=  14.0s
[CV] kernel=rbf, C=30.0, gamma=0.1 ...................................
[CV] ................... kernel=rbf, C=30.0, gamma=0.03, total=  13.8s
[CV] kernel=rbf, C=30.0, gamma=0.1 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.1, total=  13.8s
[CV] kernel=rbf, C=30.0, gamma=0.1 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.1, total=  13.6s
[CV] kernel=rbf, C=30.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.1, total=  13.6s
[CV] kernel=rbf, C=30.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.1, total=  13.7s
[CV] kernel=rbf, C=30.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.1, total=  13.9s
[CV] kernel=rbf, C=30.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.3, total=  13.3s
[CV] kernel=rbf, C=30.0, gamma=0.3 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=30.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.3, total=  13.3s
[CV] kernel=rbf, C=30.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.3, total=  13.6s
[CV] kernel=rbf, C=30.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=0.3, total=  13.5s
[CV] kernel=rbf, C=30.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=1.0, total=  13.3s
[CV] kernel=rbf, C=30.0, gamma=1.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=30.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=1.0, total=  13.2s
[CV] kernel=rbf, C=30.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=30.0, gamma=3.0 ...................................


[Parallel(n_jobs=4)]: Done 154 tasks      | elapsed: 11.8min


[CV] .................... kernel=rbf, C=30.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=30.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=30.0, gamma=3.0 ...................................
[CV] .................... kernel=rbf, C=30.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=100.0, gamma=0.01 .................................
[CV] .................... kernel=rbf, C=30.0, gamma=3.0, total=  13.9s
[CV] kernel=rbf, C=100.0, gamma=0.01 .................................
[CV] .................... kernel=rbf, C=30.0, gamma=3.0, total=  13.9s
[CV] kernel=rbf, C=100.0, gamma=0.01 .................................
[CV] .................... kernel=rbf, C=30.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=100.0, gamma=0.01 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.01, total=  13.8s
[CV] kernel=rbf, C=100.0, gamma=0.01 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.01, total=  13.8s
[CV] kernel=rbf, C=100.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.01, total=  13.9s
[CV] kernel=rbf, C=100.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.01, total=  14.0s
[CV] kernel=rbf, C=100.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.01, total=  14.0s
[CV] kernel=rbf, C=100.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.03, total=  13.7s
[CV] kernel=rbf, C=100.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.03, total=  13.8s
[CV] kernel=rbf, C=100.0, gamma=0.1 ..................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.03, total=  13.7s
[CV] kernel=rbf, C=100.0, gamma=0.1 ..................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.03, total=  14.0s
[CV] kernel=rbf, C=100.0, gamma=0.1 ..................................
[CV] .................. kernel=rbf, C=100.0, gamma=0.03, total=  14.4s
[CV] kernel=rbf, C=100.0, gamma=0.1 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.1, total=  13.3s
[CV] kernel=rbf, C=100.0, gamma=0.1 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.1, total=  13.4s
[CV] kernel=rbf, C=100.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.1, total=  13.5s
[CV] kernel=rbf, C=100.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.1, total=  13.6s
[CV] kernel=rbf, C=100.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.1, total=  13.6s
[CV] kernel=rbf, C=100.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.3, total=  13.0s
[CV] kernel=rbf, C=100.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.3, total=  13.4s
[CV] kernel=rbf, C=100.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.3, total=  13.5s
[CV] kernel=rbf, C=100.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.3, total=  13.8s
[CV] kernel=rbf, C=100.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=0.3, total=  13.5s
[CV] kernel=rbf, C=100.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=100.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=100.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=100.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=100.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=1.0, total=  12.8s
[CV] kernel=rbf, C=100.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=3.0, total=  14.2s
[CV] kernel=rbf, C=100.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=100.0, gamma=3.0, total=  14.2s
[CV] kernel=rbf, C=300.0, gamma=0.01 .................................
[CV] ................... kernel=rbf, C=100.0, gamma=3.0, total=  14.2s
[CV] kernel=rbf, C=300.0, gamma=0.01 .................................
[CV] ................... kernel=rbf, C=100.0, gamma=3.0, total=  14.1s
[CV] kernel=rbf, C=300.0, gamma=0.01 .................................
[CV] ................... kernel=rbf, C=100.0, gamma=3.0, total=  14.2s
[CV] kernel=rbf, C=300.0, gamma=0.01 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.01, total=  13.9s
[CV] kernel=rbf, C=300.0, gamma=0.01 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.01, total=  13.7s
[CV] kernel=rbf, C=300.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.01, total=  13.7s
[CV] kernel=rbf, C=300.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.01, total=  13.7s
[CV] kernel=rbf, C=300.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.01, total=  13.7s
[CV] kernel=rbf, C=300.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.03, total=  13.1s
[CV] kernel=rbf, C=300.0, gamma=0.03 .................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.03, total=  13.1s
[CV] kernel=rbf, C=300.0, gamma=0.1 ..................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.03, total=  13.0s
[CV] kernel=rbf, C=300.0, gamma=0.1 ..................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.03, total=  13.1s
[CV] kernel=rbf, C=300.0, gamma=0.1 ..................................
[CV] .................. kernel=rbf, C=300.0, gamma=0.03, total=  13.0s
[CV] kernel=rbf, C=300.0, gamma=0.1 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.1, total=  12.8s
[CV] kernel=rbf, C=300.0, gamma=0.1 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.1, total=  12.8s
[CV] kernel=rbf, C=300.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.1, total=  12.9s
[CV] kernel=rbf, C=300.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.1, total=  12.8s
[CV] kernel=rbf, C=300.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.1, total=  12.8s
[CV] kernel=rbf, C=300.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.3, total=  12.6s
[CV] kernel=rbf, C=300.0, gamma=0.3 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.3, total=  12.7s
[CV] kernel=rbf, C=300.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.3, total=  12.7s
[CV] kernel=rbf, C=300.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.3, total=  12.7s
[CV] kernel=rbf, C=300.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=0.3, total=  12.7s
[CV] kernel=rbf, C=300.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=1.0, total=  12.5s
[CV] kernel=rbf, C=300.0, gamma=1.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=1.0, total=  12.9s
[CV] kernel=rbf, C=300.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=1.0, total=  12.6s
[CV] kernel=rbf, C=300.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=1.0, total=  12.5s
[CV] kernel=rbf, C=300.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=1.0, total=  12.5s
[CV] kernel=rbf, C=300.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=3.0, total=  14.1s
[CV] kernel=rbf, C=300.0, gamma=3.0 ..................................
[CV] ................... kernel=rbf, C=300.0, gamma=3.0, total=  13.8s
[CV] kernel=rbf, C=1000.0, gamma=0.01 ................................
[CV] ................... kernel=rbf, C=300.0, gamma=3.0, total=  13.8s
[CV] kernel=rbf, C=1000.0, gamma=0.01 ................................
[CV] ................... kernel=rbf, C=300.0, gamma=3.0, total=  13.8s
[CV] kernel=rbf, C=1000.0, gamma=0.01 ................................
[CV] ................... kernel=rbf, C=300.0, gamma=3.0, total=  14.0s
[CV] kernel=rbf, C=1000.0, gamma=0.01 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.01, total=  12.9s
[CV] kernel=rbf, C=1000.0, gamma=0.01 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.01, total=  13.0s
[CV] kernel=rbf, C=1000.0, gamma=0.03 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.01, total=  12.9s
[CV] kernel=rbf, C=1000.0, gamma=0.03 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.01, total=  13.1s
[CV] kernel=rbf, C=1000.0, gamma=0.03 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.01, total=  13.0s
[CV] kernel=rbf, C=1000.0, gamma=0.03 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.03, total=  12.7s
[CV] kernel=rbf, C=1000.0, gamma=0.03 ................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.03, total=  12.7s
[CV] kernel=rbf, C=1000.0, gamma=0.1 .................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.03, total=  12.7s
[CV] kernel=rbf, C=1000.0, gamma=0.1 .................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.03, total=  12.8s
[CV] kernel=rbf, C=1000.0, gamma=0.1 .................................
[CV] ................. kernel=rbf, C=1000.0, gamma=0.03, total=  12.7s
[CV] kernel=rbf, C=1000.0, gamma=0.1 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.1, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=0.1 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.1, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=0.3 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.1, total=  12.7s
[CV] kernel=rbf, C=1000.0, gamma=0.3 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.1, total=  12.6s
[CV] kernel=rbf, C=1000.0, gamma=0.3 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.1, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=0.3 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.3, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=0.3 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.3, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=1.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.3, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=1.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.3, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=1.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=0.3, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=1.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=1.0, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=1.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=1.0, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=3.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=1.0, total=  12.4s
[CV] kernel=rbf, C=1000.0, gamma=3.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=1.0, total=  12.5s
[CV] kernel=rbf, C=1000.0, gamma=3.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=1.0, total=  12.4s
[CV] kernel=rbf, C=1000.0, gamma=3.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=3.0, total=  13.8s
[CV] kernel=rbf, C=1000.0, gamma=3.0 .................................
[CV] .................. kernel=rbf, C=1000.0, gamma=3.0, total=  13.8s
[CV] .................. kernel=rbf, C=1000.0, gamma=3.0, total=  13.6s
[CV] .................. kernel=rbf, C=1000.0, gamma=3.0, total=  13.6s
[CV] .................. kernel=rbf, C=1000.0, gamma=3.0, total=  13.3s


[Parallel(n_jobs=4)]: Done 250 out of 250 | elapsed: 19.5min finished





GridSearchCV(cv=5, error_score='raise',
       estimator=SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False),
       fit_params=None, iid=True, n_jobs=4,
       param_grid=[{u'kernel': [u'linear'], u'C': [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0]}, {u'kernel': [u'rbf'], u'C': [1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0], u'gamma': [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]}],
       pre_dispatch='2*n_jobs', refit=True, return_train_score='warn',
       scoring=u'neg_mean_squared_error', verbose=2)
</code></pre>
<p>The best model achieves the following score (evaluated using 5-fold cross validation):</p>
<pre class=" language-python"><code class="prism  language-python">negative_mse <span class="token operator">=</span> grid_search<span class="token punctuation">.</span>best_score_
rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>negative_mse<span class="token punctuation">)</span>
rmse
</code></pre>
<pre><code>70363.903139641669
</code></pre>
<p>That’s much worse than the <code>RandomForestRegressor</code>. Let’s check the best hyperparameters found:</p>
<pre class=" language-python"><code class="prism  language-python">grid_search<span class="token punctuation">.</span>best_params_
</code></pre>
<pre><code>{u'C': 30000.0, u'kernel': u'linear'}
</code></pre>
<p>The linear kernel seems better than the RBF kernel. Notice that the value of <code>C</code> is the maximum tested value. When this happens you definitely want to launch the grid search again with higher values for <code>C</code> (removing the smallest values), because it is likely that higher values of <code>C</code> will be better.</p>
<h2 id="section-1">2.</h2>
<p>Question: Try replacing <code>GridSearchCV</code> with <code>RandomizedSearchCV</code>.</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> RandomizedSearchCV
<span class="token keyword">from</span> scipy<span class="token punctuation">.</span>stats <span class="token keyword">import</span> expon<span class="token punctuation">,</span> reciprocal

<span class="token comment"># see https://docs.scipy.org/doc/scipy-0.19.0/reference/stats.html</span>
<span class="token comment"># for `expon()` and `reciprocal()` documentation and more probability distribution functions.</span>

<span class="token comment"># Note: gamma is ignored when kernel is "linear"</span>
param_distribs <span class="token operator">=</span> <span class="token punctuation">{</span>
        <span class="token string">'kernel'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">'linear'</span><span class="token punctuation">,</span> <span class="token string">'rbf'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string">'C'</span><span class="token punctuation">:</span> reciprocal<span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">,</span> <span class="token number">200000</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string">'gamma'</span><span class="token punctuation">:</span> expon<span class="token punctuation">(</span>scale<span class="token operator">=</span><span class="token number">1.0</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>

svm_reg <span class="token operator">=</span> SVR<span class="token punctuation">(</span><span class="token punctuation">)</span>
rnd_search <span class="token operator">=</span> RandomizedSearchCV<span class="token punctuation">(</span>svm_reg<span class="token punctuation">,</span> param_distributions<span class="token operator">=</span>param_distribs<span class="token punctuation">,</span>
                                n_iter<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">5</span><span class="token punctuation">,</span> scoring<span class="token operator">=</span><span class="token string">'neg_mean_squared_error'</span><span class="token punctuation">,</span>
                                verbose<span class="token operator">=</span><span class="token number">2</span><span class="token punctuation">,</span> n_jobs<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
rnd_search<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing_prepared<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>Fitting 5 folds for each of 50 candidates, totalling 250 fits
[CV] kernel=linear, C=629.782329591, gamma=3.01012143092 .............
[CV] kernel=linear, C=629.782329591, gamma=3.01012143092 .............
[CV] kernel=linear, C=629.782329591, gamma=3.01012143092 .............
[CV] kernel=linear, C=629.782329591, gamma=3.01012143092 .............
[CV]  kernel=linear, C=629.782329591, gamma=3.01012143092, total=   8.1s
[CV] kernel=linear, C=629.782329591, gamma=3.01012143092 .............
[CV]  kernel=linear, C=629.782329591, gamma=3.01012143092, total=   8.2s
[CV] kernel=rbf, C=26290.2064643, gamma=0.908446969632 ...............
[CV]  kernel=linear, C=629.782329591, gamma=3.01012143092, total=   8.2s
[CV] kernel=rbf, C=26290.2064643, gamma=0.908446969632 ...............
[CV]  kernel=linear, C=629.782329591, gamma=3.01012143092, total=   8.2s
[CV] kernel=rbf, C=26290.2064643, gamma=0.908446969632 ...............
[CV]  kernel=linear, C=629.782329591, gamma=3.01012143092, total=   7.9s
[CV] kernel=rbf, C=26290.2064643, gamma=0.908446969632 ...............
[CV]  kernel=rbf, C=26290.2064643, gamma=0.908446969632, total=  25.5s
[CV] kernel=rbf, C=26290.2064643, gamma=0.908446969632 ...............
[CV]  kernel=rbf, C=26290.2064643, gamma=0.908446969632, total=  26.0s
[CV] kernel=rbf, C=84.1410790058, gamma=0.0598387686087 ..............
[CV]  kernel=rbf, C=26290.2064643, gamma=0.908446969632, total=  25.8s
[CV] kernel=rbf, C=84.1410790058, gamma=0.0598387686087 ..............
[CV]  kernel=rbf, C=26290.2064643, gamma=0.908446969632, total=  26.0s
[CV] kernel=rbf, C=84.1410790058, gamma=0.0598387686087 ..............
[CV]  kernel=rbf, C=84.1410790058, gamma=0.0598387686087, total=  13.3s
[CV] kernel=rbf, C=84.1410790058, gamma=0.0598387686087 ..............
[CV]  kernel=rbf, C=84.1410790058, gamma=0.0598387686087, total=  13.2s
[CV] kernel=rbf, C=84.1410790058, gamma=0.0598387686087 ..............
[CV]  kernel=rbf, C=26290.2064643, gamma=0.908446969632, total=  16.1s
[CV] kernel=linear, C=432.378848131, gamma=0.154161967467 ............
[CV]  kernel=rbf, C=84.1410790058, gamma=0.0598387686087, total=  13.3s
[CV] kernel=linear, C=432.378848131, gamma=0.154161967467 ............
[CV]  kernel=linear, C=432.378848131, gamma=0.154161967467, total=   7.9s
[CV] kernel=linear, C=432.378848131, gamma=0.154161967467 ............
[CV]  kernel=rbf, C=84.1410790058, gamma=0.0598387686087, total=  13.3s
[CV] kernel=linear, C=432.378848131, gamma=0.154161967467 ............
[CV]  kernel=rbf, C=84.1410790058, gamma=0.0598387686087, total=  13.3s
[CV] kernel=linear, C=432.378848131, gamma=0.154161967467 ............
[CV]  kernel=linear, C=432.378848131, gamma=0.154161967467, total=   8.0s
[CV] kernel=rbf, C=24.1750829461, gamma=3.50355747516 ................
[CV]  kernel=linear, C=432.378848131, gamma=0.154161967467, total=   8.1s
[CV] kernel=rbf, C=24.1750829461, gamma=3.50355747516 ................
[CV]  kernel=linear, C=432.378848131, gamma=0.154161967467, total=   8.0s
[CV] kernel=rbf, C=24.1750829461, gamma=3.50355747516 ................
[CV]  kernel=linear, C=432.378848131, gamma=0.154161967467, total=   8.1s
[CV] kernel=rbf, C=24.1750829461, gamma=3.50355747516 ................
[CV] . kernel=rbf, C=24.1750829461, gamma=3.50355747516, total=  14.6s
[CV] kernel=rbf, C=24.1750829461, gamma=3.50355747516 ................
[CV] . kernel=rbf, C=24.1750829461, gamma=3.50355747516, total=  14.4s
[CV] kernel=rbf, C=113564.039406, gamma=0.000779069236658 ............
[CV] . kernel=rbf, C=24.1750829461, gamma=3.50355747516, total=  14.3s
[CV] kernel=rbf, C=113564.039406, gamma=0.000779069236658 ............
[CV] . kernel=rbf, C=24.1750829461, gamma=3.50355747516, total=  14.4s
[CV] kernel=rbf, C=113564.039406, gamma=0.000779069236658 ............
[CV] . kernel=rbf, C=24.1750829461, gamma=3.50355747516, total=  14.5s
[CV] kernel=rbf, C=113564.039406, gamma=0.000779069236658 ............
[CV]  kernel=rbf, C=113564.039406, gamma=0.000779069236658, total=  12.7s
[CV] kernel=rbf, C=113564.039406, gamma=0.000779069236658 ............
[CV]  kernel=rbf, C=113564.039406, gamma=0.000779069236658, total=  12.8s
[CV] kernel=rbf, C=108.304882388, gamma=0.36275372946 ................
[CV]  kernel=rbf, C=113564.039406, gamma=0.000779069236658, total=  12.8s
[CV] kernel=rbf, C=108.304882388, gamma=0.36275372946 ................
[CV]  kernel=rbf, C=113564.039406, gamma=0.000779069236658, total=  12.8s
[CV] kernel=rbf, C=108.304882388, gamma=0.36275372946 ................
[CV]  kernel=rbf, C=113564.039406, gamma=0.000779069236658, total=  12.8s
[CV] kernel=rbf, C=108.304882388, gamma=0.36275372946 ................
[CV] . kernel=rbf, C=108.304882388, gamma=0.36275372946, total=  12.7s
[CV] kernel=rbf, C=108.304882388, gamma=0.36275372946 ................
[CV] . kernel=rbf, C=108.304882388, gamma=0.36275372946, total=  12.7s
[CV] kernel=linear, C=21.3449536726, gamma=0.0233325235983 ...........
[CV]  kernel=linear, C=21.3449536726, gamma=0.0233325235983, total=   7.9s
[CV] kernel=linear, C=21.3449536726, gamma=0.0233325235983 ...........


[Parallel(n_jobs=4)]: Done  33 tasks      | elapsed:  2.6min


[CV] . kernel=rbf, C=108.304882388, gamma=0.36275372946, total=  12.8s
[CV] kernel=linear, C=21.3449536726, gamma=0.0233325235983 ...........
[CV] . kernel=rbf, C=108.304882388, gamma=0.36275372946, total=  12.8s
[CV] kernel=linear, C=21.3449536726, gamma=0.0233325235983 ...........
[CV] . kernel=rbf, C=108.304882388, gamma=0.36275372946, total=  12.7s
[CV] kernel=linear, C=21.3449536726, gamma=0.0233325235983 ...........
[CV]  kernel=linear, C=21.3449536726, gamma=0.0233325235983, total=   8.1s
[CV] kernel=rbf, C=5603.27031743, gamma=0.150234528727 ...............
[CV]  kernel=linear, C=21.3449536726, gamma=0.0233325235983, total=   8.0s
[CV] kernel=rbf, C=5603.27031743, gamma=0.150234528727 ...............
[CV]  kernel=linear, C=21.3449536726, gamma=0.0233325235983, total=   8.0s
[CV] kernel=rbf, C=5603.27031743, gamma=0.150234528727 ...............
[CV]  kernel=linear, C=21.3449536726, gamma=0.0233325235983, total=   8.1s
[CV] kernel=rbf, C=5603.27031743, gamma=0.150234528727 ...............
[CV]  kernel=rbf, C=5603.27031743, gamma=0.150234528727, total=  12.5s
[CV] kernel=rbf, C=5603.27031743, gamma=0.150234528727 ...............
[CV]  kernel=rbf, C=5603.27031743, gamma=0.150234528727, total=  12.6s
[CV] kernel=rbf, C=157055.109894, gamma=0.26497040005 ................
[CV]  kernel=rbf, C=5603.27031743, gamma=0.150234528727, total=  12.5s
[CV] kernel=rbf, C=157055.109894, gamma=0.26497040005 ................
[CV]  kernel=rbf, C=5603.27031743, gamma=0.150234528727, total=  12.4s
[CV] kernel=rbf, C=157055.109894, gamma=0.26497040005 ................
[CV]  kernel=rbf, C=5603.27031743, gamma=0.150234528727, total=  12.5s
[CV] kernel=rbf, C=157055.109894, gamma=0.26497040005 ................
[CV] . kernel=rbf, C=157055.109894, gamma=0.26497040005, total=  30.4s
[CV] kernel=rbf, C=157055.109894, gamma=0.26497040005 ................
[CV] . kernel=rbf, C=157055.109894, gamma=0.26497040005, total=  31.8s
[CV] kernel=linear, C=27652.4643587, gamma=0.222735862129 ............
[CV] . kernel=rbf, C=157055.109894, gamma=0.26497040005, total=  36.9s
[CV] kernel=linear, C=27652.4643587, gamma=0.222735862129 ............
[CV] . kernel=rbf, C=157055.109894, gamma=0.26497040005, total=  29.5s
[CV] kernel=linear, C=27652.4643587, gamma=0.222735862129 ............
[CV]  kernel=linear, C=27652.4643587, gamma=0.222735862129, total=  17.4s
[CV] kernel=linear, C=27652.4643587, gamma=0.222735862129 ............
[CV]  kernel=linear, C=27652.4643587, gamma=0.222735862129, total=  18.0s
[CV] kernel=linear, C=27652.4643587, gamma=0.222735862129 ............
[CV]  kernel=linear, C=27652.4643587, gamma=0.222735862129, total=  19.0s
[CV] kernel=linear, C=171377.395704, gamma=0.628789100541 ............
[CV] . kernel=rbf, C=157055.109894, gamma=0.26497040005, total=  32.9s
[CV] kernel=linear, C=171377.395704, gamma=0.628789100541 ............
[CV]  kernel=linear, C=27652.4643587, gamma=0.222735862129, total=  17.3s
[CV] kernel=linear, C=171377.395704, gamma=0.628789100541 ............
[CV]  kernel=linear, C=27652.4643587, gamma=0.222735862129, total=  15.3s
[CV] kernel=linear, C=171377.395704, gamma=0.628789100541 ............
[CV]  kernel=linear, C=171377.395704, gamma=0.628789100541, total=  56.4s
[CV] kernel=linear, C=171377.395704, gamma=0.628789100541 ............
[CV]  kernel=linear, C=171377.395704, gamma=0.628789100541, total= 1.2min
[CV] kernel=linear, C=5385.29382017, gamma=0.186961251977 ............
[CV]  kernel=linear, C=171377.395704, gamma=0.628789100541, total= 1.2min
[CV] kernel=linear, C=5385.29382017, gamma=0.186961251977 ............
[CV]  kernel=linear, C=171377.395704, gamma=0.628789100541, total= 1.0min
[CV] kernel=linear, C=5385.29382017, gamma=0.186961251977 ............
[CV]  kernel=linear, C=5385.29382017, gamma=0.186961251977, total=   9.6s
[CV] kernel=linear, C=5385.29382017, gamma=0.186961251977 ............
[CV]  kernel=linear, C=5385.29382017, gamma=0.186961251977, total=   9.8s
[CV] kernel=linear, C=5385.29382017, gamma=0.186961251977 ............
[CV]  kernel=linear, C=5385.29382017, gamma=0.186961251977, total=   9.9s
[CV] kernel=rbf, C=22.5990321662, gamma=2.85079687894 ................
[CV]  kernel=linear, C=5385.29382017, gamma=0.186961251977, total=   9.5s
[CV] kernel=rbf, C=22.5990321662, gamma=2.85079687894 ................
[CV]  kernel=linear, C=5385.29382017, gamma=0.186961251977, total=   9.6s
[CV] kernel=rbf, C=22.5990321662, gamma=2.85079687894 ................
[CV] . kernel=rbf, C=22.5990321662, gamma=2.85079687894, total=  13.5s
[CV] kernel=rbf, C=22.5990321662, gamma=2.85079687894 ................
[CV]  kernel=linear, C=171377.395704, gamma=0.628789100541, total=  49.5s
[CV] kernel=rbf, C=22.5990321662, gamma=2.85079687894 ................
[CV] . kernel=rbf, C=22.5990321662, gamma=2.85079687894, total=  13.6s
[CV] kernel=linear, C=34246.7519463, gamma=0.363287859969 ............
[CV] . kernel=rbf, C=22.5990321662, gamma=2.85079687894, total=  13.4s
[CV] kernel=linear, C=34246.7519463, gamma=0.363287859969 ............
[CV] . kernel=rbf, C=22.5990321662, gamma=2.85079687894, total=  13.6s
[CV] kernel=linear, C=34246.7519463, gamma=0.363287859969 ............
[CV] . kernel=rbf, C=22.5990321662, gamma=2.85079687894, total=  13.7s
[CV] kernel=linear, C=34246.7519463, gamma=0.363287859969 ............
[CV]  kernel=linear, C=34246.7519463, gamma=0.363287859969, total=  21.0s
[CV] kernel=linear, C=34246.7519463, gamma=0.363287859969 ............
[CV]  kernel=linear, C=34246.7519463, gamma=0.363287859969, total=  20.5s
[CV] kernel=rbf, C=167.727895608, gamma=0.275787054226 ...............
[CV]  kernel=linear, C=34246.7519463, gamma=0.363287859969, total=  22.0s
[CV] kernel=rbf, C=167.727895608, gamma=0.275787054226 ...............
[CV]  kernel=linear, C=34246.7519463, gamma=0.363287859969, total=  20.9s
[CV] kernel=rbf, C=167.727895608, gamma=0.275787054226 ...............
[CV]  kernel=rbf, C=167.727895608, gamma=0.275787054226, total=  13.0s
[CV] kernel=rbf, C=167.727895608, gamma=0.275787054226 ...............
[CV]  kernel=linear, C=34246.7519463, gamma=0.363287859969, total=  18.7s
[CV] kernel=rbf, C=167.727895608, gamma=0.275787054226 ...............
[CV]  kernel=rbf, C=167.727895608, gamma=0.275787054226, total=  12.8s
[CV] kernel=linear, C=61.543605425, gamma=0.683547228134 .............
[CV]  kernel=rbf, C=167.727895608, gamma=0.275787054226, total=  13.0s
[CV] kernel=linear, C=61.543605425, gamma=0.683547228134 .............
[CV]  kernel=rbf, C=167.727895608, gamma=0.275787054226, total=  12.9s
[CV] kernel=linear, C=61.543605425, gamma=0.683547228134 .............
[CV]  kernel=rbf, C=167.727895608, gamma=0.275787054226, total=  12.9s
[CV] kernel=linear, C=61.543605425, gamma=0.683547228134 .............
[CV]  kernel=linear, C=61.543605425, gamma=0.683547228134, total=   8.4s
[CV] kernel=linear, C=61.543605425, gamma=0.683547228134 .............
[CV]  kernel=linear, C=61.543605425, gamma=0.683547228134, total=   8.2s
[CV] kernel=rbf, C=98.7389738992, gamma=0.496036536049 ...............
[CV]  kernel=linear, C=61.543605425, gamma=0.683547228134, total=   8.2s
[CV] kernel=rbf, C=98.7389738992, gamma=0.496036536049 ...............
[CV]  kernel=linear, C=61.543605425, gamma=0.683547228134, total=   8.1s
[CV] kernel=rbf, C=98.7389738992, gamma=0.496036536049 ...............
[CV]  kernel=linear, C=61.543605425, gamma=0.683547228134, total=   8.1s
[CV] kernel=rbf, C=98.7389738992, gamma=0.496036536049 ...............
[CV]  kernel=rbf, C=98.7389738992, gamma=0.496036536049, total=  12.9s
[CV] kernel=rbf, C=98.7389738992, gamma=0.496036536049 ...............
[CV]  kernel=rbf, C=98.7389738992, gamma=0.496036536049, total=  12.9s
[CV] kernel=rbf, C=8935.50563595, gamma=0.373546581658 ...............
[CV]  kernel=rbf, C=98.7389738992, gamma=0.496036536049, total=  12.9s
[CV] kernel=rbf, C=8935.50563595, gamma=0.373546581658 ...............
[CV]  kernel=rbf, C=98.7389738992, gamma=0.496036536049, total=  13.1s
[CV] kernel=rbf, C=8935.50563595, gamma=0.373546581658 ...............
[CV]  kernel=rbf, C=98.7389738992, gamma=0.496036536049, total=  13.2s
[CV] kernel=rbf, C=8935.50563595, gamma=0.373546581658 ...............
[CV]  kernel=rbf, C=8935.50563595, gamma=0.373546581658, total=  13.0s
[CV] kernel=rbf, C=8935.50563595, gamma=0.373546581658 ...............
[CV]  kernel=rbf, C=8935.50563595, gamma=0.373546581658, total=  13.0s
[CV] kernel=linear, C=135.767758248, gamma=0.838636245625 ............
[CV]  kernel=rbf, C=8935.50563595, gamma=0.373546581658, total=  13.3s
[CV] kernel=linear, C=135.767758248, gamma=0.838636245625 ............
[CV]  kernel=linear, C=135.767758248, gamma=0.838636245625, total=   8.1s
[CV] kernel=linear, C=135.767758248, gamma=0.838636245625 ............
[CV]  kernel=rbf, C=8935.50563595, gamma=0.373546581658, total=  13.0s
[CV] kernel=linear, C=135.767758248, gamma=0.838636245625 ............
[CV]  kernel=linear, C=135.767758248, gamma=0.838636245625, total=   8.2s
[CV] kernel=linear, C=135.767758248, gamma=0.838636245625 ............
[CV]  kernel=rbf, C=8935.50563595, gamma=0.373546581658, total=  12.9s
[CV] kernel=rbf, C=151136.202825, gamma=1.49224537714 ................
[CV]  kernel=linear, C=135.767758248, gamma=0.838636245625, total=   8.2s
[CV] kernel=rbf, C=151136.202825, gamma=1.49224537714 ................
[CV]  kernel=linear, C=135.767758248, gamma=0.838636245625, total=   7.9s
[CV] kernel=rbf, C=151136.202825, gamma=1.49224537714 ................
[CV]  kernel=linear, C=135.767758248, gamma=0.838636245625, total=   8.2s
[CV] kernel=rbf, C=151136.202825, gamma=1.49224537714 ................
[CV] . kernel=rbf, C=151136.202825, gamma=1.49224537714, total= 2.1min
[CV] kernel=rbf, C=151136.202825, gamma=1.49224537714 ................
[CV] . kernel=rbf, C=151136.202825, gamma=1.49224537714, total= 2.2min
[CV] kernel=linear, C=761.43167585, gamma=2.61263365142 ..............
[CV]  kernel=linear, C=761.43167585, gamma=2.61263365142, total=   7.9s
[CV] kernel=linear, C=761.43167585, gamma=2.61263365142 ..............
[CV]  kernel=linear, C=761.43167585, gamma=2.61263365142, total=   8.0s
[CV] kernel=linear, C=761.43167585, gamma=2.61263365142 ..............
[CV] . kernel=rbf, C=151136.202825, gamma=1.49224537714, total= 2.6min
[CV] kernel=linear, C=761.43167585, gamma=2.61263365142 ..............
[CV]  kernel=linear, C=761.43167585, gamma=2.61263365142, total=   8.1s
[CV] kernel=linear, C=761.43167585, gamma=2.61263365142 ..............
[CV]  kernel=linear, C=761.43167585, gamma=2.61263365142, total=   7.9s
[CV] kernel=linear, C=97392.8188304, gamma=0.0926554589531 ...........
[CV]  kernel=linear, C=761.43167585, gamma=2.61263365142, total=   8.0s
[CV] kernel=linear, C=97392.8188304, gamma=0.0926554589531 ...........
[CV] . kernel=rbf, C=151136.202825, gamma=1.49224537714, total= 2.9min
[CV] kernel=linear, C=97392.8188304, gamma=0.0926554589531 ...........
[CV]  kernel=linear, C=97392.8188304, gamma=0.0926554589531, total=  40.9s
[CV] kernel=linear, C=97392.8188304, gamma=0.0926554589531 ...........
[CV]  kernel=linear, C=97392.8188304, gamma=0.0926554589531, total=  39.7s
[CV] kernel=linear, C=97392.8188304, gamma=0.0926554589531 ...........
[CV]  kernel=linear, C=97392.8188304, gamma=0.0926554589531, total= 1.1min
[CV] kernel=linear, C=2423.07599849, gamma=3.24861427024 .............
[CV]  kernel=linear, C=97392.8188304, gamma=0.0926554589531, total=  34.6s
[CV] kernel=linear, C=2423.07599849, gamma=3.24861427024 .............
[CV]  kernel=linear, C=2423.07599849, gamma=3.24861427024, total=   9.0s
[CV] kernel=linear, C=2423.07599849, gamma=3.24861427024 .............
[CV]  kernel=linear, C=97392.8188304, gamma=0.0926554589531, total=  42.4s
[CV] kernel=linear, C=2423.07599849, gamma=3.24861427024 .............
[CV]  kernel=linear, C=2423.07599849, gamma=3.24861427024, total=   9.4s
[CV] kernel=linear, C=2423.07599849, gamma=3.24861427024 .............
[CV]  kernel=linear, C=2423.07599849, gamma=3.24861427024, total=   9.2s
[CV] kernel=linear, C=717.363299726, gamma=0.316560443209 ............
[CV]  kernel=linear, C=2423.07599849, gamma=3.24861427024, total=   9.4s
[CV] kernel=linear, C=717.363299726, gamma=0.316560443209 ............
[CV]  kernel=linear, C=717.363299726, gamma=0.316560443209, total=   8.4s
[CV] kernel=linear, C=717.363299726, gamma=0.316560443209 ............
[CV]  kernel=linear, C=2423.07599849, gamma=3.24861427024, total=   8.8s
[CV] kernel=linear, C=717.363299726, gamma=0.316560443209 ............
[CV]  kernel=linear, C=717.363299726, gamma=0.316560443209, total=   8.3s
[CV] kernel=linear, C=717.363299726, gamma=0.316560443209 ............
[CV] . kernel=rbf, C=151136.202825, gamma=1.49224537714, total= 2.5min
[CV] kernel=rbf, C=4446.66752118, gamma=3.35972844566 ................
[CV]  kernel=linear, C=717.363299726, gamma=0.316560443209, total=   8.5s
[CV] kernel=rbf, C=4446.66752118, gamma=3.35972844566 ................
[CV]  kernel=linear, C=717.363299726, gamma=0.316560443209, total=   8.6s
[CV] kernel=rbf, C=4446.66752118, gamma=3.35972844566 ................
[CV]  kernel=linear, C=717.363299726, gamma=0.316560443209, total=   8.1s
[CV] kernel=rbf, C=4446.66752118, gamma=3.35972844566 ................
[CV] . kernel=rbf, C=4446.66752118, gamma=3.35972844566, total=  14.6s
[CV] kernel=rbf, C=4446.66752118, gamma=3.35972844566 ................
[CV] . kernel=rbf, C=4446.66752118, gamma=3.35972844566, total=  14.6s
[CV] kernel=linear, C=2963.56412121, gamma=0.151898147821 ............
[CV] . kernel=rbf, C=4446.66752118, gamma=3.35972844566, total=  14.7s
[CV] kernel=linear, C=2963.56412121, gamma=0.151898147821 ............
[CV] . kernel=rbf, C=4446.66752118, gamma=3.35972844566, total=  14.5s
[CV] kernel=linear, C=2963.56412121, gamma=0.151898147821 ............
[CV]  kernel=linear, C=2963.56412121, gamma=0.151898147821, total=   9.0s
[CV] kernel=linear, C=2963.56412121, gamma=0.151898147821 ............
[CV]  kernel=linear, C=2963.56412121, gamma=0.151898147821, total=   9.4s
[CV] kernel=linear, C=2963.56412121, gamma=0.151898147821 ............
[CV]  kernel=linear, C=2963.56412121, gamma=0.151898147821, total=   9.5s
[CV] kernel=linear, C=91.6426738169, gamma=0.0157599448359 ...........
[CV] . kernel=rbf, C=4446.66752118, gamma=3.35972844566, total=  14.7s
[CV] kernel=linear, C=91.6426738169, gamma=0.0157599448359 ...........
[CV]  kernel=linear, C=2963.56412121, gamma=0.151898147821, total=   9.0s
[CV] kernel=linear, C=91.6426738169, gamma=0.0157599448359 ...........
[CV]  kernel=linear, C=2963.56412121, gamma=0.151898147821, total=   9.0s
[CV] kernel=linear, C=91.6426738169, gamma=0.0157599448359 ...........
[CV]  kernel=linear, C=91.6426738169, gamma=0.0157599448359, total=   7.8s
[CV] kernel=linear, C=91.6426738169, gamma=0.0157599448359 ...........
[CV]  kernel=linear, C=91.6426738169, gamma=0.0157599448359, total=   8.0s
[CV] kernel=rbf, C=24547.6019757, gamma=0.221539440506 ...............
[CV]  kernel=linear, C=91.6426738169, gamma=0.0157599448359, total=   8.1s
[CV] kernel=rbf, C=24547.6019757, gamma=0.221539440506 ...............
[CV]  kernel=linear, C=91.6426738169, gamma=0.0157599448359, total=   7.7s
[CV] kernel=rbf, C=24547.6019757, gamma=0.221539440506 ...............
[CV]  kernel=linear, C=91.6426738169, gamma=0.0157599448359, total=   8.1s
[CV] kernel=rbf, C=24547.6019757, gamma=0.221539440506 ...............
[CV]  kernel=rbf, C=24547.6019757, gamma=0.221539440506, total=  13.6s
[CV] kernel=rbf, C=24547.6019757, gamma=0.221539440506 ...............
[CV]  kernel=rbf, C=24547.6019757, gamma=0.221539440506, total=  13.3s
[CV] kernel=rbf, C=22.7692794106, gamma=0.221697602314 ...............
[CV]  kernel=rbf, C=24547.6019757, gamma=0.221539440506, total=  13.3s
[CV] kernel=rbf, C=22.7692794106, gamma=0.221697602314 ...............
[CV]  kernel=rbf, C=24547.6019757, gamma=0.221539440506, total=  13.3s
[CV] kernel=rbf, C=22.7692794106, gamma=0.221697602314 ...............
[CV]  kernel=rbf, C=24547.6019757, gamma=0.221539440506, total=  13.5s
[CV] kernel=rbf, C=22.7692794106, gamma=0.221697602314 ...............
[CV]  kernel=rbf, C=22.7692794106, gamma=0.221697602314, total=  13.2s
[CV] kernel=rbf, C=22.7692794106, gamma=0.221697602314 ...............
[CV]  kernel=rbf, C=22.7692794106, gamma=0.221697602314, total=  13.1s
[CV] kernel=linear, C=16483.8505298, gamma=1.47521452604 .............
[CV]  kernel=rbf, C=22.7692794106, gamma=0.221697602314, total=  13.2s
[CV] kernel=linear, C=16483.8505298, gamma=1.47521452604 .............
[CV]  kernel=linear, C=16483.8505298, gamma=1.47521452604, total=  13.0s
[CV] kernel=linear, C=16483.8505298, gamma=1.47521452604 .............
[CV]  kernel=linear, C=16483.8505298, gamma=1.47521452604, total=  14.1s
[CV] kernel=linear, C=16483.8505298, gamma=1.47521452604 .............
[CV]  kernel=rbf, C=22.7692794106, gamma=0.221697602314, total=  13.1s
[CV] kernel=linear, C=16483.8505298, gamma=1.47521452604 .............
[CV]  kernel=rbf, C=22.7692794106, gamma=0.221697602314, total=  13.0s
[CV] kernel=rbf, C=101445.668813, gamma=1.05290408458 ................
[CV]  kernel=linear, C=16483.8505298, gamma=1.47521452604, total=  14.3s
[CV] kernel=rbf, C=101445.668813, gamma=1.05290408458 ................
[CV]  kernel=linear, C=16483.8505298, gamma=1.47521452604, total=  12.4s
[CV] kernel=rbf, C=101445.668813, gamma=1.05290408458 ................


[Parallel(n_jobs=4)]: Done 154 tasks      | elapsed: 15.4min


[CV]  kernel=linear, C=16483.8505298, gamma=1.47521452604, total=  14.7s
[CV] kernel=rbf, C=101445.668813, gamma=1.05290408458 ................
[CV] . kernel=rbf, C=101445.668813, gamma=1.05290408458, total=  59.7s
[CV] kernel=rbf, C=101445.668813, gamma=1.05290408458 ................
[CV] . kernel=rbf, C=101445.668813, gamma=1.05290408458, total=  57.7s
[CV] kernel=rbf, C=56681.8085903, gamma=0.976301191712 ...............
[CV] . kernel=rbf, C=101445.668813, gamma=1.05290408458, total= 1.2min
[CV] kernel=rbf, C=56681.8085903, gamma=0.976301191712 ...............
[CV] . kernel=rbf, C=101445.668813, gamma=1.05290408458, total= 1.3min
[CV] kernel=rbf, C=56681.8085903, gamma=0.976301191712 ...............
[CV]  kernel=rbf, C=56681.8085903, gamma=0.976301191712, total=  25.2s
[CV] kernel=rbf, C=56681.8085903, gamma=0.976301191712 ...............
[CV]  kernel=rbf, C=56681.8085903, gamma=0.976301191712, total=  25.3s
[CV] kernel=rbf, C=56681.8085903, gamma=0.976301191712 ...............
[CV]  kernel=rbf, C=56681.8085903, gamma=0.976301191712, total=  24.7s
[CV] kernel=rbf, C=48.1582239093, gamma=0.463335116798 ...............
[CV] . kernel=rbf, C=101445.668813, gamma=1.05290408458, total= 1.0min
[CV] kernel=rbf, C=48.1582239093, gamma=0.463335116798 ...............
[CV]  kernel=rbf, C=56681.8085903, gamma=0.976301191712, total=  28.0s
[CV] kernel=rbf, C=48.1582239093, gamma=0.463335116798 ...............
[CV]  kernel=rbf, C=48.1582239093, gamma=0.463335116798, total=  12.7s
[CV] kernel=rbf, C=48.1582239093, gamma=0.463335116798 ...............
[CV]  kernel=rbf, C=48.1582239093, gamma=0.463335116798, total=  12.8s
[CV] kernel=rbf, C=48.1582239093, gamma=0.463335116798 ...............
[CV]  kernel=rbf, C=56681.8085903, gamma=0.976301191712, total=  27.3s
[CV] kernel=rbf, C=399.726815571, gamma=1.30787578396 ................
[CV]  kernel=rbf, C=48.1582239093, gamma=0.463335116798, total=  12.8s
[CV] kernel=rbf, C=399.726815571, gamma=1.30787578396 ................
[CV]  kernel=rbf, C=48.1582239093, gamma=0.463335116798, total=  12.8s
[CV] kernel=rbf, C=399.726815571, gamma=1.30787578396 ................
[CV]  kernel=rbf, C=48.1582239093, gamma=0.463335116798, total=  12.8s
[CV] kernel=rbf, C=399.726815571, gamma=1.30787578396 ................
[CV] . kernel=rbf, C=399.726815571, gamma=1.30787578396, total=  12.6s
[CV] kernel=rbf, C=399.726815571, gamma=1.30787578396 ................
[CV] . kernel=rbf, C=399.726815571, gamma=1.30787578396, total=  12.6s
[CV] kernel=linear, C=251.140738863, gamma=0.823810520491 ............
[CV] . kernel=rbf, C=399.726815571, gamma=1.30787578396, total=  12.7s
[CV] kernel=linear, C=251.140738863, gamma=0.823810520491 ............
[CV]  kernel=linear, C=251.140738863, gamma=0.823810520491, total=   7.9s
[CV] kernel=linear, C=251.140738863, gamma=0.823810520491 ............
[CV] . kernel=rbf, C=399.726815571, gamma=1.30787578396, total=  12.6s
[CV] kernel=linear, C=251.140738863, gamma=0.823810520491 ............
[CV] . kernel=rbf, C=399.726815571, gamma=1.30787578396, total=  12.7s
[CV] kernel=linear, C=251.140738863, gamma=0.823810520491 ............
[CV]  kernel=linear, C=251.140738863, gamma=0.823810520491, total=   8.1s
[CV] kernel=linear, C=60.1737364289, gamma=1.24912634432 .............
[CV]  kernel=linear, C=251.140738863, gamma=0.823810520491, total=   8.2s
[CV] kernel=linear, C=60.1737364289, gamma=1.24912634432 .............
[CV]  kernel=linear, C=251.140738863, gamma=0.823810520491, total=   8.2s
[CV] kernel=linear, C=60.1737364289, gamma=1.24912634432 .............
[CV]  kernel=linear, C=251.140738863, gamma=0.823810520491, total=   8.3s
[CV] kernel=linear, C=60.1737364289, gamma=1.24912634432 .............
[CV]  kernel=linear, C=60.1737364289, gamma=1.24912634432, total=   8.5s
[CV] kernel=linear, C=60.1737364289, gamma=1.24912634432 .............
[CV]  kernel=linear, C=60.1737364289, gamma=1.24912634432, total=   8.5s
[CV] kernel=rbf, C=15415.1615449, gamma=0.269167751462 ...............
[CV]  kernel=linear, C=60.1737364289, gamma=1.24912634432, total=   9.0s
[CV] kernel=rbf, C=15415.1615449, gamma=0.269167751462 ...............
[CV]  kernel=linear, C=60.1737364289, gamma=1.24912634432, total=   8.9s
[CV] kernel=rbf, C=15415.1615449, gamma=0.269167751462 ...............
[CV]  kernel=linear, C=60.1737364289, gamma=1.24912634432, total=   8.8s
[CV] kernel=rbf, C=15415.1615449, gamma=0.269167751462 ...............
[CV]  kernel=rbf, C=15415.1615449, gamma=0.269167751462, total=  13.5s
[CV] kernel=rbf, C=15415.1615449, gamma=0.269167751462 ...............
[CV]  kernel=rbf, C=15415.1615449, gamma=0.269167751462, total=  13.4s
[CV] kernel=linear, C=1888.914851, gamma=0.739678838777 ..............
[CV]  kernel=rbf, C=15415.1615449, gamma=0.269167751462, total=  13.2s
[CV] kernel=linear, C=1888.914851, gamma=0.739678838777 ..............
[CV]  kernel=rbf, C=15415.1615449, gamma=0.269167751462, total=  13.1s
[CV] kernel=linear, C=1888.914851, gamma=0.739678838777 ..............
[CV]  kernel=linear, C=1888.914851, gamma=0.739678838777, total=   9.0s
[CV] kernel=linear, C=1888.914851, gamma=0.739678838777 ..............
[CV]  kernel=linear, C=1888.914851, gamma=0.739678838777, total=   9.3s
[CV] kernel=linear, C=1888.914851, gamma=0.739678838777 ..............
[CV]  kernel=linear, C=1888.914851, gamma=0.739678838777, total=   9.3s
[CV] kernel=linear, C=55.5383891123, gamma=0.578634378499 ............
[CV]  kernel=rbf, C=15415.1615449, gamma=0.269167751462, total=  13.6s
[CV] kernel=linear, C=55.5383891123, gamma=0.578634378499 ............
[CV]  kernel=linear, C=1888.914851, gamma=0.739678838777, total=   8.7s
[CV] kernel=linear, C=55.5383891123, gamma=0.578634378499 ............
[CV]  kernel=linear, C=1888.914851, gamma=0.739678838777, total=   8.7s
[CV] kernel=linear, C=55.5383891123, gamma=0.578634378499 ............
[CV]  kernel=linear, C=55.5383891123, gamma=0.578634378499, total=   8.1s
[CV] kernel=linear, C=55.5383891123, gamma=0.578634378499 ............
[CV]  kernel=linear, C=55.5383891123, gamma=0.578634378499, total=   8.1s
[CV] kernel=rbf, C=26.7144808239, gamma=1.01172955093 ................
[CV]  kernel=linear, C=55.5383891123, gamma=0.578634378499, total=   8.1s
[CV] kernel=rbf, C=26.7144808239, gamma=1.01172955093 ................
[CV]  kernel=linear, C=55.5383891123, gamma=0.578634378499, total=   7.9s
[CV] kernel=rbf, C=26.7144808239, gamma=1.01172955093 ................
[CV]  kernel=linear, C=55.5383891123, gamma=0.578634378499, total=   7.8s
[CV] kernel=rbf, C=26.7144808239, gamma=1.01172955093 ................
[CV] . kernel=rbf, C=26.7144808239, gamma=1.01172955093, total=  12.9s
[CV] kernel=rbf, C=26.7144808239, gamma=1.01172955093 ................
[CV] . kernel=rbf, C=26.7144808239, gamma=1.01172955093, total=  13.0s
[CV] kernel=linear, C=3582.05527805, gamma=1.18913702221 .............
[CV] . kernel=rbf, C=26.7144808239, gamma=1.01172955093, total=  13.2s
[CV] kernel=linear, C=3582.05527805, gamma=1.18913702221 .............
[CV] . kernel=rbf, C=26.7144808239, gamma=1.01172955093, total=  13.3s
[CV] kernel=linear, C=3582.05527805, gamma=1.18913702221 .............
[CV]  kernel=linear, C=3582.05527805, gamma=1.18913702221, total=  10.2s
[CV] kernel=linear, C=3582.05527805, gamma=1.18913702221 .............
[CV] . kernel=rbf, C=26.7144808239, gamma=1.01172955093, total=  13.2s
[CV] kernel=linear, C=3582.05527805, gamma=1.18913702221 .............
[CV]  kernel=linear, C=3582.05527805, gamma=1.18913702221, total=   9.3s
[CV] kernel=linear, C=198.700478181, gamma=0.528281974883 ............
[CV]  kernel=linear, C=3582.05527805, gamma=1.18913702221, total=   9.5s
[CV] kernel=linear, C=198.700478181, gamma=0.528281974883 ............
[CV]  kernel=linear, C=3582.05527805, gamma=1.18913702221, total=   9.3s
[CV] kernel=linear, C=198.700478181, gamma=0.528281974883 ............
[CV]  kernel=linear, C=3582.05527805, gamma=1.18913702221, total=   9.1s
[CV] kernel=linear, C=198.700478181, gamma=0.528281974883 ............
[CV]  kernel=linear, C=198.700478181, gamma=0.528281974883, total=   7.9s
[CV] kernel=linear, C=198.700478181, gamma=0.528281974883 ............
[CV]  kernel=linear, C=198.700478181, gamma=0.528281974883, total=   8.0s
[CV] kernel=linear, C=129.800060414, gamma=2.86213836765 .............
[CV]  kernel=linear, C=198.700478181, gamma=0.528281974883, total=   8.4s
[CV] kernel=linear, C=129.800060414, gamma=2.86213836765 .............
[CV]  kernel=linear, C=198.700478181, gamma=0.528281974883, total=   8.2s
[CV] kernel=linear, C=129.800060414, gamma=2.86213836765 .............
[CV]  kernel=linear, C=198.700478181, gamma=0.528281974883, total=   8.0s
[CV] kernel=linear, C=129.800060414, gamma=2.86213836765 .............
[CV]  kernel=linear, C=129.800060414, gamma=2.86213836765, total=   8.3s
[CV] kernel=linear, C=129.800060414, gamma=2.86213836765 .............
[CV]  kernel=linear, C=129.800060414, gamma=2.86213836765, total=   8.1s
[CV] kernel=rbf, C=288.426929959, gamma=0.1758083585 .................
[CV]  kernel=linear, C=129.800060414, gamma=2.86213836765, total=   8.3s
[CV] kernel=rbf, C=288.426929959, gamma=0.1758083585 .................
[CV]  kernel=linear, C=129.800060414, gamma=2.86213836765, total=   8.5s
[CV] kernel=rbf, C=288.426929959, gamma=0.1758083585 .................
[CV]  kernel=linear, C=129.800060414, gamma=2.86213836765, total=   8.3s
[CV] kernel=rbf, C=288.426929959, gamma=0.1758083585 .................
[CV] .. kernel=rbf, C=288.426929959, gamma=0.1758083585, total=  13.5s
[CV] kernel=rbf, C=288.426929959, gamma=0.1758083585 .................
[CV] .. kernel=rbf, C=288.426929959, gamma=0.1758083585, total=  13.2s
[CV] kernel=linear, C=6287.03948943, gamma=0.350456725533 ............
[CV] .. kernel=rbf, C=288.426929959, gamma=0.1758083585, total=  12.9s
[CV] kernel=linear, C=6287.03948943, gamma=0.350456725533 ............
[CV] .. kernel=rbf, C=288.426929959, gamma=0.1758083585, total=  13.4s
[CV] kernel=linear, C=6287.03948943, gamma=0.350456725533 ............
[CV]  kernel=linear, C=6287.03948943, gamma=0.350456725533, total=  10.8s
[CV] kernel=linear, C=6287.03948943, gamma=0.350456725533 ............
[CV]  kernel=linear, C=6287.03948943, gamma=0.350456725533, total=  10.6s
[CV] kernel=linear, C=6287.03948943, gamma=0.350456725533 ............
[CV]  kernel=linear, C=6287.03948943, gamma=0.350456725533, total=  11.4s
[CV] kernel=rbf, C=61217.0442134, gamma=1.62796894074 ................
[CV] .. kernel=rbf, C=288.426929959, gamma=0.1758083585, total=  13.6s
[CV] kernel=rbf, C=61217.0442134, gamma=1.62796894074 ................
[CV]  kernel=linear, C=6287.03948943, gamma=0.350456725533, total=  10.5s
[CV] kernel=rbf, C=61217.0442134, gamma=1.62796894074 ................
[CV]  kernel=linear, C=6287.03948943, gamma=0.350456725533, total=  11.5s
[CV] kernel=rbf, C=61217.0442134, gamma=1.62796894074 ................
[CV] . kernel=rbf, C=61217.0442134, gamma=1.62796894074, total=  45.7s
[CV] kernel=rbf, C=61217.0442134, gamma=1.62796894074 ................
[CV] . kernel=rbf, C=61217.0442134, gamma=1.62796894074, total=  52.0s
[CV] kernel=rbf, C=926.97876841, gamma=2.14797959306 .................
[CV] . kernel=rbf, C=61217.0442134, gamma=1.62796894074, total=  48.4s
[CV] kernel=rbf, C=926.97876841, gamma=2.14797959306 .................
[CV] . kernel=rbf, C=61217.0442134, gamma=1.62796894074, total=  49.4s
[CV] kernel=rbf, C=926.97876841, gamma=2.14797959306 .................
[CV] .. kernel=rbf, C=926.97876841, gamma=2.14797959306, total=  13.2s
[CV] kernel=rbf, C=926.97876841, gamma=2.14797959306 .................
[CV] .. kernel=rbf, C=926.97876841, gamma=2.14797959306, total=  13.2s
[CV] kernel=rbf, C=926.97876841, gamma=2.14797959306 .................
[CV] .. kernel=rbf, C=926.97876841, gamma=2.14797959306, total=  13.1s
[CV] kernel=linear, C=33946.1570649, gamma=2.26424264929 .............
[CV] .. kernel=rbf, C=926.97876841, gamma=2.14797959306, total=  13.2s
[CV] kernel=linear, C=33946.1570649, gamma=2.26424264929 .............
[CV] . kernel=rbf, C=61217.0442134, gamma=1.62796894074, total=  45.9s
[CV] kernel=linear, C=33946.1570649, gamma=2.26424264929 .............
[CV] .. kernel=rbf, C=926.97876841, gamma=2.14797959306, total=  13.0s
[CV] kernel=linear, C=33946.1570649, gamma=2.26424264929 .............
[CV]  kernel=linear, C=33946.1570649, gamma=2.26424264929, total=  20.6s
[CV] kernel=linear, C=33946.1570649, gamma=2.26424264929 .............
[CV]  kernel=linear, C=33946.1570649, gamma=2.26424264929, total=  20.1s
[CV] kernel=linear, C=84789.8294774, gamma=0.31763590853 .............
[CV]  kernel=linear, C=33946.1570649, gamma=2.26424264929, total=  18.4s
[CV] kernel=linear, C=84789.8294774, gamma=0.31763590853 .............
[CV]  kernel=linear, C=33946.1570649, gamma=2.26424264929, total=  21.0s
[CV] kernel=linear, C=84789.8294774, gamma=0.31763590853 .............
[CV]  kernel=linear, C=33946.1570649, gamma=2.26424264929, total=  18.7s
[CV] kernel=linear, C=84789.8294774, gamma=0.31763590853 .............
[CV]  kernel=linear, C=84789.8294774, gamma=0.31763590853, total=  37.6s
[CV] kernel=linear, C=84789.8294774, gamma=0.31763590853 .............
[CV]  kernel=linear, C=84789.8294774, gamma=0.31763590853, total=  41.3s
[CV]  kernel=linear, C=84789.8294774, gamma=0.31763590853, total=  51.1s
[CV]  kernel=linear, C=84789.8294774, gamma=0.31763590853, total=  54.8s
[CV]  kernel=linear, C=84789.8294774, gamma=0.31763590853, total=  30.1s


[Parallel(n_jobs=4)]: Done 250 out of 250 | elapsed: 24.6min finished





RandomizedSearchCV(cv=5, error_score='raise',
          estimator=SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False),
          fit_params=None, iid=True, n_iter=50, n_jobs=4,
          param_distributions={u'kernel': [u'linear', u'rbf'], u'C': &lt;scipy.stats._distn_infrastructure.rv_frozen object at 0x7f6dc0425c50&gt;, u'gamma': &lt;scipy.stats._distn_infrastructure.rv_frozen object at 0x7f6dc0242310&gt;},
          pre_dispatch='2*n_jobs', random_state=42, refit=True,
          return_train_score='warn', scoring=u'neg_mean_squared_error',
          verbose=2)
</code></pre>
<p>The best model achieves the following score (evaluated using 5-fold cross validation):</p>
<pre class=" language-python"><code class="prism  language-python">negative_mse <span class="token operator">=</span> rnd_search<span class="token punctuation">.</span>best_score_
rmse <span class="token operator">=</span> np<span class="token punctuation">.</span>sqrt<span class="token punctuation">(</span><span class="token operator">-</span>negative_mse<span class="token punctuation">)</span>
rmse
</code></pre>
<pre><code>54767.99053704409
</code></pre>
<p>Now this is much closer to the performance of the <code>RandomForestRegressor</code> (but not quite there yet). Let’s check the best hyperparameters found:</p>
<pre class=" language-python"><code class="prism  language-python">rnd_search<span class="token punctuation">.</span>best_params_
</code></pre>
<pre><code>{u'C': 157055.10989448498, u'gamma': 0.26497040005002437, u'kernel': u'rbf'}
</code></pre>
<p>This time the search found a good set of hyperparameters for the RBF kernel. Randomized search tends to find better hyperparameters than grid search in the same amount of time.</p>
<p>Let’s look at the exponential distribution we used, with <code>scale=1.0</code>. Note that some samples are much larger or smaller than 1.0, but when you look at the log of the distribution, you can see that most values are actually concentrated roughly in the range of exp(-2) to exp(+2), which is about 0.1 to 7.4.</p>
<pre class=" language-python"><code class="prism  language-python">expon_distrib <span class="token operator">=</span> expon<span class="token punctuation">(</span>scale<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">.</span><span class="token punctuation">)</span>
samples <span class="token operator">=</span> expon_distrib<span class="token punctuation">.</span>rvs<span class="token punctuation">(</span><span class="token number">10000</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>figure<span class="token punctuation">(</span>figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>subplot<span class="token punctuation">(</span><span class="token number">121</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">"Exponential distribution (scale=1.0)"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>samples<span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>subplot<span class="token punctuation">(</span><span class="token number">122</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">"Log of this distribution"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>np<span class="token punctuation">.</span>log<span class="token punctuation">(</span>samples<span class="token punctuation">)</span><span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<p><img src="output_162_0.png" alt="png"></p>
<p>The distribution we used for <code>C</code> looks quite different: the scale of the samples is picked from a uniform distribution within a given range, which is why the right graph, which represents the log of the samples, looks roughly constant. This distribution is useful when you don’t have a clue of what the target scale is:</p>
<pre class=" language-python"><code class="prism  language-python">reciprocal_distrib <span class="token operator">=</span> reciprocal<span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">,</span> <span class="token number">200000</span><span class="token punctuation">)</span>
samples <span class="token operator">=</span> reciprocal_distrib<span class="token punctuation">.</span>rvs<span class="token punctuation">(</span><span class="token number">10000</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>figure<span class="token punctuation">(</span>figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>subplot<span class="token punctuation">(</span><span class="token number">121</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">"Reciprocal distribution (scale=1.0)"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>samples<span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>subplot<span class="token punctuation">(</span><span class="token number">122</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">"Log of this distribution"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>np<span class="token punctuation">.</span>log<span class="token punctuation">(</span>samples<span class="token punctuation">)</span><span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<p><img src="output_164_0.png" alt="png"></p>
<p>The reciprocal distribution is useful when you have no idea what the scale of the hyperparameter should be (indeed, as you can see on the figure on the right, all scales are equally likely, within the given range), whereas the exponential distribution is best when you know (more or less) what the scale of the hyperparameter should be.</p>
<h2 id="section-2">3.</h2>
<p>Question: Try adding a transformer in the preparation pipeline to select only the most important attributes.</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>base <span class="token keyword">import</span> BaseEstimator<span class="token punctuation">,</span> TransformerMixin

<span class="token keyword">def</span> <span class="token function">indices_of_top_k</span><span class="token punctuation">(</span>arr<span class="token punctuation">,</span> k<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> np<span class="token punctuation">.</span>sort<span class="token punctuation">(</span>np<span class="token punctuation">.</span>argpartition<span class="token punctuation">(</span>np<span class="token punctuation">.</span>array<span class="token punctuation">(</span>arr<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">-</span>k<span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token operator">-</span>k<span class="token punctuation">:</span><span class="token punctuation">]</span><span class="token punctuation">)</span>

<span class="token keyword">class</span> <span class="token class-name">TopFeatureSelector</span><span class="token punctuation">(</span>BaseEstimator<span class="token punctuation">,</span> TransformerMixin<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> feature_importances<span class="token punctuation">,</span> k<span class="token punctuation">)</span><span class="token punctuation">:</span>
        self<span class="token punctuation">.</span>feature_importances <span class="token operator">=</span> feature_importances
        self<span class="token punctuation">.</span>k <span class="token operator">=</span> k
    <span class="token keyword">def</span> <span class="token function">fit</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        self<span class="token punctuation">.</span>feature_indices_ <span class="token operator">=</span> indices_of_top_k<span class="token punctuation">(</span>self<span class="token punctuation">.</span>feature_importances<span class="token punctuation">,</span> self<span class="token punctuation">.</span>k<span class="token punctuation">)</span>
        <span class="token keyword">return</span> self
    <span class="token keyword">def</span> <span class="token function">transform</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> X<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> X<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span>feature_indices_<span class="token punctuation">]</span>
</code></pre>
<p>Note: this feature selector assumes that you have already computed the feature importances somehow (for example using a <code>RandomForestRegressor</code>). You may be tempted to compute them directly in the <code>TopFeatureSelector</code>'s <code>fit()</code> method, however this would likely slow down grid/randomized search since the feature importances would have to be computed for every hyperparameter combination (unless you implement some sort of cache).</p>
<p>Let’s define the number of top features we want to keep:</p>
<pre class=" language-python"><code class="prism  language-python">k <span class="token operator">=</span> <span class="token number">5</span>
</code></pre>
<p>Now let’s look for the indices of the top k features:</p>
<pre class=" language-python"><code class="prism  language-python">top_k_feature_indices <span class="token operator">=</span> indices_of_top_k<span class="token punctuation">(</span>feature_importances<span class="token punctuation">,</span> k<span class="token punctuation">)</span>
top_k_feature_indices
</code></pre>
<pre><code>array([ 0,  1,  7,  9, 12])
</code></pre>
<pre class=" language-python"><code class="prism  language-python">np<span class="token punctuation">.</span>array<span class="token punctuation">(</span>attributes<span class="token punctuation">)</span><span class="token punctuation">[</span>top_k_feature_indices<span class="token punctuation">]</span>
</code></pre>
<pre><code>array([u'longitude', u'latitude', u'median_income', u'pop_per_hhold',
       u'INLAND'],
      dtype='&lt;U18')
</code></pre>
<p>Let’s double check that these are indeed the top k features:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token builtin">sorted</span><span class="token punctuation">(</span><span class="token builtin">zip</span><span class="token punctuation">(</span>feature_importances<span class="token punctuation">,</span> attributes<span class="token punctuation">)</span><span class="token punctuation">,</span> reverse<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token punctuation">:</span>k<span class="token punctuation">]</span>
</code></pre>
<pre><code>[(0.36615898061813418, 'median_income'),
 (0.16478099356159051, 'INLAND'),
 (0.10879295677551573, u'pop_per_hhold'),
 (0.073344235516012421, 'longitude'),
 (0.062909070482620302, 'latitude')]
</code></pre>
<p>Looking good… Now let’s create a new pipeline that runs the previously defined preparation pipeline, and adds top k feature selection:</p>
<pre class=" language-python"><code class="prism  language-python">preparation_and_feature_selection_pipeline <span class="token operator">=</span> Pipeline<span class="token punctuation">(</span><span class="token punctuation">[</span>
    <span class="token punctuation">(</span><span class="token string">'preparation'</span><span class="token punctuation">,</span> full_pipeline<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">(</span><span class="token string">'feature_selection'</span><span class="token punctuation">,</span> TopFeatureSelector<span class="token punctuation">(</span>feature_importances<span class="token punctuation">,</span> k<span class="token punctuation">)</span><span class="token punctuation">)</span>
<span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_prepared_top_k_features <span class="token operator">=</span> preparation_and_feature_selection_pipeline<span class="token punctuation">.</span>fit_transform<span class="token punctuation">(</span>housing<span class="token punctuation">)</span>
</code></pre>
<p>Let’s look at the features of the first 3 instances:</p>
<pre class=" language-python"><code class="prism  language-python">housing_prepared_top_k_features<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">:</span><span class="token number">3</span><span class="token punctuation">]</span>
</code></pre>
<pre><code>array([[-1.15604281,  0.77194962, -0.61493744, -0.08649871,  0.        ],
       [-1.17602483,  0.6596948 ,  1.33645936, -0.03353391,  0.        ],
       [ 1.18684903, -1.34218285, -0.5320456 , -0.09240499,  0.        ]])
</code></pre>
<p>Now let’s double check that these are indeed the top k features:</p>
<pre class=" language-python"><code class="prism  language-python">housing_prepared<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">:</span><span class="token number">3</span><span class="token punctuation">,</span> top_k_feature_indices<span class="token punctuation">]</span>
</code></pre>
<pre><code>array([[-1.15604281,  0.77194962, -0.61493744, -0.08649871,  0.        ],
       [-1.17602483,  0.6596948 ,  1.33645936, -0.03353391,  0.        ],
       [ 1.18684903, -1.34218285, -0.5320456 , -0.09240499,  0.        ]])
</code></pre>
<p>Works great!  :)</p>
<h2 id="section-3">4.</h2>
<p>Question: Try creating a single pipeline that does the full data preparation plus the final prediction.</p>
<pre class=" language-python"><code class="prism  language-python">prepare_select_and_predict_pipeline <span class="token operator">=</span> Pipeline<span class="token punctuation">(</span><span class="token punctuation">[</span>
    <span class="token punctuation">(</span><span class="token string">'preparation'</span><span class="token punctuation">,</span> full_pipeline<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">(</span><span class="token string">'feature_selection'</span><span class="token punctuation">,</span> TopFeatureSelector<span class="token punctuation">(</span>feature_importances<span class="token punctuation">,</span> k<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">(</span><span class="token string">'svm_reg'</span><span class="token punctuation">,</span> SVR<span class="token punctuation">(</span><span class="token operator">**</span>rnd_search<span class="token punctuation">.</span>best_params_<span class="token punctuation">)</span><span class="token punctuation">)</span>
<span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">prepare_select_and_predict_pipeline<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>Pipeline(memory=None,
     steps=[(u'preparation', FeatureUnion(n_jobs=1,
       transformer_list=[(u'num_pipeline', Pipeline(memory=None,
     steps=[(u'selector', DataFrameSelector(attribute_names=['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income'])),...gamma=0.26497040005002437, kernel=u'rbf', max_iter=-1, shrinking=True,
  tol=0.001, verbose=False))])
</code></pre>
<p>Let’s try the full pipeline on a few instances:</p>
<pre class=" language-python"><code class="prism  language-python">some_data <span class="token operator">=</span> housing<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token number">4</span><span class="token punctuation">]</span>
some_labels <span class="token operator">=</span> housing_labels<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token number">4</span><span class="token punctuation">]</span>

<span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Predictions:\t"</span><span class="token punctuation">,</span> prepare_select_and_predict_pipeline<span class="token punctuation">.</span>predict<span class="token punctuation">(</span>some_data<span class="token punctuation">)</span><span class="token punctuation">)</span>
<span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Labels:\t\t"</span><span class="token punctuation">,</span> <span class="token builtin">list</span><span class="token punctuation">(</span>some_labels<span class="token punctuation">)</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Predictions:	 [ 203214.28978849  371846.88152572  173295.65441612   47328.3970888 ]
Labels:		 [286600.0, 340600.0, 196900.0, 46300.0]
</code></pre>
<p>Well, the full pipeline seems to work fine. Of course, the predictions are not fantastic: they would be better if we used the best <code>RandomForestRegressor</code> that we found earlier, rather than the best <code>SVR</code>.</p>
<h2 id="section-4">5.</h2>
<p>Question: Automatically explore some preparation options using <code>GridSearchCV</code>.</p>
<pre class=" language-python"><code class="prism  language-python">param_grid <span class="token operator">=</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span><span class="token string">'preparation__num_pipeline__imputer__strategy'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">'mean'</span><span class="token punctuation">,</span> <span class="token string">'median'</span><span class="token punctuation">,</span> <span class="token string">'most_frequent'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
         <span class="token string">'feature_selection__k'</span><span class="token punctuation">:</span> <span class="token builtin">list</span><span class="token punctuation">(</span><span class="token builtin">range</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token builtin">len</span><span class="token punctuation">(</span>feature_importances<span class="token punctuation">)</span> <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">}</span>
<span class="token punctuation">]</span>

grid_search_prep <span class="token operator">=</span> GridSearchCV<span class="token punctuation">(</span>prepare_select_and_predict_pipeline<span class="token punctuation">,</span> param_grid<span class="token punctuation">,</span> cv<span class="token operator">=</span><span class="token number">5</span><span class="token punctuation">,</span>
                                scoring<span class="token operator">=</span><span class="token string">'neg_mean_squared_error'</span><span class="token punctuation">,</span> verbose<span class="token operator">=</span><span class="token number">2</span><span class="token punctuation">,</span> n_jobs<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">)</span>
grid_search_prep<span class="token punctuation">.</span>fit<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> housing_labels<span class="token punctuation">)</span>
</code></pre>
<pre><code>Fitting 5 folds for each of 48 candidates, totalling 240 fits
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean 
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean 
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean 
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean, total=  10.4s
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean, total=  10.4s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median 
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean, total=  10.7s
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean, total=  10.7s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median 
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=mean, total=  10.4s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median, total=  10.4s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median, total=  10.4s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median, total=  10.5s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median, total=  10.4s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=median, total=  10.4s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.2s
[CV] feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.2s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.6s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.0s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=1, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.4s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean, total=  10.9s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean, total=  10.9s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean, total=  10.7s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean, total=  10.9s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=mean, total=  10.8s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median, total=  10.6s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median, total=  10.8s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median, total=  10.7s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median, total=  10.8s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=median, total=  10.9s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.2s
[CV] feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.5s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.3s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.5s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=2, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.6s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean, total=  10.9s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean, total=  11.4s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean, total=  11.1s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median 


[Parallel(n_jobs=4)]: Done  33 tasks      | elapsed:  2.2min


[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean, total=  11.0s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=mean, total=  11.0s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median, total=  11.1s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median, total=  11.2s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median, total=  11.1s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median, total=  11.0s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=median, total=  11.0s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.7s
[CV] feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.6s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.8s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.2s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=3, preparation__num_pipeline__imputer__strategy=most_frequent, total=  11.9s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean, total=  12.0s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean, total=  11.7s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean, total=  11.9s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean, total=  11.7s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=mean, total=  11.4s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median, total=  11.7s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median, total=  11.5s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median, total=  11.8s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median, total=  11.7s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=median, total=  11.5s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.3s
[CV] feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.1s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.3s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.3s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=4, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.0s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean, total=  11.9s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean, total=  12.0s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean, total=  12.0s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean, total=  12.2s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=mean, total=  11.9s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median, total=  11.9s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median, total=  12.0s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median, total=  12.1s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median, total=  12.1s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=median, total=  11.8s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.5s
[CV] feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.7s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.7s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.8s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=5, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.5s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean, total=  12.2s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean, total=  12.6s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean, total=  12.2s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean, total=  12.1s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=mean, total=  12.6s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median, total=  12.3s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median, total=  12.5s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median, total=  12.2s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median, total=  12.1s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=median, total=  12.8s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.9s
[CV] feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent, total=  13.6s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.8s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent, total=  12.8s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=6, preparation__num_pipeline__imputer__strategy=most_frequent, total=  13.2s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean, total=  13.1s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean, total=  12.9s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean, total=  13.7s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean, total=  13.5s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=mean, total=  13.1s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median, total=  14.4s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median, total=  13.2s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median, total=  13.2s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median, total=  12.6s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=median, total=  12.9s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent, total=  13.9s
[CV] feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent, total=  14.9s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent, total=  14.4s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent, total=  13.4s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=7, preparation__num_pipeline__imputer__strategy=most_frequent, total=  14.4s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean, total=  15.4s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean, total=  14.9s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean, total=  16.5s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean, total=  16.4s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median, total=  16.4s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=mean, total=  18.1s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median, total=  15.1s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median, total=  17.0s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median, total=  17.1s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=median, total=  16.8s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent, total=  16.3s
[CV] feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent, total=  16.0s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent, total=  15.8s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent, total=  17.5s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=8, preparation__num_pipeline__imputer__strategy=most_frequent, total=  16.8s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean, total=  23.4s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean, total=  21.6s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean, total=  23.0s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean, total=  22.1s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=mean, total=  19.3s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median, total=  18.9s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median, total=  21.9s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median, total=  22.8s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median, total=  22.5s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=median, total=  19.5s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent, total=  23.1s
[CV] feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent, total=  23.3s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent, total=  22.4s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent, total=  22.3s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=9, preparation__num_pipeline__imputer__strategy=most_frequent, total=  21.3s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean, total=  21.9s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean, total=  23.1s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean, total=  25.2s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean, total=  28.5s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=mean, total=  23.5s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median, total=  22.2s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median, total=  24.5s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median, total=  24.4s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median, total=  26.8s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=median, total=  22.7s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent, total=  23.1s
[CV] feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent, total=  23.9s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent, total=  22.9s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent, total=  25.2s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=10, preparation__num_pipeline__imputer__strategy=most_frequent, total=  25.7s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean, total=  26.9s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean, total=  29.2s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean, total=  26.7s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean, total=  28.8s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median 


[Parallel(n_jobs=4)]: Done 154 tasks      | elapsed: 12.7min


[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median, total=  24.5s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=mean, total=  27.4s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median, total=  23.7s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median, total=  24.6s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median, total=  28.1s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=median, total=  29.2s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent, total=  30.0s
[CV] feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent, total=  24.0s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent, total=  24.8s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent, total=  27.3s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=11, preparation__num_pipeline__imputer__strategy=most_frequent, total=  33.2s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean, total=  30.3s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean, total=  29.8s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean, total=  28.8s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean, total=  29.1s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=mean, total=  30.3s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median, total=  26.6s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median, total=  27.7s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median, total=  30.4s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median, total=  28.0s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=median, total=  27.7s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent, total=  26.9s
[CV] feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent, total=  28.2s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent, total=  27.2s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent, total=  28.0s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=12, preparation__num_pipeline__imputer__strategy=most_frequent, total=  33.8s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean, total=  31.5s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean, total=  34.6s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean, total=  30.9s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean, total=  33.9s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=mean, total=  26.6s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median, total=  28.3s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median, total=  33.8s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median, total=  35.1s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median, total=  30.7s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=median, total=  34.1s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent, total=  29.0s
[CV] feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent, total=  33.7s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent, total=  34.4s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent, total=  35.2s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=13, preparation__num_pipeline__imputer__strategy=most_frequent, total=  30.6s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean, total=  27.4s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean, total=  32.9s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean, total=  33.3s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean, total=  33.6s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=mean, total=  30.4s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median, total=  32.1s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median, total=  33.6s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median, total=  32.7s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median, total=  32.5s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=median, total=  29.5s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent, total=  29.1s
[CV] feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent, total=  30.6s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent, total=  33.0s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent, total=  34.7s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean, total=  32.0s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean, total=  33.5s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=14, preparation__num_pipeline__imputer__strategy=most_frequent, total=  40.0s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean, total=  27.2s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean, total=  35.1s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=mean, total=  31.9s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median, total=  29.1s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median, total=  32.3s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median, total=  36.0s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median, total=  32.6s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=median, total=  35.5s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent, total=  35.7s
[CV] feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent, total=  29.9s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent, total=  35.5s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent, total=  36.4s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean, total=  34.7s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=15, preparation__num_pipeline__imputer__strategy=most_frequent, total=  38.2s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean, total=  32.7s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean, total=  35.2s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean, total=  30.2s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median, total=  31.4s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=mean, total=  35.8s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median, total=  34.6s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median, total=  27.8s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median, total=  32.9s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=median, total=  33.4s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent, total=  30.1s
[CV] feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent 
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent, total=  32.3s
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent, total=  34.6s
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent, total=  32.5s
[CV]  feature_selection__k=16, preparation__num_pipeline__imputer__strategy=most_frequent, total=  34.5s


[Parallel(n_jobs=4)]: Done 240 out of 240 | elapsed: 25.7min finished





GridSearchCV(cv=5, error_score='raise',
       estimator=Pipeline(memory=None,
     steps=[(u'preparation', FeatureUnion(n_jobs=1,
       transformer_list=[(u'num_pipeline', Pipeline(memory=None,
     steps=[(u'selector', DataFrameSelector(attribute_names=['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income'])),...gamma=0.26497040005002437, kernel=u'rbf', max_iter=-1, shrinking=True,
  tol=0.001, verbose=False))]),
       fit_params=None, iid=True, n_jobs=4,
       param_grid=[{u'feature_selection__k': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], u'preparation__num_pipeline__imputer__strategy': [u'mean', u'median', u'most_frequent']}],
       pre_dispatch='2*n_jobs', refit=True, return_train_score='warn',
       scoring=u'neg_mean_squared_error', verbose=2)
</code></pre>
<pre class=" language-python"><code class="prism  language-python">grid_search_prep<span class="token punctuation">.</span>best_params_
</code></pre>
<pre><code>{u'feature_selection__k': 15,
 u'preparation__num_pipeline__imputer__strategy': u'most_frequent'}
</code></pre>
<p>The best imputer strategy is <code>most_frequent</code> and apparently almost all features are useful (15 out of 16). The last one (<code>ISLAND</code>) seems to just add some noise.</p>
<p>Congratulations! You already know quite a lot about Machine Learning. :)<br>
<strong>Chapter 2 – End-to-end Machine Learning project</strong></p>
<p><em>Welcome to Machine Learning Housing Corp.! Your task is to predict median house values in Californian districts, given a number of features from these districts.</em></p>
<p><em>This notebook contains all the sample code and solutions to the exercices in chapter 2.</em></p>
<p><strong>Note</strong>: You may find little differences between the code outputs in the book and in these Jupyter notebooks: these slight differences are mostly due to the random nature of many training algorithms: although I have tried to make these notebooks’ outputs as constant as possible, it is impossible to guarantee that they will produce the exact same output on every platform. Also, some data structures (such as dictionaries) do not preserve the item order. Finally, I fixed a few minor bugs (I added notes next to the concerned cells) which lead to slightly different results, without changing the ideas presented in the book.</p>
<h1 id="setup-1">Setup</h1>
<p>First, let’s make sure this notebook works well in both python 2 and 3, import a few common modules, ensure MatplotLib plots figures inline and prepare a function to save the figures:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># To support both python 2 and python 3</span>
<span class="token keyword">from</span> __future__ <span class="token keyword">import</span> division<span class="token punctuation">,</span> print_function<span class="token punctuation">,</span> unicode_literals

<span class="token comment"># Common imports</span>
<span class="token keyword">import</span> numpy <span class="token keyword">as</span> np
<span class="token keyword">import</span> os
<span class="token keyword">import</span> sys

<span class="token comment"># to make this notebook's output stable across runs</span>
np<span class="token punctuation">.</span>random<span class="token punctuation">.</span>seed<span class="token punctuation">(</span><span class="token number">42</span><span class="token punctuation">)</span>

<span class="token comment"># To plot pretty figures</span>
<span class="token operator">%</span>matplotlib inline
<span class="token keyword">import</span> matplotlib
<span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>pyplot <span class="token keyword">as</span> plt
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'axes.labelsize'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">14</span>
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'xtick.labelsize'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">12</span>
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'ytick.labelsize'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">12</span>

<span class="token comment"># Where to save the figures</span>
PROJECT_ROOT_DIR <span class="token operator">=</span> <span class="token string">"."</span>
CHAPTER_ID <span class="token operator">=</span> <span class="token string">"end_to_end_project"</span>
IMAGES_PATH <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>PROJECT_ROOT_DIR<span class="token punctuation">,</span> <span class="token string">"images"</span><span class="token punctuation">,</span> CHAPTER_ID<span class="token punctuation">)</span>
<span class="token keyword">if</span> <span class="token operator">not</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>exists<span class="token punctuation">(</span>IMAGES_PATH<span class="token punctuation">)</span><span class="token punctuation">:</span>
    os<span class="token punctuation">.</span>makedirs<span class="token punctuation">(</span>IMAGES_PATH<span class="token punctuation">)</span>

<span class="token keyword">def</span> <span class="token function">save_fig</span><span class="token punctuation">(</span>fig_id<span class="token punctuation">,</span> tight_layout<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> fig_extension<span class="token operator">=</span><span class="token string">"png"</span><span class="token punctuation">,</span> resolution<span class="token operator">=</span><span class="token number">300</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    path <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>IMAGES_PATH<span class="token punctuation">,</span> fig_id <span class="token operator">+</span> <span class="token string">"."</span> <span class="token operator">+</span> fig_extension<span class="token punctuation">)</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Saving figure"</span><span class="token punctuation">,</span> fig_id<span class="token punctuation">)</span>
    <span class="token keyword">if</span> tight_layout<span class="token punctuation">:</span>
        plt<span class="token punctuation">.</span>tight_layout<span class="token punctuation">(</span><span class="token punctuation">)</span>
    plt<span class="token punctuation">.</span>savefig<span class="token punctuation">(</span>path<span class="token punctuation">,</span> <span class="token builtin">format</span><span class="token operator">=</span>fig_extension<span class="token punctuation">,</span> dpi<span class="token operator">=</span>resolution<span class="token punctuation">)</span>

<span class="token comment"># Ignore useless warnings (see SciPy issue #5998)</span>
<span class="token keyword">import</span> warnings
warnings<span class="token punctuation">.</span>filterwarnings<span class="token punctuation">(</span>action<span class="token operator">=</span><span class="token string">"ignore"</span><span class="token punctuation">,</span> module<span class="token operator">=</span><span class="token string">"scipy"</span><span class="token punctuation">,</span> message<span class="token operator">=</span><span class="token string">"^internal gelsd"</span><span class="token punctuation">)</span>
</code></pre>
<h1 id="get-the-data-1">Get the data</h1>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> os
<span class="token keyword">import</span> tarfile
<span class="token keyword">from</span> six<span class="token punctuation">.</span>moves <span class="token keyword">import</span> urllib

DOWNLOAD_ROOT <span class="token operator">=</span> <span class="token string">"https://raw.githubusercontent.com/ageron/handson-ml/master/"</span>
HOUSING_PATH <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span><span class="token string">"datasets"</span><span class="token punctuation">,</span> <span class="token string">"housing"</span><span class="token punctuation">)</span>
HOUSING_URL <span class="token operator">=</span> DOWNLOAD_ROOT <span class="token operator">+</span> <span class="token string">"datasets/housing/housing.tgz"</span>

<span class="token keyword">def</span> <span class="token function">fetch_housing_data</span><span class="token punctuation">(</span>housing_url<span class="token operator">=</span>HOUSING_URL<span class="token punctuation">,</span> housing_path<span class="token operator">=</span>HOUSING_PATH<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">if</span> <span class="token operator">not</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>isdir<span class="token punctuation">(</span>housing_path<span class="token punctuation">)</span><span class="token punctuation">:</span>
        os<span class="token punctuation">.</span>makedirs<span class="token punctuation">(</span>housing_path<span class="token punctuation">)</span>
    tgz_path <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>housing_path<span class="token punctuation">,</span> <span class="token string">"housing.tgz"</span><span class="token punctuation">)</span>
    urllib<span class="token punctuation">.</span>request<span class="token punctuation">.</span>urlretrieve<span class="token punctuation">(</span>housing_url<span class="token punctuation">,</span> tgz_path<span class="token punctuation">)</span>
    housing_tgz <span class="token operator">=</span> tarfile<span class="token punctuation">.</span><span class="token builtin">open</span><span class="token punctuation">(</span>tgz_path<span class="token punctuation">)</span>
    housing_tgz<span class="token punctuation">.</span>extractall<span class="token punctuation">(</span>path<span class="token operator">=</span>housing_path<span class="token punctuation">)</span>
    housing_tgz<span class="token punctuation">.</span>close<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">fetch_housing_data<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> pandas <span class="token keyword">as</span> pd

<span class="token keyword">def</span> <span class="token function">load_housing_data</span><span class="token punctuation">(</span>housing_path<span class="token operator">=</span>HOUSING_PATH<span class="token punctuation">)</span><span class="token punctuation">:</span>
    csv_path <span class="token operator">=</span> os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>housing_path<span class="token punctuation">,</span> <span class="token string">"housing.csv"</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> pd<span class="token punctuation">.</span>read_csv<span class="token punctuation">(</span>csv_path<span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing <span class="token operator">=</span> load_housing_data<span class="token punctuation">(</span><span class="token punctuation">)</span>
housing<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-122.23</td>
      <td>37.88</td>
      <td>41.0</td>
      <td>880.0</td>
      <td>129.0</td>
      <td>322.0</td>
      <td>126.0</td>
      <td>8.3252</td>
      <td>452600.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-122.22</td>
      <td>37.86</td>
      <td>21.0</td>
      <td>7099.0</td>
      <td>1106.0</td>
      <td>2401.0</td>
      <td>1138.0</td>
      <td>8.3014</td>
      <td>358500.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-122.24</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>1467.0</td>
      <td>190.0</td>
      <td>496.0</td>
      <td>177.0</td>
      <td>7.2574</td>
      <td>352100.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-122.25</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>1274.0</td>
      <td>235.0</td>
      <td>558.0</td>
      <td>219.0</td>
      <td>5.6431</td>
      <td>341300.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-122.25</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>1627.0</td>
      <td>280.0</td>
      <td>565.0</td>
      <td>259.0</td>
      <td>3.8462</td>
      <td>342200.0</td>
      <td>NEAR BAY</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;class 'pandas.core.frame.DataFrame'&gt;
RangeIndex: 20640 entries, 0 to 20639
Data columns (total 10 columns):
longitude             20640 non-null float64
latitude              20640 non-null float64
housing_median_age    20640 non-null float64
total_rooms           20640 non-null float64
total_bedrooms        20433 non-null float64
population            20640 non-null float64
households            20640 non-null float64
median_income         20640 non-null float64
median_house_value    20640 non-null float64
ocean_proximity       20640 non-null object
dtypes: float64(9), object(1)
memory usage: 1.6+ MB
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"ocean_proximity"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;1H OCEAN     9136
INLAND        6551
NEAR OCEAN    2658
NEAR BAY      2290
ISLAND           5
Name: ocean_proximity, dtype: int64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>describe<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20433.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
      <td>20640.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-119.569704</td>
      <td>35.631861</td>
      <td>28.639486</td>
      <td>2635.763081</td>
      <td>537.870553</td>
      <td>1425.476744</td>
      <td>499.539680</td>
      <td>3.870671</td>
      <td>206855.816909</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.003532</td>
      <td>2.135952</td>
      <td>12.585558</td>
      <td>2181.615252</td>
      <td>421.385070</td>
      <td>1132.462122</td>
      <td>382.329753</td>
      <td>1.899822</td>
      <td>115395.615874</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-124.350000</td>
      <td>32.540000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>1.000000</td>
      <td>0.499900</td>
      <td>14999.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>-121.800000</td>
      <td>33.930000</td>
      <td>18.000000</td>
      <td>1447.750000</td>
      <td>296.000000</td>
      <td>787.000000</td>
      <td>280.000000</td>
      <td>2.563400</td>
      <td>119600.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>-118.490000</td>
      <td>34.260000</td>
      <td>29.000000</td>
      <td>2127.000000</td>
      <td>435.000000</td>
      <td>1166.000000</td>
      <td>409.000000</td>
      <td>3.534800</td>
      <td>179700.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>-118.010000</td>
      <td>37.710000</td>
      <td>37.000000</td>
      <td>3148.000000</td>
      <td>647.000000</td>
      <td>1725.000000</td>
      <td>605.000000</td>
      <td>4.743250</td>
      <td>264725.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>-114.310000</td>
      <td>41.950000</td>
      <td>52.000000</td>
      <td>39320.000000</td>
      <td>6445.000000</td>
      <td>35682.000000</td>
      <td>6082.000000</td>
      <td>15.000100</td>
      <td>500001.000000</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token operator">%</span>matplotlib inline
<span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>pyplot <span class="token keyword">as</span> plt

housing<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>bins<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">,</span><span class="token number">15</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"attribute_histogram_plots"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure attribute_histogram_plots
</code></pre>
<p><img src="output_13_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># to make this notebook's output identical at every run</span>
np<span class="token punctuation">.</span>random<span class="token punctuation">.</span>seed<span class="token punctuation">(</span><span class="token number">42</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> numpy <span class="token keyword">as</span> np

<span class="token comment"># For illustration only. Sklearn has train_test_split()</span>
<span class="token keyword">def</span> <span class="token function">split_train_test</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> test_ratio<span class="token punctuation">)</span><span class="token punctuation">:</span>
    shuffled_indices <span class="token operator">=</span> np<span class="token punctuation">.</span>random<span class="token punctuation">.</span>permutation<span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">)</span>
    test_set_size <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span> <span class="token operator">*</span> test_ratio<span class="token punctuation">)</span>
    test_indices <span class="token operator">=</span> shuffled_indices<span class="token punctuation">[</span><span class="token punctuation">:</span>test_set_size<span class="token punctuation">]</span>
    train_indices <span class="token operator">=</span> shuffled_indices<span class="token punctuation">[</span>test_set_size<span class="token punctuation">:</span><span class="token punctuation">]</span>
    <span class="token keyword">return</span> data<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span>train_indices<span class="token punctuation">]</span><span class="token punctuation">,</span> data<span class="token punctuation">.</span>iloc<span class="token punctuation">[</span>test_indices<span class="token punctuation">]</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> split_train_test<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> <span class="token number">0.2</span><span class="token punctuation">)</span>
<span class="token keyword">print</span><span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>train_set<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token string">"train +"</span><span class="token punctuation">,</span> <span class="token builtin">len</span><span class="token punctuation">(</span>test_set<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token string">"test"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>16512 train + 4128 test
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> zlib <span class="token keyword">import</span> crc32

<span class="token keyword">def</span> <span class="token function">test_set_check</span><span class="token punctuation">(</span>identifier<span class="token punctuation">,</span> test_ratio<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> crc32<span class="token punctuation">(</span>np<span class="token punctuation">.</span>int64<span class="token punctuation">(</span>identifier<span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token operator">&amp;</span> <span class="token number">0xffffffff</span> <span class="token operator">&lt;</span> test_ratio <span class="token operator">*</span> <span class="token number">2</span><span class="token operator">**</span><span class="token number">32</span>

<span class="token keyword">def</span> <span class="token function">split_train_test_by_id</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> test_ratio<span class="token punctuation">,</span> id_column<span class="token punctuation">)</span><span class="token punctuation">:</span>
    ids <span class="token operator">=</span> data<span class="token punctuation">[</span>id_column<span class="token punctuation">]</span>
    in_test_set <span class="token operator">=</span> ids<span class="token punctuation">.</span><span class="token builtin">apply</span><span class="token punctuation">(</span><span class="token keyword">lambda</span> id_<span class="token punctuation">:</span> test_set_check<span class="token punctuation">(</span>id_<span class="token punctuation">,</span> test_ratio<span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> data<span class="token punctuation">.</span>loc<span class="token punctuation">[</span><span class="token operator">~</span>in_test_set<span class="token punctuation">]</span><span class="token punctuation">,</span> data<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>in_test_set<span class="token punctuation">]</span>
</code></pre>
<p>The implementation of <code>test_set_check()</code> above works fine in both Python 2 and Python 3. In earlier releases, the following implementation was proposed, which supported any hash function, but was much slower and did not support Python 2:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> hashlib

<span class="token keyword">def</span> <span class="token function">test_set_check</span><span class="token punctuation">(</span>identifier<span class="token punctuation">,</span> test_ratio<span class="token punctuation">,</span> <span class="token builtin">hash</span><span class="token operator">=</span>hashlib<span class="token punctuation">.</span>md5<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> <span class="token builtin">hash</span><span class="token punctuation">(</span>np<span class="token punctuation">.</span>int64<span class="token punctuation">(</span>identifier<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>digest<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">&lt;</span> <span class="token number">256</span> <span class="token operator">*</span> test_ratio
</code></pre>
<p>If you want an implementation that supports any hash function and is compatible with both Python 2 and Python 3, here is one:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">test_set_check</span><span class="token punctuation">(</span>identifier<span class="token punctuation">,</span> test_ratio<span class="token punctuation">,</span> <span class="token builtin">hash</span><span class="token operator">=</span>hashlib<span class="token punctuation">.</span>md5<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> <span class="token builtin">bytearray</span><span class="token punctuation">(</span><span class="token builtin">hash</span><span class="token punctuation">(</span>np<span class="token punctuation">.</span>int64<span class="token punctuation">(</span>identifier<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>digest<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">&lt;</span> <span class="token number">256</span> <span class="token operator">*</span> test_ratio
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_with_id <span class="token operator">=</span> housing<span class="token punctuation">.</span>reset_index<span class="token punctuation">(</span><span class="token punctuation">)</span>   <span class="token comment"># adds an `index` column</span>
train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> split_train_test_by_id<span class="token punctuation">(</span>housing_with_id<span class="token punctuation">,</span> <span class="token number">0.2</span><span class="token punctuation">,</span> <span class="token string">"index"</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing_with_id<span class="token punctuation">[</span><span class="token string">"id"</span><span class="token punctuation">]</span> <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"longitude"</span><span class="token punctuation">]</span> <span class="token operator">*</span> <span class="token number">1000</span> <span class="token operator">+</span> housing<span class="token punctuation">[</span><span class="token string">"latitude"</span><span class="token punctuation">]</span>
train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> split_train_test_by_id<span class="token punctuation">(</span>housing_with_id<span class="token punctuation">,</span> <span class="token number">0.2</span><span class="token punctuation">,</span> <span class="token string">"id"</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">test_set<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>index</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>ocean_proximity</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>-122.26</td>
      <td>37.84</td>
      <td>42.0</td>
      <td>2555.0</td>
      <td>665.0</td>
      <td>1206.0</td>
      <td>595.0</td>
      <td>2.0804</td>
      <td>226700.0</td>
      <td>NEAR BAY</td>
      <td>-122222.16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>-122.26</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>2202.0</td>
      <td>434.0</td>
      <td>910.0</td>
      <td>402.0</td>
      <td>3.2031</td>
      <td>281500.0</td>
      <td>NEAR BAY</td>
      <td>-122222.15</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>-122.26</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>3503.0</td>
      <td>752.0</td>
      <td>1504.0</td>
      <td>734.0</td>
      <td>3.2705</td>
      <td>241800.0</td>
      <td>NEAR BAY</td>
      <td>-122222.15</td>
    </tr>
    <tr>
      <th>12</th>
      <td>12</td>
      <td>-122.26</td>
      <td>37.85</td>
      <td>52.0</td>
      <td>2491.0</td>
      <td>474.0</td>
      <td>1098.0</td>
      <td>468.0</td>
      <td>3.0750</td>
      <td>213500.0</td>
      <td>NEAR BAY</td>
      <td>-122222.15</td>
    </tr>
    <tr>
      <th>13</th>
      <td>13</td>
      <td>-122.26</td>
      <td>37.84</td>
      <td>52.0</td>
      <td>696.0</td>
      <td>191.0</td>
      <td>345.0</td>
      <td>174.0</td>
      <td>2.6736</td>
      <td>191300.0</td>
      <td>NEAR BAY</td>
      <td>-122222.16</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> train_test_split

train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> train_test_split<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> test_size<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">test_set<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20046</th>
      <td>-119.01</td>
      <td>36.06</td>
      <td>25.0</td>
      <td>1505.0</td>
      <td>NaN</td>
      <td>1392.0</td>
      <td>359.0</td>
      <td>1.6812</td>
      <td>47700.0</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>3024</th>
      <td>-119.46</td>
      <td>35.14</td>
      <td>30.0</td>
      <td>2943.0</td>
      <td>NaN</td>
      <td>1565.0</td>
      <td>584.0</td>
      <td>2.5313</td>
      <td>45800.0</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>15663</th>
      <td>-122.44</td>
      <td>37.80</td>
      <td>52.0</td>
      <td>3830.0</td>
      <td>NaN</td>
      <td>1310.0</td>
      <td>963.0</td>
      <td>3.4801</td>
      <td>500001.0</td>
      <td>NEAR BAY</td>
    </tr>
    <tr>
      <th>20484</th>
      <td>-118.72</td>
      <td>34.28</td>
      <td>17.0</td>
      <td>3051.0</td>
      <td>NaN</td>
      <td>1705.0</td>
      <td>495.0</td>
      <td>5.7376</td>
      <td>218600.0</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>9814</th>
      <td>-121.93</td>
      <td>36.62</td>
      <td>34.0</td>
      <td>2351.0</td>
      <td>NaN</td>
      <td>1063.0</td>
      <td>428.0</td>
      <td>3.7250</td>
      <td>278000.0</td>
      <td>NEAR OCEAN</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"median_income"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>hist<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;matplotlib.axes._subplots.AxesSubplot at 0x7f6db0132fd0&gt;
</code></pre>
<p><img src="output_27_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># Divide by 1.5 to limit the number of income categories</span>
housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span> <span class="token operator">=</span> np<span class="token punctuation">.</span>ceil<span class="token punctuation">(</span>housing<span class="token punctuation">[</span><span class="token string">"median_income"</span><span class="token punctuation">]</span> <span class="token operator">/</span> <span class="token number">1.5</span><span class="token punctuation">)</span>
<span class="token comment"># Label those above 5 as 5</span>
housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>where<span class="token punctuation">(</span>housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span> <span class="token operator">&lt;</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">5.0</span><span class="token punctuation">,</span> inplace<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>3.0    7236
2.0    6581
4.0    3639
5.0    2362
1.0     822
Name: income_cat, dtype: int64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>hist<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>&lt;matplotlib.axes._subplots.AxesSubplot at 0x7f6db00c60d0&gt;
</code></pre>
<p><img src="output_30_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">from</span> sklearn<span class="token punctuation">.</span>model_selection <span class="token keyword">import</span> StratifiedShuffleSplit

split <span class="token operator">=</span> StratifiedShuffleSplit<span class="token punctuation">(</span>n_splits<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">,</span> test_size<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>
<span class="token keyword">for</span> train_index<span class="token punctuation">,</span> test_index <span class="token keyword">in</span> split<span class="token punctuation">.</span>split<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    strat_train_set <span class="token operator">=</span> housing<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>train_index<span class="token punctuation">]</span>
    strat_test_set <span class="token operator">=</span> housing<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>test_index<span class="token punctuation">]</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">strat_test_set<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>strat_test_set<span class="token punctuation">)</span>
</code></pre>
<pre><code>3.0    0.350533
2.0    0.318798
4.0    0.176357
5.0    0.114583
1.0    0.039729
Name: income_cat, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>housing<span class="token punctuation">)</span>
</code></pre>
<pre><code>3.0    0.350581
2.0    0.318847
4.0    0.176308
5.0    0.114438
1.0    0.039826
Name: income_cat, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">income_cat_proportions</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> data<span class="token punctuation">[</span><span class="token string">"income_cat"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>value_counts<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span>

train_set<span class="token punctuation">,</span> test_set <span class="token operator">=</span> train_test_split<span class="token punctuation">(</span>housing<span class="token punctuation">,</span> test_size<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">,</span> random_state<span class="token operator">=</span><span class="token number">42</span><span class="token punctuation">)</span>

compare_props <span class="token operator">=</span> pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token string">"Overall"</span><span class="token punctuation">:</span> income_cat_proportions<span class="token punctuation">(</span>housing<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token string">"Stratified"</span><span class="token punctuation">:</span> income_cat_proportions<span class="token punctuation">(</span>strat_test_set<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token string">"Random"</span><span class="token punctuation">:</span> income_cat_proportions<span class="token punctuation">(</span>test_set<span class="token punctuation">)</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span>sort_index<span class="token punctuation">(</span><span class="token punctuation">)</span>
compare_props<span class="token punctuation">[</span><span class="token string">"Rand. %error"</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">100</span> <span class="token operator">*</span> compare_props<span class="token punctuation">[</span><span class="token string">"Random"</span><span class="token punctuation">]</span> <span class="token operator">/</span> compare_props<span class="token punctuation">[</span><span class="token string">"Overall"</span><span class="token punctuation">]</span> <span class="token operator">-</span> <span class="token number">100</span>
compare_props<span class="token punctuation">[</span><span class="token string">"Strat. %error"</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">100</span> <span class="token operator">*</span> compare_props<span class="token punctuation">[</span><span class="token string">"Stratified"</span><span class="token punctuation">]</span> <span class="token operator">/</span> compare_props<span class="token punctuation">[</span><span class="token string">"Overall"</span><span class="token punctuation">]</span> <span class="token operator">-</span> <span class="token number">100</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">compare_props
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>Overall</th>
      <th>Random</th>
      <th>Stratified</th>
      <th>Rand. %error</th>
      <th>Strat. %error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1.0</th>
      <td>0.039826</td>
      <td>0.040213</td>
      <td>0.039729</td>
      <td>0.973236</td>
      <td>-0.243309</td>
    </tr>
    <tr>
      <th>2.0</th>
      <td>0.318847</td>
      <td>0.324370</td>
      <td>0.318798</td>
      <td>1.732260</td>
      <td>-0.015195</td>
    </tr>
    <tr>
      <th>3.0</th>
      <td>0.350581</td>
      <td>0.358527</td>
      <td>0.350533</td>
      <td>2.266446</td>
      <td>-0.013820</td>
    </tr>
    <tr>
      <th>4.0</th>
      <td>0.176308</td>
      <td>0.167393</td>
      <td>0.176357</td>
      <td>-5.056334</td>
      <td>0.027480</td>
    </tr>
    <tr>
      <th>5.0</th>
      <td>0.114438</td>
      <td>0.109496</td>
      <td>0.114583</td>
      <td>-4.318374</td>
      <td>0.127011</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">for</span> set_ <span class="token keyword">in</span> <span class="token punctuation">(</span>strat_train_set<span class="token punctuation">,</span> strat_test_set<span class="token punctuation">)</span><span class="token punctuation">:</span>
    set_<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"income_cat"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">,</span> inplace<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
</code></pre>
<h1 id="discover-and-visualize-the-data-to-gain-insights-1">Discover and visualize the data to gain insights</h1>
<pre class=" language-python"><code class="prism  language-python">housing <span class="token operator">=</span> strat_train_set<span class="token punctuation">.</span>copy<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"bad_visualization_plot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure bad_visualization_plot
</code></pre>
<p><img src="output_39_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.1</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"better_visualization_plot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure better_visualization_plot
</code></pre>
<p><img src="output_40_1.png" alt="png"></p>
<p>The argument <code>sharex=False</code> fixes a display bug (the x-axis values and legend were not displayed). This is a temporary fix (see: <a href="https://github.com/pandas-dev/pandas/issues/10611">https://github.com/pandas-dev/pandas/issues/10611</a>). Thanks to Wilmer Arellano for pointing it out.</p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.4</span><span class="token punctuation">,</span>
    s<span class="token operator">=</span>housing<span class="token punctuation">[</span><span class="token string">"population"</span><span class="token punctuation">]</span><span class="token operator">/</span><span class="token number">100</span><span class="token punctuation">,</span> label<span class="token operator">=</span><span class="token string">"population"</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span><span class="token number">7</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    c<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> cmap<span class="token operator">=</span>plt<span class="token punctuation">.</span>get_cmap<span class="token punctuation">(</span><span class="token string">"jet"</span><span class="token punctuation">)</span><span class="token punctuation">,</span> colorbar<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span>
    sharex<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>legend<span class="token punctuation">(</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"housing_prices_scatterplot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure housing_prices_scatterplot
</code></pre>
<p><img src="output_42_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>image <span class="token keyword">as</span> mpimg
california_img<span class="token operator">=</span>mpimg<span class="token punctuation">.</span>imread<span class="token punctuation">(</span>PROJECT_ROOT_DIR <span class="token operator">+</span> <span class="token string">'/images/end_to_end_project/california.png'</span><span class="token punctuation">)</span>
ax <span class="token operator">=</span> housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"longitude"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"latitude"</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span><span class="token number">7</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                       s<span class="token operator">=</span>housing<span class="token punctuation">[</span><span class="token string">'population'</span><span class="token punctuation">]</span><span class="token operator">/</span><span class="token number">100</span><span class="token punctuation">,</span> label<span class="token operator">=</span><span class="token string">"Population"</span><span class="token punctuation">,</span>
                       c<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> cmap<span class="token operator">=</span>plt<span class="token punctuation">.</span>get_cmap<span class="token punctuation">(</span><span class="token string">"jet"</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                       colorbar<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.4</span><span class="token punctuation">,</span>
                      <span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>imshow<span class="token punctuation">(</span>california_img<span class="token punctuation">,</span> extent<span class="token operator">=</span><span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">124.55</span><span class="token punctuation">,</span> <span class="token operator">-</span><span class="token number">113.80</span><span class="token punctuation">,</span> <span class="token number">32.45</span><span class="token punctuation">,</span> <span class="token number">42.05</span><span class="token punctuation">]</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.5</span><span class="token punctuation">,</span>
           cmap<span class="token operator">=</span>plt<span class="token punctuation">.</span>get_cmap<span class="token punctuation">(</span><span class="token string">"jet"</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>ylabel<span class="token punctuation">(</span><span class="token string">"Latitude"</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>xlabel<span class="token punctuation">(</span><span class="token string">"Longitude"</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>

prices <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span>
tick_values <span class="token operator">=</span> np<span class="token punctuation">.</span>linspace<span class="token punctuation">(</span>prices<span class="token punctuation">.</span><span class="token builtin">min</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> prices<span class="token punctuation">.</span><span class="token builtin">max</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token number">11</span><span class="token punctuation">)</span>
cbar <span class="token operator">=</span> plt<span class="token punctuation">.</span>colorbar<span class="token punctuation">(</span><span class="token punctuation">)</span>
cbar<span class="token punctuation">.</span>ax<span class="token punctuation">.</span>set_yticklabels<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token string">"$%dk"</span><span class="token operator">%</span><span class="token punctuation">(</span><span class="token builtin">round</span><span class="token punctuation">(</span>v<span class="token operator">/</span><span class="token number">1000</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token keyword">for</span> v <span class="token keyword">in</span> tick_values<span class="token punctuation">]</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>
cbar<span class="token punctuation">.</span>set_label<span class="token punctuation">(</span><span class="token string">'Median House Value'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">)</span>

plt<span class="token punctuation">.</span>legend<span class="token punctuation">(</span>fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"california_housing_prices_plot"</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure california_housing_prices_plot
</code></pre>
<p><img src="output_43_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">corr_matrix <span class="token operator">=</span> housing<span class="token punctuation">.</span>corr<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">corr_matrix<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>sort_values<span class="token punctuation">(</span>ascending<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>median_house_value    1.000000
median_income         0.687160
total_rooms           0.135097
housing_median_age    0.114110
households            0.064506
total_bedrooms        0.047689
population           -0.026920
longitude            -0.047432
latitude             -0.142724
Name: median_house_value, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment"># from pandas.tools.plotting import scatter_matrix # For older versions of Pandas</span>
<span class="token keyword">from</span> pandas<span class="token punctuation">.</span>plotting <span class="token keyword">import</span> scatter_matrix

attributes <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> <span class="token string">"median_income"</span><span class="token punctuation">,</span> <span class="token string">"total_rooms"</span><span class="token punctuation">,</span>
              <span class="token string">"housing_median_age"</span><span class="token punctuation">]</span>
scatter_matrix<span class="token punctuation">(</span>housing<span class="token punctuation">[</span>attributes<span class="token punctuation">]</span><span class="token punctuation">,</span> figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">12</span><span class="token punctuation">,</span> <span class="token number">8</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"scatter_matrix_plot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure scatter_matrix_plot
</code></pre>
<p><img src="output_46_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"median_income"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span>
             alpha<span class="token operator">=</span><span class="token number">0.1</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>axis<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">16</span><span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">550000</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
save_fig<span class="token punctuation">(</span><span class="token string">"income_vs_house_value_scatterplot"</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>Saving figure income_vs_house_value_scatterplot
</code></pre>
<p><img src="output_47_1.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">[</span><span class="token string">"rooms_per_household"</span><span class="token punctuation">]</span> <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"total_rooms"</span><span class="token punctuation">]</span><span class="token operator">/</span>housing<span class="token punctuation">[</span><span class="token string">"households"</span><span class="token punctuation">]</span>
housing<span class="token punctuation">[</span><span class="token string">"bedrooms_per_room"</span><span class="token punctuation">]</span> <span class="token operator">=</span> housing<span class="token punctuation">[</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">]</span><span class="token operator">/</span>housing<span class="token punctuation">[</span><span class="token string">"total_rooms"</span><span class="token punctuation">]</span>
housing<span class="token punctuation">[</span><span class="token string">"population_per_household"</span><span class="token punctuation">]</span><span class="token operator">=</span>housing<span class="token punctuation">[</span><span class="token string">"population"</span><span class="token punctuation">]</span><span class="token operator">/</span>housing<span class="token punctuation">[</span><span class="token string">"households"</span><span class="token punctuation">]</span>
</code></pre>
<p>Note: there was a bug in the previous cell, in the definition of the <code>rooms_per_household</code> attribute. This explains why the correlation value below differs slightly from the value in the book (unless you are reading the latest version).</p>
<pre class=" language-python"><code class="prism  language-python">corr_matrix <span class="token operator">=</span> housing<span class="token punctuation">.</span>corr<span class="token punctuation">(</span><span class="token punctuation">)</span>
corr_matrix<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>sort_values<span class="token punctuation">(</span>ascending<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
</code></pre>
<pre><code>median_house_value          1.000000
median_income               0.687160
rooms_per_household         0.146285
total_rooms                 0.135097
housing_median_age          0.114110
households                  0.064506
total_bedrooms              0.047689
population_per_household   -0.021985
population                 -0.026920
longitude                  -0.047432
latitude                   -0.142724
bedrooms_per_room          -0.259984
Name: median_house_value, dtype: float64
</code></pre>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>kind<span class="token operator">=</span><span class="token string">"scatter"</span><span class="token punctuation">,</span> x<span class="token operator">=</span><span class="token string">"rooms_per_household"</span><span class="token punctuation">,</span> y<span class="token operator">=</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span>
             alpha<span class="token operator">=</span><span class="token number">0.2</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>axis<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">520000</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<p><img src="output_51_0.png" alt="png"></p>
<pre class=" language-python"><code class="prism  language-python">housing<span class="token punctuation">.</span>describe<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>median_house_value</th>
      <th>rooms_per_household</th>
      <th>bedrooms_per_room</th>
      <th>population_per_household</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16354.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16512.000000</td>
      <td>16354.000000</td>
      <td>16512.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-119.575834</td>
      <td>35.639577</td>
      <td>28.653101</td>
      <td>2622.728319</td>
      <td>534.973890</td>
      <td>1419.790819</td>
      <td>497.060380</td>
      <td>3.875589</td>
      <td>206990.920724</td>
      <td>5.440341</td>
      <td>0.212878</td>
      <td>3.096437</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.001860</td>
      <td>2.138058</td>
      <td>12.574726</td>
      <td>2138.458419</td>
      <td>412.699041</td>
      <td>1115.686241</td>
      <td>375.720845</td>
      <td>1.904950</td>
      <td>115703.014830</td>
      <td>2.611712</td>
      <td>0.057379</td>
      <td>11.584826</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-124.350000</td>
      <td>32.540000</td>
      <td>1.000000</td>
      <td>6.000000</td>
      <td>2.000000</td>
      <td>3.000000</td>
      <td>2.000000</td>
      <td>0.499900</td>
      <td>14999.000000</td>
      <td>1.130435</td>
      <td>0.100000</td>
      <td>0.692308</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>-121.800000</td>
      <td>33.940000</td>
      <td>18.000000</td>
      <td>1443.000000</td>
      <td>295.000000</td>
      <td>784.000000</td>
      <td>279.000000</td>
      <td>2.566775</td>
      <td>119800.000000</td>
      <td>4.442040</td>
      <td>0.175304</td>
      <td>2.431287</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>-118.510000</td>
      <td>34.260000</td>
      <td>29.000000</td>
      <td>2119.500000</td>
      <td>433.000000</td>
      <td>1164.000000</td>
      <td>408.000000</td>
      <td>3.540900</td>
      <td>179500.000000</td>
      <td>5.232284</td>
      <td>0.203031</td>
      <td>2.817653</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>-118.010000</td>
      <td>37.720000</td>
      <td>37.000000</td>
      <td>3141.000000</td>
      <td>644.000000</td>
      <td>1719.250000</td>
      <td>602.000000</td>
      <td>4.744475</td>
      <td>263900.000000</td>
      <td>6.056361</td>
      <td>0.239831</td>
      <td>3.281420</td>
    </tr>
    <tr>
      <th>max</th>
      <td>-114.310000</td>
      <td>41.950000</td>
      <td>52.000000</td>
      <td>39320.000000</td>
      <td>6210.000000</td>
      <td>35682.000000</td>
      <td>5358.000000</td>
      <td>15.000100</td>
      <td>500001.000000</td>
      <td>141.909091</td>
      <td>1.000000</td>
      <td>1243.333333</td>
    </tr>
  </tbody>
</table>

<h1 id="prepare-the-data-for-machine-learning-algorithms-1">Prepare the data for Machine Learning algorithms</h1>
<pre class=" language-python"><code class="prism  language-python">housing <span class="token operator">=</span> strat_train_set<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"median_house_value"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span> <span class="token comment"># drop labels for training set</span>
housing_labels <span class="token operator">=</span> strat_train_set<span class="token punctuation">[</span><span class="token string">"median_house_value"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>copy<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<pre class=" language-python"><code class="prism  language-python">sample_incomplete_rows <span class="token operator">=</span> housing<span class="token punctuation">[</span>housing<span class="token punctuation">.</span>isnull<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token builtin">any</span><span class="token punctuation">(</span>axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">]</span><span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token punctuation">)</span>
sample_incomplete_rows
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4629</th>
      <td>-118.30</td>
      <td>34.07</td>
      <td>18.0</td>
      <td>3759.0</td>
      <td>NaN</td>
      <td>3296.0</td>
      <td>1462.0</td>
      <td>2.2708</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>6068</th>
      <td>-117.86</td>
      <td>34.01</td>
      <td>16.0</td>
      <td>4632.0</td>
      <td>NaN</td>
      <td>3038.0</td>
      <td>727.0</td>
      <td>5.1762</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>17923</th>
      <td>-121.97</td>
      <td>37.35</td>
      <td>30.0</td>
      <td>1955.0</td>
      <td>NaN</td>
      <td>999.0</td>
      <td>386.0</td>
      <td>4.6328</td>
      <td>&lt;1H OCEAN</td>
    </tr>
    <tr>
      <th>13656</th>
      <td>-117.30</td>
      <td>34.05</td>
      <td>6.0</td>
      <td>2155.0</td>
      <td>NaN</td>
      <td>1039.0</td>
      <td>391.0</td>
      <td>1.6675</td>
      <td>INLAND</td>
    </tr>
    <tr>
      <th>19252</th>
      <td>-122.79</td>
      <td>38.48</td>
      <td>7.0</td>
      <td>6837.0</td>
      <td>NaN</td>
      <td>3468.0</td>
      <td>1405.0</td>
      <td>3.1662</td>
      <td>&lt;1H OCEAN</td>
    </tr>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">sample_incomplete_rows<span class="token punctuation">.</span>dropna<span class="token punctuation">(</span>subset<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">]</span><span class="token punctuation">)</span>    <span class="token comment"># option 1</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>total_bedrooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_income</th>
      <th>ocean_proximity</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>

<pre class=" language-python"><code class="prism  language-python">sample_incomplete_rows<span class="token punctuation">.</span>drop<span class="token punctuation">(</span><span class="token string">"total_bedrooms"</span><span class="token punctuation">,</span> axis<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span>       <span class="token comment"># option 2</span>
</code></pre>
<div>
</div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>longitude</th>
      <th>latitude</th>
      <th>housing_median_age</th>
      <th>total_rooms</th>
      <th>population</th>
      <th>households</th>
      <th>median_i
</th></tr></thead></table>
