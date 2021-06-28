from abc import ABC, abstractmethod
import tkinter as tk


class Frame(tk.Frame, ABC):
    '''The abstract class of a screen frame'''

    @abstractmethod
    def on_switch(self):
        '''Being called when the window is switched to self'''
