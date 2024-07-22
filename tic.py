
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import (ListProperty, NumericProperty)
from kivy.uix.modalview import ModalView



class GridEntry(Button):
    coords = ListProperty([0,0])



class TicTacToe(App):
    def build(self):
        return TicTacToeGrid()

    pass

class TicTacToeGrid(GridLayout):

    #Adds internal status list representing  who has played and where
    status = ListProperty([0, 0, 0, 0, 0, 0,
                               0, 0, 0])
    current_player = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(TicTacToeGrid, self).__init__(*args, **kwargs)
        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(coords = (row, column))   #Makes the 3x3 grid
                grid_entry.bind(on_release=self.button_pressed) #Bind method is used to call the button_pressed function 
                self.add_widget(grid_entry)

    def button_pressed(self, button):
        player = {1: "0", -1: "X"} #Labels for the players
        colours = {1: (1, 0, 1, 1), -1: (0, 1, 0, 1)}#(r, g, b, a) Colors for Xs and Os
        row, column = button.coords

        status_index = 3*row + column
        already_played = self.status[status_index] 

        if not already_played:
            self.status[status_index] = self.current_player
            button.text = {1: '0', -1: 'X'}[self.current_player]
            self.current_player *= -1


    def on_status(self, instance, new_value):
        status = new_value

        #covers the detection of a won or draw board: prints it to only stdout
        sums = [sum(status[0:3]),
                sum(status[3:6]),
                sum(status[6:9]), 
                sum(status[1::3]),
                sum(status[2::3]),
                sum(status[::4]),
                sum(status[2:-2:2])]
        
        winner = None 

        #Results
        if 3 in sums:
            print('Os wins')
        elif -3 in sums:
            print('Xs wins')
        elif 0 not in self.status:
            print('Draw!')

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=50)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss= self.reset)
            popup.open()
        

    def reset(self, *args):
        self.status = [0 for _ in range(9)]

        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)

        self.current_player = 1
                
        
                
                

        #print('{} button clicked'.format(instance.coords))
    pass

if __name__ == "__main__":
    TicTacToe().run() #Runs the code on tic 

