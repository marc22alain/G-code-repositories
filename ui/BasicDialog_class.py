from Tkinter import *

class BasicDialog(Toplevel):
    '''
    Magic from https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    '''

    def __init__(self, parent, title = None, ok_callback=None, cancel_callback=None):
        self.ok_callback = ok_callback
        self.cancel_callback = cancel_callback

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        # self.result = None

        body = Frame(self)
        # instantiate the user input boxes
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        # instantiate the standard accept/cancel buttons
        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            print 'WTF **********'
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)


    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        assert False, 'I should not run'
        pass


    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        # validate user input
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        # do TKinter stuff ?
        self.withdraw()
        # do TKinter stuff ?
        self.update_idletasks()
        # do optional stuff
        self.apply()
        # close and stuff
        try:
            self.ok_callback()
        except AttributeError as e:
            print 'no OK function defined - AttributeError'
            print e
        except TypeError:
            print 'no OK function defined - TypeError'

        self.close()

    def cancel(self, event=None):
        try:
            self.cancel_callback()
        except AttributeError as e:
            print 'no CANCEL function defined - AttributeError'
            print e
        except TypeError:
            print 'no CANCEL function defined - TypeError'
        self.close()

    def close(self):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        '''
        Override to validate user's input
        '''
        pass # override

    def apply(self):
        '''
        Override to do stuff
        '''
        pass # override
