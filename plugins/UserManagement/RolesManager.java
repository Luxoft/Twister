/*
File: RolesManager.java ; This file is part of Twister.
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

import javax.swing.DefaultListModel;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JPanel;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;


public class RolesManager extends JFrame {
	private static final long serialVersionUID = 1L;
	private javax.swing.JButton cancel;
    private javax.swing.JLabel groupname;
    private javax.swing.JTextField groupnamefield;
    private javax.swing.JButton ok;
    private javax.swing.JLabel rolesl;
    private javax.swing.JList roleslist;
    private javax.swing.JScrollPane roleslistscroll;
    private JPanel p = new JPanel();
    private XmlRpcClient client;
    private String roles;
    private UserManagement um;
	
	public RolesManager(int x, int y, String name,String roles, XmlRpcClient client, UserManagement um ){
		this.client = client;
		this.roles = roles;
		this.um = um;
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		initComponents();
		setVisible(true);
		setBounds(x,y,320,640);
		setAlwaysOnTop(true);
		groupnamefield.setText(name);
		populateRoleList();
	}
	
	private void initComponents() {

        groupname = new javax.swing.JLabel();
        groupnamefield = new javax.swing.JTextField();
        roleslistscroll = new javax.swing.JScrollPane();
        roleslist = new javax.swing.JList();
        rolesl = new javax.swing.JLabel();
        cancel = new javax.swing.JButton();
        ok = new javax.swing.JButton();

        p.setBorder(javax.swing.BorderFactory.createBevelBorder(javax.swing.border.BevelBorder.RAISED));

        groupname.setText("Group Name:");

        groupnamefield.setEditable(false);

        roleslist.setModel(new javax.swing.AbstractListModel() {
            String[] strings = {""};
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        roleslistscroll.setViewportView(roleslist);

        rolesl.setText("Roles:");

        cancel.setText("Cancel");

        ok.setText("Ok");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(p);
        p.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(groupname)
                            .addComponent(rolesl))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(roleslistscroll)
                            .addComponent(groupnamefield)))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGap(0, 241, Short.MAX_VALUE)
                        .addComponent(ok)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(cancel)))
                .addContainerGap())
        );

        layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {cancel, ok});

        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(groupname)
                    .addComponent(groupnamefield, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(rolesl)
                    .addComponent(roleslistscroll, javax.swing.GroupLayout.DEFAULT_SIZE, 239, Short.MAX_VALUE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(cancel)
                    .addComponent(ok))
                .addContainerGap())
        );
        add(p);
        
        cancel.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent e) {
				dispose();
			}
		});
        
        ok.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent ev) {
				JList list = roleslist;
                String [] selected = new String[list.getSelectedValuesList().size()];
                for(int i=0;i<list.getSelectedValuesList().size();i++){
                    selected[i] = list.getSelectedValuesList().get(i).toString();
                }
                StringBuilder sb = new StringBuilder();
                for(String st:selected){
                	sb.append(st);
                	sb.append(",");
                }
                if(sb.length()>0)sb.setLength(sb.length()-1);
                try {
					String st = client.execute("usersAndGroupsManager", new Object[]{"set group",groupnamefield.getText(),sb.toString()}).toString();
					if(st.equals("true")){
						um.populateGroups();
						um.populateUsersTable();
					}
                } catch (XmlRpcException e) {
					e.printStackTrace();
				}
				dispose();
			}
		});
    }
	
	public void populateRoleList(){
		try {
			Object[] st = (Object [])client.execute("usersAndGroupsManager", new Object[]{"list roles"});
			
			DefaultListModel listModel = new DefaultListModel();
			for(Object o:st){
				listModel.addElement(o.toString());
			}
			roleslist.setModel(listModel);
			
			
			String groups[] = roles.split(",");
			int[]selection = new int[groups.length];
			int size = roleslist.getModel().getSize();
			int index = 0;
			for(int x=0;x<size;x++){
				for(String gr:groups){
					if(gr.equals(roleslist.getModel().getElementAt(x))){
						selection[index] = x;
						index++;
					}
				}
			}
			roleslist.setSelectedIndices(selection);
        } catch (XmlRpcException e) {
			e.printStackTrace();
		}
	}
}
