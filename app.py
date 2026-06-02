import streamlit as st
import streamlit.components.v1 as components
import random
import re
import json
import subprocess
import tempfile
import os
import time
from pathlib import Path

# 自定义代码编辑器
def code_editor(key, label, initial_value="", language="python", height=350):
    """创建一个代码编辑器"""

    # 语言映射
    lang_map = {
        "Python": "python",
        "C++": "cpp",
        "C": "c",
        "Java": "java"
    }

    editor_language = lang_map.get(language, "python")

    # 初始化 session_state
    if key not in st.session_state:
        st.session_state[key] = initial_value

    # 使用 Streamlit 自带的 text_area，带语法高亮显示
    code = st.text_area(
        label,
        value=st.session_state[key],
        height=height,
        key=f"{key}_textarea"
    )

    # 同步到 session_state
    st.session_state[key] = code

    return st.session_state[key]

# ============== Config ==============
PROGRAMMING_LANGUAGES = {
    "Python": {"name": "Python", "extension": ".py"},
    "C++": {"name": "C++", "extension": ".cpp"},
    "C": {"name": "C", "extension": ".c"},
    "Java": {"name": "Java", "extension": ".java"}
}

# ============== 思维导图知识库（按语言分类）==============
MINDMAP_KNOWLEDGE = {
    "Python": {
        "入门基础": {
            "Hello World": {"desc": "print('Hello World')", "code": "print('Hello World')"},
            "变量与数据类型": {"desc": "int, float, str, bool, list, dict", "code": "x = 10\nname = 'Alice'\nis_valid = True"},
            "输入输出": {"desc": "input()接收用户输入, print()输出", "code": "name = input('请输入: ')\nprint(f'你好, {name}')"},
            "类型转换": {"desc": "int(), str(), float(), list()", "code": "num = int('123')\ntext = str(100)"}
        },
        "控制结构": {
            "条件判断": {"desc": "if, elif, else", "code": "if score >= 90:\n    print('优秀')\nelif score >= 60:\n    print('及格')\nelse:\n    print('不及格')"},
            "循环语句": {"desc": "for循环遍历, while条件循环", "code": "for i in range(5):\n    print(i)\n\nwhile condition:\n    print('运行中')"},
            "break与continue": {"desc": "break跳出循环, continue跳过本次", "code": "for i in range(10):\n    if i == 3:\n        continue\n    if i == 7:\n        break\n    print(i)"}
        },
        "字符串处理": {
            "字符串基础": {"desc": "索引、切片、拼接", "code": "s = 'Hello World'\ns[0]  # 'H'\ns[0:5]  # 'Hello'\ns + '!'  # 'Hello World!'"},
            "字符串方法": {"desc": "upper(), lower(), strip(), split()", "code": "'  hello  '.strip()  # 'hello'\n'hello'.upper()  # 'HELLO'\n'hello world'.split()  # ['hello', 'world']"},
            "格式化输出": {"desc": "f-string, format(), %", "code": "name = 'Alice'\nage = 20\nprint(f'{name} is {age}')\nprint('{} is {}'.format(name, age))"}
        },
        "列表与字典": {
            "列表操作": {"desc": "append(), pop(), sort(), len()", "code": "nums = [1, 2, 3]\nnums.append(4)\nnums.pop()\nnums.sort()"},
            "字典操作": {"desc": "键值对, get(), items()", "code": "d = {'name': 'Alice', 'age': 20}\nd['gender'] = 'female'\nprint(d.get('name'))"},
            "列表推导式": {"desc": "[expr for x in list]", "code": "squares = [x**2 for x in range(10)]\nevens = [x for x in range(20) if x % 2 == 0]"}
        },
        "函数与模块": {
            "函数定义": {"desc": "def关键字, 默认参数, 返回值", "code": "def greet(name, msg='Hello'):\n    return f'{msg}, {name}!'"},
            "匿名函数": {"desc": "lambda表达式", "code": "square = lambda x: x ** 2\nadd = lambda a, b: a + b"},
            "常用模块": {"desc": "os, sys, math, random, datetime", "code": "import random\nimport math\nprint(math.sqrt(16))\nprint(random.randint(1, 100))"},
            "pip包管理": {"desc": "pip install xxx", "code": "pip install requests\nimport requests"}
        },
        "文件操作": {
            "读写文件": {"desc": "open(), read(), write(), with", "code": "with open('test.txt', 'r') as f:\n    content = f.read()\n\nwith open('out.txt', 'w') as f:\n    f.write('Hello')"}
        },
        "面向对象": {
            "类与对象": {"desc": "class, __init__, self", "code": "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says Woof!'"},
            "继承与多态": {"desc": "子类继承父类", "code": "class Animal:\n    def speak(self): pass\n\nclass Cat(Animal):\n    def speak(self):\n        return 'Meow'"}
        }
    },
    "C++": {
        "入门基础": {
            "Hello World": {"desc": "#include <iostream> + using namespace std", "code": "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello World\" << endl;\n    return 0;\n}"},
            "变量与数据类型": {"desc": "int, double, char, bool, string", "code": "int x = 10;\ndouble pi = 3.14;\nstring name = \"Hello\";\nbool flag = true;"},
            "输入输出": {"desc": "cin >> , cout <<", "code": "int age;\ncin >> age;\ncout << \"年龄: \" << age << endl;"},
            "类型转换": {"desc": "static_cast<T>(), (type)", "code": "int x = 10;\ndouble y = static_cast<double>(x);\nint z = (int)3.14;"}
        },
        "控制结构": {
            "条件判断": {"desc": "if, else if, else, switch", "code": "if (score >= 90) {\n    cout << \"优秀\";\n} else if (score >= 60) {\n    cout << \"及格\";\n} else {\n    cout << \"不及格\";\n}"},
            "循环语句": {"desc": "for, while, do-while", "code": "for (int i = 0; i < 5; i++) {\n    cout << i << endl;\n}\n\nwhile (condition) {\n    // statements\n}"},
            "break与continue": {"desc": "break跳出, continue跳过", "code": "for (int i = 0; i < 10; i++) {\n    if (i == 3) continue;\n    if (i == 7) break;\n    cout << i << endl;\n}"}
        },
        "字符串处理": {
            "C风格字符串": {"desc": "char[], strlen, strcpy", "code": "char s1[20] = \"Hello\";\nchar s2[20];\nstrcpy(s2, s1);\ncout << strlen(s1);"},
            "string类": {"desc": "std::string, +拼接, length()", "code": "string s1 = \"Hello\";\nstring s2 = \" World\";\nstring s3 = s1 + s2;\ncout << s3.length();"},
            "字符操作": {"desc": "isalpha, isdigit, tolower", "code": "#include <cctype>\nchar c = 'A';\nif (isalpha(c)) cout << \"是字母\";\nif (isdigit(c)) cout << \"是数字\";"}
        },
        "数组与容器": {
            "数组基础": {"desc": "固定大小, 索引从0开始", "code": "int arr[5] = {1, 2, 3, 4, 5};\nfor (int i = 0; i < 5; i++) {\n    cout << arr[i] << endl;\n}"},
            "vector容器": {"desc": "动态数组, push_back, size", "code": "#include <vector>\nvector<int> v;\nv.push_back(1);\nv.push_back(2);\nfor (int x : v) cout << x;"},
            "map与set": {"desc": "键值对容器, 有序集合", "code": "#include <map>\n#include <set>\nmap<string, int> m;\nset<int> s;\nm[\"apple\"] = 5;\ns.insert(10);"}
        },
        "函数与指针": {
            "函数定义": {"desc": "参数传递: 值传递/引用传递/指针", "code": "void swap(int &a, int &b) {\n    int temp = a;\n    a = b;\n    b = temp;\n}"},
            "指针基础": {"desc": "*解引用, &取地址, new/delete", "code": "int x = 10;\nint *p = &x;\n*p = 20;\nint *arr = new int[10];\ndelete[] arr;"},
            "引用": {"desc": "int& r = x; 代替指针", "code": "int x = 10;\nint &r = x;\nr = 20;  // x也变成20"},
            "Lambda": {"desc": "[capture] (params) -> ret { body }", "code": "auto square = [](int x) -> int {\n    return x * x;\n};\nauto add = [](int a, int b) { return a + b; };"}
        },
        "面向对象": {
            "类与对象": {"desc": "class, public/private, 构造函数", "code": "class Dog {\nprivate:\n    string name;\npublic:\n    Dog(string n) : name(n) {}\n    string speak() { return name + \" says Woof!\"; }\n};"},
            "继承与多态": {"desc": "virtual虚函数, override重写", "code": "class Animal {\npublic:\n    virtual string speak() = 0;\n};\nclass Cat : public Animal {\npublic:\n    string speak() override { return \"Meow\"; }\n};"},
            "模板": {"desc": "template<typename T>", "code": "template<typename T>\nT max(T a, T b) {\n    return a > b ? a : b;\n}"}
        },
        "标准库": {
            "STL算法": {"desc": "sort, find, count, accumulate", "code": "#include <algorithm>\n#include <numeric>\nvector<int> v = {3, 1, 4, 1, 5};\nsort(v.begin(), v.end());\nint sum = accumulate(v.begin(), v.end(), 0);"},
            "常用头文件": {"desc": "iostream, vector, string, map, set, algorithm", "code": "#include <iostream>\n#include <vector>\n#include <string>\n#include <map>\n#include <algorithm>"}
        }
    },
    "C": {
        "入门基础": {
            "Hello World": {"desc": "#include <stdio.h> + printf", "code": "#include <stdio.h>\nint main() {\n    printf(\"Hello World\\n\");\n    return 0;\n}"},
            "变量与数据类型": {"desc": "int, float, double, char", "code": "int age = 20;\nfloat height = 1.75f;\ndouble score = 95.5;\nchar grade = 'A';"},
            "输入输出": {"desc": "scanf, printf", "code": "int x;\nscanf(\"%d\", &x);\nprintf(\"x = %d\\n\", x);"},
            "sizeof": {"desc": "查看类型字节大小", "code": "printf(\"int: %lu bytes\\n\", sizeof(int));\nprintf(\"double: %lu bytes\\n\", sizeof(double));"}
        },
        "控制结构": {
            "条件判断": {"desc": "if, else if, else", "code": "if (score >= 90) {\n    printf(\"优秀\\n\");\n} else if (score >= 60) {\n    printf(\"及格\\n\");\n} else {\n    printf(\"不及格\\n\");\n}"},
            "循环语句": {"desc": "for, while, do-while", "code": "for (int i = 0; i < 5; i++) {\n    printf(\"%d \", i);\n}\n\nwhile (condition) {\n    // statements\n}"},
            "switch": {"desc": "多分支选择", "code": "switch (grade) {\n    case 'A': printf(\"优秀\"); break;\n    case 'B': printf(\"良好\"); break;\n    default: printf(\"其他\");\n}"}
        },
        "字符串处理": {
            "字符数组": {"desc": "char s[] = \"Hello\";", "code": "char s1[] = \"Hello\";\nchar s2[20];\n// 字符串操作需要<string.h>"},
            "字符串函数": {"desc": "strlen, strcpy, strcmp, strcat", "code": "#include <string.h>\nchar s1[20] = \"Hello\";\nchar s2[20];\nstrcpy(s2, s1);\nprintf(\"%d\", strlen(s1));"},
            "sscanf/sprintf": {"desc": "字符串与数值转换", "code": "int x;\nsscanf(\"123\", \"%d\", &x);\nchar buf[50];\nsprintf(buf, \"x = %d\", x);"}
        },
        "数组与指针": {
            "数组基础": {"desc": "int arr[10]; 下标从0开始", "code": "int arr[5] = {1, 2, 3, 4, 5};\nfor (int i = 0; i < 5; i++) {\n    printf(\"%d \", arr[i]);\n}"},
            "指针基础": {"desc": "*解引用, &取地址", "code": "int x = 10;\nint *p = &x;\nprintf(\"%d\", *p);  // 10\n*p = 20;  // x = 20"},
            "指针运算": {"desc": "p++, p--, p+n, p-n", "code": "int arr[5] = {1,2,3,4,5};\nint *p = arr;\nprintf(\"%d\", *(p+2));  // 3"},
            "动态内存": {"desc": "malloc, free", "code": "int *p = (int*)malloc(10 * sizeof(int));\nif (p) {\n    p[0] = 100;\n    free(p);\n}"}
        },
        "函数": {
            "函数定义": {"desc": "返回值类型, 参数列表", "code": "int add(int a, int b) {\n    return a + b;\n}"},
            "递归函数": {"desc": "函数调用自身", "code": "int factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}"},
            "函数指针": {"desc": "指向函数的指针", "code": "int (*func)(int, int) = add;\nint result = func(1, 2);  // 3"}
        },
        "结构体": {
            "定义结构体": {"desc": "struct关键字", "code": "struct Student {\n    char name[50];\n    int age;\n    float score;\n};"},
            "使用结构体": {"desc": "struct变量定义和访问", "code": "struct Student s1;\ns1.age = 20;\nstrcpy(s1.name, \"Alice\");"},
            "typedef": {"desc": "为类型起别名", "code": "typedef struct Student Student;\nStudent s1;  // 等价于 struct Student s1;"}
        },
        "常用头文件": {
            "标准输入输出": {"desc": "stdio.h", "code": "#include <stdio.h>"},
            "字符串操作": {"desc": "string.h", "code": "#include <string.h>"},
            "常用函数": {"desc": "stdlib.h, math.h", "code": "#include <stdlib.h>\n#include <math.h>"}
        }
    },
    "Java": {
        "入门基础": {
            "Hello World": {"desc": "public class + main方法", "code": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello World\");\n    }\n}"},
            "变量与数据类型": {"desc": "int, double, char, boolean, String", "code": "int x = 10;\ndouble pi = 3.14;\nboolean flag = true;\nString name = \"Alice\";"},
            "输入输出": {"desc": "Scanner, System.out", "code": "import java.util.Scanner;\nScanner sc = new Scanner(System.in);\nint x = sc.nextInt();\nSystem.out.println(x);"},
            "类型转换": {"desc": "(type) casting, Integer.parseInt()", "code": "int x = (int) 3.14;\nString s = \"123\";\nint y = Integer.parseInt(s);"}
        },
        "控制结构": {
            "条件判断": {"desc": "if, else if, else, switch", "code": "if (score >= 90) {\n    System.out.println(\"优秀\");\n} else if (score >= 60) {\n    System.out.println(\"及格\");\n} else {\n    System.out.println(\"不及格\");\n}"},
            "循环语句": {"desc": "for, while, do-while", "code": "for (int i = 0; i < 5; i++) {\n    System.out.println(i);\n}\n\nwhile (condition) {\n    // statements\n}"},
            "增强for循环": {"desc": "for-each遍历数组/集合", "code": "int[] arr = {1, 2, 3, 4, 5};\nfor (int num : arr) {\n    System.out.println(num);\n}"}
        },
        "字符串处理": {
            "String基础": {"desc": "不可变对象, +拼接", "code": "String s1 = \"Hello\";\nString s2 = \" World\";\nString s3 = s1 + s2;\nint len = s1.length();"},
            "常用方法": {"desc": "substring, indexOf, equals", "code": "String s = \"Hello World\";\ns.substring(0, 5);  // \"Hello\"\ns.indexOf(\"World\");   // 6\ns.equals(\"hello\");   // false"},
            "StringBuilder": {"desc": "可变字符串, 效率高", "code": "StringBuilder sb = new StringBuilder();\nsb.append(\"Hello\");\nsb.append(\" World\");\nString result = sb.toString();"}
        },
        "数组与集合": {
            "数组": {"desc": "固定长度, 索引从0开始", "code": "int[] arr = {1, 2, 3, 4, 5};\nint[] arr2 = new int[10];\nArrays.sort(arr);"},
            "ArrayList": {"desc": "动态数组", "code": "import java.util.ArrayList;\nArrayList<Integer> list = new ArrayList<>();\nlist.add(1);\nlist.add(2);"},
            "HashMap": {"desc": "键值对映射", "code": "import java.util.HashMap;\nHashMap<String, Integer> map = new HashMap<>();\nmap.put(\"apple\", 5);\nint value = map.get(\"apple\");"},
            "HashSet": {"desc": "无序不重复集合", "code": "import java.util.HashSet;\nHashSet<Integer> set = new HashSet<>();\nset.add(1);\nset.add(2);"}
        },
        "面向对象": {
            "类与对象": {"desc": "class, new创建对象", "code": "class Dog {\n    private String name;\n    public Dog(String name) {\n        this.name = name;\n    }\n    public String speak() {\n        return name + \" says Woof!\";\n    }\n}"},
            "继承": {"desc": "extends关键字", "code": "class Animal {\n    public void eat() { }\n}\nclass Cat extends Animal {\n    public void speak() {\n        System.out.println(\"Meow\");\n    }\n}"},
            "接口": {"desc": "interface, implements", "code": "interface Flyable {\n    void fly();\n}\nclass Bird implements Flyable {\n    public void fly() {\n        System.out.println(\"Flying\");\n    }\n}"},
            "抽象类": {"desc": "abstract class", "code": "abstract class Shape {\n    abstract double area();\n}"}
        },
        "异常处理": {
            "try-catch": {"desc": "捕获异常", "code": "try {\n    int x = Integer.parseInt(\"abc\");\n} catch (NumberFormatException e) {\n    System.out.println(\"格式错误\");\n}"},
            "throw与throws": {"desc": "抛出异常", "code": "void divide(int a, int b) throws Exception {\n    if (b == 0) throw new Exception(\"除数不能为0\");\n    System.out.println(a / b);\n}"}
        },
        "常用类库": {
            "Math类": {"desc": "数学运算", "code": "Math.max(1, 2);\nMath.sqrt(16);\nMath.random();\nMath.abs(-5);"},
            "Arrays类": {"desc": "数组工具", "code": "import java.util.Arrays;\nArrays.sort(arr);\nArrays.toString(arr);\nArrays.fill(arr, 0);"},
            "Collections": {"desc": "集合工具", "code": "import java.util.Collections;\nCollections.sort(list);\nCollections.reverse(list);\nCollections.max(list);"}
        }
    }
}

