# -*- coding: cp936 -*-
import wx
from pylab import *

import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.cm as cm



class ImageWindow(wx.ScrolledWindow):


    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(5,5)
        self.LeftClickFlag=0
        self.RightClickFlag=0
        self.CurrPos=0
        #self.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.OnScroll)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        #ADD MOUSE DRAG EVENT TO REPLACE SCROLLING
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.overlay=wx.Overlay()
        #ruler=RC.RulerCtrl(self, -1, pos=(0, np.size(specW, axis=0)), size=(np.size(specW , axis = 1),1),orient=wx.HORIZONTAL, style=wx.NO_BORDER)
        #ruler.SetFlip(flip=True)
        #ruler.SetRange(0, np.size(specW , axis = 1))

    def SetBitmap(self, bitmap):
        self.bitmap = bitmap
        #self.buffer = wx.EmptyBitmap(bitmap.GetWidth(), bitmap.GetHeight()+15)
        self.buffer = self.bitmap
        self.SetScrollbars(1,0, self.bitmap.GetWidth(), 200)


    def OnPaint(self, event):
        #dc = wx.BufferedPaintDC(self, self.bitmap)
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        #dc.DrawBitmap(self.bitmap, 0, 0)
        odc=wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        if self.LeftClickFlag==1:
            dc.SetPen(wx.Pen('red', 1))
            dc.DrawLine(self.LeX,0,
                        self.LeX, 150)
        if self.RightClickFlag==1:
            dc.SetPen(wx.Pen('blue',1))
            dc.DrawLine(self.RiX,0,
                        self.RiX, 150)
        #Draw a transparent rectangle to emphasize the selected area
        if(self.LeftClickFlag == 1 and self.RightClickFlag == 1 and self.LeX!=self.RiX):
            Colour = wx.Colour(139, 0, 255, 100) #notice the alpha channel
            brush = wx.Brush(Colour)
            if self.RiX > self.LeX:
                width = self.RiX - self.LeX
                x = self.LeX
            else:
                width = self.LeX- self.RiX
                x = self.RiX
            height  = self.bitmap.GetHeight()
            pdc = wx.GCDC(dc)
            pdc.SetBrush(brush)
            pdc.DrawRectangle(x, 0, width, height)
        dc.SetPen(wx.Pen('yellow',1))
        dc.DrawLine(-self.CalcScrolledPosition(0,0)[0] + 150, 0, -self.CalcScrolledPosition(0,0)[0] + 150, 150)
        dc.SetPen(wx.Pen('green',1))
        dc.DrawLine(self.CurrPos, 0, self.CurrPos, 150)
        del odc
    



    def OnMouseClick(self, event):
        #print event.GetLogicalPosition(self.cdc)
        self.LeftClickFlag = 1
        self.OLeX=event.X -self.CalcScrolledPosition(0,0)[0]
        self.LeX = self.OLeX
        self.Startx = self.LeX
        self.Refresh()
        #self.CaptureMouse()
        #del odc
        event.Skip()

    def OnLeftUp(self, event):
        self.Endx = event.X - self.CalcScrolledPosition(0,0)[0]
        if self.Endx != self.Startx:
            self.Scroll(-self.CalcScrolledPosition(0,0)[0] + self.Endx - self.Startx, 0)
        event.Skip()

    def OnRightClick(self, event):
        self.RightClickFlag = 1
        self.ORiX=event.X - self.CalcScrolledPosition(0,0)[0]
        self.RiX = self.ORiX
        self.Startr = self.RiX
        self.Refresh()
        event.Skip()

    def OnRightUp(self, event):
        self.Endr = event.X - self.CalcScrolledPosition(0,0)[0]
        if self.Endr != self.Startr:
            self.Scroll(-self.CalcScrolledPosition(0,0)[0] + self.Endr - self.Startr, 0)
        event.Skip()


class SimFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Frame")
        self.panel=SpecPanel(self)
        self.SetSize((360,200))


