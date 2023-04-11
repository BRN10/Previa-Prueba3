from tkinter import ttk #ttk es la biblio que nos permite diseñar la interfaz
from tkinter import *

import sqlite3

class Product:

    db_name = 'database.db'


    # El metodo init es el primer metodo que se ejecuta cuando se crea un objeto.
    # El metodo init se llama automaticamente / similar a un constructor en otros lenguajes
    def __init__(self, window):
        self.wind = window
        self.wind.title('Products App')

    # Creating a FRAME CONTAINER, Creacion de un contenedor de marcos.
        frame = LabelFrame(self.wind, text='Register a New Product')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

    # Name Input
        Label(frame, text='Name: ').grid(row=1, column=0)
        # vamos a guardar esta caja de texto en una propiedad de mi clase llamada name
        # por que? para poder manipularla, es decir, el usuario va a ingresar datos en el input, si yo quiero almacenar lo voy a guardar en un propiedad, obtener ese dato
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        #self: permite al usuario especificar y acceder a los atributos y metodos de una instancia de la clase

    # Price Input
        Label(frame, text='Price: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2,column=1)

    # Button Add Product
        ttk.Button(frame, text='Save Product', command= self.add_product).grid(row=3, columnspan=2, sticky=W+E)
    # Out Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
    # Table
    #self es la manera de agregar propiedades a nuestra clase
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text= 'Name', anchor=CENTER)
        self.tree.heading('#1', text='Price', anchor=CENTER)
        
        self.get_products()

    # Buttons
        ttk.Button(text='DELETE', command=self.delete_product).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text='EDIT', command=self.edit_product).grid(row=5, column=1, sticky=W+E)



    # vamos a crear la base de datos en sqLite
    # parametros: self de la clase para obtener accedo a las propiedades
    # query consulta
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn: #metodo para conectarse a la bd y la guardamos con el nombre de conn
            cursor = conn.cursor() #  conn tiene un metodo llamando cursor que permite obtener la posicion en la que estoy en la bd
            result = cursor.execute(query, parameters) # cursor + execute permite ejecutar una consulta sql
            # cursor si enviamos un query de insert no retorna resultado, si enviamos un query de select retorna parametros, lo vamos a guardar en result 
            conn.commit() # commit ejecuta la funcion 
        return result

    def get_products(self):
        # CLEANING TABLE
        records = self.tree.get_children() #obtener todos los datos que esten en la tabla
        for element in records: 
            self.tree.delete(element)
        # QUERING DATA 
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values= row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            #print(self.name.get())
            #print(self.price.get())
            query = 'INSERT INTO product VALUES (NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else: 
           self.message['text'] = 'Name  and Price are required'
        self.get_products()
    
    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query,(name,))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        
        #Old Name
        Label(self.edit_wind, text='Old Name: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=  StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)
        
        #New Name
        Label(self.edit_wind, text= 'New Name').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #Old Price
        Label(self.edit_wind, text='Old Price').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value = old_price), state='readonly').grid(row=2, column=2)

        #New Price
        Label(self.edit_wind, text='New Price').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(name)
        self.get_products()

# iniciar la app 
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
