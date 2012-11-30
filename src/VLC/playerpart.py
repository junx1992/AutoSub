import wx # 2.8
import wx.lib.platebtn as pbtn
import wx.lib.stattext as stattext
import sys
import myvlc.vlc as vlc
import os
import user

class PlayerPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,-1)

        # Attribute
        myfont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL,False, u'Segoe UI')
        Backgroud=(57,59,66)
        Fontcolor=(229,229,229)
        bback=(77,77,77)
        ctrlpanelcolor=(51,51,51)

        #Panels
        # This is the subtitlepanel
        self.subtitlepanel=wx.Panel(self, -1);

        # The first panel of the video
        self.videopanel = wx.Panel(self, -1)
        self.videopanel.SetBackgroundColour(wx.BLACK)

        # The second panel holds controls
        self.ctrlpanel = wx.Panel(self, -1 )        
        self.ctrlpanel.SetBackgroundColour(ctrlpanelcolor)


        #  functions

        #  timeslider
        self.timeslider = wx.Slider(self.ctrlpanel, -1, 0, 0, 1000,size=(500,20)) #timeline
        self.timeslider.SetRange(0, 1000)
                
        #  buffergauge
        self.buffergauge = wx.Gauge(self.ctrlpanel, -1,1000,size=(500,5)) 
        self.buffergauge.SetRange(1000)
                
        #  display time                                                                          
        self.displaytime=stattext.GenStaticText(self.ctrlpanel, -1, "00:00/00:00",style=wx.ALIGN_RIGHT)                
        self.displaytime.SetFont(myfont)

        #  pause button                              
        pausebmp=wx.Bitmap("./Icons/pause.png",wx.BITMAP_TYPE_PNG)
        pausebmp.SetSize(size=(40,40))                
        #  play button
        playbmp=wx.Bitmap("./Icons/play.png",wx.BITMAP_TYPE_PNG)                
        playbmp.SetSize(size=(40,40))                
        self.play   = pbtn.PlateButton(self.ctrlpanel)                            
        self.play.SetBitmap(bmp=playbmp)                             
                
        #  volume button
        self.volume = pbtn.PlateButton(self.ctrlpanel)                
        volumebmp=wx.Bitmap("./Icons/volume.png",wx.BITMAP_TYPE_PNG)
        self.volume.SetSize((20,20))
        self.volume.SetBitmap(bmp=volumebmp)
        #  fullscreen button
        self.fullscreen = pbtn.PlateButton(self.ctrlpanel)                
        fullscreenbmp=wx.Bitmap("./Icons/fullscreen.png", wx.BITMAP_TYPE_PNG)
        self.fullscreen.SetSize(size=(20,20))
        self.fullscreen.SetBitmap(bmp=fullscreenbmp)
        #  right button
        self.right=pbtn.PlateButton(self.ctrlpanel)                
        rightbmp=wx.Bitmap("./Icons/right.png",wx.BITMAP_TYPE_PNG)
        self.right.SetSize(size=(20,20))
        self.right.SetBitmap(bmp=rightbmp)
        #  left button
        self.left=pbtn.PlateButton(self.ctrlpanel)                
        leftbmp=wx.Bitmap("./Icons/left.png",wx.BITMAP_TYPE_PNG)
        self.left.SetSize(size=(20,20))
        self.left.SetBitmap(bmp=leftbmp)
        #  voice slider
        self.volslider = wx.Slider(self.ctrlpanel, -1, 0, 0, 100, size=(83, -1))

        """Bind Control to Events"""
        self.Bind(wx.EVT_BUTTON, self.OnPlayButton, self.play)                          
        self.Bind(wx.EVT_BUTTON, self.OnToggleVolume, self.volume)
        self.Bind(wx.EVT_SLIDER, self.OnSetVolume, self.volslider)
        self.Bind(wx.EVT_SLIDER, self.OnSetPlayTime, self.timeslider)
        #self.Bind(wx.EVT_BUTTON, self.OnToggleFullScreen, self.fullscreen)                
        self.Bind(wx.EVT_BUTTON, self.OnRight,self.right)
        self.Bind(wx.EVT_BUTTON, self.OnLeft, self.left)

        # Do the Layout
        self.__DoLayout__()
        self.SetBackgroundColour(ctrlpanelcolor)


        # finally create the timer, which updates the timeslider
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # VLC player controls
        self.Instance = vlc.Instance('--subsdec-encoding=GB18030','--freetype-font=PMingLiU')
        self.player = self.Instance.media_player_new()

        self.Bind(wx.EVT_CLOSE,self.OnExit)

        # Set the Fast Key
        acceltbl=wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('O'),1),(wx.ACCEL_CTRL,ord('C'),2),(wx.ACCEL_CTRL,ord('P'),3),(wx.ACCEL_CTRL,ord('A'),4),(wx.ACCEL_CTRL,ord('S'),5),(wx.ACCEL_CTRL,ord('F'),6),(wx.ACCEL_CTRL,ord('V'),7)])
        self.SetAcceleratorTable(acceltbl)

    def __DoLayout__(self):
        
        # ctrlbox
        ctrlbox=wx.GridBagSizer(vgap=0, hgap=0)
        ctrlbox.Add(self.displaytime,(0,1))                
        ctrlbox.Add(self.volume,(0,8))                
        ctrlbox.Add(self.volslider,(0,9))
        ctrlbox.Add(self.timeslider,(1,0),span=(1,10),flag=wx.EXPAND)
        ctrlbox.Add(self.buffergauge,(2,0),span=(1,10),flag=wx.EXPAND)                
        ctrlbox.Add(self.left,(4,5))
        ctrlbox.Add(self.play,(4,6))               
        ctrlbox.Add(self.right,(4,7))
        ctrlbox.Add(self.fullscreen,(4,9),flag=wx.ALIGN_BOTTOM|wx.ALIGN_CENTER)
        ctrlbox.AddGrowableCol(0)
        ctrlbox.AddGrowableCol(1)
        ctrlbox.AddGrowableCol(2)
        ctrlbox.AddGrowableCol(3)
        ctrlbox.AddGrowableCol(4)
        ctrlbox.AddGrowableCol(5)
        ctrlbox.AddGrowableCol(6)
        ctrlbox.AddGrowableCol(7)
        ctrlbox.AddGrowableCol(8)
        ctrlbox.AddGrowableCol(9)
        self.ctrlpanel.SetSizer(ctrlbox)
        # together
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        sizer.Add(self.ctrlpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        self.SetSizer(sizer)
    
    def OnExit(self, evt):
        self.player.stop()
        self.Close()
        evt.Skip()

    def OnOpen(self, evt):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.OnStop(None)

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        dlg = wx.FileDialog(self, "Choose a file", user.home, "","*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
                dirname = dlg.GetDirectory()
                filename = dlg.GetFilename()
                # Creation
                self.mediapath=unicode(os.path.join(dirname, filename))
                self.Media = self.Instance.media_new(self.mediapath)
                #m=self.Instance.media_new(r'D:\shiyan\number3\New folder\1.rmvb')
                self.player.set_media(self.Media)
                # Report the title of the file chosen
                title = self.player.get_title()
                #  if an error was encountred while retriving the title, then use
                #  filename
                if title == -1:
                        title = filename
                #self.SetTitle("%s - AutoSub" % title)

                # set the window id where to render VLC's video output
                self.player.set_hwnd(self.videopanel.GetHandle())
                # set the volume slider to the current volume
                self.volslider.SetValue(self.player.audio_get_volume() / 2)                        
                self.title=title             

                # finally destroy the dialog
                dlg.Destroy()
                
                # create the new dialog to choose the recognization and translation
                self.select_dialog=SelectDialog(None,"Choice")
                self.select_dialog.ShowModal()
                # Finally Play~FIXME: this should be made cross-platform
                self.OnPlay(None)
                #self.Spec.GetAddr(self.Spec,self.mediapath)                        
        else:
                dlg.Destroy()

    def OnPlay(self, evt):
        """Toggle the status to Play/Pause.

        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # wx.FileDialog to select a file
        if not self.player.get_media():
                self.OnOpen(None)
        else:
                # Try to launch the media, if this fails display an error message
                if self.player.play() == -1:
                        self.errorDialog("Unable to play.")
                else:
                        self.timer.Start(100)
                                

    def OnPlayButton(self,evt):
        pausebmp=wx.Bitmap("./Icons/pause.png",wx.BITMAP_TYPE_PNG)
        pausebmp.SetSize(size=(40,40))

        playbmp=wx.Bitmap("./Icons/play.png",wx.BITMAP_TYPE_PNG)                
        playbmp.SetSize(size=(40,40))    
                
        if not self.player.get_media():
                self.OnOpen(None)
                self.play.SetBitmap(bmp=pausebmp)
        else:
                self.OnPause(self)
                if self.player.is_playing()==True:                                                           
                        self.play.SetBitmap(bmp=playbmp)
                                
                else:                                
                        self.play.SetBitmap(bmp=pausebmp)                                

    def OnPause(self, evt):
            """Pause the player.
            """
            self.player.pause()

    def OnStop(self, evt):
            """Stop the player.
            """
            self.player.stop()
            # reset the time slider
            self.timeslider.SetValue(0)
            self.timer.Stop()

    def OnTimer(self, evt):
        """Update the time slider according to the current movie time.
        """
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        self.timeslider.SetRange(-1, length)
        self.buffergauge.SetRange(length)
                
        length_second=length/1000
        self.length_min=length_second/60
        self.length_sec=length_second-self.length_min*60

        # update the time on the slider                
        time = self.player.get_time()
        self.timeslider.SetValue(time)

        # update the displaytime 
        second=time/1000
        self.current_min=second/60
        self.current_second=second-self.current_min*60

        # give the time to spec
        #self.Spec.CurrPos(self.Spec,time)


                
        if self.current_min<10:
                str_min="0"+str(self.current_min)
        else:
                str_min=str(self.current_min)
        if self.current_second<10:
                str_sec="0"+str(self.current_second)
        else:
                str_sec=str(self.current_second)
                        
        if self.length_min<10:
                str_length_min="0"+str(self.length_min)
        else:
                str_length_min=str(self.length_min)
        if self.length_sec<10:
                str_length_sec="0"+str(self.length_sec)
        else:
                str_length_sec=str(self.length_sec)
                self.displaytime.SetLabel(str_min+":"+str_sec+"/"+str_length_min+":"+str_length_sec)

        #spectoright
        #ll=self.Spec.GetLeft(self.Spec)
                
        #if(ll!="-1"):
                #self.subpanel.SetLeft(self.subpanel,ll)
        #rr=self.Spec.GetRight(self.Spec)
        #if(rr!="-1"):
                #self.subpanel.SetRight(self.subpanel,rr)
                

    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()
        self.player.audio_set_mute(not is_mute)
        if is_mute==True:
                mutebmp=wx.Bitmap("./Icons/volume.png",wx.BITMAP_TYPE_PNG)
                self.volume.SetSize((20,20))
                self.volume.SetBitmap(bmp=mutebmp)
        else:
                notmutebmp=wx.Bitmap("./Icons/no_volume.png",wx.BITMAP_TYPE_PNG)
                self.volume.SetSize((20,20))
                self.volume.SetBitmap(bmp=notmutebmp)
                
        self.volslider.SetValue(self.player.audio_get_volume() / 2)

    def OnSetVolume(self, evt):
        """Set the volume according to the volume sider.
        """
        volume = self.volslider.GetValue() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if self.player.audio_set_volume(volume) == -1:
                self.errorDialog("Failed to set volume")


    def OnSetPlayTime(self, evt):
        """Set the progress of the movie.
        """
        settime = self.timeslider.GetValue()
        self.player.set_time(settime)
                

    def OnSetBuffer(self, evt):                
        self.buffergauge.SetValue(self.timeslider.GetValue())
        pass


    def OnToggleFullScreen(self, evt):
        is_fullscreen=self.IsFullScreen()
        self.ShowFullScreen(show= not is_fullscreen)               


    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK|wx.ICON_ERROR)
        edialog.ShowModal()
    def OnFeedBack(self, evt):
        feedbackdialog=FeedBackDialog(None,"FeedBack")
        feedbackdialog.ShowModal()

    def OnRight(self, evt):                
        self.player.set_position(self.player.get_position()+0.03)
        evt.Skip()
        
    def OnLeft(self, evt):
        self.player.set_position(self.player.get_position()-0.03)
        evt.Skip()

class SelectDialog(wx.Dialog):
    def __init__(self,parent,title=""):
        super(SelectDialog,self).__init__(parent,title=title)

        # Attributes
        self.checkbox1=wx.CheckBox(self,label="Need Recognization")
        self.checkbox2=wx.CheckBox(self,label="Need Translation")
        src_lan=["English","Japanese"]
        tran_lan=["Chinese","Japanese","English"]
        self.recg_box=wx.ComboBox(self,-1,value="English",choices=src_lan,style=wx.CB_READONLY)
        self.tran_box=wx.ComboBox(self,-1,value="Chinese",choices=tran_lan,style=wx.CB_READONLY)
        self.button=wx.Button(self,wx.ID_OK)                
        self.button.SetDefault()
        self.isrecognize=False
        self.istranslate=False

        # Layout
        self.__DoLayout()
        self.SetInitialSize()

        # Bind Event  
        self.Bind(wx.EVT_BUTTON,self.OnDecide,self.button)                

    def __DoLayout(self):
        sizer=wx.GridBagSizer(vgap=8,hgap=8)                
        sizer.Add(self.checkbox1,(1,1))
        sizer.Add(self.checkbox2,(3,1))
        sizer.Add(wx.StaticText(self,-1,"Source Language:"),(1,2))
        sizer.Add(wx.StaticText(self,-1,"Target Language:"),(3,2))
        sizer.Add(self.recg_box,(1,3))
        sizer.Add(self.tran_box,(3,3))
        sizer.Add((1,4),(1,5))
        sizer.Add((3,4),(3,5))
        sizer.Add(self.button,(5,2))                
        self.SetSizer(sizer)

        
    def OnDecide(self,evt):
        self.sorcelan=self.recg_box.GetValue()
        self.targetlan=self.tran_box.GetValue()        
        if self.checkbox1.GetValue()==True:
                self.isrecognize=True                
        if self.checkbox2.GetValue()==True:
                self.istranslate=True
        self.Destroy()
                             
        
                
class FeedBackDialog(wx.Dialog):
    def __init__(self,parent,title=""):
        super(FeedBackDialog,self).__init__(parent,title=title)

        # Attributes
        self.mail=wx.TextCtrl(self)
        self.suggestion=wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.button=wx.Button(self,wx.ID_OK)
        self.button.SetDefault()

        # Layout
        self.__DoLayout()
        self.SetInitialSize()
                
    def __DoLayout(self):
        sizer = wx.GridBagSizer(vgap=8, hgap=8)
        mail_lbl = wx.StaticText(self, label="ContactMail:")
        suggestion_lbl = wx.StaticText(self, label="Suggestions:")
        # Add the event type fields
        sizer.Add(mail_lbl, (1, 1))
        sizer.Add(self.mail, (1, 2), (1, 15), wx.EXPAND)
        # Add the details field
        sizer.Add(suggestion_lbl, (2, 1))
        sizer.Add(self.suggestion, (2, 2), (5, 15), wx.EXPAND)
        # Add a spacer to pad out the right side
        sizer.Add((5, 5), (2, 17))
        # And another to the pad out the bottom
        sizer.Add((5, 5), (7, 0))
        sizer.Add(self.button,(7,7))
        self.SetSizer(sizer)
    def GetMail(self):
        return self.mail.GetValue()
    def GetSuggestion(self):
        return self.suggestion.GetValue() 

class SimFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Frame")
        self.panel=PlayerPanel(self)
        self.SetSize((600,600))

if __name__=='__main__':
        app = wx.PySimpleApp()
        frame = SimFrame()
        frame.Show()
        app.MainLoop()
