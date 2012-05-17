/*
   File: DatabaseFrame.java ; This file is part of Twister.

   Copyright © 2012 , Luxoft

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

import java.awt.event.WindowEvent;
import java.awt.event.WindowAdapter;
import javax.swing.JFrame;
import javax.swing.JButton;
import javax.swing.JComboBox;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JTextField;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.tree.TreePath;
import javax.swing.tree.DefaultMutableTreeNode;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;
import javax.swing.DefaultComboBoxModel;
import java.awt.Component;
import javax.swing.JComboBox;
import javax.swing.GroupLayout;
import java.awt.FlowLayout;
import javax.swing.JTextArea;
import javax.swing.JPanel;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import javax.swing.LayoutStyle;
import java.awt.Dimension;
import java.awt.Color;
import javax.swing.BorderFactory;
import java.awt.event.WindowFocusListener;
import java.awt.event.WindowEvent;
import javax.swing.JScrollPane;

public class DatabaseFrame extends JFrame {

	private JButton ok;
	private JComboBox fieldsCombo;
	private JScrollPane scroll;
	private JTree tree;
	private DefPanel userDefinition;
	private JTextArea fileddescription;
	private String[] desc;

	public DatabaseFrame(DefPanel userDefinition) {
		setTitle(userDefinition.getDescription());
		Repository.frame.setEnabled(false);
		addWindowListener(new WindowAdapter() {

			public void windowClosing(WindowEvent e) {
				Repository.frame.setEnabled(true);
				dispose();
			}
		});
		initComponents();
		this.userDefinition = userDefinition;
	}

	private void initComponents() {
		requestFocus();
		addWindowFocusListener(new WindowFocusListener() {

			public void windowLostFocus(WindowEvent ev) {
				toFront();
			}

			public void windowGainedFocus(WindowEvent ev) {
			}
		});
		fieldsCombo = new JComboBox();
		fileddescription = new JTextArea();
		fileddescription.setEditable(false);
		ok = new JButton();

		fieldsCombo.setModel(new DefaultComboBoxModel(new String[] {}));
		fieldsCombo.setPreferredSize(new Dimension(100, 20));
		fileddescription.setBackground(new Color(240, 240, 240));
		fileddescription.setLineWrap(true);
		fileddescription.setWrapStyleWord(true);
		JScrollPane jScrollPane1 = new JScrollPane();
		jScrollPane1.setBorder(BorderFactory.createTitledBorder(
				BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)),
				"Description"));
		jScrollPane1.setViewportView(fileddescription);
		ok.setText("ok");
		javax.swing.GroupLayout layout = new javax.swing.GroupLayout(
				getContentPane());
		getContentPane().setLayout(layout);
		layout.setHorizontalGroup(layout
				.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addContainerGap()
								.addComponent(fieldsCombo,
										javax.swing.GroupLayout.PREFERRED_SIZE,
										javax.swing.GroupLayout.DEFAULT_SIZE,
										javax.swing.GroupLayout.PREFERRED_SIZE)
								.addPreferredGap(
										javax.swing.LayoutStyle.ComponentPlacement.RELATED,
										312, Short.MAX_VALUE).addComponent(ok)
								.addContainerGap())
				.addGroup(
						layout.createParallelGroup(
								javax.swing.GroupLayout.Alignment.LEADING)
								.addGroup(
										javax.swing.GroupLayout.Alignment.TRAILING,
										layout.createSequentialGroup()
												.addGap(120, 120, 120)
												.addComponent(
														jScrollPane1,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														290, Short.MAX_VALUE)
												.addGap(65, 65, 65))));
		layout.setVerticalGroup(layout
				.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addGap(19, 19, 19)
								.addGroup(
										layout.createParallelGroup(
												javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(
														fieldsCombo,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(ok))
								.addContainerGap(24, Short.MAX_VALUE))
				.addGroup(
						layout.createParallelGroup(
								javax.swing.GroupLayout.Alignment.LEADING)
								.addGroup(
										layout.createSequentialGroup()
												.addContainerGap()
												.addComponent(
														jScrollPane1,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														44, Short.MAX_VALUE)
												.addContainerGap())));
		pack();

		fieldsCombo.addItemListener(new ItemListener() {

			public void itemStateChanged(ItemEvent e) {
				if (fieldsCombo.getSelectedIndex() != -1) {
					fileddescription.setText(desc[fieldsCombo
							.getSelectedIndex()]);
				}
			}
		});

		ok.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent ev) {
				userDefinition.setParentField(
						(String) fieldsCombo.getSelectedItem(), true);
				Repository.frame.setEnabled(true);
				dispose();
			}
		});
		pack();
	}

	public void executeQuery() {
		fieldsCombo.removeAllItems();
		XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
		try {
			config.setServerURL(new URL("http://" + Repository.host + ":"
					+ Repository.getCentralEnginePort()));
		} // !!! NU uita sa updatezi portul in mesajul de eroare
		catch (Exception e) {
			System.out.println("Could not conect to " + Repository.host + " :"
					+ Repository.getCentralEnginePort());
		}
		XmlRpcClient client = new XmlRpcClient();
		client.setConfig(config);
		String query = userDefinition.getFieldID();
		;
		try {
			String result = (String) client.execute("runDBSelect",
					new Object[] { query });
			System.out.println("Query result:" + result);
			String[] fields;
			if (result.indexOf("MySQL Error") != -1) {
				fields = new String[] { "?" };
				desc = new String[] { result };
			} else {
				fields = result.split(",");
				desc = new String[fields.length];
				for (int i = 0; i < fields.length; i++) {
					if (fields[i].indexOf("|") != -1) {
						desc[i] = fields[i].substring(fields[i].indexOf("|"));
					} else {
						desc[i] = "";
					}
					fields[i] = fields[i].split("\\|")[0];
				}
			}
			fieldsCombo.setModel(new DefaultComboBoxModel(fields));
			fileddescription.setText(desc[0]);
		} catch (Exception e) {
		}
	}
}
