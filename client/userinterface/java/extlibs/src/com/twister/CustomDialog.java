/*
File: CustomDialog.java ; This file is part of Twister.
Version: 2.003

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package com.twister;

import java.awt.Component;

import javax.swing.BoxLayout;
import javax.swing.Icon;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.event.AncestorEvent;
import javax.swing.event.AncestorListener;

/*
 * custom dialog class
 * to implement always on top
 * 
 */
public class CustomDialog{
	
	private static JDialog dialog;
	private static long timeout;
	private static Thread timout;
	private static boolean timeoutexited = false; 
	
	public static void main(String [] args){
		
		JFrame f = new JFrame();
		f.setVisible(true);
		f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		CustomDialog.setTimeout(2000);
		CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,JOptionPane.OK_CANCEL_OPTION, f,"Input", "message").toString();
	}
	
	public static JDialog getDialog(Object message,Object[] options,int messagetype,int optionType,
            						Component parent,String title,Icon icon){
		JOptionPane pane = new JOptionPane(message, messagetype,optionType, icon, options);
		JDialog dialog = pane.createDialog(parent, title);
		dialog.setModal(true);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        return dialog;
	}

    /*
     * options presented as buttons 
     */
    public static String showButtons(Component parent, int messagetype,
                                    int optiontype, Icon icon,
                                    Object[] options, String title,String message){
        JOptionPane pane = new JOptionPane(message, messagetype, 
                                            optiontype, icon, options);
        dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        if(CustomDialog.timeout>0)CustomDialog.startTimeout();
        dialog.setVisible(true);
        if(timeoutexited){
        	timeoutexited = false;
        	return "*timeout*";
        }
        if(pane.getValue()==null){
        	CustomDialog.closeDialog();
            return "NULL";}
        else{
        	CustomDialog.closeDialog();
            return (String)pane.getValue();}}
        
    
    /*
     * used for OK, CANCEL, OPTION
     */
    public static Object showDialog(Object message,int type,int options,
                                    Component parent,String title,Icon icon){
        JOptionPane pane = new JOptionPane(message,type,options,icon);
        dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setModal(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        if(CustomDialog.timeout>0)CustomDialog.startTimeout();
        dialog.setVisible(true);
        if(timeoutexited){
        	timeoutexited = false;
        	return "*timeout*";
        }
        if(pane.getValue()==null){
        	CustomDialog.closeDialog();
            return -1;}
        else{
        	CustomDialog.closeDialog();
            return pane.getValue();}}
    
    /*
     * used for input dialog
     */
    public static String showInputDialog(int type,int options,Component parent,
                                            String title,String text){
        final  JTextField field = new JTextField();
        field.addAncestorListener(new AncestorListener() {
			
			@Override
			public void ancestorRemoved(AncestorEvent arg0) {
				// TODO Auto-generated method stub
			}
			
			@Override
			public void ancestorMoved(AncestorEvent arg0) {
				// TODO Auto-generated method stub
				
			}
			
			@Override
			public void ancestorAdded(AncestorEvent arg0) {
				field.requestFocusInWindow();
				
			}
		});
        JLabel label = new JLabel(text);
        JPanel p = new JPanel();
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        p.add(label);
        p.add(field);
        JOptionPane pane = new JOptionPane(p,type,options);
        field.setFocusable(true);
        dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        if(CustomDialog.timeout>0)CustomDialog.startTimeout();
        dialog.setVisible(true);
        if(timeoutexited){
        	timeoutexited = false;
        	return "*timeout*";
        }
        if(pane.getValue().toString().equals("uninitializedValue"))return null;
        if(pane.getValue()==null||(Integer)pane.getValue()==JOptionPane.CANCEL_OPTION){
        	CustomDialog.closeDialog();
            return null;}
        else{
        	CustomDialog.closeDialog();
            return field.getText();
        }
    }
    
    /*
     * used to show info
     */
    public static String showInfo(int type,Component parent,
                                String title,String text){
        JLabel label = new JLabel(text);
        JOptionPane pane = new JOptionPane(label,type,
                                           JOptionPane.DEFAULT_OPTION);
        dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        if(CustomDialog.timeout>0)CustomDialog.startTimeout();
        dialog.setVisible(true);
        CustomDialog.closeDialog();
        if(timeoutexited){
        	timeoutexited = false;
        	return "*timeout*";
        }
        return "true";
    }
    
    /*
     * used for dialog timeout, when timout reached, dialog gets disposed
     * return true if it was executed
     * returns false if it was not executed
     */
    public static boolean startTimeout(){
    	if(CustomDialog.timeout>0){
    		timout = new Thread(){
    			public void run(){
    				try {
    					System.out.println("starting sleep timeout for: "+timeout);
						Thread.sleep(timeout);
						CustomDialog.timeout=0;
						if(CustomDialog.dialog!=null && CustomDialog.dialog.isVisible()){
							CustomDialog.dialog.dispose();
							timeoutexited = true;
						}
					} catch (InterruptedException e) {
						CustomDialog.timeout=0;
					}
    			}
    		};
    		timout.start();
    		return true;
    	} else {
    		return false;
    	}
    }
    
    //timeout setter
    public static void setTimeout(long timeout){
    	System.out.println("setting Dialog timeout to:"+timeout);
    	CustomDialog.timeout=timeout;
    }
    
    private static void closeDialog(){
    	dialog.dispose();
    	CustomDialog.timeout=0;
    	if(timout!=null)timout.interrupt();
    }
}