/*
File: MySftpBrowser.java ; This file is part of Twister.
Version: 2.002
Copyright (C) 2012 , Luxoft

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

import javax.swing.GroupLayout.Alignment;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.JComboBox;

import java.awt.Component;

import javax.swing.DefaultListCellRenderer;
import javax.swing.ImageIcon;
import java.awt.Image;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import com.jcraft.jsch.Channel;

import javax.imageio.ImageIO;
import javax.swing.SwingConstants;
import javax.swing.ListSelectionModel;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumn;
import javax.swing.table.TableModel;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import com.jcraft.jsch.ChannelSftp;
import javax.swing.GroupLayout;
import javax.swing.LayoutStyle.ComponentPlacement;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Properties;
import java.util.TimeZone;
import java.util.Vector;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;
import java.util.Collections;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.Container;

public class MySftpBrowser extends JFrame {
	private static final long serialVersionUID = 1L;
	private JPanel main;
	private JButton cancel, open;
	private JLabel filename;
	private JScrollPane jScrollPane2;
	private JLabel look;
	private JTextField tfilename;
	private JComboBox tree;
	private ChannelSftp c;
	private JButton up;
	private JTextField text;
	private ItemListener listener;
	private Container container;
	private Image suitaicon, tcicon, upicon;
	private boolean visible;
	private Session session;
	private HashMap<Integer, String> gid = new HashMap<Integer, String>();
	private HashMap<Integer, String> uid = new HashMap<Integer, String>();
	private JCheckBox author = new JCheckBox("author");
	private JCheckBox group = new JCheckBox("group");
	private JCheckBox date = new JCheckBox("date");
	private JCheckBox size = new JCheckBox("size");
	private JTable table;

	/*
	 * c - SFTP connection initialized in repository text - the jtextfield that
	 * holds the path container - the parent for sftp browser
	 */
	public MySftpBrowser(String host, String user, String passwd,
			JTextField text, final Container container) {
		this.text = text;
		this.container = container;
		author.setSelected(true);
		group.setSelected(true);
		date.setSelected(true);
		size.setSelected(true);
		initializeSftp(user, host, passwd);
		getIcons();
		initComponents();
		add(main);
		setAlwaysOnTop(true);
		try {
			container.setEnabled(false);
		} catch (Exception e) {
			e.printStackTrace();
		}
		author.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(1);
				columnSwitch(col,author.isSelected());
			}
		});
		group.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(2);
				columnSwitch(col,group.isSelected());
			}
		});
		date.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(4);
				columnSwitch(col,date.isSelected());
			}
		});
		size.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(3);
				columnSwitch(col,size.isSelected());
			}
		});
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				try {
					container.setEnabled(true);
				} catch (Exception ex) {
					ex.printStackTrace();
				}
				visible = false;
				c.quit();
				c.disconnect();
				session.disconnect();
				dispose();
			}
		});
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setBounds(150, 150, 650, 300);
		setVisible(true);
		visible = true;
		String path;
		try {
			path = text.getText();
		} catch (Exception e) {
			path = "/";
		}
		if (path != null && !path.equals("")) {
			try {
				c.cd(path);
				populateTree();
				populateBrowser();
			} catch (Exception e) {
				e.printStackTrace();
				populateTree();
				populateBrowser();
			}
		} else {
			populateTree();
			populateBrowser();
		}
	}
	
	private void columnSwitch(TableColumn col, boolean enable){
		if(!enable){
			col.setMinWidth(0);
			col.setMaxWidth(0);
			col.setWidth(0);
		} else {
			col.setMinWidth(0);
			col.setMaxWidth(1000);
			col.setWidth(100);
			col.setPreferredWidth(100);
		}
	}

	/*
	 * read ssh stream
	 */
	private void readSSH(BufferedReader in, Channel channel) {
		try {
			String line = in.readLine();
			String[] comp;
			while (!line.endsWith("$ ")) {
				line = in.readLine();
				comp = line.split(":");
				if (comp.length == 7) {
					uid.put(new Integer(comp[2]), comp[0]);
					gid.put(new Integer(comp[3]), comp[0]);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * method to initialize sftp connection used to browse server
	 */
	private void initializeSftp(String user, String host, String passwd) {
		try {
			JSch jsch = new JSch();
			session = jsch.getSession(user, host, 22);
			session.setPassword(passwd);
			Properties config = new Properties();
			config.put("StrictHostKeyChecking", "no");
			session.setConfig(config);
			session.connect();
			Channel channel = session.openChannel("sftp");
			channel.connect();
			c = (ChannelSftp) channel;
			channel = session.openChannel("shell");
			channel.connect();
			DataInputStream dataIn = new DataInputStream(
					channel.getInputStream());
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					dataIn));
			DataOutputStream dataOut = new DataOutputStream(
					channel.getOutputStream());
			dataOut.writeBytes("cat /etc/passwd \r\n");
			dataOut.flush();
			readSSH(reader, channel);
			dataIn.close();
			dataOut.close();
			channel.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * method to initialize icons used in browser window
	 */
	private void getIcons() {
		try {
			InputStream in = getClass().getResourceAsStream("suita.png");
			suitaicon = new ImageIcon(ImageIO.read(in)).getImage();
			in = MySftpBrowser.class.getResourceAsStream("tc.png");
			tcicon = new ImageIcon(ImageIO.read(in)).getImage();
			in = MySftpBrowser.class.getResourceAsStream("up.png");
			upicon = new ImageIcon(ImageIO.read(in)).getImage();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/*
	 * method to populate the combobox that holds the tree to browse with the
	 * curent location of the sftp connection
	 */
	private void populateTree() {
		try {
			for (ItemListener it : tree.getItemListeners()) {
				tree.removeItemListener(it);
			}
			tree.removeAllItems();
			String[] home = c.pwd().split("/");
			tree.addItem("sftp://" + c.getSession().getHost() + "/");
			for (String s : home) {
				if (!s.equals("")) {
					tree.addItem(s);
				}
			}
			tree.setSelectedIndex(tree.getItemCount() - 1);
			tree.addItemListener(listener);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * method to populate the main window with files and folders according to
	 * current location of sftp connection
	 */
	private void populateBrowser() {
		try {
			DefaultTableModel model = (DefaultTableModel)table.getModel();
			model.setRowCount(0);
			Vector<LsEntry> vector1 = c.ls(".");
			Vector<LsEntry> folders = new Vector<LsEntry>();
			Vector<LsEntry> files = new Vector<LsEntry>();
			int lssize = vector1.size();
			String current;
			for (int i = 0; i < lssize; i++) {
				if (vector1.get(i).getFilename().split("\\.").length == 0) {
					continue;
				}
				try {
					current = c.pwd();
					c.cd(vector1.get(i).getFilename());
					c.cd(current);
					folders.add(vector1.get(i));
				} catch (SftpException e) {
					if (e.id == 4) {
						files.add(vector1.get(i));
					} else {
						e.printStackTrace();
					}
				}
			}
			Collections.sort(folders);
			Collections.sort(files);
			long d;
			DateFormat format = new SimpleDateFormat("yyyy.MM.dd HH:mm:ss");
			Date date;
			for (LsEntry s : folders) {
				d= s.getAttrs().getMTime();
				d*=1000;
				date = new Date(d);
				model.addRow(new Object[] {
						new MyLabel(s.getFilename(), null,
								SwingConstants.LEFT, 0),
						new MyLabel(uid.get(new Integer(s.getAttrs().getUId())), null,
								SwingConstants.LEFT, 2),
						new MyLabel(gid.get(new Integer(s.getAttrs().getGId())), null,
								SwingConstants.LEFT, 2),
						new MyLabel("", null,
								SwingConstants.LEFT, 2),
						new MyLabel(format.format(date), null,
								SwingConstants.LEFT, 2), });
			}
			for (LsEntry s : files) {
				d= s.getAttrs().getMTime();
				d*=1000;
				date = new Date(d);
				model.addRow(new Object[] {
						new MyLabel(s.getFilename(), null,
								SwingConstants.LEFT, 1),
						new MyLabel(uid.get(new Integer(s.getAttrs().getUId())), null,
								SwingConstants.LEFT, 2),
						new MyLabel(gid.get(new Integer(s.getAttrs().getGId())), null,
								SwingConstants.LEFT, 2),
						new MyLabel(s.getAttrs().getSize() + "", null,
								SwingConstants.LEFT, 2),
						new MyLabel(format.format(date), null,
								SwingConstants.LEFT, 2), });
			}
			model.fireTableDataChanged();
			table.revalidate();
			table.repaint();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public boolean isVisible() {
		return visible;
	}

	/*
	 * method to replace the jtextfield that was passed as a parameter to the
	 * constructor with the selection of the user
	 */
	public void save() {
		StringBuilder s = new StringBuilder();
		s.append("/");
		for (int i = 1; i < tree.getItemCount(); i++) {
			s.append(tree.getItemAt(i) + "/");
		}
		s.append(tfilename.getText());
		if (text != null)
			text.setText(s.toString());
	}

	/*
	 * initialization method
	 */
	private void initComponents() {
		up = new JButton(new ImageIcon(upicon));
		main = new JPanel();
		tree = new JComboBox();
		look = new JLabel();
		filename = new JLabel();
		tfilename = new JTextField();
		cancel = new JButton("Cancel");
		open = new JButton("Save");
		jScrollPane2 = new JScrollPane();
		jScrollPane2.setAlignmentX(LEFT_ALIGNMENT);

		up.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				try {
					StringBuilder s = new StringBuilder();
					s.append("/");
					for (int i = 1; i < tree.getItemCount(); i++) {
						s.append(tree.getItemAt(i) + "/");
					}
					c.cd(s.toString());
					c.cd("..");
					populateTree();
					populateBrowser();
					tfilename.setText("");
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});

		listener = new ItemListener() {
			public void itemStateChanged(ItemEvent evt) {
				if (evt.getStateChange() == ItemEvent.SELECTED) {
					try {
						int nr = tree.getSelectedIndex();
						while (tree.getItemCount() > nr + 1) {
							tree.removeItemAt(nr + 1);
						}
						StringBuilder s = new StringBuilder();
						s.append("/");
						for (int i = 1; i < tree.getItemCount(); i++) {
							s.append(tree.getItemAt(i) + "/");
						}
						c.cd(s.toString());
						populateTree();
						populateBrowser();
						tfilename.setText("");
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			}
		};

		tree.addItemListener(listener);
		look.setFont(new java.awt.Font("Tahoma", 1, 12));
		look.setText("Look in:");

		filename.setFont(new java.awt.Font("Tahoma", 1, 12));
		filename.setText("File name:");

		cancel.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				dispose();
				visible = false;
				try {
					container.setEnabled(true);
				} catch (Exception e) {}
				c.disconnect();
				session.disconnect();
			}
		});

		open.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				save();
				dispose();
				visible = false;
				try {
					container.setEnabled(true);
				} catch (Exception e) {
				}
				c.disconnect();
				session.disconnect();
			}
		});
		
		String[] columnnames = new String[] { "Name", "Author", "Group",
				"Size", "Date" };
		Object[][] data = new Object[][] {};
		DefaultTableModel model = new DefaultTableModel(data, columnnames);
		table = new JTable(model) {
			private static final long serialVersionUID = 1L;
			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		table.setAutoCreateRowSorter(true);
		table.getTableHeader().setReorderingAllowed(false);
		jScrollPane2.setViewportView(table);
		table.setDefaultRenderer(Object.class, new MyTableCellRender());
		table.setShowGrid(false);
		table.setBackground(table.getParent().getBackground());
		table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		table.addMouseListener(new MouseAdapter() {

			@Override
			public void mouseClicked(MouseEvent ev) {

				MyLabel selected = (MyLabel) table.getModel().getValueAt(
						table.rowAtPoint(ev.getPoint()),
						table.columnAtPoint(ev.getPoint()));
				if (ev.getClickCount() == 2) {
					if (selected.getType() == 0) {
						try {
							c.cd(selected.toString());
						} catch (Exception e) {
							e.printStackTrace();
						}
						for (ItemListener it : tree.getItemListeners()) {
							tree.removeItemListener(it);
						}
						tree.addItem(selected.toString());
						tree.setSelectedIndex(tree.getItemCount() - 1);
						tree.addItemListener(listener);
						populateBrowser();
						tfilename.setText("");
					} else {
						tfilename.setText(selected.toString());
						save();
						container.setEnabled(true);
						dispose();
					}
				} else {
					tfilename.setText(selected.toString());
				}

			}
		});

		GroupLayout layout = new GroupLayout(main);
		main.setLayout(layout);
		layout.setHorizontalGroup(layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addContainerGap()
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.LEADING)
												.addComponent(jScrollPane2)
												.addGroup(
														layout.createSequentialGroup()
																.addComponent(
																		filename)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		tfilename))
												.addGroup(
														GroupLayout.Alignment.TRAILING,
														layout.createSequentialGroup()
																.addGap(0,
																		0,
																		Short.MAX_VALUE)
																.addComponent(
																		open)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		cancel))
												.addGroup(
														layout.createSequentialGroup()
																.addComponent(
																		look)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		tree,
																		GroupLayout.PREFERRED_SIZE,
																		251,
																		GroupLayout.PREFERRED_SIZE)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		up, 30,
																		30, 30)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		author)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		group)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		size)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		date)
																.addGap(0,
																		105,
																		Short.MAX_VALUE)))
								.addContainerGap()));

		layout.linkSize(SwingConstants.HORIZONTAL, new Component[] { cancel,
				open });

		layout.setVerticalGroup(layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addContainerGap()
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.BASELINE)
												.addComponent(look)
												.addComponent(
														tree,
														GroupLayout.PREFERRED_SIZE,
														GroupLayout.DEFAULT_SIZE,
														GroupLayout.PREFERRED_SIZE)
												.addComponent(up, 25, 25, 25)
												.addGroup(
														layout.createSequentialGroup()
																.addGroup(
																		layout.createParallelGroup(
																				Alignment.BASELINE)
																				.addComponent(
																						author)
																				.addComponent(
																						group)
																				.addComponent(
																						size)
																				.addComponent(
																						date))))
								.addPreferredGap(ComponentPlacement.RELATED)
								.addComponent(jScrollPane2,
										GroupLayout.DEFAULT_SIZE, 165,
										Short.MAX_VALUE)
								.addPreferredGap(ComponentPlacement.RELATED)
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.BASELINE)
												.addComponent(filename)
												.addComponent(
														tfilename,
														GroupLayout.PREFERRED_SIZE,
														GroupLayout.DEFAULT_SIZE,
														GroupLayout.PREFERRED_SIZE))
								.addPreferredGap(ComponentPlacement.RELATED)
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.BASELINE)
												.addComponent(cancel)
												.addComponent(open))
								.addGap(12, 12, 12)));
	}

	/*
	 * my implementation of a DefaultListCellRenderer to represent folders and
	 * files in main browser
	 */
	class IconListRenderer extends DefaultListCellRenderer {
		private static final long serialVersionUID = 1L;
		EmptyBorder border = new EmptyBorder(2, 3, 2, 3);

		public Component getListCellRendererComponent(JList list, Object value,
				int index, boolean isSelected, boolean cellHasFocus) {
			JLabel label = (JLabel) super.getListCellRendererComponent(list,
					value, index, isSelected, cellHasFocus);
			label.setIcon(((JLabel) value).getIcon());
			label.setBorder(border);
			return label;
		}
	}

	/*
	 * my implementation of jlabel to hold the type of jlabel(folder or file)
	 * and icon
	 */
	class MyLabel extends JLabel {
		private static final long serialVersionUID = 1L;
		private int type;

		// 0 folder , 1 file , 2 text;
		public MyLabel(String text, ImageIcon icon, int i, int type) {
			super(text, icon, i);
			this.type = type;
		}

		public int getType() {
			return this.type;
		}

		public String toString() {
			return this.getText();
		}
	}

	/*
	 * my implementation of TableCellRenderer to render icons accordingly
	 * to item type
	 */
	class MyTableCellRender extends DefaultTableCellRenderer {
		private static final long serialVersionUID = 1L;

		@Override
		public Component getTableCellRendererComponent(JTable arg0,
				Object arg1, boolean arg2, boolean arg3, int arg4, int arg5) {
			JLabel label;
			if (((MyLabel) arg1).getType() == 0) {
				label = (JLabel) super.getTableCellRendererComponent(arg0,
						arg1, arg2, arg3, arg4, arg5);
				label.setIcon(new ImageIcon(suitaicon));
				if(!arg2)label.setBackground(arg0.getParent().getBackground());
				return label;
			} else if (((MyLabel) arg1).getType() == 1)	{
				label = (JLabel) super.getTableCellRendererComponent(arg0,
						arg1, arg2, arg3, arg4, arg5);
				label.setIcon(new ImageIcon(tcicon));
				if(!arg2)label.setBackground(arg0.getParent().getBackground());
				return label;
			} else{
				label = (JLabel)super.getTableCellRendererComponent(arg0,
						arg1, arg2, arg3, arg4, arg5);
				label.setIcon(null);
				if(!arg2)label.setBackground(arg0.getParent().getBackground());
				return label;
			}	
		}
	}
}