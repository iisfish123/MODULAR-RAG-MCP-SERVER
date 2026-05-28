# python 特性

0. """多行注释"""
1. input("请输入姓名：") 阻塞输出，直到用户回车输入
2. 字符串 f"你好，{name}" 格式化输出
3. range(start, stop, step) 生成一个序列，从 start 开始，到 stop 结束，步长为 step
4. match 表达式类似switch case 语句 + if 语句组合
5. for ... in 解构
6. while ... else 语句
7. 解构数组 [*arr1,*arr2]
8. 数据容器：list, tuple, dict, set, str
9. list数组函数集合

## 列表函数

1. 列表 list 可以修改

- num in list 检查元素是否在列表中
- num not in list 检查元素是否不在列表中
- 合并列表 + 运算符
- list[0, 2, 1] 切片 start\stop\step 从索引 0 开始，到索引 2 结束，步长为 1
- 列表推导式 [x * 2 for x in range(10)] 生成一个列表，列表中的元素为 0, 2, 4, 6, 8, 10, 12, 14, 16
- append() 添加元素
- pop() 删除最后一个元素
- insert() 插入元素
- remove() 删除元素
- clear() 清空列表
- sort() 排序
- reverse() 反转
- index() 查找元素索引
- count() 统计元素出现次数
- extend() 扩展列表
- copy() 复制列表
- pop() 删除元素
- clear() 清空列表
- sort() 排序
- reverse() 反转
- index() 查找元素索引
- count() 统计元素出现次数
- extend() 扩展列表
- copy() 复制列表
- pop() 删除元素
- clear() 清空列表
- sort() 排序
- reverse() 反转
- index() 查找元素索引
- count() 统计元素出现次数

------------------------------

## 字符串

1. str字符串无法修改，所以下列方法只能用于查询字符串信息而不能修改字符串

- len() 字符串长度
- str[0, 2, 1] 切片 start\stop\step 从索引 0 开始，到索引 2 结束，步长为 1
- find() 查找子字符串索引
- count() 统计子字符串出现次数
- replace() 替换子字符串
- split() 分割字符串
- join() 合并字符串
- upper() 转换为大写
- lower() 转换为小写
- title() 转换为标题格式
- strip() 移除首尾空格
- lstrip() 移除左侧空格
- rstrip() 移除右侧空格
- replace() 替换子字符串
- split() 分割字符串
- join() 合并字符串
- upper() 转换为大写
- lower() 转换为小写
- title() 转换为标题格式
- strip() 移除首尾空格
- lstrip() 移除左侧空格
- rstrip() 移除右侧空格
- replace() 替换子字符串
- split() 分割字符串
- join() 合并字符串
- upper() 转换为大写
- lower()

## 元组

1. 元组 tuple不可修改
2. 元组 t1 = (1, 2, 3, 4) 用()括起来或者直接写t1 = 1, 2, 3, 4
3. 解包1: a, b, c, d = t1
4. 解包2: a, b, c, d = t1[0], t1[1], t1[2], t1[3]
5. 解包3: a, b, c, d = t1[0:2], t1[2:3]
6. 解包4: a, *rest, d = t1 剩余解构

------------------------------

## 集合

1. set集合 无序，不重复，元素集合
2. {for s1 in foot_ball_set if s1 not in basket_ball_set}# 差集，只在foot_ball_set中的元素，不在basket_ball_set中
3. | 运算符 并集，合并s1和s2，返回新集合
4. & 运算符 交集，取s1和s2的交集，返回新集合
5. ^ 运算符 对称差集，只在s1或s2中的元素，但不在s1和s2同时存在返回新集合
6. - 运算符 差集，只在s1中的元素，不在s2中返回新集合

- set() 创建集合
- add() 添加元素
- remove() 删除元素
- clear() 清空集合
- len() 集合长度
- union() 并集 s1.union(s2) 合并s1和s2，返回新集合
- intersection() 交集 s1.intersection(s2) 取s1和s2的交集，返回新集合
- difference() 差集 s1.difference(s2) 只在s1中的元素
- symmetric_difference() 对称差集 s1.symmetric_difference(s2) 只在s1或s2中的元素，但不在s1和s2同时存在返回新集合

