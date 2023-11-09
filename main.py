import requests
import tkinter as tk

def get_gold_price():
    url = 'https://api.metalpriceapi.com/v1/latest'
    params = {
        'api_key': '9140e2d186d86ea1634db72f98a661a7',
        'base': 'XAU',
        'currencies': 'AUD'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            return int(data['rates']['AUD'])
    return None

class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Gold Price')
        self.master.geometry('200x100')
        self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.master.bind('<Escape>', self.on_faded)
        self.master.bind('<Button-1>', self.start_move)
        self.master.bind('<B1-Motion>', self.on_move)
        self.label = tk.Label(self.master, font=('Arial', 48))
        self.label.pack(expand=True)
        self.last_price = None
        self.update_price()
        self.faded = False

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f'+{x}+{y}')

    def on_close(self):
        self.master.after(1000, self.master.destroy)

    def update_price(self):
        price = get_gold_price()
        if price is not None:
            self.label.config(text=f'{price:04d}')
        self.master.after(30000, self.update_price)

    def on_faded(self, event=None):
        if not self.faded:
            self.faded = True
            self.master.attributes('-alpha', 0.1)
        else:
            self.faded = False
            self.master.attributes('-alpha', 1.0)
        #self.master.after(1000, self.master.destroy)

root = tk.Tk()
root.overrideredirect(True)
root.geometry('200x100+600+500')
root.wm_attributes('-topmost', 1)
app = App(root)
root.mainloop()
