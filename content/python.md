Title: Понимание и рецепты Python
Date: 2014-07-10 16:22
Tags: python
Category: IT
Author: Swasher

Понимание python
=========================================

#### map

В map передается функция, и список. На выходе получаем список такой же длины, с выполненной функцией над каждым элементом списка.
Самый простой пример:

    ::python
    def f(x):
        return x*x
        
    a = [1, 2, 3, 4]

    m = map(f, a)
    
m - это итератор, объект типа `<class 'map'>`. Его можно итерировать как список или кортеж: `for i in m: print(i)`

С функцией отображения (map) удобно использовать лямбда-функции:

    ::python
    m = map(lambda x: x*x, a)

Так же в map можно передать несколько списков

    ::python
    a = [1, 2, 3, 4]
    b = [5, 6, 7, 8]
    m = map(lambda x, y: x*y, a, b)


Рецепты
=========================================

### Рыба

    ::python
    import random
    words = "lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et".split()
    " ".join([random.choice(words) for i in range(1000)])

### Форматирование с помощью словаря

Используется способ 'распаковка словаря'

    ::python
    text = """\
    Hi my name is "{person_name}"
    I am from "{location}"
    You must be "{person_met}"\
    """
    person = {'person_name': 'Joan', 'location': 'USA', 'person_met': 'Victor'}
    
    print text.format(**person)
    
    
### if в одну строку
    
    ::python
    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    
### Открытие файла

По окончании выполнения `with` файл f будет закрыт в лююбом случае

    ::python
    with open('workfile', 'r') as f:
        read_data = f.read()
        
### Классы: итерация и нахождение инстанса по имени

Создадим класс Fruit и три инстанса. В классе создадим два вспомагательных
атрибута - словарь _dic, который хранит все экземпляры в виде {'apricot': <__main__.Fruit instance at 0x7f373cede9e0>}
и список _list, содержащий, соответственно, список экземпляров

    ::python
    class Fruit():
        _dic = {}
        _list = []
    
        def __init__(self, name, color):
            self._dic[name] = self
            self._list.append(self)
            self.name = name
            self.color = color
    
    apple = Fruit('apple', 'red')
    plum = Fruit('plum', 'blue')
    apricot = Fruit('apricot', 'orange')
    
Теперь можно 'взять' объект по имени (с помощью словаря)
    
    ::python
    fruit_string = 'plum'
    favorit_fruit = Fruit._dic[fruit_string]
    print type(favorit_fruit)
    print favorit_fruit.name
    
И можно итерировать все объекты класса (с помощью списка)
    
    ::python
    for fruit in Fruit._list:
        print 'fruit=', fruit.name, 'color=', fruit.color
        
### Определить, конфликтует ли переменная с зарезервированным словом python
        
    ::python
    >>> import keyword
    >>> keyword.iskeyword("in")
    True
    >>> keyword.kwlist
    ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', ... ]
    
Так же можно узнать все встроенные имена
    
    ::python
    >>> dir(__builtins__)
    ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError' ... ]
        
### Импорт и глобальные переменные

Кратко про импорт (модуль - что импортируется, скрипт - куда импортируется)

- `import module` - модуль становится доступен в скрипте, обращение к ресурсам module.variable. *Не копирует* ресурсы в
текущую область видимости. При импорте модуль выполняется, но только **первый раз**. 
- `from module import variable` - импортируем переменную в скрипт. Доступна просто как variable. *Копирует* ресурс в
текущую область видимости. Может конфликтовать с одноименной переменной скрипта.
- `from module import *` - аналогично предыдущему, импортируется все функции и переменные.  *Копирует* ресурсы в
текущую область видимости. Следует избегать, чтобы не возникал конфликт имен.
- `__variable__` - переменные и функции с двойным подчеркивание не будут импортированы при `from module import *`



main.py

    ::python
    import class
    
    # Теперь можно выполнить функцию из импортированного модуля,
    # и переменные, которые объявлены в ней как global, станут доступны в main 
    classes.fruit_init()
    a = classes.plum
    
    >>>print a.name
    plum    
    
class.py

    ::python
    class Fruit():
        def __init__(self, name, color):
            self.name = name
            self.color = color
        
    def fruit_init():
        global apple, plum, apricot
        apple = Fruit('apple', 'red')
        plum = Fruit('plum', 'blue')
        apricot = Fruit('apricot', 'orange')
        
