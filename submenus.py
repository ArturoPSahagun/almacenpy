import PySimpleGUI as sg
import psycopg2 as db
from datetime import datetime
from tkcalendar import *
import sys
import os

class Muestra:
    layout = [[]]

    def __init__(self, conn, tabla):
        self.conn = conn
        cur = conn.cursor()
        cur.execute('SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s', (tabla,))
        campos = cur.fetchall()
        self.layout = [[sg.Tree(data=sg.TreeData(),
                                text_color='black',
                                headings=campos,
                                auto_size_columns=False,
                                justification='center',
                                col0_width=8,
                                def_col_width=10,
                                key='-TREE-')]]

    def ejecutar_producto(self):
        window = sg.Window('Mostrar Todos los Productos', self.layout, finalize=True)
        data = sg.TreeData()
        cur = self.conn.cursor()
        cur.execute('select distinct depto from producto')
        padres = cur.fetchall()
        for pa in padres:
            data.insert('', pa[0], pa, values=[' '])
        cur.execute('select * from producto')
        productos = cur.fetchall()
        for pro in productos:
            data.insert(pro[7], pro[0],' ', values=pro)

        window['-TREE-'].update(data)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

    def ejecutar_usuario(self):
        window = sg.Window('Mostrar Todos los Usuarios', self.layout, finalize=True)
        data = sg.TreeData()
        cur = self.conn.cursor()
        cur.execute('select distinct turno from usuario')
        padres = cur.fetchall()
        for pa in padres:
            data.insert('', pa[0], pa, values=[' '])
        cur.execute('select * from usuario')
        productos = cur.fetchall()
        for pro in productos:
            data.insert(pro[3], pro[0],' ', values=pro)

        window['-TREE-'].update(data)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class muestra_es:
    layout = [[]]

    def __init__(self, conn, tabla):
        self.conn = conn
        cur = conn.cursor()
        cur.execute('SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s', (tabla,))
        campos = cur.fetchall()
        self.layout = [[sg.Tree(data= sg.TreeData(),
                                text_color='black',
                                headings=campos,
                                auto_size_columns=False,
                                justification='center',
                                col0_width=0,
                                def_col_width=10,
                                key='-TREE-')]]

    def ejecutar_entrada(self):
        window = sg.Window('Mostrar Todos las Entradas', self.layout, finalize=True)
        data = sg.TreeData()
        cur = self.conn.cursor()
        cur.execute('select * from entrada')
        padres = cur.fetchall()
        hijos_campos = ['','𝗦𝗞𝗨', '𝗡𝗢𝗠𝗕𝗥𝗘', '𝗖𝗔𝗡𝗧𝗜𝗗𝗔𝗗']
        hijos = []
        for pa in padres:
            #data.insert(self, parent='', key=pa[0], text='', values=pa )
            data.insert('', pa[0], '', values=pa)
            data.insert(pa[0], 'campos'+str(pa[0]), '', values=hijos_campos)
            cur.execute('SELECT mercanciaenentrada.sku, nombre, cantidad '
                        'FROM mercanciaenentrada '
                        'INNER JOIN producto '
                        'ON mercanciaenentrada.sku = producto.sku '
                        'WHERE identrada = %s', (pa[0],))
            hijos = cur.fetchall()
            for hi in hijos:
                data.insert(pa[0], str(pa[0])+hi[0], '', values=(' ',) + hi)
        #print(cur.fetchall())

        window['-TREE-'].update(data)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

    def ejecutar_salida(self):
        window = sg.Window('Mostrar Todos las Salidas', self.layout, finalize=True)
        data = sg.TreeData()
        cur = self.conn.cursor()
        cur.execute('select * from salida')
        padres = cur.fetchall()
        hijos_campos = ['','𝗦𝗞𝗨', '𝗡𝗢𝗠𝗕𝗥𝗘', '𝗖𝗔𝗡𝗧𝗜𝗗𝗔𝗗']
        hijos = []
        for pa in padres:
            #data.insert(self, parent='', key=pa[0], text='', values=pa )
            data.insert('', pa[0], '', values=pa)
            data.insert(pa[0], 'campos'+str(pa[0]), '', values=hijos_campos)
            cur.execute('SELECT mercanciaensalida.sku, nombre, cantidad '
                        'FROM mercanciaensalida '
                        'INNER JOIN producto '
                        'ON mercanciaensalida.sku = producto.sku '
                        'WHERE idsalida = %s', (pa[0],))
            hijos = cur.fetchall()
            for hi in hijos:
                data.insert(pa[0], str(pa[0])+hi[0], '', values=(' ',) + hi)
        #print(cur.fetchall())

        window['-TREE-'].update(data)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class editar_productos:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout=[[sg.Text("Ingrese sku del producto a editar: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-'), sg.Button('Buscar')],
                     [sg.Text("Ubicacion: "), sg.Input(size=(20, 1), key='-UBICACIONINPUT-')],
                     [sg.Text("Nombre:\t  "), sg.Input(size=(20, 1), key='-NOMBREINPUT-')],
                     [sg.Text("Marca:\t  "), sg.Input(size=(20, 1), key='-MARCAINPUT-')],
                     [sg.Text("Tamaño:\t  "), sg.Input(size=(20, 1), key='-SIZEINPUT-')],
                     [sg.Text("Color:\t  "), sg.Input(size=(20, 1), key='-COLORINPUT-')],
                     [sg.Text("Precio:\t  "), sg.Input(size=(20, 1), key='-PRECIOINPUT-')],
                     [sg.Text("Depto:\t  "), sg.Input(size=(20, 1), key='-DPTOINPUT-')],
                     [sg.Text("Existencia:"), sg.Input(size=(20, 1), key='-EXISTENCIAINPUT-')],
                     [sg.Text("Disponible:"), sg.Combo(size=(20, 1), key='-DISPONIBLEINPUT-', values=[1, 0])],
                     [sg.Button('Actualizar')]
                     ]


    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Editar producto", self.layout)
        while True:
            event, values = window.read()
            if  event == 'Buscar':
                cur.execute('select * from producto where sku = %s', (values['-CODIGOINPUT-'],))
                productos = cur.fetchall()
                if len(productos) > 0:
                    window['-UBICACIONINPUT-'].update(productos[0][1])
                    window['-NOMBREINPUT-'].update(productos[0][2])
                    window['-MARCAINPUT-'].update(productos[0][3])
                    window['-SIZEINPUT-'].update(productos[0][4])
                    window['-COLORINPUT-'].update(productos[0][5])
                    window['-PRECIOINPUT-'].update(productos[0][6])
                    window['-DPTOINPUT-'].update(productos[0][7])
                    window['-EXISTENCIAINPUT-'].update(productos[0][8])
                    window['-DISPONIBLEINPUT-'].update(productos[0][9])
            elif event == 'Actualizar':
                cur.execute('UPDATE producto '
                            'SET ubicacion = %s, '
                            'nombre = %s, '
                            'marca = %s, '
                            'size = %s, '
                            'color = %s, '
                            'precio = %s, '
                            'depto = %s, '
                            'existencias = %s, '
                            'disponible = %s '
                            'WHERE sku = %s',
                            (values['-UBICACIONINPUT-'],
                             values['-NOMBREINPUT-'],
                             values['-MARCAINPUT-'],
                             values['-SIZEINPUT-'],
                             values['-COLORINPUT-'],
                             values['-PRECIOINPUT-'],
                             values['-DPTOINPUT-'],
                             values['-EXISTENCIAINPUT-'],
                             bool(values['-DISPONIBLEINPUT-']),
                             values['-CODIGOINPUT-'], ))
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class editar_usuarios:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout=[[sg.Text("Ingrese username del usuario a editar: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-'), sg.Button('Buscar')],
                     [sg.Text("Password: "), sg.Input(size=(20, 1), key='-PASSWORDINPUT-')],
                     [sg.Text("Nombre:\t  "), sg.Input(size=(20, 1), key='-NOMBREINPUT-')],
                     [sg.Text("Turno:\t  "), sg.Input(size=(20, 1), key='-TURNOINPUT-')],
                     [sg.Button('Actualizar')]
                     ]


    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Editar usuario", self.layout)
        while True:
            event, values = window.read()
            if  event == 'Buscar':
                cur.execute('select * from usuario where username = %s', (values['-CODIGOINPUT-'],))
                usuarios = cur.fetchall()
                if len(usuarios) > 0:
                    window['-PASSWORDINPUT-'].update(usuarios[0][1])
                    window['-NOMBREINPUT-'].update(usuarios[0][2])
                    window['-TURNOINPUT-'].update(usuarios[0][3])

            elif event == 'Actualizar':
                cur.execute('UPDATE usuario '
                            'SET password = %s, '
                            'nombre = %s, '
                            'Turno = %s '
                            'WHERE username = %s',
                            (values['-PASSWORDINPUT-'],
                             values['-NOMBREINPUT-'],
                             values['-TURNOINPUT-'],
                             values['-CODIGOINPUT-'], ))
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class crear_usuarios:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout = [[sg.Text("Username: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-')],
                       [sg.Text("Password: "), sg.Input(size=(20, 1), key='-PASSWORDINPUT-')],
                       [sg.Text("Nombre:\t  "), sg.Input(size=(20, 1), key='-NOMBREINPUT-')],
                       [sg.Text("Turno:\t  "), sg.Input(size=(20, 1), key='-TURNOINPUT-')],
                       [sg.Button('Crear')]
                       ]

    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Crear usuario", self.layout)
        while True:
            event, values = window.read()
            if event == 'Crear':
                cur.execute('INSERT INTO usuario '
                            'VALUES(%s, %s, %s, %s)',
                            (values['-CODIGOINPUT-'],
                             values['-PASSWORDINPUT-'],
                             values['-NOMBREINPUT-'],
                             values['-TURNOINPUT-'],))
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class eliminar_usuarios:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout = [[sg.Text("Ingrese username del usuario a eliminar: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-', enable_events=True)],
                       [sg.Text(' ', key='-CONDENADO-', size=(29, 1), background_color='lightgray')],
                       [sg.Button('Eliminar'), sg.Button('Cancelar')]
                       ]

    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Eliminar usuario", self.layout)
        while True:
            event, values = window.read()
            if values['-CODIGOINPUT-'] != '':
                cur.execute('select nombre, turno from usuario where username = %s and activo = \'t\'', (values['-CODIGOINPUT-'],))
                cond = cur.fetchall()
                if len(cond) > 0:
                    window['-CONDENADO-'].update(cond[0][0] + ', turno ' + cond[0][1])
            if event == 'Eliminar':
                cur.execute('update usuario set activo = \'f\' where username = %s', (values['-CODIGOINPUT-'],))
                break
            if event == 'Cancelar':
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()
