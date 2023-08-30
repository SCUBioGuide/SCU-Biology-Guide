import tkinter
import tkinter.messagebox
from ChemicalEquation import getBalancerAnswer

class MyDialog(object): #定义对话框类
    def __init__(self, root): #对话框初始化
        self.top = tkinter.Toplevel(root) #生成TopLevel组件
        label = tkinter.Label(self.top, text='请输入待配平的化学方程式') # 生成标签组件
        label.pack()
        self.entry = tkinter.Entry(self.top,width=60) # 生成文本框组件
        self.entry.pack()
        self.entry.focus() # 文本框获得焦点
        button = tkinter.Button(self.top, text='Ok', command=self.Ok)  #生成按钮，设置按钮处理函数
        button.pack()

    def Ok(self): # 定义按钮事件处理函数
        self.input = self.entry.get()  # 获取文本框中的内容，保存为input
        self.top.destroy() #销毁对话框

    def get(self): # 返回在文本框中内容
        return getBalancerAnswer(self.input)


class MyButton(object):
    def __init__(self, root, type):
        self.root = root # 保持父窗口引用
        if type == 0: # 类不同创建不同按钮
            self.button = tkinter.Button(root, text='Run', command=self.Create)
        else:
            self.button = tkinter.Button(root, text='Quit', command=self.Quit)
        self.button.pack()

    def Create(self):
        d = MyDialog(self.root) # 生成一个对话框
        self.button.wait_window(d.top) # 等待对话框结束
        tkinter.messagebox.showinfo('结果', '配平结果:\n' + d.get()) # 输出输入值，重点语句

    def Quit(self): # 退出主窗口
        self.root.quit()


root = tkinter.Tk()
root.title("化学方程式配平")
root.geometry("500x200")
MyButton(root, 0)
MyButton(root, 1)

root.mainloop()