### Замер скорости выполнения команды

    ::python
    print '\n-->Staring Jpeg preview compression...'

    import time

    class Profiler(object):
        def __enter__(self):
            self._startTime = time.time()

        def __exit__(self, type, value, traceback):
            print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)

    with Profiler() as p:
        os.system(gs_compress)
    with Profiler() as p:
        os.system(make_thumb)
    with Profiler() as p:
        os.system(make_jpeg)

    print 'Compression finished.'
    
### Регулярки

**Компилирование** 

    ::python
    prog = re.compile(pattern)
    result = prog.match(string)

Такое сочетание эквивалентно 
    
    ::python
    result = re.match(pattern, string)

В простых программах в этом нет необходимости, питон сам кеширует.

**search() vs. match()**

match ищет паттерн только в начале строки, в то время как search по всей строке:

    ::python
    >>> re.match("c", "abcdef")  # No match
    >>> re.search("c", "abcdef") # Match
    <_sre.SRE_Match object at ...>
    
### Дата-время

*struct*

Возьмем время создания файла. Время имеет тип float, и содержит в себе кол-во секунд с начала эпохи. 

    ::python
    >>> f = 'requirements.txt'
    >>> import os
    >>> os.path.getmtime(f)
    1422608317.0
    >>> type(os.path.getmtime(f))
    <type 'float'>

Переведем время в тип [struct_time](https://docs.python.org/2/library/time.html#time.struct_time)
Этот тип возвращается функциями gmtime(), localtime(), and strptime().
Тип данных `struct_time` - это так называемый named-tuple: можно обращаться как по индексу, так и по имени атрибута

    ::python
    >>> from time import gmtime
    >>> time_struct = gmtime(os.path.getmtime(f))
    
    >>> type(time_struct)
    <type 'time.struct_time'>
    
    >>> time_struct
    time.struct_time(tm_year=2015, tm_mon=1, tm_mday=30, tm_hour=8, tm_min=58, tm_sec=37, \ 
                     tm_wday=4, tm_yday=30, tm_isdst=0)
     
    >>> print time_struct[0], time_struct.year, time_struct[1], time_struct.tm_mon
    2015 2015 1 1
    
*float -> datetime*:

    ::python
    >>> import datetime
    >>> ts = os.path.getmtime(f)
    >>> obj = datetime.datetime.fromtimestamp(ts)
    
    >>> type(obj)
    <type 'datetime.datetime'>
    
    >>> obj
    datetime.datetime(2015, 1, 30, 10, 58, 37)

*string <-> struct*

    ::python
    >>> from time import strftime
    >>> time_string = strftime("%d %b %Y", time_struct)
    >>> print type(time_string), time_string
    <type 'str'> 30 Jan 2015
        
    >>> import time
    >>> time_struct = time.strptime(time_string, "%d %b %Y")
    >>> print type(time_struct), time_struct
    <type 'time.struct_time'> time.struct_time(tm_year=2015, tm_mon=1, tm_mday=30, \
                                               tm_hour=0, tm_min=0, tm_sec=0, \
                                               tm_wday=4, tm_yday=30, tm_isdst=-1)
    
*struct -> datetime*

    ::python
    >>> from datetime import datetime
    >>> time_obj = datetime.strptime(time_string, "%d %b %Y")
    >>> type(time_obj)
    <type 'datetime.datetime'>
    
*datetime -> string* [directives](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)

    ::python
    >>> d = datetime.datetime.now()                                                                                                                                                                                                              
    >>> d                                                                                                                                                                                                                                        
    datetime.datetime(2015, 4, 10, 23, 0, 4, 599450)                                                                                                                                                                                             
    >>> type(d)                                                                                                                                                                                                                                  
    <type 'datetime.datetime'>
    >>> d.strftime("%B %d, %Y")                                                                                                                                                                                                               
    'April 10, 2015'
    
    
### Строки

Преобразовать список в строку

    ::python
    >>> list1 = ['1', '2', '3']
    >>> str1 = ''.join(list1)
    
или предварительно выполнив какое-то действие над элементом списка:
    
    ::python
    >>> list1 = [1, 2, 3]
    >>> str1 = ''.join(str(e) for e in list1)
    
## Замер скорости выполнения

https://github.com/dreid/yunomi

## Автоматический интерактив (аналог expect)

http://stackoverflow.com/a/10483096/1334825

## Ошибки Unicode

Ошибка: 

    'ascii' codec can't encode characters in position 0-14: ordinal not in range(128)

Код (метод класса в Джанго):    

    def __str__(self):
        return '{}'.format(self.name)
        
Решение:

    def __str__(self):
        return '{}'.format(self.name.encode('utf8'))
        
