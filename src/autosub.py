"""
Get the Main Frame and link the other
"""

import core.ffmpeg_decoder as fd
import core.sub_generator as sg
import core.spectrum as sp
import sys
import wx
from core.naive_vad2 import *
from VLC.playerpart import *
from VLC.spectrum_widget.SpecWin import *
from VLC.subtitle_widget.SubtitleEditor import *
sys.path.append("/VLC")

class MainFrame(wx.Frame):
    """ The Main Window"""
    def __init__(self,title):
        frame=wx.Frame.__init__(self,None,-1,title)        
        # Attribute
        myfont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL,False, u'Segoe UI')
        Backgroud=(57,59,66)
        Fontcolor=(229,229,229)
        bback=(77,77,77)
        ctrlpanelcolor=(51,51,51)
        self.mainpanel=wx.Panel(self)
        self.playerpanel=PlayerPanel(self.mainpanel)
        self.subpanel=Subtitle(self.mainpanel,-1)
        self.spec=SpecPanel(self.mainpanel,"VLC/spectrum_widget/Icon/speceg.jpg")
        self.splitter = wx.SplitterWindow(self.mainpanel, -1, style=wx.SP_3D)
        self.subtitle=None        
        self.ohandle=None
        self.dec=None
        self.vad=None
        self.sub=None
        self.specd=None        
        self.end=0
        # Menu
        #Menu Bar
        self.frame_menubar=wx.MenuBar()
        #  File Menu
        self.icon=wx.Icon('./VLC/Icons/autosub.ico',wx.wx.BITMAP_TYPE_ICO);
        self.SetIcon(self.icon);
        self.file_menu=wx.Menu()
        menu_open=self.file_menu.Append(-1,"&Open \tCtrl+O")
        self.file_menu.AppendSeparator()
        menu_close=self.file_menu.Append(-1,"&Close \tCtrl+C")        
        self.frame_menubar.Append(self.file_menu, "&File")
        #  Edit Menu
        self.edit_menu=wx.Menu()
        menu_play=self.edit_menu.Append(-1,"&Play \tCtrl+P")
        self.edit_menu.AppendSeparator()
        menu_pause=self.edit_menu.Append(-1,"P&ause \tCtrl+A")
        self.edit_menu.AppendSeparator()
        menu_stop=self.edit_menu.Append(-1,"&Stop \tCtrl+S")
        self.edit_menu.AppendSeparator()
        menu_fullscreen=self.edit_menu.Append(-1,"&FullScreen \tCtrl+F")
        self.edit_menu.AppendSeparator()
        menu_volume=self.edit_menu.Append(-1,"&Volume \tCtrl+V")
        self.edit_menu.AppendSeparator()
        self.frame_menubar.Append(self.edit_menu, "&Edit")

        #  Sub Menu
        self.sub_menu=wx.Menu()
        op=self.sub_menu.Append(-1,"Open Subtitle")
        self.sub_menu.AppendSeparator()
        sa=self.sub_menu.Append(-1,"Save Subtitle")
        self.frame_menubar.Append(self.sub_menu, "Subtitle")
        #  Help Menu
        self.help_menu=wx.Menu()                
        menu_feedback=self.help_menu.Append(-1,"&FeedBack")
        self.help_menu.AppendSeparator()
        self.frame_menubar.Append(self.help_menu, "Help")
        self.SetMenuBar(self.frame_menubar)   

        # Bind Event
        #  Menu Bind
        self.Bind(wx.EVT_MENU, self.OnPlayButton, menu_open)
        self.Bind(wx.EVT_MENU, self.playerpanel.OnExit, menu_close)
        self.Bind(wx.EVT_MENU, self.OnPlayButton, menu_play)
        self.Bind(wx.EVT_MENU, self.playerpanel.OnPause, menu_pause)
        self.Bind(wx.EVT_MENU, self.playerpanel.OnStop, menu_stop)
        self.Bind(wx.EVT_MENU, self.OnToggleFullScreen, menu_fullscreen)
        self.Bind(wx.EVT_MENU, self.playerpanel.OnToggleVolume, menu_volume)
        self.Bind(wx.EVT_MENU, self.playerpanel.OnFeedBack, menu_feedback)
        self.Bind(wx.EVT_MENU, self.subpanel.OpenFile, op)
        self.Bind(wx.EVT_MENU, self.SaveSubtitle, sa)
        
        self.subpanel.Bind(wx.EVT_LISTBOX_DCLICK,self.Select,self.subpanel.listBox)
        self.Bind(wx.EVT_BUTTON,self.OnToggleFullScreen,self.playerpanel.fullscreen)
        self.playerpanel.Bind(wx.EVT_BUTTON,self.OnPlayButton,self.playerpanel.play)
        self.playerpanel.Bind(wx.EVT_TIMER, self.OnTimer, self.playerpanel.timer)
        self.Bind(wx.EVT_CLOSE,self.OnExit)
        
        #self.Bind(wx.EVT_MAXIMIZE, self.RePaint,self)
        #self.Bind(wx.EVT_SIZE,self.RePaint,self)

        # Layout
        self.__DoLayout__()
        self.flag=False
        self.mainpanel.SetBackgroundColour(wx.BLACK)
        
    def __DoLayout__(self):    
        self.subpanel.Show()
        self.spec.Show()
        self.splitter.Show()
        BigSizer=wx.GridBagSizer(hgap=0,vgap=0)
        BigSizer.Add(self.subpanel,(0,0),flag=wx.EXPAND)
        BigSizer.Add(self.spec,(1,0),flag=wx.EXPAND)
        BigSizer.Add(self.splitter,(0,1),(2,1))
        BigSizer.Add(self.playerpanel,(0,2),(2,1),flag=wx.EXPAND)

        BigSizer.AddGrowableRow(0,5)
        BigSizer.AddGrowableRow(1,2)
        BigSizer.AddGrowableCol(0,3)        
        BigSizer.AddGrowableCol(2,4)
        self.mainpanel.SetSizer(BigSizer)
        self.SetMinSize((1020,650))        
        self.Centre()
        #self.DoPaint()
        self.Refresh()

    def __DoLayoutTwo__(self):
        self.subpanel.Hide()
        self.spec.Hide()
        self.splitter.Hide()
        BigSizer=wx.GridBagSizer(hgap=0,vgap=0)
        BigSizer.Add(self.playerpanel,(0,0),flag=wx.EXPAND)
        BigSizer.AddGrowableRow(0)
        BigSizer.AddGrowableCol(0)
        self.mainpanel.SetSizer(BigSizer)
        self.SetMinSize((1020,650))        
        self.Centre()
        #self.DoPaint()
        
        

    def Select(self,evt):
        self.subpanel.ChooseOneItem(self.subpanel)
        begintime=self.subpanel.begintime.GetValue()
        endtime=self.subpanel.endtime.GetValue()                
        tmp_begin=begintime.split(':')
        tmp_end=endtime.split(':')
        if(len(tmp_begin)==3):
                begin_sec=int(tmp_begin[0])*60*60+int(tmp_begin[1])*60+float(tmp_begin[2])
                self.spec.GetLeftLex(self.spec,begin_sec)
        if(len(tmp_end)==3):
                end_sec=int(tmp_end[0])*60*60+int(tmp_end[1])*60+float(tmp_end[2])
                self.spec.GetRightLex(self.spec,end_sec)

    def OnOpen(self,evt):        
        self.playerpanel.OnOpen(None)
        self.bitmap.Hide()
        self.SetTitle("%s - AutoSub" % self.playerpanel.title)
        lan={"English":"en" ,"Chinese":"zh-cn" ,"Japanese":"ja"}
        lang_from = None
        lang_to = None
        source = None
        target = None
        if self.playerpanel.select_dialog.isrecognize==True:            
            # Set recognize parameter
            lang_from=lan[self.playerpanel.select_dialog.sorcelan]
            
        if self.playerpanel.select_dialog.istranslate==True:
            # Set translation parameter
            lang_to=lan[self.playerpanel.select_dialog.targetlan]

        source=self.playerpanel.mediapath
        # Set target name
        if not target:
            target = source[:source.rfind('.')] + '.srt'
        self.subtitle=target       
        
        self.currentfile=None
        
        self.dec = fd.ffmpeg_decoder(source,output_rate = 8000)
        self.vad = naive_vad(self.dec.ostream.get_handle())
        self.sub = sg.sub_generator(self.vad.ostream.get_handle(), source, target, lang_from = lang_from, lang_to = lang_to)
        
        self.ohandle = self.sub.ostream.get_handle()
        self.specd = sp.spectrum(self.dec.ostream.get_handle(), window_size = 1024)
        handle = self.specd.ostream.get_handle()
        #self.Spec.OpenData(self.Spec,self.ohandle)
        self.dec.start()
        self.vad.start()
        self.sub.start()
        self.specd.start()
        self.spec.OpenData(self.spec,handle)

    def SaveSubtitle(self,evt):
        self.subpanel.SaveFile(self.subpanel)
        self.playerpanel.player.video_set_subtitle_file(self.subpanel.filename)
        
    def OnPlayButton(self,evt):
        pausebmp=wx.Bitmap("./Icons/pause.png",wx.BITMAP_TYPE_PNG)
        pausebmp.SetSize(size=(40,40))
        playbmp=wx.Bitmap("./Icons/play.png",wx.BITMAP_TYPE_PNG)                
        playbmp.SetSize(size=(40,40))
        
                
        if not self.playerpanel.player.get_media():
                self.OnOpen(None)
                self.playerpanel.play.SetBitmap(bmp=pausebmp)
        else:
                self.playerpanel.OnPause(self)
                if self.playerpanel.player.is_playing()==True:                                                           
                        self.playerpanel.play.SetBitmap(bmp=playbmp)
                                
                else:                                
                        self.playerpanel.play.SetBitmap(bmp=pausebmp)

     # float second to time string 
    def OnFormatTime(self,floattime):
        time=int(floattime)
        str_decimaltime=str(int((floattime-time)*1000))
        sec=time%60
        all_min=time/60
        hour=all_min/60
        mini=all_min%60
        if sec<9:
            str_sec='0'+str(sec)
        else:
            str_sec=str(sec)
        if mini<9:
            str_min='0'+str(mini)
        else:
            str_min=str(mini)
        if hour<9:
            str_hour='0'+str(hour)
        else:
            str_hour=str(hour)

        string_time=str_hour+':'+str_min+':'+str_sec+'.'+str_decimaltime
        return string_time

    def OnTimer(self,evt):
        self.playerpanel.OnTimer(self.playerpanel)
        time = self.playerpanel.player.get_time()
        
        #give the time to spec
        self.spec.CurrPos(self.spec,time)
        #spectoright
        ll=self.spec.GetLeft(self.spec)
                
        if(ll!="-1"):
                self.subpanel.SetLeft(self.subpanel,ll)
        rr=self.spec.GetRight(self.spec)
        if(rr!="-1"):
                self.subpanel.SetRight(self.subpanel,rr)
                
        if self.ohandle.has_data(1):            
            (start,self.end,text)=self.ohandle.read(1)[2][0][0]            
            self.playerpanel.player.video_set_subtitle_file(self.subtitle)
            str_start=self.OnFormatTime(start)
            str_end=self.OnFormatTime(self.end)
            self.subpanel.AddSub(self.subpanel,str_start,str_end,text)
            # Set buffer time
        if self.playerpanel.player.get_length()!=0:
            self.playerpanel.buffergauge.SetValue(self.end*self.playerpanel.buffergauge.GetRange()*1000/self.playerpanel.player.get_length())

    def OnExit(self, evt):   
        self.playerpanel.player.stop()
        evt.Skip()
        self.Destroy()

    def DoPaint(self):        
        img=wx.Image("./Icons/StartPage.jpg", wx.BITMAP_TYPE_ANY)
        tempsize=self.playerpanel.videopanel.GetSize()                
        img.Rescale(width=tempsize.x,height=tempsize.y)
        img=img.ConvertToBitmap()
        self.bitmap=wx.StaticBitmap(self.playerpanel.videopanel,-1,img,(0,0))
        

    def RePaint(self,evt):
        evt.Skip()
        self.bitmap.Destroy()
        img=wx.Image("./Icons/StartPage.jpg", wx.BITMAP_TYPE_ANY)
        tempsize=self.playerpanel.videopanel.GetSize()
        #print tempsize
        img.Rescale(width=tempsize.x,height=tempsize.y)
        img=img.ConvertToBitmap()
        self.bitmap=wx.StaticBitmap(self.playerpanel.videopanel,-1,img,(0,0))        

    def OnToggleFullScreen(self,evt):
        self.flag=not self.flag
        if(self.flag==True):
            self.__DoLayoutTwo__()
        else:
            self.__DoLayout__()
        is_fullscreen=self.IsFullScreen()
        self.ShowFullScreen(show= not is_fullscreen)

class MyApp(wx.PySimpleApp):
    def __init__(self):
        app=wx.PySimpleApp.__init__(self)



if __name__ == '__main__':
        # Create a wx.App(), which handles the windowing system event loop
        app = MyApp()        
        # Create the window containing our small media player
        PlayerFrame = MainFrame("AutoSub")
        
        # Subtitle(PlayerFrame, title='Subtitle',positon=(1100,300))
        PlayerFrame.SetPosition((0,0))
        #app.SetTopWindow(PlayerFrame)
        # show the player window centred and run the application
        
        #PlayerFrame.Centre()
        
        PlayerFrame.Show() 
        app.MainLoop()
        
            