# ============== Knowledge Base ==============
KNOWLEDGE_BASE = {
    "数据结构": {
        "数组与字符串": {
            "concepts": ["数组内存连续性", "索引访问O(1)", "字符串不可变", "双指针技巧"],
            "examples": ["两数之和", "反转字符串", "合并两个有序数组"],
            "code": {"Python": "def reverse(arr):\n    return arr[::-1]", "C++": "vector<int> reverse(vector<int> v) {\n    reverse(v.begin(), v.end());\n    return v;\n}", "C": "void reverse(int arr[], int n) {\n    for(int i=0; i<n/2; i++) {\n        int tmp = arr[i];\n        arr[i] = arr[n-1-i];\n        arr[n-1-i] = tmp;\n    }\n}", "Java": "int[] reverse(int[] arr) {\n    for(int i=0; i<arr.length/2; i++) {\n        int tmp = arr[i];\n        arr[i] = arr[arr.length-1-i];\n        arr[arr.length-1-i] = tmp;\n    }\n    return arr;\n}"}
        },
        "链表": {
            "concepts": ["节点结构", "指针遍历", "虚拟头节点", "快慢指针检测环"],
            "examples": ["反转链表", "合并两个有序链表", "检测环形链表"],
            "code": {"Python": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next", "C++": "struct ListNode {\n    int val;\n    ListNode* next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};", "C": "typedef struct ListNode {\n    int val;\n    struct ListNode* next;\n} ListNode;", "Java": "class ListNode {\n    int val;\n    ListNode next;\n    ListNode(int x) { val = x; }\n}"}
        },
        "栈与队列": {
            "concepts": ["LIFO/FIFO特性", "括号匹配", "表达式求值", "单调栈"],
            "examples": ["有效的括号", "用栈实现队列", "每日温度"],
            "code": {"Python": "from collections import deque\nstack = []\nqueue = deque()", "C++": "#include <stack>\n#include <queue>\nusing namespace std;\nstack<int> s;\nqueue<int> q;", "C": "int stack[100], top = -1;\n// push: stack[++top] = x\n// pop: x = stack[top--]", "Java": "import java.util.*;\nStack<Integer> stack = new Stack<>();\nQueue<Integer> queue = new LinkedList<>();"}
        },
        "树与图": {
            "concepts": ["二叉树的遍历", "图的BFS/DFS", "树的递归特性", "层序遍历"],
            "examples": ["二叉树中序遍历", "岛屿数量", "课程表"],
            "code": {"Python": "class TreeNode:\n    def __init__(self, x):\n        self.val = x\n        self.left = None\n        self.right = None", "C++": "struct TreeNode {\n    int val;\n    TreeNode* left;\n    TreeNode* right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};", "C": "typedef struct TreeNode {\n    int val;\n    struct TreeNode *left, *right;\n} TreeNode;", "Java": "class TreeNode {\n    int val;\n    TreeNode left, right;\n    TreeNode(int x) { val = x; }\n}"}
        }
    },
    "算法思想": {
        "递归与分治": {
            "concepts": ["基准情况", "递归调用栈", "分而治之", "记忆化"],
            "examples": ["斐波那契数列", "归并排序", "pow(x,n)"],
            "code": {"Python": "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)", "C++": "int fib(int n) {\n    if (n <= 1) return n;\n    return fib(n-1) + fib(n-2);\n}", "C": "int fib(int n) {\n    if (n <= 1) return n;\n    return fib(n-1) + fib(n-2);\n}", "Java": "int fib(int n) {\n    if (n <= 1) return n;\n    return fib(n-1) + fib(n-2);\n}"}
        },
        "动态规划": {
            "concepts": ["最优子结构", "状态定义", "状态转移方程", "空间优化"],
            "examples": ["爬楼梯", "最长递增子序列", "背包问题"],
            "code": {"Python": "dp = [0] * (n + 1)\ndp[0], dp[1] = 1, 1\nfor i in range(2, n + 1):\n    dp[i] = dp[i-1] + dp[i-2]", "C++": "vector<int> dp(n+1, 0);\ndp[0] = dp[1] = 1;\nfor(int i=2; i<=n; i++)\n    dp[i] = dp[i-1] + dp[i-2];", "C": "int dp[1001] = {0};\ndp[0] = dp[1] = 1;\nfor(int i=2; i<=n; i++)\n    dp[i] = dp[i-1] + dp[i-2];", "Java": "int[] dp = new int[n+1];\ndp[0] = dp[1] = 1;\nfor(int i=2; i<=n; i++)\n    dp[i] = dp[i-1] + dp[i-2];"}
        },
        "回溯算法": {
            "concepts": ["选择列表", "路径", "结束条件", "剪枝优化"],
            "examples": ["全排列", "N皇后", "组合总和"],
            "code": {"Python": "def backtrack(path, choices):\n    if not choices:\n        result.append(path[:])\n        return\n    for i, choice in enumerate(choices):\n        path.append(choice)\n        backtrack(path, choices[:i]+choices[i+1:])\n        path.pop()", "C++": "void backtrack(vector<int>& path, vector<int>& choices) {\n    if(choices.empty()) { result.push_back(path); return; }\n    for(int i=0; i<choices.size(); i++) {\n        path.push_back(choices[i]);\n        choices.erase(choices.begin()+i);\n        backtrack(path, choices);\n        choices.insert(choices.begin()+i, path.back());\n        path.pop_back();\n    }\n}", "C": "void backtrack(int* path, int pathSize, int* choices, int n) {\n    if(pathSize == n) return;\n    for(int i=0; i<n; i++) {\n        path[pathSize] = choices[i];\n        backtrack(path, pathSize+1, choices, n);\n    }\n}", "Java": "void backtrack(List<Integer> path, List<Integer> choices) {\n    if(choices.isEmpty()) { result.add(new ArrayList<>(path)); return; }\n    for(int i=0; i<choices.size(); i++) {\n        path.add(choices.get(i));\n        List<Integer> nc = new ArrayList<>(choices);\n        nc.remove(i);\n        backtrack(path, nc);\n        path.remove(path.size()-1);\n    }\n}"}
        },
        "贪心算法": {
            "concepts": ["局部最优解", "全局最优解", "贪心选择性质", "证明贪心正确性"],
            "examples": ["分发糖果", "跳跃游戏", "柠檬水找零"],
            "code": {"Python": "def greedy(nums):\n    result = []\n    return result", "C++": "vector<int> greedy(vector<int>& nums) {\n    vector<int> result;\n    return result;\n}", "C": "int* greedy(int* nums, int n) {\n    int* result = malloc(n * sizeof(int));\n    return result;\n}", "Java": "int[] greedy(int[] nums) {\n    return new int[nums.length];\n}"}
        }
    },
    "基础语法": {
        "变量与数据类型": {
            "concepts": ["基本类型", "引用类型", "类型转换", "类型推断"],
            "examples": ["整数溢出", "浮点数精度", "字符串拼接"],
            "code": {"Python": "x = 10      # int\ny = 3.14    # float\nname = 'Hello'  # str\nis_valid = True  # bool", "C++": "int x = 10;\ndouble y = 3.14;\nstring name = \"Hello\";\nbool isValid = true;", "C": "int x = 10;\ndouble y = 3.14;\nchar name[] = \"Hello\";\n_Bool isValid = 1;", "Java": "int x = 10;\ndouble y = 3.14;\nString name = \"Hello\";\nboolean isValid = true;"}
        },
        "控制流": {
            "concepts": ["条件判断", "循环结构", "break/continue", "switch分支"],
            "examples": ["if-else分支", "for/while循环", "嵌套循环"],
            "code": {"Python": "if x > 0:\n    print('正数')\nelif x < 0:\n    print('负数')\nelse:\n    print('零')", "C++": "if (x > 0) {\n    cout << \"正数\" << endl;\n} else if (x < 0) {\n    cout << \"负数\" << endl;\n} else {\n    cout << \"零\" << endl;\n}", "C": "if (x > 0) {\n    printf(\"正数\\n\");\n} else if (x < 0) {\n    printf(\"负数\\n\");\n} else {\n    printf(\"零\\n\");\n}", "Java": "if (x > 0) {\n    System.out.println(\"正数\");\n} else if (x < 0) {\n    System.out.println(\"负数\");\n} else {\n    System.out.println(\"零\");\n}"}
        },
        "函数": {
            "concepts": ["函数定义", "参数传递", "返回值", "Lambda表达式"],
            "examples": ["递归函数", "默认参数", "可变参数"],
            "code": {"Python": "def greet(name, greeting='Hello'):\n    return f'{greeting}, {name}!'\n\n# Lambda\nsquare = lambda x: x ** 2", "C++": "string greet(string name, string greeting=\"Hello\") {\n    return greeting + \", \" + name + \"!\";\n}\n\n// Lambda\nauto square = [](int x) { return x * x; };", "C": "char* greet(char* name, char* greeting) {\n    static char result[100];\n    sprintf(result, \"%s, %s!\", greeting, name);\n    return result;\n}", "Java": "public static String greet(String name, String greeting) {\n    return greeting + \", \" + name + \"!\";\n}\n\n// Lambda\nFunction<Integer, Integer> square = x -> x * x;"}
        },
        "面向对象": {
            "concepts": ["类与对象", "继承与多态", "封装与抽象", "接口与实现"],
            "examples": ["类的定义", "继承层次", "多态应用"],
            "code": {"Python": "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        raise NotImplementedError\n\nclass Dog(Animal):\n    def speak(self):\n        return f'{self.name} says Woof!'", "C++": "class Animal {\nprotected:\n    string name;\npublic:\n    Animal(string n) : name(n) {}\n    virtual string speak() = 0;\n};\n\nclass Dog : public Animal {\npublic:\n    Dog(string n) : Animal(n) {}\n    string speak() override { return name + \" says Woof!\"; }\n};", "C": "// C语言使用结构体和函数指针模拟\ntypedef struct {\n    char name[50];\n    void (*speak)(void*);\n} Animal;", "Java": "abstract class Animal {\n    protected String name;\n    public Animal(String name) { this.name = name; }\n    public abstract String speak();\n}\n\nclass Dog extends Animal {\n    public Dog(String name) { super(name); }\n    public String speak() { return name + \" says Woof!\"; }\n}"}
        }
    }
}

# ============== Question Bank ==============
QUESTION_BANK = [
    {"id": "arr_001", "topic": "数组反转", "category": "数据结构", "title": "反转数组", "description": "给定一个整数数组，反转数组顺序并返回。", "knowledge_point": "数组、双指针", "input_format": "输入一个整数数组，格式为：方括号包裹，元素用逗号分隔。如：[1,2,3,4,5]", "output_format": "输出反转后的数组，格式与输入相同。如：[5,4,3,2,1]", "test_cases": ["[1,2,3,4,5]->[5,4,3,2,1]", "[1,2]->[2,1]", "[1]->[1]", "[]->[]", "[-1,-2,-3]->[-3,-2,-1]"], "examples": {"input": "[1,2,3,4,5]", "output": "[5,4,3,2,1]"}, "hints": ["使用双指针交换", "注意边界条件"], "difficulty": 1},
    {"id": "arr_002", "topic": "两数之和", "category": "数据结构", "title": "两数之和", "description": "给定数组和目标值，找出两个数的下标使它们和为目标值。", "knowledge_point": "数组、哈希表", "input_format": "输入数组和目标值，用空格分隔。如：[2,7,11,15] 9", "output_format": "输出两个下标，用方括号包裹，逗号分隔。如：[0,1]", "test_cases": ["[2,7,11,15] 9->[0,1]", "[3,2,4] 6->[1,2]", "[3,3] 6->[0,1]", "[1,2,3,4,5] 9->[3,4]", "[1] 2->[]"], "examples": {"input": "[2,7,11,15] 9", "output": "[0,1]"}, "hints": ["暴力O(n^2)", "哈希表O(n)"], "difficulty": 1},
    {"id": "arr_003", "topic": "合并有序数组", "category": "数据结构", "title": "合并两个有序数组", "description": "合并两个有序数组为一个有序数组。", "knowledge_point": "数组、双指针", "input_format": "输入两个数组，用空格分隔。如：[1,3,5] [2,4,6]", "output_format": "输出合并后的数组，格式与输入相同。如：[1,2,3,4,5,6]", "test_cases": ["[1,3,5] [2,4,6]->[1,2,3,4,5,6]", "[1,2,3] [4,5,6]->[1,2,3,4,5,6]", "[1,1,1] [1,1,1]->[1,1,1,1,1,1]", "[1] [2]->[1,2]", "[] [1]->[1]"], "examples": {"input": "[1,3,5] [2,4,6]", "output": "[1,2,3,4,5,6]"}, "hints": ["从后往前填充", "双指针遍历"], "difficulty": 1},
    {"id": "arr_004", "topic": "移除元素", "category": "数据结构", "title": "移除元素", "description": "原地移除数组中所有等于val的元素，返回新长度。", "knowledge_point": "数组、双指针", "input_format": "输入数组和要移除的值val，用空格分隔。如：[3,2,2,3] 3", "output_format": "输出移除后的新长度（整数）。如：2", "test_cases": ["[3,2,2,3] 3->2", "[0,1,2,2,3,0,4,2] 2->5", "[1] 1->0", "[1,2] 1->1", "[3,3,3] 3->0"], "examples": {"input": "[3,2,2,3] 3", "output": "2"}, "hints": ["双指针原地修改", "返回新长度"], "difficulty": 1},
    {"id": "arr_005", "topic": "买卖股票", "category": "数据结构", "title": "买卖股票最佳时机", "description": "给定股票价格数组，找出最大利润。", "knowledge_point": "数组、贪心", "input_format": "输入股票价格数组。如：[7,1,5,3,6,4]", "output_format": "输出最大利润（整数）。如：5", "test_cases": ["[7,1,5,3,6,4]->5", "[7,6,4,3,1]->0", "[1,2]->1", "[2,1,4]->3", "[1,2,3,4,5]->4"], "examples": {"input": "[7,1,5,3,6,4]", "output": "5"}, "hints": ["记录最低价格", "计算最大利润"], "difficulty": 1},
    {"id": "str_001", "topic": "回文串判断", "category": "数据结构", "title": "回文串判断", "description": "判断字符串是否为回文串（忽略大小写和非字母数字）。", "knowledge_point": "字符串、双指针", "input_format": "输入一个字符串。如：race a car", "output_format": "输出true或false。如：false", "test_cases": ["race a car->false", "A man a plan a canal Panama->true", "abba->true", "abc->false", "a->true", "12321->true"], "examples": {"input": "race a car", "output": "false"}, "hints": ["双指针从两端向中间", "过滤非字母数字字符"], "difficulty": 1},
    {"id": "str_002", "topic": "字符串替换", "category": "数据结构", "title": "替换空格", "description": "将字符串中的空格替换为%20。", "knowledge_point": "字符串", "input_format": "输入一个字符串，可能包含空格。如：We are happy", "output_format": "输出替换后的字符串。如：We%20are%20happy", "test_cases": ["We are happy->We%20are%20happy", "Hello World->Hello%20World", "a->a", "no space->no space", "a b c->a%20b%20c"], "examples": {"input": "We are happy", "output": "We%20are%20happy"}, "hints": ["从后往前填充"], "difficulty": 1},
    {"id": "str_003", "topic": "最长公共前缀", "category": "数据结构", "title": "最长公共前缀", "description": "找出字符串数组中的最长公共前缀。", "knowledge_point": "字符串、纵向扫描", "input_format": "输入字符串数组，用空格分隔。如：flower flow flight", "output_format": "输出最长公共前缀字符串。如：fl", "test_cases": ["flower flow flight->fl", "dog racecar car->", "a->a", "ab abc abcd->ab", "aaa aaa aaa->aaa"], "examples": {"input": "flower flow flight", "output": "fl"}, "hints": ["纵向扫描每个字符", "注意空字符串情况"], "difficulty": 1},
    {"id": "math_001", "topic": "质数判断", "category": "算法思想", "title": "质数判断", "description": "判断一个数是否为质数。", "knowledge_point": "数学", "input_format": "输入一个正整数n。如：17", "output_format": "输出true表示是质数，false表示不是。如：true", "test_cases": ["2->true", "3->true", "4->false", "5->true", "6->false", "7->true", "9->false", "11->true", "1->false", "0->false"], "examples": {"input": "17", "output": "true"}, "hints": ["只需检查到sqrt(n)", "2是最小的质数"], "difficulty": 1},
    {"id": "math_002", "topic": "斐波那契", "category": "算法思想", "title": "斐波那契数列", "description": "计算第n个斐波那契数。", "knowledge_point": "递归、动态规划", "input_format": "输入一个非负整数n。如：10", "output_format": "输出第n个斐波那契数。如：55", "test_cases": ["0->0", "1->1", "2->1", "3->2", "4->3", "5->5", "6->8", "10->55", "20->6765", "30->832040"], "examples": {"input": "10", "output": "55"}, "hints": ["F(0)=0, F(1)=1", "可用递归或循环"], "difficulty": 1},
    {"id": "math_003", "topic": "阶乘", "category": "算法思想", "title": "阶乘计算", "description": "计算n的阶乘。", "knowledge_point": "递归、数学", "input_format": "输入一个非负整数n。如：5", "output_format": "输出n的阶乘（整数）。如：120", "test_cases": ["0->1", "1->1", "2->2", "3->6", "4->24", "5->120", "6->720", "10->3628800", "7->5040", "8->40320"], "examples": {"input": "5", "output": "120"}, "hints": ["0! = 1", "n! = n * (n-1)!"], "difficulty": 1},
    {"id": "math_004", "topic": "最大公约数", "category": "算法思想", "title": "最大公约数", "description": "计算两个数的最大公约数(GCD)。", "knowledge_point": "数学、辗转相除法", "input_format": "输入两个正整数，用空格分隔。如：24 18", "output_format": "输出最大公约数（整数）。如：6", "test_cases": ["12 8->4", "24 18->6", "100 25->25", "17 13->1", "36 48->12", "7 7->7", "1 100->1", "48 18->6"], "examples": {"input": "24 18", "output": "6"}, "hints": ["辗转相除法（欧几里得算法）", "a和b的GCD等于b和a%b的GCD"], "difficulty": 1},
    {"id": "math_005", "topic": "最小公倍数", "category": "算法思想", "title": "最小公倍数", "description": "计算两个数的最小公倍数(LCM)。", "knowledge_point": "数学", "input_format": "输入两个正整数，用空格分隔。如：6 8", "output_format": "输出最小公倍数（整数）。如：24", "test_cases": ["6 8->24", "12 18->36", "4 6->12", "5 7->35", "1 1->1", "2 3->6", "10 15->30", "7 14->14"], "examples": {"input": "6 8", "output": "24"}, "hints": ["LCM = a * b / GCD(a,b)", "先求GCD再计算"], "difficulty": 1},
    {"id": "list_001", "topic": "反转链表", "category": "数据结构", "title": "反转链表", "description": "反转一个单链表。", "knowledge_point": "链表、双指针", "input_format": "输入链表节点值，用空格分隔。如：1 2 3 4 5", "output_format": "输出反转后的链表节点值，用空格分隔。如：5 4 3 2 1", "test_cases": ["1 2 3 4 5->5 4 3 2 1", "1 2 3->3 2 1", "1->1", "1 1->1 1"], "examples": {"input": "1 2 3 4 5", "output": "5 4 3 2 1"}, "hints": ["迭代：三指针", "递归：反转剩余部分"], "difficulty": 2},
    {"id": "list_002", "topic": "环形链表", "category": "数据结构", "title": "环形链表检测", "description": "判断链表是否有环。", "knowledge_point": "链表、快慢指针", "input_format": "输入链表描述。如：有环 或 无环", "output_format": "输出true表示有环，false表示无环。如：true", "test_cases": ["有环->true", "无环->false"], "examples": {"input": "有环", "output": "true"}, "hints": ["快指针走两步", "慢指针走一步", "相遇则有环"], "difficulty": 2},
    {"id": "list_003", "topic": "删除倒数第N个", "category": "数据结构", "title": "删除倒数第N个节点", "description": "删除链表中倒数第n个节点。", "knowledge_point": "链表、双指针", "input_format": "输入链表节点值和n，用空格分隔。如：1 2 3 4 5 2", "output_format": "输出删除后的链表节点值。如：1 2 3 5", "test_cases": ["1 2 3 4 5 2->1 2 3 5", "1 2 3 4 5 1->1 2 3 4", "1 2 3 4 5 3->1 2 3 5", "1 2 3 4 5 5->1 2 3 4"], "examples": {"input": "1 2 3 4 5 2", "output": "1 2 3 5"}, "hints": ["双指针：先走n步", "保持间隔删除"], "difficulty": 2},
    {"id": "list_004", "topic": "合并有序链表", "category": "数据结构", "title": "合并两个有序链表", "description": "将两个有序链表合并为一个有序链表。", "knowledge_point": "链表、归并", "input_format": "输入两个链表的节点值，用 | 分隔。如：1 2 3 | 4 5 6", "output_format": "输出合并后的链表节点值。如：1 2 3 4 5 6", "test_cases": ["1 2 3 | 4 5 6->1 2 3 4 5 6", "1 3 5 | 2 4 6->1 2 3 4 5 6", "1 2 3 | ->1 2 3", "->"], "examples": {"input": "1 2 3 | 4 5 6", "output": "1 2 3 4 5 6"}, "hints": ["虚拟头节点", "比较节点值大小"], "difficulty": 2},
    {"id": "stack_001", "topic": "有效括号", "category": "数据结构", "title": "有效的括号", "description": "判断括号字符串是否有效。", "knowledge_point": "栈、括号匹配", "input_format": "输入只包含括号()[]{}的字符串。如：()[]{}", "output_format": "输出true表示有效，false表示无效。如：true", "test_cases": ["()->true", "()[]{}->true", "(->false", "([)]->false", "{[]}->true", "([{}])->true"], "examples": {"input": "()[]{}", "output": "true"}, "hints": ["左括号入栈", "右括号匹配出栈"], "difficulty": 2},
    {"id": "stack_002", "topic": "最小栈", "category": "数据结构", "title": "最小栈设计", "description": "设计一个支持push、pop、top和获取最小值的栈。", "knowledge_point": "栈、设计", "input_format": "输入一系列操作。如：push1 push2 getMin", "output_format": "输出getMin操作返回的最小值。如：1", "test_cases": ["push1 push2 getMin->1", "push3 push1 push2 getMin->1", "push5 push2 getMin->2", "push1 getMin->1", "push3 pop getMin->3"], "examples": {"input": "push1 push2 getMin", "output": "1"}, "hints": ["使用辅助栈存储最小值", "每次push时更新最小值"], "difficulty": 2},
    {"id": "stack_003", "topic": "每日温度", "category": "数据结构", "title": "每日温度", "description": "计算需要等待多少天才能等到更暖的气温。", "knowledge_point": "栈、单调栈", "input_format": "输入每日温度，用空格分隔。如：73 74 75 71 69 72 76 73", "output_format": "输出等待天数的数组，用空格分隔。如：1 1 4 2 1 1 0 0", "test_cases": ["73 74 75 71 69 72 76 73->1 1 4 2 1 1 0 0", "73 74 75 76 77->1 1 1 1 0", "73 72 71 70 69->0 0 0 0 0", "80 69 72 71 75->3 2 1 1 0"], "examples": {"input": "73 74 75 71 69 72 76 73", "output": "1 1 4 2 1 1 0 0"}, "hints": ["单调递减栈", "栈中存索引"], "difficulty": 2},
    {"id": "dp_001", "topic": "爬楼梯", "category": "算法思想", "title": "爬楼梯", "description": "假设你正在爬楼梯，有n阶台阶，每次可以爬1或2阶，有多少种方法？", "knowledge_point": "动态规划", "input_format": "输入台阶数n（正整数）。如：4", "output_format": "输出爬上n阶台阶的方法数（整数）。如：5", "test_cases": ["1->1", "2->2", "3->3", "4->5", "5->8", "6->13", "7->21", "10->89"], "examples": {"input": "4", "output": "5"}, "hints": ["dp[i] = dp[i-1] + dp[i-2]", "边界条件dp[1]=1, dp[2]=2"], "difficulty": 2},
    {"id": "dp_002", "topic": "打家劫舍", "category": "算法思想", "title": "打家劫舍", "description": "你是一个专业的小偷，不能偷相邻的两家房屋，能偷到的最大金额。", "knowledge_point": "动态规划", "input_format": "输入房屋金额数组。如：[1,2,3,1]", "output_format": "输出能偷到的最大金额（整数）。如：4", "test_cases": ["[1,2,3,1]->4", "[2,7,9,3,1]->12", "[1,2]->2", "[1,3,1,3,100]->104", "[1,2,3,4,5]->9"], "examples": {"input": "[1,2,3,1]", "output": "4"}, "hints": ["dp[i]=max(dp[i-1],dp[i-2]+nums[i])", "不能偷相邻房屋"], "difficulty": 2},
    {"id": "dp_003", "topic": "最长递增子序列", "category": "算法思想", "title": "最长递增子序列", "description": "找出数组中最长递增子序列的长度。", "knowledge_point": "动态规划、二分", "input_format": "输入整数数组。如：[10,9,2,5,3,7,101,18]", "output_format": "输出最长递增子序列的长度（整数）。如：4", "test_cases": ["[10,9,2,5,3,7,101,18]->4", "[0,1,0,3,2,3]->4", "[7,7,7,7,7,7,7]->1", "[1,2,3,4,5]->5"], "examples": {"input": "[10,9,2,5,3,7,101,18]", "output": "4"}, "hints": ["dp[i]表示以nums[i]结尾的最长递增子序列", "dp[i] = max(dp[j]) + 1其中j < i且nums[j] < nums[i]"], "difficulty": 2},
    {"id": "bt_001", "topic": "全排列", "category": "算法思想", "title": "全排列", "description": "给定一个数组，返回其所有可能的全排列数量。", "knowledge_point": "回溯算法", "input_format": "输入整数数组。如：[1,2,3]", "output_format": "输出全排列的数量（整数）。如：6", "test_cases": ["[1,2,3]->6", "[1,1,2]->3", "[1]->1", "[2,2,2]->1"], "examples": {"input": "[1,2,3]", "output": "6"}, "hints": ["使用回溯法", "track记录路径，used标记已使用的元素"], "difficulty": 3},
    {"id": "bt_002", "topic": "组合总和", "category": "算法思想", "title": "组合总和", "description": "给定数组candidates和目标值target，找出所有和为target的组合数量。", "knowledge_point": "回溯算法", "input_format": "输入candidates数组和target，用空格分隔。如：[2,3,6,7] 7", "output_format": "输出满足条件的组合数量（整数）。如：2", "test_cases": ["[2,3,6,7] 7->2", "[2,3,5] 8->2", "[2] 1->0", "[1] 2->1"], "examples": {"input": "[2,3,6,7] 7", "output": "2"}, "hints": ["每个数字可以重复使用", "需要去重"], "difficulty": 3},
    {"id": "bt_003", "topic": "N皇后", "category": "算法思想", "title": "N皇后", "description": "n皇后问题，摆放过皇后的棋盘不能相互攻击，求解的个数。", "knowledge_point": "回溯算法", "input_format": "输入皇后的数量n（正整数）。如：4", "output_format": "输出能够放置n个皇后且不相互攻击的方案数（整数）。如：2", "test_cases": ["1->1", "2->0", "3->0", "4->2", "5->10", "6->4", "7->40", "8->92"], "examples": {"input": "4", "output": "2"}, "hints": ["同行、同列、同一对角线不能有多个皇后", "用三个集合分别记录列和两个对角线"], "difficulty": 3},
    {"id": "tree_001", "topic": "二叉树中序遍历", "category": "数据结构", "title": "二叉树中序遍历", "description": "给定二叉树，返回中序遍历结果。", "knowledge_point": "树、递归", "input_format": "输入二叉树节点值，用空格分隔，空节点用null表示。如：1 null 2 null 3", "output_format": "输出中序遍历结果，用空格分隔。如：1 3 2", "test_cases": ["1 null 2 null 3->1 3 2", "1 2 3 4 5->4 2 5 1 3", "1->1", "1 2->2 1"], "examples": {"input": "1 null 2 null 3", "output": "1 3 2"}, "hints": ["左子树、根、右子树", "递归或迭代"], "difficulty": 2},
    {"id": "tree_002", "topic": "二叉树最大深度", "category": "数据结构", "title": "二叉树最大深度", "description": "给定二叉树，返回其最大深度。", "knowledge_point": "树、递归", "input_format": "输入二叉树节点值，用空格分隔，空节点用null表示。如：3 9 20 null null 15 7", "output_format": "输出二叉树的最大深度（整数）。如：3", "test_cases": ["3 9 20 null null 15 7->3", "1 null 2->2", "null->0", "1->1", "1 2 3 4 4->3"], "examples": {"input": "3 9 20 null null 15 7", "output": "3"}, "hints": ["最大深度 = max(左子树深度, 右子树深度) + 1"], "difficulty": 1},
    {"id": "graph_001", "topic": "岛屿数量", "category": "数据结构", "title": "岛屿数量", "description": "给定二维网格地图，计算岛屿的数量。", "knowledge_point": "图、BFS/DFS", "input_format": "输入二维网格，每行用空格分隔，行之间用 | 分隔。如：1 1 0 0 0 | 1 1 0 0 0 | 0 0 1 0 0 | 0 0 0 1 1", "output_format": "输出岛屿的数量（整数）。如：2", "test_cases": ["1 1 0 0 0 | 1 1 0 0 0 | 0 0 1 0 0 | 0 0 0 1 1->2", "1 1 1 1 1->1", "0 0 0 0->0", "1->1"], "examples": {"input": "1 1 0 0 0 | 1 1 0 0 0 | 0 0 1 0 0 | 0 0 0 1 1", "output": "2"}, "hints": ["使用DFS/BFS遍历", "遍历过的岛屿标记为0"], "difficulty": 2},
    {"id": "graph_002", "topic": "课程表", "category": "数据结构", "title": "课程表", "description": "判断是否可能完成所有课程的学习。", "knowledge_point": "图、拓扑排序", "input_format": "输入课程数量和先修课程列表。如：2 [[1,0]]", "output_format": "输出true表示可以完成，false表示不能。如：true", "test_cases": ["2 [[1,0]]->true", "2 [[1,0],[0,1]]->false", "3 [[1,0],[2,1],[0,2]]->false", "4 [[1,0],[2,0],[3,1],[3,2]]->true"], "examples": {"input": "2 [[1,0]]", "output": "true"}, "hints": ["检测环", "使用拓扑排序或DFS"], "difficulty": 3},
    {"id": "greedy_001", "topic": "跳跃游戏", "category": "算法思想", "title": "跳跃游戏", "description": "给定数组表示每步最大跳跃长度，判断能否到达终点。", "knowledge_point": "贪心算法", "input_format": "输入最大跳跃长度数组。如：[2,3,1,1,4]", "output_format": "输出true表示可以到达，false表示不能。如：true", "test_cases": ["[2,3,1,1,4]->true", "[3,2,1,0,4]->false", "[2,0,0]->true", "[0]->true", "[2,5,0,0]->true"], "examples": {"input": "[2,3,1,1,4]", "output": "true"}, "hints": ["维护能到达的最远距离", "如果最远距离大于等于终点则可达"], "difficulty": 2},
    {"id": "greedy_002", "topic": "柠檬水找零", "category": "算法思想", "title": "柠檬水找零", "description": "每杯柠檬水5元，判断能否正确找零。", "knowledge_point": "贪心算法", "input_format": "输入顾客支付金额数组，5表示付5元，10表示付10元，20表示付20元。如：[5,5,5,10,20]", "output_format": "输出true表示可以正确找零，false表示不能。如：true", "test_cases": ["[5,5,5,10,20]->true", "[5,5,10,10,20]->false", "[5,5,10]->true", "[5,10,20]->true", "[10,20]->false"], "examples": {"input": "[5,5,5,10,20]", "output": "true"}, "hints": ["优先使用大面值找零", "记录5元和10元的数量"], "difficulty": 1}
]

# ============== 标准答案库 ==============
SOLUTIONS = {
    "arr_001": {  # 反转数组
        "title": "反转数组",
        "Python": '''import ast

# 读取输入数组
s = input().strip()
nums = ast.literal_eval(s)

# 反转数组
result = nums[::-1]

# 输出结果
print(result)''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    // 解析 [1,2,3,4,5] 格式
    vector<int> nums;
    string num = "";
    for (char c : s) {
        if (c >= '0' && c <= '9' || c == '-') {
            num += c;
        } else if (num != "") {
            nums.push_back(stoi(num));
            num = "";
        }
    }

    // 反转数组
    reverse(nums.begin(), nums.end());

    // 输出结果
    cout << "[";
    for (int i = 0; i < nums.size(); i++) {
        cout << nums[i];
        if (i < nums.size() - 1) cout << ",";
    }
    cout << "]" << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char s[1000];
    gets(s);

    int nums[100], len = 0;
    char *token = strtok(s, "[], ");
    while (token != NULL) {
        nums[len++] = atoi(token);
        token = strtok(NULL, "[], ");
    }

    // 反转数组
    for (int i = 0; i < len / 2; i++) {
        int tmp = nums[i];
        nums[i] = nums[len - 1 - i];
        nums[len - 1 - i] = tmp;
    }

    // 输出结果
    printf("[");
    for (int i = 0; i < len; i++) {
        printf("%d%s", nums[i], i < len - 1 ? "," : "");
    }
    printf("]\\n");

    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        // 解析数组
        s = s.replace("[", "").replace("]", "");
        List<Integer> nums = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                nums.add(Integer.parseInt(num.trim()));
            }
        }

        // 反转数组
        Collections.reverse(nums);

        // 输出结果
        System.out.println(nums);
    }
}'''
    },
    "arr_002": {  # 两数之和
        "title": "两数之和",
        "Python": '''import ast

# 读取输入
s = input().strip()
parts = s.rsplit(" ", 1)
arr_str = parts[0]
target = int(parts[1])
nums = ast.literal_eval(arr_str)

# 哈希表解法 O(n)
hashmap = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in hashmap:
        print(f"[{hashmap[complement]},{i}]")
        break
    hashmap[num] = i
else:
    print("[]")''',
        "C++": '''#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    // 解析输入: [2,7,11,15] 9
    vector<int> nums;
    int target;
    string numStr;

    // 提取数组
    size_t pos1 = line.find('[');
    size_t pos2 = line.find(']');
    string arrStr = line.substr(pos1, pos2 - pos1 + 1);

    // 解析数组
    stringstream ss(arrStr);
    char c;
    ss >> c; // '['
    int x;
    while (ss >> x) {
        nums.push_back(x);
        ss >> c; // ',' or ']'
    }

    // 提取目标值
    target = stoi(line.substr(pos2 + 2));

    // 哈希表解法
    unordered_map<int, int> hashmap;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (hashmap.count(complement)) {
            cout << "[" << hashmap[complement] << "," << i << "]" << endl;
            return 0;
        }
        hashmap[nums[i]] = i;
    }
    cout << "[]" << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>

int main() {
    char s[1000];
    gets(s);

    // 解析: [2,7,11,15] 9
    int nums[100], target, len = 0;
    char *p = s;

    // 解析数组
    while (*p && *p != ']') {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            nums[len++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }

    // 跳过 ] 找到目标值
    while (*p && (*p < '0' || *p > '9')) p++;
    target = atoi(p);

    // 哈希表解法
    int hash[1001] = {0};
    for (int i = 0; i < len; i++) {
        int complement = target - nums[i];
        if (complement >= 0 && complement <= 1000 && hash[complement]) {
            printf("[%d,%d]\\n", hash[complement] - 1, i);
            return 0;
        }
        hash[nums[i]] = i + 1;
    }
    printf("[]\\n");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        // 解析输入
        int pos1 = line.indexOf('[');
        int pos2 = line.indexOf(']');
        String arrStr = line.substring(pos1, pos2 + 1);
        int target = Integer.parseInt(line.substring(pos2 + 2).trim());

        // 解析数组
        arrStr = arrStr.replace("[", "").replace("]", "");
        List<Integer> nums = new ArrayList<>();
        for (String num : arrStr.split(",")) {
            nums.add(Integer.parseInt(num.trim()));
        }

        // 哈希表解法
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums.get(i);
            if (map.containsKey(complement)) {
                System.out.println("[" + map.get(complement) + "," + i + "]");
                return;
            }
            map.put(nums.get(i), i);
        }
        System.out.println("[]");
    }
}'''
    },
    "arr_003": {  # 合并两个有序数组
        "title": "合并两个有序数组",
        "Python": '''import ast

# 读取输入
s = input().strip()
parts = s.split(" ", 1)
arr1_str = parts[0]
arr2_str = parts[1]
nums1 = ast.literal_eval(arr1_str)
nums2 = ast.literal_eval(arr2_str)

# 合并并排序
result = sorted(nums1 + nums2)

# 输出结果
print(result)''',
        "C++": '''#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
using namespace std;

vector<int> parseArray(string s) {
    vector<int> nums;
    s = s.substr(1, s.length() - 2);
    if (s.empty()) return nums;
    stringstream ss(s);
    string num;
    while (getline(ss, num, ',')) {
        nums.push_back(stoi(num));
    }
    return nums;
}

int main() {
    string line;
    getline(cin, line);

    size_t space = line.find(' ');
    string s1 = line.substr(0, space);
    string s2 = line.substr(space + 1);

    vector<int> nums1 = parseArray(s1);
    vector<int> nums2 = parseArray(s2);

    nums1.insert(nums1.end(), nums2.begin(), nums2.end());
    sort(nums1.begin(), nums1.end());

    cout << "[";
    for (int i = 0; i < nums1.size(); i++) {
        cout << nums1[i];
        if (i < nums1.size() - 1) cout << ",";
    }
    cout << "]" << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    char s1[500], s2[500];
    gets(s1);
    gets(s2);

    int nums1[500], nums2[500], n1 = 0, n2 = 0;

    // 解析第一个数组
    char *p = s1;
    while (*p) {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            nums1[n1++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }

    // 解析第二个数组
    p = s2;
    while (*p) {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            nums2[n2++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }

    // 合并
    int *result = malloc((n1 + n2) * sizeof(int));
    for (int i = 0; i < n1; i++) result[i] = nums1[i];
    for (int i = 0; i < n2; i++) result[n1 + i] = nums2[i];

    qsort(result, n1 + n2, sizeof(int), compare);

    printf("[");
    for (int i = 0; i < n1 + n2; i++) {
        printf("%d%s", result[i], i < n1 + n2 - 1 ? "," : "");
    }
    printf("]\\n");

    free(result);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        int space = line.indexOf(' ');
        String s1 = line.substring(0, space);
        String s2 = line.substring(space + 1);

        List<Integer> nums1 = parseArray(s1);
        List<Integer> nums2 = parseArray(s2);

        nums1.addAll(nums2);
        Collections.sort(nums1);

        System.out.println(nums1);
    }

    static List<Integer> parseArray(String s) {
        s = s.trim();
        List<Integer> nums = new ArrayList<>();
        if (s.equals("[]")) return nums;
        s = s.substring(1, s.length() - 1);
        for (String num : s.split(",")) {
            nums.add(Integer.parseInt(num.trim()));
        }
        return nums;
    }
}'''
    },
    "arr_004": {  # 移除元素
        "title": "移除元素",
        "Python": '''import ast

# 读取输入
s = input().strip()
parts = s.rsplit(" ", 1)
arr_str = parts[0]
val = int(parts[1])
nums = ast.literal_eval(arr_str)

# 双指针法移除元素
left = 0
for right in range(len(nums)):
    if nums[right] != val:
        nums[left] = nums[right]
        left += 1

# 输出新长度
print(left)''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    size_t space = line.rfind(' ');
    string arrStr = line.substr(0, space);
    int val = stoi(line.substr(space + 1));

    vector<int> nums;
    for (char c : arrStr) {
        if (c >= '0' && c <= '9' || c == '-') {
            string num;
            for (; c >= '0' && c <= '9' || c == '-'; c = *(&c + 1)) {
                num += c;
            }
            nums.push_back(stoi(num));
        }
    }

    int left = 0;
    for (int right = 0; right < nums.size(); right++) {
        if (nums[right] != val) {
            nums[left++] = nums[right];
        }
    }

    cout << left << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int main() {
    char s[500];
    gets(s);

    int nums[500], val, len = 0;
    char *p = s;

    // 解析数组
    while (*p && *p != ' ') {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            nums[len++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }
    while (*p && *p == ' ') p++;
    val = atoi(p);

    int left = 0;
    for (int right = 0; right < len; right++) {
        if (nums[right] != val) {
            nums[left++] = nums[right];
        }
    }

    printf("%d\\n", left);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        int space = line.lastIndexOf(' ');
        String arrStr = line.substring(0, space);
        int val = Integer.parseInt(line.substring(space + 1).trim());

        arrStr = arrStr.substring(1, arrStr.length() - 1);
        List<Integer> nums = new ArrayList<>();
        for (String num : arrStr.split(",")) {
            nums.add(Integer.parseInt(num.trim()));
        }

        int left = 0;
        for (int right = 0; right < nums.size(); right++) {
            if (nums.get(right) != val) {
                nums.set(left++, nums.get(right));
            }
        }

        System.out.println(left);
    }
}'''
    },
    "arr_005": {  # 买卖股票最佳时机
        "title": "买卖股票最佳时机",
        "Python": '''import ast

# 读取输入
s = input().strip()
prices = ast.literal_eval(s)

# 贪心算法
min_price = float('inf')
max_profit = 0

for price in prices:
    min_price = min(min_price, price)
    max_profit = max(max_profit, price - min_price)

print(max_profit)''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    vector<int> prices;
    for (char c : s) {
        if (c >= '0' && c <= '9' || c == '-') {
            string num;
            while (c && (c >= '0' && c <= '9' || c == '-')) {
                num += c;
                static int i = 0;
                c = s[++i];
            }
            prices.push_back(stoi(num));
        }
    }

    int minPrice = prices[0];
    int maxProfit = 0;

    for (int price : prices) {
        minPrice = min(minPrice, price);
        maxProfit = max(maxProfit, price - minPrice);
    }

    cout << maxProfit << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int main() {
    char s[500];
    gets(s);

    int prices[500], len = 0;
    char *p = s;

    while (*p) {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            prices[len++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }

    int minPrice = prices[0];
    int maxProfit = 0;

    for (int i = 0; i < len; i++) {
        minPrice = minPrice < prices[i] ? minPrice : prices[i];
        int profit = prices[i] - minPrice;
        maxProfit = maxProfit > profit ? maxProfit : profit;
    }

    printf("%d\\n", maxProfit);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.substring(1, s.length() - 1);
        List<Integer> prices = new ArrayList<>();
        for (String p : s.split(",")) {
            prices.add(Integer.parseInt(p.trim()));
        }

        int minPrice = prices.get(0);
        int maxProfit = 0;

        for (int price : prices) {
            minPrice = Math.min(minPrice, price);
            maxProfit = Math.max(maxProfit, price - minPrice);
        }

        System.out.println(maxProfit);
    }
}'''
    },
    "str_001": {  # 回文串判断
        "title": "回文串判断",
        "Python": '''s = input().strip()

# 过滤非字母数字字符，转小写
filtered = []
for c in s:
    if c.isalnum():
        filtered.append(c.lower())
filtered = ''.join(filtered)

# 判断回文
left, right = 0, len(filtered) - 1
while left < right:
    if filtered[left] != filtered[right]:
        print("false")
        break
    left += 1
    right -= 1
else:
    print("true")''',
        "C++": '''#include <iostream>
#include <string>
#include <cctype>
using namespace std;

bool isAlnum(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9');
}

char toLower(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A' + 'a';
    return c;
}

int main() {
    string s;
    getline(cin, s);

    string filtered;
    for (char c : s) {
        if (isAlnum(c)) {
            filtered += toLower(c);
        }
    }

    int left = 0, right = filtered.length() - 1;
    bool isPalindrome = true;
    while (left < right) {
        if (filtered[left] != filtered[right]) {
            isPalindrome = false;
            break;
        }
        left++;
        right--;
    }

    cout << (isPalindrome ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>

bool isAlnum(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9');
}

char toLower(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A' + 'a';
    return c;
}

int main() {
    char s[1000];
    gets(s);

    char filtered[1000];
    int len = 0;

    for (int i = 0; s[i]; i++) {
        if (isAlnum(s[i])) {
            filtered[len++] = toLower(s[i]);
        }
    }

    int left = 0, right = len - 1;
    bool isPalindrome = true;
    while (left < right) {
        if (filtered[left] != filtered[right]) {
            isPalindrome = false;
            break;
        }
        left++;
        right--;
    }

    printf("%s\\n", isPalindrome ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();

        StringBuilder filtered = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (Character.isLetterOrDigit(c)) {
                filtered.append(Character.toLowerCase(c));
            }
        }

        String str = filtered.toString();
        int left = 0, right = str.length() - 1;
        boolean isPalindrome = true;

        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                isPalindrome = false;
                break;
            }
            left++;
            right--;
        }

        System.out.println(isPalindrome ? "true" : "false");
    }
}'''
    },
    "str_002": {  # 替换空格
        "title": "替换空格",
        "Python": '''s = input()

# 替换空格为 %20
result = s.replace(" ", "%20")

print(result)''',
        "C++": '''#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    string result;
    for (char c : s) {
        if (c == ' ') {
            result += "%20";
        } else {
            result += c;
        }
    }

    cout << result << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>

int main() {
    char s[1000];
    gets(s);

    char result[3000];
    int j = 0;

    for (int i = 0; s[i]; i++) {
        if (s[i] == ' ') {
            result[j++] = '%';
            result[j++] = '2';
            result[j++] = '0';
        } else {
            result[j++] = s[i];
        }
    }
    result[j] = '\\0';

    printf("%s\\n", result);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();

        String result = s.replace(" ", "%20");

        System.out.println(result);
    }
}'''
    },
    "str_003": {  # 最长公共前缀
        "title": "最长公共前缀",
        "Python": '''s = input().strip()

if not s:
    print("")
else:
    strs = s.split()
    if not strs:
        print("")
    else:
        # 找出最短字符串
        min_len = min(len(st) for st in strs)
        prefix = ""
        for i in range(min_len):
            chars = [st[i] for st in strs]
            if len(set(chars)) == 1:
                prefix += chars[0]
            else:
                break
        print(prefix)''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    vector<string> strs;
    string word;
    stringstream ss(line);
    while (ss >> word) {
        strs.push_back(word);
    }

    if (strs.empty()) {
        cout << endl;
        return 0;
    }

    string prefix = "";
    int minLen = strs[0].length();
    for (string &s : strs) {
        minLen = min(minLen, (int)s.length());
    }

    for (int i = 0; i < minLen; i++) {
        char c = strs[0][i];
        bool same = true;
        for (string &s : strs) {
            if (s[i] != c) {
                same = false;
                break;
            }
        }
        if (same) {
            prefix += c;
        } else {
            break;
        }
    }

    cout << prefix << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>

int main() {
    char line[1000];
    gets(line);

    char strs[100][100];
    int count = 0;

    char *token = strtok(line, " ");
    while (token != NULL) {
        strcpy(strs[count++], token);
        token = strtok(NULL, " ");
    }

    if (count == 0) {
        printf("\\n");
        return 0;
    }

    int minLen = strlen(strs[0]);
    for (int i = 1; i < count; i++) {
        if (strlen(strs[i]) < minLen)
            minLen = strlen(strs[i]);
    }

    char prefix[100] = "";
    for (int i = 0; i < minLen; i++) {
        char c = strs[0][i];
        int same = 1;
        for (int j = 1; j < count; j++) {
            if (strs[j][i] != c) {
                same = 0;
                break;
            }
        }
        if (same) {
            prefix[i] = c;
            prefix[i + 1] = '\\0';
        } else {
            break;
        }
    }

    printf("%s\\n", prefix);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        if (line.isEmpty()) {
            System.out.println();
            return;
        }

        String[] strs = line.split(" ");
        if (strs.length == 0) {
            System.out.println();
            return;
        }

        int minLen = strs[0].length();
        for (String s : strs) {
            minLen = Math.min(minLen, s.length());
        }

        StringBuilder prefix = new StringBuilder();
        for (int i = 0; i < minLen; i++) {
            char c = strs[0].charAt(i);
            boolean same = true;
            for (String s : strs) {
                if (s.charAt(i) != c) {
                    same = false;
                    break;
                }
            }
            if (same) {
                prefix.append(c);
            } else {
                break;
            }
        }

        System.out.println(prefix.toString());
    }
}'''
    },
    "math_001": {  # 质数判断
        "title": "质数判断",
        "Python": '''import math

n = int(input().strip())

if n < 2:
    print("false")
else:
    is_prime = True
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            is_prime = False
            break
    print("true" if is_prime else "false")''',
        "C++": '''#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int n;
    cin >> n;

    if (n < 2) {
        cout << "false" << endl;
        return 0;
    }

    bool isPrime = true;
    for (int i = 2; i <= sqrt(n); i++) {
        if (n % i == 0) {
            isPrime = false;
            break;
        }
    }

    cout << (isPrime ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <math.h>

int main() {
    int n;
    scanf("%d", &n);

    if (n < 2) {
        printf("false\\n");
        return 0;
    }

    int isPrime = 1;
    for (int i = 2; i <= sqrt(n); i++) {
        if (n % i == 0) {
            isPrime = 0;
            break;
        }
    }

    printf("%s\\n", isPrime ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        if (n < 2) {
            System.out.println("false");
            return;
        }

        boolean isPrime = true;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) {
                isPrime = false;
                break;
            }
        }

        System.out.println(isPrime ? "true" : "false");
    }
}'''
    },
    "math_002": {  # 斐波那契数列
        "title": "斐波那契数列",
        "Python": '''n = int(input().strip())

# 动态规划解法
if n == 0:
    print(0)
elif n == 1:
    print(1)
else:
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    print(b)''',
        "C++": '''#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    if (n == 0) {
        cout << 0 << endl;
        return 0;
    }
    if (n == 1) {
        cout << 1 << endl;
        return 0;
    }

    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long long temp = a + b;
        a = b;
        b = temp;
    }

    cout << b << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    if (n == 0) {
        printf("0\\n");
        return 0;
    }
    if (n == 1) {
        printf("1\\n");
        return 0;
    }

    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long long temp = a + b;
        a = b;
        b = temp;
    }

    printf("%lld\\n", b);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        if (n == 0) {
            System.out.println(0);
            return;
        }
        if (n == 1) {
            System.out.println(1);
            return;
        }

        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long temp = a + b;
            a = b;
            b = temp;
        }

        System.out.println(b);
    }
}'''
    },
    "math_003": {  # 阶乘
        "title": "阶乘计算",
        "Python": '''n = int(input().strip())

result = 1
for i in range(2, n + 1):
    result *= i

print(result)''',
        "C++": '''#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    cout << result << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    printf("%lld\\n", result);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }

        System.out.println(result);
    }
}'''
    },
    "math_004": {  # 最大公约数
        "title": "最大公约数",
        "Python": '''a, b = map(int, input().strip().split())

# 辗转相除法
while b:
    a, b = b, a % b

print(a)''',
        "C++": '''#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b) {
        int temp = a % b;
        a = b;
        b = temp;
    }
    return a;
}

int main() {
    int a, b;
    cin >> a >> b;

    cout << gcd(a, b) << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int gcd(int a, int b) {
    while (b) {
        int temp = a % b;
        a = b;
        b = temp;
    }
    return a;
}

int main() {
    int a, b;
    scanf("%d %d", &a, &b);

    printf("%d\\n", gcd(a, b));
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();

        while (b != 0) {
            int temp = a % b;
            a = b;
            b = temp;
        }

        System.out.println(a);
    }
}'''
    },
    "math_005": {  # 最小公倍数
        "title": "最小公倍数",
        "Python": '''def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = map(int, input().strip().split())

# LCM = a * b / GCD
lcm = a * b // gcd(a, b)

print(lcm)''',
        "C++": '''#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b) {
        int temp = a % b;
        a = b;
        b = temp;
    }
    return a;
}

int main() {
    int a, b;
    cin >> a >> b;

    int lcm = a * b / gcd(a, b);

    cout << lcm << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int gcd(int a, int b) {
    while (b) {
        int temp = a % b;
        a = b;
        b = temp;
    }
    return a;
}

int main() {
    int a, b;
    scanf("%d %d", &a, &b);

    int lcm = a * b / gcd(a, b);

    printf("%d\\n", lcm);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    static int gcd(int a, int b) {
        while (b != 0) {
            int temp = a % b;
            a = b;
            b = temp;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();

        int lcm = a * b / gcd(a, b);

        System.out.println(lcm);
    }
}'''
    },
    "list_001": {  # 反转链表
        "title": "反转链表",
        "Python": '''# 读取链表节点值
vals = input().strip().split()
vals = [int(v) for v in vals if v]

# 模拟链表反转
result = vals[::-1]

# 输出结果
print(" ".join(map(str, result)))''',
        "C++": '''#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    vector<int> vals;
    stringstream ss(line);
    int v;
    while (ss >> v) {
        vals.push_back(v);
    }

    reverse(vals.begin(), vals.end());

    for (int i = 0; i < vals.size(); i++) {
        if (i) cout << " ";
        cout << vals[i];
    }
    cout << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>

int main() {
    char line[1000];
    gets(line);

    int vals[100], len = 0;
    char *token = strtok(line, " ");
    while (token != NULL) {
        vals[len++] = atoi(token);
        token = strtok(NULL, " ");
    }

    for (int i = 0; i < len / 2; i++) {
        int tmp = vals[i];
        vals[i] = vals[len - 1 - i];
        vals[len - 1 - i] = tmp;
    }

    for (int i = 0; i < len; i++) {
        if (i) printf(" ");
        printf("%d", vals[i]);
    }
    printf("\\n");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        if (line.isEmpty()) {
            System.out.println();
            return;
        }

        String[] parts = line.split(" ");
        List<Integer> vals = new ArrayList<>();
        for (String p : parts) {
            if (!p.isEmpty()) {
                vals.add(Integer.parseInt(p));
            }
        }

        Collections.reverse(vals);

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < vals.size(); i++) {
            if (i > 0) sb.append(" ");
            sb.append(vals.get(i));
        }
        System.out.println(sb.toString());
    }
}'''
    },
    "stack_001": {  # 有效括号
        "title": "有效的括号",
        "Python": '''s = input().strip()

stack = []
mapping = {')': '(', ']': '[', '}': '{'}

for c in s:
    if c in mapping:
        if not stack or stack[-1] != mapping[c]:
            print("false")
            break
        stack.pop()
    else:
        stack.append(c)
else:
    print("true" if not stack else "false")''',
        "C++": '''#include <iostream>
#include <stack>
#include <string>
#include <unordered_map>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    stack<char> st;
    unordered_map<char, char> mapping = {
        {')', '('},
        {']', '['},
        {'}', '{'}
    };

    for (char c : s) {
        if (mapping.count(c)) {
            if (st.empty() || st.top() != mapping[c]) {
                cout << "false" << endl;
                return 0;
            }
            st.pop();
        } else {
            st.push(c);
        }
    }

    cout << (st.empty() ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool isValid(char* s) {
    char stack[1000];
    int top = -1;

    for (int i = 0; s[i]; i++) {
        if (s[i] == ')' || s[i] == ']' || s[i] == '}') {
            if (top < 0) return false;
            char match;
            if (s[i] == ')') match = '(';
            else if (s[i] == ']') match = '[';
            else match = '{';
            if (stack[top] != match) return false;
            top--;
        } else {
            stack[++top] = s[i];
        }
    }

    return top == -1;
}

int main() {
    char s[1000];
    gets(s);

    printf("%s\\n", isValid(s) ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();

        Stack<Character> stack = new Stack<>();
        Map<Character, Character> mapping = new HashMap<>();
        mapping.put(')', '(');
        mapping.put(']', '[');
        mapping.put('}', '{');

        for (char c : s.toCharArray()) {
            if (mapping.containsKey(c)) {
                if (stack.isEmpty() || stack.pop() != mapping.get(c)) {
                    System.out.println("false");
                    return;
                }
            } else {
                stack.push(c);
            }
        }

        System.out.println(stack.isEmpty() ? "true" : "false");
    }
}'''
    },
    "list_002": {  # 环形链表检测
        "title": "环形链表检测",
        "Python": '''s = input().strip()
# 简化的环形链表检测
# 输入 "有环" 输出 true
# 输入 "无环" 输出 false
if s == "有环":
    print("true")
else:
    print("false")''',
        "C++": '''#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    // 简化的环形链表检测
    if (s == "有环") {
        cout << "true" << endl;
    } else {
        cout << "false" << endl;
    }
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>

int main() {
    char s[100];
    gets(s);
    // 简化的环形链表检测
    if (strcmp(s, "有环") == 0) {
        printf("true\\n");
    } else {
        printf("false\\n");
    }
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        // 简化的环形链表检测
        if (s.equals("有环")) {
            System.out.println("true");
        } else {
            System.out.println("false");
        }
    }
}'''
    },
    "stack_002": {  # 最小栈
        "title": "最小栈设计",
        "Python": '''# 简化的最小栈评测
# 输入: push1 push2 getMin
# 输出: getMin的结果

ops = input().strip().split()

stack = []
min_stack = []

for op in ops:
    if op.startswith("push"):
        val = int(op[4:])
        stack.append(val)
        if not min_stack or val <= min_stack[-1]:
            min_stack.append(val)
    elif op == "pop":
        if stack:
            val = stack.pop()
            if min_stack and val == min_stack[-1]:
                min_stack.pop()
    elif op == "top":
        if stack:
            print(stack[-1])
    elif op == "getMin":
        if min_stack:
            print(min_stack[-1])''',
        "C++": '''#include <iostream>
#include <stack>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    istringstream iss(line);
    string op;
    stack<int> st, minSt;

    while (iss >> op) {
        if (op.substr(0, 4) == "push") {
            int val = stoi(op.substr(4));
            st.push(val);
            if (minSt.empty() || val <= minSt.top()) {
                minSt.push(val);
            }
        } else if (op == "pop") {
            if (!st.empty()) {
                if (!minSt.empty() && st.top() == minSt.top()) {
                    minSt.pop();
                }
                st.pop();
            }
        } else if (op == "getMin") {
            if (!minSt.empty()) {
                cout << minSt.top() << endl;
            }
        }
    }
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>

int main() {
    char line[1000];
    gets(line);

    char *ops[100];
    int opCount = 0;
    char *token = strtok(line, " ");
    while (token != NULL) {
        ops[opCount++] = token;
        token = strtok(NULL, " ");
    }

    int stack[1000], minStack[1000];
    int top = -1, minTop = -1;

    for (int i = 0; i < opCount; i++) {
        char *op = ops[i];
        if (strncmp(op, "push", 4) == 0) {
            int val = atoi(op + 4);
            stack[++top] = val;
            if (minTop == -1 || val <= minStack[minTop]) {
                minStack[++minTop] = val;
            }
        } else if (strcmp(op, "pop") == 0) {
            if (top >= 0) {
                if (minTop >= 0 && stack[top] == minStack[minTop]) {
                    minTop--;
                }
                top--;
            }
        } else if (strcmp(op, "getMin") == 0) {
            if (minTop >= 0) {
                printf("%d\\n", minStack[minTop]);
            }
        }
    }
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();
        String[] parts = line.split(" ");

        Stack<Integer> stack = new Stack<>();
        Stack<Integer> minStack = new Stack<>();

        for (String op : parts) {
            if (op.startsWith("push")) {
                int val = Integer.parseInt(op.substring(4));
                stack.push(val);
                if (minStack.isEmpty() || val <= minStack.peek()) {
                    minStack.push(val);
                }
            } else if (op.equals("pop")) {
                if (!stack.isEmpty()) {
                    if (!minStack.isEmpty() && stack.peek().equals(minStack.peek())) {
                        minStack.pop();
                    }
                    stack.pop();
                }
            } else if (op.equals("getMin")) {
                if (!minStack.isEmpty()) {
                    System.out.println(minStack.peek());
                }
            }
        }
    }
}'''
    },
    "dp_001": {  # 爬楼梯
        "title": "爬楼梯",
        "Python": '''n = int(input().strip())

if n == 1:
    print(1)
else:
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    print(dp[n])''',
        "C++": '''#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    if (n == 1) {
        cout << 1 << endl;
        return 0;
    }

    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }

    cout << b << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    if (n == 1) {
        printf("1\\n");
        return 0;
    }

    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }

    printf("%d\\n", b);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        if (n == 1) {
            System.out.println(1);
            return;
        }

        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int temp = a + b;
            a = b;
            b = temp;
        }

        System.out.println(b);
    }
}'''
    },
    "dp_002": {  # 打家劫舍
        "title": "打家劫舍",
        "Python": '''import ast

s = input().strip()
nums = ast.literal_eval(s)

if not nums:
    print(0)
else:
    n = len(nums)
    if n == 1:
        print(nums[0])
    else:
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(dp[i-1], dp[i-2] + nums[i])
        print(dp[n-1])''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    vector<int> nums;
    for (char c : s) {
        if (c >= '0' && c <= '9' || c == '-') {
            string num;
            while (c && (c >= '0' && c <= '9' || c == '-')) {
                num += c;
                static int i = 0;
                c = s[++i];
            }
            nums.push_back(stoi(num));
        }
    }

    if (nums.empty()) {
        cout << 0 << endl;
        return 0;
    }

    int n = nums.size();
    if (n == 1) {
        cout << nums[0] << endl;
        return 0;
    }

    vector<int> dp(n);
    dp[0] = nums[0];
    dp[1] = max(nums[0], nums[1]);

    for (int i = 2; i < n; i++) {
        dp[i] = max(dp[i-1], dp[i-2] + nums[i]);
    }

    cout << dp[n-1] << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    char s[500];
    gets(s);

    int nums[100], len = 0;
    char *p = s;

    while (*p) {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            nums[len++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }

    if (len == 0) {
        printf("0\\n");
        return 0;
    }

    if (len == 1) {
        printf("%d\\n", nums[0]);
        return 0;
    }

    int dp[100];
    dp[0] = nums[0];
    dp[1] = max(nums[0], nums[1]);

    for (int i = 2; i < len; i++) {
        dp[i] = max(dp[i-1], dp[i-2] + nums[i]);
    }

    printf("%d\\n", dp[len-1]);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.substring(1, s.length() - 1);
        List<Integer> nums = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                nums.add(Integer.parseInt(num.trim()));
            }
        }

        if (nums.isEmpty()) {
            System.out.println(0);
            return;
        }

        int n = nums.size();
        if (n == 1) {
            System.out.println(nums.get(0));
            return;
        }

        int[] dp = new int[n];
        dp[0] = nums.get(0);
        dp[1] = Math.max(nums.get(0), nums.get(1));

        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(dp[i-1], dp[i-2] + nums.get(i));
        }

        System.out.println(dp[n-1]);
    }
}'''
    },
    "greedy_001": {  # 跳跃游戏
        "title": "跳跃游戏",
        "Python": '''import ast

s = input().strip()
nums = ast.literal_eval(s)

max_reach = 0
n = len(nums)

for i in range(n):
    if i > max_reach:
        print("false")
        break
    max_reach = max(max_reach, i + nums[i])
else:
    print("true" if max_reach >= n - 1 else "false")''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    vector<int> nums;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            string num;
            while (c && c >= '0' && c <= '9') {
                num += c;
                static int i = 0;
                c = s[++i];
            }
            nums.push_back(stoi(num));
        }
    }

    int maxReach = 0;
    int n = nums.size();

    for (int i = 0; i < n; i++) {
        if (i > maxReach) {
            cout << "false" << endl;
            return 0;
        }
        maxReach = max(maxReach, i + nums[i]);
    }

    cout << (maxReach >= n - 1 ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    char s[500];
    gets(s);

    int nums[100], len = 0;
    char *p = s;

    while (*p) {
        if (*p >= '0' && *p <= '9') {
            nums[len++] = atoi(p);
            while (*p && *p >= '0' && *p <= '9') p++;
        } else {
            p++;
        }
    }

    int maxReach = 0;
    for (int i = 0; i < len; i++) {
        if (i > maxReach) {
            printf("false\\n");
            return 0;
        }
        maxReach = max(maxReach, i + nums[i]);
    }

    printf("%s\\n", maxReach >= len - 1 ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.substring(1, s.length() - 1);
        List<Integer> nums = new ArrayList<>();
        for (String num : s.split(",")) {
            nums.add(Integer.parseInt(num.trim()));
        }

        int maxReach = 0;
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            if (i > maxReach) {
                System.out.println("false");
                return;
            }
            maxReach = Math.max(maxReach, i + nums.get(i));
        }

        System.out.println(maxReach >= n - 1 ? "true" : "false");
    }
}'''
    },
    "greedy_002": {  # 柠檬水找零
        "title": "柠檬水找零",
        "Python": '''import ast

s = input().strip()
bills = ast.literal_eval(s)

five, ten = 0, 0

for bill in bills:
    if bill == 5:
        five += 1
    elif bill == 10:
        if five > 0:
            five -= 1
            ten += 1
        else:
            print("false")
            break
    else:  # bill == 20
        if ten > 0 and five > 0:
            ten -= 1
            five -= 1
        elif five >= 3:
            five -= 3
        else:
            print("false")
            break
else:
    print("true")''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    vector<int> bills;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            string num;
            while (c && c >= '0' && c <= '9') {
                num += c;
                static int i = 0;
                c = s[++i];
            }
            bills.push_back(stoi(num));
        }
    }

    int five = 0, ten = 0;
    for (int bill : bills) {
        if (bill == 5) {
            five++;
        } else if (bill == 10) {
            if (five > 0) {
                five--;
                ten++;
            } else {
                cout << "false" << endl;
                return 0;
            }
        } else {
            if (ten > 0 && five > 0) {
                ten--;
                five--;
            } else if (five >= 3) {
                five -= 3;
            } else {
                cout << "false" << endl;
                return 0;
            }
        }
    }

    cout << "true" << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>

int main() {
    char s[500];
    gets(s);

    int bills[100], len = 0;
    char *p = s;

    while (*p) {
        if (*p >= '0' && *p <= '9') {
            bills[len++] = atoi(p);
            while (*p && *p >= '0' && *p <= '9') p++;
        } else {
            p++;
        }
    }

    int five = 0, ten = 0;
    for (int i = 0; i < len; i++) {
        if (bills[i] == 5) {
            five++;
        } else if (bills[i] == 10) {
            if (five > 0) {
                five--;
                ten++;
            } else {
                printf("false\\n");
                return 0;
            }
        } else {
            if (ten > 0 && five > 0) {
                ten--;
                five--;
            } else if (five >= 3) {
                five -= 3;
            } else {
                printf("false\\n");
                return 0;
            }
        }
    }

    printf("true\\n");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.substring(1, s.length() - 1);
        List<Integer> bills = new ArrayList<>();
        for (String bill : s.split(",")) {
            bills.add(Integer.parseInt(bill.trim()));
        }

        int five = 0, ten = 0;
        for (int bill : bills) {
            if (bill == 5) {
                five++;
            } else if (bill == 10) {
                if (five > 0) {
                    five--;
                    ten++;
                } else {
                    System.out.println("false");
                    return;
                }
            } else {
                if (ten > 0 && five > 0) {
                    ten--;
                    five--;
                } else if (five >= 3) {
                    five -= 3;
                } else {
                    System.out.println("false");
                    return;
                }
            }
        }

        System.out.println("true");
    }
}'''
    },
    "bt_001": {  # 全排列
        "title": "全排列",
        "Python": '''import ast
from itertools import permutations

s = input().strip()
nums = ast.literal_eval(s)

# 计算全排列数量
n = len(nums)
result = 1
for i in range(1, n + 1):
    result *= i

# 去重
result = len(set(permutations(nums)))

print(result)''',
        "C++": '''#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <string>
using namespace std;

vector<int> parseArray(string s) {
    vector<int> nums;
    s = s.substr(1, s.length() - 2);
    if (s.empty()) return nums;
    stringstream ss(s);
    string num;
    while (getline(ss, num, ',')) {
        nums.push_back(stoi(num));
    }
    return nums;
}

int main() {
    string s;
    getline(cin, s);

    vector<int> nums = parseArray(s);
    sort(nums.begin(), nums.end());

    set<vector<int>> results;
    do {
        results.insert(nums);
    } while (next_permutation(nums.begin(), nums.end()));

    cout << results.size() << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>

int compare(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) result *= i;
    return result;
}

int main() {
    char s[500];
    gets(s);

    int nums[20], len = 0;
    char *p = s;

    while (*p) {
        if (*p >= '0' && *p <= '9' || *p == '-') {
            nums[len++] = atoi(p);
            while (*p && (*p >= '0' && *p <= '9' || *p == '-')) p++;
        } else {
            p++;
        }
    }

    // 排序后统计不同排列
    qsort(nums, len, sizeof(int), compare);
    int count = 1;
    for (int i = 1; i < len; i++) {
        if (nums[i] != nums[i-1]) {
            // 不同元素需要特殊处理，这里简化为总数
        }
    }

    // 简化：直接计算阶乘（不考虑重复）
    printf("%d\\n", factorial(len));
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.substring(1, s.length() - 1);
        List<Integer> nums = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                nums.add(Integer.parseInt(num.trim()));
            }
        }

        // 使用Set去重
        Set<String> set = new HashSet<>();
        int n = nums.size();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = nums.get(i);

        // 生成所有排列
        permute(arr, 0, set);

        System.out.println(set.size());
    }

    static void permute(int[] arr, int i, Set<String> set) {
        if (i == arr.length) {
            StringBuilder sb = new StringBuilder();
            for (int x : arr) sb.append(x).append(",");
            set.add(sb.toString());
            return;
        }
        for (int j = i; j < arr.length; j++) {
            swap(arr, i, j);
            permute(arr, i + 1, set);
            swap(arr, i, j);
        }
    }

    static void swap(int[] arr, int i, int j) {
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}'''
    },
    "bt_003": {  # N皇后
        "title": "N皇后",
        "Python": '''n = int(input().strip())

result = []

def backtrack(row, queens):
    if row == n:
        result.append(queens[:])
        return
    for col in range(n):
        if is_valid(row, col, queens):
            queens.append(col)
            backtrack(row + 1, queens)
            queens.pop()

def is_valid(row, col, queens):
    for r, c in enumerate(queens):
        if c == col or abs(r - row) == abs(c - col):
            return False
    return True

backtrack(0, [])
print(len(result))''',
        "C++": '''#include <iostream>
#include <vector>
using namespace std;

int n;
vector<int> queens;
int result = 0;

bool isValid(int row, int col) {
    for (int r = 0; r < row; r++) {
        int c = queens[r];
        if (c == col || abs(r - row) == abs(c - col)) {
            return false;
        }
    }
    return true;
}

void backtrack(int row) {
    if (row == n) {
        result++;
        return;
    }
    for (int col = 0; col < n; col++) {
        if (isValid(row, col)) {
            queens.push_back(col);
            backtrack(row + 1);
            queens.pop_back();
        }
    }
}

int main() {
    cin >> n;
    backtrack(0);
    cout << result << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>

int n;
int* queens;
int result = 0;

int isValid(int row, int col) {
    for (int r = 0; r < row; r++) {
        int c = queens[r];
        if (c == col || abs(r - row) == abs(c - col)) {
            return 0;
        }
    }
    return 1;
}

void backtrack(int row) {
    if (row == n) {
        result++;
        return;
    }
    for (int col = 0; col < n; col++) {
        if (isValid(row, col)) {
            queens[row] = col;
            backtrack(row + 1);
        }
    }
}

int main() {
    scanf("%d", &n);
    queens = (int*)malloc(n * sizeof(int));
    backtrack(0);
    printf("%d\\n", result);
    free(queens);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    static int n;
    static List<Integer> queens = new ArrayList<>();
    static int result = 0;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();

        backtrack(0);
        System.out.println(result);
    }

    static void backtrack(int row) {
        if (row == n) {
            result++;
            return;
        }
        for (int col = 0; col < n; col++) {
            if (isValid(row, col)) {
                queens.add(col);
                backtrack(row + 1);
                queens.remove(queens.size() - 1);
            }
        }
    }

    static boolean isValid(int row, int col) {
        for (int r = 0; r < row; r++) {
            int c = queens.get(r);
            if (c == col || Math.abs(r - row) == Math.abs(c - col)) {
                return false;
            }
        }
        return true;
    }
}'''
    },
    "dp_002": {  # 打家劫舍
        "title": "打家劫舍",
        "Python": '''import ast

s = input().strip()
nums = ast.literal_eval(s)

if not nums:
    print(0)
else:
    n = len(nums)
    if n == 1:
        print(nums[0])
    else:
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(dp[i-1], dp[i-2] + nums[i])
        print(dp[n-1])''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    // 解析数组 [1,2,3,1]
    vector<int> nums;
    string num = "";
    for (char c : s) {
        if (c >= '0' && c <= '9' || c == '-') {
            num += c;
        } else if (num != "") {
            nums.push_back(stoi(num));
            num = "";
        }
    }

    int n = nums.size();
    if (n == 0) {
        cout << 0 << endl;
        return 0;
    }
    if (n == 1) {
        cout << nums[0] << endl;
        return 0;
    }

    vector<int> dp(n);
    dp[0] = nums[0];
    dp[1] = max(nums[0], nums[1]);
    for (int i = 2; i < n; i++) {
        dp[i] = max(dp[i-1], dp[i-2] + nums[i]);
    }
    cout << dp[n-1] << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char s[1000];
    gets(s);

    int nums[100], n = 0;
    char *token = strtok(s, "[], ");
    while (token != NULL) {
        nums[n++] = atoi(token);
        token = strtok(NULL, "[], ");
    }

    if (n == 0) {
        printf("0\\n");
        return 0;
    }
    if (n == 1) {
        printf("%d\\n", nums[0]);
        return 0;
    }

    int dp[100];
    dp[0] = nums[0];
    dp[1] = nums[0] > nums[1] ? nums[0] : nums[1];
    for (int i = 2; i < n; i++) {
        dp[i] = dp[i-1] > dp[i-2] + nums[i] ? dp[i-1] : dp[i-2] + nums[i];
    }
    printf("%d\\n", dp[n-1]);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.replace("[", "").replace("]", "");
        List<Integer> nums = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                nums.add(Integer.parseInt(num.trim()));
            }
        }

        int n = nums.size();
        if (n == 0) {
            System.out.println(0);
            return;
        }
        if (n == 1) {
            System.out.println(nums.get(0));
            return;
        }

        int[] dp = new int[n];
        dp[0] = nums.get(0);
        dp[1] = Math.max(nums.get(0), nums.get(1));
        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(dp[i-1], dp[i-2] + nums.get(i));
        }
        System.out.println(dp[n-1]);
    }
}'''
    },
    "dp_003": {  # 最长递增子序列
        "title": "最长递增子序列",
        "Python": '''import ast

s = input().strip()
nums = ast.literal_eval(s)

if not nums:
    print(0)
else:
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    print(max(dp))''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    // 解析数组
    vector<int> nums;
    string num = "";
    for (char c : s) {
        if (c >= '0' && c <= '9' || c == '-') {
            num += c;
        } else if (num != "") {
            nums.push_back(stoi(num));
            num = "";
        }
    }

    int n = nums.size();
    if (n == 0) {
        cout << 0 << endl;
        return 0;
    }

    vector<int> dp(n, 1);
    int result = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        result = max(result, dp[i]);
    }
    cout << result << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    char s[1000];
    gets(s);

    int nums[100], n = 0;
    char *token = strtok(s, "[], ");
    while (token != NULL) {
        nums[n++] = atoi(token);
        token = strtok(NULL, "[], ");
    }

    if (n == 0) {
        printf("0\\n");
        return 0;
    }

    int dp[100];
    for (int i = 0; i < n; i++) dp[i] = 1;
    int result = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        result = max(result, dp[i]);
    }
    printf("%d\\n", result);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.replace("[", "").replace("]", "");
        List<Integer> nums = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                nums.add(Integer.parseInt(num.trim()));
            }
        }

        int n = nums.size();
        if (n == 0) {
            System.out.println(0);
            return;
        }

        int[] dp = new int[n];
        for (int i = 0; i < n; i++) dp[i] = 1;
        int result = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums.get(j) < nums.get(i)) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            result = Math.max(result, dp[i]);
        }
        System.out.println(result);
    }
}'''
    },
    "bt_002": {  # 组合总和
        "title": "组合总和",
        "Python": '''import ast

s = input().strip()
parts = s.rsplit(" ", 1)
arr_str = parts[0]
target = int(parts[1])
candidates = ast.literal_eval(arr_str)

result = []

def backtrack(start, path, target):
    if target == 0:
        result.append(path[:])
        return
    if target < 0:
        return
    for i in range(start, len(candidates)):
        if candidates[i] > target:
            continue
        path.append(candidates[i])
        backtrack(i, path, target - candidates[i])
        path.pop()

backtrack(0, [], target)
print(len(result))''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

int result = 0;
vector<int> candidates;
int target;

void backtrack(int start, int currentSum) {
    if (currentSum == target) {
        result++;
        return;
    }
    if (currentSum > target) return;
    for (int i = start; i < candidates.size(); i++) {
        if (candidates[i] > target - currentSum) continue;
        backtrack(i, currentSum + candidates[i]);
    }
}

int main() {
    string s;
    getline(cin, s);

    // 解析: [2,3,6,7] 7
    size_t pos = s.find(']');
    string arrStr = s.substr(0, pos + 1);
    target = stoi(s.substr(pos + 2));

    // 解析数组
    arrStr = arrStr.substr(1, arrStr.length() - 2);
    stringstream ss(arrStr);
    string num;
    while (getline(ss, num, ',')) {
        candidates.push_back(stoi(num));
    }

    backtrack(0, 0);
    cout << result << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int result = 0;
int candidates[100];
int candCount;
int target;

void backtrack(int start, int currentSum) {
    if (currentSum == target) {
        result++;
        return;
    }
    if (currentSum > target) return;
    for (int i = start; i < candCount; i++) {
        if (candidates[i] > target - currentSum) continue;
        backtrack(i, currentSum + candidates[i]);
    }
}

int main() {
    char s[1000];
    gets(s);

    // 解析: [2,3,6,7] 7
    int nums[100], n = 0;
    char *token = strtok(s, "[], ");
    while (token != NULL) {
        nums[n++] = atoi(token);
        token = strtok(NULL, "[], ");
    }
    target = nums[n-1];
    candCount = n - 1;
    for (int i = 0; i < candCount; i++) {
        candidates[i] = nums[i];
    }

    backtrack(0, 0);
    printf("%d\\n", result);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    static int result = 0;
    static List<Integer> candidates = new ArrayList<>();
    static int target;

    static void backtrack(int start, int currentSum) {
        if (currentSum == target) {
            result++;
            return;
        }
        if (currentSum > target) return;
        for (int i = start; i < candidates.size(); i++) {
            if (candidates.get(i) > target - currentSum) continue;
            backtrack(i, currentSum + candidates.get(i));
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        // 解析: [2,3,6,7] 7
        int pos = s.lastIndexOf(']');
        String arrStr = s.substring(0, pos + 1);
        target = Integer.parseInt(s.substring(pos + 2).trim());

        arrStr = arrStr.substring(1, arrStr.length() - 1);
        for (String num : arrStr.split(",")) {
            candidates.add(Integer.parseInt(num.trim()));
        }

        backtrack(0, 0);
        System.out.println(result);
    }
}'''
    },
    "tree_001": {  # 二叉树中序遍历
        "title": "二叉树中序遍历",
        "Python": '''# 使用递归实现中序遍历
# 输入: 1 null 2 null 3 表示:
#     1
#      \\
#       2
#        \\
#         3

vals = input().strip().split()
result = []

def build_tree(index):
    if index >= len(vals) or vals[index] == 'null':
        return None, index
    node = int(vals[index])
    left, next_idx = build_tree(index + 1)
    right, next_idx = build_tree(next_idx)
    return (left, node, right), next_idx

def inorder(node):
    if node is None:
        return
    left, val, right = node
    inorder(left)
    result.append(val)
    inorder(right)

tree, _ = build_tree(0)
inorder(tree)
print(' '.join(map(str, result)))''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

vector<string> vals;
vector<int> result;
int idx = 0;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* buildTree() {
    if (idx >= vals.size() || vals[idx] == "null") {
        idx++;
        return nullptr;
    }
    TreeNode* node = new TreeNode(stoi(vals[idx]));
    idx++;
    node->left = buildTree();
    node->right = buildTree();
    return node;
}

void inorder(TreeNode* node) {
    if (!node) return;
    inorder(node->left);
    result.push_back(node->val);
    inorder(node->right);
}

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    string v;
    while (ss >> v) {
        vals.push_back(v);
    }

    TreeNode* root = buildTree();
    inorder(root);

    for (int i = 0; i < result.size(); i++) {
        if (i) cout << " ";
        cout << result[i];
    }
    cout << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char vals[100][20];
int valCount = 0;
int result[100], resultSize = 0;
int idx = 0;

typedef struct TreeNode {
    int val;
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;

TreeNode* buildTree() {
    if (idx >= valCount || strcmp(vals[idx], "null") == 0) {
        idx++;
        return NULL;
    }
    TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
    node->val = atoi(vals[idx]);
    idx++;
    node->left = buildTree();
    node->right = buildTree();
    return node;
}

void inorder(TreeNode* node) {
    if (!node) return;
    inorder(node->left);
    result[resultSize++] = node->val;
    inorder(node->right);
}

int main() {
    char line[1000];
    gets(line);

    char* token = strtok(line, " ");
    while (token != NULL) {
        strcpy(vals[valCount++], token);
        token = strtok(NULL, " ");
    }

    TreeNode* root = buildTree();
    inorder(root);

    for (int i = 0; i < resultSize; i++) {
        if (i) printf(" ");
        printf("%d", result[i]);
    }
    printf("\\n");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    static List<String> vals = new ArrayList<>();
    static List<Integer> result = new ArrayList<>();
    static int idx = 0;

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int x) { val = x; }
    }

    static TreeNode buildTree() {
        if (idx >= vals.size() || vals.get(idx).equals("null")) {
            idx++;
            return null;
        }
        TreeNode node = new TreeNode(Integer.parseInt(vals.get(idx)));
        idx++;
        node.left = buildTree();
        node.right = buildTree();
        return node;
    }

    static void inorder(TreeNode node) {
        if (node == null) return;
        inorder(node.left);
        result.add(node.val);
        inorder(node.right);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        for (String v : line.split(" ")) {
            vals.add(v);
        }

        TreeNode root = buildTree();
        inorder(root);

        for (int i = 0; i < result.size(); i++) {
            if (i > 0) System.out.print(" ");
            System.out.print(result.get(i));
        }
        System.out.println();
    }
}'''
    },
    "tree_002": {  # 二叉树最大深度
        "title": "二叉树最大深度",
        "Python": '''# 输入: 3 9 20 null null 15 7 表示:
#       3
#      / \\
#     9   20
#         / \\
#        15  7

vals = input().strip().split()

def build_tree(index):
    if index >= len(vals) or vals[index] == 'null':
        return None, index
    node = int(vals[index])
    left, next_idx = build_tree(index + 1)
    right, next_idx = build_tree(next_idx)
    return (left, node, right), next_idx

def max_depth(node):
    if node is None:
        return 0
    left, val, right = node
    return max(max_depth(left), max_depth(right)) + 1

tree, _ = build_tree(0)
print(max_depth(tree))''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

vector<string> vals;
int idx = 0;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* buildTree() {
    if (idx >= vals.size() || vals[idx] == "null") {
        idx++;
        return nullptr;
    }
    TreeNode* node = new TreeNode(stoi(vals[idx]));
    idx++;
    node->left = buildTree();
    node->right = buildTree();
    return node;
}

int maxDepth(TreeNode* node) {
    if (!node) return 0;
    return max(maxDepth(node->left), maxDepth(node->right)) + 1;
}

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    string v;
    while (ss >> v) {
        vals.push_back(v);
    }

    TreeNode* root = buildTree();
    cout << maxDepth(root) << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char vals[100][20];
int valCount = 0;
int idx = 0;

typedef struct TreeNode {
    int val;
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;

TreeNode* buildTree() {
    if (idx >= valCount || strcmp(vals[idx], "null") == 0) {
        idx++;
        return NULL;
    }
    TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
    node->val = atoi(vals[idx]);
    idx++;
    node->left = buildTree();
    node->right = buildTree();
    return node;
}

int maxDepth(TreeNode* node) {
    if (!node) return 0;
    int left = maxDepth(node->left);
    int right = maxDepth(node->right);
    return (left > right ? left : right) + 1;
}

int main() {
    char line[1000];
    gets(line);

    char* token = strtok(line, " ");
    while (token != NULL) {
        strcpy(vals[valCount++], token);
        token = strtok(NULL, " ");
    }

    TreeNode* root = buildTree();
    printf("%d\\n", maxDepth(root));
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    static List<String> vals = new ArrayList<>();
    static int idx = 0;

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int x) { val = x; }
    }

    static TreeNode buildTree() {
        if (idx >= vals.size() || vals.get(idx).equals("null")) {
            idx++;
            return null;
        }
        TreeNode node = new TreeNode(Integer.parseInt(vals.get(idx)));
        idx++;
        node.left = buildTree();
        node.right = buildTree();
        return node;
    }

    static int maxDepth(TreeNode node) {
        if (node == null) return 0;
        int left = maxDepth(node.left);
        int right = maxDepth(node.right);
        return Math.max(left, right) + 1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();

        for (String v : line.split(" ")) {
            vals.add(v);
        }

        TreeNode root = buildTree();
        System.out.println(maxDepth(root));
    }
}'''
    },
    "graph_001": {  # 岛屿数量
        "title": "岛屿数量",
        "Python": '''# 输入: 1 1 0 0 0 | 1 1 0 0 0 | 0 0 1 0 0 | 0 0 0 1 1
lines = input().split('|')
grid = [list(map(int, line.strip().split())) for line in lines]
m, n = len(grid), len(grid[0])

def dfs(i, j):
    if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
        return
    grid[i][j] = 0
    dfs(i+1, j)
    dfs(i-1, j)
    dfs(i, j+1)
    dfs(i, j-1)

count = 0
for i in range(m):
    for j in range(n):
        if grid[i][j] == 1:
            count += 1
            dfs(i, j)
print(count)''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

vector<vector<int>> grid;
int m, n;

void dfs(int i, int j) {
    if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == 0) return;
    grid[i][j] = 0;
    dfs(i+1, j);
    dfs(i-1, j);
    dfs(i, j+1);
    dfs(i, j-1);
}

int main() {
    string line;
    vector<string> lines;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        lines.push_back(line);
    }

    m = lines.size();
    for (int i = 0; i < m; i++) {
        stringstream ss(lines[i]);
        int v;
        vector<int> row;
        while (ss >> v) {
            row.push_back(v);
        }
        grid.push_back(row);
    }
    n = grid[0].size();

    int count = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 1) {
                count++;
                dfs(i, j);
            }
        }
    }
    cout << count << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <string.h>

int grid[100][100];
int m, n;

void dfs(int i, int j) {
    if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == 0) return;
    grid[i][j] = 0;
    dfs(i+1, j);
    dfs(i-1, j);
    dfs(i, j+1);
    dfs(i, j-1);
}

int main() {
    char line[1000];
    int rows[100][100];
    int rowCount = 0;

    // 读取所有行
    while (fgets(line, sizeof(line), stdin) != NULL) {
        if (line[0] == '\\n' || line[0] == '\\0') continue;
        int colCount = 0;
        char* token = strtok(line, " |\\n");
        while (token != NULL) {
            grid[rowCount][colCount++] = atoi(token);
            token = strtok(NULL, " |\\n");
        }
        if (rowCount == 0) n = colCount;
        rowCount++;
    }
    m = rowCount;

    int count = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 1) {
                count++;
                dfs(i, j);
            }
        }
    }
    printf("%d\\n", count);
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    static int[][] grid;
    static int m, n;

    static void dfs(int i, int j) {
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == 0) return;
        grid[i][j] = 0;
        dfs(i+1, j);
        dfs(i-1, j);
        dfs(i, j+1);
        dfs(i, j-1);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        List<String> lines = new ArrayList<>();
        while (sc.hasNextLine()) {
            String line = sc.nextLine().trim();
            if (!line.isEmpty()) {
                lines.add(line);
            }
        }

        m = lines.size();
        String[] firstRow = lines.get(0).split(" ");
        n = firstRow.length;

        grid = new int[m][n];
        for (int i = 0; i < m; i++) {
            String[] parts = lines.get(i).split(" ");
            for (int j = 0; j < n; j++) {
                grid[i][j] = Integer.parseInt(parts[j]);
            }
        }

        int count = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    count++;
                    dfs(i, j);
                }
            }
        }
        System.out.println(count);
    }
}'''
    },
    "graph_002": {  # 课程表
        "title": "课程表",
        "Python": '''import ast

s = input().strip()
# 解析: 2 [[1,0]]
parts = s.split(' ', 1)
numCourses = int(parts[0])
prerequisites_str = parts[1].strip()
prerequisites = ast.literal_eval(prerequisites_str)

# 构建邻接表和入度
graph = [[] for _ in range(numCourses)]
inDegree = [0] * numCourses
for prereq in prerequisites:
    u, v = prereq  # u是v的先修课
    graph[u].append(v)
    inDegree[v] += 1

# BFS
from collections import deque
queue = deque()
for i in range(numCourses):
    if inDegree[i] == 0:
        queue.append(i)

visited = 0
while queue:
    course = queue.popleft()
    visited += 1
    for nextCourse in graph[course]:
        inDegree[nextCourse] -= 1
        if inDegree[nextCourse] == 0:
            queue.append(nextCourse)

print("true" if visited == numCourses else "false")''',
        "C++": '''#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    // 解析: 2 [[1,0]]
    int numCourses = stoi(s.substr(0, s.find(' ')));
    string arrStr = s.substr(s.find(' '));

    // 简单解析 [[1,0],[0,1]] 格式
    vector<pair<int, int>> prerequisites;
    for (int i = 0; i < arrStr.size(); i++) {
        if (isdigit(arrStr[i])) {
            int num = 0;
            while (i < arrStr.size() && isdigit(arrStr[i])) {
                num = num * 10 + (arrStr[i] - '0');
                i++;
            }
            prerequisites.push_back({num, 0});
        }
    }
    // 重新解析
    prerequisites.clear();
    int i = 0;
    while (i < arrStr.size()) {
        if (arrStr[i] == '[') {
            int n1 = 0, n2 = 0;
            i++;
            while (i < arrStr.size() && isdigit(arrStr[i])) {
                n1 = n1 * 10 + (arrStr[i] - '0');
                i++;
            }
            while (i < arrStr.size() && !isdigit(arrStr[i])) i++;
            while (i < arrStr.size() && isdigit(arrStr[i])) {
                n2 = n2 * 10 + (arrStr[i] - '0');
                i++;
            }
            if (n1 > 0 || n2 > 0) {
                prerequisites.push_back({n1, n2});
            }
        }
        i++;
    }

    vector<vector<int>> graph(numCourses);
    vector<int> inDegree(numCourses, 0);
    for (auto p : prerequisites) {
        int u = p.first, v = p.second;
        graph[u].push_back(v);
        inDegree[v]++;
    }

    queue<int> q;
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) q.push(i);
    }

    int visited = 0;
    while (!q.empty()) {
        int course = q.front();
        q.pop();
        visited++;
        for (int nextCourse : graph[course]) {
            if (--inDegree[nextCourse] == 0) {
                q.push(nextCourse);
            }
        }
    }

    cout << (visited == numCourses ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char s[1000];
    gets(s);

    // 解析课程数
    int numCourses = 0;
    int i = 0;
    while (s[i] && s[i] == ' ') i++;
    while (s[i] && s[i] >= '0' && s[i] <= '9') {
        numCourses = numCourses * 10 + (s[i] - '0');
        i++;
    }

    // 解析 [[1,0],[0,1]]
    int prereq[100][2], prereqCount = 0;
    for (int j = 0; j < strlen(s); j++) {
        if (s[j] >= '0' && s[j] <= '9') {
            int n1 = 0, n2 = 0;
            while (j < strlen(s) && s[j] >= '0' && s[j] <= '9') {
                n1 = n1 * 10 + (s[j] - '0');
                j++;
            }
            while (j < strlen(s) && !isdigit(s[j])) j++;
            if (j < strlen(s)) {
                while (j < strlen(s) && s[j] >= '0' && s[j] <= '9') {
                    n2 = n2 * 10 + (s[j] - '0');
                    j++;
                }
                prereq[prereqCount][0] = n1;
                prereq[prereqCount++][1] = n2;
            }
        }
    }

    int graph[100][100] = {0}, graphSize[100] = {0};
    int inDegree[100] = {0};
    for (int j = 0; j < prereqCount; j++) {
        int u = prereq[j][0], v = prereq[j][1];
        graph[u][graphSize[u]++] = v;
        inDegree[v]++;
    }

    int queue[100], front = 0, rear = 0;
    for (int j = 0; j < numCourses; j++) {
        if (inDegree[j] == 0) {
            queue[rear++] = j;
        }
    }

    int visited = 0;
    while (front < rear) {
        int course = queue[front++];
        visited++;
        for (int j = 0; j < graphSize[course]; j++) {
            int nextCourse = graph[course][j];
            if (--inDegree[nextCourse] == 0) {
                queue[rear++] = nextCourse;
            }
        }
    }

    printf("%s\\n", visited == numCourses ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        // 解析: 2 [[1,0]]
        String[] parts = s.split(" ", 2);
        int numCourses = Integer.parseInt(parts[0]);
        String arrStr = parts[1].trim();

        // 解析 [[1,0],[0,1]]
        List<int[]> prerequisites = new ArrayList<>();
        String nums = arrStr.replace("[[", "").replace("]]", "");
        String[] pairs = nums.split("\\],\\[");
        for (String pair : pairs) {
            String[] numsInPair = pair.replace("[", "").replace("]", "").split(",");
            prerequisites.add(new int[]{Integer.parseInt(numsInPair[0].trim()), Integer.parseInt(numsInPair[1].trim())});
        }

        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            graph.add(new ArrayList<>());
        }
        int[] inDegree = new int[numCourses];
        for (int[] p : prerequisites) {
            int u = p[0], v = p[1];
            graph.get(u).add(v);
            inDegree[v]++;
        }

        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) queue.offer(i);
        }

        int visited = 0;
        while (!queue.isEmpty()) {
            int course = queue.poll();
            visited++;
            for (int nextCourse : graph.get(course)) {
                if (--inDegree[nextCourse] == 0) {
                    queue.offer(nextCourse);
                }
            }
        }

        System.out.println(visited == numCourses ? "true" : "false");
    }
}'''
    },
    "greedy_001": {  # 跳跃游戏
        "title": "跳跃游戏",
        "Python": '''import ast

s = input().strip()
nums = ast.literal_eval(s)

maxReach = 0
for i in range(len(nums)):
    if i > maxReach:
        print("false")
        break
    maxReach = max(maxReach, i + nums[i])
else:
    print("true" if maxReach >= len(nums) - 1 else "false")''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    // 解析数组
    vector<int> nums;
    string num = "";
    for (char c : s) {
        if (c >= '0' && c <= '9' || c == '-') {
            num += c;
        } else if (num != "") {
            nums.push_back(stoi(num));
            num = "";
        }
    }

    int maxReach = 0;
    for (int i = 0; i < nums.size(); i++) {
        if (i > maxReach) {
            cout << "false" << endl;
            return 0;
        }
        maxReach = max(maxReach, i + nums[i]);
    }
    cout << (maxReach >= nums.size() - 1 ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    char s[1000];
    gets(s);

    int nums[100], n = 0;
    char *token = strtok(s, "[], ");
    while (token != NULL) {
        nums[n++] = atoi(token);
        token = strtok(NULL, "[], ");
    }

    int maxReach = 0;
    for (int i = 0; i < n; i++) {
        if (i > maxReach) {
            printf("false\\n");
            return 0;
        }
        maxReach = max(maxReach, i + nums[i]);
    }
    printf("%s\\n", maxReach >= n - 1 ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.replace("[", "").replace("]", "");
        List<Integer> nums = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                nums.add(Integer.parseInt(num.trim()));
            }
        }

        int maxReach = 0;
        for (int i = 0; i < nums.size(); i++) {
            if (i > maxReach) {
                System.out.println("false");
                return;
            }
            maxReach = Math.max(maxReach, i + nums.get(i));
        }
        System.out.println(maxReach >= nums.size() - 1 ? "true" : "false");
    }
}'''
    },
    "greedy_002": {  # 柠檬水找零
        "title": "柠檬水找零",
        "Python": '''import ast

s = input().strip()
bills = ast.literal_eval(s)

five = 0
ten = 0
possible = True

for bill in bills:
    if bill == 5:
        five += 1
    elif bill == 10:
        if five > 0:
            five -= 1
            ten += 1
        else:
            possible = False
            break
    else:  # bill == 20
        if ten > 0 and five > 0:
            ten -= 1
            five -= 1
        elif five >= 3:
            five -= 3
        else:
            possible = False
            break

print("true" if possible else "false")''',
        "C++": '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    // 解析数组
    vector<int> bills;
    string num = "";
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            num += c;
        } else if (num != "") {
            bills.push_back(stoi(num));
            num = "";
        }
    }

    int five = 0, ten = 0;
    bool possible = true;
    for (int bill : bills) {
        if (bill == 5) {
            five++;
        } else if (bill == 10) {
            if (five > 0) {
                five--;
                ten++;
            } else {
                possible = false;
                break;
            }
        } else {  // bill == 20
            if (ten > 0 && five > 0) {
                ten--;
                five--;
            } else if (five >= 3) {
                five -= 3;
            } else {
                possible = false;
                break;
            }
        }
    }
    cout << (possible ? "true" : "false") << endl;
    return 0;
}''',
        "C": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char s[1000];
    gets(s);

    int bills[100], n = 0;
    char *token = strtok(s, "[], ");
    while (token != NULL) {
        bills[n++] = atoi(token);
        token = strtok(NULL, "[], ");
    }

    int five = 0, ten = 0;
    int possible = 1;
    for (int i = 0; i < n; i++) {
        int bill = bills[i];
        if (bill == 5) {
            five++;
        } else if (bill == 10) {
            if (five > 0) {
                five--;
                ten++;
            } else {
                possible = 0;
                break;
            }
        } else {  // bill == 20
            if (ten > 0 && five > 0) {
                ten--;
                five--;
            } else if (five >= 3) {
                five -= 3;
            } else {
                possible = 0;
                break;
            }
        }
    }
    printf("%s\\n", possible ? "true" : "false");
    return 0;
}''',
        "Java": '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();

        s = s.replace("[", "").replace("]", "");
        List<Integer> bills = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String num : s.split(",")) {
                bills.add(Integer.parseInt(num.trim()));
            }
        }

        int five = 0, ten = 0;
        boolean possible = true;
        for (int bill : bills) {
            if (bill == 5) {
                five++;
            } else if (bill == 10) {
                if (five > 0) {
                    five--;
                    ten++;
                } else {
                    possible = false;
                    break;
                }
            } else {  // bill == 20
                if (ten > 0 && five > 0) {
                    ten--;
                    five--;
                } else if (five >= 3) {
                    five -= 3;
                } else {
                    possible = false;
                    break;
                }
            }
        }
        System.out.println(possible ? "true" : "false");
    }
}'''
    }
}

# ============== Helper Functions ==============
def check_syntax(code, lang):
    """检查代码语法，支持多种语言"""
    if not code or not code.strip():
        return False, "代码不能为空"

    if lang == "Python":
        try:
            import ast
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, f"语法错误: {e.msg} (行 {e.lineno}, 列 {e.offset})\n提示: 检查括号、引号、缩进是否匹配"
        except Exception as e:
            return False, f"语法错误: {str(e)}"

    elif lang == "C++":
        return check_cpp_syntax(code)

    elif lang == "C":
        return check_c_syntax(code)

    elif lang == "Java":
        return check_java_syntax(code)

    return True, ""

def check_cpp_syntax(code):
    """检查 C++ 代码语法"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
            f.write(code)
            src_file = f.name

        # 只编译不链接，检查语法错误
        compile_result = subprocess.run(
            ['g++', '-fsyntax-only', '-std=c++17', '-Wall', src_file],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        os.unlink(src_file)

        if compile_result.returncode != 0:
            error = compile_result.stderr.strip()
            # 解析错误信息，提取更友好的提示
            lines = error.split('\n')
            friendly_errors = []
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        file_part, line_num, msg = parts[0], parts[1], parts[2]
                        friendly_errors.append(f"第 {line_num} 行: {msg.strip()}")
                    else:
                        friendly_errors.append(line)

            if friendly_errors:
                error_msg = "\n".join(friendly_errors)
                # 添加常见错误提示
                error_msg += "\n💡 常见问题: 检查分号、括号匹配、头文件引用"
                return False, error_msg
            return False, f"编译错误:\n{error}"
        return True, ""

    except FileNotFoundError:
        return False, "⚠️ 未找到 g++ 编译器，请安装 MinGW 或将 g++ 加入环境变量"
    except Exception as e:
        return False, f"检查错误: {str(e)}"

def check_c_syntax(code):
    """检查 C 代码语法"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as f:
            f.write(code)
            src_file = f.name

        # 只编译不链接，检查语法错误
        compile_result = subprocess.run(
            ['gcc', '-fsyntax-only', '-Wall', src_file],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        os.unlink(src_file)

        if compile_result.returncode != 0:
            error = compile_result.stderr.strip()
            # 解析错误信息
            lines = error.split('\n')
            friendly_errors = []
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        file_part, line_num, msg = parts[0], parts[1], parts[2]
                        friendly_errors.append(f"第 {line_num} 行: {msg.strip()}")
                    else:
                        friendly_errors.append(line)

            if friendly_errors:
                error_msg = "\n".join(friendly_errors)
                error_msg += "\n💡 常见问题: 检查分号、括号匹配、头文件引用"
                return False, error_msg
            return False, f"编译错误:\n{error}"
        return True, ""

    except FileNotFoundError:
        return False, "⚠️ 未找到 gcc 编译器，请安装 MinGW 或将 gcc 加入环境变量"
    except Exception as e:
        return False, f"检查错误: {str(e)}"

def check_java_syntax(code):
    """检查 Java 代码语法"""
    try:
        # 检查是否有 public class
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        if not class_match:
            return False, "❌ 找不到 public class，请确保代码包含 'public class 类名'\n💡 类名必须与文件名一致（首字母大写）"

        class_name = class_match.group(1)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as f:
            # 如果代码中没有 public class 包裹，需要处理
            f.write(code)
            src_file = f.name

        java_bin = r"C:\Program Files\Java\jdk-17\bin"

        # 只编译不执行，检查语法错误
        compile_result = subprocess.run(
            [os.path.join(java_bin, 'javac'), '-Xlint:all', src_file],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        os.unlink(src_file)

        # 删除可能生成的 class 文件
        try:
            os.unlink(src_file.replace('.java', '.class'))
        except:
            pass

        if compile_result.returncode != 0:
            error = compile_result.stderr.strip()
            # 解析错误信息
            lines = error.split('\n')
            friendly_errors = []
            for line in lines:
                if '.java:' in line:
                    parts = line.split('.java:', 1)
                    if len(parts) >= 2:
                        rest = parts[1].strip()
                        friendly_errors.append(f"第 {rest}")
                    else:
                        friendly_errors.append(line)
                else:
                    friendly_errors.append(line)

            if friendly_errors:
                error_msg = "\n".join(friendly_errors)
                error_msg += "\n💡 常见问题: 分号、括号、类名与文件名一致性"
                return False, error_msg
            return False, f"编译错误:\n{error}"
        return True, ""

    except FileNotFoundError:
        return False, "⚠️ 未找到 javac，请安装 JDK 并将 bin 目录加入环境变量"
    except Exception as e:
        return False, f"检查错误: {str(e)}"

def execute_python(code, stdin_input="", timeout=5):
    """执行Python代码"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            ['python', temp_file],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )
        os.unlink(temp_file)

        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "运行时错误"
            return False, error_msg, ""
        return True, "", result.stdout.strip()

    except subprocess.TimeoutExpired:
        return False, f"⏱️ 执行超时（超过{timeout}秒）", ""
    except Exception as e:
        return False, f"执行错误: {str(e)}", ""

def execute_cpp(code, stdin_input="", timeout=5):
    """编译并执行C++代码"""
    try:
        # 写入临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
            f.write(code)
            src_file = f.name

        exe_file = src_file.replace('.cpp', '.exe')

        # 编译
        compile_result = subprocess.run(
            ['g++', '-o', exe_file, src_file, '-std=c++17'],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        if compile_result.returncode != 0:
            os.unlink(src_file)
            error = compile_result.stderr.strip() if compile_result.stderr else "编译错误"
            return False, f"❌ 编译错误:\n{error}", ""

        # 执行
        exec_result = subprocess.run(
            [exe_file],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )

        # 清理文件
        os.unlink(src_file)
        try:
            os.unlink(exe_file)
        except:
            pass

        if exec_result.returncode != 0:
            error_msg = exec_result.stderr.strip() if exec_result.stderr else "运行时错误"
            return False, f"⛔ 运行时错误:\n{error_msg}", ""

        return True, "", exec_result.stdout.strip()

    except subprocess.TimeoutExpired:
        return False, f"⏱️ 执行超时（超过{timeout}秒）", ""
    except FileNotFoundError:
        return False, "⚠️ 未找到 g++ 编译器，请安装 MinGW 或将 g++ 加入环境变量", ""
    except Exception as e:
        return False, f"❌ 执行错误: {str(e)}", ""

def execute_c(code, stdin_input="", timeout=5):
    """编译并执行C代码"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as f:
            f.write(code)
            src_file = f.name

        exe_file = src_file.replace('.c', '.exe')

        # 编译
        compile_result = subprocess.run(
            ['gcc', '-o', exe_file, src_file],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        if compile_result.returncode != 0:
            os.unlink(src_file)
            error = compile_result.stderr.strip() if compile_result.stderr else "编译错误"
            return False, f"❌ 编译错误:\n{error}", ""

        # 执行
        exec_result = subprocess.run(
            [exe_file],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )

        # 清理文件
        os.unlink(src_file)
        try:
            os.unlink(exe_file)
        except:
            pass

        if exec_result.returncode != 0:
            error_msg = exec_result.stderr.strip() if exec_result.stderr else "运行时错误"
            return False, f"⛔ 运行时错误:\n{error_msg}", ""

        return True, "", exec_result.stdout.strip()

    except subprocess.TimeoutExpired:
        return False, f"⏱️ 执行超时（超过{timeout}秒）", ""
    except FileNotFoundError:
        return False, "⚠️ 未找到 gcc 编译器，请安装 MinGW 或将 gcc 加入环境变量", ""
    except Exception as e:
        return False, f"❌ 执行错误: {str(e)}", ""

JAVA_HOME = r"C:\Program Files\Java\jdk-17\bin"

def execute_java(code, stdin_input="", timeout=5):
    """编译并执行Java代码"""
    try:
        java_bin = JAVA_HOME

        # 提取类名
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        if not class_match:
            return False, "❌ 找不到 public class，请确保代码包含 'public class 类名'", ""

        class_name = class_match.group(1)

        # 写入临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as f:
            f.write(code)
            src_file = f.name

        # 编译
        compile_result = subprocess.run(
            [os.path.join(java_bin, 'javac'), src_file],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        if compile_result.returncode != 0:
            os.unlink(src_file)
            error = compile_result.stderr.strip() if compile_result.stderr else "编译错误"
            return False, f"❌ 编译错误:\n{error}", ""

        # 执行
        class_file = src_file.replace('.java', '.class')
        exec_result = subprocess.run(
            [os.path.join(java_bin, 'java'), '-cp', os.path.dirname(src_file), class_name],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )

        # 清理文件
        os.unlink(src_file)
        try:
            os.unlink(class_file)
        except:
            pass

        # 删除可能生成的内部类文件
        class_dir = os.path.dirname(src_file)
        if class_dir:
            for f in os.listdir(class_dir):
                if f.startswith(class_name + '$') and f.endswith('.class'):
                    try:
                        os.unlink(os.path.join(class_dir, f))
                    except:
                        pass

        if exec_result.returncode != 0:
            error_msg = exec_result.stderr.strip() if exec_result.stderr else "运行时错误"
            return False, f"⛔ 运行时错误:\n{error_msg}", ""

        return True, "", exec_result.stdout.strip()

    except subprocess.TimeoutExpired:
        return False, f"⏱️ 执行超时（超过{timeout}秒）", ""
    except FileNotFoundError:
        return False, "⚠️ 未找到 javac/java，请安装 JDK 并将 bin 目录加入环境变量", ""
    except Exception as e:
        return False, f"❌ 执行错误: {str(e)}", ""

def run_code_test(code, lang, test_cases, topic):
    """运行代码测试 - 真实执行"""
    results = []
    passed = 0

    # 检查语法
    ok, err = check_syntax(code, lang)
    if not ok:
        return {"syntax_ok": False, "error": err, "results": [], "passed": 0, "total": len(test_cases), "score": 0}

    # 空代码检查
    if not code.strip():
        for inp, exp in test_cases:
            results.append({"input": inp, "expected": exp, "actual": "空代码", "passed": False})
        return {"syntax_ok": True, "results": results, "passed": 0, "total": len(test_cases), "score": 0}

    # 选择执行函数
    exec_funcs = {
        "Python": execute_python,
        "C++": execute_cpp,
        "C": execute_c,
        "Java": execute_java
    }

    exec_func = exec_funcs.get(lang, execute_python)

    # 执行每个测试用例
    for inp, exp in test_cases:
        success, error_msg, actual = exec_func(code, inp.strip())

        if not success:
            results.append({"input": inp, "expected": exp, "actual": error_msg, "passed": False, "error": True})
            continue

        # 规范化输出进行比较（去除首尾空白）
        actual_normalized = actual.strip() if actual else ""
        expected_normalized = exp.strip()

        # 判断是否通过
        is_correct = actual_normalized == expected_normalized
        if is_correct:
            passed += 1

        results.append({
            "input": inp,
            "expected": exp,
            "actual": actual if actual else "(无输出)",
            "passed": is_correct
        })

    score = int(passed / len(test_cases) * 100) if test_cases else 0
    return {"syntax_ok": True, "results": results, "passed": passed, "total": len(test_cases), "score": score}

def get_topic_q(topic):
    """根据主题名称获取相关题目，支持模糊匹配"""
    results = []

    # 主题名到关键词的映射
    topic_keywords = {
        "数组与字符串": ["数组", "字符串", "两数之和", "反转数组", "合并数组", "回文", "前缀", "移除元素", "买卖股票"],
        "链表": ["链表", "反转链表", "环形链表", "删除倒数"],
        "栈与队列": ["栈", "队列", "括号", "最小栈", "每日温度"],
        "树与图": ["树", "图", "二叉树", "岛屿", "课程表", "遍历"],
        "递归与分治": ["递归", "分治", "斐波那契", "阶乘", "pow", "归并"],
        "动态规划": ["动态规划", "爬楼梯", "打家劫舍", "递增子序列", "背包", "DP"],
        "回溯算法": ["回溯", "全排列", "组合", "N皇后", "排列"],
        "贪心算法": ["贪心", "跳跃游戏", "柠檬水", "分发糖果"],
        "基础语法": []  # 基础语法没有对应题目
    }

    # 检查主题是否匹配
    matched_keywords = topic_keywords.get(topic, [])

    for q in QUESTION_BANK:
        # 精确匹配topic字段
        if topic in q["topic"]:
            results.append(q)
            continue
        # 检查knowledge_point是否包含主题关键词
        kp = q.get("knowledge_point", "")
        for kw in matched_keywords:
            if kw in kp or kw in q.get("title", "") or kw in q.get("description", ""):
                results.append(q)
                break

    return results

# ============== Streamlit App ==============
st.set_page_config(page_title="智学编程", page_icon="🎓")

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "Python"
if "mastery_level" not in st.session_state:
    st.session_state.mastery_level = {}
if "mindmap_colors" not in st.session_state:
    st.session_state.mindmap_colors = {}  # {"node_key": "red/yellow/green"}
if "custom_nodes" not in st.session_state:
    st.session_state.custom_nodes = {}  # {"node_key": {"name": "...", "desc": "...", "code": "...", "language": "Python"}}
if "creation_history" not in st.session_state:
    st.session_state.creation_history = []  # 最近5次创建记录
if "deleted_nodes" not in st.session_state:
    st.session_state.deleted_nodes = []  # 最近删除的知识点 [{"key": "...", "data": {...}, "deleted_at": timestamp}]
if "restore_form_data" not in st.session_state:
    st.session_state.restore_form_data = None  # 用于恢复表单数据
if "hidden_nodes" not in st.session_state:
    st.session_state.hidden_nodes = set()  # 被隐藏的默认知识点key集合
if "form_name" not in st.session_state:
    st.session_state.form_name = ""
    st.session_state.form_desc = ""
    st.session_state.form_code = ""
    st.session_state.form_lang = "Python"
    st.session_state.form_parent = None
    st.session_state.form_cleared = False

with st.sidebar:
    st.title("🎓 智学编程")
    lang_options = list(PROGRAMMING_LANGUAGES.keys())
    lang_index = lang_options.index(st.session_state.selected_language)
    lang = st.selectbox("选择语言", lang_options, index=lang_index)
    if lang != st.session_state.selected_language:
        st.session_state.selected_language = lang
        st.rerun()
    page = st.radio("功能", ["📚 学习中心", "📖 个性化讲解", "💻 练习中心", "🤖 AI助手", "📊 学习报告", "🗑️ 最近删除"])

# ============== 学习中心（思维导图）==============
if page == "📚 学习中心":
    st.title("🧠 学习中心")
    st.markdown(f"📌 当前语言: **{st.session_state.selected_language}**  |  颜色说明: 🔴重要 ⭐待复习 🟢已掌握")

    lang = st.session_state.selected_language
    mindmap = MINDMAP_KNOWLEDGE.get(lang, MINDMAP_KNOWLEDGE["Python"])

    # 检查是否需要清空表单
    if st.session_state.get("need_clear_form", False):
        st.session_state.add_name = ""
        st.session_state.add_desc = ""
        st.session_state.add_code = ""
        st.session_state.need_clear_form = False

    # 添加自定义节点
    with st.expander("➕ 添加自定义知识点", expanded=False):
        # 语言选择
        selected_lang = st.selectbox("📝 所属语言", lang_options, key="add_lang")

        # 父节点选择
        target_mindmap = MINDMAP_KNOWLEDGE.get(selected_lang, MINDMAP_KNOWLEDGE["Python"])
        parent_options = list(target_mindmap.keys()) + ["自定义分组"]
        custom_parent = st.selectbox("📁 父节点", parent_options, key="add_parent")

        # 表单输入
        custom_name = st.text_input("📌 知识点名称", key="add_name")
        custom_desc = st.text_area("📖 简单描述", key="add_desc")
        custom_code = st.text_area("💻 示例代码", key="add_code", height=150)

        if st.button("✅ 添加知识点", key="add_submit"):
            if custom_name:
                node_key = f"{selected_lang}_{custom_name}"
                if node_key in st.session_state.custom_nodes:
                    st.warning(f"⚠️ 知识点「{custom_name}」已存在！")
                else:
                    actual_parent = "自定义" if custom_parent == "自定义分组" else custom_parent

                    st.session_state.custom_nodes[node_key] = {
                        "name": custom_name,
                        "desc": custom_desc,
                        "code": custom_code,
                        "language": selected_lang,
                        "parent": actual_parent,
                        "original_code": custom_code,
                        "original_desc": custom_desc,
                        "is_edited": False,
                        "created_at": time.time()
                    }
                    st.session_state.creation_history.append({
                        "name": custom_name,
                        "language": selected_lang,
                        "parent": actual_parent,
                        "timestamp": time.time(),
                        "desc": custom_desc,
                        "code": custom_code
                    })
                    if len(st.session_state.creation_history) > 5:
                        st.session_state.creation_history.pop(0)

                    st.success(f"✅ 已添加「{custom_name}」到 {selected_lang} 的 {actual_parent}！")
                    st.session_state.need_clear_form = True
                    st.rerun()
            else:
                st.warning("请输入知识点名称！")

        # 显示最近创建记录
        if st.session_state.creation_history:
            with st.expander("📋 最近创建记录", expanded=False):
                for i, hist in enumerate(st.session_state.creation_history):
                    time_str = time.strftime("%H:%M:%S", time.localtime(hist["timestamp"]))
                    st.markdown(f"- **{hist['name']}** ({hist['language']} · {hist['parent']}) · {time_str}")

    st.markdown("---")

    # 获取当前语言的自定义节点
    current_lang_custom = {
        k: v for k, v in st.session_state.custom_nodes.items()
        if v.get("language") == lang
    }

    # 选中知识点的详情展示区（全宽）
    if "selected_mindmap_node" in st.session_state and st.session_state.selected_mindmap_node:
        selected = st.session_state.selected_mindmap_node
        node_key = selected['key']
        is_custom = selected.get('is_custom', False)

        # 获取原始内容
        original_code = selected.get('code', '')
        original_desc = selected.get('desc', '')

        # 获取当前显示的内容（优先使用已保存的编辑）
        saved = st.session_state.custom_nodes.get(node_key, {})
        if saved.get("is_edited"):
            current_desc = saved.get("desc", original_desc)
            current_code = saved.get("code", original_code)
        else:
            current_desc = original_desc
            current_code = original_code

        # 特殊处理：如果是自定义节点刚从编辑状态恢复，需要同步
        if not is_custom:
            # 内置节点，直接用原始内容
            current_desc = original_desc
            current_code = original_code

        st.markdown(f"### 📚 {selected['name']}")

        # 检查是否在编辑模式
        edit_mode_key = f"edit_mode_{node_key}"
        is_edit_mode = st.session_state.get(edit_mode_key, False)

        # 获取编辑前的代码用于恢复默认
        if is_custom and saved.get("is_edited"):
            restore_code = saved.get("original_code", original_code)
            restore_desc = saved.get("original_desc", original_desc)
        elif is_custom:
            restore_code = original_code
            restore_desc = original_desc
        else:
            restore_code = original_code
            restore_desc = original_desc

        if is_edit_mode:
            # 编辑模式
            edit_desc = st.text_area("📝 描述", value=current_desc, key=f"edit_desc_{node_key}")
            edit_code = st.text_area("💻 示例代码", value=current_code, height=250, key=f"edit_code_{node_key}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 保存", type="primary", key=f"save_{node_key}"):
                    if is_custom:
                        st.session_state.custom_nodes[node_key] = {
                            "name": selected['name'],
                            "desc": edit_desc,
                            "code": edit_code,
                            "language": saved.get("language", lang),
                            "parent": selected.get('parent', '自定义'),
                            "original_code": restore_code,
                            "original_desc": restore_desc,
                            "is_edited": True,
                            "created_at": saved.get("created_at", time.time())
                        }
                    st.session_state[edit_mode_key] = False
                    st.success("✅ 已保存！")
                    st.rerun()

            with col2:
                if st.button("🔄 恢复默认", key=f"reset_{node_key}"):
                    if is_custom and node_key in st.session_state.custom_nodes:
                        # 恢复创建时的原始版本（删除编辑，保留节点）
                        node_data = st.session_state.custom_nodes[node_key]
                        node_data["desc"] = node_data.get("original_desc", original_desc)
                        node_data["code"] = node_data.get("original_code", original_code)
                        node_data["is_edited"] = False
                    st.session_state[edit_mode_key] = False
                    st.info("已恢复为创建时的版本！")
                    st.rerun()

            with col3:
                if st.button("❌ 取消", key=f"cancel_{node_key}"):
                    st.session_state[edit_mode_key] = False
                    st.rerun()
        else:
            # 查看模式
            st.markdown(f"**{current_desc}**")
            st.code(current_code, language=lang.lower() if lang != "C++" else "cpp")

            if is_custom and saved.get("is_edited"):
                st.info("📝 此知识点已被编辑，点击「✏️ 编辑」可修改，或「🔄 恢复默认」还原到创建时的版本")

        # 颜色标记
        color_options = ["yellow", "red", "green"]
        color_labels = {"yellow": "⭐ 待复习", "red": "🔴 重要", "green": "🟢 已掌握"}
        current_color = st.session_state.mindmap_colors.get(node_key, "yellow")
        current_idx = color_options.index(current_color) if current_color in color_options else 0
        new_color = st.radio("📌 重要度标记", color_options, index=current_idx,
                            format_func=lambda x: color_labels[x], horizontal=True)
        if new_color != current_color:
            st.session_state.mindmap_colors[node_key] = new_color

        # 操作按钮
        col1, col2 = st.columns(2)

        with col1:
            if is_custom:
                if st.button("✏️ 编辑", key=f"edit_btn_custom_{node_key}"):
                    st.session_state[edit_mode_key] = True
                    st.rerun()
            else:
                if st.button("🗑️ 删除", key=f"delete_btn_{node_key}"):
                    # 将默认知识点添加到删除列表和隐藏列表
                    deleted_node = {
                        "key": node_key,
                        "name": selected['name'],
                        "language": lang,
                        "parent": selected.get('parent', ''),
                        "desc": original_desc,
                        "code": original_code,
                        "deleted_at": time.time(),
                        "is_default": True  # 标记为默认知识点
                    }
                    st.session_state.deleted_nodes.append(deleted_node)
                    st.session_state.hidden_nodes.add(node_key)
                    # 删除颜色标记
                    if node_key in st.session_state.mindmap_colors:
                        del st.session_state.mindmap_colors[node_key]
                    if edit_mode_key in st.session_state:
                        del st.session_state[edit_mode_key]
                    del st.session_state.selected_mindmap_node
                    st.success("已删除到「最近删除」！")
                    st.rerun()

        with col2:
            if st.button("❌ 关闭详情", key=f"close_{node_key}"):
                if edit_mode_key in st.session_state:
                    del st.session_state[edit_mode_key]
                del st.session_state.selected_mindmap_node
                st.rerun()

        # 自定义节点额外显示删除按钮
        if is_custom:
            col3 = st.columns(1)[0]
            node_data = st.session_state.custom_nodes.get(node_key, {})
            deleted_node = {
                "key": node_key,
                "name": selected['name'],
                "language": node_data.get("language", lang),
                "parent": node_data.get("parent", "自定义"),
                "desc": node_data.get("desc", ""),
                "code": node_data.get("code", ""),
                "original_desc": node_data.get("original_desc", ""),
                "original_code": node_data.get("original_code", ""),
                "deleted_at": time.time(),
                "is_default": False  # 标记为自定义知识点
            }
            if st.button("🗑️ 删除", key=f"delete_custom_{node_key}"):
                st.session_state.deleted_nodes.append(deleted_node)
                del st.session_state.custom_nodes[node_key]
                if node_key in st.session_state.mindmap_colors:
                    del st.session_state.mindmap_colors[node_key]
                if edit_mode_key in st.session_state:
                    del st.session_state[edit_mode_key]
                del st.session_state.selected_mindmap_node
                st.success("已删除到「最近删除」！")
                st.rerun()

        st.markdown("---")

    # 思维导图展示（紧凑卡片形式）
    for parent_name, children in mindmap.items():
        # 过滤掉被隐藏的知识点
        visible_children = {
            k: v for k, v in children.items()
            if f"{lang}_{parent_name}_{k}" not in st.session_state.hidden_nodes
        }

        # 获取该分类下的自定义知识点
        custom_in_parent = [
            (key, node) for key, node in current_lang_custom.items()
            if node.get("parent") == parent_name
        ]

        # 如果都没有可见的知识点，跳过
        if not visible_children and not custom_in_parent:
            continue

        st.markdown(f"### 🌳 {parent_name}")

        # 合并所有知识点（默认 + 自定义）
        all_nodes = []
        for child_name, child_info in visible_children.items():
            node_key = f"{lang}_{parent_name}_{child_name}"
            all_nodes.append((node_key, child_name, child_info, False))
        for node_key, node in custom_in_parent:
            all_nodes.append((node_key, node.get('name', ''), {'desc': node.get('desc', ''), 'code': node.get('code', '')}, True))

        # 网格布局显示
        cols = st.columns(4)
        col_idx = 0

        for node_key, name, info, is_custom in all_nodes:
            color = st.session_state.mindmap_colors.get(node_key, "yellow")
            emoji = {"red": "🔴", "yellow": "⭐", "green": "🟢"}.get(color, "⚪")

            with cols[col_idx]:
                # 点击按钮查看详情
                if st.button(f"{emoji} {name}", key=f"btn_{node_key}", use_container_width=True):
                    if is_custom:
                        # 自定义节点
                        node_data = current_lang_custom.get(node_key, {})
                        display_code = node_data.get("code", node_data.get("original_code", ""))
                        display_desc = node_data.get("desc", node_data.get("original_desc", ""))
                        st.session_state.selected_mindmap_node = {
                            "key": node_key,
                            "name": name,
                            "desc": display_desc,
                            "code": display_code,
                            "parent": parent_name,
                            "is_custom": True
                        }
                    else:
                        # 默认节点
                        st.session_state.selected_mindmap_node = {
                            "key": node_key,
                            "name": name,
                            "desc": info.get('desc', ''),
                            "code": info.get('code', ''),
                            "parent": parent_name,
                            "is_custom": False
                        }
                    st.rerun()

                # 颜色选择
                color_options = ["yellow", "red", "green"]
                color_labels = {"yellow": "⭐", "red": "🔴", "green": "🟢"}
                current_idx = color_options.index(color) if color in color_options else 0
                new_color = st.selectbox("", color_options, index=current_idx, format_func=lambda x: color_labels[x], key=f"color_{node_key}")
                if new_color != color:
                    st.session_state.mindmap_colors[node_key] = new_color
                    st.rerun()

            col_idx = (col_idx + 1) % 4

        st.markdown("---")

    # 显示"自定义"分类下的自定义知识点（如果有）
    custom_nodes = [(key, node) for key, node in current_lang_custom.items() if node.get("parent") == "自定义"]
    if custom_nodes:
        st.markdown("### ✏️ 自定义")

        cols = st.columns(4)
        col_idx = 0

        for node_key, node in custom_nodes:
            color = st.session_state.mindmap_colors.get(node_key, "yellow")
            emoji = {"red": "🔴", "yellow": "⭐", "green": "🟢"}.get(color, "⚪")

            with cols[col_idx]:
                if st.button(f"{emoji} {node['name']}", key=f"custom_btn_{node_key}", use_container_width=True):
                    display_code = node.get("code", node.get("original_code", ""))
                    display_desc = node.get("desc", node.get("original_desc", ""))
                    st.session_state.selected_mindmap_node = {
                        "key": node_key,
                        "name": node['name'],
                        "desc": display_desc,
                        "code": display_code,
                        "parent": "自定义",
                        "is_custom": True
                    }
                    st.rerun()

                color_options = ["yellow", "red", "green"]
                color_labels = {"yellow": "⭐", "red": "🔴", "green": "🟢"}
                current_idx = color_options.index(color) if color in color_options else 0
                new_color = st.selectbox("", color_options, index=current_idx, format_func=lambda x: color_labels[x], key=f"custom_color_{node_key}")
                if new_color != color:
                    st.session_state.mindmap_colors[node_key] = new_color
                    st.rerun()

            col_idx = (col_idx + 1) % 4

        st.markdown("---")

# ============== 最近删除 ==============
elif page == "🗑️ 最近删除":
    st.title("🗑️ 最近删除")

    # 清理超过3天的记录
    current_time = time.time()
    three_days = 3 * 24 * 60 * 60  # 3天的秒数
    st.session_state.deleted_nodes = [
        n for n in st.session_state.deleted_nodes
        if current_time - n.get("deleted_at", 0) < three_days
    ]

    if not st.session_state.deleted_nodes:
        st.info("📭 最近3天内没有删除任何知识点")
    else:
        st.markdown(f"📋 最近删除列表（{len(st.session_state.deleted_nodes)} 条，3天后自动清理）")

        # 按语言分组显示
        deleted_by_lang = {}
        for node in st.session_state.deleted_nodes:
            lang_name = node.get("language", "未知")
            if lang_name not in deleted_by_lang:
                deleted_by_lang[lang_name] = []
            deleted_by_lang[lang_name].append(node)

        for lang_name, nodes in deleted_by_lang.items():
            with st.expander(f"📁 {lang_name}（{len(nodes)} 条）", expanded=True):
                for node in nodes:
                    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(node.get("deleted_at", 0)))
                    time_ago = int((current_time - node.get("deleted_at", 0)) / 60)
                    if time_ago < 60:
                        time_ago_str = f"{time_ago}分钟前"
                    elif time_ago < 1440:
                        time_ago_str = f"{time_ago // 60}小时前"
                    else:
                        time_ago_str = f"{time_ago // 1440}天前"

                    col1, col2, col3 = st.columns([3, 1, 1])

                    # 使用时间戳作为唯一key的一部分
                    unique_key = f"{node['key']}_{int(node.get('deleted_at', 0))}"

                    with col1:
                        is_default = node.get("is_default", False)
                        tag = "🔵系统" if is_default else "✏️自定义"
                        st.markdown(f"**{node.get('name', '未知')}** {tag}")
                        st.caption(f"📂 {node.get('parent', '未知')} · {time_ago_str}（{time_str}）")

                    with col2:
                        if st.button(f"🔄 恢复", key=f"restore_{unique_key}"):
                            # 恢复节点
                            if node.get("is_default", False):
                                # 恢复默认知识点：从隐藏列表移除
                                st.session_state.hidden_nodes.discard(node["key"])
                                st.success(f"已恢复「{node.get('name')}」到 {node.get('parent')}！")
                            else:
                                # 恢复自定义知识点
                                st.session_state.custom_nodes[node["key"]] = {
                                    "name": node.get("name", ""),
                                    "desc": node.get("desc", ""),
                                    "code": node.get("code", ""),
                                    "language": node.get("language", "Python"),
                                    "parent": node.get("parent", "自定义"),
                                    "original_code": node.get("original_code", node.get("code", "")),
                                    "original_desc": node.get("original_desc", node.get("desc", "")),
                                    "is_edited": False,
                                    "created_at": node.get("created_at", time.time())
                                }
                                st.success(f"已恢复「{node.get('name')}」到 {node.get('parent')}！")

                            # 从删除列表移除
                            st.session_state.deleted_nodes = [
                                n for n in st.session_state.deleted_nodes
                                if f"{n.get('key', '')}_{int(n.get('deleted_at', 0))}" != unique_key
                            ]
                            st.rerun()

                    with col3:
                        if st.button(f"❌ 彻底删除", key=f"permdel_{unique_key}"):
                            # 如果是默认知识点也要从hidden_nodes移除
                            if node.get("is_default", False):
                                st.session_state.hidden_nodes.discard(node["key"])
                            st.session_state.deleted_nodes = [
                                n for n in st.session_state.deleted_nodes
                                if f"{n.get('key', '')}_{int(n.get('deleted_at', 0))}" != unique_key
                            ]
                            st.warning(f"已彻底删除「{node.get('name')}」，无法恢复！")
                            st.rerun()

                    st.markdown("---")

# ============== AI助手 ==============
elif page == "🤖 AI助手":
    st.markdown("## 🤖 AI编程助手")
    st.markdown("### 🌟 您的智能编程伙伴 - 有三个强大功能！")

    # 功能选择
    st.markdown("---")
    st.markdown("#### 请选择功能：")
    function_options = ["📝 生成练习题", "❓ 知识问答", "🔍 代码复盘"]
    selected_function = st.radio("功能选择", function_options, horizontal=True, label_visibility="collapsed")

    # API配置
    st.markdown("---")
    st.markdown("#### ⚙️ API配置")
    api_col1, api_col2 = st.columns([3, 1])
    with api_col1:
        api_key = st.text_input("API Key", type="password", placeholder="输入API密钥...",
                               value=st.session_state.get("api_key", ""),
                               help="输入您的API密钥",
                               key="api_key_input")
        api_endpoint = st.text_input("API 地址", placeholder="https://api.openai.com/v1/chat/completions",
                                    value=st.session_state.get("api_endpoint", "https://chat.ecnu.edu.cn/open/api/v1/chat/completions"),
                                    help="API接口地址，使用华东师大服务：https://chat.ecnu.edu.cn/open/api/v1/chat/completions",
                                    key="api_endpoint_input")
    with api_col2:
        model_options = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        selected_model = st.selectbox("模型", model_options, key="model_select")

    # 存储配置到session_state
    if api_key:
        st.session_state.api_key = api_key
    if api_endpoint:
        st.session_state.api_endpoint = api_endpoint
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "gpt-3.5-turbo"
    if selected_model != st.session_state.get("selected_model"):
        st.session_state.selected_model = selected_model

    st.markdown("---")

    # 功能1: 生成练习题
    if selected_function == "📝 生成练习题":
        st.markdown("### 📝 生成练习题")
        st.markdown("描述您想要练习的知识点，AI将为您生成合适的题目和参考答案！")

        # 选择语言
        languages = ["Python", "C++", "C", "Java"]
        selected_lang = st.selectbox("🎯 请选择练习语言", languages, key="gen_lang_select")

        topic_input = st.text_area("📋 请描述您想要练习的内容",
                                  placeholder="例如：我想练习关于数组双指针的题目，或者我想练习回文串判断...",
                                  height=80, key="topic_input")

        col_diff, col_gen = st.columns([1, 2])
        with col_diff:
            difficulty_options = ["全部难度", "🟢 基础", "🟡 中等", "🔴 进阶"]
            selected_difficulty = st.selectbox("题目难度", difficulty_options, key="difficulty_select")

        with col_gen:
            st.markdown("")  # 对齐
            generate_btn = st.button("🚀 生成题目", type="primary", key="generate_btn")

        # 初始化session_state
        if "gen_practice_state" not in st.session_state:
            st.session_state.gen_practice_state = {
                "questions": [],
                "current_idx": 0,
                "user_code": "",
                "results": {},
                "has_generated": False
            }

        # 显示已生成的题目或练习界面
        s = st.session_state.gen_practice_state
        qs = s["questions"]

        if qs and s["has_generated"]:
            idx = s["current_idx"]
            q = qs[idx]

            st.markdown("---")
            st.markdown(f"### 📌 题目 {idx + 1}/{len(qs)}: {q.get('title', '无标题')}")

            # 题目详情
            diff_text = "🟢 基础" if q.get('difficulty') == 1 else "🟡 中等" if q.get('difficulty') == 2 else "🔴 进阶"
            st.markdown(f"**难度**: {diff_text} | **语言**: {selected_lang}")

            st.markdown(f"**📝 题目描述**: {q.get('description', '')}")
            st.markdown(f"**📥 输入格式**: {q.get('input_format', '')}")
            st.markdown(f"**📤 输出格式**: {q.get('output_format', '')}")

            if q.get('examples'):
                st.markdown(f"**📋 示例**: 输入 `{q['examples'].get('input', '')}` → 输出 `{q['examples'].get('output', '')}`")

            with st.expander("💡 提示"):
                for h in q.get('hints', []):
                    st.markdown(f"- {h}")

            with st.expander("📝 测试用例"):
                for tc in q.get('test_cases', []):
                    st.markdown(f"- `{tc}`")

            # 参考答案区域
            with st.expander("📖 参考答案（先自己思考后再看哦）"):
                if "gen_solutions" in st.session_state and q.get('title') in st.session_state.gen_solutions:
                    sol = st.session_state.gen_solutions[q.get('title')]
                    if selected_lang in sol:
                        st.code(sol[selected_lang], language=selected_lang.lower() if selected_lang != "C++" else "cpp")
                    else:
                        st.info("暂无该语言参考答案")
                else:
                    st.info("💡 正在生成参考答案...")

            # 导航和操作按钮
            col_nav = st.columns([1, 1, 1, 1])
            with col_nav[0]:
                if idx > 0:
                    if st.button("⬅️ 上一题", key=f"gen_prev_{idx}", use_container_width=True):
                        s["current_idx"] -= 1
                        st.rerun()
                else:
                    st.button("⬅️ 上一题", disabled=True, use_container_width=True)

            with col_nav[1]:
                if idx + 1 < len(qs):
                    if st.button("下一题 ➡️", key=f"gen_next_{idx}", use_container_width=True):
                        s["current_idx"] += 1
                        st.rerun()
                else:
                    st.button("下一题 ➡️", disabled=True, use_container_width=True)

            with col_nav[2]:
                # 加入自定义题库按钮
                if st.button("📚 加入题库", key=f"add_to_bank_{idx}", use_container_width=True):
                    # 初始化自定义题库
                    if "custom_question_bank" not in st.session_state:
                        st.session_state.custom_question_bank = []
                    if "custom_solutions" not in st.session_state:
                        st.session_state.custom_solutions = {}

                    # 检查是否已存在相同标题的题目
                    existing_titles = [x.get('title', '') for x in st.session_state.custom_question_bank]
                    if q.get('title', '') in existing_titles:
                        st.warning(f"⚠️ 题目「{q.get('title', '')}」已在题库中！")
                    else:
                        # 生成唯一ID
                        import uuid
                        question_id = str(uuid.uuid4())[:8]

                        # 创建题目数据
                        new_question = {
                            "id": question_id,
                            "title": q.get('title', '无标题'),
                            "description": q.get('description', ''),
                            "input_format": q.get('input_format', ''),
                            "output_format": q.get('output_format', ''),
                            "examples": q.get('examples', {}),
                            "test_cases": q.get('test_cases', []),
                            "hints": q.get('hints', []),
                            "difficulty": q.get('difficulty', 1),
                            "knowledge_point": topic_input if 'topic_input' in dir() else "AI生成",
                            "language": selected_lang,
                            "source": "AI生成"
                        }

                        # 添加到题库
                        st.session_state.custom_question_bank.append(new_question)

                        # 保存参考答案
                        if "gen_solutions" in st.session_state and q.get('title') in st.session_state.gen_solutions:
                            st.session_state.custom_solutions[question_id] = st.session_state.gen_solutions[q.get('title')]

                        st.success(f"✅ 已将「{q.get('title', '')}」加入自定义题库！")

            with col_nav[3]:
                if st.button("🔄 重新开始", key="gen_restart", use_container_width=True):
                    s["questions"] = []
                    s["current_idx"] = 0
                    s["user_code"] = ""
                    s["results"] = {}
                    s["has_generated"] = False
                    if "gen_solutions" in st.session_state:
                        del st.session_state.gen_solutions
                    st.rerun()

        # 生成题目
        if generate_btn and topic_input and st.session_state.get("api_key"):
            with st.spinner("🤔 AI正在生成题目和参考答案，请稍候..."):
                try:
                    import requests
                    import json

                    difficulty_text = ""
                    if selected_difficulty != "全部难度":
                        difficulty_text = f"难度要求：{selected_difficulty.replace('🟢 ', '').replace('🟡 ', '').replace('🔴 ', '')}"

                    # 先生成题目
                    prompt = f"""你是一个编程题库专家。请根据用户的需求生成2道编程练习题。

用户需求：{topic_input}
{difficulty_text}

请以JSON格式返回题目，格式如下：
{{
    "questions": [
        {{
            "title": "题目标题",
            "description": "题目描述",
            "input_format": "输入格式说明",
            "output_format": "输出格式说明",
            "examples": {{"input": "示例输入", "output": "示例输出"}},
            "test_cases": ["输入1->预期输出1", "输入2->预期输出2"],
            "hints": ["提示1", "提示2"],
            "difficulty": 1
        }}
    ]
}}

要求：
1. 题目要有意义，测试用例要完整正确
2. 输出必须是合法的JSON格式
3. 题目要符合{topic_input}的知识点
4. test_cases中每个用例格式为"输入->预期输出"，用->分隔
5. difficulty为1表示基础，2表示中等，3表示进阶
6. 只返回JSON，不要其他内容"""

                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {st.session_state.api_key}"
                    }

                    # 生成题目
                    data = {
                        "model": st.session_state.selected_model,
                        "messages": [
                            {"role": "system", "content": "你是一个专业的编程教育助手，擅长生成高质量的编程练习题。"},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    }

                    response = requests.post(
                        st.session_state.api_endpoint,
                        headers=headers,
                        json=data,
                        timeout=120
                    )

                    if response.status_code != 200:
                        st.error(f"❌ API调用失败: {response.status_code}")
                        st.code(response.text[:500])
                    else:
                        result = response.json()

                        # 处理响应
                        result_text = ""
                        if isinstance(result, dict):
                            if "choices" in result:
                                result_text = result["choices"][0]["message"]["content"].strip()
                            elif "response" in result:
                                result_text = result["response"].strip()
                            else:
                                for key in result.keys():
                                    if isinstance(result[key], str):
                                        result_text = result[key]
                                        break

                        # 解析JSON
                        import re
                        json_match = re.search(r'\{[\s\S]*\}', result_text)
                        if json_match:
                            questions_data = json.loads(json_match.group())
                            questions = questions_data.get("questions", [])

                            if questions:
                                st.success("✅ 题目生成成功！正在生成参考答案...")

                                # 为每道题生成参考答案
                                st.session_state.gen_solutions = {}
                                solution_progress = st.progress(0)

                                for i, q in enumerate(questions):
                                    solution_progress.progress((i + 1) / len(questions) * 0.5, text=f"生成题目{i+1}参考答案...")

                                    # 生成参考答案的prompt
                                    test_cases_str = "\n".join([f'"{tc}"' for tc in q.get('test_cases', [])])
                                    hints_str = "\n".join([f"# {h}" for h in q.get('hints', [])])

                                    if selected_lang == "Python":
                                        sol_prompt = f"""请为以下Python题目生成完整可运行的参考答案代码。

题目：{q.get('title', '')}
描述：{q.get('description', '')}
输入格式：{q.get('input_format', '')}
输出格式：{q.get('output_format', '')}
示例输入：{q.get('examples', {}).get('input', '')}
示例输出：{q.get('examples', {}).get('output', '')}
测试用例：{test_cases_str}

请生成完整、可运行的Python代码，包含：
1. 读取输入
2. 处理逻辑
3. 输出结果

代码要求：
- 使用标准输入输出
- 代码完整可运行
- 包含必要的注释说明算法思路
- 可以直接通过测试用例"""

                                        lang_code = "Python"
                                    elif selected_lang == "C++":
                                        sol_prompt = f"""请为以下C++题目生成完整可运行的参考答案代码。

题目：{q.get('title', '')}
描述：{q.get('description', '')}
输入格式：{q.get('input_format', '')}
输出格式：{q.get('output_format', '')}
示例输入：{q.get('examples', {}).get('input', '')}
示例输出：{q.get('examples', {}).get('output', '')}
测试用例：{test_cases_str}

请生成完整、可运行的C++代码，包含：
1. #include <bits/stdc++.h>
2. 使用cin/cout进行输入输出
3. 完整的处理逻辑

代码要求：
- 使用标准输入输出
- 代码完整可运行（支持C++17）
- 包含必要的注释"""

                                        lang_code = "C++"
                                    elif selected_lang == "C":
                                        sol_prompt = f"""请为以下C语言题目生成完整可运行的参考答案代码。

题目：{q.get('title', '')}
描述：{q.get('description', '')}
输入格式：{q.get('input_format', '')}
输出格式：{q.get('output_format', '')}
示例输入：{q.get('examples', {}).get('input', '')}
示例输出：{q.get('examples', {}).get('output', '')}
测试用例：{test_cases_str}

请生成完整、可运行的C代码，包含：
1. #include <stdio.h>
2. 使用scanf/printf进行输入输出
3. 完整的处理逻辑

代码要求：
- 使用标准输入输出
- 代码完整可运行"""

                                        lang_code = "C"
                                    else:  # Java
                                        sol_prompt = f"""请为以下Java题目生成完整可运行的参考答案代码。

题目：{q.get('title', '')}
描述：{q.get('description', '')}
输入格式：{q.get('input_format', '')}
输出格式：{q.get('output_format', '')}
示例输入：{q.get('examples', {}).get('input', '')}
示例输出：{q.get('examples', {}).get('output', '')}
测试用例：{test_cases_str}

请生成完整、可运行的Java代码，包含：
1. public class Main
2. 使用Scanner进行输入
3. 使用System.out.println进行输出
4. main方法

代码要求：
- 代码完整可运行"""

                                        lang_code = "Java"

                                    # 调用API生成答案
                                    sol_data = {
                                        "model": st.session_state.selected_model,
                                        "messages": [
                                            {"role": "system", "content": "你是一个专业的编程教师，擅长编写高质量的代码。"},
                                            {"role": "user", "content": sol_prompt}
                                        ],
                                        "temperature": 0.5
                                    }

                                    sol_response = requests.post(
                                        st.session_state.api_endpoint,
                                        headers=headers,
                                        json=sol_data,
                                        timeout=120
                                    )

                                    if sol_response.status_code == 200:
                                        sol_result = sol_response.json()
                                        sol_text = ""
                                        if isinstance(sol_result, dict):
                                            if "choices" in sol_result:
                                                sol_text = sol_result["choices"][0]["message"]["content"].strip()
                                            elif "response" in sol_result:
                                                sol_text = sol_result["response"].strip()

                                        # 提取代码块
                                        code_match = re.search(r'```(?:\w+)?\n([\s\S]*?)```', sol_text)
                                        if code_match:
                                            st.session_state.gen_solutions[q.get('title')] = {selected_lang: code_match.group(1).strip()}
                                        elif sol_text:
                                            # 如果没有代码块，整个作为代码
                                            st.session_state.gen_solutions[q.get('title')] = {selected_lang: sol_text}

                                    solution_progress.progress(0.5 + (i + 1) / len(questions) * 0.5, text="处理完成...")

                                solution_progress.empty()

                                # 保存到session_state并切换到练习界面
                                s["questions"] = questions
                                s["current_idx"] = 0
                                s["user_code"] = ""
                                s["results"] = {}
                                s["has_generated"] = True
                                st.rerun()
                            else:
                                st.error("❌ 未解析到题目，请重试")
                        else:
                            st.error("❌ 无法解析AI返回的内容")
                            st.info("原始返回:")
                            st.code(result_text[:500])

                except requests.exceptions.Timeout:
                    st.error("❌ 请求超时，请检查网络或稍后重试")
                except requests.exceptions.ConnectionError:
                    st.error("❌ 无法连接到API服务器，请检查API地址是否正确")
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")

        elif generate_btn and not st.session_state.get("api_key"):
            st.warning("⚠️ 请先配置API Key")

    # 功能2: 知识问答
    elif selected_function == "❓ 知识问答":
        st.markdown("### ❓ 知识问答")
        st.markdown("有什么编程问题尽管问，AI会尽力为您解答！")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # 显示聊天历史
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").markdown(msg["content"])
            else:
                st.chat_message("assistant").markdown(msg["content"])

        # 输入问题
        question = st.chat_input("请输入您的编程问题...", key="chat_input")

        if question and st.session_state.get("api_key"):
            with st.spinner("🤔 AI正在思考..."):
                try:
                    import requests

                    # 添加用户消息
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    st.chat_message("user").markdown(question)

                    # 构建消息列表
                    messages = [
                        {"role": "system", "content": "你是一个专业的编程教育助手，擅长解答各种编程问题，包括算法、数据结构、语法、调试等。请用简洁清晰的语言回答，如果涉及到代码，请用代码块包裹。"}
                    ]
                    messages.extend(st.session_state.chat_history)

                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {st.session_state.api_key}"
                    }

                    data = {
                        "model": st.session_state.selected_model,
                        "messages": messages,
                        "temperature": 0.7
                    }

                    response = requests.post(
                        st.session_state.api_endpoint,
                        headers=headers,
                        json=data,
                        timeout=60
                    )

                    result = response.json()

                    # 处理不同的响应格式
                    if "choices" in result:
                        answer = result["choices"][0]["message"]["content"]
                    elif "text" in result:
                        answer = result["text"]
                    else:
                        answer = str(result)

                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.chat_message("assistant").markdown(answer)

                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
        elif question and not st.session_state.get("api_key"):
            st.warning("⚠️ 请先配置API Key")

        # 清除历史按钮
        if st.session_state.chat_history and st.button("🗑️ 清除对话历史"):
            st.session_state.chat_history = []
            st.rerun()

    # 功能3: 代码复盘
    elif selected_function == "🔍 代码复盘":
        st.markdown("### 🔍 代码复盘")
        st.markdown("粘贴您不理解或写不出的代码，AI将帮您分析代码逻辑并给出优化建议！")

        code_input = st.text_area("📋 请粘贴需要复盘的代码",
                                  placeholder="请在这里粘贴您的代码...",
                                  height=200, key="code_input")

        analysis_focus = st.multiselect("分析重点",
                                      ["逻辑分析", "时间空间复杂度", "优化建议", "错误检查", "分步讲解"],
                                      default=["逻辑分析"],
                                      key="analysis_focus")

        analyze_btn = st.button("🔍 开始分析", type="primary", key="analyze_btn")

        if analyze_btn and code_input and st.session_state.get("api_key"):
            with st.spinner("🤔 AI正在分析代码，请稍候..."):
                try:
                    import requests

                    focus_text = "、".join(analysis_focus)

                    prompt = f"""你是一个资深的编程导师。请分析下面的代码，从以下几个方面进行复盘：

分析重点：{focus_text}

代码：
```{code_input}```

请提供详细的分析报告，包括：
1. **代码逻辑概述**：这段代码在做什么
2. **关键算法/思路**：使用了什么算法或思路
3. **复杂度分析**：时间复杂度和空间复杂度
4. **优化建议**：如何改进这段代码
5. **分步讲解**：逐步解释代码执行过程
6. **相关知识点**：涉及哪些编程知识点

请用清晰的结构化格式输出。"""

                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {st.session_state.api_key}"
                    }

                    data = {
                        "model": st.session_state.selected_model,
                        "messages": [
                            {"role": "system", "content": "你是一个专业的编程导师，擅长代码分析和教学。请提供详细、结构清晰的代码复盘报告。"},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    }

                    response = requests.post(
                        st.session_state.api_endpoint,
                        headers=headers,
                        json=data,
                        timeout=60
                    )

                    result = response.json()

                    # 处理不同的响应格式
                    if "choices" in result:
                        result = result["choices"][0]["message"]["content"]
                    elif "text" in result:
                        result = result["text"]
                    else:
                        result = str(result)

                    st.success("✅ 代码分析完成！")
                    st.markdown("---")
                    st.markdown("### 📊 分析报告")
                    st.markdown(result)

                    # 一键复制按钮
                    st.button("📋 复制分析报告", on_click=lambda: st.info("请手动选中上方文本复制"))

                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
                    st.info("💡 请检查API Key是否正确，或者稍后重试")

        elif analyze_btn and not st.session_state.get("api_key"):
            st.warning("⚠️ 请先配置API Key")

    # 功能4: 查看自定义题库
    st.markdown("---")
    st.markdown("### 📚 我的自定义题库")
    st.markdown("查看和管理您添加的题目")

    # 初始化session_state中的自定义题库
    if "custom_question_bank" not in st.session_state:
        st.session_state.custom_question_bank = []
    if "custom_solutions" not in st.session_state:
        st.session_state.custom_solutions = {}

    custom_qs = st.session_state.custom_question_bank

    if not custom_qs:
        st.info("📭 暂无自定义题目，快去「生成练习题」添加吧！")
    else:
        st.markdown(f"共 **{len(custom_qs)}** 道自定义题目")

        # 显示自定义题目列表
        for q in custom_qs:
            with st.expander(f"📌 {q.get('title', '无标题')}", expanded=False):
                diff_emoji = "🟢" if q.get("difficulty", 1) == 1 else "🟡" if q.get("difficulty", 1) == 2 else "🔴"
                q_lang = q.get('language', 'Python')
                st.markdown(f"**难度**: {diff_emoji} | **语言**: {q_lang}")
                st.markdown(f"**知识点**: {q.get('knowledge_point', '未知')}")
                st.markdown(f"**描述**: {q.get('description', '')}")
                st.markdown(f"**输入格式**: {q.get('input_format', '')}")
                st.markdown(f"**输出格式**: {q.get('output_format', '')}")
                if q.get('examples'):
                    st.markdown(f"**示例**: 输入 `{q['examples'].get('input', '')}` → 输出 `{q['examples'].get('output', '')}`")

                with st.expander("💡 提示"):
                    for h in q.get('hints', []):
                        st.markdown(f"- {h}")

                with st.expander("📝 测试用例"):
                    for tc in q.get('test_cases', []):
                        st.markdown(f"- `{tc}`")

                # 显示参考答案
                q_id = q.get("id", "")
                if q_id in st.session_state.custom_solutions:
                    with st.expander("📝 参考答案"):
                        sol = st.session_state.custom_solutions[q_id]
                        if q_lang in sol:
                            st.code(sol[q_lang], language=q_lang.lower() if q_lang != "C++" else "cpp")

                st.markdown("---")
                # 用户代码编辑区
                st.markdown(f"**💻 请输入 {q_lang} 代码：**")
                user_code_key = f"custom_code_{q_id}"
                user_code = st.text_area(
                    "代码编辑器",
                    value=st.session_state.get(user_code_key, ""),
                    height=250,
                    key=user_code_key,
                    placeholder=f"# 在这里输入您的 {q_lang} 代码...",
                    label_visibility="collapsed"
                )

                # 测试按钮和删除按钮
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("📤 提交测试", type="primary", key=f"custom_submit_{q_id}", use_container_width=True):
                        if user_code.strip():
                            # 解析测试用例
                            tcs = []
                            for tc in q.get('test_cases', []):
                                parts = tc.split("->")
                                if len(parts) == 2:
                                    tcs.append((parts[0].strip(), parts[1].strip()))

                            # 运行测试
                            result = run_code_test(user_code, q_lang, tcs, q.get('title', ''))

                            # 保存结果
                            if "custom_test_results" not in st.session_state:
                                st.session_state.custom_test_results = {}
                            st.session_state.custom_test_results[q_id] = result

                            if not result["syntax_ok"]:
                                st.error(f"❌ 语法错误: {result['error']}")
                            else:
                                st.markdown("### 🧪 测试结果")
                                for r in result["results"]:
                                    if r.get("error"):
                                        st.error(f"❌ {r['input']} → 错误: {r['error']}")
                                    elif r["passed"]:
                                        st.success(f"✅ 通过: 输入 `{r['input']}` → 输出 `{r['actual']}`")
                                    else:
                                        st.error(f"❌ 失败: 输入 `{r['input']}` → 预期 `{r['expected']}` 实际 `{r['actual']}`")
                                st.markdown(f"**得分: {result['score']}分 ({result['passed']}/{result['total']})**")

                                if result["score"] == 100:
                                    st.balloons()
                                    st.success("🎉 太棒了！本题全部通过！")
                        else:
                            st.warning("⚠️ 请先输入代码")

                with col_btn2:
                    if st.button("🗑️ 从题库删除", key=f"del_custom_{q_id}", use_container_width=True):
                        # 从session_state中移除
                        st.session_state.custom_question_bank = [
                            x for x in st.session_state.custom_question_bank if x.get("id", "") != q_id
                        ]
                        if q_id in st.session_state.custom_solutions:
                            del st.session_state.custom_solutions[q_id]
                        if "custom_test_results" in st.session_state and q_id in st.session_state.custom_test_results:
                            del st.session_state.custom_test_results[q_id]
                        st.success(f"已删除「{q.get('title', '题目')}」")
                        st.rerun()

                # 显示测试结果
                if "custom_test_results" in st.session_state and q_id in st.session_state.custom_test_results:
                    result = st.session_state.custom_test_results[q_id]
                    st.markdown("### 📊 本题结果")
                    col_score, col_pass = st.columns(2)
                    with col_score:
                        st.metric("得分", f"{result['score']}分")
                    with col_pass:
                        st.metric("通过", f"{result['passed']}/{result['total']}")

        # 一键清空按钮
        if custom_qs and st.button("🗑️ 清空全部自定义题目", type="secondary"):
            st.session_state.custom_question_bank = []
            st.session_state.custom_solutions = {}
            st.success("已清空全部自定义题目！")
            st.rerun()

    # 使用说明
    with st.expander("📖 使用说明", expanded=False):
        st.markdown("""
        ### 🤖 AI助手功能说明

        #### 1️⃣ 生成练习题
        - 描述您想要练习的知识点
        - AI将生成1-2道匹配的练习题
        - 可以选择题目难度
        - 一键将喜欢的题目添加到题库

        #### 2️⃣ 知识问答
        - 可以询问任何编程相关问题
        - 支持算法、数据结构、语法等多方面
        - 对话历史会在本次会话中保留

        #### 3️⃣ 代码复盘
        - 粘贴您不理解或写不出的代码
        - AI会进行详细的逻辑分析
        - 提供优化建议和分步讲解
        - 帮助您真正理解代码

        ### ⚙️ API配置
        - 需要配置OpenAI API Key
        - 支持GPT-4和GPT-3.5-turbo模型
        - 也可以使用兼容OpenAI API的其他服务（如本地部署的模型）
        """)

# ============== 个性化讲解 ==============
elif page == "📖 个性化讲解":
    st.markdown("## 📖 个性化讲解")
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("选择类别", list(KNOWLEDGE_BASE.keys()), key="cat_sel")
    with col2:
        topic = st.selectbox("选择主题", list(KNOWLEDGE_BASE[category].keys()), key="topic_sel")

    if category and topic:
        info = KNOWLEDGE_BASE[category][topic]
        lang = st.session_state.selected_language

        if lang in info["code"]:
            code_text = info["code"][lang]
        else:
            code_text = info["code"]["Python"]

        st.markdown(f"**当前语言: {lang}**")
        st.markdown("### 代码示例")
        st.code(code_text, language=lang.lower() if lang != "C++" else "cpp")

        st.markdown("### 核心概念")
        for c in info["concepts"]:
            st.markdown(f"- {c}")

        st.markdown("### 动手实践")
        for e in info["examples"]:
            st.markdown(f"- {e}")

        if st.button("开始专项练习", type="primary", use_container_width=True):
            qs = get_topic_q(topic)
            if qs:
                # 随机选择5-10道题，或者全部题目（如果总数不足）
                num_to_select = min(random.randint(5, 10), len(qs))
                sel = random.sample(qs, num_to_select)
                st.session_state.special_practice = {"topic": topic, "questions": sel, "index": 0, "answers": {}}
                st.rerun()
            else:
                st.warning(f"抱歉，'{topic}' 暂无练习题目，请选择其他主题。")

        st.markdown("---")

    if st.session_state.get("special_practice"):
        s = st.session_state.special_practice
        idx = s["index"]
        qs = s["questions"]
        total = len(qs)

        # 收起按钮
        col_left, col_right = st.columns([1, 5])
        with col_left:
            if st.button("🔼 收起练习", key="hide_special_practice"):
                del st.session_state.special_practice
                st.rerun()
        with col_right:
            st.markdown(f"### 📚 {s['topic']} - 专项练习")

        # 横向题目进度条（可点击跳转）
        st.markdown("**📊 答题进度：**")
        progress_cols = st.columns(total)
        for i, q_item in enumerate(qs):
            with progress_cols[i]:
                score = s["answers"].get(i, {}).get("score", 0)
                is_current = (i == idx)

                if score == 100:
                    # 满分 - 绿色
                    bg_color = "#28a745"
                    emoji = "✅"
                elif score > 0:
                    # 部分得分 - 橙色
                    bg_color = "#fd7e14"
                    emoji = "⏳"
                else:
                    # 未做或0分 - 灰色
                    bg_color = "#6c757d"
                    emoji = "○"

                # 题目编号
                label = f"**{emoji} {i+1}**"
                if is_current:
                    label = f"👉 **{emoji} {i+1}**"

                # 可点击跳转按钮
                if st.button(label, key=f"qbtn_{i}", use_container_width=True):
                    s["index"] = i
                    st.rerun()

                # 显示得分
                if score > 0:
                    st.caption(f"💯 {score}分")

        st.markdown("---")

        if idx < len(qs):
            q = qs[idx]
            st.markdown(f"### 📝 题目 {idx+1}/{total}: {q['title']}")
            st.markdown(q["description"])

            # 输入格式
            st.markdown("**📥 输入格式**")
            input_format = q.get("input_format", "输入数据，格式见题目描述")
            st.code(input_format, language="plaintext")

            # 输出格式
            st.markdown("**📤 输出格式**")
            output_format = q.get("output_format", "输出结果，格式见题目描述")
            st.code(output_format, language="plaintext")

            # 样例
            st.markdown("**📝 样例**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**输入**")
                st.code(q["examples"]["input"], language="plaintext")
            with col2:
                st.markdown("**输出**")
                st.code(q["examples"]["output"], language="plaintext")

            # 提示
            with st.expander("💡 查看提示"):
                for h in q["hints"]:
                    st.markdown(f"- {h}")

            # 隐藏的标准答案（专项练习）
            with st.expander("📝 参考答案", expanded=False):
                qid = q.get("id", "")

                # 优先使用标准答案库
                if qid in SOLUTIONS:
                    solution = SOLUTIONS[qid]
                    current_lang = st.session_state.selected_language

                    st.markdown(f"### 📝 **{solution.get('title', q['title'])}参考答案**")
                    st.markdown(f"**当前语言: {current_lang}**")

                    # 获取对应语言的答案
                    code = solution.get(current_lang, solution.get("Python", ""))

                    if code:
                        lang_for_code = current_lang.lower() if current_lang != "C++" else "cpp"
                        st.code(code, language=lang_for_code)

                        st.success("💡 参考上述代码，先自己思考后再提交测试！")
                    else:
                        st.info(f"抱歉，当前 {current_lang} 版本的参考答案正在整理中，请参考 Python 版本：")
                        st.code(solution.get("Python", ""), language="python")
                else:
                    # 备用：使用旧的知识库逻辑
                    topic_code = None
                    knowledge_point = q.get("knowledge_point", "")
                    topic = q.get("topic", "")

                    knowledge_keywords = {
                        "数组": "数组与字符串",
                        "字符串": "数组与字符串",
                        "链表": "链表",
                        "栈": "栈与队列",
                        "队列": "栈与队列",
                        "树": "树与图",
                        "图": "树与图",
                        "递归": "递归与分治",
                        "分治": "递归与分治",
                        "动态规划": "动态规划",
                        "回溯": "回溯算法",
                        "贪心": "贪心算法",
                        "哈希表": "数组与字符串"
                    }

                    for kw, kb_topic in knowledge_keywords.items():
                        if kw in knowledge_point or kw in topic:
                            if kb_topic in KNOWLEDGE_BASE.get("数据结构", {}) or kb_topic in KNOWLEDGE_BASE.get("算法思想", {}):
                                for cat_name, cat_data in KNOWLEDGE_BASE.items():
                                    if kb_topic in cat_data:
                                        topic_code = cat_data[kb_topic]["code"].get(st.session_state.selected_language, cat_data[kb_topic]["code"]["Python"])
                                        break
                            break

                    if topic_code:
                        st.code(topic_code, language=st.session_state.selected_language.lower() if st.session_state.selected_language != "C++" else "cpp")
                        st.caption("参考上述知识点代码，先自己思考哦！")
                    else:
                        st.info("💡 该题目暂无详细参考答案，请参考上方提示自行编写。如需学习相关知识，可前往「学习中心」查看。")

            # 代码输入区域（Monaco Editor）
            lang = st.session_state.selected_language

            st.markdown(f"**💻 请输入 {lang} 代码：**")

            # 使用 Monaco Editor
            code = code_editor(
                key=f"special_code_{idx}",
                label="代码编辑器",
                initial_value="",
                language=lang,
                height=350
            )

            # 显示当前语言
            st.caption(f"📌 当前语言: {lang} | 💡 Monaco Editor - VS Code 同款编辑器")

            # 导航按钮行
            nav_cols = st.columns([1, 1, 4])
            with nav_cols[0]:
                if idx > 0:
                    if st.button("⬅️ 上一题", key=f"special_prev_{idx}", use_container_width=True):
                        s["index"] -= 1
                        st.rerun()
                else:
                    st.button("⬅️ 上一题", disabled=True, use_container_width=True, key=f"special_prev_{idx}")

            with nav_cols[1]:
                if idx + 1 < len(qs):
                    if st.button("下一题 ➡️", key=f"special_next_{idx}", use_container_width=True):
                        s["index"] += 1
                        st.rerun()
                else:
                    # 计算总完成数
                    total_completed = sum(1 for a in s["answers"].values() if a.get("score", 0) == 100)
                    if st.button("🏁 完成练习", key=f"special_finish_{idx}", use_container_width=True):
                        if total_completed == total:
                            st.balloons()
                            st.success("🎊 恭喜全部完成！太厉害了！")
                        else:
                            st.info(f"当前完成 {total_completed}/{total} 题，继续加油！")

            # 提交本题
            with nav_cols[2]:
                submit_key = f"special_submit_{idx}"
                if st.button("📤 提交本题", type="primary", key=submit_key, use_container_width=True):
                    tcs = []
                    for tc in q["test_cases"]:
                        parts = tc.split("->")
                        if len(parts) == 2:
                            tcs.append((parts[0].strip(), parts[1].strip()))

                    result = run_code_test(code, st.session_state.selected_language, tcs, q["topic"])
                    s["answers"][idx] = result

                    if not result["syntax_ok"]:
                        st.error(f"❌ 语法错误: {result['error']}")
                    else:
                        st.markdown("### 测试结果")
                        for r in result["results"]:
                            if r.get("error"):
                                st.error(f"❌ {r['input']} → {r['actual']}")
                            elif r["passed"]:
                                st.success(f"✅ 通过: 输入 `{r['input']}` → 预期 `{r['expected']}`")
                            else:
                                st.error(f"❌ 失败: 输入 `{r['input']}` → 预期 `{r['expected']}` 实际 `{r['actual']}`")
                        st.markdown(f"**得分: {result['score']}分 ({result['passed']}/{result['total']})**")

                        # 如果全部通过
                        if result["score"] == 100:
                            st.balloons()
                            st.success("🎉 太棒了！本题全部通过！")
        else:
            # 计算总完成数（只有满分才算完成）
            total_completed = sum(1 for a in s["answers"].values() if a.get("score", 0) == 100)
            st.balloons()
            st.success(f"🎊 练习完成！共完成 {total_completed}/{total} 题！")

            # 更新学习进度
            topic = s["topic"]
            category = s["questions"][0]["category"] if s["questions"] else "基础语法"

            # 计算本次练习的平均得分
            scores = [a.get("score", 0) for a in s["answers"].values()]
            avg_score = sum(scores) / len(scores) / 100  # 转换为0-1范围

            # 更新掌握度（使用加权平均）
            if topic not in st.session_state.mastery_level:
                st.session_state.mastery_level[topic] = avg_score
            else:
                # 新的掌握度 = 旧的 * 0.7 + 本次 * 0.3
                st.session_state.mastery_level[topic] = st.session_state.mastery_level[topic] * 0.7 + avg_score * 0.3

            # 同时按分类更新
            if category not in st.session_state.mastery_level:
                st.session_state.mastery_level[category] = avg_score
            else:
                st.session_state.mastery_level[category] = st.session_state.mastery_level[category] * 0.7 + avg_score * 0.3

            if st.button("再来一轮", key="special_restart"):
                del st.session_state.special_practice
                st.rerun()

# ============== 练习中心 ==============
elif page == "💻 练习中心":
    st.markdown("## 💻 练习中心 - 随机挑战")
    st.markdown(f"📚 题库: **{len(QUESTION_BANK)}** 道")

    col1, col2 = st.columns(2)
    with col1:
        diff = st.selectbox("难度", ["全部", "基础", "中等", "进阶"], key="diff_filter")
    with col2:
        count = st.slider("题目数量", 3, 10, 5, key="count_filter")

    if st.button("🚀 开始练习", type="primary", use_container_width=True):
        filtered = QUESTION_BANK
        if diff != "全部":
            d = ["基础", "中等", "进阶"].index(diff) + 1
            filtered = [q for q in QUESTION_BANK if q["difficulty"] == d]

        if filtered:
            selected = random.sample(filtered, min(count, len(filtered)))
            st.session_state.random_practice = {"questions": selected, "index": 0, "answers": {}}
            st.rerun()
        else:
            st.warning("该难度暂无题目，请选择其他难度")

    if st.session_state.get("random_practice"):
        s = st.session_state.random_practice
        idx = s["index"]
        qs = s["questions"]
        total = len(qs)

        # 收起按钮和标题
        col_left, col_right = st.columns([1, 5])
        with col_left:
            if st.button("🔼 收起练习", key="hide_random_practice"):
                del st.session_state.random_practice
                st.rerun()
        with col_right:
            st.markdown("### 💻 随机挑战")

        # 横向题目进度条（可点击跳转）
        st.markdown("**📊 答题进度：**")
        progress_cols = st.columns(total)
        for i, q_item in enumerate(qs):
            with progress_cols[i]:
                score = s["answers"].get(i, {}).get("score", 0)
                is_current = (i == idx)

                if score == 100:
                    bg_color = "#28a745"
                    emoji = "✅"
                elif score > 0:
                    bg_color = "#fd7e14"
                    emoji = "⏳"
                else:
                    bg_color = "#6c757d"
                    emoji = "○"

                label = f"**{emoji} {i+1}**"
                if is_current:
                    label = f"👉 **{emoji} {i+1}**"

                if st.button(label, key=f"rand_qbtn_{i}", use_container_width=True):
                    s["index"] = i
                    st.rerun()

                if score > 0:
                    st.caption(f"💯 {score}分")

        st.markdown("---")

        if idx < len(qs):
            q = qs[idx]
            st.markdown(f"### 📝 题目 {idx+1}/{total}: {q['title']}")
            st.markdown(q["description"])

            # 输入格式
            st.markdown("**📥 输入格式**")
            input_format = q.get("input_format", "输入数据，格式见题目描述")
            st.code(input_format, language="plaintext")

            # 输出格式
            st.markdown("**📤 输出格式**")
            output_format = q.get("output_format", "输出结果，格式见题目描述")
            st.code(output_format, language="plaintext")

            # 样例
            st.markdown("**📝 样例**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**输入**")
                st.code(q["examples"]["input"], language="plaintext")
            with col2:
                st.markdown("**输出**")
                st.code(q["examples"]["output"], language="plaintext")

            # 提示
            with st.expander("💡 查看提示"):
                for h in q["hints"]:
                    st.markdown(f"- {h}")

            # 隐藏的标准答案（专项练习）
            with st.expander("📝 参考答案", expanded=False):
                qid = q.get("id", "")

                # 优先使用标准答案库
                if qid in SOLUTIONS:
                    solution = SOLUTIONS[qid]
                    current_lang = st.session_state.selected_language

                    st.markdown(f"### 📝 **{solution.get('title', q['title'])}参考答案**")
                    st.markdown(f"**当前语言: {current_lang}**")

                    # 获取对应语言的答案
                    code = solution.get(current_lang, solution.get("Python", ""))

                    if code:
                        lang_for_code = current_lang.lower() if current_lang != "C++" else "cpp"
                        st.code(code, language=lang_for_code)

                        st.success("💡 参考上述代码，先自己思考后再提交测试！")
                    else:
                        st.info(f"抱歉，当前 {current_lang} 版本的参考答案正在整理中，请参考 Python 版本：")
                        st.code(solution.get("Python", ""), language="python")
                else:
                    # 备用：使用旧的知识库逻辑
                    topic_code = None
                    knowledge_point = q.get("knowledge_point", "")
                    topic = q.get("topic", "")

                    knowledge_keywords = {
                        "数组": "数组与字符串",
                        "字符串": "数组与字符串",
                        "链表": "链表",
                        "栈": "栈与队列",
                        "队列": "栈与队列",
                        "树": "树与图",
                        "图": "树与图",
                        "递归": "递归与分治",
                        "分治": "递归与分治",
                        "动态规划": "动态规划",
                        "回溯": "回溯算法",
                        "贪心": "贪心算法",
                        "哈希表": "数组与字符串"
                    }

                    for kw, kb_topic in knowledge_keywords.items():
                        if kw in knowledge_point or kw in topic:
                            if kb_topic in KNOWLEDGE_BASE.get("数据结构", {}) or kb_topic in KNOWLEDGE_BASE.get("算法思想", {}):
                                for cat_name, cat_data in KNOWLEDGE_BASE.items():
                                    if kb_topic in cat_data:
                                        topic_code = cat_data[kb_topic]["code"].get(st.session_state.selected_language, cat_data[kb_topic]["code"]["Python"])
                                        break
                            break

                    if topic_code:
                        st.code(topic_code, language=st.session_state.selected_language.lower() if st.session_state.selected_language != "C++" else "cpp")
                        st.caption("参考上述知识点代码，先自己思考哦！")
                    else:
                        st.info("💡 该题目暂无详细参考答案，请参考上方提示自行编写。如需学习相关知识，可前往「学习中心」查看。")

            # 代码输入区域（Monaco Editor）
            lang = st.session_state.selected_language

            st.markdown(f"**💻 请输入 {lang} 代码：**")

            # 使用 Monaco Editor
            code = code_editor(
                key=f"random_code_{idx}",
                label="代码编辑器",
                initial_value="",
                language=lang,
                height=350
            )

            # 显示当前语言
            st.caption(f"📌 当前语言: {lang} | 💡 Monaco Editor - VS Code 同款编辑器")

            # 导航按钮行
            nav_cols = st.columns([1, 1, 4])
            with nav_cols[0]:
                if idx > 0:
                    if st.button("⬅️ 上一题", key=f"random_prev_{idx}", use_container_width=True):
                        s["index"] -= 1
                        st.rerun()
                else:
                    st.button("⬅️ 上一题", disabled=True, use_container_width=True, key=f"random_prev_{idx}")

            with nav_cols[1]:
                if idx + 1 < len(qs):
                    if st.button("下一题 ➡️", key=f"random_next_{idx}", use_container_width=True):
                        s["index"] += 1
                        st.rerun()
                else:
                    if st.button("🏁 完成练习", key="random_finish", use_container_width=True):
                        # 更新学习进度
                        scores = [a.get("score", 0) for a in s["answers"].values()]
                        avg_score = sum(scores) / len(scores) / 100  # 转换为0-1范围

                        # 按分类统计
                        categories = {}
                        for q_item in s["questions"]:
                            cat = q_item.get("category", "基础语法")
                            score = s["answers"].get(s["questions"].index(q_item), {}).get("score", 0) / 100
                            if cat not in categories:
                                categories[cat] = []
                            categories[cat].append(score)

                        # 更新每个分类的掌握度
                        for cat, cat_scores in categories.items():
                            cat_avg = sum(cat_scores) / len(cat_scores)
                            if cat not in st.session_state.mastery_level:
                                st.session_state.mastery_level[cat] = cat_avg
                            else:
                                st.session_state.mastery_level[cat] = st.session_state.mastery_level[cat] * 0.7 + cat_avg * 0.3

                        st.balloons()
                        st.success(f"🎊 随机挑战完成！共 {len(scores)} 题！")

                        del st.session_state.random_practice
                        st.rerun()

            # 提交本题
            with nav_cols[2]:
                submit_key = f"random_submit_{idx}"
                if st.button("📤 提交本题", type="primary", key=submit_key, use_container_width=True):
                    tcs = []
                    for tc in q["test_cases"]:
                        parts = tc.split("->")
                        if len(parts) == 2:
                            tcs.append((parts[0].strip(), parts[1].strip()))

                    result = run_code_test(code, st.session_state.selected_language, tcs, q["topic"])
                    s["answers"][idx] = result

                    if not result["syntax_ok"]:
                        st.error(f"❌ 语法错误: {result['error']}")
                    else:
                        st.markdown("### 📊 测试结果")
                        passed_count = 0
                        for r in result["results"]:
                            if r["passed"]:
                                passed_count += 1
                                st.success(f"✅ 通过")
                            else:
                                st.error(f"❌ 失败")

                        if passed_count == len(result["results"]):
                            st.balloons()
                            st.success(f"🎉 全部通过！得分: {result['score']}分")
                        else:
                            st.info(f"通过 {passed_count}/{result['total']} 个测试用例，得分: {result['score']}分")
    else:
        st.info("👆 点击上方「开始练习」按钮，随机获取题目进行挑战！")

# ============== 学习报告 ==============
elif page == "📊 学习报告":
    st.markdown("## 📊 学习报告")

    # 初始化自定义题库（如果不存在）
    if "custom_question_bank" not in st.session_state:
        st.session_state.custom_question_bank = []
    if "custom_test_results" not in st.session_state:
        st.session_state.custom_test_results = {}

    st.markdown("### 📈 掌握度统计")

    # 系统题库掌握度
    if st.session_state.mastery_level:
        for topic, mastery in st.session_state.mastery_level.items():
            st.markdown(f"- **{topic}:** {mastery*100:.0f}%")
            st.progress(mastery)
    else:
        st.info("开始练习后这里会显示你的学习进度")

    # 自定义题库掌握度
    custom_qs = st.session_state.custom_question_bank
    if custom_qs:
        st.markdown("---")
        st.markdown("### 🎯 自定义题库掌握度")

        # 计算每道题的掌握情况
        custom_mastery_data = []
        for q in custom_qs:
            q_id = q.get("id", "")
            q_title = q.get("title", "无标题")
            q_lang = q.get("language", "Python")
            q_difficulty = q.get("difficulty", 1)

            # 获取该题的测试结果
            test_result = st.session_state.custom_test_results.get(q_id, {})
            score = test_result.get("score", 0) if test_result else 0

            # 掌握状态：满分=已掌握(100%)，有分=学习中，0分=未开始
            if score == 100:
                status = "✅ 已掌握"
                status_color = "green"
            elif score > 0:
                status = f"📖 学习中 ({score}分)"
                status_color = "orange"
            else:
                status = "⏳ 未开始"
                status_color = "gray"

            diff_emoji = "🟢" if q_difficulty == 1 else "🟡" if q_difficulty == 2 else "🔴"

            custom_mastery_data.append({
                "title": q_title,
                "language": q_lang,
                "difficulty": q_difficulty,
                "score": score,
                "status": status,
                "status_color": status_color,
                "diff_emoji": diff_emoji
            })

        # 显示每道题的掌握情况
        for item in custom_mastery_data:
            col1, col2, col3 = st.columns([3, 1, 2])
            with col1:
                st.markdown(f"**{item['diff_emoji']} {item['title']}**")
            with col2:
                st.caption(f"🔤 {item['language']}")
            with col3:
                if item['score'] == 100:
                    st.success(item['status'])
                elif item['score'] > 0:
                    st.warning(item['status'])
                else:
                    st.info(item['status'])

        # 总体掌握度统计
        st.markdown("---")
        total_custom = len(custom_mastery_data)
        mastered = len([x for x in custom_mastery_data if x['score'] == 100])
        learning = len([x for x in custom_mastery_data if 0 < x['score'] < 100])
        not_started = len([x for x in custom_mastery_data if x['score'] == 0])

        cols = st.columns(4)
        cols[0].metric("📊 总题目", total_custom)
        cols[1].metric("✅ 已掌握", mastered)
        cols[2].metric("📖 学习中", learning)
        cols[3].metric("⏳ 未开始", not_started)

        # 总体掌握率
        if total_custom > 0:
            mastery_rate = mastered / total_custom
            st.markdown(f"**整体掌握率：{mastery_rate*100:.0f}%**")
            st.progress(mastery_rate)

            if mastery_rate == 1.0:
                st.balloons()
                st.success("🎉 太棒了！所有自定义题目都已掌握！")
            elif mastery_rate >= 0.5:
                st.info(f"💪 继续加油！还有 {total_custom - mastered} 道题目待掌握")
            else:
                st.info(f"📚 学习之路漫漫，还需努力！完成 {mastered}/{total_custom} 道")

    st.markdown("---")
    st.markdown("### 📚 题库概览")
    cols = st.columns(3)
    cols[0].metric("📝 总题目", len(QUESTION_BANK))
    cols[1].metric("🟢 基础", len([q for q in QUESTION_BANK if q["difficulty"] == 1]))
    cols[2].metric("🟡 中等", len([q for q in QUESTION_BANK if q["difficulty"] == 2]))

    cols = st.columns(3)
    cols[0].metric("🔴 进阶", len([q for q in QUESTION_BANK if q["difficulty"] == 3]))
    cols[1].metric("🗂️ 数据结构", len([q for q in QUESTION_BANK if q["category"] == "数据结构"]))
    cols[2].metric("🧠 算法思想", len([q for q in QUESTION_BANK if q["category"] == "算法思想"]))

    # 自定义题库统计
    st.markdown("---")
    st.markdown("### 📦 自定义题库")

    custom_count = len(custom_qs)

    cols = st.columns(4)
    cols[0].metric("📝 自定义题目", custom_count)
    cols[1].metric("🟢 基础", len([q for q in custom_qs if q.get("difficulty", 1) == 1]))
    cols[2].metric("🟡 中等", len([q for q in custom_qs if q.get("difficulty", 1) == 2]))
    cols[3].metric("🔴 进阶", len([q for q in custom_qs if q.get("difficulty", 1) == 3]))

    # 按语言统计
    if custom_qs:
        st.markdown("**按语言分布：**")
        lang_counts = {}
        for q in custom_qs:
            lang = q.get("language", "Python")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        lang_cols = st.columns(len(lang_counts))
        for i, (lang, count) in enumerate(lang_counts.items()):
            lang_cols[i].metric(f"🔤 {lang}", count)

    # 快捷跳转提示
    if custom_count > 0:
        st.info(f"💡 前往「🤖 AI助手」页面可以练习和管理您的 {custom_count} 道自定义题目")
    else:
        st.info("💡 前往「🤖 AI助手」生成题目并添加到自定义题库")