------------------------------

## 字典

1. dict字典 无序，不重复，键值对集合
2. dict1 = {'name': '张三', 'age': 18, 'gender': '男'} # 字典字面值
3. for k, v in dict1.items(): 遍历字典的所有键值对，k为键，v为值

- dict() 创建字典
- len() 字典长度
- dict.keys() 获取所有键
- dict.values() 获取所有值
- dict.items() 获取所有键值对
- dict.get('name') 获取键为name的值
- dict.get('name', '默认值') 获取键为name的值，若不存在则返回默认值
- dict.pop('name') 删除键为name的键值对
- dict.popitem() 删除最后一个键值对
- dict.update({'name': '李四', 'age': 20}) 更新字典
- dict.clear() 清空字典
- del dict['name'] 删除键为name的键值对

### 数据容器总结与对比

| 特性 | 字符串（str） | 列表（list） | 元组（tuple） | 集合（set） | 字典（dict） |
| --- | --- | --- | --- | --- | --- |
| 有序性 | 有序 | 有序 | 有序 | 无序 | 有序（3.7+） |
| 重复元素 | 允许 | 允许 | 允许 | 不允许 | key 不允许 |
| 可变性 | 不可变 | 可变 | 不可变 | 可变 | 可变 |
| 索引访问 | 支持 | 支持 | 支持 | 不支持 | 不支持 |
| 切片操作 | 支持 | 支持 | 支持 | 不支持 | 不支持 |
| 使用场景 | 文本处理 | 有序可重复数据集合 | 固定数据记录 | 去重数据集合 | 键值对 |

## 函数

