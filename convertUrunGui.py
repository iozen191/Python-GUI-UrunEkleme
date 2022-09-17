from PyQt5 import uic

with open("urunGui.py","w",encoding="utf-8") as file:
    uic.compileUi("urunGui.ui",file)