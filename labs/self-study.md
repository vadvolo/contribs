## Дополнительные задания

> [!NOTE]
> За основу берём Lab10, 11 или 12.

### 1. Реализовать механику отключения BGP сессий на коммутаторах.

Модифицировать существующие генераторы таким образом, чтобы при назначении тега `damaged` на любое из устройств в топологии Annet административно выключала все настроенные на нем BGP-сессии.  
*Тег `damaged` уже есть в Netbox.*

**Результат:**
```diff
  router bgp 65111
    address-family ipv4
+     neighbor 10.1.1.11 shutdown
+     neighbor 10.2.1.11 shutdown
```

### 2. Проанонсировать статические маршруты с ToR

1. Создать генератор, прописывающий на всех ToR статические маршруты, направленные в `Null0`. Сеть определяется через **netbox device id** - `192.168.<netbox device id>.0/24`. **netbox device id** доступен в атрибуте `id` объекта класса `Device`.  
	Новый генератор необходимо добавить в результат функции `get_generators()`, определяемой в файле `lab_generators/__init__.py`.
2. Добавить в существующие генераторы создание route-map с именем `IMPORT_STATIC`, которая назначает всем маршрутам **bgp community** `65000:1`.
3. Настроить в mesh для всех ToR редистрибуцию статических маршрутов с route-map `IMPORT_STATIC`. 

Mesh описывает соединения между устройствами, BGP-пиринги (`peers`) и опции BGP (`global_options`).
- `global_options` определяются в функции с декоратором `device`,
- `peers` определяются в функции с декоратором `direct`. 

Эти функции определены в модуле `mesh_view`. Параметры редистрибуции задаются в `global_options`.

**Результат:**
``diff
# -------------------- tor-1-1.nh.com.cfg --------------------
+ ip route 192.168.7.0 255.255.255.0 Null0
+ route-map IMPORT_STATIC permit 10
+   set community 65000:1
  router bgp 65111
    address-family ipv4
+     redistribute static route-map IMPORT_STATIC
# -------------------- tor-1-2.nh.com.cfg --------------------
+ ip route 192.168.8.0 255.255.255.0 Null0
+ route-map IMPORT_STATIC permit 10
+   set community 65000:1
  router bgp 65112
    address-family ipv4
+     redistribute static route-map IMPORT_STATIC
# -------------------- tor-1-3.nh.com.cfg --------------------
+ ip route 192.168.9.0 255.255.255.0 Null0
+ route-map IMPORT_STATIC permit 10
+   set community 65000:1
  router bgp 65113
    address-family ipv4
+     redistribute static route-map IMPORT_STATIC
```