1. def 函数
2. 返回值可以返回多个值，用逗号隔开，返回值为元组
3. 函数最好写函数文档, 用"""多行注释括起来，说明函数的功能，参数param，返回值return等，用于IDE提示
4. 函数内部修改全局变量，可以使用global关键字
5. 函数传参 - 固定参数：位置参数、关键字参数name=value1, name2=value2
6. 函数传参 - 不定长参数：可变参数*args；关键字传递参数**kwargs，kwargs是dict字典键值对类型.kwargs('name')

------------------------------

## 匿名函数

1. lambda 匿名函数 不能换行
2. lambda 参数列表: 函数体; 如 add = lambda x, y: x + y; add()
total_price = [goods[1] + goods[2] for goods in args]

------------------------------

## 类型注解

1. 类型注解用于在函数参数、返回值、变量等位置指定类型，用于IDE提示和类型检查
2. 变量跟TS类型注解类似，用于指定变量的类型，用于IDE提示和类型检查
3. 函数def 函数名(参数1: 类型1, 参数2: 类型2, ...) -> 返回值类型: 函数体
4. 例子 def add(a: tuple[int, int]) -> int: return a[0] + a[1]

------------------------------

## 模块导入方式

导入方式有如下5种方式：

1. 模块，一个.py文件就是一个模块，是组织代码方式，模块可以定义函数、类、变量等
2. import 模块名 导入模块
3. from 模块名 import 函数名, 类名, 变量名 导入模块中的函数、类、变量
4. from 模块名 import * 导入模块中的所有函数、类、变量
5. import 模块名 as 别名 导入模块并起别名
6. from 模块名 import * as 别名 导入模块中的所有函数、类、变量并起别名
7. from 模块名 import * 通配符 - 导入模块中的所有函数、类、变量
8. __all__关键字； 只影响import \* 的导入方式不会影响其他导入方式，由上述可知道import* 可以导出所有， 那么在模块内部定义 __all__ = ['函数名', '类名', '变量名'] 导出模块中的函数、类、变量，用于导入模块时指定导出的函数、类、变量，若不指定则导出所有函数、类、变量，用于导入模块时指定导出的函数、类、变量，若不指定则导出所有函数、类、变量

9. 可以使用 拿到模块的变量，函数，类等
10. __name__关键字；__name__ == '__main__' 判断是否是主程序，若为True程序从main函数开始执行
11. if __name__ == '__main__':
    print('hello world')

12. python内置模块如下：

- math 数学模块
- random 随机数模块
- time 时间模块
- sys 系统模块
- os 操作系统模块
- re 正则表达式模块
- json JSON模块
- csv CSV模块
- xml XML模块
- html HTML模块
- xml.etree.ElementTree XML模块
- xml.dom.minidom XML模块
- xml.dom.minidom.minidom XML模块
- xml.dom.minidom.minidom.minidom XML模块

------------------------------

## 包package 包本质是文件夹，包含了特殊文件__init__.py，用于标识这是一个包

包的5种导入方式：

1. import 包名 导入包
2. from 包名 import 函数名, 类名, 变量名 导入包中的函数、类、变量
3. from 包名 import * 导入包中的所有函数、类、变量
4. import 包名 as 别名 导入包并起别名
5. from 包名 import * as 别名 导入包中的所有函数、类、变量并起别名
6. from 包名 import * 通配符 - 导入包中的所有函数、类、变量
7. __all__关键字； 只影响import \* 的导入方式不会影响其他导入方式，由上述可知道import* 可以导出所有， 那么在包内部定义 __all__ = ['函数名', '类名', '变量名'] 导出包中的函数、类、变量，用于导入包时指定导出的函数、类、变量，若不指定则导出所有函数、类、变量，用于导入包时指定

------------------------------

## 类class

1. 定义类、属性、方法、魔法方法，并实例化对象
2. 各种魔法方法
3. 静态属性（车有4个轮子）没有实例属性就去找类属性、静态方法

```python
# 定义
class 类名:
    __private = 11
    def __init__(self, 参数1, 参数2, ...): # 魔法方法，用于初始化对象的属性，类似构造函数()
        self.属性名 = 参数1
        self.属性名 = 参数2
        ...
    def __str__(self): # 魔法方法，返回对象的字符串表示 print(obj)的时候默认调用此方法，相当toString()
        return f'类名({self.属性名}, {self.属性名})'
    def 方法名(self):
        方法体
    def running():
        print('running')
# 实例化
obj = 类名(参数1, 参数2, ...)
# 调用方法
obj.方法名()
```

## 异常处理

1. try-except语句
2. except语句
3. finally语句

```python
try:
    代码块1
except 异常类型1 as 变量1:
    代码块2
except 异常类型2 as 变量2:
    代码块3
finally:
    代码块4
```

## python web介绍

1. flask 框架
2. django 框架
3. fastapi 框架

------------------------------

## 面向 AI Agent + RAG 的工程化补充（Node.js 转 Python）

### 1) 运行方式与模块导入心智模型

1. 一个 `.py` 文件就是一个模块；一个包含 `__init__.py` 的目录就是一个包（package）
2. 推荐用模块方式运行，能避免很多相对导入问题：

```bash
python -m package.module
```

1. 入口惯用法（脚本模式）：

```python
def main() -> None:
    print("hello")

if __name__ == "__main__":
    main()
```

1. 导入规则要点：
   1. `import xxx` / `from xxx import yyy` 都基于 `sys.path` 查找
   2. 同名文件/目录会遮蔽标准库或第三方包（例如你写了 `json.py`）
   3. 包内模块互相导入，优先使用显式相对导入（`from .utils import foo`）或保证用 `python -m` 从包根运行

### 2) `.venv` 虚拟环境（建议每个项目一个）

目标：保证“解释器 + 依赖”只在当前项目里生效，避免全局污染。

1. 在项目根目录创建虚拟环境（macOS/Linux）：

```bash
python3 -m venv .venv
```

1. 激活/退出：

```bash
source .venv/bin/activate
deactivate
```

1. 永远用 `python -m pip`，避免 pip 指向错误解释器：

```bash
python -m pip install --upgrade pip
python -m pip install <package>
python -m pip list
```

1. 快速自检“pip 和 python 是同一个环境”：

```bash
which python
python -c "import sys; print(sys.executable)"
python -m pip -V
```

1. 依赖冻结与还原（学习阶段最朴素可靠）：

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

1. 建议把 `.venv/` 加入 gitignore（只建议，不强制）

### 3) 文件与数据处理（RAG 场景高频）

1. 用 `pathlib.Path` 代替字符串拼路径：

```python
from pathlib import Path

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "docs.txt"
text = data_path.read_text(encoding="utf-8")
```

1. JSON 读写（注意 `ensure_ascii=False` 保留中文）：

```python
import json
from pathlib import Path

path = Path("data.json")
obj = json.loads(path.read_text(encoding="utf-8"))
path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
```

1. 文本编码常见坑：默认编码在不同机器上可能不同；读写文本尽量显式 `encoding="utf-8"`

### 4) 类型标注进阶（写 Agent/RAG 代码更稳）

1. 常用类型：
   1. `list[str]` / `dict[str, int]`
   2. `Any`：不得已才用
   3. `Optional[T]`：`T | None`（Python 3.10+）
   4. `Callable[[In], Out]`：回调函数

```python
from typing import Any, Callable

def run_pipeline(items: list[str], transform: Callable[[str], str]) -> list[str]:
    return [transform(x) for x in items]

def parse_payload(payload: dict[str, Any]) -> str | None:
    value = payload.get("text")
    return value if isinstance(value, str) else None
```

1. 结构化字典（比 `dict[str, Any]` 更强）：

```python
from typing import TypedDict

class Document(TypedDict):
    id: str
    content: str
    source: str
```

### 5) 数据对象：`dataclasses`

适合做轻量数据容器（比如文档、检索结果、工具输入输出）。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Doc:
    id: str
    content: str
    source: str
```

### 6) 异步基础（Agent/RAG 编排经常需要）

1. `async def` 定义协程，`await` 等待 I/O
2. 并发跑多个 I/O 用 `asyncio.gather`
3. 限流用 `asyncio.Semaphore`（避免同时请求过多）

```python
import asyncio

async def fetch(x: int) -> int:
    await asyncio.sleep(0.1)
    return x * 2

async def main() -> None:
    results = await asyncio.gather(*(fetch(i) for i in range(5)))
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

### 7) 日志与异常（比 print 更适合工程）

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("app")

def work() -> None:
    logger.info("start")

work()
```

### 8) 纠错与易错点（对照你现有笔记）

1. 切片写法是 `obj[start:stop:step]`，不是 `obj[0, 2, 1]`
2. 集合推导式是 `{expr for x in xs if cond}`，例如 `{x for x in a if x not in b}`
3. Python 里没有 `from 模块名 import * as 别名` 这种语法；需要别名用：

```python
import some_module as m
from some_module import some_func as f
```

### 9) `with` 上下文管理器（资源自动释放）

核心：`with` 会在代码块结束时自动“收尾”，无论是正常结束还是抛异常。常见用途：文件、锁、连接、临时目录等。
with open() 会自动调用 close() 方法关闭文件，无需手动调用。保证数据安全

```python
with open("demo.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

1. 文件读写（最常见）：

```python
from pathlib import Path

path = Path("demo.txt")
path.write_text("hello\n", encoding="utf-8")

with path.open("r", encoding="utf-8") as f:
    text = f.read()
```

1. 自定义上下文管理器：实现 `__enter__` / `__exit__`

```python
class Timer:
    def __enter__(self):
        import time

        self._time = time
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = self._time.perf_counter() - self.start
        return False


with Timer() as t:
    total = sum(range(100000))

_ = t.elapsed
```

1. `contextlib`（标准库）常用工具：

```python
from contextlib import ExitStack, contextmanager, suppress
from pathlib import Path

@contextmanager
def open_two(a: Path, b: Path):
    with a.open("r", encoding="utf-8") as fa, b.open("r", encoding="utf-8") as fb:
        yield fa, fb


with suppress(FileNotFoundError):
    Path("missing.txt").read_text(encoding="utf-8")


paths = [Path("a.txt"), Path("b.txt")]
for p in paths:
    p.write_text(p.name, encoding="utf-8")

with ExitStack() as stack:
    files = [stack.enter_context(p.open("r", encoding="utf-8")) for p in paths]
    data = [f.read() for f in files]
```

1. `async with`（异步资源管理：HTTP session / 连接池等常见）

```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def call(self) -> str:
        await asyncio.sleep(0.01)
        return "ok"


async def main() -> None:
    async with AsyncResource() as r:
        _ = await r.call()

asyncio.run(main())
```

### 10) 迭代器与生成器（大数据/大文件友好）

1. 迭代协议：`iter(obj)` 得到迭代器，`next(it)` 逐个取值，耗尽会抛 `StopIteration`
2. 生成器：用 `yield` 一边产出一边计算，适合 RAG 的“文档流式加载/处理”

```python
from collections.abc import Iterator
from pathlib import Path

def iter_lines(path: Path) -> Iterator[str]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line:
                yield line


path = Path("lines.txt")
path.write_text("a\n\nb\n", encoding="utf-8")
items = list(iter_lines(path))
```

1. 生成器表达式（惰性） vs 列表推导式（立即创建列表）：

```python
nums = (i * 2 for i in range(10))
first_three = [next(nums) for _ in range(3)]
```

### 11) 装饰器（Decorator）

1. 装饰器本质：函数接收函数并返回新函数；`@decorator` 是语法糖
2. `functools.wraps` 用来保留原函数的名字/文档/签名信息

```python
from functools import wraps
from time import perf_counter

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        elapsed = perf_counter() - start
        return result, elapsed

    return wrapper

@timed
def add(a: int, b: int) -> int:
    return a + b

value, cost = add(1, 2)
```

1. `lru_cache`（适合缓存“纯函数”的结果，比如一些解析/标准化逻辑）

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def normalize(s: str) -> str:
    return " ".join(s.lower().split())
```

### 12) 标准库高频工具（collections / itertools / functools）

1. `collections.Counter` 统计：

```python
from collections import Counter

counts = Counter(["a", "b", "a"])
top = counts.most_common(1)
```

1. `collections.defaultdict` 分组聚合：

```python
from collections import defaultdict

groups: defaultdict[str, list[int]] = defaultdict(list)
for k, v in [("a", 1), ("a", 2), ("b", 3)]:
    groups[k].append(v)
```

1. `collections.deque` 双端队列（比 list 更适合频繁头部 pop）：

```python
from collections import deque

q = deque([1, 2, 3])
q.appendleft(0)
first = q.popleft()
```

1. `itertools.chain / islice`（拼接与截取迭代器）：

```python
from itertools import chain, islice

xs = chain([1, 2], [3, 4])
first_two = list(islice(xs, 2))
```

1. `itertools.groupby`（按相邻相同 key 分组，通常需要先排序）：

```python
from itertools import groupby

items = ["a", "a", "b", "b", "b", "a"]
groups = [(k, list(g)) for k, g in groupby(items)]
```

1. `functools.partial`（偏函数，等价于“预先绑定部分参数”）：

```python
from functools import partial

def mul(a: int, b: int) -> int:
    return a * b

double = partial(mul, 2)
value = double(21)
```

### 13) 配置与环境变量（不要把密钥写死）

1. 基础读法：`os.getenv(key, default)`，并做类型转换：

```python
import os

port = int(os.getenv("APP_PORT", "8000"))
debug = os.getenv("APP_DEBUG", "false").lower() in {"1", "true", "yes", "y"}
```

1. 复杂配置（JSON 形式放进环境变量）：

```python
import json
import os

raw = os.getenv("APP_ALLOWED_ORIGINS", "[]")
origins = json.loads(raw)
```

1. 约定：密钥（API Key、Token）只放环境变量或安全的密钥管理里，不写进仓库文件
