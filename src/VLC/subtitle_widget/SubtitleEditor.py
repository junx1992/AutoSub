import wx
import os
from subtitleparser import *
from SubtitleUI import TestFrame
class Subtitle(wx.Panel):
    colLabels = ["homer", "marge", "bart", "lisa", "maggie"]
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.sizer=self.InitUI()
    def InitUI(self):       
        myfont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Segoe UI')
        Backgroud=(57,59,66)
        Fontcolor=(229,229,229)
        bback=(77,77,77)
        ctrlbar=wx.BoxSizer(wx.HORIZONTAL)

        self.save  = wx.Button(self, label="Save")
        self.save.SetFont(myfont)  
        self.save.SetBackgroundColour(bback)  
        self.save.SetForegroundColour(Fontcolor)  
 
        self.add   = wx.Button(self, label="Add")
        self.add.SetFont(myfont)   
        self.add.SetBackgroundColour(bback)  
        self.add.SetForegroundColour(Fontcolor)  

        self.delete = wx.Button(self,label="Delete")
        self.delete.SetFont(myfont)   
        self.delete.SetBackgroundColour(bback)  
        self.delete.SetForegroundColour(Fontcolor) 
                
        self.Bind(wx.EVT_BUTTON, self.SaveItem, self.save)
        self.Bind(wx.EVT_BUTTON, self.Additem, self.add)
        self.Bind(wx.EVT_BUTTON,self.deleteitem,self.delete)        
        textbox=wx.TextAttr(Fontcolor,Backgroud)
        
        self.begintext=wx.StaticText(self,-1,"Start Time:")
        self.begintext.SetFont(myfont)
        self.begintext.SetForegroundColour(Fontcolor)
        
        self.begintime=wx.TextCtrl(self,size=(250,25),style=wx.TE_RICH2)
        self.begintime.SetBackgroundColour((57,59,66))
        self.begintime.SetFont(myfont)
        self.begintime.SetForegroundColour(Fontcolor) 
        self.begintime.SetValue("00:00:00.000")

        self.endtext=wx.StaticText(self,-1,"End Time:")
        self.endtext.SetFont(myfont)
        self.endtext.SetForegroundColour(Fontcolor) 

        self.endtime=wx.TextCtrl(self,size=(250,25),style=wx.TE_RICH2)
        self.endtime.SetBackgroundColour((57,59,66))
        self.endtime.SetFont(myfont)
        self.endtime.SetForegroundColour(Fontcolor) 
        self.endtime.SetValue("00:00:00.000")

        self.text=wx.StaticText(self,-1,"Content")
        self.text.SetFont(myfont)
        self.text.SetForegroundColour(Fontcolor)
 
        self.TextCtrl=wx.TextCtrl(self, size=(250, 50),style=wx.TE_RICH2)
        self.TextCtrl.SetBackgroundColour((57,59,66))
        
        self.TextCtrl.SetDefaultStyle(textbox)
        self.TextCtrl.SetFont(myfont)
        self.TextCtrl.SetForegroundColour(Fontcolor)
        
        samplelist=['']
        self.listBox=wx.ListBox(parent=self,id=-1,size=(250,100),choices=samplelist,style=wx.LB_SINGLE)
        self.listBox.SetBackgroundColour(Backgroud)
        self.listBox.SetFont(myfont)
        self.listBox.SetForegroundColour(Fontcolor)

        self.SetBackgroundColour(Backgroud)
        self.__DoLayout__()        
        

    def __DoLayout__(self):
        sizer=wx.GridBagSizer(vgap=0, hgap=0)
        sizer.Add(self.begintext,(0,1))
        sizer.Add(self.begintime,(1,1),(1,5),wx.EXPAND)
        sizer.Add(self.endtext,(2,1))
        sizer.Add(self.endtime,(3,1),(1,5),wx.EXPAND)
        sizer.Add(self.text,(4,1))
        sizer.Add(self.TextCtrl,(5,1),(2,5),wx.EXPAND)
        sizer.Add(self.listBox,(8,1),(4,5),wx.EXPAND)
        sizer.Add(self.save,(12,1))
        sizer.Add(self.add,(12,3))
        sizer.Add(self.delete,(12,5))
        sizer.Add((1,6),(1,7))
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableRow(4)
        sizer.AddGrowableRow(5)
        sizer.AddGrowableRow(6)
        sizer.AddGrowableRow(7)
        sizer.AddGrowableRow(8)
        sizer.AddGrowableRow(9)
        sizer.AddGrowableRow(10)
        sizer.AddGrowableRow(11)
        sizer.AddGrowableRow(12)
       
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableCol(4)
        sizer.AddGrowableCol(5)
        sizer.AddGrowableCol(6)
        sizer.AddGrowableCol(7)
        #sizer.SetMinSize((300,400))
        self.SetSizer(sizer,wx.EXPAND)

        
        

    def ChooseOneItem(self,event):
        index=self.listBox.GetSelection()
        content=self.listBox.GetString(index)
        tmp=content.split(' ')

        # self.num.SetValue(tmp[0])
        if(len(tmp)>1):
            self.begintime.SetValue(tmp[1])            
        if(len(tmp)>3):
            self.endtime.SetValue(tmp[3])                                   
        ct=0
        subti=""
        for i in tmp:
            if(ct>3):
                subti=subti+' '+i;
            ct=ct+1;
        # print type(subti);
        self.TextCtrl.SetValue(subti)
        
    def SaveFile(self,event):
        file_wildcard="All files(*.*)|*.*"
        dlg=wx.FileDialog(self,"Save subtitles",
                        os.getcwd(),style=wx.SAVE,wildcard=file_wildcard)
        if(dlg.ShowModal()==wx.ID_OK):
            self.filename=dlg.GetPath()
        myfile=self.filename;
        f=open(myfile,"w");
        num=self.listBox.GetCount()

        for i in range(0,num):
            tmp=self.listBox.GetString(i);
            item=tmp.split(' ');
            f.write(str(i+1)+'\n');
            if(len(item)>3):
                f.write(item[1]+' '+item[2]+'> '+item[3]+'\n')
            ct=0
            subti=""
            for i in item:
                if(ct>4):
                    subti=subti+' '+i;
                ct=ct+1;
            csub=(subti)
            
            f.write(csub+'\n'+'\n');
        f.close()
    def SaveItem(self,event):
        # num=self.num.GetValue();
        time=self.begintime.GetValue()+' -- '+self.endtime.GetValue()
        text=self.TextCtrl.GetValue();
        res=' '+time+' '+text;
        num=self.listBox.GetSelection() 
        self.listBox.SetString(num,res)

    def Additem(self,event):
        # num=self.num.GetValue();
        time=self.begintime.GetValue()+' -- '+self.endtime.GetValue()
        text=self.TextCtrl.GetValue();
        res=' '+time+' '+text;
        num=self.listBox.GetSelection() 
        if(num==-1):
            num=0;
        ans=[];
        ans.append(res);    
        self.listBox.InsertItems(ans,num)
            
    def deleteitem(self,event):
        num=self.listBox.GetSelection();
        print num
        dd=int(num)

        self.listBox.Delete(dd);
    def SetLeft(self,event,lefttime):
        self.begintime.SetValue(lefttime)
    def SetRight(self,event,righttime):
        self.endtime.SetValue(righttime)
    def AddSub(self,event,st,et,context):
        srt=' '+st+' -- '+et+' '+context;
        #ad=srt.decode('utf-8','ignore');
        self.listBox.Append(srt);
        
    def OpenTheFile(self,event,url):
        foot=url;
        if(foot[len(foot)-1] == 't' ):
            li=SrtParser(foot)
        elif (foot[len(foot)-1]== 's'):
            li=AssParser(foot);
        self.listBox.Clear()
        for i in li:
            srt=' '+i[1]+' -- '+i[2]+' '+i[3];
            ad=srt.decode('utf-8','ignore');
            self.listBox.Append(ad);
    def OpenFile(self,event):
        file_wildcard = "All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Open subtitle file...",
                            os.getcwd(), 
                            style = wx.OPEN,
                            wildcard = file_wildcard)
        if(dlg.ShowModal() == wx.ID_OK):
            self.filename=dlg.GetPath()
        # print unicode.__doc__
        else :
            return;
        foot=self.filename

        if(foot[len(foot)-1] == 't' ):
            li=SrtParser(foot)
        elif (foot[len(foot)-1]== 's'):
            li=AssParser(foot);
        self.listBox.Clear()
        for i in li:
            srt=' '+i[1]+' -- '+i[2]+' '+i[3];
            ad=srt.decode('utf-8','ignore');
            self.listBox.Append(ad);
            # print ad;



class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        
        self.InitUI()
        
    def InitUI(self):   

        
        self.panel= Subtitle(self, -1)
        # motto.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana'))

        self.SetSize((360, 400))
        self.Centre()
        self.Show(True)


if __name__ == '__main__':
    app = wx.App(redirect=False)
    Example(None);
    app.MainLoop()