class SpecPanel(wx.Panel):
    def __init__(self,parent,iconadd='./Icon/speceg.jpg'):

        wx.Panel.__init__(self,parent,-1)

        self.Spec_Flag = 0
        Background=(57,59,66)
        myfont = wx.Font(10,wx.SWISS, wx.NORMAL, wx.NORMAL,False,u'Segoe UI')
        myfont_small = wx.Font(8,wx.SWISS, wx.NORMAL, wx.NORMAL,False,u'Segoe UI')
        back = (77,77,77)
        FontColour=(229,229,229)
        self.orim = wx.Image(iconadd, wx.BITMAP_TYPE_JPEG)
        
        #SET THE DEFAULT VALUE OF THE SLIDER POS
        self.pos = 200

        self.panel = wx.Panel(self, -1)

        self.ratio = self.orim.GetLength()/self.VideoLen*60

        self.sld = wx.Slider(self.panel, value = 200, minValue = 150, maxValue =500,
            size=(10, 25), style=wx.SL_VERTICAL | wx.SL_AUTOTICKS|wx.SL_LABELS, name='width')
        self.sld.SetTickFreq(20, 1)
        self.sld1 = wx.Slider(self.panel, value = 200, minValue = 150, maxValue =500,
            size=(10, 25), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.sld1.SetTickFreq(20, 1)

        self.Bind(wx.EVT_MENU, self.LeftButton, id=1)
        self.Bind(wx.EVT_MENU, self.RightButton, id=2)
        self.Bind(wx.EVT_MENU, self.LeftText, id=1)
        acceltbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('Z'),1),(wx.ACCEL_CTRL,ord('X'),2)])
        self.SetAcceleratorTable(acceltbl)

        #ADD TWO BUTTONS TO MANIPULATE THE LEFT AND RIGHT BORDER
        self.button1 = wx.Button(self.panel, id=1, label='left',  size = (30,15))
        self.button2 = wx.Button(self.panel, id=2, label='right',  size = (30,15))
        self.button3 = wx.Button(self.panel, id=3, label='start', size = (40,15))
        self.button1.SetFont(myfont)
        self.button1.SetBackgroundColour(back)
        self.button1.SetForegroundColour(FontColour)
        self.button2.SetFont(myfont)
        self.button2.SetBackgroundColour(back)
        self.button2.SetForegroundColour(FontColour)
        self.button3.SetFont(myfont)
        self.button3.SetBackgroundColour(back)
        self.button3.SetForegroundColour(FontColour)
        self.button1.Bind(wx.EVT_BUTTON, self.LeftButton)
        self.button2.Bind(wx.EVT_BUTTON, self.RightButton)
        #self.button1.Bind(wx.EVT_BUTTON, self.LeftText)
        #self.button2.Bind(wx.EVT_BUTTON, self.RightText)
        self.button3.Bind(wx.EVT_BUTTON, self.GetData)
        self.textleft = wx.TextCtrl(self.panel, id=3, size=(40, 20))
        self.textright = wx.TextCtrl(self.panel, id=4,  size=(40, 20))
        self.textmid = wx.TextCtrl(self.panel, id=5,  size=(40,20))
        self.textcurr = wx.TextCtrl(self.panel, id=6,  size=(40,20))
        self.textleft.SetBackgroundColour((57,59,66))
        self.textleft.SetFont(myfont_small)
        self.textleft.SetForegroundColour(FontColour)
        self.textright.SetBackgroundColour((57,59,66))
        self.textright.SetFont(myfont_small)
        self.textright.SetForegroundColour(FontColour)
        self.textmid.SetBackgroundColour((57,59,66))
        self.textmid.SetFont(myfont_small)
        self.textmid.SetForegroundColour(FontColour)
        self.textcurr.SetBackgroundColour((57,59,66))
        self.textcurr.SetFont(myfont_small)
        self.textcurr.SetForegroundColour(FontColour)

            
        self.im = self.orim
        self.bm = self.im.ConvertToBitmap()


        self.wind = ImageWindow(self)
        self.wind.SetBitmap(self.im.ConvertToBitmap())
        self.wind.Refresh()
        self.wind.SetScrollbars(1,0, self.im.GetWidth(), 200)
        wx.EVT_SLIDER(self.sld, self.sld.GetId(),self.sliderUpdate1)
        wx.EVT_SLIDER(self.sld1, self.sld1.GetId(),self.sliderUpdate2)
        #UPDATE THE TEXT ON LEFT CLICKING
        self.wind.Bind(wx.EVT_LEFT_UP, self.LeftText)
        self.wind.Bind(wx.EVT_RIGHT_UP, self.RightText)
        self.wind.Bind(wx.EVT_SCROLLWIN, self.MidText)
        self.wind.Bind(wx.EVT_LEFT_UP, self.MidText)
        self.wind.Bind(wx.EVT_RIGHT_UP, self.MidText)
        self.sld1.Bind(wx.EVT_SLIDER, self.sliderUpdate2)
        #self.wind.Bind(wx.EVT_TIMER, self.CurrText, self.wind.timer)
        self.wind.FitInside()
        #self.wind.SetScrollbars(1,0, self.im.GetWidth(), 200)


        sizer = wx.GridBagSizer(vgap=0, hgap =0)
        sizer.Add(self.button1, (0,0), flag = wx.EXPAND)
        sizer.Add(self.button2,(0,2),flag = wx.EXPAND)
        sizer.Add(self.button3, (0,4),flag = wx.EXPAND)
        sizer.Add(self.textleft, (1,4),flag = wx.EXPAND)
        sizer.Add(self.textright, (2,4),flag = wx.EXPAND)
        sizer.Add(self.textmid, (3,4),flag = wx.EXPAND)
        sizer.Add(self.textcurr, (4,4),flag = wx.EXPAND)
        sizer.Add((0,5),(1,5))
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableCol(4)
        sizer.AddGrowableCol(5)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.SetMinSize((100,100))
        sizer.Add(self.sld, (1,0),(4,1),flag = wx.EXPAND)
        sizer.Add(self.sld1, (1,2),(4,1),flag = wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.panel.SetMinSize((100,200))
        Bigsizer = wx.BoxSizer()
        self.wind.SetMinSize((150,200))
        Bigsizer.Add(self.wind,proportion=3, flag=wx.ALL|wx.EXPAND)
        Bigsizer.Add(self.panel,proportion=2, flag=wx.ALL|wx.EXPAND)
        self.SetSizer(Bigsizer)
        self.SetBackgroundColour(Background)

    def GetLength(self, event, length):
        self.VideoLen = length

    def OpenData(self,event, handle):
        self.handle = handle

    def GetAddr(self, event, path):
        self.addr = path
    
    def GetData(self,event):
        Num = 0

        while self.handle.more_data():
            iter = 0
            q = []
            pos, n, q = self.handle.read(1000, q)
            for p in q:
                if iter == 0:
                    temp = p.T[::-1]
                    vector = np.log10(temp + 1)
                else:
                    temp = p.T[::-1]
                    vector = np.append(vector, np.log10(temp + 1), axis =1)
                iter = iter +1
                #plt.imshow(np.log(p.T+1))
                #plt.show()
            vector = vector/np.amax(vector)
            vector = [vector, vector, vector]
            vector = np.dstack(vector)
            #plt.imsave(path, vector, cmap = cm.gray)
            im = wx.ImageFromBuffer(int(np.size(vector, axis = 1)), int(np.size(vector, axis = 0)), np.uint8(vector))
            if Num == 0:
                self.specW = vector
                list = [vector]
            else:
                self.specW = np.append(self.specW, vector, axis = 1)
                list.append(vector)
            Num = Num + 1

        self.spec = self.specW*255.0
            
        self.orim = wx.ImageFromBuffer(int(np.size(self.spec , axis = 1)), int(np.size(self.spec, axis = 0)), np.uint8(self.spec))
        self.orim = self.orim.Rescale(self.orim.GetWidth(), 140)
        self.wind.overlay.Reset()
        self.wind.SetBitmap(self.orim.ConvertToBitmap())
        self.Spec_Flag =1
        self.im = self.orim
        self.bm = self.im.ConvertToBitmap()

    
    def sliderUpdate1(self, event):
        self.pos = self.sld.GetValue()
        self.wind.overlay.Reset()
        if self.Spec_Flag == 1:
            self.orim = wx.ImageFromBuffer(int(np.size(self.spec , axis = 1)), int(np.size(self.spec, axis = 0)), np.uint8(self.spec))
        else:
            self.orim = wx.Image('./Icon/speceg.jpg', wx.BITMAP_TYPE_JPEG)
        NWID = round(self.bm.GetWidth() * self.pos/200.0)
        NHET = round(self.im.GetHeight())
        self.im = self.orim.Rescale(NWID ,NHET)
        self.wind.SetBitmap(self.im.ConvertToBitmap())
        self.wind.SetScrollbars(1,0, self.im.GetWidth(), 200)
        if self.wind.LeftClickFlag == 1:
            self.wind.LeX = self.wind.OLeX*self.pos/200.0
            self.LeftText(event)
        if self.wind.RightClickFlag == 1:
            self.wind.RiX = self.wind.ORiX*self.pos/200.0
            self.RightText(event)
        self.wind.Refresh()
        if self.wind.LeftClickFlag == 1:
            self.wind.Scroll(self.currx*self.pos/200.0, 0)

    def sliderUpdate2(self, event):
        self.pos = self.sld1.GetValue()
        self.wind.Refresh()
        if self.Spec_Flag ==  1:
            self.wind.overlay.Reset()
            self.spec = self.specW*self.pos
            self.im = wx.ImageFromBuffer(int(np.size(self.spec, axis = 1)), int(np.size(self.spec, axis = 0)), np.uint8(self.spec))
            self.im=self.im.Rescale(self.im.GetWidth(), 140)
            self.wind.SetBitmap(self.im.ConvertToBitmap())
        else:
            pass


    def LeftButton(self, event):
        if self.wind.LeftClickFlag == 1:
            self.wind.LeX = self.wind.LeX -self.pos/200.0
            self.wind.Refresh()
        #event.Skip()
        self.LeftText(event)
        event.Skip()

    def RightButton(self, event):
        if self.wind.RightClickFlag == 1:
            self.wind.RiX = self.wind.RiX +self.pos/200.0
            self.wind.Refresh()
        self.RightText(event)
        event.Skip()

    def LeftText(self, event):
        self.textleft.Clear()
        if self.wind.LeftClickFlag ==1:
            time = self.wind.LeX/self.ratio/self.pos*200
            lefttext=str(int(time/60/60))+":"+str(int(time/60%60))+":"+str(int(time%60)) + "."+str(int(((round(time, 2) - int(time))*100)))
            self.leftstr=lefttext
            self.textleft.WriteText(str(int(time/60/60))+":"+str(int(time/60%60))+":"+str(int(time%60)) + "."+str(int(((round(time, 2) - int(time))*100))))
        #event.Skip()
        return
        

    def RightText(self, event):
        self.textright.Clear()
        if self.wind.RightClickFlag==1:
            time = self.wind.RiX/self.ratio/self.pos*200
            righttext=str(int(time/60/60))+":"+str(int(time/60%60))+":"+str(int(time%60)) + "."+str(int(((round(time, 2) - int(time))*100)))
            self.rightstr=righttext
            self.textright.WriteText(str(int(time/60/60))+":"+str(int(time/60%60))+":"+str(int(time%60)) + "."+str(int(((round(time, 2) - int(time))*100))))
        #event.Skip()
        return
        
    def GetLeft(self,event):
        try:
            return self.leftstr
        except:
            return "-1"
    def GetRight(self,event):
        try:
            return self.rightstr
        except:
            return "-1"
    def MidText(self, event):
        self.textmid.Clear()
        time = (-self.wind.CalcScrolledPosition(0,0)[0] + 150)/self.ratio*200.0/self.pos
        self.textmid.WriteText(str(int(time/60/60))+":"+str(int(time/60%60))+":"+str(int(time%60))+ ":"+str(int(((round(time, 2) - int(time))*100))))
        self.currx = -self.wind.CalcScrolledPosition(0,0)[0]
        self.wind.Refresh()
        event.Skip()

    def GetLeftLex(self,event,lefttime):
        self.wind.LeftClickFlag =1    
        self.wind.LeX=lefttime*self.ratio
        self.wind.Scroll(self.wind.LeX - 50, 0)
        self.LeftText(event)
        self.wind.Refresh()

    def GetRightLex(self,event,righttime):
        self.wind.RightClickFlag =1
        self.wind.RiX=righttime*self.ratio
        self.RightText(event)
        self.wind.Refresh()

    """def CurrText(self, event):
        self.textcurr.Clear()
        time = (self.wind.CurrPos) * 200.0/self.pos/self.ratio
        self.textcurr.WriteText(str(int(time/60/60))+":"+str(int(time/60%60))+":"+str(int(time%60))+ ":"+str(int(((round(time, 2) - int(time))*100))))
        event.Skip()"""

    def CurrPos(self, event, milisec):
        self.textcurr.Clear()
        time = milisec
        self.textcurr.WriteText(str(int(time/1000/60/60)) +":" +str(int(time/1000/60%60)) + ":" +str(int(time/1000%60)) +":" +str(int(time%1000)))
        self.wind.CurrPos = time/1000*self.ratio
        self.wind.Refresh()
        


if __name__=='__main__':
        app = wx.PySimpleApp()
        f = SimFrame()
        f.Show()
        app.MainLoop()

