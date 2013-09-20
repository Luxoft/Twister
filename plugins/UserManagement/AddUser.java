/*
File: AddUser.java ; This file is part of Twister.
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
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.ListSelectionModel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import com.twister.CustomDialog;


public class AddUser extends JFrame{
	private JPanel p;
	private javax.swing.JButton add;
    private javax.swing.JButton cancel;
    private javax.swing.JScrollPane groupscroll;
    private javax.swing.JLabel groupslabel;
    private javax.swing.JList groupslist;
    private javax.swing.JLabel userslabel;
    private javax.swing.JList userslist;
    private javax.swing.JScrollPane usersscroll;
    private String [] users,groups;
    private UserManagement um;
    private javax.swing.JButton listusers;
    private javax.swing.JTextField tusername;
    private javax.swing.JLabel username;
	
	public AddUser(int x,int y,String [] groups,UserManagement um){
		this.um = um;
		this.groups = groups;
		setTitle("Add existing user to configuration");
		setVisible(true);
		setBounds(x,y,420,340);
		setAlwaysOnTop(true);
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		initComponents();
	}
	
	
	private void initComponents() {
		p = new JPanel();
		
		tusername = new javax.swing.JTextField();
        listusers = new javax.swing.JButton();
        username = new javax.swing.JLabel();
        listusers.setText("List Users");
        listusers.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				users = um.getUsers();
				userslist.setModel(new javax.swing.AbstractListModel() {
		            public int getSize() { return users.length; }
		            public Object getElementAt(int i) { return users[i]; }
		        });
				
			}
		});
        
        username.setText("Username:"); 
        
		cancel = new javax.swing.JButton();
		cancel.setText("Cancel");
        cancel.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				AddUser.this.dispose();
			}
		});
        
        add = new javax.swing.JButton();
        add.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				
				if(!tusername.getText().equals("")&&groupslist.getSelectedIndex()!=-1){
					String [] selected = new String[groupslist.getSelectedValuesList().size()];
					for(int i=0;i<groupslist.getSelectedValuesList().size();i++){
	                    selected[i] = groupslist.getSelectedValuesList().get(i).toString();
	                }
	                StringBuilder sb = new StringBuilder();
	                for(String st:selected){
	                	sb.append(st);
	                	sb.append(",");
	                }
	                sb.setLength(sb.length()-1);
					um.addUser(tusername.getText(), sb.toString(),AddUser.this);
				} else {
					CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,AddUser.this,
		                    "Warning", "Please set one user and one group");
					return;
				}
			}
		});
        userslabel = new javax.swing.JLabel();
        usersscroll = new javax.swing.JScrollPane();
        userslist = new javax.swing.JList();
        userslist.getSelectionModel().addListSelectionListener(new ListSelectionListener() {
			
			@Override
			public void valueChanged(ListSelectionEvent e) {
				tusername.setText(userslist.getSelectedValue().toString());
				
			}
		});
        groupslabel = new javax.swing.JLabel();
        groupscroll = new javax.swing.JScrollPane();
        groupslist = new javax.swing.JList();

        cancel.setText("Cancel");

        add.setText("Add");

        userslabel.setText("Available users:");
        userslist.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

        
        usersscroll.setViewportView(userslist);

        groupslabel.setText("Available groups:");

        groupslist.setModel(new javax.swing.AbstractListModel() {
            public int getSize() { return groups.length; }
            public Object getElementAt(int i) { return groups[i]; }
        });
        groupscroll.setViewportView(groupslist);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(p);
        p.setLayout(layout);
        layout.setHorizontalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(layout.createSequentialGroup()
                    .addContainerGap()
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addComponent(tusername)
                        .addGroup(layout.createSequentialGroup()
                            .addComponent(username)
                            .addGap(0, 0, Short.MAX_VALUE))
                        .addComponent(usersscroll, javax.swing.GroupLayout.DEFAULT_SIZE, 193, Short.MAX_VALUE)
                        .addGroup(layout.createSequentialGroup()
                            .addComponent(listusers)
                            .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                            .addGap(18, 18, 18)
                            .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                .addComponent(groupslabel)
                                .addComponent(groupscroll))
                            .addContainerGap())
                        .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                            .addGap(67, 67, 67)
                            .addComponent(add)
                            .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                            .addComponent(cancel)
                            .addGap(10, 10, 10))))
            );

            layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {add, cancel});

            layout.setVerticalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                    .addContainerGap()
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(groupslabel)
                        .addComponent(username))
                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                            .addComponent(tusername, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                            .addComponent(listusers)
                            .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                            .addComponent(usersscroll, javax.swing.GroupLayout.DEFAULT_SIZE, 174, Short.MAX_VALUE))
                        .addComponent(groupscroll))
                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(cancel)
                        .addComponent(add))
                    .addContainerGap())
            );
		add(p);
    }
}