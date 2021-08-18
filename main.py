from clases import *
from submenus import *
import sys



conn = db.connect("dbname=almacenroyal user=arturo")
conn.autocommit = True
cur = conn.cursor()
sg.ChangeLookAndFeel('LightGreen6')

user = ''
treedata = sg.TreeData()


layout_login = [[sg.Text("Introduzca su usuario y contraseña")],
                [sg.Text("Usuario:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-NAMEINPUT-')],
                [sg.Text("Contraseña:\t"), sg.Input(size=(20, 1), enable_events=True, key='-PASSWORDINPUT-', password_char='•')],
                [sg.Button('Login')],
                [sg.Text("", key='-ERRORTEXT-')]
                ]
window = sg.Window('Sistema de Almacen', layout_login)

while True:
    event, values = window.read()
    if event == "Login" :
        cur.execute('select password from usuario where username = \'' + values['-NAMEINPUT-'] + '\'')
        query = cur.fetchall()
        passw = ' '
        if len(query) > 0:
            passw = query[0][0]

        if passw != values['-PASSWORDINPUT-']:
            sg.Popup('Error', 'Usuario o contraseña incorrectos')
            window.FindElement('-PASSWORDINPUT-').Update('')
            continue
        else:
            user = values['-NAMEINPUT-']
            window.close()
            break
        window.close()
        break
    if event == sg.WIN_CLOSED :
        sys.exit()
        break

consult_layout = [[sg.Text("Codigo:"), sg.Input(size=(5, 1), enable_events=True, key='-CODIGOINPUT-'),
                   sg.Text("Nombre:"), sg.Input(size=(10,1),enable_events=True, key='-NAMEINPUT-'),
                   sg.Text('Departamento:'), sg.Combo((), enable_events=True, key='-DPTOINPUT-')],
                  [sg.Text('Marca:'), sg.Combo((), enable_events=True, key='-MARCAINPUT-'),
                   sg.Text('Tamaño:'), sg.Combo((), enable_events=True, key='-SIZEINPUT-'),
                   sg.Text('Color:'), sg.Combo((), enable_events=True, key='-COLORINPUT-'),
                   sg.Button('Buscar')],
                  [sg.Tree(data=treedata,
                           text_color='black',
                           headings=['   Nombre   ', 'Dpto', 'Marca', 'Tamaño', 'Color', 'Precio', 'Exis.','Ubicacion'],
                           auto_size_columns=True,
                           justification='center',
                           num_rows=15,
                           col0_width=6,
                           key='-LISTA-',
                           enable_events=True)]]

button_layout = [[sg.Button('Entradas', size=(10, 3))],
                 [sg.Button('Salidas', size=(10, 3))],
                 [sg.Button('Altas', size=(10, 3))],
                 [sg.Button('Bajas', size=(10, 3))],
                 [sg.Button('Conteo', size=(10, 3))],
                 [sg.Button('Salir', size=(10, 3))]]

layout_main =   [[sg.Menu([['Mostrar', ['Mostrar Productos', 'Mostrar Usuarios', 'Mostrar Entradas', 'Mostrar Salidas']],
                           ['Editar',['Editar Productos', 'Editar Usuarios']],
                           ['Eliminar/Crear', ['Eliminar Usuarios', 'Crear Usuarios']]])],
                 [sg.Text("Bienvenido, " + user)],
                 [sg.Frame('Consultas', consult_layout), sg.Column(button_layout)]
                ]
window = sg.Window("Sistema de almacen", layout_main, finalize=True)
cur.execute('SELECT DISTINCT depto FROM producto')
dptos = cur.fetchall()
dptos = [i for sub in dptos for i in sub]
dptos.append('')
window['-DPTOINPUT-'].update(values=(dptos))
cur.execute('SELECT DISTINCT marca FROM producto')
marcas = cur.fetchall()
marcas = [i for sub in marcas for i in sub]
window['-MARCAINPUT-'].update(values=(marcas))
cur.execute('SELECT DISTINCT size FROM producto')
sizes = cur.fetchall()
sizes = [i for sub in sizes for i in sub]
window['-SIZEINPUT-'].update(values=(sizes))
cur.execute('SELECT DISTINCT color FROM producto')
colores = cur.fetchall()
colores = [i for sub in colores for i in sub]
window['-COLORINPUT-'].update(values=(colores))

#bucle principal
while True:
    event, values = window.read()
    if event == 'Entradas':
        fe = Feature_entrada(conn, user)
        fe.ejecutar()
    elif event == "Altas":
        fa = Feature_alta(conn, user)
        fa.ejecutar()
        cur.execute('SELECT DISTINCT depto FROM producto')
        dptos = cur.fetchall()
        dptos = [i for sub in dptos for i in sub]
        dptos.append('')
        window['-DPTOINPUT-'].update(values=(dptos))
        cur.execute('SELECT DISTINCT marca FROM producto')
        marcas = cur.fetchall()
        marcas = [i for sub in marcas for i in sub]
        window['-MARCAINPUT-'].update(values=(marcas))
        cur.execute('SELECT DISTINCT size FROM producto')
        sizes = cur.fetchall()
        sizes = [i for sub in sizes for i in sub]
        window['-SIZEINPUT-'].update(values=(sizes))
        cur.execute('SELECT DISTINCT color FROM producto')
        colores = cur.fetchall()
        colores = [i for sub in colores for i in sub]
        window['-COLORINPUT-'].update(values=(colores))
    elif event == "Salidas":
        fs = Feature_salida(conn, user)
        fs.ejecutar()
    elif event == 'Buscar' :
        cur.execute('SELECT sku, nombre, depto, marca, size, color, precio, existencias, ubicacion '
                   'from producto where disponible = True '
                   'and sku like %s'
                   'and nombre ilike %s'
                   'and depto ilike %s'
                   'and marca ilike %s'
                   'and size ilike %s'
                   'and color ilike %s',
                   ('%'+values['-CODIGOINPUT-']+'%',
                    '%'+values['-NAMEINPUT-']+'%',
                    '%'+values['-DPTOINPUT-']+'%',
                    '%'+values['-MARCAINPUT-']+'%',
                    '%'+values['-SIZEINPUT-']+'%',
                    '%'+values['-COLORINPUT-']+'%'))
        todo = cur.fetchall()
        for prod in todo:
            treedata.insert('', prod[0], prod[0], values=[prod[1], prod[2], prod[3], prod[4], prod[5], prod[6], prod[7], prod[8]])
        window['-LISTA-'].update(treedata)
        treedata = sg.TreeData()

    elif event == 'Mostrar Productos':
        mp = Muestra(conn, 'producto')
        mp.ejecutar_producto()
    elif event == 'Mostrar Usuarios':
        mu = Muestra(conn, 'usuario')
        mu.ejecutar_usuario()
    elif event == 'Mostrar Entradas':
        me = muestra_es(conn, 'entrada')
        me.ejecutar_entrada()
    elif event == 'Mostrar Salidas':
        ms = muestra_es(conn, 'salida')
        ms.ejecutar_salida()
    elif event == 'Editar Productos':
        ep = editar_productos(conn)
        ep.ejecutar()
    elif event == 'Editar Usuarios':
        eu = editar_usuarios(conn)
        eu.ejecutar()
    elif event == 'Crear Usuarios':
        cu = crear_usuarios(conn)
        cu.ejecutar()
    elif event == 'Eliminar Usuarios':
        du = eliminar_usuarios(conn)
        du.ejecutar()
    elif event == 'Bajas':
        fb = Feature_Baja(conn)
        fb.ejecutar()
    elif event == 'Conteo':
        fc = Feature_conteo(conn, user)
        fc.ejecutar()
    elif event == 'Salir':
        break
    if event == sg.WIN_CLOSED:
        break



cur.close()
conn.close()
window.close()
