/*
File: UserManagement.java ; This file is part of Twister.
Version: 2.009

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

import java.applet.Applet;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.InputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.GroupLayout;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.LayoutStyle;
import javax.swing.ListSelectionModel;
import javax.swing.UIManager;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableCellRenderer;
import com.twister.CustomDialog;
import com.twister.Item;
import com.twister.plugin.twisterinterface.CommonInterface;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;

public class UserManagement implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;
	private JPanel p;
	private CommonInterface maincomp;
	private Icon back;
	private JButton editgroups, auser, ruser;
	private JPanel grouppanel, jPanel1;
	private JLabel groupslabel;
	private JList groupslist;
	private JScrollPane groupslistscroll;
	private JTable groupstable;
	private JScrollPane groupstablescroll;
	private JLabel userlabel;
	private JLabel usernamel;
	private JTextField usernamet;
	private JPanel userproppanel;
	private JScrollPane userscroll;
	private JPanel userspanel;
	private JTable usertable;
	private XmlRpcClient client;
	private JButton bckbtn;
	private JLabel timeout;
	private JTextField timeoutt;
	private Hashtable<String, String> variables;

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,
			final Document pluginsConfig, Applet applet) {
		this.variables = variables;
		System.out.println("Initializing " + getName() + " ... ");
		p = new JPanel();

		try {
			InputStream in = getClass().getResourceAsStream("back.png");
			Image im = ImageIO.read(in);
			back = new ImageIcon(im);
		} catch (Exception e) {
			e.printStackTrace();
		}
		initComponents();
		try {
			applet.removeAll();
			applet.setLayout(new BorderLayout());
			applet.add(p, BorderLayout.CENTER);
			applet.revalidate();
			applet.repaint();
		} catch (Exception e) {
			e.printStackTrace();
		}
		initializeRPC();
		populateUsersTable();
		populateGroupsList();
		populateGroups();

		System.out.println("successful");
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public void setInterface(CommonInterface arg0) {
		this.maincomp = arg0;
	}

	@Override
	public String getFileName() {
		String filename = "UserManagement.jar";
		return filename;
	}

	@Override
	public void terminate() {
		System.out.println("Terminating " + getName());
		p = null;
		maincomp = null;
		back = null;
		editgroups = null;
		auser = null;
		ruser = null;
		grouppanel = null;
		jPanel1 = null;
		groupslabel = null;
		groupslist = null;
		groupslistscroll = null;
		groupstable = null;
		groupstablescroll = null;
		userlabel = null;
		usernamel = null;
		usernamet = null;
		userproppanel = null;
		userscroll = null;
		userspanel = null;
		usertable = null;
		client = null;
		bckbtn = null;
		timeout = null;
		timeoutt = null;
		variables = null;
	}

	@Override
	public String getName() {
		String name = "UserManagement";
		return name;
	}

	public void populateUsersTable() {
		try {
			int row = usertable.getSelectedRow();
			String username = null;
			if (row != -1) {
				username = usertable.getValueAt(row, 0).toString();
			}

			HashMap<String, HashMap> hm = (HashMap<String, HashMap>) client
					.execute("usersAndGroupsManager",
							new Object[] { "list users" });
			Object[] users = hm.keySet().toArray();
			DefaultTableModel dtm = ((DefaultTableModel) usertable.getModel());
			dtm.setRowCount(0);

			for (Object ob : users) {
				Object[] ob2 = (Object[]) hm.get(ob.toString()).get("groups");
				StringBuilder sb = new StringBuilder();
				for (Object o : ob2) {
					sb.append(o.toString() + ",");
				}
				if (sb.length() > 0)
					sb.setLength(sb.length() - 1);

				ob2 = (Object[]) hm.get(ob.toString()).get("roles");
				StringBuilder sb2 = new StringBuilder();
				for (Object o : ob2) {
					sb2.append(o.toString() + ",");
				}
				if (sb2.length() > 0)
					sb2.setLength(sb2.length() - 1);

				String timeout = (String) hm.get(ob.toString()).get("timeout")
						.toString();
				dtm.addRow(new String[] { ob.toString(), timeout,
						sb.toString(), sb2.toString() });
			}
			if (username != null) {
				int rows = usertable.getRowCount();
				for (int i = 0; i < rows; i++) {
					if (username.equals(usertable.getValueAt(i, 0).toString())) {
						usertable.setRowSelectionInterval(i, i);
						break;
					}
				}
			}
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}
	}

	public void populateGroupsList() {
		try {
			HashMap<String, HashMap> hm = (HashMap<String, HashMap>) client
					.execute("usersAndGroupsManager",
							new Object[] { "list groups" });
			Object[] groups = hm.keySet().toArray();

			DefaultListModel listModel = new DefaultListModel();
			for (Object o : groups) {
				listModel.addElement(o.toString());
			}
			groupslist.setModel(listModel);
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}
	}

	/*initialize rpc connection to
	 * used to query CE for data
	 */
	public void initializeRPC() {
		try {
			XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
			configuration.setServerURL(new URL("http://"
					+ variables.get("host") + ":"
					+ variables.get("centralengineport")));
			configuration.setBasicPassword(variables.get("password"));
			configuration.setBasicUserName(variables.get("user"));
			client = new XmlRpcClient();
			client.setConfig(configuration);
			System.out.println("Client initialized: " + client);
		} catch (Exception e) {
			System.out.println("Could not conect to " + variables.get("host")
					+ " :" + variables.get("centralengineport")
					+ "for RPC client initialization");
		}
	}

	private void initComponents() {
		timeout = new JLabel("Timeout:");
		timeoutt = new JTextField();
		timeoutt.setBorder(null);
		timeoutt.addKeyListener(new KeyAdapter() {
			public void keyReleased(KeyEvent ev) {
				if (!usernamet.getText().equals("")) {
					String[] selected = new String[groupslist
							.getSelectedValuesList().size()];
					for (int i = 0; i < groupslist.getSelectedValuesList()
							.size(); i++) {
						selected[i] = groupslist.getSelectedValuesList().get(i)
								.toString();
					}
					StringBuilder sb = new StringBuilder();
					for (String st : selected) {
						sb.append(st);
						sb.append(",");
					}
					sb.setLength(sb.length() - 1);
					try {
						String st = client.execute(
								"usersAndGroupsManager",
								new Object[] { "set user", usernamet.getText(),
										sb.toString(), timeoutt.getText() })
								.toString();
						if (st.equals("true")) {
							populateUsersTable();
						}
					} catch (XmlRpcException ex) {
						ex.printStackTrace();
					}
				}

			}
		});

		jPanel1 = new JPanel();
		jPanel1.setBorder(javax.swing.BorderFactory.createLineBorder(new Color(
				153, 153, 153)));
		userspanel = new JPanel();
		userlabel = new JLabel();
		userscroll = new JScrollPane();
		userscroll.setBorder(null);
		usertable = new javax.swing.JTable() {
			private static final long serialVersionUID = 1L;

			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		usertable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		userproppanel = new JPanel();
		usernamel = new JLabel();
		usernamet = new JTextField();
		groupslabel = new JLabel();
		groupslistscroll = new JScrollPane();
		groupslist = new JList();
		grouppanel = new JPanel();
		groupstablescroll = new JScrollPane();
		groupstable = new javax.swing.JTable();
		editgroups = new javax.swing.JButton();
		auser = new javax.swing.JButton("Add User");
		auser.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				addUser();
			}
		});
		ruser = new javax.swing.JButton("Remove User");
		ruser.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				removeUser();
			}
		});
		bckbtn = new javax.swing.JButton("Control Panel", back);

		bckbtn.setMaximumSize(new java.awt.Dimension(135, 25));
		bckbtn.setMinimumSize(new java.awt.Dimension(135, 25));
		bckbtn.setPreferredSize(new java.awt.Dimension(135, 25));

		bckbtn.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				maincomp.loadComponent("ControlPanel");
			}
		});

		p.setPreferredSize(new Dimension(1024, 768));

		userspanel.setBackground(new java.awt.Color(220, 220, 220));

		userlabel.setFont(new java.awt.Font("Tahoma", 0, 18));
		userlabel.setText("Users");

		usertable.setModel(new javax.swing.table.DefaultTableModel(
				new Object[][] {}, new String[] { "User Name", "Timeout (min)",
						"User Groups", "User Roles" }) {
			public Class getColumnClass(int columnIndex) {
				return String.class;
			}
		});

		usertable.setDefaultRenderer(String.class, new MultiLineCellRenderer());
		userscroll.setViewportView(usertable);

		GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
		jPanel1.setLayout(jPanel1Layout);
		jPanel1Layout.setHorizontalGroup(jPanel1Layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						GroupLayout.Alignment.TRAILING,
						jPanel1Layout
								.createSequentialGroup()
								.addContainerGap(GroupLayout.DEFAULT_SIZE,
										Short.MAX_VALUE)
								.addComponent(auser)
								.addPreferredGap(
										LayoutStyle.ComponentPlacement.RELATED)
								.addComponent(ruser).addContainerGap())
				.addComponent(userscroll, GroupLayout.Alignment.TRAILING));
		jPanel1Layout
				.setVerticalGroup(jPanel1Layout
						.createParallelGroup(GroupLayout.Alignment.LEADING)
						.addGroup(
								GroupLayout.Alignment.TRAILING,
								jPanel1Layout
										.createSequentialGroup()
										.addComponent(userscroll,
												GroupLayout.DEFAULT_SIZE, 134,
												Short.MAX_VALUE)
										.addPreferredGap(
												LayoutStyle.ComponentPlacement.RELATED)
										.addGroup(
												jPanel1Layout
														.createParallelGroup(
																GroupLayout.Alignment.BASELINE)
														.addComponent(auser)
														.addComponent(ruser))
										.addContainerGap()));

		GroupLayout userspanelLayout = new GroupLayout(userspanel);
		userspanel.setLayout(userspanelLayout);
		userspanelLayout.setHorizontalGroup(userspanelLayout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						userspanelLayout.createSequentialGroup()
								.addComponent(userlabel)
								.addGap(0, 0, Short.MAX_VALUE))
				.addComponent(jPanel1, GroupLayout.DEFAULT_SIZE,
						GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE));
		userspanelLayout.setVerticalGroup(userspanelLayout.createParallelGroup(
				GroupLayout.Alignment.LEADING)
				.addGroup(
						userspanelLayout
								.createSequentialGroup()
								.addComponent(userlabel)
								.addPreferredGap(
										LayoutStyle.ComponentPlacement.RELATED)
								.addComponent(jPanel1,
										GroupLayout.DEFAULT_SIZE,
										GroupLayout.DEFAULT_SIZE,
										Short.MAX_VALUE)));

		userproppanel.setBorder(BorderFactory.createTitledBorder(
				BorderFactory.createLineBorder(new Color(51, 51, 51)),
				"User properties", TitledBorder.DEFAULT_JUSTIFICATION,
				TitledBorder.DEFAULT_POSITION, null, new Color(51, 51, 51)));

		usernamel.setText("User name:");

		usernamet.setEditable(false);

		groupslabel.setText("Groups");

		groupslist.setModel(new javax.swing.AbstractListModel() {
			String[] strings = { "" };

			public int getSize() {
				return strings.length;
			}

			public Object getElementAt(int i) {
				return strings[i];
			}
		});
		groupslistscroll.setViewportView(groupslist);

		GroupLayout userproppanelLayout = new GroupLayout(userproppanel);
		userproppanel.setLayout(userproppanelLayout);
		userproppanelLayout
				.setHorizontalGroup(userproppanelLayout
						.createParallelGroup(GroupLayout.Alignment.LEADING)
						.addGroup(
								userproppanelLayout
										.createSequentialGroup()
										.addContainerGap()
										.addGroup(
												userproppanelLayout
														.createParallelGroup(
																GroupLayout.Alignment.TRAILING,
																false)
														.addComponent(
																groupslistscroll)
														.addGroup(
																userproppanelLayout
																		.createParallelGroup(
																				GroupLayout.Alignment.LEADING)
																		.addComponent(
																				groupslabel)
																		.addGroup(
																				userproppanelLayout
																						.createSequentialGroup()
																						.addGroup(
																								userproppanelLayout
																										.createParallelGroup(
																												GroupLayout.Alignment.LEADING)
																										.addComponent(
																												usernamel)
																										.addComponent(
																												timeout))
																						.addPreferredGap(
																								LayoutStyle.ComponentPlacement.RELATED)
																						.addGroup(
																								userproppanelLayout
																										.createParallelGroup(
																												GroupLayout.Alignment.LEADING,
																												false)
																										.addComponent(
																												usernamet,
																												GroupLayout.DEFAULT_SIZE,
																												163,
																												Short.MAX_VALUE)
																										.addComponent(
																												timeoutt)))))
										.addContainerGap(
												GroupLayout.DEFAULT_SIZE,
												Short.MAX_VALUE)));
		userproppanelLayout
				.setVerticalGroup(userproppanelLayout
						.createParallelGroup(GroupLayout.Alignment.LEADING)
						.addGroup(
								userproppanelLayout
										.createSequentialGroup()
										.addContainerGap()
										.addGroup(
												userproppanelLayout
														.createParallelGroup(
																GroupLayout.Alignment.BASELINE)
														.addComponent(usernamel)
														.addComponent(
																usernamet,
																GroupLayout.PREFERRED_SIZE,
																GroupLayout.DEFAULT_SIZE,
																GroupLayout.PREFERRED_SIZE))
										.addPreferredGap(
												LayoutStyle.ComponentPlacement.RELATED)
										.addGroup(
												userproppanelLayout
														.createParallelGroup(
																GroupLayout.Alignment.LEADING)
														.addComponent(timeout)
														.addComponent(
																timeoutt,
																GroupLayout.PREFERRED_SIZE,
																GroupLayout.DEFAULT_SIZE,
																GroupLayout.PREFERRED_SIZE))
										.addPreferredGap(
												LayoutStyle.ComponentPlacement.UNRELATED)
										.addComponent(groupslabel)
										.addPreferredGap(
												LayoutStyle.ComponentPlacement.RELATED)
										.addComponent(groupslistscroll)
										.addContainerGap()));

		grouppanel.setBorder(BorderFactory.createTitledBorder(
				BorderFactory.createLineBorder(new Color(51, 51, 51)),
				"Groups", TitledBorder.DEFAULT_JUSTIFICATION,
				TitledBorder.DEFAULT_POSITION, null, new Color(51, 51, 51)));

		groupstable.setModel(new DefaultTableModel(new Object[][] {
				{ null, null, null, null }, { null, null, null, null } },
				new String[] { "Group Name", "Group Roles" }) {
			public Class getColumnClass(int columnIndex) {
				return String.class;
			}
		});
		groupstable.setDefaultRenderer(String.class,
				new MultiLineCellRenderer());
		groupstablescroll.setViewportView(groupstable);

		editgroups.setText("Edit Group Roles");

		GroupLayout grouppanelLayout = new GroupLayout(grouppanel);
		grouppanel.setLayout(grouppanelLayout);
		grouppanelLayout
				.setHorizontalGroup(grouppanelLayout
						.createParallelGroup(GroupLayout.Alignment.LEADING)
						.addGroup(
								GroupLayout.Alignment.TRAILING,
								grouppanelLayout
										.createSequentialGroup()
										.addContainerGap()
										.addGroup(
												grouppanelLayout
														.createParallelGroup(
																GroupLayout.Alignment.TRAILING)
														.addComponent(
																groupstablescroll)
														.addGroup(
																grouppanelLayout
																		.createSequentialGroup()
																		.addGap(0,
																				0,
																				Short.MAX_VALUE)
																		.addComponent(
																				editgroups)))
										.addContainerGap()));
		grouppanelLayout.setVerticalGroup(grouppanelLayout.createParallelGroup(
				GroupLayout.Alignment.LEADING)
				.addGroup(
						grouppanelLayout
								.createSequentialGroup()
								.addContainerGap()
								.addComponent(groupstablescroll,
										GroupLayout.PREFERRED_SIZE, 227,
										GroupLayout.PREFERRED_SIZE)
								.addPreferredGap(
										LayoutStyle.ComponentPlacement.RELATED)
								.addComponent(editgroups)
								.addContainerGap(GroupLayout.DEFAULT_SIZE,
										Short.MAX_VALUE)));

		GroupLayout layout = new GroupLayout(p);
		p.setLayout(layout);

		layout.setHorizontalGroup(layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addContainerGap()
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.LEADING)
												.addGroup(
														layout.createSequentialGroup()
																.addGroup(
																		layout.createParallelGroup(
																				GroupLayout.Alignment.LEADING)
																				.addComponent(
																						userspanel,
																						GroupLayout.DEFAULT_SIZE,
																						GroupLayout.DEFAULT_SIZE,
																						Short.MAX_VALUE)
																				.addGroup(
																						layout.createSequentialGroup()
																								.addComponent(
																										userproppanel,
																										GroupLayout.PREFERRED_SIZE,
																										GroupLayout.DEFAULT_SIZE,
																										GroupLayout.PREFERRED_SIZE)
																								.addPreferredGap(
																										LayoutStyle.ComponentPlacement.RELATED)
																								.addComponent(
																										grouppanel,
																										GroupLayout.DEFAULT_SIZE,
																										GroupLayout.DEFAULT_SIZE,
																										Short.MAX_VALUE)))
																.addContainerGap())
												.addGroup(
														GroupLayout.Alignment.TRAILING,
														layout.createSequentialGroup()
																.addGap(0,
																		0,
																		Short.MAX_VALUE)
																.addComponent(
																		bckbtn,
																		GroupLayout.PREFERRED_SIZE,
																		GroupLayout.DEFAULT_SIZE,
																		GroupLayout.PREFERRED_SIZE)
																.addGap(22, 22,
																		22)))));
		layout.setVerticalGroup(layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						GroupLayout.Alignment.TRAILING,
						layout.createSequentialGroup()
								.addContainerGap()
								.addComponent(userspanel,
										GroupLayout.DEFAULT_SIZE,
										GroupLayout.DEFAULT_SIZE,
										Short.MAX_VALUE)
								.addPreferredGap(
										LayoutStyle.ComponentPlacement.RELATED)
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.LEADING,
												false)
												.addComponent(
														userproppanel,
														GroupLayout.DEFAULT_SIZE,
														GroupLayout.DEFAULT_SIZE,
														Short.MAX_VALUE)
												.addComponent(
														grouppanel,
														GroupLayout.DEFAULT_SIZE,
														GroupLayout.DEFAULT_SIZE,
														Short.MAX_VALUE))
								.addPreferredGap(
										LayoutStyle.ComponentPlacement.UNRELATED)
								.addComponent(bckbtn,
										GroupLayout.PREFERRED_SIZE,
										GroupLayout.DEFAULT_SIZE,
										GroupLayout.PREFERRED_SIZE)
								.addGap(7, 7, 7)));

		editgroups.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				editGroup();
			}
		});

		usertable.addMouseListener(new MouseAdapter() {
			public void mouseReleased(MouseEvent ev) {
				setUser(ev);
			}
		});
	}

	private void addUser() {
		try {
			HashMap<String, HashMap> hm = (HashMap<String, HashMap>) client
					.execute("usersAndGroupsManager",
							new Object[] { "list groups" });
			Object[] resp = hm.keySet().toArray();
			String[] groups = new String[resp.length];
			for (int i = 0; i < resp.length; i++) {
				groups[i] = resp[i].toString();
			}
			new AddUser((int) auser.getLocationOnScreen().getX() - 320,
					(int) auser.getLocationOnScreen().getY() - 240, groups,
					this);
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}
	}

	public String[] getUsers() {
		Object[] resp = null;
		try {
			resp = (Object[]) client.execute("listUsers", new Object[] {});
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}
		ArrayList<String> al = new ArrayList<String>();
		int rows = usertable.getRowCount();
		boolean found;
		for (Object ob : resp) {
			found = false;
			for (int j = 0; j < rows; j++) {
				if (ob.toString().equals(usertable.getValueAt(j, 0).toString())) {
					found = true;
					break;
				}
			}
			if (!found) {
				al.add(ob.toString());
			}
		}
		String[] users = new String[al.size()];
		al.toArray(users);
		return users;
	}

	public void addUser(String username, String groups, AddUser au) {
		try {
			String st = client.execute("usersAndGroupsManager",
					new Object[] { "set user", username, groups, "01" })
					.toString();
			if (st.equals("true")) {
				populateUsersTable();
				au.dispose();
			} else {
				CustomDialog
						.showInfo(JOptionPane.ERROR_MESSAGE, p, "ERROR", st);
			}
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}

	}

	private void removeUser() {
		int row = usertable.getSelectedRow();
		if (row == -1) {
			CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, p, "Warning",
					"Please select a row from users table");
			return;
		}
		String username = usertable.getValueAt(row, 0).toString();
		try {
			String resp = client.execute("usersAndGroupsManager",
					new Object[] { "delete user", username }).toString();
			if (resp.equals("true")) {
				((DefaultTableModel) usertable.getModel()).removeRow(row);
				usernamet.setText("");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void editGroup() {
		int row = groupstable.getSelectedRow();
		if (row == -1) {
			CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, p, "Warning",
					"Please select a row from groups table");
			return;
		}
		String groupname = groupstable.getValueAt(row, 0).toString();
		String roles = groupstable.getValueAt(row, 1).toString();
		new RolesManager((int) editgroups.getLocationOnScreen().getX() - 320,
				(int) editgroups.getLocationOnScreen().getY() - 240, groupname,
				roles, client, this);
	}

	public void setUser(MouseEvent ev) {
		int row = usertable.rowAtPoint(ev.getPoint());
		String username = usertable.getValueAt(row, 0).toString();
		usernamet.setText(username);
		String timeout = usertable.getValueAt(
				usertable.rowAtPoint(ev.getPoint()), 1).toString();

		timeoutt.setText(timeout);
		String groups[] = usertable.getValueAt(row, 2).toString().split(",");

		for (ListSelectionListener l : groupslist.getListSelectionListeners()) {
			groupslist.removeListSelectionListener(l);
		}

		int[] selection = new int[groups.length];
		int size = groupslist.getModel().getSize();
		int index = 0;
		for (int x = 0; x < size; x++) {
			for (String gr : groups) {
				if (gr.equals(groupslist.getModel().getElementAt(x))) {
					selection[index] = x;
					index++;
				}
			}
		}
		groupslist.setSelectedIndices(selection);
		groupslist.addListSelectionListener(new MyListSelectionListener());
	}

	public void populateGroups() {
		try {
			HashMap<String, HashMap> hm = (HashMap<String, HashMap>) client
					.execute("usersAndGroupsManager",
							new Object[] { "list groups" });
			Object[] groups = hm.keySet().toArray();
			DefaultTableModel dtm = ((DefaultTableModel) groupstable.getModel());
			dtm.setRowCount(0);
			StringBuilder sb = new StringBuilder();
			for (Object o : groups) {
				sb.setLength(0);
				Object[] roles = (Object[]) ((HashMap) hm.get(o.toString()))
						.get("roles");
				for (Object ob : roles) {
					sb.append(ob.toString());
					sb.append(",");
				}
				if (sb.length() > 0)
					sb.setLength(sb.length() - 1);
				dtm.addRow(new String[] { o.toString(), sb.toString() });
			}
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}
	}

	class MyListSelectionListener implements ListSelectionListener {
		public void valueChanged(ListSelectionEvent evt) {
			if (!evt.getValueIsAdjusting()) {
				if (usernamet.getText().equals(""))
					return;
				JList list = (JList) evt.getSource();
				String[] selected = new String[list.getSelectedValuesList()
						.size()];
				for (int i = 0; i < list.getSelectedValuesList().size(); i++) {
					selected[i] = list.getSelectedValuesList().get(i)
							.toString();
				}
				StringBuilder sb = new StringBuilder();
				for (String st : selected) {
					sb.append(st);
					sb.append(",");
				}
				sb.setLength(sb.length() - 1);
				int resp = (Integer) CustomDialog.showDialog(new JLabel(
						"Set groups to: " + sb.toString() + "?"),
						JOptionPane.QUESTION_MESSAGE,
						JOptionPane.OK_CANCEL_OPTION, p, "Set groups!", null);
				if (resp != JOptionPane.OK_OPTION) {
					return;
				}
				try {
					String st = client.execute(
							"usersAndGroupsManager",
							new Object[] { "set user", usernamet.getText(),
									sb.toString() }).toString();
					if (st.equals("true")) {
						populateUsersTable();
					}
				} catch (XmlRpcException e) {
					e.printStackTrace();
				}

			}
		}
	}

	class MultiLineCellRenderer extends JTextArea implements TableCellRenderer {
		private List<List<Integer>> rowColHeight = new ArrayList<List<Integer>>();

		public MultiLineCellRenderer() {
			setLineWrap(true);
			setWrapStyleWord(true);
			setOpaque(true);
		}

		public Component getTableCellRendererComponent(JTable table,
				Object value, boolean isSelected, boolean hasFocus, int row,
				int column) {
			if (isSelected) {
				setForeground(table.getSelectionForeground());
				setBackground(table.getSelectionBackground());
			} else {
				setForeground(table.getForeground());
				setBackground(table.getBackground());
			}
			setFont(table.getFont());
			if (hasFocus) {
				setBorder(UIManager.getBorder("Table.focusCellHighlightBorder"));
				if (table.isCellEditable(row, column)) {
					setForeground(UIManager
							.getColor("Table.focusCellForeground"));
					setBackground(UIManager
							.getColor("Table.focusCellBackground"));
				}
			} else {
				setBorder(new EmptyBorder(1, 2, 1, 2));
			}
			setText((value == null) ? "" : value.toString());
			adjustRowHeight(table, row, column);
			return this;
		}

		private void adjustRowHeight(JTable table, int row, int column) {
			int cWidth = table.getTableHeader().getColumnModel()
					.getColumn(column).getWidth();
			setSize(new Dimension(cWidth, 1000));
			int prefH = getPreferredSize().height;
			while (rowColHeight.size() <= row) {
				rowColHeight.add(new ArrayList<Integer>(column));
			}
			List<Integer> colHeights = rowColHeight.get(row);
			while (colHeights.size() <= column) {
				colHeights.add(0);
			}
			colHeights.set(column, prefH);
			int maxH = prefH;
			for (Integer colHeight : colHeights) {
				if (colHeight > maxH) {
					maxH = colHeight;
				}
			}
			if (table.getRowHeight(row) != maxH) {
				table.setRowHeight(row, maxH);
			}
		}
	}

	public static void main(String[] args) {
		JFrame fr = new JFrame();
		fr.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		fr.setBounds(100, 100, 800, 600);
		UserManagement cp = new UserManagement();
		Hashtable ht = new Hashtable();
		ht.put("user", "tscguest");
		ht.put("password", "tscguest");
		ht.put("centralengineport", "8000");
		ht.put("host", "tsc-server");
		cp.init(null, null, ht, null, null);
		fr.add(cp.getContent());
		fr.setVisible(true);
	}

	@Override
	public String getDescription(String arg0) {
		return "";
	}

	@Override
	public void resizePlugin(int arg0, int arg1) {
	}
}