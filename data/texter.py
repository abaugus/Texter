#!/usr/bin/env python
# Texter
# Text editor for linux platform 
# Happy Coding :)

import pygtk
import os  
import pango
import sys
pygtk.require("2.0")
import gtk
import gobject

class Texter(object):       
	
	# When our window is destroyed, we want to break out of the GTK main loop. 
    	# We do this by calling gtk_main_quit().
    	def on_window_destroy(self, widget, data = None):
    		gtk.main_quit()	
	
	# Called when user clicks the 'New' button. This will check for saving the file
	# if the file is modified and then delete the buffer and reset to default
	# status.
	def on_new_menu_activate(self, menuitem, data=None):
    		
		if self.check_for_save(): self.on_save_menu_activate(None, None)
        	
		# clear editor for a new file
        	buff = self.text_view.get_buffer()
        	buff.set_text("")
        	buff.set_modified(False)
        	self.filename = None
        	self.reset_default_status()
    	
	# Called when user clicks the 'Open' button. This lets you open a already saved file 
	# in the editor. 		
	def on_open_menu_activate(self, menuitem , data = None):	
		
		if self.check_for_save(): self.on_save_menu_activate(None, None)
		
		filename = self.get_open_filename()
        	if filename: self.load_file(filename)		

	# Called when the user clicks the 'Save' menu. We need to allow the user to choose 
    	# a file to save if it's an untitled document, and then call write_file() on that 
    	# file.
    	def on_save_menu_activate(self, menuitem, data=None):
        
        	if self.filename == None : 
        		filename = self.get_save_filename()
            		if filename: self.write_file(filename)
        		else: self.write_file(None)
	
	# Called when the user clicks the 'Save As' menu. We need to allow the user to choose 
    	# a file to save if it's an untitled document, and then call write_file() on that 
    	# file or Save the openened file with other name or directory.
    	def on_saveas_menu_activate(self, menuitem, data=None):
        
        	filename = self.get_save_filename()
            	if filename: self.write_file(filename)		
	
	# Called when the user clicks the 'Quit' menu. We need to prompt for save if 
    	# the file has been modified and then break out of the GTK+ main loop          
    	def on_quit_menu_activate(self, menuitem, data=None):
    
        	if self.check_for_save(): self.on_save_menu_activate(None, None)
        	gtk.main_quit()

	# Called when user want to cut the selected text
	def on_cut_menu_activate(self, menu2 , data = None):
		
		buff = self.text_view.get_buffer();
        	buff.cut_clipboard (gtk.clipboard_get(), True);

	# Called when user want to copy the selected text
	def on_copy_menu_activate(self, menu2 , data = None):
	
		buff = self.text_view.get_buffer();
	        buff.copy_clipboard (gtk.clipboard_get());

	# Called when user want to paste the selected text
	def on_paste_menu_activate(self, menu2 , data = None):
	
		buff = self.text_view.get_buffer();
	        buff.paste_clipboard (gtk.clipboard_get(),None, True);

	# Called when user want to delete the selected text
	def on_delete_menu_activate(self, menu2 , data = None):
		
		buff = self.text_view.get_buffer();
        	buff.delete_selection (False, True);		
	
	def add_languages(self, i):
        	self.languages.extend(i)
        	#self.emit('languages-changed')
    
    	def language_named(self, name):
        	for l in self.languages:
            		if l.name == name:
                		return l

	# Called when the user clicks 'About' 	
	def on_about_menu_activate(self,menuitem, data = None):
		
		if self.about_dialog:
			self.about_dialog.present()
			return
		
		authors =["Abhishek Bind <email@abhishekbind2013@gmail.com>"]

		about_dialog = gtk.AboutDialog()	
		about_dialog.set_transient_for(self.window)		
		about_dialog.set_program_name("Texter")
        	about_dialog.set_version("1.0")
		about_dialog.set_copyright("Copyright (c) 2015 Abhishek Bind")
        	about_dialog.set_comments("Text editor for linux platform")
        	about_dialog.set_website("https://sites.google.com/site/abhishekbind2013/")
        	about_dialog.set_logo(gtk.gdk.pixbuf_new_from_file("texter_icon.jpeg"))
        	about_dialog.run()
        	about_dialog.destroy()
	
	#def on_undo_menu_activate(self,menu3, data = None):

	#def on_redo_menu_activate(self,menu3, data = None):
	
	# This function will check to see if the text buffer has been
	# modified and prompt the user to save if it has been modified.
    	def check_for_save (self):
    
        	ret = False
        	buff = self.text_view.get_buffer()
        
        	if buff.get_modified():

            		# we need to prompt for save
            		message = "Do you want to save the changes you have made?"
            		dialog = gtk.MessageDialog(self.window,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, 
                                       message)
            		dialog.set_title("Save?")
            
            		if dialog.run() == gtk.RESPONSE_NO: ret = False
            		else: ret = True
            
            		dialog.destroy()
        
        	return ret    
    	
	# We call get_save_filename() when we want to get a filename to save from the
    	# user. It will present the user with a file chooser dialog and return the 
    	# filename or None.    
    	def get_save_filename(self):
    
        	filename = None
        	chooser = gtk.FileChooserDialog("Save File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        
        	response = chooser.run()
        	if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        	chooser.destroy()
        
        	return filename
	
	# This gets the file name which is to be open 	
	def get_open_filename(self):
		
		filename = None
		chooser = gtk.FileChooserDialog("Open File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        	response = chooser.run()
        	if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        	chooser.destroy()
        
        	return filename

	# We call load_file() when we have a filename and want to load it into the 
    	# buffer for the GtkTextView. The previous contents are overwritten.    
    	def load_file(self, filename):
    
        	# add Loading message to status bar and ensure GUI is current
       		self.statusbar.push(self.statusbar_cid, "Loading %s" % filename)
        	while gtk.events_pending(): gtk.main_iteration()
        
        	try:
            	# get the file contents
            		fin = open(filename, "r")
            		text = fin.read()
            		fin.close()
            
            		# disable the text view while loading the buffer with the text
            		self.text_view.set_sensitive(False)
            		buff = self.text_view.get_buffer()
            		buff.set_text(text)
            		buff.set_modified(False)
            		self.text_view.set_sensitive(True)
            
			# now we can set the current filename since loading was a success
			self.filename = filename
			    
		except:
			# error loading file, show message to user
			self.error_message ("Could not open file: %s" % filename)
			    
		# clear loading status and restore default 
		self.statusbar.pop(self.statusbar_cid)
		self.reset_default_status()


	# for writing in file
	def write_file(self, filename):
    
       		# add Saving message to status bar and ensure GUI is current
        	if filename: 
            		self.statusbar.push(self.statusbar_cid, "Saving %s" % filename)
        	else:
            		self.statusbar.push(self.statusbar_cid, "Saving %s" % self.filename)
            
        	while gtk.events_pending(): gtk.main_iteration()
        
        	try:
	    		# disable text view while getting contents of buffer
		    	buff = self.text_view.get_buffer()
		    	self.text_view.set_sensitive(False)
		    	text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
		    	self.text_view.set_sensitive(True)
		    	buff.set_modified(False)
		    
		    	# set the contents of the file to the text from the buffer
		    	if filename: fout = open(filename, "w")
		    	else: fout = open(self.filename, "w")
		    	fout.write(text)
		    	fout.close()
		    
		    	if filename: self.filename = filename

        	except:
            		# error writing file, show message to user
            		self.error_message ("Could not save file: %s" % filename)
        
        	# clear saving status and restore default     
		self.statusbar.pop(self.statusbar_cid)
        	self.reset_default_status()
       	
	# This prints the error message 
	def error_message(self,message):
		
		print message
		
		dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        
        	dialog.run()
       	 	dialog.destroy()
		

	# getting row and column on key press
	def on_text_view_key_press_event(self,text_view,data = None):
	        
		iter = gtk.TextIter
		mark = gtk.TextMark		
		mark = self.text_view.get_buffer().get_insert()		
		iter = self.text_view.get_buffer().get_iter_at_mark(mark)		
		row = iter.get_line()+1 		
		column =iter.get_line_offset()+1 		
		
		cursor = "Ln: "+str(row)+",Col: "+str(column)		
		self.statusbar.pop(self.statusbar_cid)
        	self.statusbar.push(self.statusbar_cid, cursor)
		
	# getting row and column on key release
	def on_text_view_key_release_event(self,text_view,data = None):
		
		iter = gtk.TextIter
		mark = gtk.TextMark		
		mark = self.text_view.get_buffer().get_insert()		
		iter = self.text_view.get_buffer().get_iter_at_mark(mark)		
		row = iter.get_line()+1 		
		column =iter.get_line_offset()+1 		
		
		cursor = "Ln: "+str(row)+",Col: "+str(column)		
		self.statusbar.pop(self.statusbar_cid)
        	self.statusbar.push(self.statusbar_cid, cursor)
		
	# reset default status    	
	def reset_default_status(self):
        
        	if self.filename: status = "File: %s" % os.path.basename(self.filename) 
        	else: status = "File: (UNTITLED)"
        
        	self.statusbar.pop(self.statusbar_cid)
        	self.statusbar.push(self.statusbar_cid, status)	
	

	# Constructor for Intialisation	
	def __init__(self):
		
		# Default values
		self.filename= None
		self.about_dialog = None
		#self.__gobject_init__()
		# Using Gtk builder to build the application from XML code which is present in "text.glade" 			
		try :			
			builder = gtk.Builder()
	    		builder.add_from_file("text.glade")
	    	except : 
			self.error_message("Unable to load XML file: text.xml")			
			sys.exit(1)
		# connects signal
		# builder.connect_signals({ "on_window_destroy" : gtk.main_quit })
		builder.connect_signals(self)
	    	
		# get the widgets which will be referenced in callbacks
        	self.window = builder.get_object("window")
        	self.statusbar = builder.get_object("statusbar")
       		self.text_view = builder.get_object("text_view")	
		
		# sets the text view background 
		self.text_view.modify_base(gtk.STATE_NORMAL,gtk.gdk.color_parse("Black"))		
		
		# sets the text view font	        
		self.text_view.modify_font(pango.FontDescription("monospace 10"))
        	
		# sets the text colour
		self.text_view.modify_text(gtk.STATE_NORMAL,gtk.gdk.color_parse("White"))		
		
		# sets the default icon to the "texter_icon.jpeg" icon
        	gtk.window_set_default_icon_name("texter_icon.jpeg")
        	
		# setup and initialize our statusbar
        	self.statusbar_cid = self.statusbar.get_context_id("statusbar")
        	self.reset_default_status()
			
		# For Syntax Highlighting
		self.language_cats = categories[:]
        	self.languages = []
        	self.add_languages(languages)
	
	# Runs the main application window 		
	def main(self):
        	self.window.show()
        	gtk.main()

if __name__ == "__main__":
	app = Texter()
	app.main()
