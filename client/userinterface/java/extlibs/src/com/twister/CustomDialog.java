/*
File: CustomDialog.java ; This file is part of Twister.
Version: 2.002

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

import javax.swing.JOptionPane;
import javax.swing.JDialog;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.Icon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.BoxLayout;
import javax.swing.event.AncestorEvent;
import javax.swing.event.AncestorListener;

/*
 * custom dialog class
 * to implement always on top
 * 
 */
public class CustomDialog{
	
	public static void main(String [] args){
		JFrame f = new JFrame();
		final JTextField tf = new JTextField();
		f.setVisible(true);
		f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		JButton one = new JButton("one");
		JButton two = new JButton("two");
		JButton three = new JButton("three");
		final JDialog dialog = CustomDialog.getDialog(tf,new JButton[]{one,two,three},JOptionPane.PLAIN_MESSAGE,JOptionPane.OK_CANCEL_OPTION,f,"test",null);
		dialog.addWindowListener(new WindowAdapter(){
			public void windowClosing(WindowEvent e){
				tf.setText("");
			}
		});
		one.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent e) {
				tf.setText("one");
				dialog.setVisible(false);
				dialog.dispose();
			}
		});
		two.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent e) {
				tf.setText("two");
				dialog.setVisible(false);
				dialog.dispose();
			}
		});
		three.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent e) {
				tf.setText("three");
				dialog.setVisible(false);
				dialog.dispose();
			}
		});
		dialog.setVisible(true);
		System.out.println(tf.getText());
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
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
        if(pane.getValue()==null){
            dialog.dispose();
            return "NULL";}
        else{
            dialog.dispose();
            return (String)pane.getValue();}}
        
    
    /*
     * used for OK, CANCEL, OPTION
     */
    public static Object showDialog(Object message,int type,int options,
                                    Component parent,String title,Icon icon){
        JOptionPane pane = new JOptionPane(message,type,options,icon);
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setModal(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
        if(pane.getValue()==null){
            dialog.dispose();
            return -1;}
        else{
            dialog.dispose();
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
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
        if(pane.getValue()==null||
           (Integer)pane.getValue()==JOptionPane.CANCEL_OPTION){
            dialog.dispose();
            return null;}
        else{
            dialog.dispose();
            return field.getText();
            }
        }
    
    /*
     * used to show info
     */
    public static void showInfo(int type,Component parent,
                                String title,String text){
        JLabel label = new JLabel(text);
        JOptionPane pane = new JOptionPane(label,type,
                                           JOptionPane.DEFAULT_OPTION);
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);}
    }
